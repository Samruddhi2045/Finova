let dash = null;
const $ = (selector) => document.querySelector(selector);
const api = async (url, options) => {
  const response = await fetch(url, options);
  if (!response.ok) throw new Error(`Request failed (${response.status})`);
  return response.json();
};
const money = (value) => `₹${Number(value || 0).toLocaleString('en-IN', {maximumFractionDigits: 2})}`;
const titleCase = (value) => value.replaceAll('_', ' ').toLowerCase().replace(/\b\w/g, (letter) => letter.toUpperCase());
const riskClass = (level) => level === 'HIGH' || level === 'CRITICAL' ? 'danger' : level === 'MEDIUM' ? 'warn' : 'good';

function nav() {
  document.querySelectorAll('nav button').forEach((button) => {
    button.onclick = () => render(button.dataset.page);
  });
}

function setPageTitle(page) {
  const titles = {
    overview: 'Controller overview',
    recon: 'Reconciliation control',
    exceptions: 'Exception queue',
    memory: 'Exception memory',
    copilot: 'Finance copilot',
    review: 'Human review desk',
    audit: 'Audit trail',
    evaluation: 'Evaluation',
    policies: 'Policy controls'
  };
  $('#title').textContent = titles[page] || 'Finova';
  $('#crumb').textContent = (titles[page] || 'Finova').toUpperCase();
  document.querySelectorAll('nav button').forEach((button) => button.classList.toggle('active', button.dataset.page === page));
}

async function render(page) {
  setPageTitle(page);
  try {
    if (page === 'overview') {
      dash = await api('/api/dashboard');
      const audit = await api('/api/audit');
      $('#last-run').textContent = audit[0]?.ts || 'Not yet run';
      $('#content').innerHTML = `
        <div class="grid">
          <div class="card hero"><div class="label">Match rate</div><div class="value">${dash.match_rate}%</div><div class="metric-note">Target: straight-through processing</div></div>
          <div class="card"><div class="label">Records reviewed</div><div class="value">${dash.total_records.toLocaleString()}</div><div class="metric-note">${dash.matched.toLocaleString()} matched</div></div>
          <div class="card"><div class="label">Open exceptions</div><div class="value danger">${dash.unresolved.toLocaleString()}</div><div class="metric-note">${dash.high_risk} high / critical risk</div></div>
          <div class="card"><div class="label">Financial exposure</div><div class="value">${money(dash.financial_exposure)}</div><div class="metric-note">Across unresolved differences</div></div>
        </div>
        <div class="two">
          <div class="panel"><p class="section-kicker">Reconciliation health</p><h3>Current control position</h3><p class="small">${dash.matched.toLocaleString()} matched of ${dash.total_records.toLocaleString()} records</p><div class="bar"><i style="width:${dash.match_rate}%"></i></div><div class="scenario"><b>Controller principle</b><br>Deterministic controls establish what happened. Investigation explains why. Policy and human review govern what happens next.</div></div>
          <div class="panel"><p class="section-kicker">Exception mix</p><h3>Where attention is concentrated</h3>${Object.entries(dash.exception_types).slice(0, 7).map(([key, value]) => `<div class="distribution-row"><b>${titleCase(key)}</b><span>${value}</span></div>`).join('')}</div>
        </div>`;
    } else if (page === 'exceptions' || page === 'review') {
      const exceptions = await api('/api/exceptions');
      $('#content').innerHTML = `<div class="panel"><p class="section-kicker">${page === 'review' ? 'Decision workflow' : 'Control queue'}</p><h3>${page === 'review' ? 'Pending human decisions' : 'All detected exceptions'}</h3><div class="table-wrap"><table class="table"><thead><tr><th>Case ID</th><th>Exception type</th><th>Difference</th><th>Risk</th><th>Status</th><th>Action</th></tr></thead><tbody>${exceptions.slice(0, 120).map((item) => `<tr><td>${item.exception_id}</td><td>${titleCase(item.exception_type)}</td><td>${money(item.discrepancy_amount)}</td><td><span class="pill ${riskClass(item.risk_level)}">${item.risk_level} · ${item.risk_score}</span></td><td>${item.review_status}</td><td class="actions"><button onclick="investigate('${item.exception_id}')">Investigate</button><button onclick="decide('${item.exception_id}','RESOLVE')">Resolve</button><button onclick="decide('${item.exception_id}','ESCALATE')">Escalate</button></td></tr>`).join('')}</tbody></table></div></div>`;
    } else if (page === 'memory') {
      const exceptions = await api('/api/exceptions');
      const selected = exceptions.find((item) => item.risk_level === 'HIGH') || exceptions[0];
      const similar = selected ? await api(`/api/exceptions/${selected.exception_id}/similar`) : [];
      $('#content').innerHTML = `<div class="panel"><p class="section-kicker">Precedent search</p><h3>Exception memory</h3><p class="small">Comparable historical cases support finance judgment; they do not make the decision.</p>${selected ? `<div class="scenario"><b>Reference case:</b> ${selected.exception_id} · ${titleCase(selected.exception_type)} · ${money(selected.discrepancy_amount)}</div><h3>Similar historical cases</h3>${similar.map((item) => `<div class="scenario"><b>${item.exception_id}</b> · ${item.transaction_id}<br>${item.root_cause}<br><span class="small">Difference ${money(item.discrepancy_amount)}</span></div>`).join('')}` : '<p class="small">No exception history is available.</p>'}</div>`;
    } else if (page === 'copilot') {
      $('#content').innerHTML = `<div class="panel"><p class="section-kicker">Controlled assistant</p><h3>Ask the finance controller copilot</h3><p class="small">Answers are grounded in current Finova data through controlled tools.</p><div class="chat"><input id="q" placeholder="e.g. What is our current match rate?"><button onclick="ask()">Ask question</button></div><div id="ans"></div></div>`;
    } else if (page === 'audit') {
      const audit = await api('/api/audit');
      $('#content').innerHTML = `<div class="panel"><p class="section-kicker">Traceability</p><h3>Audit trail</h3><div class="table-wrap"><table class="table"><thead><tr><th>Timestamp</th><th>Event</th><th>Detail</th></tr></thead><tbody>${audit.map((item) => `<tr><td>${item.ts}</td><td>${titleCase(item.event)}</td><td>${item.detail}</td></tr>`).join('')}</tbody></table></div></div>`;
    } else if (page === 'evaluation') {
      const evaluation = await api('/api/evaluation');
      $('#content').innerHTML = `<div class="grid"><div class="card"><div class="label">Match rate</div><div class="value">${evaluation.match_rate}%</div></div><div class="card"><div class="label">Precision</div><div class="value good">${evaluation.precision}%</div></div><div class="card"><div class="label">Recall</div><div class="value good">${evaluation.recall}%</div></div><div class="card"><div class="label">F1 score</div><div class="value">${evaluation.f1}%</div></div></div><div class="panel"><p class="section-kicker">Ground-truth evaluation</p><h3>Control performance</h3><p>${evaluation.total_records.toLocaleString()} synthetic records · ${evaluation.ground_truth_exceptions} seeded exceptions · ${money(evaluation.financial_exposure)} exposure.</p><p class="small">${evaluation.note}</p></div>`;
    } else if (page === 'policies') {
      const policies = await api('/api/policies');
      $('#content').innerHTML = `<div class="panel"><p class="section-kicker">Guardrails</p><h3>Policy controls</h3><p class="small">Policies constrain recommendations and force human review where financial risk warrants it.</p><div class="table-wrap"><table class="table"><thead><tr><th>Policy</th><th>Rule</th><th>System action</th></tr></thead><tbody>${policies.map((item) => `<tr><td>${item.name}</td><td>${item.rule}</td><td><span class="pill">${item.action}</span></td></tr>`).join('')}</tbody></table></div></div>`;
    } else if (page === 'recon') {
      $('#content').innerHTML = `<div class="panel"><p class="section-kicker">Controlled process</p><h3>Run a reconciliation cycle</h3><p>The controller generates seeded records, validates source values, detects exceptions, scores exposure, and rebuilds the review queue.</p><button class="primary-button" onclick="runController()">Run controller now</button><div id="runmsg" class="answer"></div></div>`;
    }
  } catch (error) {
    $('#content').innerHTML = `<div class="panel"><h3>Unable to load this view</h3><p class="small">${error.message}. Refresh and try again.</p></div>`;
  }
}

async function runController() {
  const result = await api('/api/reconciliation/run', {method: 'POST'});
  alert(`Controller completed: ${result.records.toLocaleString()} records, ${result.exceptions.toLocaleString()} exceptions.`);
  render('overview');
}

async function investigate(id) {
  const result = await api(`/api/exceptions/${id}/investigate`, {method: 'POST'});
  alert(`${result.summary}\n\nRoot cause: ${result.probable_root_cause}\n\nRecommendation: ${result.recommended_action}\n\nHuman review: ${result.requires_human_review ? 'REQUIRED' : 'Not mandatory'}`);
}

async function decide(id, decision) {
  await api(`/api/reviews/${id}/decision`, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({decision, note: 'Decision made in Finova Review Desk'})});
  render('review');
}

async function ask() {
  const question = $('#q').value.trim();
  if (!question) return;
  const result = await api('/api/copilot', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({question})});
  $('#ans').innerHTML = `<div class="answer">${result.answer}</div>`;
}

nav();
render('overview');
