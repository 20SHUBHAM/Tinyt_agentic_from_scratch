function download(filename, text) {
  const a = document.createElement('a');
  a.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(text));
  a.setAttribute('download', filename);
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

const state = { personas: [], framework: null, transcript: null, summary: null, llm: { apiKey: '', baseUrl: '', model: '' } };

document.addEventListener('DOMContentLoaded', () => {
  // Tabs
  document.querySelectorAll('.tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
      tab.classList.add('active');
      document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
    });
  });

  // Settings
  const apiKey = document.getElementById('apiKey');
  const baseUrl = document.getElementById('baseUrl');
  const model = document.getElementById('model');
  const saveSettings = document.getElementById('saveSettings');
  const settingsStatus = document.getElementById('settingsStatus');
  saveSettings.addEventListener('click', () => {
    state.llm.apiKey = apiKey.value.trim();
    state.llm.baseUrl = baseUrl.value.trim() || 'https://api.openai.com/v1';
    state.llm.model = model.value.trim();
    settingsStatus.textContent = state.llm.apiKey ? 'Saved.' : 'Missing API key';
  });

  // Personas
  const description = document.getElementById('description');
  const count = document.getElementById('count');
  const countValue = document.getElementById('countValue');
  const generate = document.getElementById('generate');
  const downloadBtn = document.getElementById('download');
  const status = document.getElementById('status');
  const clearBtn = document.getElementById('clear-personas');

  count.addEventListener('input', () => { countValue.textContent = count.value; });

  generate.addEventListener('click', async () => {
    const desc = (description.value || '').trim();
    if (!desc) {
      status.textContent = 'Please provide a short description to guide persona generation.';
      return;
    }
    try {
      status.textContent = 'Generating personas...';
      const res = await fetch('/api/personas', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.llm.apiKey}`,
          'X-LLM-Base-Url': state.llm.baseUrl,
          'X-LLM-Model': state.llm.model,
        },
        body: JSON.stringify({ description: desc, count: parseInt(count.value, 10) || 5 })
      });
      if (!res.ok) throw new Error(await res.text());
      const personas = await res.json();
      state.personas = personas;
      status.textContent = `Generated ${personas.length} participants.`;
      renderPersonas(personas);
      downloadBtn.disabled = personas.length === 0;
      document.getElementById('generate-framework').disabled = false;
    } catch (e) {
      status.textContent = `Error: ${e.message}`;
    }
  });

  clearBtn.addEventListener('click', () => {
    state.personas = [];
    renderPersonas([]);
    status.textContent = '';
    downloadBtn.disabled = true;
  });

  downloadBtn.addEventListener('click', () => {
    download('personas.json', JSON.stringify(state.personas, null, 2));
  });

  // Framework
  const topic = document.getElementById('topic');
  const goals = document.getElementById('goals');
  const duration = document.getElementById('duration');
  const phases = document.getElementById('phases');
  const genFramework = document.getElementById('generate-framework');
  const dlFramework = document.getElementById('download-framework');
  const frameworkView = document.getElementById('framework-view');
  genFramework.addEventListener('click', async () => {
    frameworkView.textContent = '';
    try {
      const res = await fetch('/api/framework', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.llm.apiKey}`,
          'X-LLM-Base-Url': state.llm.baseUrl,
          'X-LLM-Model': state.llm.model,
        },
        body: JSON.stringify({
          topic: (topic.value || '').trim(),
          goals: (goals.value || '').trim(),
          duration: parseInt(duration.value, 10) || 30,
          phases: (phases.value || '').trim(),
          personas: state.personas
        })
      });
      if (!res.ok) throw new Error(await res.text());
      const fw = await res.json();
      state.framework = fw;
      renderFramework(fw, frameworkView);
      dlFramework.disabled = false;
      document.getElementById('run-sim').disabled = false;
    } catch (e) {
      frameworkView.textContent = `Error: ${e.message}`;
    }
  });
  dlFramework.addEventListener('click', () => download('framework.json', JSON.stringify(state.framework, null, 2)));

  // Simulation
  const runSim = document.getElementById('run-sim');
  const dlTranscript = document.getElementById('download-transcript');
  const simStatus = document.getElementById('sim-status');
  const transcriptEl = document.getElementById('transcript');
  runSim.addEventListener('click', async () => {
    simStatus.textContent = 'Simulating...';
    transcriptEl.innerHTML = '';
    try {
      const res = await fetch('/api/simulate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.llm.apiKey}`,
          'X-LLM-Base-Url': state.llm.baseUrl,
          'X-LLM-Model': state.llm.model,
        },
        body: JSON.stringify({ personas: state.personas, framework: state.framework })
      });
      if (!res.ok) throw new Error(await res.text());
      const sim = await res.json();
      state.transcript = sim;
      renderTranscript(sim, transcriptEl);
      simStatus.textContent = 'Simulation complete.';
      dlTranscript.disabled = false;
      document.getElementById('generate-summary').disabled = false;
      document.getElementById('qa-ask').disabled = false;
    } catch (e) {
      simStatus.textContent = `Error: ${e.message}`;
    }
  });
  dlTranscript.addEventListener('click', () => download('transcript.json', JSON.stringify(state.transcript, null, 2)));

  // Summary
  const schemaEl = document.getElementById('summary-schema');
  const genSummary = document.getElementById('generate-summary');
  const dlSummary = document.getElementById('download-summary');
  const summaryView = document.getElementById('summary-view');
  genSummary.addEventListener('click', async () => {
    summaryView.textContent = '';
    try {
      const res = await fetch('/api/summary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.llm.apiKey}`,
          'X-LLM-Base-Url': state.llm.baseUrl,
          'X-LLM-Model': state.llm.model,
        },
        body: JSON.stringify({ schema: schemaEl.value, transcript: state.transcript })
      });
      if (!res.ok) throw new Error(await res.text());
      const report = await res.json();
      state.summary = report;
      summaryView.textContent = JSON.stringify(report, null, 2);
      dlSummary.disabled = false;
    } catch (e) {
      summaryView.textContent = `Error: ${e.message}`;
    }
  });
  dlSummary.addEventListener('click', () => download('summary.json', JSON.stringify(state.summary, null, 2)));

  // Q&A
  const qaInput = document.getElementById('qa-input');
  const qaAsk = document.getElementById('qa-ask');
  const qaAnswers = document.getElementById('qa-answers');
  qaAsk.addEventListener('click', async () => {
    qaAnswers.innerHTML = '';
    try {
      const res = await fetch('/api/qa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.llm.apiKey}`,
          'X-LLM-Base-Url': state.llm.baseUrl,
          'X-LLM-Model': state.llm.model,
        },
        body: JSON.stringify({ question: (qaInput.value || '').trim(), transcript: state.transcript })
      });
      if (!res.ok) throw new Error(await res.text());
      const ans = await res.json();
      renderQA(ans, qaAnswers);
    } catch (e) {
      qaAnswers.textContent = `Error: ${e.message}`;
    }
  });
});

function renderPersonas(list) {
  const root = document.getElementById('personas');
  root.innerHTML = '';
  list.forEach(p => {
    const el = document.createElement('div');
    el.className = 'persona';
    el.innerHTML = `
      <h3>${p.name} — ${p.occupation ?? ''} ${p.age ? `(${p.age})` : ''}</h3>
      ${p.personality ? `<div class="meta">${p.personality}</div>` : ''}
      ${p.background ? `<div class="kv"><strong>Background:</strong> ${p.background}</div>` : ''}
      ${Array.isArray(p.motivations) ? `<div class="kv"><strong>Motivations:</strong> ${p.motivations.join(', ')}</div>` : ''}
      ${Array.isArray(p.constraints) ? `<div class="kv"><strong>Constraints:</strong> ${p.constraints.join(', ')}</div>` : ''}
    `;
    root.appendChild(el);
  });
}

function renderFramework(fw, root) {
  if (!fw || !fw.phases) { root.textContent = 'No framework'; return; }
  root.innerHTML = '';
  fw.phases.forEach(ph => {
    const el = document.createElement('div');
    el.className = 'framework-phase';
    el.innerHTML = `<strong>${ph.name}</strong> — ${ph.minutes || '?'} min` +
      (ph.prompts ? `<div><em>Prompts:</em> ${ph.prompts.join('; ')}</div>` : '') +
      (ph.moderatorCues ? `<div><em>Cues:</em> ${ph.moderatorCues.join('; ')}</div>` : '');
    root.appendChild(el);
  });
}

function renderTranscript(sim, root) {
  const items = sim?.transcript || [];
  root.innerHTML = '';
  items.forEach(msg => {
    const el = document.createElement('div');
    el.className = 'message';
    el.innerHTML = `<strong>${msg.speaker}</strong>${msg.phase ? ` <span class="meta">[${msg.phase}]</span>` : ''}<div>${msg.text}</div>`;
    root.appendChild(el);
  });
}

function renderQA(ans, root) {
  root.innerHTML = '';
  const el = document.createElement('div');
  el.className = 'message';
  const quotes = (ans.quotes || []).map(q => `“${q.quote}” — ${q.speaker}`).join('<br/>');
  el.innerHTML = `<div>${ans.answer || ''}</div><div class="meta">Confidence: ${ans.confidence ?? 'n/a'}</div>${quotes ? `<div class="kv">${quotes}</div>` : ''}`;
  root.appendChild(el);
}

