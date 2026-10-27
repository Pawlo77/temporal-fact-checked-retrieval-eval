# 2025 - Panchendrarajan - MultiClaimNet

## Citation

- Authors: Rrubaa Panchendrarajan, Rubén Míguez Pérez, Arkaitz Zubiaga
- Title: MultiClaimNet: A Massively Multilingual Dataset of Fact-Checked Claim Clusters
- Venue: Findings of the ACL: EMNLP 2025, Suzhou, pages 11203-11215
- Year: 2025
- URL: https://aclanthology.org/2025.findings-emnlp.599/ ; data https://zenodo.org/records/15100352 ; preprint arXiv 2503.22280
- Verified on: 2026-10-27 (abstract page and Zenodo record read; PDF body not read)

## What it does

- Releases three multilingual claim-cluster datasets (claims in 86 languages in total): ClaimCheck and ClaimMatch built from two existing claim-matching datasets, and a large set built from MultiClaim.
- The large set is built by approximate-nearest-neighbour retrieval of candidate claim pairs plus automated LLM annotation of claim similarity, then clustering ("limited manual intervention").
- Benchmarks clustering techniques and sentence embedders.
- Zenodo fields: Claim, ClusterID, Language, Translation, NID; the MultiClaim subset also carries Timestamp and URL from the original dataset.
- Zenodo access: files restricted; research-only, institutional e-mail, no re-sharing; record licence shown as CC BY 4.0.

## Key numbers

- Zenodo table: ClaimCheck 1,187 claims / 197 clusters / 22 languages; ClaimMatch 1,171 / 192 / 36; MultiClaim 85.3K claims / 30.9K clusters / 78 languages.

## Relation to our project

- Enabler, not competitor: cluster ids plus timestamps let us find earlier same-claim fact-checks (siblings) for cluster-expanded qrels.
- Caveat: the clusters come from automated LLM similarity labels, so sibling relevance inherits that noise; our human validation step is needed.
- The 85.3K claims are a subset of MultiClaim fact-checks (v1 has 205,751), so many fact-checks have no cluster id; sibling coverage must be reported.
- No temporal evaluation.

## Verification

- Status: OK.
- Line 64 ("85.3K MultiClaim claims grouped into 30.9K clusters across 78 languages, with timestamps and URLs") correct. Add: clusters are formed from LLM-annotated similarity, and the venue citation should name Panchendrarajan et al.
