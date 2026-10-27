# 2011 - Ounis - TREC 2011 Microblog Track Overview

## Citation

- Authors: Iadh Ounis, Craig Macdonald, Jimmy Lin, Ian Soboroff
- Title: Overview of the TREC-2011 Microblog Track
- Venue: Proceedings of TREC 2011 (TREC 20), NIST Special Publication 500-296, DOI 10.6028/NIST.SP.500-296.microblog-overview
- Year: 2011 (proceedings; NIST lists publication 2013)
- URL: https://trec.nist.gov/pubs/trec20/papers/MICROBLOG.OVERVIEW.pdf
- Verified on: 2026-10-27 (PDF read). Not cited in the Enhanced topic research note; added as missed prior work.

## What it does

- Defines the real-time search task "At time t, find tweets about topic X" over the Tweets2011 corpus (about 16M tweets, 23 Jan - 8 Feb 2011).
- Each of 50 topics carries a `querytime` and `querytweettime`, the query's timestamp.
- Requires at least one compulsory automatic run without external or future evidence, and defines them explicitly.
- Future evidence: "Information that would not have been available to the system at the timestamp of the query", with the example of IDF scores computed using tweets not yet posted at query time.
- Reports compulsory (real-time, no external resources) runs separately from unconstrained runs (Tables 2-4).

## Key numbers

- 59 groups, 184 runs; pooling to depth 30; 49 topics evaluated (topic 50 had no relevant tweets).
- Table 1: best P@30 0.6116, median 0.2575 (all relevant).
- Bootstrap test: differences in P@30 or MAP below 0.07 have run-swap probability above 5%.
- Spearman rho 0.82 between group rankings by MAP and by P@30.
- 14 groups did not submit the compulsory constrained run.

## Relation to our project

- The strongest prior instance of time-respecting IR evaluation: query-time document cutoffs plus an explicit ban on future corpus statistics. Our causal protocol should cite it as the origin of the idea and position the novelty as its first application to PFCR, with answerability, pool-size and label decomposition.
- Adds a leakage type missing from the note's taxonomy: corpus-statistics leakage. BM25 IDF (and any normalisation, vocabulary, or dense-index training) computed over the full pool uses future fact-checks even when future documents are filtered from results. The causal protocol must rebuild BM25 statistics per cutoff (or per rolling origin) or report the effect.
- Its separate reporting of constrained vs unconstrained runs is a template for our random vs causal tables.
- Does NOT cover: claim matching, multilingual retrieval, answerability, relevance labels created after the fact.

## Verification

- Not in the note (missed). Recommend adding to the Novelty map under "What already exists" and to the leakage taxonomy (corpus-statistics leakage).
