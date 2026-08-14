# Research report

## Current result

Reaction Integrity Lab has completed its source, provenance, licensing, endpoint, published-log,
and first released-data split audit. It has **not yet completed the independent model
reproduction**. Therefore the 44%, 47%, 21%, and 24% cells are presented only as published
reference values.

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
common exact five-slot output tuple appears in 16.08% of training rows; this descriptive prevalence
is **not** the paper's frequency-informed top-3 baseline.

The audit also records empty padded component slots. These are structural absences in fixed-width
columns and must not be described generically as chemical-data errors.

## What remains unknown

- whether all four published model cells reproduce within the frozen ±1 percentage-point rule;
- how much run-to-run seed variation exists;
- whether the confirmed exact identity separation leaves high chemical-similarity leakage;
- how performance changes under a truly prospective or patent-family/time-based split.

No conclusion about model-score reproduction is warranted yet.
