# BEM Experiment 172: Layered Payload Corrected Ladder Synthesis

Date: 2026-06-28

## Purpose

Synthesize the corrected extended layered payload stress ladder after repairing
the low-contrast case.

Run `169` executed the original four-case extended ladder, but one row was
degenerate because it had zero target cells. Run `171` executed the repaired
low-contrast case. This run combines the three non-degenerate rows from run
`169` with the repaired low-contrast row from run `171`.

This run does not rerun FDTD or BEM solvers, compare against field data, launch
GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/172_project_core_bem_layered_payload_corrected_ladder_synthesis
```

Key artifacts:

```text
data/project_core_bem_layered_payload_corrected_ladder_cases.csv
data/project_core_bem_layered_payload_original_extended_cases.csv
data/project_core_bem_layered_payload_corrected_ladder_synthesis_summary.json
figures/project_core_bem_layered_payload_corrected_ladder_synthesis.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_CORRECTED_LADDER_SYNTHESIS.md
scripts/run_project_core_bem_layered_payload_corrected_ladder_synthesis.py
scripts/test_project_core_bem_layered_payload_corrected_ladder_synthesis.py
```

## Result

```text
corrected cases:                    4
original degenerate cases:          1
corrected zero-target-cell cases:   0
passed cases:                       3
failed cases:                       1
acceptance L2 gate:                 0.75
worst case:                         larger_radius_epsr9
worst leave-one L2:                 0.7745663063852277
extended layered stress ready:      false
larger-radius repair design ready:  true
field transfer ready:               false
3D validation ready:                false
GPU/HPC ready:                      false
```

| Case | Evidence source | Target cells | Best leave-one L2 | Ready |
| --- | --- | ---: | ---: | --- |
| shallow_z_epsr9 | run 169 | 526 | 0.678333487523724 | true |
| larger_radius_epsr9 | run 169 | 1013 | 0.7745663063852277 | false |
| low_contrast_epsr7p5 | run 171 | 533 | 0.6672239886633535 | true |
| high_interface_epsr12 | run 169 | 533 | 0.5738072739328918 | true |

## Interpretation

The low-contrast problem is resolved as a design artifact. The repaired
low-contrast case passes with real target cells.

The corrected ladder still fails because the larger-radius case remains above
the `0.75` leave-one-scan gate. The remaining issue is now localized: the
current layered payload adapter is stressed by the larger target footprint, not
by the low-contrast condition.

## Decision

Do not promote the extended layered payload ladder.

The next BEM branch should target the larger-radius failure. Keep project-core
bridge promotion, field transfer, 3D validation, GPU/HPC, and field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_low_contrast_repair_contract.py
tests/test_project_core_bem_layered_payload_low_contrast_repair_execution.py
tests/test_project_core_bem_layered_payload_corrected_ladder_synthesis.py
8 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_corrected_ladder_synthesis.py: pass
tests/test_project_core_bem_layered_payload_corrected_ladder_synthesis.py: pass
```

Figure check:

```text
2878x811, dynamic range=255
```
