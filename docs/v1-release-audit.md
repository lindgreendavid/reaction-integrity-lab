# v1.0.0 release audit

## Release meaning

Product v1.0.0 means the public audit is stable, reproducible, tested, and explicit about every
completed and incomplete evidence layer. It is not a claim that the authors' neural checkpoints
have been independently reproduced.

## Completed evidence

- primary paper, code commit, licenses, Figshare versions, file IDs, sizes, and MD5 checksums;
- deterministic reproduction of all four frequency-informed baselines within 0.46 percentage
  points of the rounded peer-reviewed values;
- exact declared input-key and full-record train/test audit;
- full-population canonical product, Bemis-Murcko scaffold, source-file, and grant-date audit;
- prespecified 1,000-row product-similarity sample against every unique valid training product;
- machine-readable reports with explicit denominators, exclusions, uncertainty, and boundaries;
- Python 3.10-3.13 CI for the core package, strict typing, linting, package build, CodeQL,
  accessibility checks, responsive layout checks, and reduced-motion support.

## Similarity and provenance result

The reaction-string/delete-rare split contains 65,444 valid test products. Of those, 3,784 (5.78%)
have a canonical product identity also present in training. Among 63,852 test rows with a nonempty
Bemis-Murcko product scaffold, 51,617 (80.84%) use a scaffold present in training. All 65,445 test
rows have an `extracted_from_file` category also seen in training. This field is reported as
source-file provenance, not as a patent-family identifier.

In the prespecified sample, 60.5% of test products have maximum Morgan/Tanimoto similarity at least
0.70 (Wilson 95% interval 57.44-63.48%), 30.0% at least 0.80 (27.24-32.91%), and 11.7% at least
0.90 (9.85-13.84%). The 8.4% at fingerprint similarity 1.0 must not be equated with canonical
identity because finite fingerprints can collide or omit distinctions.

These results show that exact reaction-input separation does not imply chemical novelty. They do
not prove leakage of unavailable information, patent-family overlap, model misconduct, or poor
prospective laboratory performance.

## Neural-model reproducibility decision

The code and paper identify the architecture and a run-selection query, but the exact four final
checkpoint/prediction bundles are not included in the Git repository or Figshare condition archive.
The plotting notebook reads runs from `ceb-sre/orderly` and predictions from a local Teamspace path;
the public API requires a W&B key, and the notebook does not record exact run IDs for all four final
cells. A new training run inferred from defaults would therefore be new evidence, not exact artifact
verification. The four neural-model cells remain labelled published references.

## Remaining research, not release debt

- a fully archived rerun if the authors publish exact checkpoints, predictions, or complete run IDs;
- a patent-family split if a verified family identifier is obtained;
- temporal model evaluation under an explicitly reconstructed cutoff split;
- reaction-level similarity beyond product-only fingerprints.

These are versioned future studies. They do not prevent the current, narrower audit product from
being stable and citable.
