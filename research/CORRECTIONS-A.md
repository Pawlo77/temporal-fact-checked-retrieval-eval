# CORRECTIONS-A

Errors and unsupported claims in `knowledge/handbook/Enhanced topic research.md`, part A (claim-retrieval literature). Checked against primary sources on 2026-10-27; per-paper evidence is in the notes in this folder. Line numbers refer to the note as read on 2026-10-27.

## Errors and unsupported claims

### 1. SemEval-2025 Task 7: weakest languages (line 59)

- Quote: "Polish and Turkish were the weakest languages for most teams."
- Problem: overstated. The overview says the two unseen languages "show a generally worse performance" than training languages, but Table 8 (columns: avg eng fra deu por spa tha msa ara tur pol) shows English as low or lower for top teams: PINGAN AI eng 0.9160, pol 0.9260, tur 0.9480; TIFIN India eng 0.8800, pol 0.8860, tur 0.9040. Polish is the lowest for PALI (0.8880) and RACAI (0.8820). Turkish is not the lowest for any of the top four.
- Fix: "The overview reports that the two unseen languages (Polish, Turkish) score generally lower than training languages; in Table 8 Polish is among the lowest-scoring languages for top teams, together with English."

### 2. SemEval-2025 Task 7: attributing methods to PINGAN AI (line 59)

- Quote: "SemEval-2025 Task 7 top systems: ensembles of multilingual embedders plus per-language fine-tuned rerankers and LLM reranking (PINGAN AI first ...)"
- Problem: PINGAN AI submitted no system paper (no reference in Tables 8/9, absent from Table 7), so its method is unknown. Per-language fine-tuned rerankers are QUST_NLP (rank 5 mono). LLM reranking of the top 50 plus RRF is TIFIN India (rank 3 mono). RACAI (rank 4 mono, 3 cross) uses a single fine-tuned BGE-Multilingual-Gemma2 embedder with no reranking.
- Fix: "Top-ranked PINGAN AI (mono avg S@10 0.9601, cross 0.85875) published no system description. Described top systems use translation plus fine-tuned embedders with hard negatives (TIFIN India, fact check AI), LLM reranking with RRF (TIFIN India), per-language fine-tuned reranker ensembles (QUST_NLP), or a single fine-tuned LLM-based embedder (RACAI)."

### 3. MultiClaim pool size (line 76; also line 43)

- Quote (line 76): "a causal pool is smaller, which raises scores (MultiClaim itself shows performance falls as pool size grows)"
- Problem: what was read does not support this. MultiClaim's pool-size experiment adds random fact-checks to 100 pairs (pool 100 to 2,100). Figure 4 plots relative S@10 between BM25 and TEMs, and the finding is that BM25 gets relatively better with larger pools. An absolute decline is not stated in the text read. Section 7 attributes lower COVID-19 scores to "the sheer amount" of similar fact-checks, which is related but not the same claim.
- Fix: "MultiClaim varied pool size by adding random fact-checks (100 to 2,100) and found the BM25-vs-TEM gap depends on pool size; we expect absolute scores to rise in smaller pools and test this with the size-matched control."

### 4. Pool-size control described as unprecedented (line 43)

- Quote: "with a pool-size-matched control that no prior PFCR evaluation has used"
- Problem: MultiClaim already ran a pool-size control (random-addition sweep).
- Fix: "with a per-query pool-size-matched control (MultiClaim varied pool size globally with random fact-checks; no prior PFCR work matched pool size to a time-restricted pool)."

### 5. Chronological PFCR splits already exist (lines 66, 79, 43)

- Quotes: line 66 lists chronological splits only for rumour detection (Mu et al.); line 79 "Training-time leakage for fine-tuned PFCR models (random vs chronological training data), absent from SemEval system papers."
- Problem: Shaar et al., Findings NAACL 2022 ("The Role of Context in Detecting Previously Fact-Checked Claims") already compared Debate-Level Chrono, Semi-Chrono, Debate-Level Random and Sentence-Level Random splits for PFCR (PolitiFact debates). Reranker MAP was 0.429 (chrono) vs 0.590 (debate random) vs 0.602 (sentence random). It called the chronological split "a more realistic scenario". No date-restricted verified-claim pool is described.
- Fix: add to "What already exists": "Chronological train/test splits for PFCR: Shaar et al., Findings NAACL 2022 (PolitiFact debates; MAP 0.602 random to 0.429 chronological); training split only, no date-restricted index, no answerability or pool-size separation." Reword line 79 to "Training-time leakage for multilingual social-media PFCR (MultiClaim/SemEval), extending the debate-level chronological split of Shaar et al. 2022."

### 6. CheckThat! 2021 split wording and scope (line 54)

- Quote: "CheckThat! 2020-2022 Task 2 (verified claim retrieval, English tweets vs Snopes; Arabic): random 70/15/15 splits for English in 2021; no causal index constraint."
- Problem: the 2021 overview gives a 70/15/15 split for English but says "randomly" only for Arabic (512/85/261). Both 2021 and 2022 also had Subtask 2B (political debates vs PolitiFact, English), which the line omits. The 2022 edition added a new test set (English 209 tweets) on top of the 2021 data. CheckThat! 2020 was not verified.
- Fix: "CheckThat! 2021-2022 Task 2: 2A tweets (English vs 13,835 Snopes claims; Arabic) and 2B debates (English vs PolitiFact); English 2A split 70/15/15 in 2021 (999/200/202) with a new 209-tweet test in 2022; no date restriction of the verified-claim pool described."

### 7. Prior Polish PFCR evidence incomplete (line 81)

- Quote: "prior Polish PFCR evidence is the 500-post SemEval test slice and MultiClaim per-language tables."
- Problem: misses AMC-16K (Vykopal et al., Findings EMNLP 2025). It has 400 human-annotated Polish monolingual pairs plus crosslingual pol-hbs, ces-pol and hun-pol pairs, and reports lower LLM performance for Polish and other Slavic languages. Ramponi et al. 2025 also includes Polish among its 47 languages.
- Fix: "Prior Polish PFCR evidence: SemEval-2025 test (500 posts, 564 pairs; per-team Polish S@10 in Table 8), MultiClaim v1 tables (6,912 fact-checks, 453 posts), AMC-16K Polish annotations and LLM results (Vykopal et al. 2025), and Polish as one of 47 languages in Ramponi et al. 2025."

### 8. Polish fact-check sources (line 88)

- Quote: "Polish sources with at least 50 fact-checks visible in Table 6 include demagog.org.pl 4,292, oko.press 1,872, sprawdzam.afp.com 458; Konkret24 coverage to verify after access."
- Problem: correct numbers but incomplete. Table 6 also lists fakenews.pl (pol) 320. Konkret24 was not seen in the Table 6 rows read.
- Fix: append "fakenews.pl 320".

### 9. MultiClaim v2 relationship semantics (lines 36, 94)

- Quote (H3, line 36): "`backlink` pairs (fact-check body links the post) are post-first by construction; `claimreview_schema` and Meta-warning pairs contain more recurring claims"
- Problem: the v2 Zenodo record lists the relationship values but does not define `backlink`. It also does not say where Meta-warning pairs (the v1 collection route through Facebook/Instagram warnings) are mapped. Line 94's "added by text identity, not by a fact-checker" is an interpretation of "(for identical claims)".
- Fix: mark these as assumptions to confirm from the data or with the dataset authors. Ramponi et al. 2025 state that only claim_review and backlink existed in the original MultiClaim, which is consistent with but does not define them.

### 10. SemEval train/dev scope (line 58, minor)

- Quote: "train/dev from MultiClaim (8 monolingual languages)"
- Problem: correct for the monolingual track. Crosslingual train/dev covers 14 languages (52 combinations). The overview also states "All posts in MultiClaim were published before 2023", which makes the test (posts to March 2024) out-of-time relative to train.
- Fix: add both facts.

### 11. MultiClaim pair counts (line 56, minor)

- Quote: "31,305 pairs"
- Problem: correct, but the paper also gives 26,774 monolingual plus 4,212 crosslingual pairs, which sum to 30,986. Anyone deriving counts from the mono/cross split will not reach 31,305.
- Fix: footnote the discrepancy; recount after data access.

## Confirmed claims (no change)

- Line 53: Shaar et al. ACL 2020 task definition (Snopes, PolitiFact).
- Line 55: CheckThat! 2025 has no PFCR task. The 2026 tasks are scientific source retrieval, numerical/temporal claims and article generation.
- Line 56: MultiClaim counts 205,751 / 39 / 28,092 / 27 / 31,305. The post-newer vs post-older result 80.02 vs 80.04 monolingual S@10 for GTR-T5 and the "not able to measure" conclusion are correct. The paper adds that "at least few samples" have the verbatim problem.
- Line 57: 20 post-date quantiles, COVID-19 drop at the start of 2020, roughly 7x more valid pairs.
- Line 58: SemEval test posts to March 2024, claim pool to May 2024, Polish and Turkish unannounced.
- Line 59: PINGAN AI scores 0.9601 (mono avg) and 0.85875 (cross).
- Line 60: MultiClaim v2 435k / 89k / 105k, before April 2025, three relationship types.
- Lines 61-64: Ramponi 2025 (47 languages, LLM reranking best, similarity negatives, random stratified split), AMC-16K (16K pairs, 20 languages), Vykopal EACL 2026 (language and retrieval bias), and MultiClaimNet (85.3K / 30.9K / 78, timestamps and URLs).
- Lines 87, 89-91, 150, 156: record ids, SemEval Polish 500/8,796/564, Snopes 18,376, PolitiFact 9,029, 26,337 dated posts (1,755 undated), and access terms.
- Line 127: metric correlations, minimum 0.986.

## Search for prior causal-index PFCR evaluation

- Searched for PFCR or claim-matching work with a time-restricted fact-check pool, chronological evaluation or temporal leakage (queries on temporal split, chronological evaluation, fact-checks published before the post, leakage, streaming).
- Found two related papers, neither of which restricts the index by date as an evaluation protocol:
  - Shaar et al., Findings NAACL 2022: a chronological training split (item 5).
  - Vykopal et al., arXiv 2504.20668: date-range filtering as a natural-language retrieval criterion. Date range was the worst-performing filter, and this is not an evaluation protocol.
- MultiClaim's post-newer vs post-older test remains the closest in-dataset analysis.
- Conclusion: no prior PFCR paper found that evaluates with a causal, date-restricted index. The novelty claim on line 74 holds as far as this search reached, but it must cite Shaar 2022 and MultiClaim Section 4.2 as precedents.
