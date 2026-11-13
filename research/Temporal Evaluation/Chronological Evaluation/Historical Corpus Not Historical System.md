---
title: "Historical Corpus Not Historical System"
aliases: ["A Historical Corpus Is Not a Historical System: Auditing Hindsight Leakage in Stateful Data Discovery"]
authors: ["Yixi Zhou", "Fan Zhang", "Sikun Wang", "Yingfan Xu", "Haipeng Zhang"]
year: 2026
venue: "arXiv preprint"
arxiv: "2609.12766"
url: "https://arxiv.org/abs/2609.12766"
citekey: zhou2026historical
verified: 2026-11-11
theme: "[[Chronological Evaluation]]"
tags: [type/paper, theme/chronological, topic/leakage, topic/temporal, topic/evaluation, topic/bm25, topic/dense-retrieval]
---
# Historical Corpus Not Historical System

> [!info] TL;DR
> Freezing the corpus for a historical replay does not freeze a stateful retriever: caches, query traces or profiles built from the full log carry interactions from after the query. The paper defines point-in-time (PIT) state as corpus plus model plus memory observed before the query, and pairs PIT with a full-stream "Future" view that differs only in memory eligibility. Across three table-text domains, Future inflates Asset Recall@100 by 2.62 to 5.24 points, and every interval excludes zero. Hindsight hides 32.7% to 48.4% of the harm of a trace memory that is worse than no memory, and on FreshStack's real query order Future still gains 2.72 points.

## Motivation

- Data discovery benchmarks (DPDisc, CMDBench, TARGET) give every request a stateless retriever, while deployed systems reuse prior interactions.
- Conversational and long-memory benchmarks define the history for a turn but never pair one query under past-only and full-stream memory.
- Temporal IR benchmarks vary corpus, model or query over time ([[StreamingQA]]; [[LongEval 2023]]) rather than isolating interaction memory.
- Recommender leakage studies impose a global timeline but change training data, user histories and item availability together ([[Data Leakage in Recommender Evaluation]]; [[Dont Get Ahead of Yourself]]).
- An aggregate score cannot show whether a gain came from historical evidence or later experience.

## Method

Notation: asset corpus $D_t$ frozen at time $t$; parameters and index $\theta_t$; request $q_i$ at stream position $i$; event $e_j$ observed at position $j$; memory $M$; budgets $B$. The paper's anchor $q_i$ plays the role of our post $q$.

**Historical state.** A stateful system returns $R_i = R(q_i; D_t, \theta_t, M_i, B)$. A valid historical state is

$$
S_{t,i} = (D_t,\ \theta_t,\ M_{<i}) ,
$$

where $M_{<i}$ holds only events observed before the anchor.

Intuition: a frozen corpus with full-log memory combines yesterday's assets with tomorrow's experience, a system that never existed.

**Three clocks.** Content clock $c(a)$ for when asset $a$ enters the corpus, observation clock $o(e_j)$ for when the system sees an event, and materialisation clock $\mu(M)$ for when the evaluator builds memory. Every asset and event that influences an output must satisfy

$$
\mathbb{1}[c(a) \le t]\ \mathbb{1}[o(e_j) < o(q_i)] = 1 .
$$

Materialisation time alone certifies nothing; each entry needs its own observation time.

**Memory views** at anchor $i$, all excluding the anchor's own event: Stateless $M^S_i = \emptyset$; PIT $M^P_i = \{e_j : j < i\}$; Future-$h$ $M^{F(h)}_i = M^P_i \cup \{e_j : i < j \le i+h\}$; Future $M^F_i = \{e_j : j \ne i\}$. A Naive view pre-materialises memory from the whole log and must equal Future.

**Metrics.** Hindsight Gain at cutoff $k$, the Temporal Violation Rate over the selected entries $A^c_i$, and the masked-harm fraction when PIT is below Stateless:

$$
\text{HG}_k = m_k(R^F_i) - m_k(R^P_i), \qquad \text{TVR}^c_i = \frac{1}{|A^c_i|}\sum_{e_j \in A^c_i} \mathbb{1}[j > i], \qquad \text{MHF} = \frac{S(F) - S(P)}{|S(P) - S(S)|} .
$$

A PIT run is valid only if TVR is zero on every row. Derived state takes the latest observation time among its ancestors.

**Trace memory.** After each stream query the fixed base retriever's top $d = 50$ assets and scores are logged, without labels. For an anchor, the 1,024 nearest past or future queries are scanned and the first 32 allowed by the view are kept. With neighbour similarity $s_{ij}$ and trace rank $r_{ja}$,

$$
u_i(a) = \sum_{j \in N_i} \frac{s_{ij}^2}{\log_2(r_{ja} + 2)} ,
$$

max-normalised, then $0.2\,u_i(a)$ is added to the base reciprocal rank $1/(r_i(a)+1)$ and the top 200 are returned.

**Positive-feedback proxy.** A query's gold assets stand in for perfect clicks; related later queries get a bonus capped at 0.02, the reciprocal score at base rank 50.

## Implementation

- **Code:** not released; manifests with hashes are described.
- **Software:** Python, NumPy, SciPy, scikit-learn, PyTorch, Sentence Transformers; four RTX 3090 GPUs for embeddings and neighbour search, CPU for replay.
- **Retrievers:** BM25 ($k_1 = 1.5$, $b = 0.75$) and a hybrid fusing BM25 and all-mpnet-base-v2 top-200 lists by RRF with constant 60.
- **Audit:** SHA-256 hashes for corpus, assets, queries, embeddings and outputs; 15 unit tests for budget parity, self exclusion, gold-label isolation and the Naive equals Future control; PIT runs abort on nonzero TVR.
- **Statistics:** contrasts averaged per query identifier, then 5,000 query-cluster bootstrap resamples.

## Data

- DPDisc (from DPBench), train, development and test pooled because labels only score: ConvFinQA 3,113 queries over 13,697 assets (13.16 gold each), HybridQA 8,820 over 53,986 (30.61), TAT-QA 1,143 over 7,517 (10.52, held-out robustness domain).
- Streams: random permutations, and semantic bursts of 4 to 16 queries from MiniBatch $k$-means on query embeddings; five seeds each; no gold labels used for ordering.
- Anchors: 100 around each of the 20%, 40%, 60% and 80% positions; nine conditions; 216,000 query-condition rows.
- FreshStack: Angular, Godot, LangChain, Laravel and YOLO topics, 672 queries over 271,816 text assets, ordered by recorded query time; 592 anchors with at least eight past and eight future events.

## Experiments

- **Primary pair:** Future vs PIT in 12 cells of domain, stream and retriever; Asset Recall@100.
- **Memory utility:** PIT vs Stateless and the masked-harm fraction.
- **Useful memory:** the positive-feedback proxy in the same 12 cells.
- **Horizon dose:** Future-$h$ for $h \in \{10, 50, 100, 250, 500\}$, and HG by anchor position.
- **Robustness:** retriever swap, near-duplicate neighbours (cosine ≥ 0.99) removed, other cutoffs and product metrics, FreshStack natural order.
- **Audit:** TVR and Naive vs Future identity.

## Results

- HG ranges from +2.62 (HybridQA, random, BM25) to +5.24 (ConvFinQA, semantic, BM25); TAT-QA +4.69 to +5.13.
- The PIT memory effect is −14.37 to −6.57 points in all 12 cells; Future masks 32.7% to 48.4% of that harm and stays below Stateless.
- With the positive-feedback proxy, Stateless < PIT < Future in all 12 cells: PIT adds 4.65 to 18.96 points and Future another 4.11 to 9.58.
- Ten future queries already add 0.65 to 1.36 points in semantic streams with the hybrid retriever; no random-stream horizon-10 interval excludes zero.
- At horizon 500, semantic streams recover 56% of full HG on ConvFinQA, 42% on HybridQA and 96% on TAT-QA, so no small look-ahead is safe in general.
- HG falls from 7.26 points at the 20% anchor to 1.43 at 80%, with all 32 slots filled in both views.
- Switching retriever changes HG by at most 0.44 points; removing near-duplicate neighbours keeps 99.9% to 100% of rows and the same HG range.
- FreshStack: HG +2.72 (CI 1.75 to 3.71); PIT memory is 4.58 points below Stateless.
- PIT TVR is zero over 24,000 PIT anchor evaluations; Future fills 50.1% to 54.0% of slots with post-anchor entries; Naive equals Future exactly.

## Limitations

- Three DPDisc domains, two retrievers, two transparent memory mechanisms and five FreshStack topics (authors).
- Asset recall only; answer quality and user satisfaction are not measured (authors).
- The fixed-log replay excludes long-run effects where rankings change later interactions (authors).
- Streams are synthetic orders of benchmark queries, except FreshStack (ours).
- Pretraining contamination and corpus drift are outside the estimand by design (authors).

## Relation to our project

- **Novelty claim not contradicted.** The paper is table-text data discovery, not PFCR. Its corpus is fixed and only interaction memory is cut at the query, the reverse of our design, where the fact-check pool itself is cut at each post.
- It does define per-query eligibility $c(a) \le t$ for corpus content, but it holds the corpus constant and measures memory only.
- Its rule that derived state inherits the latest timestamp among its ancestors applies to our BM25 statistics, embeddings fine-tuned on later data and LLM rerankers ([[TREC 2011 Microblog]]; [[LLM Temporal Leakage]]).
- Its paired within-query design and Naive equals Future identity check are a model for our full versus causal pool comparison ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- Its point that leakage can hide a harmful component supports reporting rank changes between protocols, not only score drops ([[Chronological Evaluation]]).

## Future work

- **Open:** applying the paired replay to production logs and learned memories with event lineage, which the authors scope out (searched 2026-11).
- **Open:** branch-specific logs to measure long-run feedback from rankings to later interactions (searched 2026-11).
- **Open:** the same audit for retrieval-augmented assistants and tool-use agents, which the authors name (searched 2026-11).
