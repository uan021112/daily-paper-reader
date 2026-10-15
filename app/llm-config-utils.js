(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) {
    module.exports = api;
  }
  if (root) {
    root.DPRLLMConfigUtils = api;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  const DEFAULT_DEEPSEEK_BASE_URL = 'https://api.deepseek.com';
  const DEFAULT_DEEPSEEK_CHAT_MODELS = [
    'deepseek-v4-flash',
    'deepseek-v4-pro',
  ];
  const DEEPSEEK_V4_MAX_OUTPUT_TOKENS = 393216;
  const DEEPSEEK_PRESETS = Object.freeze({
    deepseek: Object.freeze({
      key: 'deepseek',
      label: 'DeepSeek 官方',
      baseUrl: 'https://api.deepseek.com',
      models: Object.freeze(['deepseek-v4-flash', 'deepseek-v4-pro']),
    }),
  });

  const normalizeText = (value) => String(value || '').trim();

  const normalizeBaseUrlForStorage = (value) => {
    let text = normalizeText(value).replace(/\/+$/g, '');
    if (!text) return '';
    text = text.replace(/\/chat\/completions$/i, '');
    return text.replace(/\/+$/g, '');
  };

  const buildChatCompletionsEndpoint = (value) => {
    const raw = normalizeText(value).replace(/\/+$/g, '');
    if (!raw) return '';
    if (/\/chat\/completions$/i.test(raw)) return raw;
    const normalized = normalizeBaseUrlForStorage(raw);
    if (!normalized) return '';
    if (/\/v\d+$/i.test(normalized)) {
      return `${normalized}/chat/completions`;
    }
    return `${normalized}/v1/chat/completions`;
  };

  const sanitizeModelList = (values, maxCount = 3) => {
    const rawList = Array.isArray(values) ? values : [values];
    const out = [];
    const seen = new Set();
    for (const value of rawList) {
      const parts = String(value || '')
        .split(/[\n,]+/)
        .map((item) => normalizeText(item))
        .filter(Boolean);
      for (const name of parts) {
        const key = name.toLowerCase();
        if (!key || seen.has(key)) continue;
        seen.add(key);
        out.push(name);
        if (out.length >= Math.max(Number(maxCount) || 0, 1)) {
          return out;
        }
      }
    }
    return out;
  };

  const resolveChatModels = (secret) => {
    const safeSecret = secret && typeof secret === 'object' ? secret : {};
    const chatList = Array.isArray(safeSecret.chatLLMs) ? safeSecret.chatLLMs : [];
    const models = [];
    const seen = new Set();
    chatList.forEach((item) => {
      if (!item || typeof item !== 'object') return;
      const baseUrl = normalizeBaseUrlForStorage(item.baseUrl || '');
      const apiKey = normalizeText(item.apiKey || '');
      const modelNames = sanitizeModelList(item.models || [], 99);
      if (!baseUrl || !apiKey || !modelNames.length) return;
      modelNames.forEach((name) => {
        const dedupeKey = `${name.toLowerCase()}\u0000${baseUrl}\u0000${apiKey}`;
        if (seen.has(dedupeKey)) return;
        seen.add(dedupeKey);
        models.push({
          name,
          apiKey,
          baseUrl,
          provider: normalizeText(item.provider || (safeSecret.llmProvider || {}).type)
            || inferChatApiProfile(baseUrl, name),
        });
      });
    });
    return models;
  };

  const resolveSummaryLLM = (secret) => {
    const safeSecret = secret && typeof secret === 'object' ? secret : {};
    const summarized = safeSecret.summarizedLLM || {};
    const baseUrl = normalizeBaseUrlForStorage(summarized.baseUrl || '');
    const apiKey = normalizeText(summarized.apiKey || '');
    const model = normalizeText(summarized.model || '');
    if (baseUrl && apiKey && model) {
      return { baseUrl, apiKey, model };
    }

    const chatModels = resolveChatModels(safeSecret);
    if (!chatModels.length) return null;
    return {
      baseUrl: normalizeBaseUrlForStorage(chatModels[0].baseUrl || ''),
      apiKey: normalizeText(chatModels[0].apiKey || ''),
      model: normalizeText(chatModels[0].name || ''),
    };
  };

  const inferProviderType = (secret) => {
    const safeSecret = secret && typeof secret === 'object' ? secret : {};
    const llmProvider = safeSecret.llmProvider || {};
    const explicit = normalizeText(llmProvider.type || llmProvider.provider || '').toLowerCase();
    if (explicit === 'deepseek' || explicit === 'openai-compatible') return explicit;
    const summary = safeSecret.summarizedLLM || {};
    const chat = (safeSecret.chatLLMs || [])[0] || {};
    const baseUrl = summary.baseUrl || chat.baseUrl || '';
    return baseUrl ? inferChatApiProfile(baseUrl, summary.model) : 'deepseek';
  };

  const getDeepSeekPreset = (key) => {
    const presetKey = normalizeText(key).toLowerCase();
    const preset = DEEPSEEK_PRESETS[presetKey];
    if (!preset) return null;
    return {
      key: preset.key,
      label: preset.label,
      baseUrl: preset.baseUrl,
      models: [...preset.models],
    };
  };

  const inferChatApiProfile = (baseUrl, model, provider) => {
    const explicit = normalizeText(provider).toLowerCase();
    if (explicit === 'deepseek' || explicit === 'openai-compatible') return explicit;
    const normalizedBaseUrl = normalizeBaseUrlForStorage(baseUrl || '').toLowerCase();
    if (/(^|\/\/)(api\.)?deepseek\.com(?:$|\/)/i.test(normalizedBaseUrl)) {
      return 'deepseek';
    }
    return 'openai-compatible';
  };

  const resolveJsonResponseMode = ({ baseUrl, model, provider, preferSchema = true }) => {
    return preferSchema && inferChatApiProfile(baseUrl, model, provider) !== 'deepseek'
      ? 'json_schema' : 'json_object';
  };

  const isDeepSeekV4Model = (model) => {
    const normalizedModel = normalizeText(model || '').toLowerCase();
    return normalizedModel === 'deepseek-v4-flash' || normalizedModel === 'deepseek-v4-pro';
  };

  const resolveMaxOutputTokens = ({ baseUrl, model, provider } = {}) => {
    const profile = inferChatApiProfile(baseUrl, model, provider);
    if (profile === 'deepseek' && isDeepSeekV4Model(model)) {
      return DEEPSEEK_V4_MAX_OUTPUT_TOKENS;
    }
    return profile === 'openai-compatible' ? 16384 : null;
  };


  const browserRequestError = (endpoint, error, pageUrl) => {
    const page = pageUrl || (typeof location !== 'undefined' ? location.href : '');
    let mixedContent = false;
    try {
      const target = new URL(endpoint);
      const host = target.hostname.toLowerCase();
      mixedContent = new URL(page).protocol === 'https:' && target.protocol === 'http:'
        && !['localhost', '127.0.0.1', '[::1]'].includes(host);
    } catch {
      // URL validity is checked by the configuration form.
    }
    if (!mixedContent && (!error || error.name !== 'TypeError')) return error || null;
    const diagnostic = new Error(mixedContent
      ? 'HTTPS 页面不能调用公共 HTTP 网关（浏览器 mixed content 限制）。后端可保存 HTTP 配置，但浏览器聊天需要 HTTPS 网关及允许本站的 CORS。浏览器连接未验证。'
      : '浏览器未收到可读响应：可能是 CORS、网络、TLS 或网关不可达。请检查网关允许本站 Origin、Authorization 和 Content-Type 的 CORS 预检；浏览器无法确认后端配置是否有效。');
    diagnostic.code = 'BROWSER_UNVERIFIED';
    return diagnostic;
  };

  const validateBaseUrl = (value) => {
    const normalized = normalizeBaseUrlForStorage(value);
    let url;
    try { url = new URL(normalized); } catch { throw new Error('请填写有效的 HTTP/HTTPS Base URL。'); }
    if (!['http:', 'https:'].includes(url.protocol) || url.username || url.password || url.search || url.hash) {
      throw new Error('Base URL 必须是无用户名、密码、查询参数或片段的 HTTP/HTTPS 地址。');
    }
    return normalized;
  };

  const buildCanonicalLlmSecrets = ({ providerType, summarizedApiKey, summarizedBaseUrl, summarizedModel, filterModel, rewriteModel }) => {
    return [
      { name: 'LLM_PROVIDER', value: providerType },
      { name: 'LLM_API_KEY', value: normalizeText(summarizedApiKey) },
      { name: 'LLM_BASE_URL', value: normalizeBaseUrlForStorage(summarizedBaseUrl) },
      { name: 'LLM_MODEL', value: normalizeText(summarizedModel) },
      { name: 'LLM_FILTER_MODEL', value: normalizeText(filterModel || summarizedModel) },
      { name: 'LLM_REWRITE_MODEL', value: normalizeText(rewriteModel || summarizedModel) },
    ];
  };

  const buildStreamingChatPayload = ({ baseUrl, model, provider, messages }) => {
    const payload = {
      model: normalizeText(model),
      messages: Array.isArray(messages) ? messages : [],
      stream: true,
    };
    const maxTokens = resolveMaxOutputTokens({ baseUrl, model, provider });
    if (maxTokens) {
      payload.max_tokens = maxTokens;
    }
    return payload;
  };

  const buildConnectivityTestPayload = ({ baseUrl, model }) => {
    const normalizedModel = normalizeText(model);
    return {
      model: normalizedModel,
      messages: [
        {
          role: 'system',
          content: 'Reply with exactly: hello world',
        },
        {
          role: 'user',
          content: 'hello world',
        },
      ],
      temperature: 0,
      max_tokens: 256,
    };
  };

  return {
    DEFAULT_DEEPSEEK_BASE_URL,
    DEFAULT_DEEPSEEK_CHAT_MODELS,
    DEEPSEEK_PRESETS,
    normalizeText,
    normalizeBaseUrlForStorage,
    buildChatCompletionsEndpoint,
    sanitizeModelList,
    resolveChatModels,
    resolveSummaryLLM,
    inferProviderType,
    getDeepSeekPreset,
    inferChatApiProfile,
    resolveJsonResponseMode,
    isDeepSeekV4Model,
    resolveMaxOutputTokens,
    buildStreamingChatPayload,
    buildConnectivityTestPayload,
    browserRequestError,
    validateBaseUrl,
    buildCanonicalLlmSecrets,
  };
});
