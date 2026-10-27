# CORRECTIONS-B

Errors and gaps found in `knowledge/handbook/Enhanced topic research.md` for part B (evaluation-methodology and model literature, plus Venue strategy). Checked against primary sources on 2026-10-27. Line numbers refer to the note as read on that date. Per-paper evidence is in the matching `research/<Year> - <Author> - <title>.md` note.

## Summary

- Papers/cards checked: 21. OK: 16. CORRECTED: 5 (LongEval, Gorman and Bedrick, Søgaard et al., Simulated Ignorance Fails, mmlw 58.46 attribution). COULD NOT VERIFY: 0. All three 2026 papers exist with the cited titles and venues.
- Venue items checked: 6. Correct: ARR/ACL 2027, ECIR 2027 resource, NLP4PI 2026, SIGIR 2027 full-paper date. Corrected: FEVER co-location, CLEF lab timing. Minor additions: SIGIR abstract deadline.
- Missed prior work: TREC 2011 Microblog track (time-respecting IR with an explicit "future evidence" ban, including corpus statistics) and StreamingQA (ICML 2022).

## Novelty map

1. Line 68: "IR temporal persistence: LongEval at CLEF 2023 onward (performance drop as test data moves away from training time)."
   - Problem: that is the lab's motivation, not its result. The 2023 retrieval overview shows no uniform drop; some runs improved on the short- and long-term collections, and the top ST systems were stable or decreasing.
   - Fix: "IR temporal persistence: LongEval (CLEF 2023 onward) evaluates systems on successive Qwant snapshots; in 2023 the change in NDCG was system-dependent, not a uniform drop (Alkhalifa et al., CLEF 2023 overview)."

2. Line 70: "Split methodology: Gorman and Bedrick, ACL 2019; Søgaard et al., EACL 2021 (random splits overestimate; prefer biased or time-based splits)"
   - Problem: Gorman and Bedrick argue for random splits over standard splits; Søgaard et al. rebut them. Søgaard et al. recommend multiple independent new samples, else biased (heuristic or adversarial) splits; "time-based" is not their stated recommendation (temporal drift is an appendix analysis).
   - Fix: "Split methodology: Gorman and Bedrick (ACL 2019) argue for random over standard splits and for significance testing; Søgaard et al. (EACL 2021) show random splits over-estimate performance on new samples and recommend independent test samples, else biased/adversarial splits."

3. Line 69: "simulated ignorance does not replicate true ignorance (arXiv 2601.13717)."
   - Problem: the paper is now published at IJCAI 2026 (Li, Wang, El Lahib, Xia, Pi; pages 5837-5845, DOI 10.24963/ijcai.2026/650). The published abstract reports 470 questions; arXiv v1 reports 477.
   - Fix: "(Li et al., IJCAI 2026; arXiv 2601.13717)".

4. Line 65 (addition, not an error): "AVeriTeC, NeurIPS 2023 (evidence must predate the claim)".
   - Add: AVeriTeC also orders train/dev/test temporally, and its pre-claim guarantee is approximate (Google date estimates; about 6% of dev answers come from fact-checking domains, mostly earlier fact-checks of the same claim). The second point supports our sibling-qrel idea.

5. Missing from "What already exists" and from the novelty claim "A formal causal protocol for PFCR ... that no prior PFCR evaluation has used" (line 43):
   - TREC 2011 Microblog track (Ounis, Macdonald, Lin, Soboroff) already ran query-time ("At time t, find tweets about topic X") evaluation with a compulsory run banning "future evidence", defined to include IDF computed on tweets posted after the query. The PFCR-specific claim still holds, but the general idea must be credited.
   - StreamingQA (Liska et al., ICML 2022): dated questions against a growing time-stamped news corpus; precedent for the rolling-origin protocol.

## Leakage taxonomy and Systems

6. Lines 106-113 (leakage taxonomy) miss corpus-statistics leakage.
   - Fix: add "Statistics leakage: BM25 IDF, vocabulary, normalisation or any index-level statistic computed over the full pool including future fact-checks (TREC 2011 Microblog's definition of future evidence)." Rebuild BM25 statistics per cutoff in the causal and rolling-origin protocols.

7. Line 119: "sdadas/mmlw-retrieval-roberta-large (PIRB NDCG@10 58.46)"
   - Problem: 58.46 is the model card's leaderboard figure for the current model version (updated 2023-12-26); the PIRB paper's Table 3 reports 58.06 for the distilled + fine-tuned polish-roberta-v2 (large) retriever. multilingual-e5-large scores 57.29 zero-shot in the same paper, so the Polish model's margin is about 1 point.
   - Fix: "(PIRB NDCG@10 58.46 per model card; paper Table 3: 58.06; mE5-large 57.29)".
   - Also, "bilingual or Polish-specialised": the card confirms distillation on 60M Polish-English pairs, so cross-lingual Polish-to-English retrieval is plausible but unreported; measure it.

8. Line 120 (addition): sdadas/polish-reranker-roberta-v3 has licence "gemma" on its card (443M parameters, 8,192-token context, PIRB reranker NDCG@10 66.21). Check the licence before releasing derived artefacts. BAAI/bge-reranker-v2-m3 is Apache-2.0.

9. Line 232: "Wang et al. 2024, Multilingual E5 Text Embeddings" is an arXiv technical report with no peer-reviewed venue; label it as such. Line 235 (Qwen3 Embedding) is likewise an arXiv technical report.

## Reference list

10. Line 224: "Don't Get Ahead of Yourself: data leakage in sequential recommender evaluation, RecSys 2025"
    - Fix: "Le, Liu, Medlar, Glowacka 2025, Don't Get Ahead of Yourself: A Critical Study on Data Leakage in Offline Evaluation of Sequential Recommenders, RecSys '25, pp. 1164-1168 (extended abstract)".

11. Line 225: "LongEval CLEF 2023: https://clef-longeval-2023.github.io/"
    - Fix: cite the overview paper: "Alkhalifa et al. 2023, Overview of the CLEF-2023 LongEval Lab on Longitudinal Evaluation of Model Performance, CLEF 2023 (LNCS), pp. 440-458, https://link.springer.com/chapter/10.1007/978-3-031-42448-9_28 ; extended overview CEUR-WS Vol-3497 paper 184".

12. Line 229: add authors: "El Lahib, Xia, Li, Wang, Pi 2026".

13. Line 230: add authors and landing page: "Zhang and Stadie 2026 ... https://aclanthology.org/2026.findings-emnlp.1690/".

14. Line 231: "Simulated Ignorance Fails (pre-cutoff forecasting): https://arxiv.org/abs/2601.13717"
    - Fix: "Li, Wang, El Lahib, Xia, Pi 2026, Simulated Ignorance Fails: A Systematic Study of LLM Behaviors on Forecasting Problems Before Model Knowledge Cutoff, IJCAI 2026: https://ijcai.org/proceedings/2026/650 ; arXiv 2601.13717".

15. Line 223: add authors "Ji, Sun, Zhang, Li".

16. Add references: Ounis et al. 2011 TREC Microblog overview (https://trec.nist.gov/pubs/trec20/papers/MICROBLOG.OVERVIEW.pdf); Liska et al. 2022 StreamingQA (https://proceedings.mlr.press/v162/liska22a.html).

## Venue strategy

17. Line 183: "ARR deadline 4 Jan 2027 per ccfddl"
    - Date is correct, but cite the official source: ACL 2027 call (https://2027.aclweb.org/calls/main/) gives ARR submission deadline 4 January 2027 (AoE); commitment deadline TBD; ACL 2027 is 17-22 August 2027 in Kyoto (main conference 20-22 Aug). Papers not accepted to main are automatically considered for Findings.

18. Line 184: "SIGIR 2027 short or resource track (full-paper deadline 21 Jan 2027; short and resource dates TBA)"
    - Correct per https://sigir2027.org/. Add: abstract deadline 14 January 2027; notification 5 April 2027; conference 18-24 July 2027, San Jose (the site's page title says 19-24 July; the body says 18-24).

19. Line 184: "ECIR 2027 resource track deadline 2 Nov 2026 is too close for results."
    - Correct per https://www.ecir2027.co.uk/call-for-resource-papers (submission 2 November 2026, notification 7 December 2026; conference 21-25 March 2027, Southampton). Full-paper (5 October 2026) and reproducibility (19 October 2026) deadlines have already passed.

20. Line 185: "FEVER (ACL-co-located; check 2027 CFP)"
    - Problem: FEVER's co-location varies; FEVER9 was co-located with EACL 2026 (28 March 2026) per https://fever.ai/ (FEVER8 was at ACL 2025). No FEVER 2027 announcement found on 2026-10-27.
    - Fix: "FEVER (co-location varies: ACL 2025, EACL 2026; no 2027 CFP yet)".

21. Line 185: "NLP4PI (2026 edition held 28 Oct 2026 at EMNLP; target 2027)"
    - Correct: the NLP4PI 2026 proceedings preface states 28 October 2026, Budapest, co-located with EMNLP 2026.

22. Line 186: "the protocol and split are a candidate task proposal for a future CLEF lab"
    - Clarify: CLEF 2027 lab proposals closed on 17 July 2026 (notification 7 Aug 2026; CLEF 2027 is 14-17 September 2027, Bucharest). The earliest possible new lab is CLEF 2028; joining an existing CLEF 2027 lab (e.g. LongEval or CheckThat!, if running) is the only 2027 option. A CLEF 2028 proposal deadline was not published as of 2026-10-27.
