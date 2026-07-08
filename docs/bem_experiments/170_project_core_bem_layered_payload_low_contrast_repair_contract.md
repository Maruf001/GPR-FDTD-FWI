# BEM Experiment 170: Layered Payload Low-Contrast Repair Contract

Date: 2026-06-28

## Purpose

Repair the degenerate low-contrast case discovered in run `169`.

Run `169` included a low-contrast layered stress case where the target
permittivity equaled the lower-halfspace permittivity. That produced zero target
cells, so the apparent pass for that row was not meaningful.

This run defines a corrected low-contrast case with nonzero contrast before any
solver execution.

This is a design-contract run. It does not rerun FDTD, rerun BEM, compare
against field data, launch GPU/HPC work, run 3D validation, or run field FWI.

## Output

```text
outputs/bem_experiments/170_project_core_bem_layered_payload_low_contrast_repair_contract
```

Key artifacts:

```text
data/project_core_bem_layered_payload_low_contrast_repair_case.csv
data/project_core_bem_layered_payload_low_contrast_repair_contract_summary.json
figures/project_core_bem_layered_payload_low_contrast_repair_contract.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LOW_CONTRAST_REPAIR_CONTRACT.md
scripts/run_project_core_bem_layered_payload_low_contrast_repair_contract.py
scripts/test_project_core_bem_layered_payload_low_contrast_repair_contract.py
```

## Result

```text
repaired cases:                     1
degenerate cases:                   0
minimum target cells:               533
minimum absolute epsr contrast:     1.5
acceptance L2 gate:                 0.75
ready for execution:                true
extended layered stress ready:      false
project-core bridge ready:          false
3D validation ready:                false
field FWI ready:                    false
GPU/HPC ready:                      false
```

The repaired case is:

| Case | lower epsr | target epsr | epsr contrast | target cells |
| --- | ---: | ---: | ---: | ---: |
| low_contrast_epsr7p5 | 6.0 | 7.5 | 1.5 | 533 |

## Interpretation

The run `169` low-contrast row is now traceable as a design bug rather than a
validated stress pass. The corrected case keeps the lower-halfspace material at
`epsr=6.0` and raises the target to `epsr=7.5`, producing a real nonzero target
cell set.

This does not repair the larger-radius failure from run `169`; it only removes
the degenerate low-contrast artifact so the extended layered ladder can be
re-evaluated honestly.

## Decision

Execute the repaired low-contrast case as the next BEM run before revising the
extended layered stress conclusion.

Keep project-core bridge promotion, 3D validation, field transfer, GPU/HPC, and
field FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_low_contrast_repair_contract.py
2 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_low_contrast_repair_contract.py: pass
tests/test_project_core_bem_layered_payload_low_contrast_repair_contract.py: pass
```

Figure check:

```text
2249x843, dynamic range=255
```
