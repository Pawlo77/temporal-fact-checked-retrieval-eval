# 2025 - Peng - SemEval-2025 Task 7 overview

## Citation

- Authors: Qiwei Peng, Robert Moro, Michal Gregor, Ivan Srba, Simon Ostermann, Marian Simko, Juraj Podroužek
- Title: SemEval-2025 Task 7: Multilingual and Crosslingual Fact-Checked Claim Retrieval
- Venue: Proceedings of the 19th International Workshop on Semantic Evaluation (SemEval-2025), Vienna
- Year: 2025
- URL: https://aclanthology.org/2025.semeval-1.323/ (PDF read); arXiv 2505.10740
- Data: https://zenodo.org/records/14989176 (published 7 Mar 2025, restricted)
- Verified on: 2026-10-27

## What it does

- Two tracks: monolingual (post and claims in the same language; pool restricted per language) and crosslingual; systems return top 10 per post; metric Success@10.
- Train/dev: subset of MultiClaim, languages with at least 500 pairs: 8 monolingual languages (Arabic, English, French, German, Malay, Portuguese, Spanish, Thai) and 14 languages / 52 combinations crosslingual.
- Test: newly collected posts "published until March 2024"; the claim pool contains the train/dev claims plus newly collected ones "ranging until May 2024"; collection extended to more fact-checkers and Telegram.
- Polish and Turkish added as unannounced monolingual test languages.
- States "All posts in MultiClaim were published before 2023."
- Zenodo record: train_dev_set, test_set, evaluation and loading scripts, baseline predictions (BM25, GTR-T5-Large, Paraphrase-Multilingual-MPNet-Base-v2, Multilingual-E5), README; same research-only, institutional-email, no-re-sharing terms as MultiClaim; total 3.5 GB.

## Key numbers

- Participation: 179 registered, 52 test submissions, 31 teams, 23 system papers.
- Table 2 (test): Polish 500 posts, 8,796 claims, 564 pairs; Turkish 500 posts, 12,536 claims, 550 pairs; monolingual total 4,276 posts, 260,880 claims, 4,959 pairs; crosslingual 4,000 posts, 272,447 claims, 5,322 pairs. Train+dev claims 153,743.
- Table 8 (monolingual S@10, column order avg eng fra deu por spa tha msa ara tur pol):
  - PINGAN AI: avg 0.9601; eng 0.9160; tur 0.9480; pol 0.9260.
  - PALI: avg 0.9472; eng 0.9040; tur 0.9300; pol 0.8880.
  - TIFIN India: avg 0.9383; eng 0.8800; tur 0.9040; pol 0.8860.
  - RACAI: avg 0.9377; eng 0.9000; pol 0.8820.
  - Baselines: E5-Large avg 0.8589 (pol 0.7980); BM25 avg 0.8123 (pol 0.7320).
- Table 9 (crosslingual S@10): PINGAN AI 0.85875; PALI 0.82675; RACAI 0.82450; TIFIN India 0.81025; GTR-T5-Large baseline 0.70525.
- Table 4: Polish test posts paired with Polish claims 55, English 14, French 2, Portuguese 1 (crosslingual test combinations).

## Relation to our project

- Not novel for us: an out-of-time test set already exists (test posts newer than all MultiClaim posts), and Polish is already a PFCR test language with published per-team scores.
- Leaves our gap open: the test pool reaches May 2024, after the last test post (March 2024), so a test post can be matched to a later fact-check; no date restriction of the pool is described.
- The Polish slice (500 posts, 564 pairs) is our main Polish evaluation source; its Polish fact-check pool for monolingual is 8,796 claims.
- Polish and Turkish were unseen in training, so the Polish-English contrast in SemEval scores mixes "unseen language" with any temporal effect; our DiD design must account for this.

## Verification

- Status: CORRECTED.
- Line 58: correct (train/dev from MultiClaim, 8 monolingual languages, test posts to March 2024, pool to May 2024, Polish and Turkish unannounced). Add: crosslingual train/dev covers 14 languages; MultiClaim posts all predate 2023.
- Line 59, first part: "PINGAN AI first monolingual average S@10 0.9601 and crosslingual 0.85875" correct.
- Line 59, approach: attributing "ensembles of multilingual embedders plus per-language fine-tuned rerankers and LLM reranking" to the top systems is only partly supported. PINGAN AI did not submit a system paper (no reference in Tables 8/9) and does not appear in Table 7, so its method is unknown. Per-language fine-tuned rerankers are QUST_NLP (rank 5 mono); LLM reranking of top 50 with Qwen2.5-72B-Instruct plus RRF is described for a top team (TIFIN India's paper confirms this for TIFIN); RACAI (rank 4 mono, 3 cross) used a single fine-tuned BGE-Multilingual-Gemma2 embedder without reranking.
- Line 59, "Polish and Turkish were the weakest languages for most teams": overstated. The overview says the two unseen languages "show a generally worse performance than the languages observed in the training data", but Table 8 shows English is as low or lower for several top teams (PINGAN AI eng 0.9160 < pol 0.9260 < tur 0.9480; TIFIN India eng 0.8800 < pol 0.8860). Polish is the lowest for PALI and RACAI; Turkish is not the lowest for any of the four top teams.
- Line 89: Polish 500 posts, 8,796 claims, 564 pairs correct.
- Line 81: "prior Polish PFCR evidence is the 500-post SemEval test slice and MultiClaim per-language tables" is incomplete: Polish is also one of the 20 AMC-16K languages (Vykopal et al. 2025, 400 annotated pairs plus pol-hbs, ces-pol, hun-pol crosslingual pairs) and is in Ramponi et al. 2025's 47 languages.
