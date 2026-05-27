<div class="dpr-home-notice-card">
  <h3 class="dpr-home-notice-title">🚀 Start Here</h3>
  <ul class="dpr-home-notice-list">
    <li><a href="#/tutorial/README">使用教程</a></li>
  </ul>
</div>

## 每次日报
- 最新运行日期：2026-05-27
- 运行时间：2026-05-27 21:51:27 UTC
- 运行状态：成功
- 本次总论文数：21
- 精读区：8
- 速读区：13

### 今日简报（AI）
今日精读8篇、速读13篇，聚焦3D重建与人体恢复两大高分方向。

最值得关注的是9分精读：长时序流式3D重建《HorizonStream》与单图联合网格与穿衣人体重建《MuNet》；速读中《OP2GS》的物体感知双透明度高斯溅射、《Pantheon360》的360°视频生成数字孪生、《Full-4D》的单视图全场景4D生成也极具参考价值。

建议优先阅读两篇9分论文，深入理解长时序注意力机制与多任务人体重建思路；速读中可重点关注双透明度原语与360°视频扩散方法，对落地动态场景生成有帮助。
- 详情：[/202605/27/README](/202605/27/README)

### 精读区论文标签
1. [HorizonStream: Long-Horizon Attention for Streaming 3D Reconstruction](/202605/27/2605.23889v1-horizonstream-long-horizon-attention-for-streaming-3d-reconstruction)  
   标签：评分：9.0/10、query:ffdr
   evidence：流式3D重建使用长程注意力
2. [MuNet: A Mutualistic Network for Joint 3D Human Mesh Recovery and 3D Clothed Human Reconstruction from Single Images](/202605/27/2605.25861v2-munet-a-mutualistic-network-for-joint-3d-human-mesh-recovery-and-3d-clothed-human-reconstruction-from-single-images)  
   标签：评分：9.0/10、query:dgen
   evidence：从单张图像进行3D人体重建
3. [Global Structure-from-Motion Meets Feedforward Reconstruction](/202605/27/2605.26103v2-global-structure-from-motion-meets-feedforward-reconstruction)  
   标签：评分：9.0/10、query:ffdr
   evidence：比较前馈重建与经典SfM方法
4. [AssetGen: Deployable 3D Asset Generation at Interactive Speed](/202605/27/2605.26137v1-assetgen-deployable-3d-asset-generation-at-interactive-speed)  
   标签：评分：9.0/10、query:dgen
   evidence：从单张图像以交互速度生成高质量三维资产
5. [Geometry-Aware Representation Denoising for Robust Multi-view 3D Reconstruction](/202605/27/2605.26230v1-geometry-aware-representation-denoising-for-robust-multi-view-3d-reconstruction)  
   标签：评分：9.0/10、query:ffdr
   evidence：通过特征去噪提升前馈多视图三维重建的鲁棒性
6. [DelowlightSplat: Feed-Forward Gaussian Splatting for Lowlight 3D Scene Reconstruction](/202605/27/2605.26629v1-delowlightsplat-feed-forward-gaussian-splatting-for-lowlight-3d-scene-reconstruction)  
   标签：评分：9.0/10、query:ffdr
   evidence：前馈式高斯泼溅用于低光照3D重建
7. [I2PRef: Image-Driven Point Completion with Iterative Refinement](/202605/27/2605.26914v1-i2pref-image-driven-point-completion-with-iterative-refinement)  
   标签：评分：9.0/10、query:ffdr
   evidence：图像到点云的直接映射用于3D重建
8. [Sketch2MinSurf: Vision-Language Guided Generation of Editable Minimal Surfaces from Hand-Drawn Sketches](/202605/27/2605.20733v1-sketch2minsurf-vision-language-guided-generation-of-editable-minimal-surfaces-from-hand-drawn-sketches)  
   标签：评分：8.0/10、query:dgen
   evidence：从手绘草图生成可编辑3D表面，结合视觉语言与几何优化

### 速读区论文标签
1. [OP2GS: Object-Aware 3D Gaussian Splatting with Dual-Opacity Primitives](/202605/27/2605.20044v1-op2gs-object-aware-3d-gaussian-splatting-with-dual-opacity-primitives)  
   标签：评分：8.0/10、query:partseg
   evidence：面向对象的3D高斯表示用于实例级分割
2. [Pantheon360: Taming Digital Twin Generation via 3D-Aware 360° Video Diffusion](/202605/27/2605.25449v1-pantheon360-taming-digital-twin-generation-via-3d-aware-360-video-diffusion)  
   标签：评分：8.0/10、query:dgen
   evidence：3D感知的全景视频扩散用于数字孪生生成
3. [Full-4D: Generating Full-Scope 4D Scenes from a Single-View Video](/202605/27/2605.25500v1-full-4d-generating-full-scope-4d-scenes-from-a-single-view-video)  
   标签：评分：8.0/10、query:dgen
   evidence：从单视角视频生成完整4D场景，使用多视角视频合成与优化重建
4. [InstructSAM: Segment Any Instance with Any Instructions](/202605/27/2605.26102v1-instructsam-segment-any-instance-with-any-instructions)  
   标签：评分：8.0/10、query:partseg
   evidence：任意指令驱动的多实例分割，桥接VLM和SAM进行实例感知查询预测
5. [Helix4D: Complex 4D Mesh Generation](/202605/27/2605.26109v1-helix4d-complex-4d-mesh-generation)  
   标签：评分：8.0/10、query:dgen
   evidence：视频条件四维网格生成，处理复杂拓扑
6. [AnySurf: Any Surface Generation with Directed Edge](/202605/27/2605.26149v1-anysurf-any-surface-generation-with-directed-edge)  
   标签：评分：8.0/10、query:dgen
   evidence：统一框架生成开放/封闭3D表面
7. [MatPhys: Learning Material-Aware Physics Parameters for Deformable Object Simulation from Videos](/202605/27/2605.19386v1-matphys-learning-material-aware-physics-parameters-for-deformable-object-simulation-from-videos)  
   标签：评分：7.0/10、query:ffdr
   evidence：前馈框架从视频预测物理参数，直接映射像素到可变形物体的物理参数
8. [Learning Structural Latent Points for Efficient Visual Representations in Robotic Manipulation](/202605/27/2605.21258v1-learning-structural-latent-points-for-efficient-visual-representations-in-robotic-manipulation)  
   标签：评分：7.0/10、query:ffdr
   evidence：前馈学习的潜在点用于3D表示
9. [Generator-Refiner-Examiner: A Tri-Module Data Augmentation Framework for 3D Human Avatar Learning from Monocular Videos](/202605/27/2605.23555v1-generator-refiner-examiner-a-tri-module-data-augmentation-framework-for-3d-human-avatar-learning-from-monocular-videos)  
   标签：评分：7.0/10、query:dgen
   evidence：从单目视频重建3D化身
10. [COSY: Compositional 3DGS Synthesis for Disentangled Human Head Editing](/202605/27/2605.24114v1-cosy-compositional-3dgs-synthesis-for-disentangled-human-head-editing)  
   标签：评分：7.0/10、query:dgen
   evidence：解耦组件的组合式3DGS合成用于人头编辑
11. [Scene Reconstruction as Mapping Priors for 3D Detection](/202605/27/2605.22997v1-scene-reconstruction-as-mapping-priors-for-3d-detection)  
   标签：评分：6.0/10、query:ffdr
   evidence：利用场景重建作为3D检测的地图先验
12. [OMGTex: One-stage Multi-style Facial Texture Reconstruction without Geometry Guidance](/202605/27/2605.25778v1-omgtex-one-stage-multi-style-facial-texture-reconstruction-without-geometry-guidance)  
   标签：评分：6.0/10、query:dgen
   evidence：无需几何指导的2D到UV纹理直接映射
13. [PinPoint: Prompting with Informative Interior Points](/202605/27/2605.26689v1-pinpoint-prompting-with-informative-interior-points)  
   标签：评分：6.0/10、query:partseg
   evidence：通过信息性内部点改进引用图像分割


<div class="dpr-home-promo-card">
  <h3 class="dpr-home-promo-title">💬 社区与支持</h3>
  <ul class="dpr-home-promo-list">
    <li>欢迎 Star / Fork / Issue / PR</li>
    <li>QQ群：583867967（欢迎交流，已有：1151人）</li>
  </ul>
</div>
