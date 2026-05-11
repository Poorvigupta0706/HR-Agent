// components/score.js

function renderScorePanel(container) {
  container.innerHTML = `
    <div class="card">
      <div class="card-title">Resume & Job Description</div>
      <div class="section-label">Job Description</div>
      <textarea id="jd-input" rows="5"
        placeholder="Paste the job description here..."></textarea>

      <div style="margin-top:1rem" class="section-label">Resume Text</div>
      <textarea id="resume-input" rows="6"
        placeholder="Paste resume text here (or it will be extracted from upload)..."></textarea>

      <div style="margin-top:1rem">
        <div class="upload-zone" id="upload-zone" onclick="document.getElementById('file-input').click()">
          <i class="ti ti-upload" style="font-size:20px"></i>
          <div style="margin-top:6px">Drop PDF resume or click to upload</div>
          <input type="file" id="file-input" accept=".pdf,.txt" style="display:none"/>
        </div>
        <div id="file-chip-wrap"></div>
      </div>

      <button class="btn btn-primary" id="analyse-btn" style="margin-top:1rem"
        onclick="runFullAnalysis()">
        <i class="ti ti-sparkles"></i> Analyse with AI
      </button>
    </div>

    <!-- Score Results (hidden until analysed) -->
    <div class="card" id="score-results" style="display:none">
      <div class="card-title">AI Generated Score</div>
      <div class="score-wrap">
        <div class="score-ring">
          <svg width="120" height="120" viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="50" fill="none" stroke="#e5e7eb" stroke-width="10"/>
            <circle id="ring-fill" cx="60" cy="60" r="50" fill="none"
              stroke="#2563eb" stroke-width="10"
              stroke-dasharray="314.16" stroke-dashoffset="314.16"
              stroke-linecap="round" transform="rotate(-90 60 60)"
              style="transition: stroke-dashoffset 0.8s ease"/>
            <text id="ring-num" x="60" y="56" text-anchor="middle"
              font-size="24" font-weight="700" fill="#1a1a1a">0</text>
            <text x="60" y="72" text-anchor="middle"
              font-size="11" fill="#9ca3af">/100</text>
          </svg>
          <span id="ring-badge" class="badge badge-maybe">—</span>
        </div>
        <div class="score-grid" id="score-grid"></div>
      </div>

      <div class="divider" style="margin:1rem 0"></div>
      <div class="row">
        <div class="col card" style="background:#f9fafb">
          <div class="section-label">JD Match</div>
          <div id="jd-match" style="font-size:24px;font-weight:700;color:#d97706">—</div>
          <div class="prose" style="font-size:11px">of required skills matched</div>
        </div>
        <div class="col card" style="background:#f9fafb">
          <div class="section-label">Confidence</div>
          <div id="confidence" style="font-size:24px;font-weight:700">—</div>
          <div class="prose" style="font-size:11px">model confidence level</div>
        </div>
      </div>
    </div>
  `;

  // File upload handler
  document.getElementById('file-input').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const chip = document.getElementById('file-chip-wrap');
    chip.innerHTML = `<div class="file-chip"><i class="ti ti-file-type-pdf"></i>${file.name} · ${(file.size/1024).toFixed(1)} KB</div>`;

    // Read as text (works for .txt; for real PDF use a PDF.js parser)
    const text = await file.text().catch(() => "");
    if (text) document.getElementById('resume-input').value = text;
  });
}

function updateScoreUI(data) {
  document.getElementById('score-results').style.display = 'block';

  // Ring
  const offset = 314.16 * (1 - data.total_score / 100);
  document.getElementById('ring-fill').setAttribute('stroke-dashoffset', offset.toFixed(2));
  document.getElementById('ring-num').textContent = Math.round(data.total_score);

  // Badge
  const badgeEl = document.getElementById('ring-badge');
  badgeEl.textContent = data.recommendation;
  badgeEl.className = `badge badge-${data.recommendation.toLowerCase()}`;

  // JD match & confidence
  document.getElementById('jd-match').textContent = Math.round(data.jd_match_score) + '%';
  document.getElementById('confidence').textContent = data.confidence_level;

  // Sub-score grid
  const subs = [
    { label: 'Skills',      value: data.skills_score,       color: '#2563eb' },
    { label: 'Experience',  value: data.experience_score,   color: '#d97706' },
    { label: 'Projects',    value: data.project_score,      color: '#7c3aed' },
    { label: 'Education',   value: data.education_score,    color: '#059669' },
    { label: 'Certs',       value: data.certification_score,color: '#dc2626' },
    { label: 'Semantic',    value: data.semantic_score,     color: '#0891b2' },
  ];

  document.getElementById('score-grid').innerHTML = subs.map(s => `
    <div class="score-mini">
      <div class="score-mini-label">${s.label}</div>
      <div class="score-mini-value" style="color:${s.color}">${s.value}/10</div>
      <div class="mini-bar">
        <div class="mini-fill" style="width:${s.value*10}%;background:${s.color}"></div>
      </div>
    </div>`).join('');
}