const assert = require('node:assert/strict');
const utils = require('../app/llm-config-utils.js');

function testEndpointsAndRawModels() {
  assert.equal(utils.normalizeBaseUrlForStorage('http://gateway.test:8080/v1/chat/completions/'), 'http://gateway.test:8080/v1');
  assert.equal(utils.buildChatCompletionsEndpoint('http://gateway.test:8080/v1'), 'http://gateway.test:8080/v1/chat/completions');
  assert.equal(utils.buildChatCompletionsEndpoint('https://gateway.test/custom-root'), 'https://gateway.test/custom-root/v1/chat/completions');
  assert.deepEqual(utils.sanitizeModelList(' vendor/model-A, vendor/model-A\nvendor/model-B ', 99), ['vendor/model-A', 'vendor/model-B']);
  assert.equal(utils.validateBaseUrl('http://gateway.test:8080/v1/'), 'http://gateway.test:8080/v1');
  for (const url of ['file:///tmp/model', 'not-a-url', 'https://user:key@gateway.test', 'https://gateway.test/?key=secret']) {
    assert.throws(() => utils.validateBaseUrl(url));
  }
}

function testSecretResolutionAndProviderBoundaries() {
  const secret = {
    llmProvider: { type: 'openai-compatible' },
    summarizedLLM: { apiKey: 'test-key', baseUrl: 'http://gateway.test:8080/v1/', model: 'vendor/summary' },
    chatLLMs: [{ apiKey: 'test-key', baseUrl: 'http://gateway.test:8080/v1/', models: ['vendor/chat', 'deepseek-v4-pro'] }],
  };
  assert.equal(utils.resolveSummaryLLM(secret).model, 'vendor/summary');
  assert.equal(utils.resolveSummaryLLM(secret).baseUrl, 'http://gateway.test:8080/v1');
  assert.deepEqual(utils.resolveChatModels(secret).map(item => item.name), ['vendor/chat', 'deepseek-v4-pro']);
  assert.equal(utils.inferProviderType(secret), 'openai-compatible');
  assert.equal(utils.inferProviderType({ summarizedLLM: { baseUrl: 'https://api.deepseek.com' } }), 'deepseek');
  assert.equal(utils.inferProviderType({ summarizedLLM: { baseUrl: 'https://gateway.test/v1', model: 'deepseek-v4-pro' } }), 'openai-compatible');
  assert.equal(utils.inferChatApiProfile('https://gateway.test/v1', 'deepseek-v4-pro'), 'openai-compatible');
  assert.equal(utils.inferChatApiProfile('https://api.deepseek.com', 'custom', 'openai-compatible'), 'openai-compatible');
  assert.equal(utils.resolveSummaryLLM({ chatLLMs: secret.chatLLMs }).model, 'vendor/chat');
}

function testProviderSpecificRequests() {
  const messages = [{ role: 'user', content: 'hi' }];
  const gateway = { baseUrl: 'https://gateway.test/v1', model: 'deepseek-v4-pro' };
  const gatewayPayload = utils.buildStreamingChatPayload({ ...gateway, messages });
  const nativePayload = utils.buildStreamingChatPayload({ baseUrl: 'https://api.deepseek.com', model: 'deepseek-v4-pro', messages });
  assert.ok(gatewayPayload.max_tokens <= 16384);
  assert.ok(gatewayPayload.max_tokens < nativePayload.max_tokens);
  assert.equal(utils.resolveJsonResponseMode(gateway), 'json_schema');
  assert.equal(utils.resolveJsonResponseMode({ ...gateway, preferSchema: false }), 'json_object');
  assert.equal(utils.resolveJsonResponseMode({ baseUrl: 'https://api.deepseek.com', model: 'deepseek-v4-flash' }), 'json_object');
}


function testBrowserDiagnosticsDoNotInventSuccess() {
  const httpsPage = 'https://reader.test/papers/';
  const mixed = utils.browserRequestError('http://gateway.test:8080/v1/chat/completions', null, httpsPage);
  assert.equal(mixed.code, 'BROWSER_UNVERIFIED');
  assert.equal(utils.browserRequestError('http://localhost:8080/v1/chat/completions', null, httpsPage), null);
  assert.equal(utils.browserRequestError('https://gateway.test/v1/chat/completions', null, httpsPage), null);
  const cors = utils.browserRequestError('https://gateway.test/v1/chat/completions', new TypeError('Failed to fetch'), httpsPage);
  assert.equal(cors.code, 'BROWSER_UNVERIFIED');
  const rejected = new Error('HTTP 401');
  assert.equal(utils.browserRequestError('https://gateway.test/v1/chat/completions', rejected, httpsPage), rejected);
}

for (const test of [testEndpointsAndRawModels, testSecretResolutionAndProviderBoundaries, testProviderSpecificRequests, testBrowserDiagnosticsDoNotInventSuccess]) {
  test();
  console.log(`${test.name} passed`);
}
