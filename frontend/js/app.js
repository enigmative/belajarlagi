/* Belajar Lagi — frontend SPA (editorial grid style) */
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

function barHtml(pct, ok, showLabel = true) {
  const w = Math.max(0, Math.min(100, pct));
  const label = showLabel ? `<div class="progress-label"><span></span><span>${Math.round(w)}%</span></div>` : '';
  return `${label}<div class="progress${showLabel ? '' : ' progress-flush'}"><div class="progress-bar" style="width:${w}%"></div></div>`;
}

function statCard(icon, label, value) {
  return `<div class="stat-card" style="display:flex;align-items:center;justify-content:space-between">
    <div>
      <div class="stat-label">${label}</div>
      <div class="stat-value">${value}</div>
    </div>
    <div style="opacity:.35"><i data-feather="${icon}" style="width:24px;height:24px"></i></div>
  </div>`;
}

function pageCard(title, bodyHtml) {
  const h = title ? `<div class="card-header"><h4 class="card-title">${title}</h4></div>` : '';
  return `<div class="card">${h}<div class="card-body">${bodyHtml}</div></div>`;
}

function pageHeading(t) { return `<h1 class="mega" style="margin-bottom:var(--line)">${t}</h1>`; }

/* ---------- Text scramble on hover (reference style) ---------- */
const SCRAMBLE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%';
function scrambleEl(el) {
  if (el._scrambling) return;
  const original = el.dataset.scrambleText || el.textContent;
  el.dataset.scrambleText = original;
  if (!original.trim()) return;
  el._scrambling = true;
  let frame = 0;
  const total = 14;
  const interval = setInterval(() => {
    let out = '';
    for (let i = 0; i < original.length; i++) {
      const ch = original[i];
      if (ch === ' ' || ch === '\n') { out += ch; continue; }
      if (frame >= total + i) {
        out += ch;
      } else if (frame > i) {
        out += SCRAMBLE_CHARS[Math.floor(Math.random() * SCRAMBLE_CHARS.length)];
      } else {
        out += ch;
      }
    }
    el.textContent = out;
    frame++;
    if (frame > total + original.length) {
      clearInterval(interval);
      el.textContent = original;
      el._scrambling = false;
    }
  }, 35);
}

function bindScramble() {
  document.querySelectorAll('.sidebar-nav a, .mobile-drawer a').forEach(el => {
    if (el._scrambleBound) return;
    el._scrambleBound = true;
    el.addEventListener('mouseenter', () => scrambleEl(el));
  });
}

/* ================= Pages ================= */

async function pageDashboard() {
  const d = await api('/api/dashboard');
  let iv = null;
  try { iv = await api('/api/interview/summary'); } catch (e) { iv = null; }
  const btn = d.current_lesson
    ? `<a class="button" href="#/lessons/${esc(d.current_lesson.slug)}">Continue — ${esc(d.current_lesson.title)} →</a>`
    : `<a class="button" href="#/roadmap">Mulai dari Roadmap →</a>`;
  const ivCard = iv ? pageCard('Interview Prep — Sprint 3 Hari', `
    <div style="padding-bottom:var(--line);margin-bottom:var(--line);border-bottom:1px solid rgba(var(--black-rgb),.1)">
      <div class="mega" style="font-size:calc(var(--font-size)*2.2);line-height:1">${iv.overall.pct}%</div>
      <div class="small text-muted" style="margin-top:.25rem">${iv.overall.correct}/${iv.overall.total} benar · ${iv.overall.wrong} salah · ${iv.overall.unseen} belum</div>
      <div style="margin-top:var(--line)"><a class="button" href="#/interview">Buka Interview →</a></div>
    </div>
    <div>
      ${iv.days.map(day => `<div style="margin-bottom:var(--line)">
        <div style="margin-bottom:.1rem"><strong>Hari ${day.day}</strong> <span class="text-muted small">${esc(day.title.split('—').pop().trim())}</span></div>
        <div class="small text-muted" style="margin-bottom:.25rem">${day.correct}/${day.total} benar</div>
        ${barHtml(day.pct, day.pct >= 100)}
      </div>`).join('')}
    </div>`) : '';
  return `
    ${pageHeading('Dashboard')}
    <p class="text-muted" style="margin-bottom:var(--line);text-transform:none;letter-spacing:0">Ringkasan progres belajarmu.</p>
    <div class="card" style="margin-bottom:var(--line)">
      <div class="card-header" style="display:flex;justify-content:space-between;align-items:center">
        <h4 class="card-title" style="margin:0">Overall Progress</h4>
        <span class="mega" style="font-size:calc(var(--font-size)*1.6)">${Math.round(d.overall_pct)}%</span>
      </div>
      <div class="card-body">${barHtml(d.overall_pct, d.overall_pct >= 100, false)}</div>
    </div>
    <div class="stat-grid" style="margin-bottom:var(--line)">
      ${statCard('layers', 'Current Phase', esc(d.current_phase || '—'))}
      ${statCard('book', 'Lessons', `${d.lessons_completed}/${d.lessons_total}`)}
      ${statCard('code', 'Challenges', `${d.challenges_passed}/${d.challenges_total}`)}
      ${statCard('award', 'Interview', iv ? `${iv.overall.correct}/${iv.overall.total}` : '—')}
      ${statCard('trending-up', 'Streak', `${d.streak} hari`)}
      ${statCard('clock', 'Waktu', esc(d.learning_time))}
    </div>
    <div class="card" style="margin-bottom:var(--line)">
      <div class="card-header"><h4 class="card-title" style="margin:0">Continue Learning</h4></div>
      <div class="card-body">
        ${d.current_lesson
          ? `<p class="card-text" style="margin-bottom:var(--line)">Lanjutkan: <strong>${esc(d.current_lesson.title)}</strong></p>`
          : '<p class="card-text text-muted" style="margin-bottom:var(--line)">Belum ada lesson aktif.</p>'}
        <div>${btn}</div>
      </div>
    </div>
    ${ivCard}
    <div class="card" style="border-top:none;padding-top:0">
      <div class="card-body" style="text-align:center">
        <p class="text-muted mb-0" style="text-transform:none;letter-spacing:0">TRY FIRST · THINK BEFORE ASKING AI</p>
        <p class="text-muted small mb-0" style="text-transform:none;letter-spacing:0">Gunakan AI untuk belajar, bukan untuk menghindar dari berpikir.</p>
      </div>
    </div>`;
}

/* ================= Interview Prep ================= */
const interviewOpen = new Set();
const interviewHintShown = {};

function interviewStatusBadge(status) {
  if (status === 'correct') return '<span class="badge badge-success">Benar</span>';
  if (status === 'wrong') return '<span class="badge badge-danger">Salah</span>';
  return '<span class="badge badge-secondary">Belum dicoba</span>';
}

function interviewKindLabel(kind) {
  return ({ mcq: 'Pilihan ganda', open: 'Trace / tulis', code: 'Live coding', oral: 'Interview lisan' })[kind] || kind;
}

function interviewPromptMarkdown(q) {
  if (q.kind !== 'mcq') return q.prompt;
  return q.prompt
    .split('\n')
    .filter(line => !/^\s*-\s*[A-D]\.\s+/.test(line))
    .join('\n')
    .trim();
}

function interviewQuestionRow(q) {
  return `<a class="interview-q-row" href="#/interview/${esc(q.id)}">
    <span class="status-dot ${esc(q.status)}"></span>
    <span style="flex:1">
      <span class="fw-bolder" style="display:block">${esc(q.title)}</span>
      <span class="small text-muted">${esc(interviewKindLabel(q.kind))} · ${q.points} poin${q.attempts ? ` · ${q.attempts}x dicoba` : ''}</span>
    </span>
    ${interviewStatusBadge(q.status)}
    <span class="text-muted">→</span>
  </a>`;
}

async function pageInterview(sub) {
  const data = await api('/api/interview');
  const filterDay = /^day[123]$/.test(sub || '') ? Number(sub.slice(3)) : null;
  if (sub && data.questions.some(q => q.id === sub)) {
    return pageInterviewQuestion(sub, data);
  }

  const days = filterDay ? data.days.filter(d => d.day === filterDay) : data.days;
  const pool = filterDay ? data.questions.filter(q => q.day === filterDay) : data.questions;
  const next = pool.find(q => q.status === 'wrong') || pool.find(q => q.status === 'unseen');
  const nextBtn = next
    ? `<a class="button" href="#/interview/${esc(next.id)}">${next.status === 'wrong' ? 'Perbaiki soal salah' : 'Mulai soal berikutnya'} →</a>`
    : '<span class="badge badge-success">Semua soal sudah benar</span>';

  const dayCards = days.map(day => {
    const dayQs = data.questions.filter(q => q.day === day.day);
    const topicSections = day.topics.map(t => {
      const tqs = dayQs.filter(q => q.topic === t.topic);
      return `<div class="interview-topic">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:var(--line)">
          <h4 style="margin:0">${esc(t.topic)}</h4>
          <span class="small text-muted">${t.correct}/${t.total} benar</span>
        </div>
        ${barHtml(t.pct, t.pct >= 100)}
        <div style="margin-top:.5rem">${tqs.map(interviewQuestionRow).join('')}</div>
      </div>`;
    }).join('');

    return `<div class="card interview-day">
      <div class="card-header" style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap">
        <div>
          <h4 class="card-title mb-1">${esc(day.title)}</h4>
          <p class="text-muted small mb-0">${esc(day.goal)}</p>
        </div>
        <div style="text-align:right">
          <div class="mega" style="font-size:calc(var(--font-size)*1.8)">${day.pct}%</div>
          <span class="small text-muted">${day.correct}/${day.total} benar</span>
        </div>
      </div>
      <div class="card-body">
        ${barHtml(day.pct, day.pct >= 100)}
        <div style="display:flex;flex-wrap:wrap;align-items:center;margin-top:var(--line);margin-bottom:var(--line)">
          <a class="button small" href="#/lessons/${esc(day.lesson)}">Teori Hari ${day.day}</a>
          <a class="button small" href="#/interview/day${day.day}" style="margin-left:.5rem">Fokus Hari ${day.day}</a>
          <span class="ms-auto small text-muted">${day.wrong} salah · ${day.unseen} belum dicoba</span>
        </div>
        ${topicSections}
      </div>
    </div>`;
  }).join('');

  const filterButtons = [
    `<a class="button ${filterDay ? 'outline' : ''}" href="#/interview">Semua</a>`,
    ...data.days.map(d => `<a class="button ${filterDay === d.day ? '' : 'outline'}" href="#/interview/day${d.day}" style="margin-left:.5rem">Hari ${d.day}</a>`),
  ].join('');

  return `
    <div class="card interview-hero mb-1">
      <div class="card-body">
        <div style="display:flex;flex-wrap:wrap;gap:var(--char2)">
          <div style="flex:2;min-width:260px">
            <span class="badge badge-primary mb-1">Sprint 3 Hari</span>
            <h3 style="margin:.25rem 0">Interview Prep — Fullstack Developer</h3>
            <p class="text-muted mb-1" style="text-transform:none;letter-spacing:0">49 soal: 9 soal inti, latihan Java/Spring/JavaScript/React, 7 live coding, dan 8 pertanyaan lisan. Jawab dulu, baru buka jawaban.</p>
            <div class="interview-legend">
              <span><span class="status-dot correct"></span>Benar</span>
              <span><span class="status-dot wrong"></span>Salah</span>
              <span><span class="status-dot unseen"></span>Belum dicoba</span>
            </div>
          </div>
          <div style="flex:1;min-width:220px">
            <div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:.25rem">
              <div><span class="text-muted small">Progres keseluruhan</span><div class="fw-bolder">${data.overall.correct}/${data.overall.total} benar</div></div>
              <div class="mega" style="font-size:calc(var(--font-size)*1.8)">${data.overall.pct}%</div>
            </div>
            ${barHtml(data.overall.pct, data.overall.pct >= 100)}
            <div style="display:flex;justify-content:space-between;align-items:center;margin-top:var(--line);flex-wrap:wrap">
              <span class="small text-muted">${data.overall.wrong} salah · ${data.overall.unseen} belum dicoba</span>
              ${nextBtn}
            </div>
          </div>
        </div>
      </div>
    </div>
    <div style="display:flex;flex-wrap:wrap;align-items:center;margin-bottom:var(--line)">
      ${filterButtons}
      <span class="ms-auto small text-muted">Klik soal untuk mulai. Progres tersimpan otomatis.</span>
    </div>
    ${dayCards}`;
}

async function pageInterviewQuestion(id, list) {
  const q = await api(`/api/interview/questions/${id}`);
  list = list || await api('/api/interview');
  const dayQs = list.questions.filter(x => x.day === q.day);
  const dayIdx = dayQs.findIndex(x => x.id === id);
  const nextQ = dayIdx >= 0 ? dayQs[dayIdx + 1] : null;
  const mcqAnswered = q.kind === 'mcq' && q.status !== 'unseen';
  const revealed = interviewOpen.has(id) || mcqAnswered;
  const shownHints = interviewHintShown[id] || 0;

  const hintButtons = q.hints.map((_, idx) => {
    const n = idx + 1;
    if (shownHints >= n) return '';
    if (n > 1 && shownHints < n - 1) return '';
    return `<button class="button small" onclick="actInterviewHint('${esc(id)}', ${n})">Buka hint ${n}</button>`;
  }).join('');

  const hintsHtml = q.hints.slice(0, shownHints).map((h, idx) =>
    `<div class="interview-hint lesson-markdown"><strong>Hint ${idx + 1}:</strong> ${renderMarkdown(h)}</div>`).join('');

  let interaction;
  if (q.kind === 'mcq') {
    const options = q.options.map(o => {
      const selected = q.last_choice === o.id;
      const isCorrect = q.correct_choice === o.id;
      const cls = revealed && isCorrect ? 'correct' : (revealed && selected && !isCorrect ? 'wrong' : '');
      return `<button type="button" class="interview-option ${cls}" ${revealed ? 'disabled' : ''} onclick="actInterviewChoose('${esc(id)}', '${esc(o.id)}')">
        <span class="option-letter">${esc(o.id.toUpperCase())}</span>
        <span style="flex:1">${esc(o.text)}</span>
        ${revealed && isCorrect ? '<span class="badge badge-success">Kunci</span>' : ''}
        ${revealed && selected && !isCorrect ? '<span class="badge badge-danger">Pilihanmu</span>' : ''}
      </button>`;
    }).join('');
    interaction = pageCard('3. Pilih jawaban', `<div class="interview-options">${options}</div>
      ${revealed ? '' : '<p class="text-muted small mb-0">Pilih satu. Kunci dan pembahasan terbuka setelah kamu menjawab.</p>'}`);
  } else {
    interaction = pageCard('3. Jawab dulu, baru buka', revealed
      ? '<p class="text-muted mb-0">Jawaban sudah terbuka. Bandingkan dengan jawabanmu, lalu tandai status di bagian bawah.</p>'
      : `<p class="text-muted">Tulis jawabanmu di kertas/editor atau ucapkan dengan suara keras. Setelah itu buka jawaban.</p>
         <button class="button" onclick="actInterviewReveal('${esc(id)}')">Lihat jawaban</button>`);
  }

  const answerHtml = revealed ? `
    ${pageCard('4. Jawaban & pembahasan', `<div class="lesson-markdown">${renderMarkdown(q.answer)}</div>`)}
    ${pageCard('5. Kesalahan umum', `<div class="lesson-markdown">${renderMarkdown(q.traps)}</div>`)}
    ${pageCard('6. Cara menjelaskan di interview', `<div class="lesson-markdown interview-speak">${renderMarkdown(q.speak)}</div>`)}
  ` : '';

  const statusActions = q.kind === 'mcq'
    ? `<div style="display:flex;align-items:center;flex-wrap:wrap">
         ${interviewStatusBadge(q.status)}
         <span class="text-muted small" style="margin-left:.5rem">${q.attempts || 0}x dicoba</span>
         <button class="button small" style="margin-left:auto" onclick="actInterviewReset('${esc(id)}')">Reset</button>
       </div>`
    : revealed
      ? `<div style="display:flex;align-items:center;flex-wrap:wrap">
         ${interviewStatusBadge(q.status)}
         <button class="button small" style="margin-left:.5rem;background:#28c76f;color:#fff" onclick="actInterviewStatus('${esc(id)}', 'correct')">Saya benar</button>
         <button class="button small outline" style="margin-left:.5rem" onclick="actInterviewStatus('${esc(id)}', 'wrong')">Saya salah</button>
         <button class="button small outline" style="margin-left:auto" onclick="actInterviewReset('${esc(id)}')">Reset</button>
       </div>`
      : '<p class="text-muted small mb-0">Buka jawaban dulu, lalu tandai apakah jawabanmu benar atau salah.</p>';

  return `
    <div class="mb-1"><a href="#/interview" class="text-muted small">← Kembali ke Interview Prep</a></div>
    <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;margin-bottom:var(--line)">
      <div>
        <h3 style="margin-bottom:.5rem">${esc(q.title)}</h3>
        <div style="display:flex;flex-wrap:wrap;align-items:center">
          <span class="badge badge-primary" style="margin-right:.5rem">Hari ${q.day}</span>
          <span class="badge badge-primary" style="margin-right:.5rem">${esc(q.topic)}</span>
          <span class="badge" style="margin-right:.5rem">${esc(interviewKindLabel(q.kind))}</span>
          <span class="badge" style="margin-right:.5rem">${q.origin === 'asli' ? 'Soal inti' : 'Latihan'}</span>
          <span class="badge">${q.points} poin</span>
        </div>
      </div>
      <div style="margin-top:.5rem">${interviewStatusBadge(q.status)}</div>
    </div>
    ${pageCard('1. Konsep dasar', `<div class="lesson-markdown">${renderMarkdown(q.concept)}</div>`)}
    ${pageCard('2. Soal', `<div class="lesson-markdown">${renderMarkdown(interviewPromptMarkdown(q))}</div>`)}
    <div style="margin-bottom:var(--line)">${hintButtons} ${hintsHtml}</div>
    ${interaction}
    ${answerHtml}
    ${pageCard('Status soal', `<p class="text-muted small">Status ini tersimpan di database dan dipakai untuk progres per hari/topik. Untuk soal pilihan ganda, status ditentukan otomatis oleh jawabanmu.</p>${statusActions}`)}
    <div style="display:flex;flex-wrap:wrap;align-items:center;margin-top:var(--line)">
      <a class="button small outline" href="#/interview/day${q.day}">Hari ${q.day}</a>
      ${nextQ
        ? `<a class="button small" style="margin-left:.5rem" href="#/interview/${esc(nextQ.id)}">Soal berikutnya →</a>`
        : `<a class="button small" style="margin-left:.5rem;background:#28c76f;color:#fff" href="#/interview">Selesai, kembali →</a>`}
    </div>`;
}

async function actInterviewChoose(id, choice) {
  if (interviewOpen.has(id)) return;
  try {
    await api(`/api/interview/questions/${id}/answer`, 'POST', { choice });
    interviewOpen.add(id);
    route();
  } catch (e) {
    alert('Gagal menjawab: ' + e.message);
  }
}

function actInterviewReveal(id) {
  interviewOpen.add(id);
  route();
}

function actInterviewHint(id, n) {
  interviewHintShown[id] = Math.max(interviewHintShown[id] || 0, n);
  route();
}

async function actInterviewStatus(id, status) {
  try {
    await api(`/api/interview/questions/${id}/status`, 'POST', { status });
    route();
  } catch (e) {
    alert('Gagal menyimpan status: ' + e.message);
  }
}

async function actInterviewReset(id) {
  try {
    await api(`/api/interview/questions/${id}/reset`, 'POST');
    interviewOpen.delete(id);
    delete interviewHintShown[id];
    route();
  } catch (e) {
    alert('Gagal reset: ' + e.message);
  }
}

async function pageRoadmap() {
  const tree = await api('/api/roadmap');
  const cards = tree.map(g => {
    const rows = g.topics.map(t => {
      const dot = t.status === 'completed'
        ? '<span class="badge badge-success">✓</span>'
        : t.status === 'current' ? '<span class="badge badge-primary">→</span>'
        : '<span class="badge badge-secondary">○</span>';
      const link = t.lesson
        ? `<a href="#/lessons/${esc(t.lesson)}">${esc(t.title)}</a>`
        : `<span class="text-muted">${esc(t.title)}</span>`;
      const st = t.status === 'completed' ? '<span class="text-success">Selesai</span>'
        : t.status === 'current' ? '<span class="text-primary">Sedang dipelajari</span>'
        : '<span class="text-muted">Belum</span>';
      return `<div style="display:flex;align-items:center;padding:.5rem 0;border-bottom:1px solid rgba(var(--black-rgb),.1)">
        <span style="margin-right:.75rem">${dot}</span><span style="flex:1">${link}</span><span class="small text-muted">${st}</span></div>`;
    }).join('');
    return `<div class="card"><div class="card-header"><h4 class="card-title" style="margin:0">${esc(g.name)}</h4></div>
      <div class="card-body" style="padding-top:.25rem">${rows}</div></div>`;
  }).join('');
  return pageHeading('Roadmap') + cards;
}

async function pageLesson(slug) {
  slug = slug || 'day01';
  const l = await api(`/api/lessons/${slug}`);
  const btn = l.completed
    ? '<span class="badge badge-success">Selesai</span>'
    : `<button class="button" onclick="actComplete('${esc(slug)}')">Mark as Complete</button>`;
  const pv = l.prev ? `<a class="button outline" href="#/lessons/${esc(l.prev.slug)}">← Previous</a>` : '';
  const nx = l.next ? `<a class="button" href="#/lessons/${esc(l.next.slug)}">Next →</a>` : '';
  return `${pageHeading(esc(l.title))}
    <div class="card"><div class="card-body lesson-markdown">${renderMarkdown(l.markdown)}</div></div>
    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;margin-top:var(--line)">
      <div>${pv} ${nx}</div>
      <div>${btn}</div>
    </div>`;
}

async function pageChallenges() {
  const list = await api('/api/challenges');
  const cards = list.map(c => {
    const color = c.difficulty === 'easy' ? 'success' : c.difficulty === 'medium' ? 'warning' : 'danger';
    const badgeCls = color === 'success' ? 'badge-success' : color === 'warning' ? '' : 'badge-danger';
    return `<div class="card"><div class="card-body" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap">
      <div>
        <h4 class="card-title" style="margin-bottom:.25rem">${esc(c.title)}</h4>
        <div>
          <span class="badge ${badgeCls}">${esc(c.difficulty)}</span>
          ${c.topic ? `<span class="badge badge-primary">${esc(c.topic)}</span>` : ''}
          <span class="small text-muted" style="display:block;margin-top:.25rem">Attempts: ${c.stats.attempts || 0} · Passed: ${c.stats.passed || 0} · Hints: ${c.stats.hints || 0}</span>
        </div>
      </div>
      <a class="button" href="#/challenge/${esc(c.slug)}">Start →</a>
    </div></div>`;
  }).join('');
  return pageHeading('Challenges') +
    '<div class="alert alert-primary">Solusi tidak ditampilkan sebelum kamu mencoba sendiri.</div>' +
    (cards || '<p class="text-muted">Belum ada challenge.</p>');
}

async function pageChallenge(slug) {
  const c = await api(`/api/challenges/${slug}`);
  return `${pageHeading(esc(c.title))}
    <div class="card"><div class="card-body lesson-markdown">${renderMarkdown(c.statement)}
      <p class="text-muted mb-0 mt-1">Tulis fungsi bernama <code>solve</code>.</p></div></div>
    <div style="display:flex;align-items:center;margin-bottom:var(--line)">
      <button class="button outline" onclick="actHint('${esc(c.slug)}',1)">Hint 1</button>
      <button class="button outline" style="margin-left:.5rem" onclick="actHint('${esc(c.slug)}',2)">Hint 2</button>
      <span class="text-muted" style="margin-left:1rem">Hints: <span id="hint-count">0</span></span>
    </div>
    <div id="hint-box"></div>
    <input type="hidden" id="hint-acc" value="0">
    <div style="margin-bottom:calc(var(--line)*2)">
      <label class="form-label">Kode kamu</label>
      <textarea id="ch-code" class="form-control" rows="12">${esc(c.starter_code)}</textarea>
    </div>
    <div style="display:flex;align-items:center">
      <button class="button" onclick="actSubmit('${esc(c.slug)}')">Run &amp; Test →</button>
      <a style="margin-left:1rem" class="text-muted small" href="#/challenges">← back</a>
    </div>
    <div id="ch-result" style="margin-top:var(--line)"></div>`;
}

async function pagePlayground() {
  return `${pageHeading('Playground — Python')}
    <div class="card"><div class="card-body">
      <label class="form-label">Code</label>
      <textarea id="pg-code" class="form-control" rows="14">numbers = [1, 2, 3]
print(sum(numbers))</textarea>
      <div style="display:flex;align-items:center;margin-top:var(--line)">
        <button class="button" onclick="actRun()">Run →</button>
        <span class="text-muted small" style="margin-left:1rem">Ctrl+Enter = run</span>
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
      return `<tr><td>
        <label style="display:flex;align-items:center;gap:.5rem;cursor:pointer">
          <input type="checkbox" data-proj="${esc(p.slug)}" data-task="${s.id}" ${s.is_done ? 'checked' : ''} onchange="actToggleTask(this)">
          <span class="${cls}">${esc(s.title)}</span>
        </label></td></tr>`;
    }).join('');
    return `<div class="card"><div class="card-header" style="display:flex;justify-content:space-between">
      <h4 class="card-title" style="margin:0">${esc(p.name)}</h4>
      <span class="text-muted small">${p.done}/${p.total}</span></div>
      <div class="card-body">
        ${barHtml(pct, p.done === p.total)}
        <table class="table" style="margin-top:var(--line)"><tbody>${rows}</tbody></table>
      </div></div>`;
  }).join('');
  return pageHeading('Projects') + (cards || '<p class="text-muted">Tidak ada project.</p>');
}

async function pageNotes() {
  const list = await api('/api/notes');
  const items = list.map(n => `
    <div class="card"><div class="card-body">
      <div style="display:flex;align-items:center;justify-content:space-between">
        <h4 class="card-title" style="margin:0">${esc(n.title)}</h4>
        <button class="button small outline" onclick="actDelNote(${n.id})">Hapus</button>
      </div>
      <pre class="mb-0 text-wrap text-muted small whitespace" style="margin-top:.5rem">${esc(n.body)}</pre>
      <div class="text-muted small" style="margin-top:.5rem">${esc(n.kind)} · ${esc(n.created_at)}</div>
    </div></div>`).join('');
  return `${pageHeading('Notes')}
    <div class="card"><div class="card-body">
      <label class="form-label">Title</label>
      <input id="n-title" class="form-control" placeholder="cth: Python Dictionary">
      <label class="form-label">Content</label>
      <textarea id="n-body" class="form-control" rows="5"></textarea>
      <div style="margin-top:var(--line)"><button class="button" onclick="actSaveNote()">Simpan →</button></div>
    </div></div>
    ${items}`;
}

async function pageMistakes() {
  const list = await api('/api/mistakes');
  const items = list.map(m => `
    <div class="card"><div class="card-body">
      <div style="display:flex;align-items:center;justify-content:space-between">
        <h4 class="card-title" style="margin:0">${esc(m.problem)}</h4>
        <button class="button small outline" onclick="actDelMistake(${m.id})">Hapus</button>
      </div>
      <div class="small" style="margin-top:.5rem">
        <span class="text-muted">Cause:</span> ${esc(m.cause)}<br>
        <span class="text-muted">Lesson:</span> ${esc(m.lesson)}<br>
        <span class="text-muted">Prevent:</span> ${esc(m.prevention)}
      </div>
      <div class="text-muted small" style="margin-top:.5rem">${esc(m.created_at)}</div>
    </div></div>`).join('');
  return `${pageHeading('Mistake Journal')}
    <div class="card"><div class="card-body">
      <label class="form-label">Problem</label><input id="m-problem" class="form-control">
      <label class="form-label">Why it happened</label><input id="m-cause" class="form-control">
      <label class="form-label">What I learned</label><input id="m-lesson" class="form-control">
      <label class="form-label">How to prevent it</label><input id="m-prevention" class="form-control">
      <div style="margin-top:var(--line)"><button class="button" onclick="actSaveMistake()">Simpan →</button></div>
    </div></div>
    ${items}`;
}

async function pageProgress() {
  const p = await api('/api/progress');
  let html = pageHeading('Progress') + `<div class="card"><div class="card-body">${barHtml(p.overall, p.overall >= 100)}</div></div>
    <div style="display:flex;flex-wrap:wrap;gap:var(--char2);margin-top:var(--line)">`;
  html += p.phases.map(x => {
    const pct = Math.round(x.pct);
    return `<div style="flex:1;min-width:220px" class="card"><div class="card-body">
      <div style="display:flex;justify-content:space-between"><h4 class="card-title" style="margin:0">${esc(x.phase)}</h4><span class="text-muted small">${x.done}/${x.total}</span></div>
      ${barHtml(pct, pct >= 100)}</div></div>`;
  }).join('');
  return html + '</div>';
}

async function pageWeekly() {
  const d = await api('/api/dashboard');
  const p = await api('/api/progress');
  const rows = p.phases.map(x => `
    <div style="display:flex;justify-content:space-between;align-items:center;padding:.5rem 0;border-bottom:1px solid rgba(var(--black-rgb),.1)">
      <span>${esc(x.phase)}</span><span class="badge badge-primary">${x.pct}%</span></div>`).join('');
  return `${pageHeading('Weekly Review')}
    <div style="display:flex;flex-wrap:wrap;gap:var(--char2)">
      <div style="flex:1;min-width:240px" class="card"><div class="card-body">
        <div style="margin-bottom:var(--line)"><span class="text-muted small">Lessons completed</span><div class="fw-bolder">${d.lessons_completed}/${d.lessons_total}</div></div>
        <div style="margin-bottom:var(--line)"><span class="text-muted small">Challenges passed</span><div class="fw-bolder">${d.challenges_passed}/${d.challenges_total}</div></div>
        <div style="margin-bottom:var(--line)"><span class="text-muted small">Learning time</span><div class="fw-bolder">${esc(d.learning_time)}</div></div>
        <div><span class="text-muted small">Streak</span><div class="fw-bolder">${d.streak} hari</div></div>
      </div></div>
      <div style="flex:2;min-width:280px" class="card"><div class="card-header"><h4 class="card-title" style="margin:0">Progress per topik</h4></div>
        <div class="card-body">${rows}
          <p class="text-muted small mb-0" style="margin-top:var(--line)">Data dari database nyata.</p></div></div>
    </div>`;
}

function pageSettings() {
  return `${pageHeading('Settings')}
    <div class="card"><div class="card-body">
      <p style="margin-bottom:var(--line)">Dark mode tersimpan di browser (localStorage).</p>
      <button class="button mb-1" onclick="toggleTheme()">Toggle theme</button>
      <hr>
      <h4 class="card-title">AI Usage Policy</h4>
      <blockquote class="blockquote" style="margin-top:.5rem">TRY FIRST. THINK BEFORE ASKING AI.<br>USE AI TO LEARN, NOT TO AVOID THINKING.</blockquote>
    </div></div>`;
}

/* ================= Actions ================= */
async function actComplete(slug) { await api(`/api/lessons/${slug}/complete`, 'POST', {}); route(); }

const hintCache = {};
async function actHint(slug, which) {
  if (!hintCache[slug]) hintCache[slug] = await api(`/api/challenges/${slug}`);
  const box = document.getElementById('hint-box');
  box.innerHTML += `<div class="alert alert-warning small mb-1">${esc(hintCache[slug]['hint' + which])}</div>`;
  document.getElementById('hint-acc').value = Number(document.getElementById('hint-acc').value) + 1;
  document.getElementById('hint-count').textContent = document.getElementById('hint-acc').value;
}

async function actSubmit(slug) {
  const code = document.getElementById('ch-code').value;
  const hints = Number(document.getElementById('hint-acc').value);
  const out = document.getElementById('ch-result');
  out.innerHTML = '<span class="text-primary">running...</span>';
  try {
    const res = await api(`/api/challenges/${slug}/submit`, 'POST', { code, hints_used: hints });
    if (res.status === 'passed') {
      out.innerHTML = `<div class="alert alert-success">PASSED ${res.passed}/${res.total} tests</div>`;
    } else {
      const f = res.failures.map(x => `<div class="small mb-1"><span class="text-danger">Expected:</span> ${esc(String(x.expected))} — <span class="text-danger">Received:</span> ${esc(String(x.got))}</div>`).join('');
      const e = res.error ? '<pre class="output mt-1 mb-0">' + esc(res.error) + '</pre>' : '';
      out.innerHTML = `<div class="alert alert-danger">FAILED ${res.passed}/${res.total} tests${f}</div>${e}`;
    }
  } catch (e) { out.innerHTML = `<div class="alert alert-danger">${esc(e.message)}</div>`; }
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

  document.querySelectorAll('.sidebar-nav a.active, .mobile-drawer a.active')
    .forEach(el => el.classList.remove('active'));
  const navID = seg === 'lessons' || seg === 'challenge' ? (seg === 'challenge' ? 'challenges' : seg) : seg;
  document.querySelectorAll(`[data-nav][href^="#/${navID}"]`).forEach(nav => {
    nav.classList.add('active');
  });

  const el = document.getElementById('content');
  try {
    if (seg === 'lessons') el.innerHTML = await pageLesson(sub);
    else if (seg === 'challenge') el.innerHTML = await pageChallenge(sub);
    else if (seg === 'interview') el.innerHTML = await pageInterview(sub);
    else if (pageMap[seg]) el.innerHTML = await pageMap[seg]();
    else el.innerHTML = '<h1 class="mega">404</h1><p>Halaman tidak ditemukan.</p>';
  } catch (e) {
    el.innerHTML = `<div class="alert alert-danger"><h4 class="alert-heading">Error</h4><pre class="mb-0" style="white-space:pre-wrap">${esc(e.message)}</pre></div>`;
  }
  const titles = { dashboard: 'Dashboard', roadmap: 'Roadmap', lessons: 'Belajar', challenges: 'Challenges', interview: 'Interview Prep', playground: 'Playground', projects: 'Projects', notes: 'Notes', mistakes: 'Mistake Journal', progress: 'Progress', weekly: 'Weekly Review', settings: 'Settings' };
  document.title = (titles[seg] || 'Belajar Lagi') + ' · Belajar Lagi';
  window.scrollTo(0, 0);
  if (window.feather) feather.replace();
  applyTheme();
}

/* ================= Theme ================= */
function applyTheme() {
  const t = localStorage.getItem('bl-theme') || 'light';
  document.documentElement.classList.toggle('dark', t === 'dark');
  ['theme-toggle', 'theme-toggle-m'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) btn.textContent = t === 'dark' ? 'Light' : 'Dark';
  });
}

function toggleTheme() {
  const t = document.documentElement.classList.contains('dark') ? 'light' : 'dark';
  localStorage.setItem('bl-theme', t);
  applyTheme();
}

/* ================= Search ================= */
function showModal(show) {
  const m = document.getElementById('search-modal');
  m.style.display = show ? 'flex' : 'none';
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
  try {
    const res = await api('/api/search?q=' + encodeURIComponent(q));
    ul.innerHTML = res.map(r =>
      `<li><a href="#/lessons/${esc(r.slug)}" onclick="closeSearch()">${esc(r.title)} <span class="text-muted small">(${esc(r.folder)})</span></a></li>`).join('') || '<li class="text-muted">Tidak ada hasil</li>';
  } catch (e) { ul.innerHTML = '<li class="text-muted">Error</li>'; }
}

function closeMobile() {
  const d = document.getElementById('mobile-drawer');
  const o = document.getElementById('mobile-overlay');
  if (d) d.style.display = 'none';
  if (o) o.style.display = 'none';
}

/* ================= Bootstrap ================= */
window.addEventListener('hashchange', route);
document.addEventListener('DOMContentLoaded', () => {
  const tt = document.getElementById('theme-toggle');
  if (tt) tt.addEventListener('click', toggleTheme);
  const sb = document.getElementById('search-btn');
  // search button not present in new nav; bind Ctrl+K only
  const si = document.getElementById('search-input');
  if (si) si.addEventListener('input', doSearch);
  const ns = document.getElementById('navbar-search');
  if (ns) ns.addEventListener('input', () => { const i = document.getElementById('search-input'); if (i) { i.value = ns.value; doSearch(); } });
  const mt = document.getElementById('menu-toggle');
  if (mt) mt.addEventListener('click', () => {
    const d = document.getElementById('mobile-drawer');
    const o = document.getElementById('mobile-overlay');
    const show = !d || d.style.display === 'none';
    if (d) d.style.display = show ? 'flex' : 'none';
    if (o) o.style.display = show ? 'block' : 'none';
  });
  const ft = document.getElementById('footer-time');
  if (ft) ft.textContent = new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
  bindScramble();
});

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