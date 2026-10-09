# Research report

## Current result

Reaction Integrity Lab has completed its source, provenance, licensing, endpoint, published-log,
released-data split audit, all four frequency-informed baseline reproductions, and the prespecified
v1 product-similarity and provenance audit. The exact neural-model artifacts remain **not
independently reproduced**. Therefore the 67%, 68%, 35%, and 36% cells remain published reference
values.

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
- reaction-level similarity beyond the completed product-only analysis;
- how performance changes under a truly prospective or patent-family/time-based split.

No conclusion about model-score reproduction is warranted yet.

## Prespecified v1 similarity and provenance audit

The full reaction-string/delete-rare test split contains 65,444 valid product structures. Canonical
product identity occurs in training for 3,784 rows (5.78%). Of the 63,852 rows with a nonempty
Bemis-Murcko product scaffold, 51,617 (80.84%) use a scaffold already present in training. Every
test row has an `extracted_from_file` category present in training; this is a source-file category,
not a verified patent-family identifier. Train and test both span grant years 1976-2016 with a
median of 2009, and no test row is later than the latest training grant year.

For the frozen 1,000-row sample, maximum product similarity against every unique valid training
product has median 0.734 and mean 0.732. The proportions at or above the frozen thresholds are:

| Maximum Morgan/Tanimoto | Sample proportion | Wilson 95% interval |
| --- | ---: | ---: |
| ≥0.70 | 60.5% | 57.44-63.48% |
| ≥0.80 | 30.0% | 27.24-32.91% |
| ≥0.90 | 11.7% | 9.85-13.84% |
| 1.00 | 8.4% | 6.84-10.28% |

Fingerprint similarity 1.0 is not canonical identity: finite fingerprints can collide or omit
distinctions. Together, these findings show that exact reaction-key separation does not guarantee a
chemically novel test set. They do not establish unavailable-information leakage, patent-family
overlap, or prospective performance.

## Neural-model reproducibility decision

The public code specifies TensorFlow 2.12, Python 3.10-3.11, seed 12345, teacher forcing, and the
W&B selection query used for Table 3. However, the exact four final model checkpoints and prediction
files are absent from the Git repository and Figshare condition archive. The plotting notebook uses
an authenticated W&B project and a local Teamspace model path without recording exact run IDs for
all four final cells. Training from inferred defaults would be a new run, not exact verification of
the published artifacts. Product v1.0.0 therefore stabilizes the completed audit without claiming
model reproduction. Full details are in [`v1-release-audit.md`](v1-release-audit.md).

## Post-release amendment (2026-10-09): within-training control

**POST-HOC, not preregistered.** The v1 similarity audit reports test-to-training overlap but gives no
reference for how much overlap any hold-out of this corpus would show. `reports/post-release-similarity-control.json`
applies the same canonicalisation, Bemis-Murcko and Morgan/Tanimoto definitions to the training set held out one
row at a time against training rows with a different exact input key (seed 20261009, 1,000-row similarity sample).
Result: product identity 8.72% (test 5.78%), scaffold 81.63% (80.84%), sampled max Tanimoto >=0.70 60.2% (60.5%),
>=0.90 14.0% (11.7%), =1.00 11.5% (8.4%). The overlap measured in the v1 audit is therefore not specific to the
released split; it is a property of the dataset. The v1 audit reproduced exactly (0 differences) on re-run. The
exact-identity gap (control higher) has no mechanism determined here. The v1 audit's conclusions about
exact-key separation not guaranteeing novelty stand; interpretation of the overlap as split-specific is withdrawn.
See `paper/paper.pdf`.
