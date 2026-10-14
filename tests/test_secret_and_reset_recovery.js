const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');

function sandbox() {
  const timers = new Map();
  let nextTimer = 0;
  const listeners = new Map();
  const context = {
    window: {
      location: { origin: 'https://tester.github.io', hostname: 'tester.github.io', pathname: '/papers/', href: 'https://tester.github.io/papers/' },
      addEventListener: (name, fn) => listeners.set(name, fn),
      removeEventListener: (name) => listeners.delete(name),
    },
    document: { readyState: 'loading', addEventListener() {} },
    console: { warn() {}, error() {}, log() {} },
    URL, AbortController,
    setTimeout(fn, ms) { const id = ++nextTimer; timers.set(id, { fn, ms }); return id; },
    clearTimeout: (id) => timers.delete(id),
    setInterval() { return 1; }, clearInterval() {},
  };
  vm.createContext(context);
  return { context, timers, listeners };
}

function secretSandbox() {
  const s = sandbox();
  s.context.location = s.context.window.location;
  vm.runInContext(fs.readFileSync('app/llm-config-utils.js', 'utf8'), s.context);
  s.context.window.DPRLLMConfigUtils = s.context.DPRLLMConfigUtils;
  const code = fs.readFileSync('app/secret.session.js', 'utf8')
    .replace(/\}\)\(\);\s*$/, 'window.probe = {fetchStaticSecretPayload, pingChatModels, init, setupOverlay, saveSummarizeSecretsToGithub, resolveRerankerConfig, RERANKER_PROFILES};})();');
  vm.runInContext(code, s.context);
  return s;
}

const response = (status, data) => ({
  ok: status >= 200 && status < 300, status, statusText: status === 401 ? 'Unauthorized' : '',
  json: async () => data, text: async () => 'test response',
});

async function testSecretReadFailuresAndRetry() {
  const { context, timers } = secretSandbox();
  let calls = 0;
  context.fetch = async () => { calls++; return response(503); };
  await assert.rejects(context.window.probe.fetchStaticSecretPayload(), /503/);
  assert.equal(calls, 2);
  context.fetch = async () => response(404);
  assert.equal(await context.window.probe.fetchStaticSecretPayload(), null);
  const payload = { salt: 'salt', iv: 'iv', ciphertext: 'cipher' };
  calls = 0;
  context.fetch = async () => ++calls === 1 ? response(503) : response(200, payload);
  assert.equal(await context.window.probe.fetchStaticSecretPayload(), payload);
  assert.equal(calls, 2);
  context.fetch = async () => response(200, null);
  await assert.rejects(context.window.probe.fetchStaticSecretPayload());
  context.fetch = async () => { throw new TypeError('Failed to fetch'); };
  await assert.rejects(context.window.probe.fetchStaticSecretPayload(), /Failed to fetch/);
  assert.equal(timers.size, 0);
}

async function testDeepSeekTimeoutAndHttpError() {
  const { context, timers } = secretSandbox();
  context.fetch = (_url, options) => new Promise((_resolve, reject) => {
    options.signal.addEventListener('abort', () => reject(options.signal.reason));
  });
  const entries = [{ model: 'deepseek-v4-flash', apiKey: 'test-only', baseUrl: 'https://api.deepseek.com' }];
  const pending = context.window.probe.pingChatModels(entries, null);
  const timer = [...timers.values()].find(t => t.ms === 20000);
  assert.ok(timer);
  timer.fn();
  await assert.rejects(pending);
  assert.equal(timers.size, 0);
  context.fetch = async () => response(401);
  await assert.rejects(context.window.probe.pingChatModels(entries, null), /HTTP 401/);
}

async function testGatewayProbeDistinguishesBrowserBlockingAndReachableFailure() {
  const { context, timers } = secretSandbox();
  const entries = [{ model: 'vendor/chat', apiKey: 'test-only', baseUrl: 'http://gateway.test:8080/v1' }];
  let calls = 0;
  context.fetch = async () => { calls++; return response(200, { choices: [{ message: { content: 'hello world' } }] }); };
  await assert.rejects(context.window.probe.pingChatModels(entries, null), error => error.code === 'BROWSER_UNVERIFIED');
  assert.equal(calls, 0, 'Mixed content is diagnosed without pretending a probe succeeded');
  entries[0].baseUrl = 'https://gateway.test/v1';
  context.fetch = async () => { throw new TypeError('Failed to fetch'); };
  await assert.rejects(context.window.probe.pingChatModels(entries, null), error => error.code === 'BROWSER_UNVERIFIED');
  context.fetch = async () => response(401);
  await assert.rejects(context.window.probe.pingChatModels(entries, null), error => !error.code && /HTTP 401/.test(error.message));
  context.fetch = async () => response(200, { choices: [{ message: { content: 'hello world' } }] });
  assert.deepEqual(Array.from(await context.window.probe.pingChatModels(entries, null)), ['vendor/chat']);
  assert.equal(timers.size, 0);
}

async function testGatewayWizardSavesRolesAndReopensWithoutChangingEndpoint() {
  const { context } = secretSandbox();
  Object.assign(context.window.location, { hostname: 'localhost', origin: 'https://localhost:8000', href: 'https://localhost:8000/' });
  const nodes = {};
  let radios = [];
  const makeNode = () => ({
    value: '', checked: false, textContent: '', style: {}, attrs: {}, children: [], listeners: {},
    classList: { add() {}, remove() {}, toggle() {} },
    addEventListener(name, fn) { if (!this.listeners[name]) this.listeners[name] = []; this.listeners[name].push(fn); },
    async emit(name) { for (const fn of this.listeners[name] || []) await fn({ currentTarget: this }); },
    setAttribute(name, value) { this.attrs[name] = value; }, getAttribute(name) { return this.attrs[name] || ''; },
    closest() { return this; }, appendChild(node) { this.children.push(node); }, replaceChildren() { this.children = []; }, focus() {},
  });
  nodes['secret-gate-overlay'] = makeNode();
  const modal = nodes['secret-gate-modal'] = makeNode();
  Object.defineProperty(modal, 'innerHTML', { set(value) {
    for (const match of value.matchAll(/id="([^"]+)"/g)) nodes[match[1]] = makeNode();
    radios = Array.from(value.matchAll(/name="secret-setup-provider" value="([^"]+)"/g), match => Object.assign(makeNode(), { value: match[1] }));
  } });
  const stored = new Map([['dpr_secret_password_v1', 'Test-password-123!']]);
  context.window.localStorage = { getItem: key => stored.get(key), setItem: (key, value) => stored.set(key, value) };
  context.document.getElementById = id => nodes[id] || null;
  context.document.querySelectorAll = () => radios;
  context.document.createElement = () => makeNode();
  context.document.dispatchEvent = () => {};
  context.requestAnimationFrame = fn => fn();
  context.crypto = require('node:crypto').webcrypto;
  context.window.crypto = context.crypto;
  context.TextEncoder = TextEncoder;
  context.TextDecoder = TextDecoder;
  context.btoa = value => Buffer.from(value, 'binary').toString('base64');
  context.window.decoded_secret_private = { readState: { paper: true }, createdAt: 'original' };
  context.window.probe.setupOverlay(false);
  context.window.DPRSecretSetup.openStep2();
  assert.deepEqual(radios.map(radio => radio.value), ['deepseek', 'openai-compatible']);
  assert.equal(radios.find(radio => radio.checked).value, 'deepseek');
  radios.forEach(radio => { radio.checked = radio.value === 'openai-compatible'; });
  await radios[1].emit('change');
  assert.equal(nodes['secret-setup-custom-section'].style.display, 'block');
  assert.equal(nodes['secret-setup-deepseek-section'].style.display, 'none');
  nodes['secret-setup-custom-api-key'].value = 'test-only';
  nodes['secret-setup-custom-base-url'].value = 'http://gateway.test:8080/v1/';
  nodes['secret-setup-custom-model-1'].value = 'vendor/chat, vendor/second';
  nodes['secret-setup-custom-model-2'].value = 'vendor/summary';
  nodes['secret-setup-filter-model'].value = 'vendor/filter';
  nodes['secret-setup-rewrite-model'].value = 'vendor/rewrite';
  let localSave;
  context.fetch = async (url, options) => {
    localSave = JSON.parse(options.body);
    return response(200, { ok: true });
  };
  await nodes['secret-setup-custom-test'].emit('click');
  assert.equal(nodes['secret-setup-backend-only-row'].style.display, 'block');
  await nodes['secret-setup-generate'].emit('click');
  assert.equal(localSave, undefined, 'Unverified config requires explicit acknowledgement');
  nodes['secret-setup-backend-only'].checked = true;
  await nodes['secret-setup-generate'].emit('click');
  assert.ok(localSave, 'Acknowledged backend-only configuration is saved');
  assert.equal(localSave.secret.llmProvider.type, 'openai-compatible');
  assert.equal(localSave.secret.llmProvider.filterModel, 'vendor/filter');
  assert.equal(localSave.secret.llmProvider.rewriteModel, 'vendor/rewrite');
  assert.equal(localSave.secret.summarizedLLM.baseUrl, 'http://gateway.test:8080/v1');
  assert.equal(localSave.secret.summarizedLLM.model, 'vendor/summary');
  assert.deepEqual(localSave.secret.chatLLMs[0].models, ['vendor/chat', 'vendor/second']);
  assert.deepEqual(localSave.secret.readState, { paper: true });
  assert.equal(localSave.secret.createdAt, 'original');
  for (const field of ['salt', 'iv', 'ciphertext']) assert.equal(typeof localSave.payload[field], 'string');
  context.window.DPRSecretSetup.openStep2();
  assert.equal(radios.find(radio => radio.checked).value, 'openai-compatible');
  assert.equal(nodes['secret-setup-custom-base-url'].value, 'http://gateway.test:8080/v1');
  assert.equal(nodes['secret-setup-custom-model-2'].value, 'vendor/summary');
  assert.equal(nodes['secret-setup-filter-model'].value, 'vendor/filter');
  assert.equal(nodes['secret-setup-rewrite-model'].value, 'vendor/rewrite');
  nodes['secret-setup-custom-base-url'].value = 'https://gateway.test/v1';
  await nodes['secret-setup-custom-base-url'].emit('input');
  context.fetch = async () => response(401);
  await nodes['secret-setup-custom-test'].emit('click');
  assert.equal(nodes['secret-setup-backend-only-row'].style.display, 'none');
  localSave = undefined;
  await nodes['secret-setup-generate'].emit('click');
  assert.equal(localSave, undefined, 'Reachable HTTP rejection cannot be bypassed as a browser limitation');
}


async function testSecretErrorUiPreservesPasswordAndCanRetry() {
  const { context } = secretSandbox();
  const nodes = {};
  const makeNode = () => ({
    style: {}, classList: { add() {}, remove() {}, toggle() {} }, listeners: {},
    addEventListener(name, fn) { this.listeners[name] = fn; },
  });
  nodes['secret-gate-overlay'] = makeNode();
  const modal = nodes['secret-gate-modal'] = makeNode();
  let html = '';
  Object.defineProperty(modal, 'innerHTML', { get: () => html, set(value) {
    html = value;
    for (const match of value.matchAll(/id="([^"]+)"/g)) nodes[match[1]] = makeNode();
  } });
  const stored = new Map([['dpr_secret_password_v1', 'saved-password']]);
  context.window.localStorage = { getItem: k => stored.get(k), removeItem: k => stored.delete(k) };
  context.document.getElementById = id => nodes[id] || null;
  context.requestAnimationFrame = fn => fn();
  context.fetch = async () => response(503);
  context.window.probe.init();
  for (let i = 0; i < 30; i++) await Promise.resolve();
  assert.match(html, /暂时无法读取密钥配置/);
  assert.equal(html.includes('新配置指引'), false);
  assert.equal(stored.get('dpr_secret_password_v1'), 'saved-password');
  context.fetch = async () => response(404);
  const retry = nodes['secret-load-retry'];
  retry.listeners.click({ currentTarget: retry });
  for (let i = 0; i < 30; i++) await Promise.resolve();
  assert.match(html, /新配置指引/);
}

async function testResetWaitsForAcknowledgement() {
  const { context, listeners } = sandbox();
  context.window.DPR_ACCESS_MODE = 'full';
  context.window.prompt = () => 'RESET_ALL';
  let release, calls = 0;
  context.window.DPRWorkflowRunner = { runWorkflowByKey() {
    calls++;
    return new Promise(resolve => { release = resolve; });
  } };
  const code = fs.readFileSync('app/subscriptions.manager.js', 'utf8')
    .replace('__test: {', '__test: {runResetContent, setResetButton: b => {resetContentBtn=b;},');
  vm.runInContext(code, context);
  const api = context.window.SubscriptionsManager.__test;
  const button = { disabled: false };
  api.setResetButton(button);
  const msg = { textContent: '', style: {} };
  const pending = api.runResetContent(msg);
  assert.equal(/已发起|已提交/.test(msg.textContent), false);
  assert.equal(button.disabled, true);
  assert.ok(listeners.has('beforeunload'));
  await api.runResetContent(msg);
  assert.equal(calls, 1);
  release(false);
  await pending;
  assert.equal(/已发起|已提交/.test(msg.textContent), false);
  assert.equal(button.disabled, false);
  assert.equal(listeners.has('beforeunload'), false);
  context.window.DPRWorkflowRunner.runWorkflowByKey = async () => true;
  await api.runResetContent(msg);
  assert.match(msg.textContent, /已提交/);
  context.window.DPRWorkflowRunner.runWorkflowByKey = async () => { throw new Error('offline'); };
  await api.runResetContent(msg);
  assert.match(msg.textContent, /offline/);
  assert.equal(button.disabled, false);
}

async function testWorkflowReturnsDispatchResultBeforeMonitoring() {
  for (const [status, monitorFailure] of [[204, false], [403, false], [204, true]]) {
    const { context } = sandbox();
    context.window.decoded_secret_private = { github: { token: 'test-only' } };
    context.fetch = async (url, init = {}) => {
      if (url.endsWith('/dispatches')) return response(status);
      if (url.includes('event=workflow_dispatch')) return monitorFailure ? response(503) : new Promise(() => {});
      if (url.includes('/runs?')) return response(200, { workflow_runs: [] });
      return response(200, { default_branch: 'main', fork: true });
    };
    const code = fs.readFileSync('app/workflows.runner.js', 'utf8')
      .replace(/\r?\n  return \{\r?\n/, '\n  return {\n    dispatchAndMonitor, setUi: (s,r) => {statusEl=s;runsEl=r;},\n');
    vm.runInContext(code, context);
    const api = context.window.DPRWorkflowRunner;
    const statusEl = { textContent: '', style: {}, classList: { toggle() {} } };
    api.setUi(statusEl, { innerHTML: '' });
    let settled = false, value;
    api.dispatchAndMonitor({ key: 'reset-content', id: 'reset-content.yml' }).then(v => { settled = true; value = v; });
    for (let i = 0; i < 50; i++) await Promise.resolve();
    assert.equal(settled, true, 'dispatch acknowledgement must not wait for run-list polling');
    assert.equal(value, status === 204);
    if (monitorFailure) assert.match(statusEl.textContent, /任务已提交，但读取进度失败/);
  }
}

async function testLegacyLocalRerankerMovesToCloud() {
  const {context} = secretSandbox();
  const value = context.window.probe.resolveRerankerConfig({rerankerLLM:{profile:'local-qwen3-0.6b',provider:'local',baseUrl:'http://localhost:9999',apiKey:'private-local-test'}});
  assert.equal(value.provider,'public_zwwen');
  assert.equal(value.baseUrl,'https://zwwen.online/rerank');
  assert.equal(value.apiKey,'');
  assert.equal(context.window.probe.RERANKER_PROFILES.some(p => p.provider==='local'),false);
}

(async () => {
  for (const test of [testLegacyLocalRerankerMovesToCloud, testSecretReadFailuresAndRetry, testDeepSeekTimeoutAndHttpError, testGatewayProbeDistinguishesBrowserBlockingAndReachableFailure, testGatewayWizardSavesRolesAndReopensWithoutChangingEndpoint, testSecretErrorUiPreservesPasswordAndCanRetry,
    testResetWaitsForAcknowledgement, testWorkflowReturnsDispatchResultBeforeMonitoring]) {
    await test();
    console.log(test.name + ' passed');
  }
})().catch(error => { console.error(error); process.exit(1); });
