# BEM Experiment 362: Real-Pair Return Packet Acceptance Gate

Date: 2026-06-29

## Purpose

Convert the guarded BEM real-pair packet gap boundary from runs `359-361` into
a rerunnable acceptance gate for the eventual returned BEM/FDTD packet.

This run does not stage packet files, run BEM/FDTD comparison, run threshold
calibration, launch GPU work, transfer to field evidence, run field FWI, or
start 3D validation. It checks the current expected packet root against the
guarded packet contract and reports what must be present before execution can
start.

## Output

```text
outputs/bem_experiments/362_project_core_bem_real_pair_return_packet_acceptance_gate
```

Key artifacts:

```text
data/project_core_bem_real_pair_return_packet_acceptance_gate_packet_file_rows.csv
data/project_core_bem_real_pair_return_packet_acceptance_gate_action_rows.csv
data/project_core_bem_real_pair_return_packet_acceptance_gate_acceptance_gate_rows.csv
data/project_core_bem_real_pair_return_packet_acceptance_gate_summary.json
figures/project_core_bem_real_pair_return_packet_acceptance_gate.png
docs/PROJECT_CORE_BEM_REAL_PAIR_RETURN_PACKET_ACCEPTANCE_GATE.md
scripts/
```

## Result

```text
acceptance gates:                   8
ready gates:                        2
blocked gates:                      6
packet items:                       34
present packet items:               0
missing packet items:               34
missing projected traces:           26
missing metadata/control files:     8
required action groups:             4
open action groups:                 4
real packet files present:          false
ready for frequency extraction:     false
real BEM/FDTD comparison ready:     false
threshold calibration ready:        false
GPU work ready:                     false
field transfer ready:               false
3D validation ready:                false
```

The two ready gates are:

| Gate | Meaning |
| --- | --- |
| `guarded_source_contracts_available` | The upstream packet contract, staging plan, and gap claim boundary are guarded. |
| `expected_packet_inventory_known` | The expected 34-file packet inventory is known. |

The six blocked gates are data/execution gates. The packet currently has no
required files present.

## Interpretation

The BEM branch is ready to accept a returned packet, but it is not ready to run
the real comparison. The current blocker is concrete: 34 files are missing,
including 26 projected FDTD traces and eight metadata/control artifacts.

## Decision

Use run `362` as the rerunnable acceptance gate for future returned BEM/FDTD
packet files. Do not run real BEM/FDTD comparison, threshold calibration, GPU
work, field transfer, field FWI, or 3D validation until this gate passes.

## Validation

Focused test:

```text
tests/test_project_core_bem_real_pair_return_packet_acceptance_gate.py
3 passed
```

Python compile check:

```text
run_project_core_bem_real_pair_return_packet_acceptance_gate.py: pass
tests/test_project_core_bem_real_pair_return_packet_acceptance_gate.py: pass
```

Figure validation:

```text
3761x980, dynamic range=255
```
