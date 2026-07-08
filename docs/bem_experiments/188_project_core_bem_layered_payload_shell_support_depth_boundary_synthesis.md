# BEM Experiment 188: Shell-Support Depth Boundary Synthesis

Date: 2026-06-28

## Purpose

Synthesize the current shell-support contract boundary after the deeper-offset
failure from runs `186` and `187`.

Run `181` established an 11-case validated local 2D BEM/FDTD shell-support
contract. Runs `186` and `187` showed that the contract should not be widened
into a depth-robust 35 mm larger-radius rule. This run records that boundary in
one table.

This run does not rerun FDTD/BEM solvers, compare against field data, run 3D
validation, launch GPU/HPC work, or run field FWI.

## Output

```text
outputs/bem_experiments/188_project_core_bem_layered_payload_shell_support_depth_boundary_synthesis
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_support_depth_boundary_rows.csv
data/project_core_bem_layered_payload_shell_support_depth_boundary_synthesis_summary.json
figures/project_core_bem_layered_payload_shell_support_depth_boundary_synthesis.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_SUPPORT_DEPTH_BOUNDARY_SYNTHESIS.md
scripts/run_project_core_bem_layered_payload_shell_support_depth_boundary_synthesis.py
scripts/test_project_core_bem_layered_payload_shell_support_depth_boundary_synthesis.py
```

## Result

```text
validated contract cases:            11
validated contract ready:            true
sub-cell shell cases:                5
sub-cell shell passes:               4
sub-cell shell failures:             1
repair support modes:                9
repair ready supports:               0
known depth failure:                 z_plus_2p5mm
worst L2:                            0.7549628470028724
worst acceptance margin:             -0.004962847002872417
depth-robust shell rule ready:       false
contract boundary synthesis ready:   true
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
field FWI ready:                     false
```

## Interpretation

The current validated shell-support contract remains scoped. It is not a
depth-robust 35 mm larger-radius rule: the deeper +2.5 mm case fails, and
shell-thickness repair did not close it.

## Decision

Keep the 11-case run `181` contract as a scoped local 2D result, with an
explicit known depth-offset failure from runs `186`-`187`.

Do not widen the claim, transfer to field, launch 3D/GPU work, or promote to
synthetic `outputs/experiments` evidence from this BEM branch.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_shell_support_depth_boundary_synthesis.py
tests/test_project_core_bem_layered_payload_larger_radius_deeper_offset_shell_repair_sweep.py
5 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_support_depth_boundary_synthesis.py: pass
tests/test_project_core_bem_layered_payload_shell_support_depth_boundary_synthesis.py: pass
```

Figure check:

```text
2464x838, dynamic range=255
```
