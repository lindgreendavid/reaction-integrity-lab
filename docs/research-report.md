# Research report

## Current result

Reaction Integrity Lab has completed its source, provenance, licensing, endpoint, published-log,
released-data split audit, and all four frequency-informed baseline reproductions. It has **not yet completed the independent model
reproduction**. Therefore the 67%, 68%, 35%, and 36% cells are presented only as published
reference values.

The final peer-reviewed article's combined solvent-and-agent Table 3 values supersede the older
31/44, 33/47, 4/21, and 5/24 baseline/model pairs still shown in the upstream repository README.
This correction was made before local model inspection. It changes the reference targets, not the
frozen endpoint or success rule.

## Four-cell baseline reproduction

The official v3 supplementary archive matched its published MD5. Using upstream commit
`77d0d900e369f3b512a44d47c740bd4bcb98fcb6`, NumPy seed 12345, the authors' shuffled 80% training
subset, and row-wise order-invariant top-three complete-condition matching produced:

| Role assignment | Rare policy | Local baseline | Published | Absolute deviation |
| --- | --- | ---: | ---: | ---: |
| Trust labels | Map to `other` | 51.57% | 52% | 0.43 pp |
| Trust labels | Delete reaction | 52.22% | 52% | 0.22 pp |
| Parse reaction string | Map to `other` | 19.55% | 20% | 0.45 pp |
| Parse reaction string | Delete reaction | 20.24% | 20% | 0.24 pp |

All four satisfy the prespecified ±1 percentage-point success rule for the baseline. This validates
the baseline implementation, data variants, split selection, and metric interpretation. It does not
substitute for training the neural model.

## What the source audit establishes

The proposed reproduction is technically tractable and falsifiable. The authors provide open code,
versioned CC BY 4.0 data, cleaning configurations, logs, and explicit benchmark numbers. The v4
chemically informed train/test files total 394,497,018 bytes, so exact-identity checks are feasible
without downloading the full 1.95 GB benchmark collection.

The official cleaning log also reveals that “cleaning” is not one operation: component-count rules,
required-field checks, deduplication, rare-component handling, scrambling, and split collision
handling each alter the estimand. The interactive site exposes these decisions separately.

## Released-data split audit

Both v4 condition Parquet files matched their Figshare MD5 checksums. Together they contain exactly
691,142 rows, equal to the final row count in the official reaction-string/delete-rare cleaning log:
625,697 training and 65,445 test rows.

Using the declared input key `(reactant_000, reactant_001, product_000)`, the test split contains
zero rows whose exact normalized input key occurs in training. Using those inputs plus the declared
two solvent and three agent slots, it also contains zero exact full-record duplicates from training.
This independently confirms the narrow identity-separation property of the released split.

The test set has 65,350 unique exact input keys for 65,445 rows, so some input keys repeat within
test with different records. Training has 611,065 unique input keys across 625,697 rows. The most
common exact five-slot output tuple appears in 16.08% of training rows. Applying the authors'
shuffled 80% training subset and top-three complete-combination rule gives 20.24% on this
reaction-string/delete-rare test set, agreeing with the peer-reviewed 20% baseline after rounding.

The audit also records empty padded component slots. These are structural absences in fixed-width
columns and must not be described generically as chemical-data errors.

## What remains unknown

- whether all four published neural-model cells reproduce within the frozen ±1 percentage-point rule;
- how much run-to-run seed variation exists;
- whether the confirmed exact identity separation leaves high chemical-similarity leakage;
- how performance changes under a truly prospective or patent-family/time-based split.

No conclusion about model-score reproduction is warranted yet.
