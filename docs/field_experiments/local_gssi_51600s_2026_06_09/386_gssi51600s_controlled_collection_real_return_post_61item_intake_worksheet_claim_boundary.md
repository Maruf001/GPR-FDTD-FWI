# Field Experiment 386: Post-Intake-Worksheet Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded real-return intake worksheet from runs `383-385` into the
field claim boundary.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/386_gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_claims.csv
data/gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary.png
```

## Result

```text
claims:                             22
guarded claims:                     18
blocked claims:                     4
intake worksheet ready:             true
intake worksheet sensitivity ready: true
worksheet rows:                     49
direct real-input rows:             33
generated follow-up rows:           16
blank completion cells:             294
completed intake rows:              0
measured-evidence rows:             0
packet requirements:                61
duplicate-path requirements:        12
collection-day intake form ready:   true
real packet files present:          false
controlled field evidence ready:    false
field FWI ready:                    false
field 3D/HPC ready:                 false
gpu priority:                       none
```

The new guarded claim records that the intake worksheet is structurally ready
and still blank. The four downstream field claims remain blocked.

## Decision

Use this as the current field claim boundary after the intake-worksheet block.
Measured evidence, provenance acceptance, archive acceptance, field FWI, GPU
work, and field 3D/HPC remain blocked.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_61item_intake_worksheet_claim_boundary.py
4 passed
```

Figure check:

```text
3941x910, dynamic range=255
```
