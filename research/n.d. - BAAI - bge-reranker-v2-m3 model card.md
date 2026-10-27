# n.d. - BAAI - bge-reranker-v2-m3 model card

## Citation

- Author: BAAI (FlagEmbedding team)
- Title: BAAI/bge-reranker-v2-m3 (model card)
- Venue: Hugging Face model card; links arXiv 2312.15503 and 2402.03216 (M3-Embedding)
- Year: not stated on the parts of the card I read (n.d.)
- URL: https://huggingface.co/BAAI/bge-reranker-v2-m3
- Verified on: 2026-10-27 (card read)

## What it does

- Cross-encoder reranker built on bge-m3 as base model; labelled multilingual, "lightweight ... strong multilingual capabilities".
- Outputs a relevance score that can be mapped to [0, 1] with a sigmoid.
- The card recommends it for multilingual use (with bge-reranker-v2-gemma) and for Chinese/English.
- Licence: Apache-2.0.
- Card evaluation: reranks top-100 from bge-m3 on MIRACL (shown as images; I took no numbers from them).

## Key numbers

- None read as text on the card. Secondary: 568M parameters, 8,192 context (polish-reranker-roberta-v3 card Table 2); MMTEB-R 58.36 (Qwen3 Embedding report).
- The card's transformers example uses max_length=512; the 8,192 figure is from the secondary source.

## Relation to our project

- S4 multilingual reranker that can score Polish posts against English fact-checks, unlike the Polish-only reranker.
- Card lists FEVER among training data for the LLM-based rerankers; training data for v2-m3 itself was not stated in what I read.
- Does NOT cover: temporal evaluation.

## Verification

- OK. Model exists and is multilingual, as the note assumes (S4).
