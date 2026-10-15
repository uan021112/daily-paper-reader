---
title: "Dream to Manipulate: Compositional World Models Empowering Robot Imitation Learning with Imagination"
authors: "Leonardo Barcellona, Andrii Zadaianchuk, Davide Allegro, Samuele Papa, Stefano Ghidoni, Efstratios Gavves"
date: 2025
pdf: "https://proceedings.iclr.cc/paper_files/paper/2025/file/8f0d446441a938d9de420a8ab8d7fd36-Paper-Conference.pdf"
tags: ["query:embodied-ai"]
score: 10
source: ICLR-2025-Accepted
selection_source: long-range
publication_date: 2025
publication_date_precision: year
publication_date_source: conference year only; exact release date unverified
publication_date_kind: unknown
id: openreview-iclr-2025-3rslw9ysgk
canonical_id: "work:8c06834993c421d356c70199"
research_run_id: 20261015-25c1e19060da
research_mode: starter
reading_status: pending
---

## Abstract
A world model provides an agent with a representation of its environment, enabling it to predict the causal consequences of its actions. Current world models typically cannot directly and explicitly imitate the actual environment in front of a robot, often resulting in unrealistic behaviors and hallucinations that make them unsuitable for real-world robotics applications. 
To overcome those challenges, we propose to rethink robot world models as learnable digital twins. We introduce DreMa, a new approach for constructing digital twins automatically using learned explicit representations of the real world and its dynamics, bridging the gap between traditional digital twins and world models.
DreMa replicates the observed world and its structure by integrating Gaussian Splatting and physics simulators, allowing robots to imagine novel configurations of objects and to predict the future consequences of robot actions thanks to its compositionality.
We leverage this capability to generate new data for imitation learning by applying equivariant transformations to a small set of demonstrations. Our evaluations across various settings demonstrate significant improvements in accuracy and robustness by incrementing actions and object distributions, reducing the data needed to learn a policy and improving the generalization of the agents. 
As a highlight, we show that a real Franka Emika Panda robot, powered by DreMa’s imagination, can successfully learn novel physical tasks from just a single example per task variation (one-shot policy learning).
Our project page can be found in: https://dreamtomanipulate.github.io/.

## 专题评审

专题相关性评分：10/10。

直接研究机器人世界模型、环境动力学预测及其在操作模仿学习中的应用。

<!-- research-reading-pending -->
中文总结与全文内容待生成；当前仅提供原始论文元数据与摘要。
<!-- /research-reading-pending -->
