# BEM Experiment 176: Layered Payload Shell-Repaired Ladder Synthesis

Date: 2026-06-28

## Purpose

Synthesize the corrected extended layered payload ladder after applying the
larger-radius shell-support repair.

Run `172` showed that the corrected ladder still failed at the 35 mm
larger-radius case. Run `175` found that an 11 mm outer-shell support closes
that 35 mm gate. This run replaces the failed full-volume larger-radius row
with the passing 11 mm shell-support row and checks the four-case ladder.

This run does not rerun FDTD or BEM solvers, compare against field data, launch
GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/176_project_core_bem_layered_payload_shell_repaired_ladder_synthesis
```

Key artifacts:

```text
data/project_core_bem_layered_payload_shell_repaired_ladder_cases.csv
data/project_core_bem_layered_payload_shell_repaired_ladder_synthesis_summary.json
figures/project_core_bem_layered_payload_shell_repaired_ladder_synthesis.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_SHELL_REPAIRED_LADDER_SYNTHESIS.md
scripts/run_project_core_bem_layered_payload_shell_repaired_ladder_synthesis.py
scripts/test_project_core_bem_layered_payload_shell_repaired_ladder_synthesis.py
```

## Result

```text
case count:                          4
passed cases:                        4
failed cases:                        0
acceptance L2 gate:                  0.75
worst case:                          larger_radius_epsr9
worst leave-one L2:                  0.7443538860706249
selected shell support:              outer_shell_11mm
shell-repaired ladder ready:         true
layered contract refresh ready:      true
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
```

| Case | Evidence source | Support mode | Shell thickness | Active cells | Best leave-one L2 | Ready |
| --- | --- | --- | ---: | ---: | ---: | --- |
| shallow_z_epsr9 | run 169 | volume_full | 0.0 | 526 | 0.678333487523724 | true |
| larger_radius_epsr9 | run 175 | outer_shell_11mm | 0.011 | 574 | 0.7443538860706249 | true |
| low_contrast_epsr7p5 | run 171 | volume_full | 0.0 | 533 | 0.6672239886633535 | true |
| high_interface_epsr12 | run 169 | volume_full | 0.0 | 533 | 0.5738072739328918 | true |

## Interpretation

The shell-support repair closes the corrected extended layered ladder. All four
stress rows pass the scoped leave-one-scan gate.

The result is still scoped. It supports a refreshed layered-payload contract for
these project-core 2D BEM/FDTD cases. It does not establish field transfer, 3D
validity, GPU/HPC readiness, or integration into the synthetic 2D FDTD
`outputs/experiments` track.

## Decision

Treat the shell-repaired extended layered payload ladder as ready for a tracked
layered-contract refresh.

Keep project-core bridge promotion beyond this scoped ladder, field transfer,
3D validation, GPU/HPC, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_larger_radius_refined_shell_support_audit.py
tests/test_project_core_bem_layered_payload_shell_repaired_ladder_synthesis.py
6 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_shell_repaired_ladder_synthesis.py: pass
tests/test_project_core_bem_layered_payload_shell_repaired_ladder_synthesis.py: pass
```

Figure check:

```text
2770x793, dynamic range=255
```
