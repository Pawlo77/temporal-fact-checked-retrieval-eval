# 2022 - Glockner - Missing Counter-Evidence

## Citation

- Authors: Max Glockner, Yufang Hou, Iryna Gurevych
- Title: Missing Counter-Evidence Renders NLP Fact-Checking Unrealistic for Misinformation
- Venue: Proceedings of EMNLP 2022 (Abu Dhabi), pages 5916-5936, DOI 10.18653/v1/2022.emnlp-main.397
- Year: 2022
- URL: https://aclanthology.org/2022.emnlp-main.397/ (PDF: https://aclanthology.org/2022.emnlp-main.397.pdf)
- Verified on: 2026-10-27 (Anthology page and PDF read)

## What it does

- Contrasts NLP fact-checking task definitions with how professional fact-checkers refute misinformation; analyses 100 PolitiFact/Snopes misinformation claims (50 per site; 25 from MultiFC-era, 25 from 2020/2021) by verification strategy.
- Defines two requirements for realistic evidence: (1) sufficient to refute the claim, (2) not leaked from existing fact-checking articles.
- Surveys fact-checking datasets and finds that no dataset with real-world misinformation satisfies both criteria.
- Detects leaked evidence in MultiFC semi-automatically (URL patterns of fact-checking sites plus regex phrases) and shows BERT models trained on Snopes/PolitiFact claims exploit leaked evidence.
- Defines leaked evidence as snippets relying on the verification of the same claim, or providing information from the claim's future.

## Key numbers

- Table 2: of 75 refuted claims analysed, fact-checkers used global counter-evidence in 20 (26.7%); about two-thirds were refuted via source guarantees.
- Section 4/Table 5: 16,244 MultiFC misinformation claims analysed; leaked evidence found for 8,999 (55.6%) by URL, 9,656 (59.7%) by phrase, 11,267 (69.7%) by URL or phrase.
- Manual check: 83.9% of 230 automatically flagged snippets confirmed leaked; 97/100 sampled claims contain at least one leaked snippet.
- Table 6: of 100 claims with no automatically detected leak, 32 still contained leaked evidence on manual inspection.

## Relation to our project

- Motivates our "label leakage" and "answerability" framing: evidence written after the claim is unrealistic for novel claims, which is exactly the situation of a PFCR query whose only gold fact-check post-dates it.
- The paper explicitly separates its concern from detecting already-verified claims (it cites Shaar et al. 2020 as a "related yet different task"); it does not evaluate claim-matching retrieval, index composition, or ranking metrics.
- Does NOT cover: retrieval over a fact-check archive, time-respecting index construction, pool-size control, multilingual or Polish data.

## Verification

- OK. The Enhanced topic research note (Novelty map, "Temporal leakage in evidence retrieval") says "Glockner et al., EMNLP 2022 (evidence leaked from fact-check articles)". Title, venue, year and the characterisation match the source. Reference-list URL resolves.
