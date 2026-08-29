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
  const w = Math.max(0, Math.min(100, pct));
  const cls = ok ? 'bg-success' : 'bg-primary';
  return `<div class="d-flex justify-content-between mb-50"><span class="text-muted small"></span><span class="small fw-bolder">${Math.round(w)}%</span></div>
    <div class="progress" style="height:8px"><div class="progress-bar ${cls}" style="width:${w}%"></div></div>`;
}

function statCard(icon, color, label, value) {
  return `<div class="col-xl-2 col-md-4 col-sm-6 col-12">
    <div class="card card-statistics">
      <div class="card-body d-flex align-items-center justify-content-between">
        <div>
          <div class="text-muted text-capitalize font-small-4 mb-25">${label}</div>
          <h4 class="fw-bolder mb-0">${value}</h4>
        </div>
        <div class="avatar bg-light-${color} p-50 m-0"><div class="avatar-content"><i data-feather="${icon}" class="font-medium-3"></i></div></div>
      </div>
    </div></div>`;
}

function pageCard(title, bodyHtml, opts) {
  const h = title ? `<div class="card-header"><h4 class="card-title">${title}</h4></div>` : '';
  return `<div class="card">${h}<div class="card-body">${bodyHtml}</div></div>`;
}

function pageHeading(t) { return `<h5 class="mb-2 text-primary font-medium-5">${t}</h5>`; }

/* ================= Pages ================= */

async function pageDashboard() {
  const d = await api('/api/dashboard');
  const btn = d.current_lesson
    ? `<a class="btn btn-primary me-50" href="#/lessons/${esc(d.current_lesson.slug)}"><i data-feather="arrow-right"></i> Continue — ${esc(d.current_lesson.title)}</a>`
    : `<a class="btn btn-primary me-50" href="#/roadmap">Mulai dari Roadmap</a>`;
  return `
    ${pageCard('Overall Progress', barHtml(d.overall_pct, d.overall_pct >= 100))}
    <div class="row match-height">
      ${statCard('layers', 'primary', 'Current Phase', esc(d.current_phase || '—'))}
      ${statCard('book', 'success', 'Lessons', `${d.lessons_completed}/${d.lessons_total}`)}
      ${statCard('code', 'warning', 'Challenges', `${d.challenges_passed}/${d.challenges_total}`)}
      ${statCard('trending-up', 'danger', 'Streak', `${d.streak} hari`)}
      ${statCard('clock', 'info', 'Learning Time', esc(d.learning_time))}
    </div>
    ${pageCard('Continue Learning',
      (d.current_lesson
        ? `<p class="card-text mb-1">Lanjutkan lesson terakhir kamu: <strong>${esc(d.current_lesson.title)}</strong></p>`
        : '<p class="card-text mb-1 text-muted">Belum ada lesson aktif.</p>') + `<div class="d-flex">${btn}</div>`)}
    ${pageCard('TRY FIRST · THINK BEFORE ASKING AI',
      '<p class="mb-0 text-muted">Gunakan AI untuk belajar, bukan untuk menghindar dari berpikir.</p>')}`;
}

async function pageRoadmap() {
  const tree = await api('/api/roadmap');
  const cards = tree.map(g => {
    const rows = g.topics.map(t => {
      const dot = t.status === 'completed'
        ? '<span class="badge bg-light-success rounded-pill">✓</span>'
        : t.status === 'current' ? '<span class="badge bg-light-primary rounded-pill">→</span>'
        : '<span class="badge bg-light-secondary rounded-pill">○</span>';
      const link = t.lesson
        ? `<a href="#/lessons/${esc(t.lesson)}" class="text-body">${esc(t.title)}</a>`
        : `<span class="text-muted">${esc(t.title)}</span>`;
      const st = t.status === 'completed' ? '<span class="text-success">Selesai</span>'
        : t.status === 'current' ? '<span class="text-primary">Sedang dipelajari</span>'
        : '<span class="text-muted">Belum</span>';
      return `<div class="d-flex align-items-center py-50 border-bottom">
        <span class="me-1">${dot}</span><span class="flex-grow-1">${link}</span><small class="text-muted">${st}</small></div>`;
    }).join('');
    return `<div class="card"><div class="card-header"><h5 class="card-title mb-0">${esc(g.name)}</h5></div>
      <div class="card-body py-0">${rows}</div></div>`;
  }).join('');
  return pageHeading('Roadmap') + cards;
}

async function pageLesson(slug) {
  slug = slug || 'day01';
  const l = await api(`/api/lessons/${slug}`);
  const btn = l.completed
    ? '<span class="badge bg-light-success"><i data-feather="check"></i> Selesai</span>'
    : `<button class="btn btn-success" onclick="actComplete('${esc(slug)}')"><i data-feather="check"></i> Mark as Complete</button>`;
  const pv = l.prev ? `<a class="btn btn-outline-primary me-50" href="#/lessons/${esc(l.prev.slug)}"><i data-feather="arrow-left"></i> Previous</a>` : '';
  const nx = l.next ? `<a class="btn btn-outline-primary" href="#/lessons/${esc(l.next.slug)}">Next <i data-feather="arrow-right"></i></a>` : '';
  return `${pageHeading(esc(l.title))}
    <div class="card"><div class="card-body lesson-markdown">${renderMarkdown(l.markdown)}</div></div>
    <div class="d-flex align-items-center justify-content-between flex-wrap">
      <div>${pv ? pv + ' ' : ''}${nx}</div>
      <div>${btn}</div>
    </div>`;
}

async function pageChallenges() {
  const list = await api('/api/challenges');
  const cards = list.map(c => {
    const color = c.difficulty === 'easy' ? 'success' : c.difficulty === 'medium' ? 'warning' : 'danger';
    return `<div class="card"><div class="card-body d-flex align-items-center justify-content-between flex-wrap">
      <div>
        <h5 class="card-title mb-25">${esc(c.title)}</h5>
        <div>
          <span class="badge bg-light-${color}">${esc(c.difficulty)}</span>
          ${c.topic ? `<span class="badge bg-light-primary">${esc(c.topic)}</span>` : ''}
          <small class="text-muted d-block mt-25">Attempts: ${c.stats.attempts || 0} · Passed: ${c.stats.passed || 0} · Hints: ${c.stats.hints || 0}</small>
        </div>
      </div>
      <a class="btn btn-primary" href="#/challenge/${esc(c.slug)}">Start Challenge</a>
    </div></div>`;
  }).join('');
  return pageHeading('Challenges') +
    '<div class="alert alert-primary" role="alert">Solusi tidak ditampilkan sebelum kamu mencoba sendiri.</div>' +
    (cards || '<p class="text-muted">Belum ada challenge.</p>');
}

async function pageChallenge(slug) {
  const c = await api(`/api/challenges/${slug}`);
  return `${pageHeading(esc(c.title))}
    <div class="card"><div class="card-body lesson-markdown">${renderMarkdown(c.statement)}
      <p class="text-muted mb-0 mt-1">Tulis fungsi bernama <code>solve</code>.</p></div></div>
    <div class="d-flex align-items-center mb-1">
      <button class="btn btn-relief-primary me-50" onclick="actHint('${esc(c.slug)}',1)">Hint 1</button>
      <button class="btn btn-relief-primary me-50" onclick="actHint('${esc(c.slug)}',2)">Hint 2</button>
      <span class="text-muted">Hints: <span id="hint-count">0</span></span>
    </div>
    <div id="hint-box"></div>
    <input type="hidden" id="hint-acc" value="0">
    <div class="mb-2"><label class="form-label">Kode kamu</label>
      <textarea id="ch-code" class="form-control" rows="12" style="font-family:ui-monospace,Consolas,monospace">${esc(c.starter_code)}</textarea></div>
    <div class="d-flex align-items-center"><button class="btn btn-primary" onclick="actSubmit('${esc(c.slug)}')"><i data-feather="play"></i> Run &amp; Test</button>
      <a class="ms-1 text-muted small" href="#/challenges">← back</a></div>
    <div id="ch-result" class="mt-1"></div>`;
}

async function pagePlayground() {
  return `${pageHeading('Playground — Python')}
    <div class="card"><div class="card-body">
      <label class="form-label">Code</label>
      <textarea id="pg-code" class="form-control" rows="14" style="font-family:ui-monospace,Consolas,monospace">numbers = [1, 2, 3]
print(sum(numbers))</textarea>
      <div class="d-flex align-items-center mt-1">
        <button class="btn btn-primary" onclick="actRun()"><i data-feather="play"></i> Run</button>
        <span class="ms-1 text-muted small">Ctrl+Enter = run</span>
      </div>
      <div id="pg-output" class="output mt-1">// output</div>
    </div></div>`;
}

async function pageProjects() {
  const list = await api('/api/projects');
  const cards = list.map(p => {
    const pct = Math.round(p.done / p.total * 100);
    const rows = p.stages.map(s => {
      const cls = s.is_done ? 'done-task' : '';
      return `<tr><td class="align-middle">
        <div class="form-check"><input class="form-check-input" type="checkbox" data-proj="${esc(p.slug)}" data-task="${s.id}" ${s.is_done ? 'checked' : ''} onchange="actToggleTask(this)">
        <label class="form-check-label ${cls}">${esc(s.title)}</label></div></td></tr>`;
    }).join('');
    return `<div class="card"><div class="card-header"><h5 class="card-title mb-0">${esc(p.name)}</h5>
      <small class="text-muted">${p.done}/${p.total}</small></div>
      <div class="card-body">${barHtml(pct, p.done === p.total)}
        <div class="table-responsive mt-1"><table class="table table-hover mb-0"><tbody>${rows}</tbody></table></div>
      </div></div>`;
  }).join('');
  return pageHeading('Projects') + (cards || '<p class="text-muted">Tidak ada project.</p>');
}

async function pageNotes() {
  const list = await api('/api/notes');
  const items = list.map(n => `
    <div class="card"><div class="card-body">
      <div class="d-flex align-items-center justify-content-between">
        <h6 class="card-title mb-1">${esc(n.title)}</h6>
        <button class="btn btn-icon btn-outline-danger btn-sm" onclick="actDelNote(${n.id})"><i data-feather="trash"></i></button>
      </div>
      <pre class="mb-0 text-wrap text-muted small whitespace">${esc(n.body)}</pre>
      <div class="text-muted small mt-50">${esc(n.kind)} · ${esc(n.created_at)}</div>
    </div></div>`).join('');
  return `${pageHeading('Notes')}
    <div class="card"><div class="card-body">
      <label class="form-label">Title</label>
      <input id="n-title" class="form-control mb-1" placeholder="cth: Python Dictionary">
      <label class="form-label">Content</label>
      <textarea id="n-body" class="form-control mb-1" rows="5"></textarea>
      <button class="btn btn-primary" onclick="actSaveNote()"><i data-feather="save"></i> Simpan</button>
    </div></div>
    ${items}`;
}

async function pageMistakes() {
  const list = await api('/api/mistakes');
  const items = list.map(m => `
    <div class="card"><div class="card-body">
      <div class="d-flex align-items-center justify-content-between">
        <h6 class="card-title mb-1">${esc(m.problem)}</h6>
        <button class="btn btn-icon btn-outline-danger btn-sm" onclick="actDelMistake(${m.id})"><i data-feather="trash"></i></button>
      </div>
      <div class="small"><span class="text-muted">Cause:</span> ${esc(m.cause)}<br>
        <span class="text-muted">Lesson:</span> ${esc(m.lesson)}<br>
        <span class="text-muted">Prevent:</span> ${esc(m.prevention)}</div>
      <div class="text-muted small mt-50">${esc(m.created_at)}</div>
    </div></div>`).join('');
  return `${pageHeading('Mistake Journal')}
    <div class="card"><div class="card-body">
      <label class="form-label">Problem</label><input id="m-problem" class="form-control mb-1">
      <label class="form-label">Why it happened</label><input id="m-cause" class="form-control mb-1">
      <label class="form-label">What I learned</label><input id="m-lesson" class="form-control mb-1">
      <label class="form-label">How to prevent it</label><input id="m-prevention" class="form-control mb-1">
      <button class="btn btn-primary" onclick="actSaveMistake()"><i data-feather="save"></i> Simpan</button>
    </div></div>
    ${items}`;
}

async function pageProgress() {
  const p = await api('/api/progress');
  let html = pageHeading('Progress') + `<div class="card"><div class="card-body">${barHtml(p.overall, p.overall >= 100)}</div></div>
    <div class="row match-height">`;
  html += p.phases.map(x => {
    const pct = Math.round(x.pct);
    return `<div class="col-xl-4 col-md-6 col-12"><div class="card"><div class="card-body">
      <div class="d-flex justify-content-between"><h6 class="card-title mb-1">${esc(x.phase)}</h6><small class="text-muted">${x.done}/${x.total}</small></div>
      ${barHtml(pct, pct >= 100)}</div></div></div>`;
  }).join('');
  return html + '</div>';
}

async function pageWeekly() {
  const d = await api('/api/dashboard');
  const p = await api('/api/progress');
  const rows = p.phases.map(x => `
    <li class="list-group-item d-flex justify-content-between align-items-center">
      <span>${esc(x.phase)}</span><span class="badge bg-light-primary rounded-pill">${x.pct}%</span></li>`).join('');
  return `${pageHeading('Weekly Review')}
    <div class="row">
      <div class="col-lg-4 col-md-6 col-12"><div class="card"><div class="card-body">
        <div class="mb-1"><span class="text-muted small">Lessons completed</span><div class="fw-bolder">${d.lessons_completed}/${d.lessons_total}</div></div>
        <div class="mb-1"><span class="text-muted small">Challenges passed</span><div class="fw-bolder">${d.challenges_passed}/${d.challenges_total}</div></div>
        <div class="mb-1"><span class="text-muted small">Learning time</span><div class="fw-bolder">${esc(d.learning_time)}</div></div>
        <div><span class="text-muted small">Streak</span><div class="fw-bolder">${d.streak} hari</div></div>
      </div></div></div>
      <div class="col-lg-8 col-md-6 col-12"><div class="card"><div class="card-header"><h5 class="card-title mb-0">Progress per topik</h5></div>
        <div class="card-body"><ul class="list-group list-group-flush">${rows}</ul>
          <p class="text-muted small mb-0 mt-1">Data dari database nyata.</p></div></div></div>
    </div>`;
}

function pageSettings() {
  return `${pageHeading('Settings')}
    <div class="card"><div class="card-body">
      <p class="mb-1">Dark mode tersimpan di browser (localStorage).</p>
      <button class="btn btn-primary mb-2" onclick="toggleTheme()"><i data-feather="moon"></i> Toggle theme</button>
      <hr>
      <h6 class="card-title">AI Usage Policy</h6>
      <blockquote class="blockquote">TRY FIRST. THINK BEFORE ASKING AI.<br>USE AI TO LEARN, NOT TO AVOID THINKING.</blockquote>
    </div></div>`;
}

/* ================= Actions ================= */
async function actComplete(slug) { await api(`/api/lessons/${slug}/complete`, 'POST', {}); route(); }

const hintCache = {};
async function actHint(slug, which) {
  if (!hintCache[slug]) hintCache[slug] = await api(`/api/challenges/${slug}`);
  const box = document.getElementById('hint-box');
  box.innerHTML += `<div class="alert alert-warning py-1 small mb-50">${esc(hintCache[slug]['hint' + which])}</div>`;
  document.getElementById('hint-acc').value = Number(document.getElementById('hint-acc').value) + 1;
  document.getElementById('hint-count').textContent = document.getElementById('hint-acc').value;
}

async function actSubmit(slug) {
  const code = document.getElementById('ch-code').value;
  const hints = Number(document.getElementById('hint-acc').value);
  const out = document.getElementById('ch-result');
  out.innerHTML = '<div class="d-flex align-items-center text-primary"><i data-feather="loader"></i> running...</div>'; feather.replace();
  try {
    const res = await api(`/api/challenges/${slug}/submit`, 'POST', { code, hints_used: hints });
    if (res.status === 'passed') {
      out.innerHTML = `<div class="alert alert-success"><i data-feather="check-circle"></i> PASSED ${res.passed}/${res.total} tests</div>`;
    } else {
      const f = res.failures.map(x => `<div class="small mb-50"><span class="text-danger">Expected:</span> ${esc(String(x.expected))} — <span class="text-danger">Received:</span> ${esc(String(x.got))}</div>`).join('');
      const e = res.error ? '<pre class="output mt-1 mb-0">' + esc(res.error) + '</pre>' : '';
      out.innerHTML = `<div class="alert alert-danger"><i data-feather="x-circle"></i> FAILED ${res.passed}/${res.total} tests${f}</div>${e}`;
    }
  } catch (e) { out.innerHTML = `<div class="alert alert-danger">${esc(e.message)}</div>`; }
  feather.replace();
}

async function actRun() {
  const out = document.getElementById('pg-output');
  out.textContent = '...running\n';
  try {
    const res = await api('/api/playground/run', 'POST', { code: document.getElementById('pg-code').value, language: 'python' });
    out.textContent = res.status === 'ok' ? res.output : (res.error || 'error');
    out.className = 'output mt-1' + (res.status !== 'ok' ? ' output-err' : '');
  } catch (e) { out.textContent = 'Network error: ' + e.message; out.className = 'output mt-1 output-err'; }
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
    el.innerHTML = `<div class="alert alert-danger"><h5 class="alert-heading">Error</h5><pre class="mb-0" style="white-space:pre-wrap">${esc(e.message)}</pre></div>`;
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
    `<li><a href="#/lessons/${esc(r.slug)}" onclick="closeSearch()">${esc(r.title)} <small class="text-muted">(${esc(r.folder)})</small></a></li>`
  ).join('') || '<li class="text-muted">Tidak ada hasil</li>';
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
