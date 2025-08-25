// Seeded RNG (Mulberry32)
function mulberry32(seed) {
  let t = seed >>> 0;
  return function() {
    t += 0x6D2B79F5;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r ^= r + Math.imul(r ^ (r >>> 7), 61 | r);
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

function stringToSeed(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
  }
  return h >>> 0;
}

function pickRandom(rng, arr) {
  return arr[Math.floor(rng() * arr.length)];
}

function sampleMany(rng, arr, k) {
  const copy = [...arr];
  const result = [];
  for (let i = 0; i < k && copy.length > 0; i++) {
    const idx = Math.floor(rng() * copy.length);
    result.push(copy.splice(idx, 1)[0]);
  }
  return result;
}

function uuid4(rng) {
  const bytes = new Uint8Array(16);
  for (let i = 0; i < 16; i++) bytes[i] = Math.floor(rng() * 256);
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const toHex = (n) => n.toString(16).padStart(2, '0');
  const hex = Array.from(bytes, toHex).join('');
  return (
    hex.slice(0, 8) + '-' +
    hex.slice(8, 12) + '-' +
    hex.slice(12, 16) + '-' +
    hex.slice(16, 20) + '-' +
    hex.slice(20)
  );
}

function synthesizePersonas(description, num) {
  const seed = stringToSeed(description + '|' + num);
  const rng = mulberry32(seed);

  const firstNames = ["Alex","Jordan","Taylor","Casey","Robin","Sam","Avery","Morgan","Riley","Drew","Jamie","Quinn"];
  const lastNames = ["Chen","Garcia","Patel","O'Neal","Khan","Johnson","Singh","Kim","Martinez","Williams","Nguyen","Brown"];
  const occupations = [
    "Undergraduate Student","Graduate Student","Software Engineer","Barista","Freelance Designer","Marketing Intern","Teaching Assistant","Sales Associate","Content Creator","Research Assistant"
  ];
  const personalities = [
    "Analytical and cautious","Enthusiastic and outgoing","Pragmatic and skeptical","Empathetic listener","Detail-oriented planner","Creative risk-taker"
  ];
  const motivationPool = [
    "Improve health/fitness","Save money","Build social connections","Optimize time","Advance career skills","Reduce stress","Track progress with data","Stay motivated with gamification"
  ];
  const constraintPool = [
    "Limited budget","Time constraints","Privacy concerns","Beginner-level experience","Accessibility needs","Unreliable internet","Device storage limits"
  ];

  const personas = [];
  const used = new Set();
  for (let i = 0; i < num; i++) {
    let name = '';
    for (let tries = 0; tries < 20; tries++) {
      const candidate = `${pickRandom(rng, firstNames)} ${pickRandom(rng, lastNames)}`;
      if (!used.has(candidate)) { name = candidate; used.add(candidate); break; }
    }
    const age = Math.floor(rng() * (55 - 18 + 1)) + 18;
    const occupation = pickRandom(rng, occupations);
    const personality = pickRandom(rng, personalities);
    const motivations = sampleMany(rng, motivationPool, Math.floor(rng() * 2) + 2);
    const constraints = sampleMany(rng, constraintPool, Math.floor(rng() * 2) + 1);

    const background = `${name} is a ${age}-year-old ${occupation}. In the context of '${description}', they bring ${personality.toLowerCase()} energy.`;

    personas.push({
      id: uuid4(rng), name, age, occupation, background, motivations, constraints, personality
    });
  }
  return personas;
}

function renderPersonas(list) {
  const root = document.getElementById('personas');
  root.innerHTML = '';
  list.forEach(p => {
    const el = document.createElement('div');
    el.className = 'persona';
    el.innerHTML = `
      <h3>${p.name} — ${p.occupation} (${p.age})</h3>
      <div class="meta">${p.personality}</div>
      <div class="kv"><strong>Background:</strong> ${p.background}</div>
      <div class="kv"><strong>Motivations:</strong> ${p.motivations.join(', ')}</div>
      <div class="kv"><strong>Constraints:</strong> ${p.constraints.join(', ')}</div>
    `;
    root.appendChild(el);
  });
}

function download(filename, text) {
  const a = document.createElement('a');
  a.setAttribute('href', 'data:application/json;charset=utf-8,' + encodeURIComponent(text));
  a.setAttribute('download', filename);
  a.style.display = 'none';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

const state = { personas: [] };

document.addEventListener('DOMContentLoaded', () => {
  const description = document.getElementById('description');
  const count = document.getElementById('count');
  const countValue = document.getElementById('countValue');
  const generate = document.getElementById('generate');
  const downloadBtn = document.getElementById('download');
  const status = document.getElementById('status');

  count.addEventListener('input', () => { countValue.textContent = count.value; });

  generate.addEventListener('click', () => {
    const desc = (description.value || '').trim();
    if (!desc) {
      status.textContent = 'Please provide a short description to guide persona generation.';
      state.personas = [];
      renderPersonas(state.personas);
      downloadBtn.disabled = true;
      return;
    }
    const n = parseInt(count.value, 10) || 5;
    state.personas = synthesizePersonas(desc, n);
    status.textContent = `Generated ${state.personas.length} participants.`;
    renderPersonas(state.personas);
    downloadBtn.disabled = state.personas.length === 0;
  });

  downloadBtn.addEventListener('click', () => {
    const payload = JSON.stringify(state.personas, null, 2);
    download('personas.json', payload);
  });
});

