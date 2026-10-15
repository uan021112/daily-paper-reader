<div class="dpr-topic-result-actions"><button type="button" data-topic-copy="docs/starter-pack/20261015-25c1e19060da/papers.md">复制论文清单</button> <a href="docs/starter-pack/20261015-25c1e19060da/papers.md" download data-no-router>下载 Markdown</a> <a href="docs/starter-pack/20261015-25c1e19060da/papers.json" download data-no-router>下载 JSON</a> <button type="button" data-topic-continue="20261015-25c1e19060da">继续生成阅读内容</button></div>

# embodied-ai · 入门导读

> 本导读基于所列论文的标题、摘要和已有速览，不代表已阅读全部全文。近期窗口不是完整领域史；检索不保证覆盖全部相关论文。模型导读需结合原文核验。

检索窗口：arXiv &#91;2025-10-15, 2026-10-15&#41;；会议 &#91;2024-10-15, 2026-10-15&#41;（UTC，结束日不含）

## 方向概览

具身智能关注的核心问题是：智能体如何在身体与环境持续交互时，将感知、空间理解、推理、规划和动作连接起来，并在环境变化、信息不完整或执行失败时调整行为。近期检索到的研究主要围绕统一感知—行动模型、可预测环境后果的世界模型、主动感知与空间推理、跨任务和跨身体泛化，以及训练与评测基础设施展开。整体趋势是从静态观察或单步动作预测，转向闭环执行、动作后果预测和部署后的适应；但这些论文覆盖的主题与场景不均衡，不能据此视为完整领域史。部分论文摘要只报告作者提出的方法或评测结论，尚不足以支持对不同路线作统一比较；安全性、真实环境长期运行和跨身体迁移的证据也并不一致。

依据：[Self-evolving Embodied AI](/20251015-20261014/2602.04411v1)；[EmbodiedBrain: Expanding Performance Boundaries of Task Planning for Embodied Intelligence](/20251015-20261014/2510.20578v1)；[World Action Models: The Next Frontier in Embodied AI](/20251015-20261014/2605.12090v1)；[ESI-Bench: Towards Embodied Spatial Intelligence that Closes the Perception-Action Loop](/20251015-20261014/2605.18746v2)；[EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents](/conference/icml-2025/openreview-icml-2025-dggf2lebps-embodiedbench-comprehensive-benchmarking-multi-modal-large-language-models-for-vision-driven-embodied-agents)；[Intelligence Across Embodiments](/20251015-20261014/2609.27095v1)

## 统一具身模型：从空间理解到可执行动作

一条研究路线试图把视觉、语言、空间推理、规划与机器人动作纳入统一模型，或通过分层架构连接这些能力。方法包括以空间定位或结构化推理作为动作生成的中间表示、联合训练多任务模型，以及将高层规划器与低层动作执行器组合。跨任务、跨环境和跨机器人身体的泛化是这类工作的共同目标，但模型在基准上的表现不能单独证明其在开放环境中的可靠性。摘要所述结果来自各自的任务和评测设置，缺少足够一致的信息来进行横向排名。

依据：[Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](/20251015-20261014/2605.30280v2)；[DM0: An Embodied-Native Vision-Language-Action Model towards Physical AI](/20251015-20261014/2602.14974v1)；[Embodied Robot Manipulation in the Era of Foundation Models: Planning and Learning Perspectives](/20251015-20261014/2512.22983v2)；[SpatialPoint: Spatial-aware Point Prediction for Embodied Localization](/20251015-20261014/2603.26690v1)；[Being-H0.5: Scaling Human-Centric Robot Learning for Cross-Embodiment Generalization](/20251015-20261014/2601.12993v1)；[ACE-Brain-0.5: A Unified Embodied Foundational Model for Physical Agentic AI](/20251015-20261014/2607.04426v1)

## 世界模型与动作后果预测

世界模型研究的问题是：智能体能否在行动前预测环境如何变化，并利用预测改进规划、控制或学习。输入论文涵盖了动作条件视频预测、共享多模态状态表示、显式场景模型、可组合数字孪生，以及将预测用于候选动作筛选等方法。一个值得关注的区分是，预测结果不仅要看起来合理，还要能反映动作的物理后果并帮助闭环行为。相关综述明确指出，长时序一致性、接触建模、幻觉控制、动作对齐和评测仍是开放问题。不同研究对“世界模型”的定义、预测对象和用途并不相同，因此不能把它们视为同一种方法。

依据：[World Action Models: The Next Frontier in Embodied AI](/20251015-20261014/2605.12090v1)；[Thinker-WM: A Unified World Model with Shared Multimodal Representations for Embodied Intelligence](/20251015-20261014/2610.18447v1)；[Learning 3D Persistent Embodied World Models](/conference/neurips-2025/openreview-neurips-2025-xttbzc7o2t-learning-3d-persistent-embodied-world-models)；[World Models for Robotic Manipulation: A Survey](/20251015-20261014/2606.00113v1)；[World Models for Embodied Intelligence: From Plausible to Controllable to Actionable](/20251015-20261014/2609.16697v1)；[TrAct: Bridging Robot Control and Visual Prediction with Visual Tracks](/20251015-20261014/2608.24101v3)

## 主动感知、空间推理与交互

在遮挡、视角受限或环境信息不完整时，智能体需要决定怎样移动、观察或操作，才能获取与任务相关的证据。输入论文提出了主动视觉推理、感知—行动闭环评测、交互式感知及多视角信息融合等方向。相关结果提示，增加观察数量未必带来更好推理；若动作没有针对信息缺口，后续观察也可能不足以纠正错误。深度、三维定位和可供性表示有助于连接空间理解与可执行动作，但其收益依赖表示质量和任务设置。现有摘要并未提供足够统一的实验细节，无法判断这些方法在不同机器人和真实场景中的普遍效果。

依据：[ESI-Bench: Towards Embodied Spatial Intelligence that Closes the Perception-Action Loop](/20251015-20261014/2605.18746v2)；[PhysVLM-AVR: Active Visual Reasoning for Multimodal Large Language Models in Physical Environments](/conference/neurips-2025/openreview-neurips-2025-aydmnzpjpv-physvlm-avr-active-visual-reasoning-for-multimodal-large-language-models-in-physical-environments)；[Zero-shot Interactive Perception](/20251015-20261014/2602.18374v1)；[Ego to World: Collaborative Spatial Reasoning in Embodied Systems via Reinforcement Learning](/20251015-20261014/2603.14811v1)；[SpatialPoint: Spatial-aware Point Prediction for Embodied Localization](/20251015-20261014/2603.26690v1)；[Embodied3DBench: Benchmarking Low-Level Embodied Spatial Intelligence of Vision Language Models](/20251015-20261014/2605.29074v1)

## 训练、数据与跨身体泛化

具身系统依赖动作轨迹、机器人示范、人类第一视角视频、仿真数据及多模态传感数据。输入论文采用的办法包括混合数据联合预训练、将人类互动经验转换为机器人训练数据、统一不同机器人的动作表示，以及利用仿真或生成模型扩展训练样本。研究动机是缓解真实机器人数据收集成本，并提升跨任务、跨场景或跨身体迁移能力。数据来源与控制接口不一致，可能使训练收益难以迁移；摘要报告的仿真、基准和真实机器人结果也不可直接等同。现有材料不足以确定哪种数据配方在不同任务上最具数据效率。

依据：[Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](/20251015-20261014/2605.30280v2)；[DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos](/20251015-20261014/2602.06949v1)；[AnyWorld: Factorized Egocentric World Models for Cross-Embodiment Generalization](/20251015-20261014/2608.29242v2)；[RoboMIND 2.0: A Multimodal, Bimanual Mobile Manipulation Dataset for Generalizable Embodied Intelligence](/20251015-20261014/2512.24653v3)；[ACE-Data-0: Human-Centric Ambient Capture as Embodied Data Engine](/20251015-20261014/2607.28625v1)；[Intelligence Across Embodiments](/20251015-20261014/2609.27095v1)

## 评测与仿真基础设施

评测工作试图拆分具身系统的能力，而不只观察最终任务是否成功。例如，基准分别考察空间理解、指令理解、规划、可供性判断、低层操作或闭环交互；仿真平台则提供多场景、动态环境或多智能体任务。这样的设计有助于定位模型的能力缺口，但基准成绩不必然代表真实部署能力。论文摘要也指出，部分模型在高层语义任务上表现较好，却在低层操作、细粒度空间推理或长时序执行上遇到困难。当前输入材料没有提供足够统一的基准定义、实现条件和比较结果，因而不能据此构造跨论文的综合排行榜。

依据：[EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents](/conference/icml-2025/openreview-icml-2025-dggf2lebps-embodiedbench-comprehensive-benchmarking-multi-modal-large-language-models-for-vision-driven-embodied-agents)；[Robobench: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models as Embodied Brain](/20251015-20261014/2510.17801v2)；[Embodied3DBench: Benchmarking Low-Level Embodied Spatial Intelligence of Vision Language Models](/20251015-20261014/2605.29074v1)；[TongSIM: A General Platform for Simulating Intelligent Machines](/20251015-20261014/2512.20206v1)；[Embodied-R1.5: Evolving Physical Intelligence via Embodied Foundation Models](/20251015-20261014/2606.11324v2)；[RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments](/20251015-20261014/2610.10409v1)

## 持续适应、执行反馈与局限

一类近期工作把研究重点从训练完成后的固定策略，转向执行过程中的进度监控、失败恢复、记忆更新和持续改进。实现方式包括闭环规划与纠错、基于经验更新外部记忆、强化微调，以及利用环境反馈迭代修改计划或执行程序。它们针对的是长时序任务中的状态变化、延迟反馈和错误累积。摘要所述成果显示出这一方向的探索范围，但不同论文对“自我改进”的定义并不相同：有的更新外部经验，有的改变策略或训练过程，有的依赖运行时规划。关于长期稳定性、安全边界、持续运行成本和跨场景可复现性的证据不足，不能将个别实验结果概括为已解决的能力。

依据：[Self-evolving Embodied AI](/20251015-20261014/2602.04411v1)；[SEEA-R1: Tree-Structured Reinforcement Fine-Tuning for Self-Evolving Embodied Agents](/conference/neurips-2025/openreview-neurips-2025-dawkepzvcn-seea-r1-tree-structured-reinforcement-fine-tuning-for-self-evolving-embodied-agents)；[ME-Brain-1.0: Memory, Cognition and Action for Evolving Embodied Intelligence](/20251015-20261014/2609.24271v1)；[HoloAgent-0: A Unified Embodied Agent Framework with 3D Spatial Memory](/20251015-20261014/2606.23565v1)；[ASENA: Self-evolving Agents for Embodied Navigation](/20251015-20261014/2609.39207v1)；[Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses](/20251015-20261014/2605.02900v2)

## 建议阅读顺序

以下为建议学习顺序，不是公布时间排序。

1. [Fundamentals of Physical AI](/20251015-20261014/2511.09497v1) · 入门
   - 阅读理由：先读其对身体、感知、行动、学习、自主性与情境性的概念框架，建立理解具身智能问题的入口；这是概念性论述，不代表该领域已有统一理论。
   - 公布时间：2025-11-12（日精度）
   - arxiv · 2025-11-12（日精度）：[原文](https://arxiv.org/pdf/2511.09497v1) / [PDF](https://arxiv.org/pdf/2511.09497v1)

2. [Self-evolving Embodied AI](/20251015-20261014/2602.04411v1) · 入门
   - 阅读理由：用综述式框架了解自我更新记忆、任务切换、环境预测和身体适应等问题，并注意区分概念框架与已实现组件。
   - 公布时间：2026-02-04（日精度）
   - arxiv · 2026-02-04（日精度）：[原文](https://arxiv.org/pdf/2602.04411v1) / [PDF](https://arxiv.org/pdf/2602.04411v1)

3. [Embodied Robot Manipulation in the Era of Foundation Models: Planning and Learning Perspectives](/20251015-20261014/2512.22983v2) · 入门
   - 阅读理由：从高层规划与低层动作建模的组织方式理解机器人操作中基础模型的设计空间。
   - 公布时间：2025-12-28（日精度）
   - arxiv · 2025-12-28（日精度）：[原文](https://arxiv.org/pdf/2512.22983v2) / [PDF](https://arxiv.org/pdf/2512.22983v2)

4. [World Models for Robotic Manipulation: A Survey](/20251015-20261014/2606.00113v1) · 入门
   - 阅读理由：通过预测表示、动作连接方式和使用环节三个问题，建立机器人操作世界模型的分类视角。
   - 公布时间：2026-05-27（日精度）
   - arxiv · 2026-05-27（日精度）：[原文](https://arxiv.org/pdf/2606.00113v1) / [PDF](https://arxiv.org/pdf/2606.00113v1)

5. [EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents](/conference/icml-2025/openreview-icml-2025-dggf2lebps-embodiedbench-comprehensive-benchmarking-multi-modal-large-language-models-for-vision-driven-embodied-agents) · 入门
   - 阅读理由：认识多模态具身智能体的能力评测如何覆盖从语义任务到导航和操作的不同层次。
   - 公布时间：2025-10-06（日精度）
   - ICML-2025-Accepted · 2025-10-06（日精度）：[官方论文集](https://proceedings.mlr.press/v267/yang25f.html) / [原文](https://openreview.net/forum?id=DgGF2LEBPS)

6. [Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](/20251015-20261014/2605.30280v2) · 进阶
   - 阅读理由：作为统一视觉—语言—动作模型的实例，观察多任务数据、动作生成和身体条件化如何被组合。
   - 公布时间：2026-05-28（日精度）
   - arxiv · 2026-05-28（日精度）：[原文](https://arxiv.org/pdf/2605.30280v2) / [PDF](https://arxiv.org/pdf/2605.30280v2)

7. [DM0: An Embodied-Native Vision-Language-Action Model towards Physical AI](/20251015-20261014/2602.14974v1) · 进阶
   - 阅读理由：对照另一种统一操作与导航的训练路线，重点关注分阶段训练和空间推理约束。
   - 公布时间：2026-02-16（日精度）
   - arxiv · 2026-02-16（日精度）：[原文](https://arxiv.org/pdf/2602.14974v1) / [PDF](https://arxiv.org/pdf/2602.14974v1)

8. [GSR: Learning Structured Reasoning for Embodied Manipulation](/20251015-20261014/2602.01693v1) · 进阶
   - 阅读理由：学习以场景图状态转移显式表示操作推理的做法，并关注其泛化主张所依赖的评测。
   - 公布时间：2026-02-02（日精度）
   - arxiv · 2026-02-02（日精度）：[原文](https://arxiv.org/pdf/2602.01693v1) / [PDF](https://arxiv.org/pdf/2602.01693v1)

9. [ESI-Bench: Towards Embodied Spatial Intelligence that Closes the Perception-Action Loop](/20251015-20261014/2605.18746v2) · 进阶
   - 阅读理由：了解把观察者视为行动者的空间智能评测，以及主动探索可能失败的原因。
   - 公布时间：2026-05-18（日精度）
   - arxiv · 2026-05-18（日精度）：[原文](https://arxiv.org/pdf/2605.18746v2) / [PDF](https://arxiv.org/pdf/2605.18746v2)

10. [World Action Models: The Next Frontier in Embodied AI](/20251015-20261014/2605.12090v1) · 进阶
   - 阅读理由：理解世界模型与动作生成联合建模这一研究范式及其架构分类。
   - 公布时间：2026-05-12（日精度）
   - arxiv · 2026-05-12（日精度）：[原文](https://arxiv.org/pdf/2605.12090v1) / [PDF](https://arxiv.org/pdf/2605.12090v1)

11. [TrAct: Bridging Robot Control and Visual Prediction with Visual Tracks](/20251015-20261014/2608.24101v3) · 专题
   - 阅读理由：专题考察视觉轨迹如何作为动作控制与未来视觉预测之间的中间接口。
   - 公布时间：2026-08-25（日精度）
   - arxiv · 2026-08-25（日精度）：[原文](https://arxiv.org/pdf/2608.24101v1)
   - arxiv · 2026-08-25（日精度）：[原文](https://arxiv.org/pdf/2608.24101v2)
   - arxiv · 2026-08-25（日精度）：[原文](https://arxiv.org/pdf/2608.24101v3) / [PDF](https://arxiv.org/pdf/2608.24101v3)

12. [Learning 3D Persistent Embodied World Models](/conference/neurips-2025/openreview-neurips-2025-xttbzc7o2t-learning-3d-persistent-embodied-world-models) · 专题
   - 阅读理由：专题考察持久三维记忆如何支持部分观测场景中的长时序预测与规划。
   - 公布时间：2025（年精度）
   - NeurIPS-2025-Accepted · 2025（年精度）：[官方论文集](https://papers.neurips.cc/paper_files/paper/2025/hash/970f59b22f4c72aec75174aae63c7459-Abstract-Conference.html) / [原文](https://openreview.net/forum?id=XTTbzC7O2T)

13. [Intelligence Across Embodiments](/20251015-20261014/2609.27095v1) · 专题
   - 阅读理由：专题阅读跨身体迁移的观点，关注身体差异、经验积累与评测需求，而不是只看单一平台成绩。
   - 公布时间：2026-09-22（日精度）
   - arxiv · 2026-09-22（日精度）：[原文](https://arxiv.org/pdf/2609.27095v1)

14. [SEEA-R1: Tree-Structured Reinforcement Fine-Tuning for Self-Evolving Embodied Agents](/conference/neurips-2025/openreview-neurips-2025-dawkepzvcn-seea-r1-tree-structured-reinforcement-fine-tuning-for-self-evolving-embodied-agents) · 专题
   - 阅读理由：专题了解树搜索和多模态奖励估计如何用于稀疏反馈下的具身强化微调。
   - 公布时间：2025（年精度）
   - NeurIPS-2025-Accepted · 2025（年精度）：[官方论文集](https://papers.neurips.cc/paper_files/paper/2025/hash/7103cd82de95a7b30983fcf74ba499ac-Abstract-Conference.html) / [原文](https://openreview.net/forum?id=dAwKePZvcN)

15. [Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses](/20251015-20261014/2605.02900v2) · 专题
   - 阅读理由：在考虑真实部署和自主执行时补充安全视角；摘要为综述性概述，具体风险需回到论文内容核实。
   - 公布时间：2026-03-28（日精度）
   - arxiv · 2026-03-28（日精度）：[原文](https://arxiv.org/pdf/2605.02900v2) / [PDF](https://arxiv.org/pdf/2605.02900v2)

任务：研究方向大礼包

固定窗口：arXiv &#91;2025-10-15, 2026-10-15&#41;；会议 &#91;2024-10-15, 2026-10-15&#41;（UTC，结束日不含）

本次候选评审上限 300，最终名单上限 100；本轮内容预算 10。

覆盖限制：仅检索配置范围内已有库存与预算内候选；向量/会议Top-k召回并非全库遍历，不保证找全相关论文。未核实录用、日期边界和缺失库存不能当作已覆盖。

缺失库存：eccv 2025、emnlp 2026、neurips 2026。

研究需求：具身智能

# embodied-ai

以下为本次固定最终名单，按相关性评分降序；不代表全部相关论文。

1. [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411v1) · 分数 10
2. [EmbodiedBrain: Expanding Performance Boundaries of Task Planning for Embodied Intelligence](https://arxiv.org/abs/2510.20578v1) · 分数 10
3. [ACE-Brain-0.5: A Unified Embodied Foundational Model for Physical Agentic AI](https://arxiv.org/abs/2607.04426v1) · 分数 10
4. [Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments](https://arxiv.org/abs/2605.30280v2) · 分数 10
5. [UAVs Meet Embodied Intelligence: Bridging Human Intents and Flying Dynamics Via Harnessing Physical-Digital AI Agents](https://arxiv.org/abs/2609.18326v1) · 分数 10
6. [TongSIM: A General Platform for Simulating Intelligent Machines](https://arxiv.org/abs/2512.20206v1) · 分数 10
7. [Fundamentals of Physical AI](https://arxiv.org/abs/2511.09497v1) · 分数 10
8. [RoboBrain 2.5: Depth in Sight, Time in Mind](https://arxiv.org/abs/2601.14352v1) · 分数 10
9. [World Action Models: The Next Frontier in Embodied AI](https://arxiv.org/abs/2605.12090v1) · 分数 10
10. [Thinker-WM: A Unified World Model with Shared Multimodal Representations for Embodied Intelligence](https://arxiv.org/abs/2610.18447v1) · 分数 10
11. [GEM: Generative Supervision Helps Embodied Intelligence](https://arxiv.org/abs/2605.28548v1) · 分数 10
12. [DM0: An Embodied-Native Vision-Language-Action Model towards Physical AI](https://arxiv.org/abs/2602.14974v1) · 分数 10
13. [HoloAgent-0: A Unified Embodied Agent Framework with 3D Spatial Memory](https://arxiv.org/abs/2606.23565v1) · 分数 10
14. [EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents](https://proceedings.mlr.press/v267/yang25f.html) · 分数 10
15. [Embodied-R1.5: Evolving Physical Intelligence via Embodied Foundation Models](https://arxiv.org/abs/2606.11324v2) · 分数 10
16. [SEEA-R1: Tree-Structured Reinforcement Fine-Tuning for Self-Evolving Embodied Agents](https://papers.neurips.cc/paper_files/paper/2025/hash/7103cd82de95a7b30983fcf74ba499ac-Abstract-Conference.html) · 分数 10
17. [ME-Brain-1.0: Memory, Cognition and Action for Evolving Embodied Intelligence](https://arxiv.org/abs/2609.24271v1) · 分数 10
18. [Capek 0.5: An Execution-Centric Vision-Language Model for Embodied Intelligence](https://arxiv.org/abs/2608.06756v1) · 分数 10
19. [Co-design of Neural and Muscle Network based on Embodied Perceptron Representation](https://arxiv.org/abs/2608.16555v1) · 分数 10
20. [Robobench: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models as Embodied Brain](https://arxiv.org/abs/2510.17801v2) · 分数 10
21. [ESI-Bench: Towards Embodied Spatial Intelligence that Closes the Perception-Action Loop](https://arxiv.org/abs/2605.18746v2) · 分数 10
22. [TANGO: Training-free Embodied AI Agents for Open-world Tasks](https://openaccess.thecvf.com/content/CVPR2025/html/Ziliotto_TANGO_Training-free_Embodied_AI_Agents_for_Open-world_Tasks_CVPR_2025_paper.html) · 分数 10
23. [ABot-ER: Unified Embodied Reasoning through Agentic Data-Model Co-Evolution](https://arxiv.org/abs/2610.18355v1) · 分数 10
24. [GSR: Learning Structured Reasoning for Embodied Manipulation](https://arxiv.org/abs/2602.01693v1) · 分数 10
25. [Thinker: A vision-language foundation model for embodied intelligence](https://arxiv.org/abs/2601.21199v1) · 分数 10
26. [Embodied Robot Manipulation in the Era of Foundation Models: Planning and Learning Perspectives](https://arxiv.org/abs/2512.22983v2) · 分数 10
27. [Embodied3DBench: Benchmarking Low-Level Embodied Spatial Intelligence of Vision Language Models](https://arxiv.org/abs/2605.29074v1) · 分数 10
28. [Mind to Hand: Purposeful Robotic Control via Embodied Reasoning](https://arxiv.org/abs/2512.08580v2) · 分数 10
29. [BLM&#36;&#95;1&#36;: A Boundless Large Model for Cross-Space, Cross-Task, and Cross-Embodiment Learning](https://arxiv.org/abs/2510.24161v1) · 分数 10
30. [RynnBrain 1.1: Towards More Capable and Generalizable Embodied Foundation Model](https://arxiv.org/abs/2607.17977v2) · 分数 10
31. [Learning 3D Persistent Embodied World Models](https://papers.neurips.cc/paper_files/paper/2025/hash/970f59b22f4c72aec75174aae63c7459-Abstract-Conference.html) · 分数 10
32. [LARM: Large Auto-Regressive Model for Long-Horizon Embodied Intelligence](https://proceedings.mlr.press/v267/li25dj.html) · 分数 10
33. [PhysVLM-AVR: Active Visual Reasoning for Multimodal Large Language Models in Physical Environments](https://papers.neurips.cc/paper_files/paper/2025/hash/05e76d29b99b14f1c63fce1a93b4d4ec-Abstract-Conference.html) · 分数 10
34. [Exploratory, Communicative, and Deployable: Vision-Driven Embodied Agents for Open-World Mobile Manipulation](https://arxiv.org/abs/2607.13653v2) · 分数 10
35. [Unified Embodied VLM Reasoning with Robotic Action via Autoregressive Discretized Pre-training](https://arxiv.org/abs/2512.24125v3) · 分数 10
36. [RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments](https://arxiv.org/abs/2610.10409v1) · 分数 10
37. [SpatialPoint: Spatial-aware Point Prediction for Embodied Localization](https://arxiv.org/abs/2603.26690v1) · 分数 10
38. [Ego to World: Collaborative Spatial Reasoning in Embodied Systems via Reinforcement Learning](https://arxiv.org/abs/2603.14811v1) · 分数 10
39. [RoboAfford++: A Generative AI-Enhanced Dataset for Multimodal Affordance Learning in Robotic Manipulation and Navigation](https://arxiv.org/abs/2511.12436v1) · 分数 10
40. [Guava: An Effective and Universal Harness for Embodied Manipulation](https://arxiv.org/abs/2606.18363v1) · 分数 10
41. [LightNav-0: Eliciting VLM Spatial Intelligence for Generalist Embodied Navigation](https://arxiv.org/abs/2608.30935v1) · 分数 10
42. [Being-H0.5: Scaling Human-Centric Robot Learning for Cross-Embodiment Generalization](https://arxiv.org/abs/2601.12993v1) · 分数 10
43. [ParallelWorld: Test-Time Scaling for Embodied Reasoning](https://arxiv.org/abs/2608.22971v1) · 分数 10
44. [ASENA: Self-evolving Agents for Embodied Navigation](https://arxiv.org/abs/2609.39207v1) · 分数 10
45. [AnyWorld: Factorized Egocentric World Models for Cross-Embodiment Generalization](https://arxiv.org/abs/2608.29242v2) · 分数 10
46. [TrAct: Bridging Robot Control and Visual Prediction with Visual Tracks](https://arxiv.org/abs/2608.24101v3) · 分数 10
47. [Advancing Omnimodal Embodied Agents from Isolated Skills to Everyday Physical Autonomy](https://arxiv.org/abs/2606.27251v1) · 分数 10
48. [&#36;&#92;mathcal&#123;N&#125;&#95;0&#36;-Foundation: Towards the Age of Tactile Intelligence](https://arxiv.org/abs/2608.29601v1) · 分数 10
49. [World Models for Robotic Manipulation: A Survey](https://arxiv.org/abs/2606.00113v1) · 分数 10
50. [RoboMIND 2.0: A Multimodal, Bimanual Mobile Manipulation Dataset for Generalizable Embodied Intelligence](https://arxiv.org/abs/2512.24653v3) · 分数 10
51. [Dream to Manipulate: Compositional World Models Empowering Robot Imitation Learning with Imagination](https://proceedings.iclr.cc/paper_files/paper/2025/hash/8f0d446441a938d9de420a8ab8d7fd36-Abstract-Conference.html) · 分数 10
52. [Grounding 3D Object Affordance with Language Instructions, Visual Observations and Interactions](https://openaccess.thecvf.com/content/CVPR2025/html/Zhu_Grounding_3D_Object_Affordance_with_Language_Instructions_Visual_Observations_and_CVPR_2025_paper.html) · 分数 10
53. [LessMimic: Long-Horizon Humanoid Interaction with Unified Distance Field Representations](https://arxiv.org/abs/2602.21723v1) · 分数 10
54. [&#36;ω&#36;-EVA: Envision, Verify, and Act with Latent Interactive World Models](https://arxiv.org/abs/2606.09457v2) · 分数 10
55. [CoEnv: Driving Embodied Multi-Agent Collaboration via Compositional Environment](https://arxiv.org/abs/2604.05484v1) · 分数 10
56. [Astra: Efficient Transformer Architecture and Contrastive Dynamics Learning for Embodied Instruction Following](https://aclanthology.org/2025.emnlp-main.688/) · 分数 10
57. [InternVLA-M1: A Spatially Guided Vision-Language-Action Framework for Generalist Robot Policy](https://arxiv.org/abs/2510.13778v1) · 分数 10
58. [Vision-Based Tactile Intelligence for Robotics: Sensing, Learning, and Embodied Manipulation](https://arxiv.org/abs/2608.15490v1) · 分数 10
59. [Act, Sense, Act: Learning Active Perception from Large-Scale Egocentric Human Data](https://arxiv.org/abs/2602.04600v2) · 分数 10
60. [ThinkAct: Vision-Language-Action Reasoning via Reinforced Visual Latent Planning](https://papers.neurips.cc/paper_files/paper/2025/hash/7749f9c0d5ff109231be21e910a3ced2-Abstract-Conference.html) · 分数 10
61. [DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos](https://arxiv.org/abs/2602.06949v1) · 分数 10
62. [Learning to infer and manipulate through distributed whole-arm interaction in a soft robot](https://arxiv.org/abs/2608.30773v1) · 分数 10
63. [Zero-shot Interactive Perception](https://arxiv.org/abs/2602.18374v1) · 分数 10
64. [ImagiNav: Scalable Embodied Navigation via Generative Visual Prediction and Inverse Dynamics](https://arxiv.org/abs/2603.13833v1) · 分数 10
65. [From Pixels to Executable Physics: Behavior-Grounded World Models for Embodied Action Consequence Prediction](https://arxiv.org/abs/2610.17630v1) · 分数 10
66. [ST4VLA: Spatially Guided Training for Vision-Language-Action Models](https://arxiv.org/abs/2602.10109v1) · 分数 10
67. [D-World: An Explicit World-Language-Action Model with Recursive Self-Improvement under Dual Control](https://arxiv.org/abs/2610.17114v1) · 分数 10
68. [Self-Improving Embodied Foundation Models](https://papers.neurips.cc/paper_files/paper/2025/hash/a3ac59dc0bf607fa35535f546110fc34-Abstract-Conference.html) · 分数 10
69. [SimWorld-Robotics: Synthesizing Photorealistic and Dynamic Urban Environments for Multimodal Robot Navigation and Collaboration](https://papers.neurips.cc/paper_files/paper/2025/hash/4a81c1aad3064fb8243b8938a49ecca0-Abstract-Conference.html) · 分数 10
70. [From Passive Execution to Active Exploration: Agentic Embodied Manipulation in Realistic Environments](https://arxiv.org/abs/2609.29091v1) · 分数 10
71. [Instruction-Augmented Long-Horizon Planning: Embedding Grounding Mechanisms in Embodied Mobile Manipulation](https://ojs.aaai.org/index.php/AAAI/article/view/33610) · 分数 10
72. [MomaGraph: State-Aware Unified Scene Graphs with Vision-Language Model for Embodied Task Planning](https://arxiv.org/abs/2512.16909v2) · 分数 10
73. [A Comprehensive Survey on World Models for Embodied AI](https://arxiv.org/abs/2510.16732v3) · 分数 9
74. [Intelligence Across Embodiments](https://arxiv.org/abs/2609.27095v1) · 分数 9
75. [World Models for Embodied Intelligence: From Plausible to Controllable to Actionable](https://arxiv.org/abs/2609.16697v1) · 分数 9
76. [FreeAskWorld: An Interactive and Closed-Loop Simulator for Human-Centric Embodied AI](https://arxiv.org/abs/2511.13524v2) · 分数 9
77. [Safety in Embodied AI: A Survey of Risks, Attacks, and Defenses](https://arxiv.org/abs/2605.02900v2) · 分数 9
78. [Knowing More, Acting Better: Hierarchical Representation for Embodied Decision-Making](https://aclanthology.org/2025.findings-emnlp.1042/) · 分数 9
79. [Toward the Cognitive--Physical Limits of Embodied Intelligence through a World-Model-Centric Autonomous Racing Agent](https://arxiv.org/abs/2608.10618v1) · 分数 9
80. [BIP3D: Bridging 2D Images and 3D Perception for Embodied Intelligence](https://openaccess.thecvf.com/content/CVPR2025/html/Lin_BIP3D_Bridging_2D_Images_and_3D_Perception_for_Embodied_Intelligence_CVPR_2025_paper.html) · 分数 9
81. [HY-Embodied-0.5: Embodied Foundation Models for Real-World Agents](https://arxiv.org/abs/2604.07430v1) · 分数 9
82. [iFlyBot-VLM Technical Report](https://arxiv.org/abs/2511.04976v1) · 分数 9
83. [Qwen-RobotWorld Technical Report: Unifying Embodied World Modeling through Language-Conditioned Video Generation](https://arxiv.org/abs/2606.17030v3) · 分数 9
84. [Explicit World Models for Reliable Human-Robot Collaboration](https://arxiv.org/abs/2601.01705v2) · 分数 9
85. [Inspect Robots: Evaluating the Capabilities and Safety of Embodied AI](https://arxiv.org/abs/2610.06306v1) · 分数 9
86. [ME-VLM:A Unified VLM for Embodied Cognition and Agent Coordination](https://arxiv.org/abs/2609.24526v1) · 分数 9
87. [EmbodiedGen V2: An Agentic, Simulation-Ready 3D World Engine for Embodied AI](https://arxiv.org/abs/2607.07459v3) · 分数 9
88. [OrbiSim: World Models as Differentiable Physics Engines for Embodied Intelligence](https://arxiv.org/abs/2605.16395v1) · 分数 9
89. [Bridging VLMs and Embodied Intelligence with Deliberate Practice Policy Optimization](https://arxiv.org/abs/2511.16602v1) · 分数 9
90. [From Digital to Physical: Digital Agents as Autonomous Coaches for Physical Intelligence](https://arxiv.org/abs/2601.21570v2) · 分数 9
91. [Beyond Description: Cognitively Benchmarking Fine-Grained Action for Embodied Agents](https://arxiv.org/abs/2511.18685v4) · 分数 9
92. [ENACT: Evaluating Embodied Cognition with World Modeling of Egocentric Interaction](https://arxiv.org/abs/2511.20937v1) · 分数 9
93. [Minimal Embodiment Enables Efficient Learning of Number Concepts in Robot](https://arxiv.org/abs/2604.11373v1) · 分数 9
94. [GigaWorld-0: World Models as Data Engine to Empower Embodied AI](https://arxiv.org/abs/2511.19861v2) · 分数 9
95. [ACE-Data-0: Human-Centric Ambient Capture as Embodied Data Engine](https://arxiv.org/abs/2607.28625v1) · 分数 9
96. [World Model Implanting for Test-time Adaptation of Embodied Agents](https://proceedings.mlr.press/v267/yoo25a.html) · 分数 9
97. [ABot-Claw: A Foundation for Persistent, Cooperative, and Self-Evolving Robotic Agents](https://arxiv.org/abs/2604.10096v2) · 分数 9
98. [Look, Zoom, Understand: The Robotic Eyeball for Embodied Perception](https://arxiv.org/abs/2511.15279v2) · 分数 9
99. [Semantic Intelligence: A Bio-Inspired Cognitive Framework for Embodied Agents](https://arxiv.org/abs/2510.17129v1) · 分数 9
100. [The Semantic Lifecycle in Embodied AI: Acquisition, Representation and Storage via Foundation Models](https://arxiv.org/abs/2601.08876v1) · 分数 9

[按公布时间查看](#/starter-pack/20261015-25c1e19060da/dates)

阅读内容：已完成 10，待补充 90。
