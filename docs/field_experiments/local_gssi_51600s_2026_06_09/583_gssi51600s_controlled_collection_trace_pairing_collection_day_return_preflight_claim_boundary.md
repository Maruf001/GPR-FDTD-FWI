# Field Experiment 583: Collection-Day Return Preflight Claim Boundary

Date: 2026-07-01

## Purpose

Record the claim boundary after the controlled-collection return preflight block
from runs `580-582`.

This run separates what is guarded from what remains blocked. The return
requirements and preflight gate are guarded. Controlled field evidence,
parser/provenance promotion, field FWI, and field 3D/HPC remain blocked because
no real measured file has passed preflight.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/583_gssi51600s_controlled_collection_trace_pairing_collection_day_return_preflight_claim_boundary
```

## Result

```text
source preflight gate ready:      true
source validation ready:          true
source sensitivity ready:         true
claims:                           5
guarded claims:                   2
blocked claims:                   3
preflight items:                  33
metadata JSON items:              24
measured DZT items:               9
candidate files present:          0
preflight-passed items:           0
ready-to-stage items:             0
controlled field evidence ready:  false
field FWI ready:                  false
field 3D/HPC ready:               false
gpu priority:                     none
```

## Decision

Use run `583` to prevent the pre-return checklist from being cited as parser
evidence, provenance evidence, controlled field evidence, field FWI readiness,
or field 3D/HPC readiness.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_trace_pairing_collection_day_return_preflight_claim_boundary.py
3 passed
```

Figure check:

```text
3401x907, dynamic range=255
```
