---
title: "SemEval-2025 Task 7"
aliases: ["SemEval-2025 Task 7: Multilingual and Crosslingual Fact-Checked Claim Retrieval"]
authors: ["Qiwei Peng", "Robert Moro", "Michal Gregor", "Ivan Srba", "Simon Ostermann", "Marian Simko", "Juraj Podroužek", "Matúš Mesarčík", "Jaroslav Kopčan", "Anders Søgaard"]
year: 2025
venue: "Proceedings of the 19th International Workshop on Semantic Evaluation (SemEval-2025), Vienna, pages 2498-2511"
arxiv: "2505.10740"
url: "https://aclanthology.org/2025.semeval-1.323/"
citekey: peng2025semeval
verified: 2026-10-27
theme: "[[Datasets and Benchmarks]]"
tags: [type/paper, theme/datasets, topic/shared-task, topic/multilingual, topic/polish, topic/benchmark, topic/temporal]
---
# SemEval-2025 Task 7

> [!info] TL;DR
> The shared task turns [[MultiClaim]] into a benchmark with a monolingual and a crosslingual track, scored by Success@10. Training data comes from MultiClaim (posts before 2023); the test set has newly collected posts up to March 2024, a pool extended to May 2024, and two unannounced languages, Polish and Turkish. 31 teams submitted; the best monolingual average was 0.9601 and the best crosslingual score 0.85875.

## Motivation

- PFCR work and shared tasks had covered English, Arabic and a few Indic languages ([[CheckThat 2022 Task 2]], [[Claim Matching Beyond English]]); most languages and all crosslingual settings were untested in a shared task.
- [[MultiClaim]] showed translation plus English models beat multilingual models; a shared task tests whether newer systems change that.
- Fact-checkers need to know whether a claim was already checked, possibly in another language.

## Method

We write a post as $q$, a fact-checked claim as $f$, the search pool as $P$ and gold set $G(q)$.

**Tracks.** Monolingual: $q$ and its gold $f$ share a language and $P$ holds only that language's claims. Crosslingual: $P$ is unrestricted and gold claims may be in other languages.

**Training and development.** MultiClaim languages with at least 500 pairs: 8 monolingual languages (Arabic, English, French, German, Malay, Portuguese, Spanish, Thai). The crosslingual track adds 6 post languages (14 in all, 52 combinations), plus a random 10% of monolingual pairs so language mismatch cannot be exploited. 3,351 pairs were added by transitivity: if posts $q_i$ and $q_j$ share a claim and $q_i$ links claim $f_k$, then $(q_j, f_k)$ is added.

Intuition: two posts making the same claim should share all the claim's fact-checks.

**Test.** New posts, "published until March 2024", collected the same way from more fact-checkers and also Telegram; the pool adds new claims "ranging until May 2024". Polish and Turkish appear only at test time. Up to 500 random posts per language.

**Metric.** Success@10, defined as in our glossary, from the top 10 submitted per post.

**Baselines.** BM25 and GTR-T5-Large on English translations; paraphrase-multilingual-MPNet and [[Multilingual E5]] Large on original text.

## Key numbers

- Monolingual winner PINGAN AI: average Success@10 0.9601 (English 0.9160, Polish 0.9260, Turkish 0.9480) vs E5-Large baseline 0.8589 and BM25 0.8123.
- Crosslingual winner PINGAN AI 0.85875 vs GTR-T5-Large baseline 0.70525; crosslingual scores are more than 10 points below monolingual for most systems.
- Polish test slice: 500 posts, 8,796 claims, 564 pairs; Polish Success@10 ranges from 0.8820 to 0.9260 among the top four teams, with baselines at 0.7980 (E5) and 0.7320 (BM25).
- Participation: 179 registered, 52 test submissions from 31 teams, 23 system papers.

## Experiments

- **Monolingual track:** described top systems translate to English and rerank the top 50 with an LLM fused by reciprocal rank (TIFIN India, see [[TIFIN India]]), fine-tune one multilingual LLM-based embedder (RACAI), or ensemble per-language fine-tuned rerankers (QUST_NLP). The two unseen languages score generally lower than training languages, though English is as low for several top teams.
- **Translation vs multilingual:** translate-to-English and original-language multilingual systems differ negligibly, unlike in [[MultiClaim]].
- **Crosslingual track:** the same pipelines carry over; reranking and voting help more here, while mixing original text with translations hurts.
- **Common recipe:** contrastive fine-tuning with in-batch negatives, then hard negatives, used by three of the five described top monolingual systems.

## Data

- Train+dev: 17,016 + 1,891 monolingual posts, 4,972 + 552 crosslingual posts, 153,743 claims.
- Test: 4,276 monolingual posts with 4,959 pairs over 260,880 claims; 4,000 crosslingual posts with 5,322 pairs over 272,447 claims.
- Crosslingual test: 11 claim languages, 14 post languages, 60 combinations; Polish posts link mostly to Polish (55) and English (14) claims.
- Zenodo record 14989176, restricted to research use.

> [!failure] Limitations
> - The test pool runs to May 2024 while test posts end in March 2024, and no date restriction of $P$ is described, so a post can be matched to a later claim.
> - Most crosslingual pairs involve English on one side.
> - About 15% of training links need image or video content.
> - The winner (PINGAN AI) published no system description, so the best method is unknown.
> - Unseen languages confound language with other effects: Polish and Turkish have no training data.

## Relation to our project

- The test set is already out-of-time relative to training, so we cannot claim temporal test posts as new; we cite it as the precedent ([[Research summary]]).
- The Polish test slice and per-team Polish scores are our main Polish source and reference numbers ([[Language scope analysis]]).
- Because the pool extends past the last post, re-evaluating with a causal pool $P(q) = \{f \in P : t_f < t_q\}$ is a direct test of our RQ1 ([[Proposed Task]]).
- Polish being unseen in training must be modelled in our Polish-English difference-in-differences ([[Enhanced topic research]]).

## Future work

- **Partly done:** transfer of techniques across tracks; [[Multilingual vs Crosslingual Retrieval]] (Ramponi et al., 2025) compares the two settings on MultiClaim v2.
- **Open:** comparing systems by compute cost, which the organisers say they did not do (searched 2026-10).
- **Open:** a time-respecting pool for the test posts (searched 2026-10).
