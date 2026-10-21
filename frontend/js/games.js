/* ===================================================================
   Belajar Lagi — Games
   Original mini games: Blok, Ular, Labirin.
   Client-side only. High scores live in localStorage.
   =================================================================== */
(function () {
  'use strict';

  const HS_PREFIX = 'bl.games.';
  const KEY_LEFT = { x: -1, y: 0 };
  const KEY_RIGHT = { x: 1, y: 0 };
  const KEY_UP = { x: 0, y: -1 };
  const KEY_DOWN = { x: 0, y: 1 };

  let cleanup = null;

  /* ---------- Shared helpers ---------- */

  function fmt(n) {
    return Number(n || 0).toLocaleString('id-ID');
  }

  function randInt(n) {
    return Math.floor(Math.random() * n);
  }

  function highScore(id) {
    try {
      return Number(localStorage.getItem(HS_PREFIX + id + '.high') || 0) || 0;
    } catch (e) {
      return 0;
    }
  }

  function saveHighScore(id, score) {
    try {
      if (score > highScore(id)) localStorage.setItem(HS_PREFIX + id + '.high', String(score));
    } catch (e) { /* private mode */ }
  }

  function visibleHighScore(id, score, el) {
    const hs = Math.max(highScore(id), score);
    if (hs > highScore(id)) saveHighScore(id, hs);
    if (el) el.textContent = hs > 0 ? 'REKOR ' + fmt(hs) : 'BELUM ADA REKOR';
    return hs;
  }

  function clockText(ms) {
    const total = Math.max(0, Math.floor(ms / 1000));
    const h = String(Math.floor(total / 3600)).padStart(2, '0');
    const m = String(Math.floor((total % 3600) / 60)).padStart(2, '0');
    const s = String(total % 60).padStart(2, '0');
    return h + ':' + m + ':' + s;
  }

  function createClock(el) {
    let base = 0;
    let since = 0;
    let timer = null;

    function draw() {
      if (el) el.textContent = clockText(base + (since ? Date.now() - since : 0));
    }

    function start() {
      if (since) return;
      since = Date.now();
      clearInterval(timer);
      timer = setInterval(draw, 250);
      draw();
    }

    function stop() {
      if (since) base += Date.now() - since;
      since = 0;
      clearInterval(timer);
      timer = null;
      draw();
    }

    function reset() {
      base = 0;
      since = 0;
      clearInterval(timer);
      timer = null;
      draw();
    }

    function dispose() {
      clearInterval(timer);
      timer = null;
      since = 0;
      base = 0;
    }

    return { start, stop, reset, dispose };
  }

  function statRow(label, id, value) {
    return `<div class="play-stat"><dt>${label}</dt><dd id="${id}">${value}</dd></div>`;
  }

  function playNav(active) {
    return `
      <nav class="play-nav" aria-label="Navigasi utama">
        <div class="play-nav-home">
          <a href="#/dashboard" class="play-brand">belajar.lagi<sup>®</sup></a>
        </div>
        <div class="play-nav-links">
          <a href="#/courses">Kelas</a>
          <a href="#/roadmap">Roadmap</a>
        </div>
        <div class="play-nav-links">
          <a href="#/progress">Progress</a>
          <a href="#/games" class="active" aria-current="page">Games</a>
        </div>
        <div class="play-nav-end">
          <a href="#/settings">Settings</a>
          <a href="#/login">Masuk</a>
        </div>
        <div class="play-nav-mobile">
          <a href="#/login">Masuk</a>
          <button class="play-menu-toggle" type="button" data-play-menu aria-expanded="false" aria-controls="play-mobile-menu">Menu</button>
        </div>
      </nav>`;
  }

  function playMobileMenu() {
    return `
      <div class="play-mobile-menu" id="play-mobile-menu" hidden>
        <button class="play-mobile-close" type="button" data-play-close>Tutup</button>
        <a href="#/dashboard">Dashboard</a>
        <a href="#/courses">Kelas</a>
        <a href="#/roadmap">Roadmap</a>
        <a href="#/progress">Progress</a>
        <a href="#/games">Games</a>
        <a href="#/settings">Settings</a>
        <a href="#/login">Masuk</a>
        <div class="play-mobile-note">Main tanpa akun. Rekor tersimpan di perangkat ini.</div>
      </div>`;
  }

  function playFooter() {
    return `
      <footer class="play-footer">
        <div class="play-footer-logo">belajar.lagi<sup>®</sup></div>
        <div class="play-footer-time" id="play-footer-time">--:--:--</div>
      </footer>`;
  }

  function bindPlayMenu(root) {
    const toggle = root.querySelector('[data-play-menu]');
    const menu = root.querySelector('#play-mobile-menu');
    const close = root.querySelector('[data-play-close]');
    if (!toggle || !menu) return () => {};

    const links = Array.from(menu.querySelectorAll('a'));

    function setOpen(open) {
      menu.hidden = !open;
      toggle.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('play-menu-open', open);
      if (open && close) close.focus({ preventScroll: true });
      if (!open) toggle.focus({ preventScroll: true });
    }

    const onToggle = (e) => {
      e.preventDefault();
      setOpen(menu.hidden);
    };
    const onClose = () => setOpen(false);
    const onLink = () => setOpen(false);
    const onKey = (e) => {
      if (e.key === 'Escape' && !menu.hidden) {
        e.preventDefault();
        setOpen(false);
      }
    };

    toggle.addEventListener('click', onToggle);
    if (close) close.addEventListener('click', onClose);
    document.addEventListener('keydown', onKey);
    links.forEach(a => a.addEventListener('click', onLink));

    let clockTimer = null;
    const timeEl = root.querySelector('#play-footer-time');
    if (timeEl) {
      const tick = () => {
        timeEl.textContent = new Date().toLocaleTimeString('id-ID', { hour12: false });
      };
      tick();
      clockTimer = setInterval(tick, 30000);
    }

    return () => {
      toggle.removeEventListener('click', onToggle);
      if (close) close.removeEventListener('click', onClose);
      document.removeEventListener('keydown', onKey);
      links.forEach(a => a.removeEventListener('click', onLink));
      clearInterval(clockTimer);
      document.body.classList.remove('play-menu-open');
    };
  }

  function stop() {
    if (cleanup) {
      const fn = cleanup;
      cleanup = null;
      try { fn(); } catch (e) { /* ignore */ }
    }
  }

  function mount(sub) {
    stop();
    const root = document.getElementById('game-root');
    if (!root) return;
    root.innerHTML = '';
    if (!sub) {
      cleanup = renderHub(root);
    } else if (sub === 'blok') {
      cleanup = createBlok(root);
    } else if (sub === 'ular') {
      cleanup = createUlar(root);
    } else if (sub === 'labirin') {
      cleanup = createLabirin(root);
    } else {
      root.innerHTML = '<div class="game-missing"><p>Permainan tidak ditemukan.</p><a class="game-btn" href="#/games">Kembali ke Games</a></div>';
    }
  }

  function shell(root, game, title, statsHtml, stageHtml, keysHtml, controlsHtml, extraHtml) {
    root.innerHTML = `
      <main class="play-main play-game-main play-${game}">
        <div class="play-game-layout">
          <aside class="play-left">
            <div>
              <h1 class="play-title">${title}</h1>
              <div class="play-best" id="${game}-high">BELUM ADA REKOR</div>
            </div>
            <div class="play-left-bottom">
              <div class="play-status desk-only" id="game-status">TEKAN SPASI UNTUK MULAI</div>
              <div class="play-status touch-only" id="game-status-touch">TEKAN TOMBOL UNTUK MULAI</div>
              <div class="play-keys desk-only">${keysHtml}</div>
            </div>
          </aside>
          <div class="play-center">
            <div class="play-board-wrap" id="game-stage">
              ${stageHtml}
              <div class="play-message" id="game-overlay" hidden></div>
            </div>
            <div class="play-touch">${controlsHtml}</div>
          </div>
          <aside class="play-right">
            <dl class="play-stats">${statsHtml}</dl>
            ${extraHtml || ''}
          </aside>
        </div>
      </main>
      ${playFooter()}`;
    return {
      stage: root.querySelector('#game-stage'),
      overlay: root.querySelector('#game-overlay'),
      status: root.querySelector('#game-status'),
    };
  }

  function showOverlay(refs, title, text, actions) {
    refs.overlay.innerHTML = `<div class="play-message-inner">
      <div class="play-message-title">${title}</div>
      ${text ? `<p class="play-message-text">${text}</p>` : ''}
      <div class="play-message-actions">${actions}</div>
    </div>`;
    refs.overlay.hidden = false;
    refs.overlay.setAttribute('role', 'dialog');
    refs.overlay.setAttribute('aria-label', title);
    if (refs.status) refs.status.textContent = title;
    refs.overlay.querySelectorAll('[data-overlay]').forEach(btn => {
      btn.addEventListener('click', () => {
        const fn = refs.actions && refs.actions[btn.dataset.overlay];
        if (fn) fn();
      });
    });
    const first = refs.overlay.querySelector('[data-overlay]');
    if (first) first.focus({ preventScroll: true });
  }

  function hideOverlay(refs) {
    refs.overlay.hidden = true;
    refs.overlay.innerHTML = '';
    refs.overlay.removeAttribute('role');
    refs.overlay.removeAttribute('aria-label');
    if (refs.status) refs.status.textContent = '';
  }

  function setActions(refs, actions) {
    refs.actions = actions;
  }

  function showStart(refs, onStart) {
    setActions(refs, { start: onStart });
    hideOverlay(refs);
    if (refs.status) refs.status.textContent = 'TEKAN SPASI UNTUK MULAI';
  }

  function bindKeys(map) {
    const handler = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      const k = e.key;
      const tag = e.target && e.target.tagName;
      if (k === ' ' && (tag === 'BUTTON' || tag === 'A' || tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT')) return;
      if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', ' '].includes(k)) e.preventDefault();
      const fn = map[k] || map[k.toLowerCase()];
      if (fn) fn(e);
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }

  function bindButtons(root, handler) {
    const buttons = Array.from(root.querySelectorAll('[data-act]'));
    const listeners = buttons.map(btn => {
      const fn = (e) => { e.preventDefault(); handler(btn.dataset.act); };
      btn.addEventListener('click', fn);
      return [btn, fn];
    });
    return () => listeners.forEach(([btn, fn]) => btn.removeEventListener('click', fn));
  }

  function bindVisibility(pauseFn) {
    const handler = () => { if (document.hidden) pauseFn(); };
    document.addEventListener('visibilitychange', handler);
    return () => document.removeEventListener('visibilitychange', handler);
  }

  function bindSwipe(el, cb) {
    let sx = 0;
    let sy = 0;
    let tracking = false;

    const start = (e) => {
      if (!e.touches || !e.touches.length) return;
      const t = e.touches[0];
      sx = t.clientX;
      sy = t.clientY;
      tracking = true;
    };

    const end = (e) => {
      if (!tracking) return;
      tracking = false;
      const t = e.changedTouches && e.changedTouches[0];
      if (!t) return;
      const dx = t.clientX - sx;
      const dy = t.clientY - sy;
      if (Math.abs(dx) < 22 && Math.abs(dy) < 22) return;
      cb(Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? 'right' : 'left') : (dy > 0 ? 'down' : 'up'));
    };

    const cancel = () => { tracking = false; };

    el.addEventListener('touchstart', start, { passive: true });
    el.addEventListener('touchend', end, { passive: true });
    el.addEventListener('touchcancel', cancel, { passive: true });
    return () => {
      el.removeEventListener('touchstart', start);
      el.removeEventListener('touchend', end);
      el.removeEventListener('touchcancel', cancel);
    };
  }

  function renderHub(root) {
    const games = [
      { id: 'blok', name: 'Blok', href: '#/games/blok' },
      { id: 'ular', name: 'Ular', href: '#/games/ular' },
      { id: 'labirin', name: 'Labirin', href: '#/games/labirin' },
    ];
    const hasScores = games.some(g => highScore(g.id) > 0);

    root.innerHTML = `
      <main class="play-main play-hub-main">
        <div class="play-hub-grid">
          <h1 class="play-hub-title">Games</h1>
          <div class="play-hub-center">
            <div class="play-hub-list" role="listbox" aria-label="Daftar permainan">
              ${games.map((g, i) => `
                <a class="play-hub-game${i === 0 ? ' selected' : ''}" href="${g.href}" role="option" aria-selected="${i === 0}" data-game="${g.id}">${g.name}</a>`).join('')}
            </div>
            <div class="play-hub-hints">Panah untuk memilih<br>Enter untuk main</div>
          </div>
          <div class="play-hub-scores">
            ${hasScores
              ? games.map(g => `<div class="play-hub-score"><span>${g.name}</span><span>${fmt(highScore(g.id))}</span></div>`).join('')
              : '<div class="play-hub-empty">Belum ada rekor</div>'}
          </div>
        </div>
      </main>
      ${playFooter()}`;

    const links = Array.from(root.querySelectorAll('.play-hub-game'));
    let selected = 0;

    function select(i, focus) {
      selected = (i + links.length) % links.length;
      links.forEach((link, n) => {
        const on = n === selected;
        link.classList.toggle('selected', on);
        link.setAttribute('aria-selected', String(on));
      });
      if (focus && links[selected]) links[selected].focus({ preventScroll: true });
    }

    const bindHover = links.map((link, i) => {
      const enter = () => select(i, false);
      const focus = () => select(i, false);
      link.addEventListener('mouseenter', enter);
      link.addEventListener('focus', focus);
      return () => {
        link.removeEventListener('mouseenter', enter);
        link.removeEventListener('focus', focus);
      };
    });

    const onKey = (e) => {
      if (e.ctrlKey || e.metaKey || e.altKey) return;
      const tag = e.target && e.target.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
        e.preventDefault();
        select(selected + 1, true);
      } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
        e.preventDefault();
        select(selected - 1, true);
      }
    };
    window.addEventListener('keydown', onKey);

    return () => {
      window.removeEventListener('keydown', onKey);
      bindHover.forEach(fn => fn());
    };
  }

  /* =================================================================
     BLOK
     ================================================================= */

  function createBlok(root) {
    const COLS = 10;
    const ROWS = 20;
    const SHAPES = {
      I: [[1, 1, 1, 1]],
      O: [[1, 1], [1, 1]],
      T: [[0, 1, 0], [1, 1, 1]],
      S: [[0, 1, 1], [1, 1, 0]],
      Z: [[1, 1, 0], [0, 1, 1]],
      J: [[1, 0, 0], [1, 1, 1]],
      L: [[0, 0, 1], [1, 1, 1]],
    };
    const SHAPE_KEYS = Object.keys(SHAPES);
    const LINE_SCORE = [0, 100, 300, 500, 800];

    const refs = shell(root, 'blok', 'Blok',
      statRow('Skor', 'blok-score', '0')
        + statRow('Level', 'blok-level', '1')
        + statRow('Baris', 'blok-lines', '0')
        + statRow('Waktu', 'blok-time', '00:00:00'),
      '<pre class="play-board game-screen" id="game-screen" aria-label="Papan Blok"></pre>',
      '← → gerak · ↑ putar<br>↓ turun · spasi jatuh<br>p jeda · r ulang',
      `<button type="button" class="game-btn" data-act="left" aria-label="Geser kiri">←</button>
       <button type="button" class="game-btn" data-act="right" aria-label="Geser kanan">→</button>
       <button type="button" class="game-btn" data-act="rot" aria-label="Putar blok">Putar</button>
       <button type="button" class="game-btn" data-act="down" aria-label="Turun">↓</button>
       <button type="button" class="game-btn" data-act="drop" aria-label="Jatuhkan">Jatuh</button>
       <button type="button" class="game-btn" data-act="pause" aria-label="Jeda">Jeda</button>`,
      `<div class="play-next-wrap"><span class="play-next-label">Berikut</span><pre class="play-next" id="game-next" aria-hidden="true"></pre></div>`);

    const screen = root.querySelector('#game-screen');
    const nextEl = root.querySelector('#game-next');
    const scoreEl = root.querySelector('#blok-score');
    const highEl = root.querySelector('#blok-high');
    const levelEl = root.querySelector('#blok-level');
    const linesEl = root.querySelector('#blok-lines');
    const clock = createClock(root.querySelector('#blok-time'));

    let board;
    let bag;
    let piece;
    let nextPiece;
    let score;
    let lines;
    let level;
    let over;
    let paused;
    let started;
    let timer;

    function emptyBoard() {
      return Array.from({ length: ROWS }, () => Array(COLS).fill(0));
    }

    function shuffledBag() {
      const a = SHAPE_KEYS.slice();
      for (let i = a.length - 1; i > 0; i--) {
        const j = randInt(i + 1);
        const tmp = a[i];
        a[i] = a[j];
        a[j] = tmp;
      }
      return a;
    }

    function pickPiece() {
      if (!bag || !bag.length) bag = shuffledBag();
      const key = bag.pop();
      return { key, shape: SHAPES[key].map(row => row.slice()) };
    }

    function collides(shape, px, py) {
      for (let y = 0; y < shape.length; y++) {
        for (let x = 0; x < shape[y].length; x++) {
          if (!shape[y][x]) continue;
          const nx = px + x;
          const ny = py + y;
          if (nx < 0 || nx >= COLS || ny >= ROWS) return true;
          if (ny >= 0 && board[ny][nx]) return true;
        }
      }
      return false;
    }

    function updateHud() {
      scoreEl.textContent = fmt(score);
      levelEl.textContent = String(level);
      linesEl.textContent = String(lines);
      visibleHighScore('blok', score, highEl);
    }

    function render() {
      const grid = board.map(row => row.slice());
      if (!over && started && piece) {
        piece.shape.forEach((row, y) => row.forEach((v, x) => {
          if (!v) return;
          const gy = piece.y + y;
          const gx = piece.x + x;
          if (gy >= 0 && gy < ROWS && gx >= 0 && gx < COLS) grid[gy][gx] = piece.key;
        }));
      }
      const linesOut = [];
      grid.forEach(row => {
        const line = row.map(v => (v ? String(v).repeat(6) : '······')).join('');
        linesOut.push(line, line);
      });
      screen.textContent = linesOut.join('\n');

      const preview = Array.from({ length: 4 }, () => Array(4).fill(0));
      const oy = Math.floor((4 - nextPiece.shape.length) / 2);
      const ox = Math.floor((4 - nextPiece.shape[0].length) / 2);
      nextPiece.shape.forEach((row, y) => row.forEach((v, x) => {
        if (v) preview[oy + y][ox + x] = 1;
      }));
      nextEl.textContent = preview.map(row => row.map(v => (v ? '##' : '  ')).join('')).join('\n');
    }

    function spawn() {
      piece = {
        key: nextPiece.key,
        shape: nextPiece.shape,
        x: Math.floor((COLS - nextPiece.shape[0].length) / 2),
        y: 0,
      };
      nextPiece = pickPiece();
      render();
      if (collides(piece.shape, piece.x, piece.y)) gameOver();
    }

    function merge() {
      piece.shape.forEach((row, y) => row.forEach((v, x) => {
        if (v && piece.y + y >= 0) board[piece.y + y][piece.x + x] = piece.key;
      }));

      let cleared = 0;
      for (let y = ROWS - 1; y >= 0; y--) {
        if (board[y].every(Boolean)) {
          board.splice(y, 1);
          board.unshift(Array(COLS).fill(0));
          cleared++;
          y++;
        }
      }

      if (cleared) {
        score += LINE_SCORE[Math.min(cleared, 4)] * level;
        lines += cleared;
        level = 1 + Math.floor(lines / 10);
      }
      updateHud();
      spawn();
    }

    function dropDelay() {
      return Math.max(110, 760 - (level - 1) * 70);
    }

    function startGame() {
      if (started || over) return;
      started = true;
      hideOverlay(refs);
      clock.start();
      schedule();
    }

    function schedule() {
      clearTimeout(timer);
      if (!started || paused || over) return;
      timer = setTimeout(() => {
        if (paused || over) return;
        if (!collides(piece.shape, piece.x, piece.y + 1)) {
          piece.y++;
          render();
          schedule();
        } else {
          merge();
          schedule();
        }
      }, dropDelay());
    }

    function move(dx) {
      if (paused || over) return;
      if (!started) startGame();
      if (!collides(piece.shape, piece.x + dx, piece.y)) {
        piece.x += dx;
        render();
      }
    }

    function rotate() {
      if (paused || over) return;
      if (!started) startGame();
      const rotated = piece.shape[0].map((_, i) => piece.shape.map(row => row[i]).reverse());
      for (const off of [0, -1, 1, -2, 2]) {
        if (!collides(rotated, piece.x + off, piece.y)) {
          piece.shape = rotated;
          piece.x += off;
          render();
          return;
        }
      }
    }

    function softDrop() {
      if (paused || over) return;
      if (!started) startGame();
      if (!collides(piece.shape, piece.x, piece.y + 1)) {
        piece.y++;
        score++;
        updateHud();
        render();
      } else {
        merge();
        schedule();
      }
    }

    function hardDrop() {
      if (paused || over) return;
      if (!started) startGame();
      let distance = 0;
      while (!collides(piece.shape, piece.x, piece.y + 1)) {
        piece.y++;
        distance++;
      }
      score += distance * 2;
      updateHud();
      merge();
      schedule();
    }

    function gameOver() {
      over = true;
      clearTimeout(timer);
      clock.stop();
      saveHighScore('blok', score);
      updateHud();
      setActions(refs, { restart: resetGame });
      showOverlay(refs, 'Selesai',
        `Skor ${fmt(score)} · ${lines} baris · level ${level}`,
        '<button type="button" class="game-btn" data-overlay="restart">Ulang</button><a class="game-btn" href="#/games">Kembali</a>');
    }

    function togglePause() {
      if (!started || over) return;
      if (paused) {
        paused = false;
        hideOverlay(refs);
        clock.start();
        schedule();
        return;
      }
      paused = true;
      clearTimeout(timer);
      clock.stop();
      setActions(refs, { resume: togglePause, restart: resetGame });
      showOverlay(refs, 'Jeda',
        'Tekan P atau tombol Lanjut untuk melanjutkan.',
        '<button type="button" class="game-btn" data-overlay="resume">Lanjut</button><button type="button" class="game-btn" data-overlay="restart">Ulang</button>');
    }

    function resetGame() {
      clearTimeout(timer);
      board = emptyBoard();
      bag = [];
      score = 0;
      lines = 0;
      level = 1;
      over = false;
      paused = false;
      started = false;
      clock.reset();
      nextPiece = pickPiece();
      updateHud();
      spawn();
      if (!over) {
        showStart(refs, startGame);
      }
    }

    const unbindKeys = bindKeys({
      ArrowLeft: () => move(-1),
      ArrowRight: () => move(1),
      ArrowUp: (e) => { if (!e.repeat) rotate(); },
      x: (e) => { if (!e.repeat) rotate(); },
      ArrowDown: () => softDrop(),
      ' ': (e) => {
        if (e.repeat) return;
        if (!started) startGame();
        else hardDrop();
      },
      p: (e) => { if (!e.repeat) togglePause(); },
      r: (e) => { if (!e.repeat) resetGame(); },
    });

    const unbindButtons = bindButtons(root, (act) => {
      if (act === 'left') move(-1);
      else if (act === 'right') move(1);
      else if (act === 'rot') rotate();
      else if (act === 'down') softDrop();
      else if (act === 'drop') hardDrop();
      else if (act === 'pause') togglePause();
    });

    const unbindSwipe = bindSwipe(refs.stage, (dir) => {
      if (dir === 'left') move(-1);
      else if (dir === 'right') move(1);
      else if (dir === 'up') rotate();
      else softDrop();
    });

    const unbindVisibility = bindVisibility(() => {
      if (started && !paused && !over) togglePause();
    });

    resetGame();

    return () => {
      clearTimeout(timer);
      clock.dispose();
      unbindKeys();
      unbindButtons();
      unbindSwipe();
      unbindVisibility();
    };
  }

  /* =================================================================
     ULAR
     ================================================================= */

  function createUlar(root) {
    const N = 20;

    const refs = shell(root, 'ular', 'Ular',
      statRow('Skor', 'ular-score', '0')
        + statRow('Panjang', 'ular-length', '3')
        + statRow('Kecepatan', 'ular-speed', '6.5')
        + statRow('Waktu', 'ular-time', '00:00:00'),
      '<pre class="play-board game-screen" id="game-screen" aria-label="Papan Ular"></pre>',
      'panah / wasd belok<br>p jeda · r ulang',
      `<button type="button" class="game-btn" data-act="up" aria-label="Atas">↑</button>
       <button type="button" class="game-btn" data-act="left" aria-label="Kiri">←</button>
       <button type="button" class="game-btn" data-act="down" aria-label="Bawah">↓</button>
       <button type="button" class="game-btn" data-act="right" aria-label="Kanan">→</button>
       <button type="button" class="game-btn" data-act="pause" aria-label="Jeda">Jeda</button>`);

    const screen = root.querySelector('#game-screen');
    const scoreEl = root.querySelector('#ular-score');
    const highEl = root.querySelector('#ular-high');
    const lengthEl = root.querySelector('#ular-length');
    const speedEl = root.querySelector('#ular-speed');
    const clock = createClock(root.querySelector('#ular-time'));

    let snake;
    let dir;
    let queue;
    let food;
    let score;
    let over;
    let paused;
    let started;
    let timer;

    function updateHud() {
      scoreEl.textContent = fmt(score);
      lengthEl.textContent = String(snake.length);
      if (speedEl) speedEl.textContent = (1000 / speed()).toFixed(1);
      visibleHighScore('ular', score, highEl);
    }

    function placeFood() {
      const free = [];
      const occupied = new Set(snake.map(s => s.x + ',' + s.y));
      for (let y = 0; y < N; y++) {
        for (let x = 0; x < N; x++) {
          if (!occupied.has(x + ',' + y)) free.push({ x, y });
        }
      }
      if (!free.length) {
        win();
        return;
      }
      food = free[randInt(free.length)];
    }

    function render() {
      const grid = Array.from({ length: N }, () => Array(N).fill(''));
      if (food) grid[food.y][food.x] = 'food';
      snake.forEach((s, i) => {
        grid[s.y][s.x] = i === 0 ? 'head' : 'body';
      });

      const lines = [];
      grid.forEach(row => {
        const line = row.map(cell => {
          if (cell === 'head') return '@@@';
          if (cell === 'body') return 'OOO';
          if (cell === 'food') return '·●·';
          let noise = '';
          for (let i = 0; i < 3; i++) noise += Math.random() < .32 ? '·' : ' ';
          return noise;
        }).join('');
        lines.push(line, line);
      });
      screen.textContent = lines.join('\n');
    }

    function speed() {
      return Math.max(70, 155 - Math.floor(score / 30) * 7);
    }

    function startGame() {
      if (started || over) return;
      started = true;
      hideOverlay(refs);
      clock.start();
      schedule();
    }

    function schedule() {
      clearTimeout(timer);
      if (!started || paused || over) return;
      timer = setTimeout(() => {
        if (paused || over) return;
        step();
        if (!paused && !over) schedule();
      }, speed());
    }

    function turn(dx, dy) {
      if (paused || over) return;
      const base = queue.length ? queue[queue.length - 1] : dir;
      if (base.x === -dx && base.y === -dy) return;
      if (base.x === dx && base.y === dy) {
        if (!started) startGame();
        return;
      }
      if (queue.length < 2) queue.push({ x: dx, y: dy });
      if (!started) startGame();
    }

    function step() {
      if (queue.length) dir = queue.shift();
      const head = { x: snake[0].x + dir.x, y: snake[0].y + dir.y };

      if (head.x < 0 || head.x >= N || head.y < 0 || head.y >= N) {
        gameOver();
        return;
      }

      const grow = food && head.x === food.x && head.y === food.y;
      const body = grow ? snake : snake.slice(0, -1);
      if (body.some(s => s.x === head.x && s.y === head.y)) {
        gameOver();
        return;
      }

      snake.unshift(head);
      if (grow) {
        score += 10;
        placeFood();
      } else {
        snake.pop();
      }
      updateHud();
      if (!over) render();
    }

    function win() {
      over = true;
      clearTimeout(timer);
      clock.stop();
      saveHighScore('ular', score);
      updateHud();
      setActions(refs, { restart: resetGame });
      showOverlay(refs, 'Papan Penuh',
        `Skor ${fmt(score)} · panjang ${snake.length}`,
        '<button type="button" class="game-btn" data-overlay="restart">Ulang</button><a class="game-btn" href="#/games">Kembali</a>');
    }

    function gameOver() {
      over = true;
      clearTimeout(timer);
      clock.stop();
      saveHighScore('ular', score);
      updateHud();
      setActions(refs, { restart: resetGame });
      showOverlay(refs, 'Selesai',
        `Skor ${fmt(score)} · panjang ${snake.length}`,
        '<button type="button" class="game-btn" data-overlay="restart">Ulang</button><a class="game-btn" href="#/games">Kembali</a>');
    }

    function togglePause() {
      if (!started || over) return;
      if (paused) {
        paused = false;
        hideOverlay(refs);
        clock.start();
        schedule();
        return;
      }
      paused = true;
      clearTimeout(timer);
      clock.stop();
      setActions(refs, { resume: togglePause, restart: resetGame });
      showOverlay(refs, 'Jeda',
        'Tekan P atau tombol Lanjut untuk melanjutkan.',
        '<button type="button" class="game-btn" data-overlay="resume">Lanjut</button><button type="button" class="game-btn" data-overlay="restart">Ulang</button>');
    }

    function resetGame() {
      clearTimeout(timer);
      snake = [{ x: 8, y: 10 }, { x: 7, y: 10 }, { x: 6, y: 10 }];
      dir = { x: 1, y: 0 };
      queue = [];
      food = null;
      score = 0;
      over = false;
      paused = false;
      started = false;
      clock.reset();
      placeFood();
      updateHud();
      render();
      if (!over) showStart(refs, startGame);
    }

    const unbindKeys = bindKeys({
      ArrowUp: () => turn(0, -1),
      ArrowDown: () => turn(0, 1),
      ArrowLeft: () => turn(-1, 0),
      ArrowRight: () => turn(1, 0),
      w: () => turn(0, -1),
      s: () => turn(0, 1),
      a: () => turn(-1, 0),
      d: () => turn(1, 0),
      ' ': (e) => { if (!e.repeat && !started) startGame(); },
      p: (e) => { if (!e.repeat) togglePause(); },
      r: (e) => { if (!e.repeat) resetGame(); },
    });

    const unbindButtons = bindButtons(root, (act) => {
      if (act === 'up') turn(0, -1);
      else if (act === 'down') turn(0, 1);
      else if (act === 'left') turn(-1, 0);
      else if (act === 'right') turn(1, 0);
      else if (act === 'pause') togglePause();
    });

    const unbindSwipe = bindSwipe(refs.stage, (dirName) => {
      if (dirName === 'up') turn(0, -1);
      else if (dirName === 'down') turn(0, 1);
      else if (dirName === 'left') turn(-1, 0);
      else turn(1, 0);
    });

    const unbindVisibility = bindVisibility(() => {
      if (started && !paused && !over) togglePause();
    });

    resetGame();

    return () => {
      clearTimeout(timer);
      clock.dispose();
      unbindKeys();
      unbindButtons();
      unbindSwipe();
      unbindVisibility();
    };
  }

  /* =================================================================
     LABIRIN
     ================================================================= */

  function createLabirin(root) {
    const MAZE = [
      '###################',
      '#........#........#',
      '#o##.###.#.###.##o#',
      '#.................#',
      '#.##.#.#####.#.##.#',
      '#....#...#...#....#',
      '####.###.#.###.####',
      '#......#...#......#',
      '#.####.#####.####.#',
      '#.#.............#.#',
      '#.#.##.## ##.##.#.#',
      '#......#...#......#',
      '####.#.#   #.#.####',
      '   #.#.# G #.#.#   ',
      '####.#.#####.#.####',
      '#........P........#',
      '#.##.###.#.###.##.#',
      '#o.#..... .....#.o#',
      '##.#.#.#####.#.#.##',
      '#....#...#...#....#',
      '###################',
    ];

    const ROWS = MAZE.length;
    const COLS = MAZE[0].length;
    const PLAYER_START = { x: 9, y: 15 };
    const GHOST_STARTS = [
      { x: 9, y: 13, glyph: 'AA', kind: 'chase' },
      { x: 8, y: 13, glyph: 'BB', kind: 'ambush' },
      { x: 10, y: 13, glyph: 'CC', kind: 'random' },
      { x: 9, y: 12, glyph: 'DD', kind: 'chase' },
    ];
    const DIRECTIONS = [KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN];

    const refs = shell(root, 'labirin', 'Labirin',
      statRow('Skor', 'lab-score', '0')
        + statRow('Nyawa', 'lab-lives', '3')
        + statRow('Pelet', 'lab-pellets', '0')
        + statRow('Waktu', 'labirin-time', '00:00:00'),
      '<pre class="play-board game-screen" id="game-screen" aria-label="Papan Labirin"></pre>',
      'panah / wasd bergerak<br>p jeda · r ulang',
      `<button type="button" class="game-btn" data-act="up" aria-label="Atas">↑</button>
       <button type="button" class="game-btn" data-act="left" aria-label="Kiri">←</button>
       <button type="button" class="game-btn" data-act="down" aria-label="Bawah">↓</button>
       <button type="button" class="game-btn" data-act="right" aria-label="Kanan">→</button>
       <button type="button" class="game-btn" data-act="pause" aria-label="Jeda">Jeda</button>`);

    const screen = root.querySelector('#game-screen');
    const scoreEl = root.querySelector('#lab-score');
    const highEl = root.querySelector('#labirin-high');
    const livesEl = root.querySelector('#lab-lives');
    const pelletsEl = root.querySelector('#lab-pellets');
    const clock = createClock(root.querySelector('#labirin-time'));

    const walls = MAZE.map(row => Array.from(row, ch => ch === '#'));
    const basePellets = MAZE.map(row => Array.from(row, ch => (ch === '.' ? 1 : ch === 'o' ? 2 : 0)));
    const initialPellets = basePellets.reduce((sum, row) => sum + row.filter(Boolean).length, 0);

    let pellets;
    let pelletsLeft;
    let player;
    let dir;
    let pendingDir;
    let ghosts;
    let score;
    let lives;
    let frightenedTicks;
    let combo;
    let over;
    let paused;
    let started;
    let tickCount;
    let timer;
    let resumeFn;

    function wrapX(x) {
      return (x + COLS) % COLS;
    }

    function walkable(x, y) {
      if (y < 0 || y >= ROWS) return false;
      return !walls[y][wrapX(x)];
    }

    function resetPellets() {
      pellets = basePellets.map(row => row.slice());
      pelletsLeft = initialPellets;
    }

    function resetActors() {
      player = { x: PLAYER_START.x, y: PLAYER_START.y };
      dir = { x: 0, y: 0 };
      pendingDir = null;
      ghosts = GHOST_STARTS.map(g => ({
        x: g.x,
        y: g.y,
        glyph: g.glyph,
        kind: g.kind,
        dir: { x: 0, y: 0 },
        eaten: 0,
      }));
      frightenedTicks = 0;
      combo = 0;
      tickCount = 0;
      resumeFn = null;
    }

    function updateHud() {
      scoreEl.textContent = fmt(score);
      livesEl.textContent = String(lives);
      pelletsEl.textContent = String(pelletsLeft);
      visibleHighScore('labirin', score, highEl);
    }

    function render() {
      const cells = Array.from({ length: ROWS }, (_, y) => (
        Array.from({ length: COLS }, (_, x) => {
          if (walls[y][x]) return ['###', '###'];
          const p = pellets[y][x];
          if (p === 2) return ['·o·', '· ·'];
          if (p === 1) return ['· ·', '· ·'];
          return ['   ', '   '];
        })
      ));

      ghosts.forEach(g => {
        if (g.eaten > 0) return;
        const glyph = frightenedTicks > 0 ? '???' : g.glyph + ' ';
        cells[g.y][g.x] = [glyph, glyph];
      });
      cells[player.y][player.x] = ['@@@', '@@@'];

      const lines = [];
      cells.forEach(row => {
        lines.push(row.map(cell => cell[0]).join(''));
        lines.push(row.map(cell => cell[1]).join(''));
      });
      screen.textContent = lines.join('\n');
    }

    function startGame(defaultDir) {
      if (started || over) return;
      started = true;
      if (defaultDir && !dir.x && !dir.y && !pendingDir) {
        pendingDir = { x: defaultDir.x, y: defaultDir.y };
      }
      hideOverlay(refs);
      clock.start();
      schedule();
    }

    function schedule() {
      clearTimeout(timer);
      if (!started || paused || over) return;
      timer = setTimeout(() => {
        if (paused || over) return;
        tickCount++;
        stepPlayer();
        if (!over && !paused) {
          checkGhostCollision();
          if (!over && !paused) {
            if (frightenedTicks > 0) frightenedTicks--;
            const ghostEvery = frightenedTicks > 0 ? 3 : 2;
            if (tickCount % ghostEvery === 0) stepGhosts();
            if (!over && !paused) render();
          }
        }
        if (!paused && !over) schedule();
      }, 115);
    }

    function stepPlayer() {
      if (pendingDir && walkable(player.x + pendingDir.x, player.y + pendingDir.y)) {
        dir = pendingDir;
        pendingDir = null;
      }
      if (!dir.x && !dir.y) return;
      if (!walkable(player.x + dir.x, player.y + dir.y)) return;

      player.x = wrapX(player.x + dir.x);
      player.y += dir.y;
      eatPellet();
    }

    function eatPellet() {
      const p = pellets[player.y][player.x];
      if (!p) return;
      pellets[player.y][player.x] = 0;
      pelletsLeft--;

      if (p === 1) {
        score += 10;
      } else {
        score += 50;
        frightenedTicks = 60;
        combo = 0;
        ghosts.forEach(g => {
          if (g.eaten === 0) g.dir = { x: -g.dir.x, y: -g.dir.y };
        });
      }

      updateHud();
      if (pelletsLeft === 0) win();
    }

    function stepGhosts() {
      ghosts.forEach(g => {
        if (g.eaten > 0) {
          g.eaten--;
          if (g.eaten === 0) {
            const start = GHOST_STARTS[ghosts.indexOf(g)];
            g.x = start.x;
            g.y = start.y;
            g.dir = { x: 0, y: 0 };
          }
          return;
        }

        const options = DIRECTIONS.filter(d => {
          if (d.x === -g.dir.x && d.y === -g.dir.y) return false;
          return walkable(g.x + d.x, g.y + d.y);
        });
        if (!options.length) {
          const fallback = DIRECTIONS.filter(d => walkable(g.x + d.x, g.y + d.y));
          if (!fallback.length) return;
          options.push(...fallback);
        }

        let choice;
        if (frightenedTicks > 0) {
          choice = options[randInt(options.length)];
        } else if (g.kind === 'random' && Math.random() < 0.5) {
          choice = options[randInt(options.length)];
        } else {
          let target = { x: player.x, y: player.y };
          if (g.kind === 'ambush' && (dir.x || dir.y)) {
            target = { x: wrapX(player.x + dir.x * 2), y: player.y + dir.y * 2 };
          }
          if (Math.random() < 0.14) {
            choice = options[randInt(options.length)];
          } else {
            let bestDistance = Infinity;
            options.forEach(d => {
              const nx = wrapX(g.x + d.x);
              const ny = g.y + d.y;
              const distance = Math.abs(nx - target.x) + Math.abs(ny - target.y);
              if (distance < bestDistance) {
                bestDistance = distance;
                choice = d;
              }
            });
          }
        }

        g.dir = choice;
        g.x = wrapX(g.x + choice.x);
        g.y += choice.y;
      });

      checkGhostCollision();
    }

    function checkGhostCollision() {
      for (const g of ghosts) {
        if (g.eaten > 0) continue;
        if (g.x !== player.x || g.y !== player.y) continue;

        if (frightenedTicks > 0) {
          score += 200 * Math.pow(2, Math.min(combo, 3));
          combo++;
          g.eaten = 24;
          updateHud();
        } else {
          loseLife();
          return;
        }
      }
    }

    function loseLife() {
      lives--;
      updateHud();
      if (lives <= 0) {
        gameOver();
        return;
      }

      paused = true;
      clearTimeout(timer);
      clock.stop();
      resumeFn = resumeRound;
      setActions(refs, { resume: () => resumeRound(), restart: resetGame });
      showOverlay(refs, 'Tertangkap',
        `Sisa nyawa: ${lives}.`,
        '<button type="button" class="game-btn" data-overlay="resume">Lanjut</button><button type="button" class="game-btn" data-overlay="restart">Ulang</button>');
    }

    function resumeRound() {
      paused = false;
      resumeFn = null;
      hideOverlay(refs);
      resetActors();
      updateHud();
      render();
      clock.start();
      schedule();
    }

    function win() {
      over = true;
      clearTimeout(timer);
      clock.stop();
      saveHighScore('labirin', score);
      updateHud();
      setActions(refs, { restart: resetGame });
      showOverlay(refs, 'Menang',
        `Semua pelet habis. Skor ${fmt(score)}.`,
        '<button type="button" class="game-btn" data-overlay="restart">Ulang</button><a class="game-btn" href="#/games">Kembali</a>');
    }

    function gameOver() {
      over = true;
      clearTimeout(timer);
      clock.stop();
      saveHighScore('labirin', score);
      updateHud();
      setActions(refs, { restart: resetGame });
      showOverlay(refs, 'Selesai',
        `Skor ${fmt(score)} · ${pelletsLeft} pelet tersisa.`,
        '<button type="button" class="game-btn" data-overlay="restart">Ulang</button><a class="game-btn" href="#/games">Kembali</a>');
    }

    function togglePause() {
      if (!started || over) return;
      if (paused) {
        const fn = resumeFn || resumeGame;
        resumeFn = null;
        fn();
        return;
      }
      paused = true;
      clearTimeout(timer);
      clock.stop();
      resumeFn = resumeGame;
      setActions(refs, { resume: togglePause, restart: resetGame });
      showOverlay(refs, 'Jeda',
        'Tekan P atau tombol Lanjut untuk melanjutkan.',
        '<button type="button" class="game-btn" data-overlay="resume">Lanjut</button><button type="button" class="game-btn" data-overlay="restart">Ulang</button>');
    }

    function resumeGame() {
      paused = false;
      hideOverlay(refs);
      clock.start();
      schedule();
    }

    function resetGame() {
      clearTimeout(timer);
      score = 0;
      lives = 3;
      over = false;
      paused = false;
      started = false;
      clock.reset();
      resetPellets();
      resetActors();
      updateHud();
      render();
      if (!over) {
        showStart(refs, () => startGame(KEY_LEFT));
      }
    }

    function setDirection(d) {
      if (paused || over) return;
      pendingDir = { x: d.x, y: d.y };
      if (!started) startGame();
    }

    const unbindKeys = bindKeys({
      ArrowUp: () => setDirection(KEY_UP),
      ArrowDown: () => setDirection(KEY_DOWN),
      ArrowLeft: () => setDirection(KEY_LEFT),
      ArrowRight: () => setDirection(KEY_RIGHT),
      w: () => setDirection(KEY_UP),
      s: () => setDirection(KEY_DOWN),
      a: () => setDirection(KEY_LEFT),
      d: () => setDirection(KEY_RIGHT),
      ' ': (e) => { if (!e.repeat && !started) startGame(KEY_LEFT); },
      p: (e) => { if (!e.repeat) togglePause(); },
      r: (e) => { if (!e.repeat) resetGame(); },
    });

    const unbindButtons = bindButtons(root, (act) => {
      if (act === 'up') setDirection(KEY_UP);
      else if (act === 'down') setDirection(KEY_DOWN);
      else if (act === 'left') setDirection(KEY_LEFT);
      else if (act === 'right') setDirection(KEY_RIGHT);
      else if (act === 'pause') togglePause();
    });

    const unbindSwipe = bindSwipe(refs.stage, (dirName) => {
      if (dirName === 'up') setDirection(KEY_UP);
      else if (dirName === 'down') setDirection(KEY_DOWN);
      else if (dirName === 'left') setDirection(KEY_LEFT);
      else setDirection(KEY_RIGHT);
    });

    const unbindVisibility = bindVisibility(() => {
      if (started && !paused && !over) togglePause();
    });

    resetGame();

    return () => {
      clearTimeout(timer);
      clock.dispose();
      unbindKeys();
      unbindButtons();
      unbindSwipe();
      unbindVisibility();
    };
  }

  window.BLGames = { mount, stop };
})();
