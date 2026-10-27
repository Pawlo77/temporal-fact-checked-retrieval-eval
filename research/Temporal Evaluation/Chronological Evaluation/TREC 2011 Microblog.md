---
title: "TREC 2011 Microblog"
aliases: ["Overview of the TREC 2011 Microblog Track", "Overview of the TREC-2011 Microblog Track"]
authors: ["Iadh Ounis", "Craig Macdonald", "Jimmy Lin", "Ian Soboroff"]
year: 2011
venue: "Proceedings of the Twentieth Text REtrieval Conference (TREC 2011), NIST Special Publication 500-296"
doi: "10.6028/NIST.SP.500-296.microblog-overview"
url: "https://trec.nist.gov/pubs/trec20/papers/MICROBLOG.OVERVIEW.pdf"
citekey: ounis2011overview
verified: 2026-10-27
theme: "[[Chronological Evaluation]]"
tags: [type/paper, theme/chronological, topic/temporal, topic/leakage, topic/shared-task, topic/evaluation, topic/english]
---
# TREC 2011 Microblog

> [!info] TL;DR
> The first TREC Microblog track defines real-time search: at time $t_q$, find tweets about a topic, using only what existed at $t_q$. Each topic carries a query timestamp, and the compulsory run must use no future evidence, which explicitly includes corpus statistics such as IDF computed from later tweets. 59 groups submitted 184 runs; the best compulsory run reached P@30 0.4551 and the median topic-level P@30 was 0.2575, so the task was far from solved.

## Motivation

- Microblog search needs the most recent relevant posts at query time, which a static ad hoc collection with no notion of query time cannot evaluate.
- Twitter's terms forbid redistributing tweets, so a reusable test collection needed a new distribution method.
- Evaluating "search at time $t_q$" offline requires rules about what a system may know at $t_q$; the track extends the TREC Blog track line of social-media evaluation ([Macdonald et al., 2010](https://doi.org/10.1145/1842890.1842899)) with such rules.

## Method

Notation of this vault: query (topic) $q$ with time $t_q$; documents (tweets) with times before or after $t_q$.

**Task.** "At time $t_q$, find tweets about topic X", ranked from newest to oldest. Each of 50 topics gives a query time and the id of the nearest tweet in the corpus.

**Future evidence.** Information not available to the system at $t_q$, for example IDF computed with tweets posted after $t_q$. **External evidence** is anything beyond the corpus (other Twitter data, Wikipedia, the web).

Intuition: a time-respecting evaluation must filter not only the returned documents but every statistic the ranker uses.

**Run types.** Groups could submit up to four runs; at least one compulsory automatic run had to use neither future nor external evidence. Results are reported for compulsory runs and, separately, for the best run of any type.

**Judging.** Runs pooled to depth 30 by submitted rank; retweets removed; near-duplicates clustered by shingling; three-level relevance by NIST assessors who also followed links. P@30 is the main measure, MAP secondary.

## Key numbers

- 59 groups, 184 runs; 49 topics evaluated (one had no relevant tweets), 33 with highly relevant tweets.
- Best compulsory run P@30 0.4551 (MAP 0.1892); per-topic best P@30 0.6116, median 0.2575 with all relevant tweets.
- With highly relevant tweets only, the per-topic median P@30 is 0.0687.
- Group ranking by best compulsory run vs best run of any type correlates at Spearman 0.93, so relaxing the time and resource rules changed group order little.
- Bootstrap test: P@30 or MAP differences below 0.07 have a run-swap probability above 5%.

## Experiments

- **Compulsory runs:** 45 groups submitted a real-time, no-external run; ranking by MAP and by P@30 agrees at Spearman 0.82.
- **Unconstrained runs:** best run per group regardless of constraints, including five manual runs; group order nearly unchanged.
- **Highly relevant only:** group order agrees with the all-relevant order at Spearman 0.95.
- **Pooling audit:** pooling by submitted rank was a mistake because groups gave ranks different meanings; comparisons across groups are less valid than within a group.

## Data

- Tweets2011: about 16 million tweets, a roughly 1% sample from 23 January to 7 February 2011, distributed as tweet ids plus download tools.
- 50 topics with query times; judgments from depth-30 pools.

> [!failure] Limitations
> - The task semantics were underspecified (rank vs score vs time order), which weakens cross-group comparison.
> - 14 groups did not submit the required compulsory run, and compliance with the no-future-evidence rule is self-reported.
> - The corpus decays as tweets are deleted, so later copies are only substantially identical.
> - Two weeks of English tweets; no measure of how much future evidence actually helped.

## Relation to our project

- The oldest precedent for our causal index: each query has a time and systems may use only documents and statistics from before it ([[Proposed Task]]). We cite it as the origin of the idea, not claim it as new.
- Its definition of future evidence names corpus-statistics leakage: BM25 IDF computed over the full fact-check pool uses later fact-checks even when they are filtered from results. Our BM25 must use causal-pool statistics, with full-pool statistics as a sensitivity row ([[Enhanced topic research]]).
- Separate reporting of constrained and unconstrained runs is the template for our random vs causal tables; the small rank change it found is a baseline expectation to test ([[Research summary]]).
- Unlike PFCR, relevance here is topical and the pool grows continuously; it has no notion of answerability.

## Future work

- **Done:** a second year of real-time search plus a real-time filtering task; [Soboroff et al., 2012](https://trec.nist.gov/pubs/trec21/papers/MICROBLOG12OVERVIEW.pdf).
- **Done:** fix collection access and run semantics with a search API shared by all participants (evaluation as a service); [Lin and Efron, 2013](https://trec.nist.gov/pubs/trec22/papers/MB.OVERVIEW.pdf).
- **Open:** measuring how much future corpus statistics inflate scores, compared with the same systems using causal statistics (searched 2026-10).
