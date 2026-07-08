# Field Experiment 314: Real-Return Post-Intake Worksheet Claim Boundary

Date: 2026-06-29

## Purpose

Fold the guarded run `311-313` field intake worksheet block into the current
field claim boundary.

This run checks that the 57-item return-packet worksheet is recognized as a
validated non-evidence handoff artifact without promoting any measured-field,
provenance, archive, field FWI, GPU, or field 3D/HPC claim.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/314_gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary
```

Key artifacts:

```text
data/gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_claim_rows.csv
data/gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary_summary.json
figures/gssi51600s_controlled_collection_real_return_post_intake_worksheet_claim_boundary.png
scripts/
```

## Result

```text
base claim count:                  12
updated claim count:               13
guarded claims:                    9
blocked claims:                    4
field intake worksheet ready:      true
accepts exact run 311:             true
rejects damaged variants:          true
real packet files present:         false
missing packet items:              57
missing measured DZT files:        9
missing metadata requirements:     32
missing checksum rows:             9
missing acceptance-result files:   7
provenance acceptance ready:       false
archive acceptance ready:          false
controlled field evidence ready:   false
field FWI ready:                   false
field 3D/HPC ready:                false
gpu priority:                      none
```

## Interpretation

The field boundary now includes the intake worksheet as a guarded handoff
artifact. That is useful for collection-day logistics, but it is not measured
field evidence and it does not close the 57 missing packet items.

The current archive still cannot support provenance acceptance, archive
acceptance, controlled field evidence, field FWI, GPU work, or field 3D/HPC
until the measured packet is staged and passes the acceptance gate.

## Decision

Use run `314` as the current field claim boundary after the intake worksheet
block. Do not promote field evidence or run field FWI until the measured packet
passes the acceptance gate.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_real_return_post_intake_worksheet_claim_boundary.py
3 passed
```

Figure validation:

```text
3437x960, dynamic range=255
```
