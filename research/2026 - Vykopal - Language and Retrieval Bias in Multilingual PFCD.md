# 2026 - Vykopal - Language and Retrieval Bias in Multilingual PFCD

## Citation

- Authors: Ivan Vykopal, Antonia Karamolegkou, Jaroslav Kopčan, Qiwei Peng, Tomáš Javůrek, Michal Gregor, Marian Simko
- Title: Investigating Language and Retrieval Bias in Multilingual Previously Fact-Checked Claim Detection
- Venue: Proceedings of EACL 2026 (Volume 1: Long Papers), Rabat, pages 5195-5221
- Year: 2026
- URL: https://aclanthology.org/2026.eacl-long.240/ (abstract page read; the PDF body was not read)
- Verified on: 2026-10-27

## What it does

- Evaluates six open multilingual LLMs across 20 languages on AMC-16K with fully multilingual prompting (task prompts translated into each language).
- Reports language bias: better performance on high-resource languages than low-resource ones, with trends by model family, size and prompting strategy.
- Introduces "retrieval bias": with multilingual embedding models, certain claims are retrieved disproportionately across posts, inflating retrieval performance for popular claims and under-representing rare ones.

## Key numbers

- From the abstract: six LLMs, 20 languages. No other numbers were read (PDF body not fetched).

## Relation to our project

- Not novel for us: any language-bias framing of Polish vs English, and the observation that popular claims dominate retrieval. Our Polish-English contrast must be framed as a temporal (causal-penalty) difference, not language bias.
- Retrieval bias toward popular claims interacts with our design: popular claims are more likely to have earlier sibling fact-checks, so cluster-expanded labels may favour them; we should report the causal penalty stratified by claim popularity (cluster size), which the note already lists as a covariate.
- No temporal protocol in what was read.

## Verification

- Status: OK (abstract-level only).
- Line 63 ("language bias and retrieval bias (popular claims retrieved disproportionately) on AMC-16K") matches the abstract.
