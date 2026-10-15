---
title: "Knowing More, Acting Better: Hierarchical Representation for Embodied Decision-Making"
authors: "Chunhui Zhang, Zhongyu Ouyang, Xingjian Diao, Zheyuan Liu, Soroush Vosoughi"
date: 2025
pdf: "https://aclanthology.org/2025.findings-emnlp.1042.pdf"
tags: ["query:embodied-ai"]
score: 9
source: EMNLP-2025-Findings
selection_source: long-range
publication_date: 2025
publication_date_precision: year
publication_date_source: conference year only; exact release date unverified
publication_date_kind: unknown
id: anthology-2025.findings-emnlp.1042
canonical_id: "work:7a426ec0e03efc495c0b55ac"
research_run_id: 20261015-25c1e19060da
research_mode: starter
reading_status: pending
---

## Abstract
Modern embodied AI uses multimodal large language models (MLLMs) as policy models, predicting actions from final-layer hidden states. This widely adopted approach, however, assumes that monolithic last-layer representations suffice for decision-making—a structural simplification at odds with decades of cognitive science, which highlights the importance of distributed, hierarchical processing for perception and action. Addressing this foundational asymmetry, we introduce a hierarchical action probing method that explicitly aggregates representations from all layers, mirroring the brain’s multi-level organization. Experiments reveal that early layers facilitate spatial grounding, middle layers support contextual integration, and later layers enable abstract generalization—which shows MLLMs inherently encode distributed action-relevant structures. These layer-wise features are integrated by a lightweight probe for spatial reasoning and contextual understanding, without costly backbone fine-tuning. This hierarchical solution shows significant improvements over standard last-layer embodied models in physical simulators, achieving a 46.6% success rate and a 62.5% gain in spatial reasoning tasks. These findings challenge conventional assumptions in embodied AI, establishing hierarchical probing as a principled alternative grounded in both cognitive theory and empirical evidence.

## 专题评审

专题相关性评分：9/10。

研究具身模型的分层表征如何提升物理模拟器中的空间推理与任务成功率。

<!-- research-reading-pending -->
中文总结与全文内容待生成；当前仅提供原始论文元数据与摘要。
<!-- /research-reading-pending -->
