// Minimal LLM client wrapper. Users provide API key, base URL, and model at runtime.

export class LLMClient {
  constructor(getSettings) {
    this.getSettings = getSettings; // () => ({ apiKey, baseUrl, model })
  }

  async complete(systemPrompt, userPrompt, options = {}) {
    const { apiKey, baseUrl, model } = this.getSettings();
    if (!apiKey || !baseUrl || !model) throw new Error('Missing LLM settings.');

    // OpenAI-compatible JSON.
    const payload = {
      model,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      temperature: options.temperature ?? 0.7,
      response_format: options.response_format ?? undefined
    };

    const resp = await fetch(`${baseUrl.replace(/\/$/, '')}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify(payload)
    });
    if (!resp.ok) {
      const txt = await resp.text();
      throw new Error(`LLM error: ${resp.status} ${txt}`);
    }
    const data = await resp.json();
    const content = data.choices?.[0]?.message?.content ?? '';
    return content;
  }
}

export class PersonaGeneratorAgent {
  constructor(llm) { this.llm = llm; }
  async run(description, count) {
    const system = 'You create diverse, realistic personas with distinct backgrounds, motivations, constraints, and personalities. Output strict JSON array.';
    const user = `Description: ${description}\nCount: ${count}\nReturn fields: id (uuid), name, age, occupation, background, motivations[], constraints[], personality.`;
    const content = await this.llm.complete(system, user);
    return safeJson(content);
  }
}

export class FrameworkAgent {
  constructor(llm) { this.llm = llm; }
  async run(topic, goals, duration, phasesCsv, personas) {
    const system = 'Design a focus group framework with phases, prompts, timings, and moderator cues. Output strict JSON.';
    const user = `Topic: ${topic}\nGoals: ${goals}\nDurationMinutes: ${duration}\nPhases: ${phasesCsv}\nParticipants: ${JSON.stringify(personas).slice(0, 5000)}\nReturn: { phases: [{ name, minutes, prompts:[], moderatorCues:[] }], guidelines: [] }`;
    const content = await this.llm.complete(system, user);
    return safeJson(content);
  }
}

export class SimulationAgent {
  constructor(llm) { this.llm = llm; }
  async run(personas, framework) {
    const system = 'Simulate realistic group discussion with natural turn-taking, interruptions, and varied tone. Output JSON transcript.';
    const user = `Participants: ${JSON.stringify(personas).slice(0, 5000)}\nFramework: ${JSON.stringify(framework).slice(0, 5000)}\nReturn: { transcript: [{ speaker, text, phase }], spontaneous: [{reactor, trigger, text}] }`;
    const content = await this.llm.complete(system, user);
    return safeJson(content);
  }
}

export class SummaryAgent {
  constructor(llm) { this.llm = llm; }
  async run(schemaJson, transcript) {
    const system = 'Produce a report strictly conforming to the provided JSON schema. Do not add extra fields.';
    const user = `Schema: ${schemaJson}\nTranscript: ${JSON.stringify(transcript).slice(0, 8000)}\nReturn: Strict JSON matching schema.`;
    const content = await this.llm.complete(system, user);
    return safeJson(content);
  }
}

export class QAAssistantAgent {
  constructor(llm) { this.llm = llm; }
  async run(question, transcript) {
    const system = 'Answer questions about the transcript with evidence quotes. Output JSON: { answer, quotes: [{speaker, quote}], confidence: 0-1 }';
    const user = `Question: ${question}\nTranscript: ${JSON.stringify(transcript).slice(0, 8000)}`;
    const content = await this.llm.complete(system, user);
    return safeJson(content);
  }
}

function safeJson(text) {
  try {
    const start = text.indexOf('{') !== -1 ? Math.min(...[...text].map((_,i)=>text[i]==='{"'?i:Infinity)) : Infinity;
  } catch {}
  try { return JSON.parse(text); } catch {
    const fence = /```[a-zA-Z]*\n([\s\S]*?)```/m;
    const m = text.match(fence);
    if (m) { try { return JSON.parse(m[1]); } catch {} }
    // Try to extract JSON substring
    const first = text.indexOf('{');
    const last = text.lastIndexOf('}');
    if (first !== -1 && last !== -1 && last > first) {
      try { return JSON.parse(text.slice(first, last + 1)); } catch {}
    }
    const arrFirst = text.indexOf('[');
    const arrLast = text.lastIndexOf(']');
    if (arrFirst !== -1 && arrLast !== -1 && arrLast > arrFirst) {
      try { return JSON.parse(text.slice(arrFirst, arrLast + 1)); } catch {}
    }
    throw new Error('Failed to parse agent JSON response');
  }
}

