# Source and provenance audit

## Primary publication

Wigh, Arrowsmith, Pomberger, Felton, and Lapkin (2024), *Journal of Chemical Information and
Modeling* 64(9), 3790–3798, DOI `10.1021/acs.jcim.4c00292`. The paper describes ORDerly, its
cleaning pipeline, condition benchmark, baseline, neural model, and the reported performance gap.

## Data identities

The public benchmark is Figshare article `23298467`, version 4, DOI
`10.6084/m9.figshare.23298467.v4`, posted 2024-02-05 under CC BY 4.0. The complete article is
1,950,044,337 bytes. This study initially downloads only:

| File | File ID | Bytes | MD5 |
| --- | ---: | ---: | --- |
| `orderly_condition_train.parquet` | 44413052 | 356,912,241 | `bbe9ab181ef8ff2bbe5bf31d4b2d6190` |
| `orderly_condition_test.parquet` | 44413040 | 37,584,777 | `8951deb64a746d7ff20e9cea12a96910` |

These v4 files use reaction-string role assignment. The trusted-label variants required for the
full 2 × 2 reproduction are in Figshare supplement `23502372`, version 3, DOI
`10.6084/m9.figshare.23502372.v3`. Its condition archive is file `44412797`, 1,463,558,231 bytes,
MD5 `4a99b6e3678e4ac312678e26fd3caec2`.

## Cleaning-log verification

The official `orderly_no_trust_no_map_clean.log` records:

- 1,771,032 initial rows;
- 1,279,207 after component-count limits;
- 1,261,701 after required reactant/product checks;
- 753,338 after exact condition-record deduplication;
- 691,142 after removing components with frequency below 100;
- 3,541 candidate test rows moved into training, 5.3101% of the initial test allocation.

These are transcribed upstream log values, not independent recomputation. The machine-readable
registry marks that distinction explicitly.

## Supporting and limiting literature

- Schwaller et al. (2021), DOI `10.1038/s42256-021-00338-1`, documents structural bias and warns
  that random reaction splits may misrepresent generalization.
- Guo et al. (2025), DOI `10.1021/acscentsci.5c00055`, reports lower product-prediction accuracy on
  author-based and harder chemistry splits than on ordinary reaction splits.
- These studies support investigating split realism. They do not independently validate ORDerly's
  exact role-assignment result, which must be reproduced on its own terms.

