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

function testReasoningRequestContracts() {
  const messages = [{ role: 'user', content: 'Return JSON.' }];
  const responseFormat = {
    type: 'json_schema',
    json_schema: { name: 'result', strict: true, schema: { type: 'object', properties: {}, additionalProperties: false } },
  };
  const samplerFields = ['temperature', 'top_p', 'frequency_penalty', 'presence_penalty'];
  for (const model of [
    'gpt-5.6-luna', 'gpt-5', 'gpt-5-mini', 'gpt-5.6-luna-2026-10-01', 'gpt-6-preview', 'gpt-10',
    'o1', 'o1-preview', 'o1-2024-12-17', 'o3', 'o3-mini-2025-01-31', 'o4-mini',
  ]) {
    const config = { baseUrl: 'https://api.openai.com/v1', model };
    const probe = utils.buildConnectivityTestPayload(config);
    const stream = utils.buildStreamingChatPayload({ ...config, messages });
    const json = utils.buildChatCompletionPayload({
      ...config, messages, response_format: responseFormat,
      temperature: 0.1, top_p: 0.9, frequency_penalty: 0, presence_penalty: 0,
      max_tokens: 2048,
    });
    const jsonObject = utils.buildChatCompletionPayload({
      ...config, messages, temperature: 0.1, response_format: { type: 'json_object' },
    });
    const jsonFallback = utils.buildChatCompletionPayload({ ...config, messages, temperature: 0.1 });
    for (const payload of [probe, stream, json, jsonObject, jsonFallback]) {
      assert.equal(payload.model, model);
      assert.equal(Object.hasOwn(payload, 'max_tokens'), false);
      assert.ok(Number.isInteger(payload.max_completion_tokens) && payload.max_completion_tokens > 0);
      for (const field of samplerFields) assert.equal(Object.hasOwn(payload, field), false);
    }
    assert.ok(probe.max_completion_tokens >= 4096, 'Probe budget must leave reasoning headroom');
    assert.equal(stream.max_completion_tokens, utils.resolveMaxOutputTokens(config));
    assert.equal(stream.stream, true);
    assert.deepEqual(stream.messages, messages);
    assert.equal(json.max_completion_tokens, 2048, 'Explicit output budgets must survive translation');
    assert.deepEqual(json.response_format, responseFormat);
    assert.deepEqual(json.messages, messages);
    assert.deepEqual(jsonObject.response_format, { type: 'json_object' });
    assert.equal(jsonFallback.max_completion_tokens, jsonObject.max_completion_tokens);
    assert.equal(Object.hasOwn(jsonFallback, 'response_format'), false);
  }
}

function testRawModelAndProviderRequestSeparation() {
  const messages = [{ role: 'user', content: 'hi' }];
  const samplers = { temperature: 0.1, top_p: 0.9, frequency_penalty: 0, presence_penalty: 0 };
  for (const config of [
    { baseUrl: 'https://gateway.test/v1', model: 'vendor/gpt-5.6-luna' },
    { baseUrl: 'https://gateway.test/v1', model: 'gpt-4.1' },
    { baseUrl: 'https://gateway.test/v1', model: 'o2-custom' },
    { baseUrl: 'https://gateway.test/v1', model: 'o10-custom' },
    { baseUrl: 'https://api.deepseek.com', model: 'gpt-5.6-luna' },
    { baseUrl: 'https://gateway.test/v1', model: 'o3-mini', provider: 'deepseek' },
    { baseUrl: 'https://gateway.test/v1', model: 'deepseek-v4-pro' },
  ]) {
    const payload = utils.buildChatCompletionPayload({ ...config, ...samplers, messages, max_tokens: 1024 });
    assert.equal(payload.model, config.model);
    assert.equal(payload.max_tokens, 1024);
    assert.equal(Object.hasOwn(payload, 'max_completion_tokens'), false);
    for (const [field, value] of Object.entries(samplers)) assert.equal(payload[field], value);
    const probe = utils.buildConnectivityTestPayload(config);
    assert.equal(probe.max_tokens, 256);
    assert.equal(probe.temperature, 0);
  }
  const gateway = utils.buildChatCompletionPayload({
    baseUrl: 'https://gateway.test/v1', model: 'GPT-5.6-Luna', messages,
    max_tokens: 1024, max_completion_tokens: 768,
    response_format: { type: 'json_object' }, stream: true, stream_options: { include_usage: true },
  });
  assert.equal(gateway.model, 'GPT-5.6-Luna');
  assert.equal(gateway.max_completion_tokens, 768);
  assert.equal(Object.hasOwn(gateway, 'max_tokens'), false);
  assert.deepEqual(gateway.response_format, { type: 'json_object' });
  assert.equal(gateway.stream, true);
  assert.deepEqual(gateway.stream_options, { include_usage: true });
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

for (const test of [testEndpointsAndRawModels, testSecretResolutionAndProviderBoundaries, testProviderSpecificRequests, testReasoningRequestContracts, testRawModelAndProviderRequestSeparation, testBrowserDiagnosticsDoNotInventSuccess]) {
  test();
  console.log(`${test.name} passed`);
}
