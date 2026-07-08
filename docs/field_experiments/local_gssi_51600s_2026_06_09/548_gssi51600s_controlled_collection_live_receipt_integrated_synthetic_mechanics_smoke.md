# Field Experiment 548: Integrated Synthetic Receipt Mechanics Smoke

Date: 2026-07-01

## Purpose

Exercise the integrated live-receipt mechanics with an output-local synthetic
positive control.

This run creates synthetic DZT and JSON files inside its own output folder. It
does not create live field evidence and does not promote receipt, parser,
provenance, archive, field FWI, or field 3D/HPC readiness.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/548_gssi51600s_controlled_collection_live_receipt_integrated_synthetic_mechanics_smoke
```

## Result

```text
synthetic DZT files:                 9
synthetic DZT signature passes:      9
synthetic metadata JSON files:       24
synthetic metadata schema passes:    24
synthetic metadata value fields:     96
synthetic blank values:              0
synthetic receipt items:             33
synthetic receipt item passes:       33
accepted live receipt items:         0
live files present:                  0
live receipt ready:                  false
field FWI ready:                     false
field 3D/HPC ready:                  false
```

## Interpretation

The integrated receipt mechanics accept a complete output-local synthetic
packet. This confirms the gate can pass correctly shaped inputs while still
refusing to treat synthetic files as live field evidence.

## Decision

Use this run as positive-control mechanics coverage only. Live receipt still
requires real external DZT and metadata files.

## Validation

Focused tests:

```text
tests/test_gssi_field_controlled_collection_live_receipt_integrated_synthetic_mechanics_smoke.py
3 passed
```

