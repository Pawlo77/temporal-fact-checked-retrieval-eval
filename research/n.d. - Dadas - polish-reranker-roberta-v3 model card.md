# n.d. - Dadas - polish-reranker-roberta-v3 model card

## Citation

- Author: Sławomir Dadas (Hugging Face user sdadas)
- Title: sdadas/polish-reranker-roberta-v3 (model card)
- Venue: Hugging Face model card
- Year: not stated on the parts of the card I read (n.d.); the card compares against Qwen3-Reranker, so it is from 2025 or later
- URL: https://huggingface.co/sdadas/polish-reranker-roberta-v3
- Verified on: 2026-10-27 (card read)

## What it does

- Polish cross-encoder reranker for RAG; successor of polish-reranker-roberta-v2.
- Based on a new long-context Polish RoBERTa (PKOBP/polish-roberta-8k), up to 8,192 tokens (v2: 512).
- Trained by knowledge distillation from the LLM reranker BAAI/bge-reranker-v2.5-gemma2-lightweight with a RankNet loss; adds about 40,000 public-administration passages.
- Licence shown on the card: "gemma" (not Apache-2.0).

## Key numbers

- 443M parameters.
- Card: NDCG@10 of 66.21 in the PIRB Rerankers category; average PIRB score rises from 64.49 to 65.17 (v2 to v3) with mmlw-retrieval-roberta-large as retriever, and from 65.30 to 66.21 with BAAI/bge-multilingual-gemma2.
- Card: outperforms Qwen3-Reranker-8B on 18 of 41 PIRB tasks.
- Table 2 (BGE-M3 retriever; opi-urzedowe / ezd-qa / ezd-ir-chunked NDCG@10): polish-reranker-roberta-v3 86.3 / 80.1 / 86.7; bge-reranker-v2-m3 (568M) 78.8 / 74.3 / 85.4; Qwen3-Reranker-8B 84.1 / 79.9 / 84.8.

## Relation to our project

- S4 Polish reranker over a Polish candidate list; the 8K context lets it read full fact-check articles, not only claims and titles.
- The "gemma" licence may restrict redistribution of derived artefacts; check before releasing anything built on it.
- Does NOT cover: cross-lingual reranking, temporal evaluation.

## Verification

- OK. The note names the model only (S4) and makes no numeric claim about it. Addition: record the gemma licence and the 66.21 PIRB reranker score from the card.
