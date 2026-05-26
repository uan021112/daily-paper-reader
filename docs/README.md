<div class="dpr-home-notice-card">
  <h3 class="dpr-home-notice-title">🚀 Start Here</h3>
  <ul class="dpr-home-notice-list">
    <li><a href="#/tutorial/README">使用教程</a></li>
  </ul>
</div>

## 每次日报
- 最新运行日期：2026-05-26
- 运行时间：2026-05-26 20:55:27 UTC
- 运行状态：成功
- 本次总论文数：25
- 精读区：12
- 速读区：13

### 今日简报（AI）
今天精读了两篇满分论文《F-RNG》与《TriSplat》，并速读了三篇高分论文，涵盖3D重建、内容生成与对应方法。最值得关注的方向是可重光照神经高斯渲染与仿真级前馈3D场景重建。建议普通读者优先速读《Efficient 3D Content Reconstruction and Generation》，以了解高效内容生成的基础思路。
- 详情：[/202605/26/README](/202605/26/README)

### 精读区论文标签
1. [F-RNG: Feed-Forward Relightable Neural Gaussians](/202605/26/2605.25975v1-f-rng-feed-forward-relightable-neural-gaussians)  
   标签：评分：10.0/10、query:ffdr
   evidence：直接从稀疏视图生成可重光照3D高斯的前馈框架
2. [TriSplat: Simulation-Ready Feed-Forward 3D Scene Reconstruction](/202605/26/2605.26115v1-trisplat-simulation-ready-feed-forward-3d-scene-reconstruction)  
   标签：评分：10.0/10、query:ffdr
   evidence：使用三角形基元的前馈3D场景重建，直接输出网格
3. [Fixed External Cameras as Common Prior Maps for Active 3D Scene Graph Generation](/202605/26/2605.18184v1-fixed-external-cameras-as-common-prior-maps-for-active-3d-scene-graph-generation)  
   标签：评分：9.0/10、query:ffdr
   evidence：使用前馈3D重建模型进行场景图生成
4. [ROAR-3D: Routing Arbitrary Views for High-Fidelity 3D Generation](/202605/26/2605.21121v1-roar-3d-routing-arbitrary-views-for-high-fidelity-3d-generation)  
   标签：评分：9.0/10、query:dgen
   evidence：单图到3D生成，利用多视角条件
5. [Stream3D: Sequential Multi-View 3D Generation via Evidential Memory](/202605/26/2605.21472v1-stream3d-sequential-multi-view-3d-generation-via-evidential-memory)  
   标签：评分：9.0/10、query:dgen
   evidence：从连续多视图流生成3D对象
6. [PhysX-Omni: Unified Simulation-Ready Physical 3D Generation for Rigid, Deformable, and Articulated Objects](/202605/26/2605.21572v1-physx-omni-unified-simulation-ready-physical-3d-generation-for-rigid-deformable-and-articulated-objects)  
   标签：评分：9.0/10、query:dgen
   evidence：统一的物理3D生成框架
7. [GIBLy: Improving 3D Semantic Segmentation through an Architecture-Agnostic Lightweight Geometric Inductive Bias Layer](/202605/26/2605.24243v1-gibly-improving-3d-semantic-segmentation-through-an-architecture-agnostic-lightweight-geometric-inductive-bias-layer)  
   标签：评分：9.0/10、query:partseg
   evidence：带有几何归纳偏置的3D语义分割
8. [ArtSplat: Feed-Forward Articulated 3D Gaussian Splatting from Sparse Multi-State Uncalibrated Views](/202605/26/2605.24304v1-artsplat-feed-forward-articulated-3d-gaussian-splatting-from-sparse-multi-state-uncalibrated-views)  
   标签：评分：9.0/10、query:ffdr
   evidence：前馈铰接三维高斯泼溅
9. [Artiverse: A Diverse and Physically Grounded Dataset for Articulated Objects](/202605/26/2605.24403v1-artiverse-a-diverse-and-physically-grounded-dataset-for-articulated-objects)  
   标签：评分：9.0/10、query:partseg
   evidence：用于部件分割训练的3D铰接物体数据集
10. [Multi-view Consistent 3D Gaussian Head Avatars 'without' Multi-view Generation](/202605/26/2605.25220v1-multi-view-consistent-3d-gaussian-head-avatars-without-multi-view-generation)  
   标签：评分：9.0/10、query:dgen
   evidence：从单张二维图像生成三维头部化身
11. [Generating 3D models from sketches of human faces using a combined approach of Convolutional Neural Networks, Procedural Modeling, and Contour Mapping](/202605/26/2605.25418v1-generating-3d-models-from-sketches-of-human-faces-using-a-combined-approach-of-convolutional-neural-networks-procedural-modeling-and-contour-mapping)  
   标签：评分：9.0/10、query:dgen
   evidence：使用CNN从手绘草图生成三维人脸模型，实现从2D输入到3D几何的直接映射
12. [Global Structure-from-Motion Meets Feedforward Reconstruction](/202605/26/2605.26103v1-global-structure-from-motion-meets-feedforward-reconstruction)  
   标签：评分：9.0/10、query:ffdr
   evidence：比较和结合SfM与前馈重建

### 速读区论文标签
1. [Efficient 3D Content Reconstruction and Generation](/202605/26/2605.18052v1-efficient-3d-content-reconstruction-and-generation)  
   标签：评分：8.0/10、query:dgen
   evidence：涵盖重建与生成两种范式的3D内容高效合成论文
2. [Tango3D: Towards Alignment for Global and Local 2D-3D Correspondence](/202605/26/2605.19727v1-tango3d-towards-alignment-for-global-and-local-2d-3d-correspondence)  
   标签：评分：8.0/10、query:ffdr
   evidence：使用几何感知2D骨干网络和3D VAE进行像素到点的直接对齐映射
3. [Fast 4D Mesh Generation by Spatio-Temporal Attention Chains](/202605/26/2605.19786v1-fast-4d-mesh-generation-by-spatio-temporal-attention-chains)  
   标签：评分：8.0/10、query:dgen
   evidence：无需训练的快速4D网格生成方法
4. [Variance Reduction for Expectations with Diffusion Teachers](/202605/26/2605.21489v2-variance-reduction-for-expectations-with-diffusion-teachers)  
   标签：评分：8.0/10、query:dgen
   evidence：文本到3D流程中扩散教师的方差减少
5. [Fishbone: From One 3D Asset to a Million Controllable Edits](/202605/26/2605.24805v1-fishbone-from-one-3d-asset-to-a-million-controllable-edits)  
   标签：评分：8.0/10、query:dgen
   evidence：可控参数化网格变形生成多样3D资产
6. [GaussianZoom: Progressive Zoom-in Generative 3D Gaussian Splatting with Geometric and Semantic Guidance](/202605/26/2605.18252v1-gaussianzoom-progressive-zoom-in-generative-3d-gaussian-splatting-with-geometric-and-semantic-guidance)  
   标签：评分：7.0/10、query:dgen
   evidence：从低分辨率输入生成式放大3D重建
7. [Text2CAD-Bench: A Benchmark for LLM-based Text-to-Parametric CAD Generation](/202605/26/2605.18430v1-text2cad-bench-a-benchmark-for-llm-based-text-to-parametric-cad-generation)  
   标签：评分：7.0/10、query:dgen
   evidence：文本到CAD生成基准
8. [Code-as-Room: Generating 3D Rooms from Top-Down View Images via Agentic Code Synthesis](/202605/26/2605.18451v1-code-as-room-generating-3d-rooms-from-top-down-view-images-via-agentic-code-synthesis)  
   标签：评分：7.0/10、query:dgen
   evidence：从顶视图图像生成三维房间
9. [PIXLRelight: Controllable Relighting via Intrinsic Conditioning](/202605/26/2605.18735v1-pixlrelight-controllable-relighting-via-intrinsic-conditioning)  
   标签：评分：7.0/10、query:dgen
   evidence：基于内在条件的前馈可控重打光
10. [DrawMotion: Generating 3D Human Motions by Freehand Drawing](/202605/26/2605.20955v1-drawmotion-generating-3d-human-motions-by-freehand-drawing)  
   标签：评分：6.0/10、query:dgen
   evidence：从文本和手绘生成三维运动
11. [3D LULC classification using multispectral LiDAR and deep learning: current and prospective schemes](/202605/26/2605.22328v1-3d-lulc-classification-using-multispectral-lidar-and-deep-learning-current-and-prospective-schemes)  
   标签：评分：6.0/10、query:partseg
   evidence：用于土地覆盖分类的3D点云语义分割
12. [GlowGS: Generative Semantic Feature Learning for 3D Gaussian Splatting in Nighttime Glow Scenes](/202605/26/2605.23602v1-glowgs-generative-semantic-feature-learning-for-3d-gaussian-splatting-in-nighttime-glow-scenes)  
   标签：评分：6.0/10、query:dgen
   evidence：夜间场景下3D高斯泼溅的生成式语义特征学习
13. [Learnable Shape Prototypes with Occlusion-Geometry-Guided Injection for Amodal Instance Segmentation](/202605/26/2605.24533v1-learnable-shape-prototypes-with-occlusion-geometry-guided-injection-for-amodal-instance-segmentation)  
   标签：评分：6.0/10、query:partseg
   evidence：可学习形状原型的无模态实例分割


<div class="dpr-home-promo-card">
  <h3 class="dpr-home-promo-title">💬 社区与支持</h3>
  <ul class="dpr-home-promo-list">
    <li>欢迎 Star / Fork / Issue / PR</li>
    <li>QQ群：583867967（欢迎交流，已有：1151人）</li>
  </ul>
</div>
