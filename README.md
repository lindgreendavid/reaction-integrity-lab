# Reaction Integrity Lab

**[Open the interactive laboratory →](https://lindgreendavid.github.io/reaction-integrity-lab/)**

[Read the Lab Notes article](https://blog-interactive.lindgreendavid.workers.dev/posts/reaction-integrity-lab-cleaning-leakage) ·
[View the v0.1.0 release](https://github.com/lindgreendavid/reaction-integrity-lab/releases/tag/v0.1.0) ·
[Read the research report](docs/research-report.md)

An inspectable reproduction and data-integrity audit for reaction-condition prediction benchmarks.
The project asks a narrow question: **does the large accuracy change reported by ORDerly survive an
exact, version-pinned reproduction, and which data decisions make the benchmark easier?**

## Status

**Research product v0.1.0 — source and released-data split audit complete; model reproduction
pending.** The public paper, official code, Figshare identities, published cleaning logs, endpoints,
and two released split-file checksums are frozen here. The figures currently shown in the
interactive site are explicitly labelled as *published reference results*. They are not claimed as
independently reproduced until the model run and its environment are archived.

## Fixed primary endpoint

The reproduction target is the paper's top-3 exact-match accuracy for the combined solvent-and-agent
target across a 2 × 2 design:

1. reaction roles from ORD labels versus chemically informed reaction-string assignment;
2. rare components mapped to `other` versus reactions containing them removed.

The published reference cells are 44%, 47%, 21%, and 24%, respectively. The primary replication
criterion, frozen before training, is absolute agreement within 1.0 percentage point for every cell
under the authors' released configuration. Wider seed variation will be reported, never hidden.

## What can already be reproduced

The lightweight audit package checks exact input overlap, full-record duplicates, missingness, and
output prevalence in any declared train/test split. Exact equality is intentionally narrower than
chemical similarity and is never presented as a complete leakage analysis.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[data,dev]'
python scripts/fetch_orderly.py
reaction-integrity \
  --train data/external/orderly_condition_train.parquet \
  --test data/external/orderly_condition_test.parquet \
  --output reports/local-split-audit.json
```

The downloaded Parquet files are checksum-verified and intentionally ignored by Git. Their exact
Figshare file IDs, byte sizes, MD5 checksums, DOI, version, and license are committed in
[`data/provenance.json`](data/provenance.json).

## Evidence boundaries

- The paper result is known, so this is a transparent reproduction—not a blinded preregistration.
- A lower score after chemical role reassignment shows that the earlier task was easier under the
  original representation. It does not establish intent, fraud, or universal model failure.
- Moving exact input collisions out of the test set prevents identity overlap; it does not eliminate
  scaffold, reaction-family, patent-family, or temporal similarity.
- The released v4 condition benchmark contains only the chemically informed variants. The full
  trusted-label contrast depends on the v3 supplementary data and the authors' pinned code.

## Repository map

| Path | Purpose |
| --- | --- |
| `docs/protocol.md` | Frozen hypotheses, endpoints, tolerances, and analysis order |
| `docs/source-audit.md` | Primary sources, provenance, licensing, and claim boundaries |
| `docs/research-report.md` | Living report that separates completed and pending evidence |
| `reports/v0.1-source-audit.json` | Machine-readable published reference registry |
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
