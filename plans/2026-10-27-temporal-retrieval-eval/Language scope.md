---
title: "Language scope"
type: plan-note
domain: vault
parent: "[[2026-10-27-temporal-retrieval-eval]]"
tags: [language-scope, power-analysis, study-design]
created: 2026-10-27
updated: 2026-10-27
related:
  - "[[Original Task]]"
  - "[[2026-10-27-temporal-retrieval-eval|Project plan]]"
  - "[[Topic research]]"
---
# Language scope

Question: is a Polish-vs-English contrast enough for a publishable causal evaluation of previously fact-checked claim retrieval (PFCR), or should the language set be broadened? Sources checked on 2026-10-27; dataset counts are the papers' published numbers, our own counts come only after data access.

## Recommendation

- Adopt option B: Polish stays the focus and headline, English the high-archive anchor, plus five languages chosen to span archive size: Spanish, German, Turkish, Czech, Slovak.
- Replace "Polish penalty is larger than English" as the only mechanism test with a dose-response test: the causal penalty as a function of archive density (log causal same-language pool size at post time, earlier-sibling count, post-to-debunk lag).
- Identify the mechanism mainly from within-language variation (the causal pool grows over time inside every language), with between-language spread as corroboration; two languages alone cannot separate "thin archive" from everything else that differs between Polish and English.
- Keep the brief's deliverables unchanged: the Polish-English difference-in-differences stays the central number, the 50-query manual analysis stays 25 Polish + 25 English.
- [[2026-10-27-temporal-retrieval-eval|Project plan]] adopts it as an additive robustness layer, gated only on MultiClaim v2 access, with Polish and English only as the fallback.

## Why two languages is thin

- A two-point contrast has zero degrees of freedom for a mechanism: any Polish-English difference is confounded with platform mix, topic mix, outlet practice (backlink vs ClaimReview), date distribution, OCR share and translation quality.
- Polish is not an extreme: MultiClaim v1 lists 6,912 Polish fact-checks, the same order as Turkish 6,676, Hindi 7,149, German 4,996 and French 4,355, so "thin national archive" is a claim about English (85,814), not about Polish specifically.
- English is a poor "control" on its own: its pool is the cross-lingual fallback for most languages (most crosslingual pairs in [[SemEval-2025 Task 7]] involve English), so it differs in kind, not only in size.
- A dose-response design turns the hypothesis into a testable prediction (penalty falls as archive density rises, within and across languages), which reviewers accept as mechanism evidence; a single difference only shows that two numbers differ.

## Why this is not the out-of-scope language-bias study

- [[Language and Retrieval Bias|Vykopal et al. (EACL 2026)]] study language bias as LLM detection performance that is better for high-resource languages, across 20 languages on [[AMC-16K]] with translated prompts, plus retrieval bias (popular claims retrieved disproportionately).
- Our outcome is a within-language protocol difference (random minus causal, same model, same language, same queries), which is a property of the archive's temporal coverage, not of model competence in a language.
- The explanatory variable is fact-check ecosystem density at query time, a per-query continuous covariate, not language identity or resource level.
- Rules that keep it out of scope: never rank languages by absolute Success@10; report only within-language deltas and slopes; no claims about which model handles which language better; language enters as a random effect, not as the finding.

## Evidence table

Counts from the papers. v1 = [[MultiClaim]] (Table 5 posts and fact-checks); v2 = monolingual pairs in the [[Multilingual vs Crosslingual Retrieval|Ramponi et al.]] MultiClaim v2 subset (post text only, languages with at least 200 posts, Table 4 diagonal); ST7 = [[SemEval-2025 Task 7]] monolingual test (Table 2).

| Language | v1 fact-checks | v1 posts | v2 subset mono pairs | ST7 test posts / pairs / pool claims | Main outlets in v1 (Table 6) |
|---|---|---|---|---|---|
| English | 85,814 | 7,307 | 19,341 | 500 / 574 / 145,287 | snopes 18,376, politifact 9,029 |
| Spanish | 14,082 | 7,319 | 7,470 | 500 / 576 / 25,440 | factual.afp 4,051, newtral 3,256 |
| Portuguese | 21,569 | 3,366 | 3,628 | 500 / 613 / 32,598 | sapo.pt 5,200, uol 3,908 |
| Arabic | 14,201 | 931 | 3,360 | 500 / 514 / 21,153 | misbar 9,027 |
| Turkish | 6,676 | 7 | 3,179 | 500 / 550 / 12,536 | teyit 3,289, malumatfurus 1,572 |
| French | 4,355 | 2,146 | 2,699 | 500 / 740 / 6,316 | factuel.afp 2,178 |
| Hindi | 7,149 | 833 | 2,470 | not in mono test | aajtak 2,493 |
| German | 4,996 | 932 | 2,381 | 500 / 549 / 7,485 | correctiv 1,783 |
| Polish | 6,912 | 453 | 1,309 | 500 / 564 / 8,796 | demagog 4,292, oko.press 1,872, sprawdzam.afp 458, fakenews.pl 320 |
| Russian | 2,715 | 28 | 454 | not in test | stopfake 1,307 |
| Slovak | 260 | 363 | 321 | not in test | fakty.afp 260 |
| Czech | 254 | 265 | 246 | not in test | napravoumiru.afp 255 |
| Ukrainian | 68 | 6 | below the 180-post cut | not in test | none listed |

- MultiClaim v2 totals (Zenodo): 435k fact-checks, 89k posts, 105k pairs, all published before April 2025; per-language fact-check counts for v2 are not public and must be computed after access.
- ST7 test posts were published until March 2024 and the test pool runs to May 2024; overlap of ST7 test posts with v2 is unknown and must be deduplicated by post id and text.
- v1 had dates for 26,337 of 28,092 posts; v2 date coverage is unknown.
- Konkret24 does not appear in the v1 list of sources with at least 50 fact-checks.
- Ukrainian has too few posts to enter; Russian is optional (moderate archive, few posts).

## Power table

Assumptions (stated, not measured): discordance d = 0.15 (share of queries whose hit flips between protocols); MDE at alpha 0.05 and 80% power = 2.80 × sqrt(d / n); answerable rate a under the strict causal protocol of 0.3 or 0.5; per-language n = max(v1 posts, v2 mono pairs / 1.1) plus ST7 test posts where present, an upper bound before date filtering and deduplication; English n for the DiD is a × 18,083. Computed with a script for this note.

| Language | n (v1/v2) | n pooled with ST7 | MDE all queries | MDE answerable a=0.3 | MDE answerable a=0.5 | MDE DiD vs English a=0.3 |
|---|---|---|---|---|---|---|
| English | 17,583 | 18,083 | 0.008 | 0.015 | 0.012 | n/a |
| Spanish | 7,319 | 7,819 | 0.013 | 0.023 | 0.018 | 0.027 |
| Portuguese | 3,366 | 3,866 | 0.019 | 0.034 | 0.026 | 0.037 |
| Arabic | 3,055 | 3,555 | 0.020 | 0.036 | 0.028 | 0.039 |
| Turkish | 2,890 | 3,390 | 0.020 | 0.037 | 0.029 | 0.040 |
| French | 2,454 | 2,954 | 0.022 | 0.040 | 0.031 | 0.043 |
| Hindi | 2,245 | 2,245 | 0.023 | 0.042 | 0.032 | 0.044 |
| German | 2,165 | 2,665 | 0.023 | 0.043 | 0.033 | 0.045 |
| Polish | 1,190 | 1,690 | 0.031 | 0.057 | 0.044 | 0.059 |
| Russian | 413 | 413 | 0.053 | 0.097 | 0.075 | 0.099 |
| Slovak | 363 | 363 | 0.057 | 0.104 | 0.080 | 0.105 |
| Czech | 265 | 265 | 0.067 | 0.122 | 0.094 | 0.123 |

- MDE columns use the v1/v2 n; pooling ST7 lowers them further.
- Polish with v2 is about 2.6 times the v1 count, so the earlier sketch (450 queries) was pessimistic if v2 is granted; the Polish DiD MDE is about 6 points of Success@10 on answerable queries at a = 0.3.

Between-language meta-regression of the per-language penalty on log10 v1 archive size (inverse-variance weights, between-language heterogeneity tau, t multiplier with k - 2 df, a = 0.3):

| Language set | k | sd of log10 archive | MDE slope per 10x archive, tau 0.02 | tau 0.04 |
|---|---|---|---|---|
| A: Polish, English | 2 | n/a | not estimable (0 df) | not estimable |
| B6: + Spanish, German, Turkish, Czech | 6 | 0.82 | 0.064 | 0.101 |
| B7: B6 + Slovak (recommended) | 7 | 0.92 | 0.050 | 0.077 |
| B8: Polish, English, Spanish, Portuguese, German, French, Turkish, Czech | 8 | 0.72 | 0.054 | 0.087 |
| C: all 12 languages above | 12 | 0.73 | 0.042 | 0.064 |

Within-language query-level slope of hit on log10 causal pool size (linear probability, p(1-p) = 0.2, sd of log10 pool size within language 0.2 or 0.4):

| Queries | MDE per 10x, sd 0.2 | sd 0.4 |
|---|---|---|
| 400 | 0.313 | 0.157 |
| 1,000 | 0.198 | 0.099 |
| 2,000 | 0.140 | 0.070 |
| 5,000 | 0.089 | 0.044 |
| 15,000 | 0.051 | 0.026 |

- Reading: Polish alone detects only a large within-language slope; pooling option B's roughly 34k queries in one mixed model gives a within-language MDE near 2-4 points per 10x pool growth, which is where the mechanism claim gets its power.
- The between-language slope is a corroboration test: with seven languages it detects only slopes of 5-8 points per 10x archive, so it must not be the headline.
- Re-state all MDEs with measured d, a and pool-size spread after the first run.

## Options matrix

| | A: Polish vs English | B: Polish focus + English + 5 spanning languages | C: all languages with enough queries, hierarchical model |
|---|---|---|---|
| Languages | pl, en | pl, en, es, de, tr, cs, sk | B + pt, fr, ar, hi, ru (12) |
| Mechanism test | DiD only, confounded | within-language dose-response + 7-point between-language slope | same, 12 points, tighter slope |
| Fits the brief | exactly | yes, as an additive layer; Polish stays the headline | dilutes the Polish focus; reads as a multilingual benchmark |
| Language-bias risk | low | low with the reporting rules above | higher: 12 per-language bars invite cross-language ranking |
| Reranking load (cross-encoder, top-100, 5 protocols; en and es subsampled to 3,000) | 4,690 queries, about 2.3M pairs | 14,373 queries, about 7.2M pairs (about 3.1x A) | about 21k-25k queries, roughly 5x A |
| Dense and BM25 load | negligible extra | negligible: encode the pool once, apply time masks at search time | negligible |
| LLM reranker (RQ5) | pl, en | keep pl, en only | keep pl, en only |
| Annotation | 50 queries + 200 pl + 200 en sibling judgments | unchanged; other languages get automatic covariates and LLM sibling judgments only | same as B, more unvalidated LLM labels |
| Data work | v1 + ST7 for two languages | per-language archive and sibling counts from v2 and [[MultiClaimNet]]; timestamp checks for 5 more languages (50 dates each) | 10 more languages of timestamp checks |
| Reviewer reaction | "n = 2 languages, Polish could differ for any reason" | "mechanism tested with variation in archive density; Polish is a well-powered case study" | "broad but shallow; why Polish in the title?" |
| Novelty | protocol novel, language claim weak | protocol plus a mechanism claim nobody has tested for PFCR | same as B, small marginal gain |

## Design details for option B

- Primary hypotheses (pre-registered): H-PL, the Polish-English DiD of the causal penalty, one test per system family with Holm across systems; H-DOSE, the coefficient of log causal pool size in a mixed-effects logistic model of per-query hit, one test.
- Model for H-DOSE: hit ~ protocol × log10(causal same-language pool size) + protocol × log(1 + earlier-sibling count) + signed log lag + calendar-time spline + (1 | language) + (1 | system) + (1 | query); calendar time is controlled because pool size grows with time and topics shift (COVID-19 period).
- Report causal pool size both same-language and cross-lingual (all earlier fact-checks), because multilingual retrievers can use foreign-language earlier debunks.
- Mediation reading: archive density → earlier-sibling availability → answerability → penalty; the gap decomposition already measures the last two steps.
- Exploratory: per-language penalties with BH-FDR across language × system cells, shown as a forest plot of deltas only.
- Inclusion rule per language: at least 250 dated queries and at least 100 strict-causal answerable queries; below that the language is reported descriptively and enters only the pooled model.
- Czech and Slovak are thin-archive anchors from a single AFP outlet each; keep them as separate points and run a leave-one-language-out check on the slope.
- 50-query manual analysis: unchanged (25 pl, 25 en), so the brief's qualitative deliverable and kappa are not diluted.
- Workstreams: the single plan in [[2026-10-27-temporal-retrieval-eval|Project plan]] runs sparse and dense baselines (W2) on all seven languages, since encoding and masking are cheap; cross-encoders (W3) on all seven, the LLM reranker and the full additive gap chain (W4) on Polish and English; the mixed model is fitted on the one shared results table.

## Venue fit and novelty

- A: workshop paper (FEVER, NLP4PI) or a Findings short; an ARR long submission risks "limited generalization" and "confounded comparison" reviews.
- B: ARR long (Findings or main) as evaluation methodology with a mechanism claim; SIGIR short or resource track; the time-masked split for seven languages is a stronger resource and a natural basis for a CLEF temporal PFCR task proposal.
- C: same venues as B with a marginal gain in generality, at the cost of the Polish framing and higher overlap with multilingual analyses from the dataset authors' group.
- No date-restricted-index PFCR evaluation was found in searches on 2026-10-27; the one chronological PFCR evaluation, [[Role of Context in PFCR|Shaar et al. 2022]] ([[Role of Context in PFCR]]), used a chronological split without a date-restricted index; [[CheckThat 2026|CheckThat! 2026]] has no PFCR task; the novelty sits in the protocol and the dose-response, not in the number of languages.

## Risks

- v2 access: without v2, Polish falls back to 453 v1 posts plus 500 ST7 test posts and the slope loses Turkish (7 v1 posts), so B degrades towards A; request v2 now.
- Archive size measured from the dataset is the dataset's coverage, not the true national ecosystem (collection is via Google Fact Check Explorer and selected outlets); state it as "indexed archive density".
- Language identification in v2 is automatic (Google Translate in the release, four detectors in [[Multilingual vs Crosslingual Retrieval|Ramponi et al.]]); per-language counts carry noise.
- Single-outlet languages (cs, sk) confound archive size with one outlet's practice; leave-one-language-out and outlet-level random effects (aggregate only, no ranked outlet list) mitigate it.
- Scope perception: a reviewer or the supervisor may still read seven languages as a language study; the reporting rules above and a one-line statement distinguishing it from [[Language and Retrieval Bias|Vykopal et al. (EACL 2026)]] address it.
- Compute: reranking roughly triples; subsample English and Spanish queries and cap top-k at 100.

## References

- [[MultiClaim]] ([[MultiClaim|Pikuliak et al.]], EMNLP 2023), Tables 5-7: https://arxiv.org/html/2305.07991v2 ; https://aclanthology.org/2023.emnlp-main.1027/
- MultiClaim v2 Zenodo record: https://zenodo.org/records/15413169
- [[SemEval-2025 Task 7]] overview ([[SemEval-2025 Task 7|Peng et al.]]), Tables 2-4: https://aclanthology.org/2025.semeval-1.323.pdf
- [[Multilingual vs Crosslingual Retrieval|Ramponi et al. 2025]], Multilingual vs Crosslingual Retrieval of Fact-Checked Claims, Table 1 and Table 4: https://arxiv.org/html/2505.22118v2 ; https://aclanthology.org/2025.emnlp-main.1480/
- [[Language and Retrieval Bias|Vykopal et al. 2026]], Investigating Language and Retrieval Bias in Multilingual PFCD, EACL: https://aclanthology.org/2026.eacl-long.240/ ; https://arxiv.org/abs/2509.25138
- [[MultiClaimNet]]: https://arxiv.org/abs/2503.22280
- [[CheckThat 2026|CheckThat! 2026]] lab overview: https://arxiv.org/abs/2602.09516
