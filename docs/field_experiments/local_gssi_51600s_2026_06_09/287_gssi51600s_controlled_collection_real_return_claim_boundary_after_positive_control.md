# Field Experiment 287: Claim Boundary After Positive Control

Date: 2026-06-28

## Purpose

Synthesize the controlled field return claim boundary after the guarded
positive-control mechanics block.

This run separates three guarded statements from four blocked statements. The
guarded statements are that the collection-day critical path is defined, the
current real return inbox is still empty, and the private synthetic
positive-control scan works mechanically. The blocked statements are real
packet completion, provenance/archive acceptance, controlled field evidence or
field FWI, and field 3D/HPC or GPU escalation.

This uses saved artifacts only. It does not stage real measured field data,
modify the real return inbox, accept provenance, accept a real archive, run
field FWI, or launch GPU/HPC work.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/287_gssi51600s_controlled_collection_real_return_claim_boundary_after_positive_control
```

Key artifacts:

```text
data/field_controlled_collection_real_return_claim_boundary_after_positive_control_claim_rows.csv
data/field_controlled_collection_real_return_claim_boundary_after_positive_control_summary.json
figures/field_controlled_collection_real_return_claim_boundary_after_positive_control.png
scripts/script_snapshot_manifest.json
docs/FIELD_CONTROLLED_COLLECTION_REAL_RETURN_CLAIM_BOUNDARY_AFTER_POSITIVE_CONTROL.md
```

## Result

```text
claims:                                7
guarded claims:                        3
blocked claims:                        4
ready claims:                          3
measured requirements complete:        0 / 50
real files present:                    0 / 9
metadata values present:               0 / 32
checksums present:                     0 / 9
acceptance gates ready:                0 / 7
synthetic positive-control pass:       true
field claim boundary ready:            true
real measured data present:            false
provenance acceptance ready:           false
controlled field evidence ready:       false
field FWI ready:                       false
field 3D/HPC ready:                    false
gpu priority:                          none
```

## Interpretation

The field return process is mechanically guarded but still not
evidence-bearing. The critical path is guarded, the current real return inbox is
still empty, and the positive-control scanner works only on synthetic private
files. The current archive has zero completed measured requirements and zero
ready acceptance gates.

## Decision

Use run `287` as the field claim boundary after the positive control. Continue
to block provenance acceptance, real archive acceptance, controlled field
evidence, field FWI, field 3D/HPC, and GPU work until real measured DZT files,
measured metadata, and checksums are staged and validated.
