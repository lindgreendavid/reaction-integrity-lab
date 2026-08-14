# Reaction Integrity Lab

**[Open the interactive laboratory →](https://lindgreendavid.github.io/reaction-integrity-lab/)**

[Read the Lab Notes article](https://blog-interactive.lindgreendavid.workers.dev/posts/reaction-integrity-lab-cleaning-leakage) ·
[View releases](https://github.com/lindgreendavid/reaction-integrity-lab/releases) ·
[Read the research report](docs/research-report.md)

An inspectable reproduction and data-integrity audit for reaction-condition prediction benchmarks.
The project asks a narrow question: **does the large accuracy change reported by ORDerly survive an
exact, version-pinned reproduction, and which data decisions make the benchmark easier?**

## Status

**Research product v1.0.0 — stable source, four-cell baseline, exact split, and prespecified
similarity/provenance audit.** The public paper, official code, Figshare identities, published
cleaning logs, endpoints, and data checksums are frozen here. The interactive site distinguishes
locally reproduced evidence from the neural-model cells that remain published references because
their exact checkpoint/prediction bundles are not in the versioned public release.

## Fixed primary endpoint

The reproduction target is the paper's top-3 exact-match accuracy for the combined solvent-and-agent
target across a 2 × 2 design:

1. reaction roles from ORD labels versus chemically informed reaction-string assignment;
2. rare components mapped to `other` versus reactions containing them removed.

The final peer-reviewed model cells are 67%, 68%, 35%, and 36%, respectively; their corresponding
frequency baselines are 52%, 52%, 20%, and 20%. The primary replication
criterion, frozen before training, is absolute agreement within 1.0 percentage point for every cell
under the authors' released configuration. Wider seed variation will be reported, never hidden.

An earlier project draft used 44%, 47%, 21%, and 24% from the upstream repository README. A direct
audit found that those are not the final article's combined solvent-and-agent Table 3 cells. The
correction and its timing are preserved in the protocol and source registry.

## What can already be reproduced

The lightweight audit package checks exact input overlap, full-record duplicates, missingness, and
output prevalence in any declared train/test split. Exact equality is intentionally narrower than
chemical similarity and is never presented as a complete leakage analysis.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[data,dev]'
python scripts/fetch_orderly.py --include-supplement
reaction-integrity \
  --train data/external/orderly_condition_train.parquet \
  --test data/external/orderly_condition_test.parquet \
  --output reports/local-split-audit.json
python scripts/reproduce_baselines.py \
  --data-dir data/external/paper-v3/condition_prediction_datasets
```

The downloaded Parquet files are checksum-verified and intentionally ignored by Git. Their exact
Figshare file IDs, byte sizes, MD5 checksums, DOI, version, and license are committed in
[`data/provenance.json`](data/provenance.json).

The deterministic four-cell baseline reproduction uses the authors' seed, shuffled 80% training
subset, and top-three exact complete-condition rule. Local results are 51.57%, 52.22%, 19.55%, and
20.24%; every value is within 0.46 percentage points of the paper's rounded 52%, 52%, 20%, and 20%.
The full machine-readable result is [`reports/v0.2-baselines.json`](reports/v0.2-baselines.json).

The v1 secondary audit additionally finds 5.78% canonical product-identity overlap and 80.84%
nonempty Bemis-Murcko scaffold overlap in the full test set. In a prespecified 1,000-row sample,
60.5% of products have a maximum training-product Morgan/Tanimoto similarity of at least 0.70
(Wilson 95% interval 57.44-63.48%). These are representation-overlap results, not proof of
patent-family leakage or prospective model failure. See
[`reports/v1-similarity-audit.json`](reports/v1-similarity-audit.json).

## Evidence boundaries

- The paper result is known, so this is a transparent reproduction—not a blinded preregistration.
- A lower score after chemical role reassignment shows that the earlier task was easier under the
  original representation. It does not establish intent, fraud, or universal model failure.
- Moving exact input collisions out of the test set prevents identity overlap; it does not eliminate
  scaffold, reaction-family, patent-family, or temporal similarity.
- The released v4 condition benchmark contains only the chemically informed variants. The full
  trusted-label contrast depends on the v3 supplementary data and the authors' pinned code.
- Exact neural checkpoints and prediction bundles for all four final cells are not contained in the
  versioned Git/Figshare release; fresh training from inferred defaults would be new evidence.

## Repository map

| Path | Purpose |
| --- | --- |
| `docs/protocol.md` | Frozen hypotheses, endpoints, tolerances, and analysis order |
| `docs/source-audit.md` | Primary sources, provenance, licensing, and claim boundaries |
| `docs/research-report.md` | Living report that separates completed and pending evidence |
| `docs/v1-release-audit.md` | v1 evidence gate, artifact decision, and remaining research |
| `reports/v0.1-source-audit.json` | Machine-readable published reference registry |
| `reports/v0.2-baselines.json` | Four-cell deterministic frequency-baseline reproduction |
| `reports/v1-similarity-audit.json` | Prespecified identity, scaffold, provenance, date, and similarity audit |
| `reports/v1-model-reproducibility.json` | Machine-readable neural-artifact availability decision |
| `src/reaction_integrity_lab/` | Small, tested split-audit package |
| [`site/`](https://lindgreendavid.github.io/reaction-integrity-lab/) | Live, accessible interactive explanation of the 2 × 2 benchmark |

## Primary sources

- Wigh et al. (2024), *ORDerly: Data Sets and Benchmarks for Chemical Reaction Data*,
  <https://doi.org/10.1021/acs.jcim.4c00292>
- ORDerly code: <https://github.com/sustainable-processes/ORDerly>
- Benchmark v4: <https://doi.org/10.6084/m9.figshare.23298467.v4>
- Supplementary data v3: <https://doi.org/10.6084/m9.figshare.23502372.v3>
- Open Reaction Database: <https://doi.org/10.1021/jacs.1c09820>

## License

Code and original prose are MIT-licensed. Upstream ORDerly datasets are CC BY 4.0 and are not
redistributed in this repository.
