/* Belajar Lagi — frontend SPA */
/* Minimal markdown renderer + hash router. No frameworks. All handlers are globals. */

function esc(s) {
  return String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function renderMarkdown(md) {
  let html = '';
  const lines = (md || '').split('\n');
  let i = 0;
  let pre = false, preBuf = [];
  let ul = false, ol = false;

  const flushPre = () => {
    if (preBuf.length) { html += '<pre><code>' + esc(preBuf.join('\n')) + '</code></pre>\n'; preBuf = []; }
  };

  while (i < lines.length) {
    const line = lines[i];

    if (/^```/.test(line.trim())) {
      flushPre(); pre = !pre; if (!pre) html += '\n'; i++; continue;
    }
    if (pre) { preBuf.push(line); i++; continue; }

    if (/^<details>/.test(line.trim())) { html += '<details><summary>' + esc('Lihat jawaban') + '</summary>'; i++; continue; }
    if (/^<\/details>/.test(line.trim())) { html += '</details>\n'; i++; continue; }

    let l = line;
    const h = l.match(/^(#{1,6})\s+(.*)/);
    if (h) { const n = h[1].length; html += `<h${n}>${inline(h[2])}</h${n}>\n`; i++; continue; }
    if (/^\s*---\s*$/.test(l)) { html += '<hr>\n'; i++; continue; }

    if (/^\s*[-*]\s+/.test(l)) {
      if (!ul) { html += '<ul>\n'; ul = true; }
      html += '<li>' + inline(l.replace(/^\s*[-*]\s+/, '')) + '</li>\n';
      i++; continue;
    } else if (ul) { html += '</ul>\n'; ul = false; }

    if (/^\s*\d+\.\s+/.test(l)) {
      if (!ol) { html += '<ol>\n'; ol = true; }
      html += '<li>' + inline(l.replace(/^\s*\d+\.\s+/, '')) + '</li>\n';
      i++; continue;
    } else if (ol) { html += '</ol>\n'; ol = false; }

    if (/^\|/.test(l) && i + 1 < lines.length && /^\|[\s:|-]+\|/.test(lines[i + 1])) {
      const parseRow = (r) => r.replace(/^\||\|$/g, '').split('|').map(s => s.trim());
      const thead = parseRow(l);
      let tbl = '<table><thead><tr>' + thead.map(t => '<th>' + inline(t) + '</th>').join('') + '</tr></thead><tbody>';
      i += 2;
      while (i < lines.length && /^\|/.test(lines[i])) {
        tbl += '<tr>' + parseRow(lines[i]).map(c => '<td>' + inline(c) + '</td>').join('') + '</tr>';
        i++;
      }
      tbl += '</tbody></table>\n';
      html += tbl; continue;
    }

    if (l.trim() === '') { i++; continue; }
    html += '<p>' + inline(l) + '</p>\n';
    i++;
  }
  flushPre();
  if (ul) html += '</ul>\n';
  if (ol) html += '</ol>\n';
  return html;
}

function inline(s) {
  return esc(s)
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>');
}

async function api(path, method = 'GET', body) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } };
  if (body !== undefined) opts.body = JSON.stringify(body);
  const r = await fetch(path, opts);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

function barHtml(pct, ok) {
  return `<div class="bar ${ok ? 'ok' : ''}"><div style="width:${Math.max(0, Math.min(100, pct))}%"></div></div><div class="ghost">${Math.round(pct)}%</div>`;
}

/* ================= Pages ================= */

async function pageDashboard() {
  const d = await api('/api/dashboard');
  const btn = d.current_lesson
    ? `<a class="act" href="#/lessons/${esc(d.current_lesson.slug)}">Continue — ${esc(d.current_lesson.title)}</a>`
    : `<a class="act" href="#/roadmap">Mulai dari Roadmap</a>`;
  return `
    <h1>BELAJAR LAGI</h1>
    <h2>Overall Progress</h2>${barHtml(d.overall_pct)}
    <div class="cards">
      <div class="card"><div class="label">Current Phase</div><div class="value">${esc(d.current_phase || '—')}</div></div>
      <div class="card"><div class="label">Lessons</div><div class="value">${d.lessons_completed}/${d.lessons_total}</div></div>
      <div class="card"><div class="label">Challenges Passed</div><div class="value">${d.challenges_passed}/${d.challenges_total}</div></div>
      <div class="card"><div class="label">Streak</div><div class="value">${d.streak} hari</div></div>
      <div class="card"><div class="label">Learning Time</div><div class="value">${esc(d.learning_time)}</div></div>
    </div>
    <div class="panel">
      <h3>Continue Learning</h3>
      ${d.current_lesson ? `<p>${esc(d.current_lesson.title)}</p>` : '<p class="ghost">Belum ada lesson aktif.</p>'}
      <div class="row">${btn}</div>
    </div>
    <div class="panel"><h3>TRY FIRST · THINK BEFORE ASKING AI</h3>
      <p class="ghost">Gunakan AI untuk belajar, bukan untuk menghindar dari berpikir.</p></div>`;
}

async function pageRoadmap() {
  const tree = await api('/api/roadmap');
  let html = '<h1>Roadmap</h1>';
  for (const g of tree) {
    html += `<h3>${esc(g.name)}</h3><div class="panel">`;
    for (const t of g.topics) {
      const icon = t.status === 'completed' ? '<span class="st done">✓</span>'
        : t.status === 'current' ? '<span class="st cur">→</span>' : '<span class="st none">○</span>';
      const link = t.lesson ? `<a href="#/lessons/${esc(t.lesson)}">${esc(t.title)}</a>` : `<span class="ghost">${esc(t.title)}</span>`;
      html += `<div class="topic">${icon}<div>${link}</div></div>`;
    }
    html += '</div>';
  }
  return html;
}

async function pageLesson(slug) {
  slug = slug || 'day01';
  const l = await api(`/api/lessons/${slug}`);
  let nav = '<div class="row">';
  if (l.prev) nav += `<a href="#/lessons/${esc(l.prev.slug)}">← Previous</a>`;
  if (l.next) nav += `<a href="#/lessons/${esc(l.next.slug)}">Next →</a>`;
  nav += '</div>';
  const btn = l.completed
    ? '<p class="ghost">✓ Selesai</p>'
    : `<button class="act" onclick="actComplete('${esc(slug)}')">Mark as Complete</button>`;
  return `<h1>${esc(l.title)}</h1><div class="panel">${renderMarkdown(l.markdown)}</div>
    ${nav}<div style="height:14px"></div>${btn}`;
}

async function pageChallenges() {
  const list = await api('/api/challenges');
  return `<h1>Challenges</h1>
    <div class="ghost">Solusi tidak ditampilkan sebelum kamu mencoba sendiri.</div>
    ${list.map(c => `
      <div class="challenge"><strong>${esc(c.title)}</strong>
        <span class="badge">${esc(c.difficulty)}</span><span class="badge">${esc(c.topic || '')}</span>
        <p class="ghost">Attempts: ${c.stats.attempts || 0} · Passed: ${c.stats.passed || 0} · Hints: ${c.stats.hints || 0}</p>
        <a class="act" href="#/challenge/${esc(c.slug)}">Start Challenge</a></div>`).join('') || '<p class="ghost">Belum ada challenge.</p>'}`;
}

async function pageChallenge(slug) {
  const c = await api(`/api/challenges/${slug}`);
  return `<h1>${esc(c.title)}</h1>
    <div class="panel">${renderMarkdown(c.statement)}<p class="ghost">Tulis fungsi bernama <code>solve</code>.</p></div>
    <div class="row">
      <button class="act" onclick="actHint('${esc(c.slug)}',1)">Hint 1</button>
      <button class="act" onclick="actHint('${esc(c.slug)}',2)">Hint 2</button>
      <span class="ghost">Hints: <span id="hint-count">0</span></span>
    </div>
    <div id="hint-box"></div>
    <input type="hidden" id="hint-acc" value="0">
    <label>Kode kamu</label>
    <textarea id="ch-code" rows="12">${esc(c.starter_code)}</textarea>
    <div class="row"><button class="act" onclick="actSubmit('${esc(c.slug)}')">Run &amp; Test</button></div>
    <div id="ch-result"></div>
    <p><a href="#/challenges">← back</a></p>`;
}

async function pagePlayground() {
  return `<h1>Playground — Python</h1>
    <label>Code</label>
    <textarea id="pg-code" rows="14">numbers = [1, 2, 3]
print(sum(numbers))</textarea>
    <div class="row"><button class="act" onclick="actRun()">▶ Run</button><span class="ghost">Ctrl+Enter = run</span></div>
    <div id="pg-output" class="output">// output</div>`;
}

async function pageProjects() {
  const list = await api('/api/projects');
  return '<h1>Projects</h1>' + (list.map(p => `
    <div class="panel"><h3>${esc(p.name)}</h3>
      ${barHtml(Math.round(p.done / p.total * 100), p.done === p.total)}
      <table><tbody>${p.stages.map(s => `
        <tr><td class="${s.is_done ? 'done-task' : ''}">
          <input type="checkbox" data-proj="${esc(p.slug)}" data-task="${s.id}" ${s.is_done ? 'checked' : ''} onchange="actToggleTask(this)"> ${esc(s.title)}
        </td></tr>`).join('')}</tbody></table></div>`).join('') || '<p class="ghost">Tidak ada project.</p>');
}

async function pageNotes() {
  const list = await api('/api/notes');
  return `<h1>Notes</h1>
    <div class="panel"><label>Title</label><input id="n-title" placeholder="cth: Python Dictionary">
      <label>Content</label><textarea id="n-body" rows="5"></textarea>
      <div class="row"><button class="act" onclick="actSaveNote()">Simpan</button></div></div>
    ${list.map(n => `<div class="note-item"><strong>${esc(n.title)}</strong>
      <button class="del" onclick="actDelNote(${n.id})">hapus</button>
      <pre style="white-space:pre-wrap">${esc(n.body)}</pre><div class="ghost">${esc(n.kind)} · ${esc(n.created_at)}</div></div>`).join('')}`;
}

async function pageMistakes() {
  const list = await api('/api/mistakes');
  return `<h1>Mistake Journal</h1>
    <div class="panel">
      <label>Problem</label><input id="m-problem">
      <label>Why it happened</label><input id="m-cause">
      <label>What I learned</label><input id="m-lesson">
      <label>How to prevent it</label><input id="m-prevention">
      <div class="row"><button class="act" onclick="actSaveMistake()">Simpan</button></div></div>
    ${list.map(m => `<div class="mistake-item"><strong>${esc(m.problem)}</strong>
      <button class="del" onclick="actDelMistake(${m.id})">hapus</button>
      <div><b>Cause:</b> ${esc(m.cause)}</div><div><b>Lesson:</b> ${esc(m.lesson)}</div>
      <div><b>Prevent:</b> ${esc(m.prevention)}</div><div class="ghost">${esc(m.created_at)}</div></div>`).join('')}`;
}

async function pageProgress() {
  const p = await api('/api/progress');
  return `<h1>Progress</h1><h3>Overall</h3>${barHtml(p.overall)}
    ${p.phases.map(x => `<h3>${esc(x.phase)} (${x.done}/${x.total})</h3>${barHtml(x.pct)}`).join('')}`;
}

async function pageWeekly() {
  const d = await api('/api/dashboard');
  const p = await api('/api/progress');
  return `<h1>Weekly Review</h1>
    <div class="panel"><div><b>Lessons completed:</b> ${d.lessons_completed}/${d.lessons_total}</div>
      <div><b>Challenges passed:</b> ${d.challenges_passed}/${d.challenges_total}</div>
      <div><b>Learning time:</b> ${esc(d.learning_time)}</div><div><b>Streak:</b> ${d.streak} hari</div></div>
    <div class="panel"><h3>Progress per topik</h3>
      ${p.phases.map(x => `<div>${esc(x.phase)}: ${x.pct}%</div>`).join('')}
      <p class="ghost">Data dari database nyata.</p></div>`;
}

function pageSettings() {
  return `<h1>Settings</h1><div class="panel">
    <p>Dark mode tersimpan di browser (localStorage).</p>
    <button class="act" onclick="toggleTheme()">Toggle theme</button>
    <h3>AI Usage Policy</h3><blockquote>TRY FIRST. THINK BEFORE ASKING AI.<br>USE AI TO LEARN, NOT TO AVOID THINKING.</blockquote>
  </div>`;
}

/* ================= Actions ================= */
async function actComplete(slug) { await api(`/api/lessons/${slug}/complete`, 'POST', {}); route(); }

const hintCache = {};
async function actHint(slug, which) {
  if (!hintCache[slug]) hintCache[slug] = await api(`/api/challenges/${slug}`);
  const box = document.getElementById('hint-box');
  box.innerHTML += `<div class="hint">${esc(hintCache[slug]['hint' + which])}</div>`;
  document.getElementById('hint-acc').value = Number(document.getElementById('hint-acc').value) + 1;
  document.getElementById('hint-count').textContent = document.getElementById('hint-acc').value;
}

async function actSubmit(slug) {
  const code = document.getElementById('ch-code').value;
  const hints = Number(document.getElementById('hint-acc').value);
  const out = document.getElementById('ch-result');
  out.innerHTML = '<div class="output">running...</div>';
  try {
    const res = await api(`/api/challenges/${slug}/submit`, 'POST', { code, hints_used: hints });
    if (res.status === 'passed') {
      out.innerHTML = `<div class="output" style="color:var(--ok)">PASSED ${res.passed}/${res.total} tests</div>`;
    } else {
      const f = res.failures.map(x => '<div class="failure">Expected: ' + esc(String(x.expected)) + ' — Received: ' + esc(String(x.got)) + '</div>').join('');
      const e = res.error ? '<pre>' + esc(res.error) + '</pre>' : '';
      out.innerHTML = `<div class="output err">FAILED ${res.passed}/${res.total} tests${f}${e}</div>`;
    }
  } catch (e) { out.innerHTML = `<div class="output err">${esc(e.message)}</div>`; }
}

async function actRun() {
  const out = document.getElementById('pg-output');
  out.textContent = '...running\n';
  try {
    const res = await api('/api/playground/run', 'POST', { code: document.getElementById('pg-code').value, language: 'python' });
    out.textContent = res.status === 'ok' ? res.output : (res.error || 'error');
    out.className = 'output' + (res.status !== 'ok' ? ' err' : '');
  } catch (e) { out.textContent = 'Network error: ' + e.message; out.className = 'output err'; }
}

async function actToggleTask(input) {
  await api(`/api/projects/${input.dataset.proj}/tasks/${input.dataset.task}`, 'POST', { is_done: input.checked });
}
async function actSaveNote() { await api('/api/notes', 'POST', { title: document.getElementById('n-title').value, body: document.getElementById('n-body').value, kind: 'concept' }); route(); }
async function actDelNote(id) { await api('/api/notes/' + id, 'DELETE'); route(); }
async function actSaveMistake() {
  await api('/api/mistakes', 'POST', {
    problem: document.getElementById('m-problem').value,
    cause: document.getElementById('m-cause').value,
    lesson: document.getElementById('m-lesson').value,
    prevention: document.getElementById('m-prevention').value,
  });
  route();
}
async function actDelMistake(id) { await api('/api/mistakes/' + id, 'DELETE'); route(); }

/* ================= Router ================= */
const pageMap = {
  'dashboard': pageDashboard, 'roadmap': pageRoadmap, 'challenges': pageChallenges,
  'playground': pagePlayground, 'projects': pageProjects, 'notes': pageNotes,
  'mistakes': pageMistakes, 'progress': pageProgress, 'weekly': pageWeekly,
  'settings': pageSettings, 'bookmarks': pageSettings,
};

async function route() {
  const hash = location.hash.replace(/^#\//, '') || 'dashboard';
  const parts = hash.split('/');
  const seg = parts[0] || 'dashboard';
  const sub = parts[1];

  document.querySelectorAll('.nav-item.active').forEach(li => li.classList.remove('active'));
  const navID = seg === 'lessons' || seg === 'challenge' ? (seg === 'challenge' ? 'challenges' : seg) : seg;
  const nav = document.querySelector(`[data-nav][href^="#/${navID}"]`);
  if (nav) { nav.classList.add('active'); nav.closest('li.nav-item')?.classList.add('active'); }

  const el = document.getElementById('content');
  try {
    if (seg === 'lessons') el.innerHTML = await pageLesson(sub);
    else if (seg === 'challenge') el.innerHTML = await pageChallenge(sub);
    else if (pageMap[seg]) el.innerHTML = await pageMap[seg]();
    else el.innerHTML = '<h1>404</h1><p>Halaman tidak ditemukan.</p>';
  } catch (e) {
    el.innerHTML = `<div class="panel"><h2>Error</h2><pre>${esc(e.message)}</pre></div>`;
  }
  const titles = { dashboard: 'Dashboard', roadmap: 'Roadmap', lessons: 'Belajar', challenges: 'Challenges', playground: 'Playground', projects: 'Projects', notes: 'Notes', mistakes: 'Mistake Journal', progress: 'Progress', weekly: 'Weekly Review', settings: 'Settings' };
  const pt = document.getElementById('page-title');
  if (pt) pt.textContent = titles[seg] || 'Belajar Lagi';
  if (window.feather) feather.replace();
  window.scrollTo(0, 0);
}

/* ================= Theme ================= */
function applyTheme() {
  const t = localStorage.getItem('bl-theme') || 'light';
  document.documentElement.setAttribute('data-theme', t);
  document.body.classList.toggle('dark-layout', t === 'dark');
  document.body.classList.toggle('semi-dark-layout', false);
  const btn = document.getElementById('theme-toggle');
  if (btn) {
    const ic = btn.querySelector('i[data-feather]');
    if (ic) { ic.setAttribute('data-feather', t === 'dark' ? 'sun' : 'moon'); if (window.feather) feather.replace(); }
  }
}
function toggleTheme() {
  const t = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  localStorage.setItem('bl-theme', t);
  applyTheme();
}

/* ================= Search ================= */
function showModal(show) {
  const m = document.getElementById('search-modal');
  if (window.$ && $.fn && $.fn.modal) { $(m).modal(show ? 'show' : 'hide'); }
  else m.classList.toggle('hidden', !show);
}
function openSearch() {
  document.getElementById('search-input').value = '';
  document.getElementById('search-results').innerHTML = '';
  showModal(true);
  document.getElementById('search-input').focus();
}
function closeSearch() { showModal(false); }
async function doSearch() {
  const q = document.getElementById('search-input').value;
  const ul = document.getElementById('search-results');
  if (!q) { ul.innerHTML = ''; return; }
  const res = await api('/api/search?q=' + encodeURIComponent(q));
  ul.innerHTML = res.map(r =>
    `<li><a href="#/lessons/${esc(r.slug)}" onclick="closeSearch()">${esc(r.title)} <span class="ghost">(${esc(r.folder)})</span></a></li>`
  ).join('') || '<li class="ghost">Tidak ada hasil</li>';
}

/* ================= Bootstrap ================= */
window.addEventListener('hashchange', route);
document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
document.getElementById('search-btn').addEventListener('click', openSearch);
document.getElementById('search-input').addEventListener('input', doSearch);
const ns = document.getElementById('navbar-search');
if (ns) ns.addEventListener('input', () => { document.getElementById('search-input').value = ns.value; doSearch(); });
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); openSearch(); }
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    const inPlay = !!document.getElementById('pg-code');
    const inCh = !!document.getElementById('ch-code');
    if (inPlay) { e.preventDefault(); actRun(); }
    else if (inCh) { e.preventDefault(); actSubmit(location.hash.split('/')[2]); }
  }
  if (e.key === 'Escape') closeSearch();
});

applyTheme();
route();
