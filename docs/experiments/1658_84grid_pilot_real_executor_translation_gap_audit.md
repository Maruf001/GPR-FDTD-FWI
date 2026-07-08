# Experiment 1658: 84-Grid Pilot Real-Executor Translation Gap Audit

Date: 2026-06-30

## Purpose

Clarify why the five-row 2D pilot cannot be executed yet, even though the
project already contains a CPU FDTD solver and an executed aggregate replay
route.

Run `1657` showed that a separate real executor script is missing. This run
goes one level deeper and checks whether each pilot row already has enough
information to be translated into concrete solver inputs.

This run does not execute FDTD, accept pilot evidence, launch GPU work, transfer
to field evidence, or promote 3D/HPC readiness.

## Output

```text
outputs/experiments/1658_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_translation_gap_audit
```

Key artifacts:

```text
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_translation_gap_audit_translation_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_translation_gap_audit_dependency_rows.csv
data/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_translation_gap_audit_summary.json
figures/local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_translation_gap_audit.png
scripts/script_snapshot_manifest.json
```

## Result

```text
source implementation audit ready:     true
pilot rows audited:                    5
standard objective profiles mapped:    4
retained_blend profiles:               1
transition bins audited:               5
direct payloads ready for execution:   0
dependencies checked:                  8
dependencies ready now:                5
blocking missing dependencies:         3
core CPU FDTD available:               true
low-level CPU probe route available:   true
transition-bin mapper available:       false
retained_blend definition available:   false
real executor script available:        false
new FDTD executed:                     false
GPU work ready:                        false
field transfer ready:                  false
3D/HPC ready:                          false
```

The four standard objective labels map to existing objective-variant strings:
`highband`, `late`, `late_high`, and `veryhigh`. The fifth pilot label,
`retained_blend`, is a policy/transition label and is not yet a concrete
objective variant.

Every pilot row remains blocked because the `transition_bin` values have not
yet been translated into explicit geometry, material, acquisition, and solver
inputs.

## Interpretation

The real-executor task is now more precise. It is not enough to duplicate the
guarded executor and call the solver. A translation layer is required first.

That layer must define:

1. how each pilot `transition_bin` maps to concrete model inputs,
2. whether `retained_blend` becomes a concrete objective or is removed from the
   executable pilot, and
3. how the resulting solver output fills the five accepted result JSON files.

## Decision

Build the translation layer before any five-row FDTD pilot execution. Keep the
pilot, full 84-row expansion, GPU work, field transfer, and 3D/HPC blocked
until that translation layer is validated.

## Validation

Focused tests:

```text
tests/test_local_2d_state_consistent_objective_revision_84grid_pilot_real_executor_translation_gap_audit.py
5 passed
```

Figure check:

```text
3293x895, dynamic range=255
```
