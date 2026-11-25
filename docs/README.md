<div class="dpr-home-notice-card dpr-home-panel">
  <div class="dpr-home-notice-header dpr-home-panel-header">
    <h3 class="dpr-home-notice-title">公告与更新</h3>
    <a class="dpr-home-notice-tutorial" href="#/tutorial/README">使用教程 <span aria-hidden="true">›</span></a>
  </div>
  <div class="dpr-home-notice-entry">
    <time class="dpr-home-notice-date" datetime="2026-10-14">10.14</time>
    <div>
      <strong class="dpr-home-notice-entry-title">支持自有 API 网关</strong>
      <span class="dpr-home-notice-entry-summary">密钥设置新增 OpenAI-compatible / Sub2API 选项，可分别配置聊天、总结、筛选和改写模型，保留 DeepSeek。网页直连仍需 HTTPS 与 CORS。</span>
    </div>
  </div>
  <div class="dpr-home-notice-entry">
    <time class="dpr-home-notice-date" datetime="2026-10-05">10.05</time>
    <div>
      <strong class="dpr-home-notice-entry-title">medRxiv 自动更新已恢复</strong>
      <span class="dpr-home-notice-entry-summary">修复超长摘要导致的向量生成失败，维护任务现会限制单条 embedding 文本长度并分片写入。受影响范围已重新同步，公开读取、关键词检索与语义检索均已验证。</span>
    </div>
  </div>
  <div class="dpr-home-notice-entry">
    <time class="dpr-home-notice-date" datetime="2026-09-16">09.16</time>
    <div>
      <strong class="dpr-home-notice-entry-title">日报跨日重复推荐已修复</strong>
      <span class="dpr-home-notice-entry-summary">历史推荐现按原始召回标签与 arXiv 论文标识去重，暂停词条不再参与评分；同一专题次日不会重复推荐相同论文。已有历史页面保留，不自动删除。</span>
    </div>
  </div>
  <div class="dpr-home-site-stats" data-dpr-site-stats hidden aria-live="polite">
    <span>今天有 <strong class="dpr-home-site-stat-value" data-dpr-daily-readers>--</strong> 人在看论文</span>
    <span class="dpr-home-site-stat-separator" aria-hidden="true">·</span>
    <span>昨天有 <strong class="dpr-home-site-stat-value" data-dpr-yesterday-readers>--</strong> 人在看论文</span>
    <span class="dpr-home-site-stat-separator" aria-hidden="true">·</span>
    <span>已有 <strong class="dpr-home-site-stat-value" data-dpr-fork-count>--</strong> 人加入 Daily Paper Reader</span>
    <span class="dpr-home-history">
      <button type="button" class="dpr-home-history-trigger" data-dpr-history-trigger aria-label="查看最近 14 天阅读趋势"><span aria-hidden="true">🔍</span></button>
      <span class="dpr-home-history-popover" data-dpr-history-popover role="tooltip">
        <span class="dpr-home-history-header">近 14 天阅读趋势</span>
        <span class="dpr-home-history-meta">
          <span data-dpr-history-range>--</span>
          <span>峰值 <strong data-dpr-history-peak>--</strong></span>
        </span>
        <span class="dpr-home-history-chart" data-dpr-history-chart></span>
      </span>
    </span>
  </div>
</div>

<div class="dpr-home-dashboard-grid">
<section class="dpr-home-dashboard-card dpr-home-report-card">
  <div class="dpr-home-dashboard-header">
    <div>
      <span class="dpr-home-dashboard-kicker">2026-11-25</span>
      <h3 class="dpr-home-dashboard-title">今日汇总</h3>
    </div>
    <strong class="dpr-home-dashboard-count">共 28 篇</strong>
  </div>
  <dl class="dpr-home-dashboard-stats">
    <div class="dpr-home-dashboard-stat"><dt>累计更新</dt><dd>1 次</dd></div>
    <div class="dpr-home-dashboard-stat"><dt>精读</dt><dd>13</dd></div>
    <div class="dpr-home-dashboard-stat"><dt>速读</dt><dd>15</dd></div>
  </dl>
  <p class="dpr-home-dashboard-body">最近更新：2026-11-25 03:44:59 UTC<br>状态：成功</p>
</section>
<section class="dpr-home-dashboard-card dpr-home-brief-card">
  <div class="dpr-home-dashboard-header">
    <div>
      <span class="dpr-home-dashboard-kicker">合并后生成</span>
      <h3 class="dpr-home-dashboard-title">今日简报</h3>
    </div>
    <strong class="dpr-home-dashboard-count">AI</strong>
  </div>
  <div class="dpr-home-dashboard-body">
<p>今日共生成 28 篇推荐（精读 13 篇，速读 15 篇）</p>
<p>精读：《From Vision to Interaction: Evaluating Dynamic Social Intelligence of VLM Agents in ALIVE-World》（9.0/10）, 《Point Dynamics as Proxy for Robotic World Models》（9.0/10）</p>
<p>速读：《CarlHOI: Counterfactual Predictive Imagination for Generalizable Multi-Humanoid Object Interaction under Constrained Environments》（8.5/10）, 《Beyond Episodic Recall: Experience-to-Knowledge Evolution for Lifelong Embodied Navigation》（8.0/10）, 《SpatialMind: Adaptive Multi-Level Geometric Fusion for Spatial Reasoning in Multimodal Large Language Models》（8.0/10）</p>
<p>这些结果覆盖了当下较热的方向，建议先看精读区论文的关键问题与方法。</p>
  </div>
</section>
<section class="dpr-home-dashboard-card dpr-home-deep-card">
  <div class="dpr-home-dashboard-header">
    <div>
      <span class="dpr-home-dashboard-kicker">今日累计</span>
      <h3 class="dpr-home-dashboard-title">精读推荐</h3>
    </div>
    <strong class="dpr-home-dashboard-count">13 篇</strong>
  </div>
  <div class="dpr-home-dashboard-body">
<ul class="dpr-home-dashboard-paper-list"><li><span class="dpr-home-dashboard-paper-title" title="From Vision to Interaction: Evaluating Dynamic Social Intelligence of VLM Agents in ALIVE-World">From Vision to Interaction: Evaluating Dynamic Social Intelligence of VLM Agents in ALIVE-World</span></li><li><span class="dpr-home-dashboard-paper-title" title="Point Dynamics as Proxy for Robotic World Models">Point Dynamics as Proxy for Robotic World Models</span></li><li><span class="dpr-home-dashboard-paper-title" title="Learning What Actions Change: Action Effect Matching for Dynamics-Faithful World Models">Learning What Actions Change: Action Effect Matching for Dynamics-Faithful World Models</span></li></ul>
  </div>
  <div class="dpr-home-dashboard-tags"><span class="dpr-home-dashboard-tag">embodied-ai <strong>9</strong></span><span class="dpr-home-dashboard-tag">feed-forward <strong>2</strong></span><span class="dpr-home-dashboard-tag">surf-recon <strong>2</strong></span></div>
</section>
<section class="dpr-home-dashboard-card dpr-home-skim-card">
  <div class="dpr-home-dashboard-header">
    <div>
      <span class="dpr-home-dashboard-kicker">今日累计</span>
      <h3 class="dpr-home-dashboard-title">速读推荐</h3>
    </div>
    <strong class="dpr-home-dashboard-count">15 篇</strong>
  </div>
  <div class="dpr-home-dashboard-body">
<ul class="dpr-home-dashboard-paper-list"><li><span class="dpr-home-dashboard-paper-title" title="CarlHOI: Counterfactual Predictive Imagination for Generalizable Multi-Humanoid Object Interaction under Constrained Environments">CarlHOI: Counterfactual Predictive Imagination for Generalizable Multi-Humanoid Object Interaction under Constrained Environments</span></li><li><span class="dpr-home-dashboard-paper-title" title="Beyond Episodic Recall: Experience-to-Knowledge Evolution for Lifelong Embodied Navigation">Beyond Episodic Recall: Experience-to-Knowledge Evolution for Lifelong Embodied Navigation</span></li><li><span class="dpr-home-dashboard-paper-title" title="SpatialMind: Adaptive Multi-Level Geometric Fusion for Spatial Reasoning in Multimodal Large Language Models">SpatialMind: Adaptive Multi-Level Geometric Fusion for Spatial Reasoning in Multimodal Large Language Models</span></li></ul>
  </div>
  <div class="dpr-home-dashboard-tags"><span class="dpr-home-dashboard-tag">embodied-ai <strong>8</strong></span><span class="dpr-home-dashboard-tag">feed-forward <strong>3</strong></span><span class="dpr-home-dashboard-tag">part-seg <strong>2</strong></span><span class="dpr-home-dashboard-tag">geometry <strong>1</strong></span><span class="dpr-home-dashboard-tag">surf-recon <strong>1</strong></span></div>
</section>
</div>

<div class="dpr-home-promo-card dpr-home-panel">
  <div class="dpr-home-panel-header">
    <h3 class="dpr-home-promo-title">社区与支持</h3>
  </div>
  <p class="dpr-home-promo-copy">欢迎通过 Star、Fork、Issue 或 PR 一起完善 Daily Paper Reader。</p>
  <div class="dpr-home-promo-meta">
    <span>QQ群 <strong>583867967</strong></span>
    <span class="dpr-home-promo-separator" aria-hidden="true">·</span>
    <span>已有 <strong>1,491</strong> 人参与交流</span>
  </div>
</div>
