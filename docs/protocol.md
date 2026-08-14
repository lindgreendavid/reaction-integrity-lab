# Frozen protocol v0.1.0

Frozen: 2026-08-14, before any local model training or inspection of locally reproduced scores.

## Study type

Transparent computational reproduction plus prespecified robustness audits. The published outcome
is already known; terms such as “preregistered discovery” must not be used.

## Primary question

Can the four published ORDerly combined solvent-and-agent top-3 exact-match accuracy cells be
reproduced from the authors' released data, code, and configuration?

## Factorial design and reference values

| Role assignment | Rare-component policy | Published baseline | Published model |
| --- | --- | ---: | ---: |
| Trust ORD labels | Map rare to `other` | 31% | 44% |
| Trust ORD labels | Delete reaction | 33% | 47% |
| Parse reaction string | Map rare to `other` | 4% | 21% |
| Parse reaction string | Delete reaction | 5% | 24% |

These are reference targets from the publication and official repository, not local results.

## Primary endpoint and success rule

- Endpoint: top-3 exact-match combination accuracy for solvents and agents.
- Unit: reaction in the released test split.
- Success: all four local point estimates are within 1.0 percentage point of the published cell.
- Partial reproduction: at least one cell exceeds that tolerance, with direction and absolute
  deviation reported for every cell.
- Failure to run is not a null result and must be labelled operationally incomplete.

## Fixed implementation order

1. Pin the paper DOI, code commit, Python environment, data versions, file IDs, checksums, and logs.
2. Verify dataset identities before reading Parquet contents.
3. Reproduce the authors' frequency-informed baseline.
4. Reproduce model training once with the authors' documented seed/configuration.
5. Repeat with five fixed seeds derived before execution and report all cells plus mean, range, and
   bootstrap interval across seeds; the single published-seed comparison remains primary.
6. Run exact-identity audits, then clearly labelled secondary similarity audits.

## Secondary audits

- exact reactant/product input-key overlap across train and test;
- exact full-record duplication across train and test;
- missing input/output cells;
- train output-combination prevalence and frequency baseline;
- sensitivity to rare-component policy;
- later, if RDKit identities can be frozen reproducibly: reaction/product similarity distributions.

Similarity-based work is secondary because thresholds and molecular representations add analyst
degrees of freedom. No similarity threshold will be selected after viewing model performance.

## Prohibited interpretations

- “The model cheated” or “the authors leaked data” without evidence of unavailable-at-inference
  information in the evaluated representation.
- “Chemical logic is always better” outside the tested ORD/USPTO construction.
- “The model does not work” based solely on a harder benchmark score.
- performance claims about prospective laboratory reactions.

