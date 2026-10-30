# Analysis reference

## Designs that remove a bias

- **Landmark comparison.** Pick a time t (for example the median unlock step). Keep units
  alive at t. Group them by status at t (event already happened or not yet). Count
  outcomes after t only. Grouping by "event ever happened" gives the event group extra
  survival by construction; on a null world it shows a large spurious lift.
- **Fresh seeds.** Tuning seeds are the selection sample. Report the chosen configuration
  on seeds never used to choose it; mark the result "n/a" with the reason when fewer than
  about five fresh seeds exist.
- **Survivorship.** A first-time median over the units that reached the event hides the
  units that never did: give the share reached, and treat the rest as censored.
- **Clustering.** Many units per group (policies per method) are not independent: test the
  within-group association, or resample groups.

## Null simulation for each derived statistic

1. Simulate the world with the effect switched off (for example independent event times,
   constant hazard). The statistic must be near zero within a stated tolerance.
2. Simulate with a known effect size; the statistic must recover it.
3. Check the real-data value against a second implementation (a plain loop, scipy, a
   hand-computed toy case), not against the same formula.

## Before quoting a number

- It comes from a file the pipeline writes; the report reads it through a generated macro.
- Quantities with too few uncensored units (fewer than three) are not printed.
- Fact-check table per note: note | line | claim | source file | verdict (match,
  mismatch, no source, flag) | fix. Flag single-seed support, causal wording, a median
  quoted as "every", a domain fact without a source, a count that is off by the censored
  or missing units.
- Words: "is accompanied by", "consistent with", "in seed 7", "the median policy".

## Review questions

- What is the unit, and is every interval and test over that unit?
- Which configurations are pooled? Which seeds chose the configuration?
- Is any group defined by something that happens later than the comparison starts?
- Does the pooled sign hold within groups?
- What is the baseline, and how many values are censored or missing?
- Would the claim survive with one seed removed?
