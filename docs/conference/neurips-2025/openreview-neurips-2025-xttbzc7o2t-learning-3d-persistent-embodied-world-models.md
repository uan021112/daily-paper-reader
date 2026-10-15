---
title: Learning 3D Persistent Embodied World Models
authors: "Siyuan Zhou, Yilun Du, Yuncong Yang, Lei Han, Peihao Chen, Dit-Yan Yeung, Chuang Gan"
date: 2025
pdf: "https://papers.neurips.cc/paper_files/paper/2025/file/970f59b22f4c72aec75174aae63c7459-Paper-Conference.pdf"
tags: ["query:embodied-ai"]
score: 10
source: NeurIPS-2025-Accepted
selection_source: long-range
publication_date: 2025
publication_date_precision: year
publication_date_source: conference year only; exact release date unverified
publication_date_kind: unknown
id: openreview-neurips-2025-xttbzc7o2t
canonical_id: "work:926dba2448a22c4c56c3599f"
research_run_id: 20261015-25c1e19060da
research_mode: starter
reading_status: pending
---

## Abstract
The ability to simulate the effects of future actions on the world is a crucial ability of intelligent embodied agents, enabling agents to anticipate the effects of their actions and make plans accordingly. While a large body of existing work has explored how to construct such world models using video models, they are often myopic in nature, without any memory of a scene not captured by currently observed images, preventing agents from making consistent long-horizon plans in complex environments where many parts of the scene are partially observed. We introduce a new persistent embodied world model with an explicit memory of previously generated content, enabling much more consistent long-horizon simulation. During generation time, our video diffusion model predicts RGB-D video of the future observations of the agent. This generation is then aggregated into a persistent 3D map of the environment. By conditioning the video model on this 3D spatial map, we illustrate how this enables video world models to faithfully simulate both seen and unseen parts of the world. Finally, we illustrate the efficacy of such a world model in downstream embodied applications, enabling effective planning and policy learning.

## 专题评审

专题相关性评分：10/10。

直接构建具身世界模型以预测行动后果并支持规划和策略学习。

<!-- research-reading-pending -->
中文总结与全文内容待生成；当前仅提供原始论文元数据与摘要。
<!-- /research-reading-pending -->
