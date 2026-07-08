# BEM Experiment 364: Real-Pair Return Packet Acceptance Gate Validation Sensitivity

Date: 2026-06-29

## Purpose

Stress-test the run `363` acceptance-gate validator with controlled damaged
variants.

This run checks that the validator accepts the exact run `362` return-packet
acceptance gate and rejects damaged variants covering gate-count drift,
packet-presence promotion, gate-order drift, blocked-reason removal,
packet-row drift, action-count drift, downstream promotion, figure validation
drift, and script-snapshot drift.

It does not stage packet files, run BEM/FDTD comparison, run threshold
calibration, launch GPU work, transfer to field evidence, run field FWI, or
start 3D validation.

## Output

```text
outputs/bem_experiments/364_project_core_bem_real_pair_return_packet_acceptance_gate_validation_sensitivity
```

Key artifacts:

```text
data/project_core_bem_real_pair_return_packet_acceptance_gate_validation_sensitivity_scenario_rows.csv
data/project_core_bem_real_pair_return_packet_acceptance_gate_validation_sensitivity_summary.json
figures/project_core_bem_real_pair_return_packet_acceptance_gate_validation_sensitivity.png
docs/PROJECT_CORE_BEM_REAL_PAIR_RETURN_PACKET_ACCEPTANCE_GATE_VALIDATION_SENSITIVITY.md
scripts/
```

## Result

```text
scenarios:                         15
expected pass:                     1
observed pass:                     1
expected failures:                 14
observed failures:                 14
unexpected outcomes:               0
sensitivity ready:                 true
accepts exact run 362:             true
rejects damaged variants:          true
real packet files present:         false
ready for frequency extraction:    false
real comparison ready:             false
threshold calibration ready:       false
GPU work ready:                    false
field transfer ready:              false
3D validation ready:               false
```

## Interpretation

The run `363` validator accepts the exact run `362` acceptance gate and rejects
the damaged variants. The gate is now guarded as a future packet-return
acceptance artifact, but the real packet is still absent.

## Decision

Use runs `362-364` as the guarded BEM real-pair return-packet acceptance gate.
Real BEM/FDTD comparison and threshold calibration remain blocked until a
complete packet is present and passes this gate.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_return_packet_acceptance_gate_validation_sensitivity.py
3 passed
```

Python compile check:

```text
run_project_core_bem_real_pair_return_packet_acceptance_gate_validation_sensitivity.py: pass
tests/test_project_core_bem_real_pair_return_packet_acceptance_gate_validation_sensitivity.py: pass
```

Figure validation:

```text
3437x922, dynamic range=255
```
