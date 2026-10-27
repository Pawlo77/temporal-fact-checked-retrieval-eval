---
title: "MultiClaimNet"
aliases: ["MultiClaimNet: A Massively Multilingual Dataset of Fact-Checked Claim Clusters"]
authors: ["Rrubaa Panchendrarajan", "Rubén Míguez Pérez", "Arkaitz Zubiaga"]
year: 2025
venue: "Findings of the Association for Computational Linguistics: EMNLP 2025, Suzhou, pages 11203-11215"
doi: "10.18653/v1/2025.findings-emnlp.599"
url: "https://aclanthology.org/2025.findings-emnlp.599/"
citekey: panchendrarajan2025multiclaimnet
verified: 2026-10-27
theme: "[[Datasets and Benchmarks]]"
tags: [type/paper, theme/datasets, topic/multilingual, topic/embedding, topic/llm, topic/benchmark, topic/temporal]
---
# MultiClaimNet

> [!info] TL;DR
> MultiClaimNet releases three datasets of fact-checked claims grouped into clusters that state the same fact, covering 86 languages. The largest groups 85.3K [[MultiClaim]] fact-checks into 30.9K clusters using nearest-neighbour candidates labelled by three LLMs, with no human labelling. Agglomerative clustering on BGE-M3 embeddings works best on the large set, and small (<1B) embedders beat 7B ones.

## Motivation

- PFCR compares each new post with every fact-check; grouping repeated claims could reduce redundancy as archives grow.
- Earlier clustering work ([[Claim Matching Beyond English]]; [Quelle et al., 2023](https://arxiv.org/abs/2310.18089)) only checked that clusters exist, without ground truth to score them.
- Manual cluster annotation is costly, so no claim-cluster dataset existed.

## Method

We write a fact-checked claim as $f$; the paper calls a claim pair "similar" when both discuss the same underlying fact, following the ClaimCheck definition.

**Clusters from pairs.** Similar pairs are treated as undirected links; connected claims form one cluster.

Intuition: if A matches B and B matches C, all three state one fact.

**Small datasets.** ClaimCheck (5.2K similar pairs, mixed manual and automatic labels) and ClaimMatch (1.5K manually labelled similar pairs), both from Newtral. Clusters with cosine similarity above 0.75 were inspected and merged by hand; clusters above 20 claims were checked for wrong merges, and none were found.

**Large dataset.** Each MultiClaim claim's English translation is embedded and its single nearest neighbour retrieved with HNSW, giving 162K candidate pairs. Exact translations are labelled similar automatically; the remaining 160K are labelled by seven LLMs, of which GPT-4, Phi-3 14B and Falcon 40B agree most (77-80%) and are kept. Only pairs all three call similar are linked (54K pairs), giving 31.2K sub-clusters.

**Merging.** Each sub-cluster is embedded as the mean of its claims; its 20 nearest sub-clusters give 25K candidate pairs above cosine 0.75. Pairs with unanimous LLM labels (8.5K) merge sub-clusters into 30.9K final clusters.

**Benchmark.** Six clustering algorithms that need no preset cluster count, and the 15 multilingual sentence embedders listed (the text says sixteen) on original-language text; scored with ARI, AMI, homogeneity, completeness, V-measure and purity.

## Key numbers

- Sizes: ClaimCheck 1,187 claims, 197 clusters, 22 languages; ClaimMatch 1,171 claims, 192 clusters, 36 languages; MultiClaim 85.3K claims, 30.9K clusters (average size 2.76, maximum 54), 78 languages.
- The MultiClaim set has 15.9K monolingual and 15K multilingual clusters; multilingual clusters hold 2.4 languages on average.
- Repeats are fast: 50% of repeated claims appear within 1.6 days and 75% within 29.3 days of the first claim in their cluster.
- On the MultiClaim set, agglomerative clustering with BGE-M3 reaches ARI 0.574 and V-measure 0.967; HDBSCAN reaches ARI 0.007.

## Experiments

- **Clustering algorithms:** affinity propagation leads on the small sets; only agglomerative clustering works on the large set, while HDBSCAN produces overly fine clusters there.
- **Embedders:** gte-multilingual-base is best on the small sets and [[BGE-M3]] on the large set; larger LLM-based embedders do not help, and LLM2Vec is worst.
- **Sensitivity:** the number of clusters found by agglomerative clustering varies 4-7.5 times more across embedders than HDBSCAN's.
- **Errors:** misgrouping from unrecognised entity aliases, missing background knowledge, ignored keywords, noisy claims, implicit claims, and merges driven by shared entities.

## Data

- ClaimCheck, ClaimMatch and MultiClaim cluster sets, as above; fields are claim, cluster id, language, English translation and claim id, plus timestamp and URL for the MultiClaim set.
- Zenodo record 15100352, restricted, research use only.

> [!failure] Limitations
> - Large-set clusters rest on LLM labels with no human validation of a sample reported.
> - One nearest neighbour per claim and unanimous-vote filtering miss links, so true clusters can be split.
> - Labels use claim text only; claims about different images or videos can be merged.
> - Claims stating several facts can link unrelated clusters.
> - Only 85.3K of MultiClaim's fact-checks are clustered.

## Relation to our project

- Cluster ids plus timestamps let us find an earlier fact-check of the same claim for a post whose gold fact-check is later, the basis of our cluster-expanded causal protocol and sibling qrels ([[Proposed Task]]).
- The fast repeat times suggest many posts have a same-cluster fact-check shortly before them, which bears on answerability under a causal pool ([[Enhanced topic research]]).
- LLM-made clusters inherit LLM errors; we validate sibling relevance by hand and report coverage of unclustered fact-checks ([[Research summary]]).

## Future work

- **Partly done:** better claim representations for clustering; [Claim2Vec](https://arxiv.org/abs/2604.09812) (Panchendrarajan et al., 2026) fine-tunes a multilingual encoder on MultiClaimNet pairs.
- **Open:** cluster retrieval, matching a post against whole clusters instead of single fact-checks (searched 2026-10).
- **Open:** iterative clustering that adds new claims over time, as the paper proposes (searched 2026-10).
