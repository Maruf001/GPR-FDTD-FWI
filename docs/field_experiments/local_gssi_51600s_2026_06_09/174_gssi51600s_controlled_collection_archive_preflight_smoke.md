# Field Experiment 174: Controlled Collection Archive Preflight Smoke

Date: 2026-06-25

## Purpose

Create a synthetic archive that satisfies the run `171` archive layout and
prove the run `173` archive preflight can pass when every required directory,
real-file slot, and metadata artifact is present and nonempty.

This is the synthetic pass-case companion to the real pending-archive failure
from run `173`.

This run does not create measured field evidence, run DZT preprocessing, field
FWI, GPU/HPC work, or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/174_gssi51600s_controlled_collection_archive_preflight_smoke
```

Key artifacts:

```text
data/field_controlled_collection_archive_preflight_smoke.csv
data/field_controlled_collection_archive_preflight_smoke_summary.json
figures/field_controlled_collection_archive_preflight.png
docs/FIELD_COLLECTION_ARCHIVE_PREFLIGHT_SMOKE.md
synthetic_archive/
scripts/run_gssi_field_controlled_collection_archive_preflight_smoke.py
scripts/test_gssi_field_controlled_collection_archive_preflight_smoke.py
scripts/script_snapshot_manifest.json
```

## Result

```text
preflight checks:                   23
passed checks:                      23
failed checks:                      0
blocking findings:                  0
synthetic archive smoke pass:       true
synthetic smoke only:               true
archive ready for checksum/intake:  true
scientific field claim ready:       false
field FWI ready:                    false
GPU/HPC ready:                      false
```

## Interpretation

The archive-preflight logic is satisfiable: a complete synthetic archive shape
passes all 23 run `173` checks.

The real pending archive remains absent. This run is not measured field
evidence and does not unblock field FWI, heavy GPU work, field 3D/HPC, or
neural-network training.

## Decision

Keep run `173` as the real archive gate. Use run `174` only to show the gate
logic can pass when a complete archive exists.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_archive_preflight_smoke.py
2 passed
```

Compile check:

```text
run_gssi_field_controlled_collection_archive_preflight_smoke.py: pass
tests/test_gssi_field_controlled_collection_archive_preflight_smoke.py: pass
```

Figure check:

```text
1996x790, dynamic range=255
```
