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
      <span class="dpr-home-dashboard-kicker">2026-10-26</span>
      <h3 class="dpr-home-dashboard-title">今日汇总</h3>
    </div>
    <strong class="dpr-home-dashboard-count">共 11 篇</strong>
  </div>
  <dl class="dpr-home-dashboard-stats">
    <div class="dpr-home-dashboard-stat"><dt>累计更新</dt><dd>1 次</dd></div>
    <div class="dpr-home-dashboard-stat"><dt>精读</dt><dd>5</dd></div>
    <div class="dpr-home-dashboard-stat"><dt>速读</dt><dd>6</dd></div>
  </dl>
  <p class="dpr-home-dashboard-body">最近更新：2026-10-26 23:09:50 UTC<br>状态：成功</p>
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
<p>今日精选聚焦单图驱动的 3D 重建、场景构建与空间理解，共 11 篇推荐。</p>
<p>最值得看的是 PixGR 的快速前馈式 3D 重建，以及 Easy-3Dfy 的物体级几何组合。</p>
<p>建议先读 PixGR 把握高分工作，再按兴趣延伸到单图场景生成或空间 grounding。</p>
  </div>
</section>
<section class="dpr-home-dashboard-card dpr-home-deep-card">
  <div class="dpr-home-dashboard-header">
    <div>
      <span class="dpr-home-dashboard-kicker">今日累计</span>
      <h3 class="dpr-home-dashboard-title">精读推荐</h3>
    </div>
    <strong class="dpr-home-dashboard-count">5 篇</strong>
  </div>
  <div class="dpr-home-dashboard-body">
<ul class="dpr-home-dashboard-paper-list"><li><span class="dpr-home-dashboard-paper-title" title="PixGR: Pixel-Space Generative Decoding for Fast Feed-Forward 3D Reconstruction">PixGR: Pixel-Space Generative Decoding for Fast Feed-Forward 3D Reconstruction</span></li><li><span class="dpr-home-dashboard-paper-title" title="Easy-3Dfy: Object-Level Geometric Composition for Single-Image 3D Scene Construction">Easy-3Dfy: Object-Level Geometric Composition for Single-Image 3D Scene Construction</span></li><li><span class="dpr-home-dashboard-paper-title" title="Complementing DINO Features with Image Structure for Part Discovery">Complementing DINO Features with Image Structure for Part Discovery</span></li></ul>
  </div>
  <div class="dpr-home-dashboard-tags"><span class="dpr-home-dashboard-tag">feed-forward <strong>3</strong></span><span class="dpr-home-dashboard-tag">embodied-ai <strong>1</strong></span><span class="dpr-home-dashboard-tag">part-seg <strong>1</strong></span></div>
</section>
<section class="dpr-home-dashboard-card dpr-home-skim-card">
  <div class="dpr-home-dashboard-header">
    <div>
      <span class="dpr-home-dashboard-kicker">今日累计</span>
      <h3 class="dpr-home-dashboard-title">速读推荐</h3>
    </div>
    <strong class="dpr-home-dashboard-count">6 篇</strong>
  </div>
  <div class="dpr-home-dashboard-body">
<ul class="dpr-home-dashboard-paper-list"><li><span class="dpr-home-dashboard-paper-title" title="ACE-Brain-0.6: Scaling Spatial Grounding for Physical Foundation Models">ACE-Brain-0.6: Scaling Spatial Grounding for Physical Foundation Models</span></li><li><span class="dpr-home-dashboard-paper-title" title="PnP*: A certifiable solver for Perspective-n-Point">PnP*: A certifiable solver for Perspective-n-Point</span></li><li><span class="dpr-home-dashboard-paper-title" title="CityLift: Compositional 3D Urban Generation from a Single Image">CityLift: Compositional 3D Urban Generation from a Single Image</span></li></ul>
  </div>
  <div class="dpr-home-dashboard-tags"><span class="dpr-home-dashboard-tag">feed-forward <strong>2</strong></span><span class="dpr-home-dashboard-tag">geometry <strong>2</strong></span><span class="dpr-home-dashboard-tag">embodied-ai <strong>1</strong></span><span class="dpr-home-dashboard-tag">part-seg <strong>1</strong></span></div>
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
