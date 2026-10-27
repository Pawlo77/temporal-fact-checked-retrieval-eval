# 2020 - Shaar - That is a Known Lie

## Citation

- Authors: Shaden Shaar, Nikolay Babulkov, Giovanni Da San Martino, Preslav Nakov
- Title: That is a Known Lie: Detecting Previously Fact-Checked Claims
- Venue: Proceedings of the 58th Annual Meeting of the ACL (ACL 2020), pages 3607-3618
- Year: 2020
- URL: https://aclanthology.org/2020.acl-main.332/ (PDF read: https://aclanthology.org/2020.acl-main.332.pdf)
- Verified on: 2026-10-27

## What it does

- Defines the task: given a check-worthy input claim and a set of verified claims, rank the verified claims so that those that help verify the input claim are ranked above the rest.
- Builds two datasets: PolitiFact (input claims are sentences from political debates/speeches linked by PolitiFact to earlier verified claims) and Snopes (tweets cited inside Snopes articles, matched against Snopes claims from ClaimsKG).
- Evaluates BM25 over title / verified claim / article body, BERT and sentence-BERT matching, and a rankSVM reranker over BM25 top-N.
- Uses MRR, MAP, MAP@k and HasPositive@k.
- Splits are given as fixed train/test counts (Table 3); the PDF excerpt read does not describe any date-based split or date restriction of the verified-claim pool.

## Key numbers

- Table 3: PolitiFact 768 Input-VerClaim pairs (614 train / 154 test), 16,636 verified claims; Snopes 1,000 pairs (800 / 200), 10,396 verified claims.
- Section 4.1: PolitiFact pairs come from overview reports for 78 public events in 2012-2019.
- Table 4: share of pairs with TF.IDF cosine above 0.25: PolitiFact 27%, Snopes 50%.
- Table 5 (PolitiFact test): best BM25 (IR:Body) MRR .565; best reranker (Rerank-IR-top-100) MRR .608.
- Section 7.2: Snopes IR:VerClaim+Title MRR 0.664.

## Relation to our project

- Not novel for us: the PFCR task definition, the "rank an archive of earlier fact-checks" framing, and the observation that fact-check articles can contain the input text verbatim (the paper drops body matching on Snopes because tweets were extracted from article bodies; Section 7.2).
- The Snopes construction (tweets found inside the fact-check article) is the same mechanism as MultiClaim backlinks; it implies most gold pairs are post-before-fact-check by construction, which supports our H1, but the paper gives no date statistics.
- Gap left: no temporal protocol, no date-restricted index.
- A follow-up by the same group (Shaar et al., Findings NAACL 2022, see `2022 - Shaar - Role of Context in PFCR.md`) adds a chronological debate-level split on the PolitiFact part.

## Verification

- Status: OK.
- Enhanced topic research line 53 ("PFCR task definition: Shaar et al., ACL 2020, 'That is a Known Lie' (Snopes, PolitiFact)") is correct.
- Additional context worth adding to the note: the PolitiFact input claims are debate sentences, not social-media posts; only the Snopes part uses tweets.
