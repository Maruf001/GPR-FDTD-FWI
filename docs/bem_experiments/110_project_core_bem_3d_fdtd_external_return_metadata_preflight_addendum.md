# BEM Experiment 110: External Return Metadata Preflight Addendum

Date: 2026-06-27

## Purpose

Make the strict comparison metadata addendum from run `109` executable as a
BEM-side return gate.

Runs `106`-`108` showed that BEM/FDTD comparison is sensitive to mesh, source,
and receiver conventions. Run `109` converted those sensitivities into 13
strict metadata fields. This run applies those fields on top of the original
12-field return metadata ledger and checks whether the upgraded gate catches
old incomplete ledgers.

This run does not install real returned files, run 3D FDTD, run real BEM/FDTD
comparison, make a 3D validation claim, or launch GPU/HPC work.

## Output

```text
outputs/bem_experiments/110_project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum
```

Key artifacts:

```text
data/project_core_bem_3d_fdtd_external_return_metadata_combined_requirements.csv
data/project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum_rows.csv
data/project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum_scenarios.csv
data/project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum_summary.json
figures/project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum.png
docs/PROJECT_CORE_BEM_3D_FDTD_EXTERNAL_RETURN_METADATA_PREFLIGHT_ADDENDUM.md
scripts/run_project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum.py
scripts/test_project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum.py
scripts/script_snapshot_manifest.json
```

## Result

```text
original metadata fields:             12
strict addendum fields:               13
combined metadata fields:             25
scenario count:                       3
real pending return ready:            false
original-only synthetic ledger ready: false
complete addendum synthetic ready:    true
real BEM/FDTD comparison ready:       false
3D validation claim ready:            false
layered 3D GPR forward model ready:   false
field FWI ready:                      false
GPU/HPC ready:                        false
```

Scenario outcomes:

| Scenario | Checks | Passed | Failed | Blocking | Ready | Strict addendum detail |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| real_pending_return | 8 | 0 | 8 | 8 | false | missing=13, blocking_missing=12 |
| synthetic_original_only_ledger | 8 | 5 | 3 | 3 | false | missing=13, blocking_missing=12 |
| synthetic_complete_addendum_ledger | 8 | 8 | 0 | 0 | true | missing=0, blocking_missing=0 |

## Interpretation

The upgraded metadata preflight rejects the current missing real return. More
importantly, it also rejects a synthetic ledger that satisfies the older
12-field return metadata contract but omits the strict 13-field BEM comparison
addendum.

The gate passes only when the full 25-field ledger is present and exact strict
values match the BEM comparison contract.

## Decision

Use the run `110` addendum preflight before accepting any real external 3D FDTD
return for BEM comparison.

Keep real BEM/FDTD comparison, 3D validation, layered 3D GPR modeling, field
FWI, and GPU/HPC work blocked until real target/background returns pass this
upgraded metadata gate and the frequency-bin gates.

## Milestone Snapshot

This result-driven BEM milestone froze:

```text
run_project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum.py
sha256: c5d71e66c54943a13e302739fdd471172272b83f587451119c325134261ee70c

test_project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum.py
sha256: 5f6885ba5264d88e2099625c41cf2fa32f5cfb3e34439d9b95280c5293fab514
```

Subsequent related BEM return-gate experiments should start from a duplicated
run-specific script.

## Validation

Focused tests:

```text
tests/test_project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum.py
4 passed
```

Figure check:

```text
project_core_bem_3d_fdtd_external_return_metadata_preflight_addendum.png
2284x842, dynamic range=255
```
