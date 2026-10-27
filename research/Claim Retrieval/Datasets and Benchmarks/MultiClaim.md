---
title: "MultiClaim"
aliases: ["Multilingual Previously Fact-Checked Claim Retrieval"]
authors: ["Matúš Pikuliak", "Ivan Srba", "Robert Moro", "Timo Hromadka", "Timotej Smoleň", "Martin Melišek", "Ivan Vykopal", "Jakub Simko", "Juraj Podroužek", "Maria Bielikova"]
year: 2023
venue: "Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP 2023), Singapore, pages 16477-16500"
arxiv: "2305.07991"
doi: "10.18653/v1/2023.emnlp-main.1027"
url: "https://aclanthology.org/2023.emnlp-main.1027/"
citekey: pikuliak2023multilingual
verified: 2026-10-27
theme: "[[Datasets and Benchmarks]]"
tags: [type/paper, theme/datasets, topic/multilingual, topic/benchmark, topic/bm25, topic/dense-retrieval, topic/temporal, topic/polish]
---
# MultiClaim

> [!info] TL;DR
> MultiClaim is the first large multilingual PFCR dataset: 28,092 social media posts in 27 languages, 205,751 fact-checks in 39 languages and 31,305 post-fact-check pairs linked by fact-checkers, including crosslingual pairs. On it, English text-embedding models applied to machine translations beat multilingual models, and BM25 stays competitive in some languages. The paper also runs three time-related checks (post-date quantiles, a post-newer vs post-older leak test, a pool-size sweep) and finds no measurable leak.

## Motivation

- Earlier PFCR data was English or Arabic, or covered a few Indic languages with about 250 positive pairs ([[Claim Matching Beyond English]]); no crosslingual PFCR data existed.
- Shared-task data came from tweets cited in fact-checks with manual cleaning ([[CheckThat 2021 Task 2]]); large English data such as [[CrowdChecked]] was noisy.
- Fact-checkers in low-resource languages most need search over existing fact-checks, so the gap is practical, not only academic.

## Method

We write the post as $q$, a fact-check as $f$ (represented by its short claim only) and the pool as $P$; the paper uses "input claim" and "fact-checked claim".

**Collection.** Fact-checks come mostly from Google Fact Check Explorer plus manually added sources such as Snopes (142 organisations). Pairs come from two routes, both set by fact-checkers: Facebook, Instagram and Twitter links in the ClaimReview "reviewed item" field, and Facebook/Instagram URLs in fact-check bodies confirmed through the platforms' fact-check warnings. Posts carry text, OCR of images, date, platform and the Meta rating; texts are machine-translated to English and language-identified.

**Evaluation.** Each post ranks the whole pool; the metric is Success@10 with Agresti-Coull intervals. Monolingual pairs search only fact-checks in the post's language; crosslingual pairs search the full pool; scores are averaged over languages with more than 100 pairs.

**Same language bias (SLB).** The share of top-10 fact-checks in the post's language when the full pool is searched.

Intuition: a high SLB retriever ignores fact-checks in other languages, which makes monolingual scores easy and crosslingual retrieval impossible.

**Supervised training.** GTR-T5 and multilingual MPNet are fine-tuned with positive pairs and random negatives on a random 80:10:10 split of posts.

## Key numbers

- Best method: GTR-T5-Large on English translations, Success@10 0.83 monolingual and 0.56 crosslingual; BM25 on original text 0.62 and 0.06, BM25 on translations 0.78 and 0.39.
- Translation helps: the best English-version method beats the best original-version method by 14% monolingual and 35% crosslingual Success@10.
- Leak test: posts newer vs older than their fact-check score "80.02 vs 80.04" monolingual Success@10 for GTR-T5; the authors could not measure a leak.
- Post-hoc annotation of 87 test posts found 719 valid pairs where the data had 96, about 7 times more; 336 were crosslingual with a non-English fact-check.
- Fine-tuning raises multilingual MPNet from 0.63 to 0.76 monolingual and 0.23 to 0.42 crosslingual Success@10 on the random test split; GTR-T5 gains only 0.82 to 0.84.

## Experiments

- **Unsupervised comparison:** 15 English and 5 multilingual embedding models plus BM25; GTR is Pareto-optimal, model size barely correlates with score (Pearson 0.03), and monolingual and crosslingual scores correlate at 0.98.
- **Pool size:** 100 pairs in each of 7 large languages, pool grown from 100 to 2,100 by adding random fact-checks; BM25 on original text gains on MPNet as the pool grows, read as a higher false positive rate of the embedding model.
- **Language filter:** without it, BM25 on original text would beat MPNet 51.9 vs 38.5 Success@10 only because of its implicit language filter.
- **Time:** 26,337 dated posts in 20 quantiles show a drop at the start of 2020; COVID-related posts score 0.72 vs 0.83 otherwise (GTR-T5, monolingual), which the authors attribute to many near-duplicate COVID fact-checks rather than domain shift. A GTR-minus-BM25 trend over time is negative but not significant (Pearson -0.33, P = 0.17).
- **Other splits:** "Missing context" and "Altered photo/video" ratings score lower; performance peaks for posts around 500 characters; Twitter scores best.
- **Post-hoc annotation:** 3,390 predictions from 6 methods judged by 3 authors; true Success@10 is higher than measured, while recall from the data is inflated and favours BM25.

## Data

- MultiClaim v1: 205,751 fact-checks (39 languages), 28,092 posts (27 languages), 31,305 pairs; the paper also gives 26,774 monolingual and 4,212 crosslingual pairs, which sum to 30,986, a gap it does not explain.
- Polish slice: 6,912 fact-checks and 453 posts; Polish sources include demagog.org.pl (4,292), oko.press (1,872), sprawdzam.afp.com (458) and fakenews.pl (320).
- Noise audit: 87 of 100 random pairs correct; the other 13 need the image or video.

> [!failure] Limitations
> - About 13% of posts hold the claim only visually.
> - Labels are far from exhaustive, especially crosslingual non-English pairs, so measured scores understate true ones.
> - Selection bias: some fact-checks quote their post verbatim ("at least few samples"), and posts are biased toward what platforms already detect.
> - Crosslingual pairs are mostly Asian-language posts with English fact-checks.
> - Every post searches the full pool regardless of dates; the leak test compares two subsets under that same pool.
> - Supervised results use a random post split and may overfit the period covered.

## Relation to our project

- Our main corpus; the per-instance timestamps make a causal pool $P(q) = \{f \in P : t_f < t_q\}$ possible ([[2026-10-27-temporal-retrieval-eval|Project plan]]).
- Its three temporal analyses are precedents we must cite: none removes future fact-checks from the pool or separates answerability from ranking, which is our RQ1 ([[Datasets and Benchmarks]]).
- The random pool-size sweep is not size-matched per query; our matched control extends it ([[Topic research]]).
- The random 80:10:10 split is the training-leakage baseline we contrast with chronological training.
- Polish (453 posts) is thin here, which is why we pool with [[SemEval-2025 Task 7]] and v2 ([[MultiClaim Zenodo Records]], [[Language scope]]).

## Future work

- **Done:** crosslingual transfer at scale; [[SemEval-2025 Task 7]] (Peng et al., 2025) ran a crosslingual track on this data, and [[Multilingual vs Crosslingual Retrieval]] compared both settings.
- **Done:** hidden positive pairs; [[AMC-16K]] (Vykopal et al., 2025) annotated 16,000 retrieved pairs.
- **Done:** harder negatives for fine-tuning; most top SemEval-2025 systems used hard negatives ([[SemEval-2025 Task 7]]).
- **Open:** evaluation with a date-restricted pool per post and answerable-only scoring (searched 2026-10).
