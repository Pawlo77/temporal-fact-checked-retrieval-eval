---
title: "LLM selection and single-model risk"
type: plan-note
domain: vault
parent: "[[2026-10-27-temporal-retrieval-eval]]"
tags: [plan, llm, model-selection, llm-as-judge, temporal-leakage, study-design]
created: 2026-10-27
updated: 2026-10-27
related:
  - "[[2026-10-27-temporal-retrieval-eval]]"
  - "[[Topic research]]"
  - "[[Language scope]]"
  - "[[Qwen3 Embedding]]"
  - "[[polish-reranker-roberta-v3]]"
  - "[[bge-reranker-v2-m3]]"
  - "[[SemEval-2025 Task 7]]"
  - "[[TIFIN India]]"
  - "[[Multilingual vs Crosslingual Retrieval]]"
  - "[[AMC-16K]]"
  - "[[Language and Retrieval Bias]]"
  - "[[Generative-AI Claim Retrieval]]"
  - "[[MultiClaimNet]]"
  - "[[CheckThat 2022 Task 2]]"
  - "[[Simulated Ignorance Fails]]"
  - "[[All Leaks Count]]"
  - "[[Temporal Leakage in Date-Filtered Web Retrieval]]"
  - "[[LLM Temporal Leakage]]"
---
# LLM selection and single-model risk

Sources checked on 2026-10-27 against primary pages (papers, model cards); numbers are the sources' numbers, VRAM figures are weights-only arithmetic (bf16, 2 bytes per parameter, KV cache extra).

**Goal:** replace the single Qwen3 family in [[2026-10-27-temporal-retrieval-eval]] (Systems, RQ5, LLM judgments) with a model set whose conclusions survive a change of family, size, cutoff and openness.

**Architecture:** evaluated LLMs (retrievers, rerankers) and judging LLMs (sibling qrels, narrative drift) come from disjoint families; RQ5 uses several models with stated cutoffs plus open-data models whose pretraining corpus can be searched; human labels arbitrate.

**Tech Stack:** open weights served locally (vLLM or Hugging Face) on A100 80 GB nodes; optional API ceiling only if [[MultiClaim]] access terms allow sending post text.

## Verdict

Yes, a single family is a real research risk, and the largest one sits in RQ5 and in the LLM-made labels, not in the retrieval scores. Parametric leakage is a property of one model's pretraining data and cutoff, and Qwen3 states no cutoff, so a pre/post-cutoff stratification built on it has no defensible boundary and cannot generalise; effective cutoffs also differ from reported ones (Cheng et al., 2024). If the same family supplies a pooled system and the judge of sibling qrels, LLM judges are documented to favour LLM rankers (Balog et al., SIGIR 2025) and their own outputs (Panickssery et al., NeurIPS 2024), which would bias exactly the cluster-expanded protocol of RQ2. Fix: at least four evaluated LLM families with stated cutoffs spread over the query period, two of them with released pretraining data (Apertus, Olmo 3) and one Polish-specialised (Bielik), a three-family judge panel disjoint from them, human-validated agreement, and pinned open weights. Cost and compute do not block this on A100 nodes.

## Risks

| Risk | Where it bites in the plan | Evidence | Mitigation |
|---|---|---|---|
| RQ5 findings are one model's | RQ5; S5 LLM-scale row | Each model's Brier score jumps at its own cutoff, not a common date ([[Simulated Ignorance Fails]], nine models); [[All Leaks Count]] uses three LLMs for the same reason | Four or more reranker families; test whether the gain jump tracks each model's own cutoff |
| No stated or reliable cutoff | Pre/post-cutoff strata of RQ5 | Qwen3 blog and report state no cutoff ([[Qwen3 Embedding]]); effective cutoffs often differ from reported ones because of old data in new CommonCrawl dumps and deduplication (Cheng et al., 2024) | Models with stated cutoffs; open-data models whose corpus can be searched for the gold fact-check; Qwen3 kept as "cutoff unknown" |
| Prompted cutoff used as a fix | Any "pretend it is date t" prompt | Cutoff instruction closes only 48% of the gap ([[Simulated Ignorance Fails]]) | Already excluded in the plan; keep it out of judge prompts too |
| Self-preference when judge and judged share a family | Sibling qrels, narrative drift, failure coding | LLM judges show significant bias towards LLM-based rankers (Balog et al., SIGIR 2025); self-recognition correlates linearly with self-preference (Panickssery et al., NeurIPS 2024); with rubric verdicts, judges can be over 50% more likely to pass their own failed outputs (arXiv 2604.06996) | Judge families disjoint from every evaluated and pooled system; leave-one-judge-out rerun |
| Circular qrels | Cluster-expanded causal protocol; RQ2 gap chain | Sibling qrels pool the top 10 of S2, S4 and S5 ([[Topic research]]); LLM labels correlate with humans but do not reliably separate top systems and can be gamed (Clarke and Dietz, arXiv 2412.17156) | Report every system under fact-checker-only qrels and under expanded qrels; humans label a stratified sample per pooled system |
| Judge weaker on Polish | Polish sibling qrels and drift labels; H-PL test | Lowest monolingual scores for Slavic languages; Llama 3.1 answered in a non-English language in 37% (8B) and 28% (70B) of chain-of-thought outputs, Polish the most ([[AMC-16K]]); target-language instructions change macro F1 by -4.00 zero-shot ([[Language and Retrieval Bias]]) | Validate each judge on the 400 Polish [[AMC-16K]] pairs before use; English instructions plus task description; per-language agreement |
| Topic-only false positives | Sibling count covariate; answerable rate | About 65% of 420 reviewed misclassifications were same-topic false relevance ([[AMC-16K]]); COVID-19 is 49.5% of retrieved claims ([[Language and Retrieval Bias]]) | Topic-stratified human audit; report judge precision on same-topic negatives |
| API drift and non-determinism | Reproducibility of reranker and judge rows | GPT-4 prime identification fell from 84% (March 2023) to 51% (June 2023) (Chen et al., arXiv 2307.09009); "deterministic" settings still swing accuracy up to 15% across runs (Atil et al., arXiv 2408.04667) | Open weights with commit hashes; temperature 0, fixed seed, cached outputs; API only as a dated ceiling row |
| Licence and data-access terms | Data release; any API call | MultiClaim is research-only with no re-sharing ([[Topic research]]); Gemma terms, Llama 3.3 Community License, Command A CC-BY-NC, Mistral Research License (model cards) | Local inference only for post text; release prompts, ids and labels, never text; record each licence in the results table |
| Language coverage | Seven-language dose-response ([[Language scope]]) | Llama 3.3 does not list Polish; Qwen3 lists Polish among 119 languages; Gemma 3 over 140; Command A and Mistral Large list Polish (model cards) | Prefer models listing Polish; run the LLM reranker on Polish and English first, as the scope plan says |
| Contamination with fact-check sites | RQ1 to RQ5 for every pretrained model | Contamination inflates fake-news detection scores by up to 23% across 17 LLMs (TripleFact, ACL 2025); fact-check-site claims stay easy after cutoffs (Chen, Huang and Dhingra, arXiv 2410.14651); Qwen3 embedders are trained on queries generated from the Qwen3 pretraining corpus ([[Qwen3 Embedding]]) | Exposure indicator per gold fact-check for open-data models; stratify, never claim leakage removed |
| Cost and compute | W3 timeline | RankGPT reranking cost about $50 per test experiment ([[Multilingual vs Crosslingual Retrieval]]); a three-family panel was over seven times cheaper than a single GPT-4 judge (Verga et al., arXiv 2404.18796) | Open weights on HPC; rerank top 30 to 50 only; cache every call |

## What other papers use

| Paper | Role | Models | Languages | Result |
|---|---|---|---|---|
| [[TIFIN India]] (SemEval-2025) | Listwise reranker of top 50, RRF fusion | Qwen2.5-72B-Instruct | Translated to English; Polish test | S@10 0.938 mono, Polish 0.886; reranking adds 0.025 |
| [CAISA (SemEval-2025)](https://aclanthology.org/2025.semeval-1.183/) | Post-filtering of retrieved claims | Llama-3-8B-Instruct | Task languages | S@10 55.7% reported |
| [[SemEval-2025 Task 7]] overview | Shared task | Winner (PINGAN AI) undescribed | 8 train languages, Polish and Turkish test-only | Polish S@10 0.882 to 0.926 for top four teams |
| [[Multilingual vs Crosslingual Retrieval]] (Ramponi et al., EMNLP 2025) | LLM reranker of top 30 | RankGPT; backbone LLM not named in the paper | 47 languages, no Polish breakdown | MRR@10 0.8042 multilingual, 0.6140 crosslingual with multilingual-e5-large |
| [[AMC-16K]] (Vykopal et al., Findings EMNLP 2025) | Pairwise relevance classifier | Mistral Large 123B, Command R+ 104B, Qwen2.5 72B and 7B, Llama3.1 70B and 8B, Mistral 7B | 20 languages incl. 400 Polish pairs | Best macro F1 82.46 mono, 80.54 cross (Mistral Large, few-shot); 70B+ significantly better |
| [[Language and Retrieval Bias]] (EACL 2026) | Relevance judge under instruction language | Qwen3 8B and 14B, Llama 3.1 8B and 70B, Gemma 3 12B and 27B | 20 languages | Slavic languages gain about 2.5 to 3.5 macro F1 from target-language prompts; Gemma 3 27B gains in every strategy |
| [[Generative-AI Claim Retrieval]] (Vykopal et al., 2025) | LLM filter of top 50 | Nine LLMs, Mistral Large best; Llama 3.3 70B in the tool | 10 languages incl. Polish | Filtering lowers S@10 0.76 to 0.70; true negative rate 90.23% |
| [[MultiClaimNet]] (Findings EMNLP 2025) | Claim-similarity labeller for clusters | GPT-4, Phi-3 14B, Falcon 40B, unanimous vote | 78 languages | 77 to 80% pairwise agreement; no human validation reported |
| [[CheckThat 2022 Task 2]] (RIET Lab) | Trained reranker | GPT-Neo | English | MAP@5 0.956 |
| [[Qwen3 Embedding]] | LLM embedder and reranker | Qwen3-Embedding-8B, Qwen3-Reranker-8B | Multilingual, no per-language table | Reranker 72.94 vs bge-reranker-v2-m3 58.36 on MMTEB retrieval |
| [[polish-reranker-roberta-v3]] | Polish cross-encoder vs LLM reranker | Qwen3-Reranker-8B as comparison | Polish (PIRB) | Polish model ahead on 18 of 41 tasks at about 5% of the parameters |
| [[Simulated Ignorance Fails]] (IJCAI 2026) | Cutoff probe | Nine models, cutoffs April 2024 to January 2025 | English | Prompted cutoff closes 48% of the gap |
| [[All Leaks Count]] (Findings EMNLP 2026) | Claim-level leakage audit | Qwen3.5-35B, Kimi-K2.5, Claude Sonnet 4 | English | Date-filtered RAG raises leakage 2.5 to 4.7 times |
| [[Temporal Leakage in Date-Filtered Web Retrieval]] (ACL 2026) | Leakage judge | gpt-oss-120b (same model as forecaster) | English | Quadratic weighted kappa 0.85 with humans on 134 documents |
| [Verga et al., 2024 (PoLL)](https://arxiv.org/abs/2404.18796) | Judge panel | Command R, Haiku, GPT-3.5 vs GPT-4 | English | Kappa with humans 0.763 vs 0.627 (NQ), max voting |
| [Balog et al., SIGIR 2025](https://arxiv.org/abs/2503.19092) | LLM relevance judge vs rankers | LLM judges and LLM rankers on TREC DL 2019/2020 | English | Significant judge bias towards LLM-based rankers |

## Proposed model set

| Role | Model | Family / owner | Size, VRAM (bf16 weights) | Stated cutoff | Open data | Polish | Licence | Why |
|---|---|---|---|---|---|---|---|---|
| Retriever (keep) | Qwen3-Embedding-8B | Qwen / Alibaba | 8B, about 16 GB, 1 GPU | None stated | No | Listed | Apache 2.0 | Strongest MMTEB embedder; "cutoff unknown" stratum |
| Reranker 1 (keep) | Qwen3-Reranker-8B | Qwen / Alibaba | 8B, about 16 GB | None stated | No | Listed | Apache 2.0 | Continuity with the plan; pointwise yes/no scoring |
| Reranker 2 | Gemma 3 27B-it | Gemma / Google | 27B, about 54 GB, one 80 GB GPU | August 2024 | No | Over 140 languages | Gemma terms | Stated cutoff inside the query period; used as PFCR judge in [[Language and Retrieval Bias]] |
| Reranker 3 (auditable) | Apertus-70B-Instruct-2509, plus Apertus-8B for the size axis | Apertus / Swiss AI | 71B, about 142 GB, two 80 GB GPUs; 8B about 16 GB | March 2024 (technical report) | Yes, reconstruction scripts | Polish among FineWeb-2 high-resource languages | Apache 2.0 | Pretraining corpus can be searched for each gold fact-check; Goldfish loss suppresses verbatim recall, so treat it as a low-memorisation contrast |
| Reranker 4 (auditable, English slice) | Olmo 3 32B | Olmo / Ai2 | 32B, about 64 GB, one 80 GB GPU | December 2024 (card) | Yes, Dolma 3 | English only | Apache 2.0 | Second open-data cutoff; English anchor only |
| Reranker 5 (Polish) | Bielik-11B-v3.0-Instruct | Bielik / SpeakLeash (Mistral 7B v0.2 base) | 11B, about 22 GB | None stated | No | Specialised | Apache 2.0 | Polish-specialised LLM against [[polish-reranker-roberta-v3]] |
| Reranker 6 (cutoff control) | Llama-3.3-70B-Instruct | Llama / Meta | 70B, about 140 GB, two GPUs | December 2023 | No | Not listed | Llama 3.3 Community | Earliest stated cutoff; widest pre/post split; English and Polish with the language caveat |
| Optional ceiling | One dated API snapshot | Closed vendor | n/a | Vendor page at run time | No | n/a | API terms | Only if MultiClaim terms allow; never in RQ5 headline |
| Judge 1 | gpt-oss-120b | OpenAI open weights | 117B total, 5.1B active; one 80 GB GPU (card) | Not on card | No | Not on card | Apache 2.0 | Disjoint family; precedent as leakage judge |
| Judge 2 | Command A (03-2025) | Cohere | 111B, about 222 GB, or 8-bit on two GPUs | Not on card | No | Listed (23 languages) | CC-BY-NC | Disjoint family; predecessor in [[AMC-16K]] |
| Judge 3 | Mistral-Large-Instruct-2411 | Mistral | 123B, about 246 GB, or 8-bit on two GPUs | Not on card | No | Listed | Mistral Research License | Best [[AMC-16K]] judge family; shares ancestry with Bielik, so Bielik rows also get a leave-Mistral-out score |
| Human arbiter | Two annotators | n/a | n/a | n/a | n/a | Native Polish speaker required | n/a | 200 Polish and 200 English sibling judgments, drift sample, 50 failing queries |

- Judge protocol: binary relevance (sibling qrels) and three-way drift (same claim, variant, updated narrative); each judge labels independently with the same released prompt; label = majority of three; ties impossible for binary, drift ties go to humans.
- Agreement weighting: weight each judge by its Cohen's kappa against [[AMC-16K]] Polish and English gold labels; report majority and weighted labels, keep majority as primary.
- Reporting: Fleiss' kappa across the three judges; Cohen's kappa of majority label vs human per language; per-judge macro F1 on [[AMC-16K]] Polish pairs; precision on same-topic negatives.
- Failure coding of the 50 queries stays human (two annotators, Cohen's kappa); LLMs may pre-sort but do not assign codes.

## Experimental controls

- Pin every model by Hugging Face repository and commit hash; record vLLM or Transformers version, dtype, quantisation, GPU type.
- Temperature 0, fixed seed, greedy decoding; given the run-to-run swings reported by Atil et al., rerun a 5% sample three times and report label flip rate.
- Release every prompt, few-shot example list and parsing rule; English instruction plus task description as default, target-language variant as sensitivity ([[Language and Retrieval Bias]]).
- Cache every request and response keyed by model hash, prompt hash and item id; results tables are rebuilt from the cache.
- Same first-stage candidates (top 30 to 50) for every reranker, so rerankers differ only in the model; report the embedder alone next to each reranked row ([[Qwen3 Embedding]]).
- Randomise candidate order for listwise rerankers and judges; for pairwise prompts score both orders.
- No API call carries post text unless the MultiClaim terms are confirmed to allow it; API rows carry the snapshot date.

## Changes to the plan

- Systems, "LLM scale" line in [[2026-10-27-temporal-retrieval-eval]]: replace "Qwen3-Embedding-8B and a Qwen3 reranker" with "Qwen3-Embedding-8B as retriever; rerankers Qwen3-Reranker-8B, Gemma 3 27B, Apertus 70B (and 8B), Llama 3.3 70B, Bielik 11B v3 on Polish, Olmo 3 32B on English", all over one shared candidate list.
- RQ5 wording: "Do LLM rerankers gain more on queries whose gold fact-check predates the model's cutoff, and does that gain track each model's own cutoff and measured exposure?"
- RQ5 design: per model $m$ with stated cutoff $K(m)$, stratify queries by gold fact-check date $t_f < K(m)$ (exposed) vs $t_f > K(m)$ (unexposed); estimate the reranker gain over the shared first stage in each stratum.
- RQ5 control: difference-in-differences against [[bge-reranker-v2-m3]] and [[polish-reranker-roberta-v3]] on the same strata, which absorbs calendar-time difficulty drift.
- RQ5 identification: models with different cutoffs (December 2023, March 2024, August 2024, December 2024) split the same queries differently; a gain jump at each model's own cutoff, not at a common date, is the leakage signature ([[Simulated Ignorance Fails]]).
- RQ5 exposure: for Apertus and Olmo 3, search the released pretraining data for each gold fact-check URL and long n-grams of its claim; per-query exposure replaces date strata for those models.
- RQ5 Qwen3 and Bielik: report as "cutoff unknown", not in the cutoff regression.
- Protocols, cluster-expanded line: "LLM-proposed" becomes "three-family judge panel, disjoint from evaluated systems, human-validated"; every system also reported on fact-checker-only qrels.
- Gap decomposition: narrative drift judged by the same panel; report Fleiss' and Cohen's kappa.
- Main risks and [[Risk register]]: add "single-family LLM dependence" with this note as mitigation; Deliverables: add released prompts, model hashes and the response cache index.
- Language scope: LLM rerankers stay on Polish and English ([[Language scope]]); judges run on all languages only after per-language validation.

## References

- Qwen3 blog (languages, licence, no cutoff): https://qwenlm.github.io/blog/qwen3/
- Qwen3 Embedding report: https://arxiv.org/abs/2506.05176
- Gemma 3 model card (cutoff August 2024): https://ai.google.dev/gemma/docs/core/model_card_3 ; https://huggingface.co/google/gemma-3-27b-it
- Apertus report (cutoff March 2024, Goldfish loss, robots.txt with hindsight): https://arxiv.org/abs/2509.14233 ; card: https://huggingface.co/swiss-ai/Apertus-70B-Instruct-2509
- Olmo 3 32B card (cutoff December 2024, English): https://huggingface.co/allenai/Olmo-3-1125-32B
- Llama 3.3 70B card (cutoff December 2023, languages): https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct
- Bielik 11B v3: https://huggingface.co/speakleash/Bielik-11B-v3.0-Instruct ; https://arxiv.org/abs/2601.11579
- PLLuM family: https://arxiv.org/abs/2511.03823
- gpt-oss-120b: https://huggingface.co/openai/gpt-oss-120b
- Command A: https://huggingface.co/CohereLabs/c4ai-command-a-03-2025
- Mistral Large 2411: https://huggingface.co/mistralai/Mistral-Large-Instruct-2411
- Ramponi et al. 2025: https://aclanthology.org/2025.emnlp-main.1480/
- SemEval-2025 Task 7: https://aclanthology.org/2025.semeval-1.323/ ; TIFIN India: https://aclanthology.org/2025.semeval-1.299/ ; CAISA: https://aclanthology.org/2025.semeval-1.183/
- AMC-16K: https://aclanthology.org/2025.findings-emnlp.852/ ; Language and Retrieval Bias: https://aclanthology.org/2026.eacl-long.240/ ; Generative-AI claim retrieval: https://arxiv.org/abs/2504.20668
- Cheng et al. 2024, Dated Data: https://arxiv.org/abs/2403.12958
- Simulated Ignorance Fails: https://ijcai.org/proceedings/2026/650 ; All Leaks Count: https://aclanthology.org/2026.findings-emnlp.1690/ ; date-filtered retrieval: https://aclanthology.org/2026.acl-short.65/
- TripleFact: https://aclanthology.org/2025.acl-long.431/ ; Chen, Huang, Dhingra: https://arxiv.org/abs/2410.14651
- Panickssery et al. 2024: https://proceedings.neurips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html
- Verga et al. 2024, PoLL: https://arxiv.org/abs/2404.18796
- Self-preference in rubric evaluation: https://arxiv.org/abs/2604.06996
- Balog, Metzler, Qin, SIGIR 2025: https://arxiv.org/abs/2503.19092
- Clarke and Dietz: https://arxiv.org/abs/2412.17156
- Chen, Zaharia, Zou: https://arxiv.org/abs/2307.09009 ; Atil et al.: https://arxiv.org/abs/2408.04667
