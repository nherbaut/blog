---
date: '2025-10-17T10:25:45+02:00'
title: What causes model size inflation and what could researchers do about it?
draft: false
type: articles
article_doi: https://doi.org/10.1145/3715275.3732006
article_oaurl: http://arxiv.org/pdf/2409.14160
article_topics:
- Sustainability
- Paradigm shift
- Scale (ratio)
article_article_authors:
- Gaël Varoquaux
- Alexandra Sasha Luccioni
- Meredith Whittaker
article_title: Hype, Sustainability, and the Price of the Bigger-is-Better Paradigm
  in AI
article_venue: 'FAccT: Fairness, Accountability, and Transparency'
article_publication_year: 2025
---

# Context and Motivation

*"All of our experiments suggest that our results can be improved simply by waiting for faster GPUs and bigger datasets to become available."*[^alexnet]

[^alexnet]: Krizhevsky, Alex, Ilya Sutskever, and Geoffrey E. Hinton. *Imagenet classification with deep convolutional neural networks.* *Advances in Neural Information Processing Systems* 25 (2012).

The AI field is dominated by large players and driven by a “bigger is better” paradigm. This creates constraints in several areas:
- Smaller, more specialized models can often compete with large general-purpose ones.
- The approach is environmentally unsustainable, especially due to inference, which now accounts for a larger share of total impact than training.
- Training requires massive amounts of data, often containing biases and privacy risks.
- Academic researchers lack access to sufficient GPU resources and must rely on large industrial partners competing for them.

The authors review current literature to provide detailed arguments supporting these points.

---

# Main Contributions

This is an opinion paper highlighting the negative consequences of the race toward ever-larger models. It argues that model size is only one dimension of performance improvement, and that benchmark-based evaluation has led to a narrow and flawed view of progress. Other important dimensions such as calibration and explainability are often neglected.

From a sustainability standpoint, inference now has a larger environmental impact than training, given its pervasive deployment. The authors show that for specific use cases, general-purpose AI models often perform similarly to smaller, task-specific ones but at a fraction of the cost and impact.

They also discuss data issues, emphasizing that large datasets are poorly documented, biased, and often include copyrighted or illegal content. Data contamination (e.g., benchmark leakage) further undermines evaluation results. Privacy is also threatened, as much of AI revenue comes from targeted advertising.

Economically, the authors note that academia struggles to contribute due to limited access to compute resources. Large corporations dominate the field, while startups spend a large share of their funding on API access to industrial models. This concentration of power suppresses innovation and aligns AI development with corporate  interests, heightening geopolitical tensions.

---

# Methodology

The paper is an opinionated survey without a formal methodology.

---

# Results and Findings

The authors propose three actions for the ML community:
- Introduce conference tracks focused on model efficiency and cost reduction, and require comparisons to simpler baselines.
- Encourage transparency about the financial and environmental cost of ML research.
- Promote realistic expectations for model evaluation, avoiding unnecessary large-scale experiments.

Ultimately, they call for a shift in the ML community toward improving both performance and efficiency.

---

# Strengths

The paper challenges current ML research practices by centering societal, environmental, and economic concerns. It takes an uncommon but valuable position in mainstream research and offers a holistic view of the problems with well-supported arguments against the model size race.

---

# Limitations or Open Questions

While the recommendations are valuable for the ML community, the authors provide limited insight into addressing the broader societal consequences they identify. The issues extend beyond academia.

Apart from environmental impacts, the paper does not deeply explore the human implications of the model size race—such as its effects on fulfilling human needs or social well-being.

---

# My Take / Why It Interests Me

This paper is relevant to me because it critically examines the current AI landscape from a machine learning research perspective. It provides useful evidence and reasoning that can support sustainability-focused AI research.
