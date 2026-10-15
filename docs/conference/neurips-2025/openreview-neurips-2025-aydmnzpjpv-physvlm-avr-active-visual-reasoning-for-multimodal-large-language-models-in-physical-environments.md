---
title: "PhysVLM-AVR: Active Visual Reasoning for Multimodal Large Language Models in Physical Environments"
authors: "Weijie Zhou, Xuantang Xiong, Yi Peng, Manli Tao, Chaoyang Zhao, Honghui Dong, Ming Tang, Jinqiao Wang"
date: 2025
pdf: "https://papers.neurips.cc/paper_files/paper/2025/file/05e76d29b99b14f1c63fce1a93b4d4ec-Paper-Conference.pdf"
tags: ["query:embodied-ai"]
score: 10
source: NeurIPS-2025-Accepted
selection_source: long-range
publication_date: 2025
publication_date_precision: year
publication_date_source: conference year only; exact release date unverified
publication_date_kind: unknown
id: openreview-neurips-2025-aydmnzpjpv
canonical_id: "work:8fbf46818d8f805a5b7cea99"
research_run_id: 20261015-25c1e19060da
research_mode: starter
reading_status: pending
---

## Abstract
Visual reasoning in multimodal large language models (MLLMs) has primarily been studied in passive, static settings, limiting their effectiveness in real-world physical environments where an embodied agent must contend with incomplete information due to occlusion or a limited field of view. Humans, in contrast, leverage their embodiment to actively explore and interact with their environment—moving, examining, and manipulating objects—to gather information through a closed-loop process integrating perception, reasoning, and action. Inspired by this capability, we introduce the Active Visual Reasoning (AVR) task, extending visual reasoning to a paradigm of embodied interaction in partially observable environments. AVR necessitates embodied agents to: (1) actively acquire information via sequential physical actions, (2) integrate observations across multiple steps for coherent reasoning, and (3) dynamically adjust decisions based on evolving visual feedback. To rigorously evaluate AVR, we introduce CLEVR-AVR, a simulation benchmark featuring multi-round interactive environments designed to assess both reasoning correctness and information-gathering efficiency. We present AVR-152k, a large-scale dataset that offers rich Chain-of-Thought (CoT) annotations detailing iterative reasoning for uncertainty identification, action-conditioned information gain prediction, and information-maximizing action selection, crucial for training agents in a higher-order Markov Decision Process. Building on this, we develop PhysVLM-AVR, an embodied MLLM achieving state-of-the-art performance on CLEVR-AVR, embodied reasoning (OpenEQA, RoboVQA), and passive visual reasoning (GeoMath, Geometry30K). Our analysis also reveals that current embodied MLLMs, despite detecting information incompleteness, struggle to actively acquire and integrate new information through interaction, highlighting a fundamental gap in active reasoning capabilities.

## 专题评审

专题相关性评分：10/10。

直接研究具身智能体通过动作获取信息并闭环推理，符合感知、行动与环境交互主题。

<!-- research-reading-pending -->
中文总结与全文内容待生成；当前仅提供原始论文元数据与摘要。
<!-- /research-reading-pending -->
