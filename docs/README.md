<div class="dpr-home-notice-card dpr-home-panel">
  <div class="dpr-home-notice-header dpr-home-panel-header">
    <h3 class="dpr-home-notice-title">公告与更新</h3>
    <a class="dpr-home-notice-tutorial" href="#/tutorial/README">使用教程 <span aria-hidden="true">›</span></a>
  </div>
  <div class="dpr-home-notice-entry">
    <time class="dpr-home-notice-date" datetime="2026-07-19">07.19</time>
    <div>
      <strong class="dpr-home-notice-entry-title">首页新增社区统计</strong>
      <span class="dpr-home-notice-entry-summary">现在可以看到今天看论文的人数和项目加入人数。</span>
    </div>
  </div>
  <div class="dpr-home-site-stats" data-dpr-site-stats hidden aria-live="polite">
    <span>今天有 <strong class="dpr-home-site-stat-value" data-dpr-daily-readers>--</strong> 人在看论文</span>
    <span class="dpr-home-site-stat-separator" aria-hidden="true">·</span>
    <span>已有 <strong class="dpr-home-site-stat-value" data-dpr-fork-count>--</strong> 人加入 Daily Paper Reader</span>
  </div>
</div>

## 每次日报
- 最新运行日期：2026-08-02
- 运行时间：2026-08-02 21:41:08 UTC
- 运行状态：成功
- 本次总论文数：24
- 精读区：11
- 速读区：13

### 今日简报（AI）
今日聚焦24篇新论文，精读2篇重点研究，速读13篇覆盖多元方向。  
最值得关注：高分10分的道路表面重建模型RoadVGGT，以及9分的可控3D服装生成框架Fashion-3DLR，分别代表自动驾驶感知与智能设计的突破。  
建议普通读者优先跟踪道路重建与智能服装生成的技术进展，后续可关注食品分割和立体几何估计的基准工作。
- 详情：[/202608/02/README](/202608/02/README)

### 精读区论文标签
1. [RoadVGGT: Road-Structure-Aware Feed-Forward Road Surface Reconstruction](/202608/02/2607.23758v1-roadvggt-road-structure-aware-feed-forward-road-surface-reconstruction)  
   标签：评分：10.0/10、query:ffdr
   evidence：用于道路表面三维重建的前馈框架，无需每场景优化
2. [Fashion-3DLR: A Controllable 3D Garment Generation Using Pairwise Fashion Elements for Intelligent Design](/202608/02/2607.23189v1-fashion-3dlr-a-controllable-3d-garment-generation-using-pairwise-fashion-elements-for-intelligent-design)  
   标签：评分：9.0/10、query:dgen
   evidence：可控三维服装生成，属于生成式三维建模
3. [UMI3D: Robust 3D Generation on Unconstrained Multi-Image Inputs via Simultaneous Focus Cross-Attention Routing](/202608/02/2607.24298v1-umi3d-robust-3d-generation-on-unconstrained-multi-image-inputs-via-simultaneous-focus-cross-attention-routing)  
   标签：评分：9.0/10、query:dgen
   evidence：针对多图像输入的鲁棒3D生成，从多张非受限图像重建3D资产
4. [MSVS-VAE: Multi-Scale Anchored VecSet for High-Fidelity 3D Reconstruction](/202608/02/2607.24436v1-msvs-vae-multi-scale-anchored-vecset-for-high-fidelity-3d-reconstruction)  
   标签：评分：9.0/10、query:ffdr
   evidence：用于高保真三维重建的前馈VAE
5. [DreamStyle3D: Efficient 3D Stylized Asset Generation via Dual-Attention Disentanglement](/202608/02/2607.24721v1-dreamstyle3d-efficient-3d-stylized-asset-generation-via-dual-attention-disentanglement)  
   标签：评分：9.0/10、query:dgen
   evidence：高效的风格化3D资产生成，实现风格与几何解耦
6. [Spline-Based Boundary Representations for Sparse View Reconstruction and Simulation Using Isogeometric Analysis](/202608/02/2607.26234v1-spline-based-boundary-representations-for-sparse-view-reconstruction-and-simulation-using-isogeometric-analysis)  
   标签：评分：9.0/10、query:dgen
   evidence：基于稀疏视图图像重建样条边界表示的3D几何
7. [Genie Sim PanoWorld: An Infinite Indoor 3D World Generation Pipeline via Panoramic Scene Modeling and Simulation](/202608/02/2607.26646v1-genie-sim-panoworld-an-infinite-indoor-3d-world-generation-pipeline-via-panoramic-scene-modeling-and-simulation)  
   标签：评分：9.0/10、query:ffdr
   evidence：无需逐场景优化的两阶段前馈模型，由单张全景图直接重建三维场景
8. [MeshFM: 2D Features Are All You Need for 3D Shape Understanding](/202608/02/2607.27592v1-meshfm-2d-features-are-all-you-need-for-3d-shape-understanding)  
   标签：评分：9.0/10、query:ffdr
   evidence：前馈三维特征预测且推理时无需优化，可直接用于部件分割
9. [4DHumanDiff: Direct Text-to-4DGS Generation for Consistent 360-Degree Dynamic Humans](/202608/02/2607.27634v1-4dhumandiff-direct-text-to-4dgs-generation-for-consistent-360-degree-dynamic-humans)  
   标签：评分：9.0/10、query:dgen
   evidence：使用4D高斯溅射从文本生成动态人物
10. [Convolutional Neural Shading for High-Quality 3D Reconstruction from Multi-View Images](/202608/02/2607.28132v1-convolutional-neural-shading-for-high-quality-3d-reconstruction-from-multi-view-images)  
   标签：评分：9.0/10、query:dgen
   evidence：使用卷积神经着色从多视图图像进行高质量三维重建
11. [ROAD: Reciprocal-Objective Alignment of Discriminative Semantics for 3D Shape Generation](/202608/02/2607.28581v1-road-reciprocal-objective-alignment-of-discriminative-semantics-for-3d-shape-generation)  
   标签：评分：9.0/10、query:dgen
   evidence：结合判别先验的扩散Transformer 3D形状生成

### 速读区论文标签
1. [DishSeg24k: A Large-Scale Benchmark for Food Segmentation with Stochastic Expert Decoding](/202608/02/2607.23070v1-dishseg24k-a-large-scale-benchmark-for-food-segmentation-with-stochastic-expert-decoding)  
   标签：评分：8.0/10、query:partseg
   evidence：大规模菜品实例分割基准与随机专家解码分割Transformer
2. [GRAPE: Graduated Routing for Articulated Portrait mesh Estimation](/202608/02/2607.23657v1-grape-graduated-routing-for-articulated-portrait-mesh-estimation)  
   标签：评分：8.0/10、query:ffdr
   evidence：单目人像网格估计直接前馈地从像素映射到三维几何
3. [A Unified Stereo Geometry Estimation Framework for Disparity and Surface Normal](/202608/02/2607.24024v1-a-unified-stereo-geometry-estimation-framework-for-disparity-and-surface-normal)  
   标签：评分：8.0/10、query:ffdr
   evidence：前馈立体匹配联合预测视差与表面法向量，属于从图像到三维几何的前馈重建
4. [PointCHR: Point Cloud Analysis via Curvature-Aware Hyperbolic Rectification](/202608/02/2607.24052v1-pointchr-point-cloud-analysis-via-curvature-aware-hyperbolic-rectification)  
   标签：评分：8.0/10、query:partseg
   evidence：保留曲率敏感的细粒度几何信息，促进部件级点云分割
5. [GenSplatCodec: Feed-Forward Gaussian Splatting Compression via One-Step Diffusion](/202608/02/2607.24403v1-gensplatcodec-feed-forward-gaussian-splatting-compression-via-one-step-diffusion)  
   标签：评分：8.0/10、query:ffdr
   evidence：面向前馈三维高斯溅射重建输出的高效压缩编解码器
6. [Multiview Multi-Person Human Mesh Recovery Under Large Scenes with Occlusions](/202608/02/2607.24302v1-multiview-multi-person-human-mesh-recovery-under-large-scenes-with-occlusions)  
   标签：评分：7.0/10、query:dgen
   evidence：多视角多人人体网格恢复基准，从图像重建三维人体网格
7. [Intrinsic and Triangulation-Agnostic Attention: A Simple and Powerful Approach for Learning on Meshes](/202608/02/2607.24954v1-intrinsic-and-triangulation-agnostic-attention-a-simple-and-powerful-approach-for-learning-on-meshes)  
   标签：评分：7.0/10、query:partseg
   evidence：面向三角形网格的注意力机制在几何处理任务中达到 SOTA，可用于三维形状部件分割
8. [WHTMix: Efficient Stereo Depth Estimation via Walsh-Hadamard Token Mixing](/202608/02/2607.25234v1-whtmix-efficient-stereo-depth-estimation-via-walsh-hadamard-token-mixing)  
   标签：评分：7.0/10、query:ffdr
   evidence：前馈立体深度估计，从像素到深度的高效映射
9. [PanoLess: Environment Reconstruction from Partial Reflective Views](/202608/02/2607.25362v1-panoless-environment-reconstruction-from-partial-reflective-views)  
   标签：评分：7.0/10、query:dgen
   evidence：利用高斯泼溅从部分反射视图重建周围环境照明图，属于从图像恢复三维环境
10. [ViDS: Video Diffusion Shader using 3D Face Tracking](/202608/02/2607.24124v1-vids-video-diffusion-shader-using-3d-face-tracking)  
   标签：评分：6.0/10、query:dgen
   evidence：利用三维人脸跟踪和视频扩散模型作为神经着色器，用于肖像动画生成
11. [Long-Tailed 3D Point Cloud Dataset Distillation](/202608/02/2607.26763v1-long-tailed-3d-point-cloud-dataset-distillation)  
   标签：评分：6.0/10、query:partseg
   evidence：面向长尾点云的数据集蒸馏方法，可服务部件级分割数据集构建
12. [Articulated Object Reconstruction from Rest-State Observation](/202608/02/2607.27749v1-articulated-object-reconstruction-from-rest-state-observation)  
   标签：评分：6.0/10、query:partseg
   evidence：从静态观测重建关节物体，融合分割与视觉-语言模型输出生成空间一致的部件结构
13. [TSOG: A Format For Temporally And Spatially Ordered Gaussians](/202608/02/2607.28049v1-tsog-a-format-for-temporally-and-spatially-ordered-gaussians)  
   标签：评分：6.0/10、query:dgen
   evidence：面向4D高斯溅射内容的高效时空有序高斯格式，支持基于神经渲染的3D内容创作


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
