# Field Experiment 338: Current 61-Item Field Claim Boundary

Date: 2026-06-29

## Purpose

Refresh the field claim boundary after the 61-item antenna-aware filesystem gap
audit, acceptance gate, and staging dependency plan.

This run does not stage measured files, run provenance acceptance, run archive
acceptance, promote controlled field evidence, run field FWI, launch GPU work,
or start field 3D/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/338_gssi51600s_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary_claim_rows.csv
data/gssi51600s_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary.png
scripts/script_snapshot_manifest.json
```

## Result

```text
claim boundary ready:               true
claims:                             15
guarded claims:                     11
blocked claims:                     4
gap audit sensitivity ready:        true
acceptance gate sensitivity ready:  true
staging sensitivity ready:          true
packet items required:              61
missing packet items:               61
missing measured DZT files:         9
metadata requirements:              36
antenna metadata addendum items:    4
missing checksum rows:              9
missing acceptance results:         7
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

## Interpretation

The field claim boundary now cites the current 61-item guarded evidence blocks:

| Claim row | Current supporting runs |
| --- | --- |
| Filesystem gap audit | 335-337 |
| Acceptance gate | 329-331 |
| Staging dependency plan | 332-334 |

The boundary is current, but this is not field evidence. The measured packet is
still absent, so provenance acceptance, archive acceptance, field FWI, GPU work,
and field 3D/HPC remain blocked.

## Decision

Use this run as the current field claim boundary. Do not promote field evidence
or run field FWI until the 61-item measured packet exists and passes the
refreshed acceptance gate.

## Validation

Focused source test:

```text
tests/test_gssi_field_controlled_collection_real_return_post_antenna_gap_gate_staging_claim_boundary.py
3 passed
```

Figure validation:

```text
3941x953, dynamic range=255
```
