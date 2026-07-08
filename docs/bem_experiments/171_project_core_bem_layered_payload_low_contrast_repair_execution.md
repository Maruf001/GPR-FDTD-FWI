# BEM Experiment 171: Layered Payload Low-Contrast Repair Execution

Date: 2026-06-28

## Purpose

Execute the repaired low-contrast layered payload case defined by run `170`.

Run `169` contained one degenerate low-contrast row with zero target cells. Run
`170` repaired the design by setting the target permittivity to `epsr=7.5` while
leaving the lower-halfspace at `epsr=6.0`. This run performs the actual local
CPU FDTD/BEM adapter comparison for that repaired case.

This run does not compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/171_project_core_bem_layered_payload_low_contrast_repair_execution
```

Key artifacts:

```text
data/project_core_bem_layered_payload_low_contrast_repair_case.csv
data/project_core_bem_layered_payload_low_contrast_repair_all_scan_metrics.csv
data/project_core_bem_layered_payload_low_contrast_repair_leave_one_metrics.csv
data/project_core_bem_layered_payload_low_contrast_repair_payload_arrays.npz
data/project_core_bem_layered_payload_low_contrast_repair_execution_summary.json
figures/project_core_bem_layered_payload_low_contrast_repair_execution.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LOW_CONTRAST_REPAIR_EXECUTION.md
scripts/run_project_core_bem_layered_payload_low_contrast_repair_execution.py
scripts/test_project_core_bem_layered_payload_low_contrast_repair_execution.py
```

## Result

```text
source contract ready:               true
case count:                          1
passed cases:                        1
failed cases:                        0
zero-target-cell cases:              0
target cells:                        533
best all-scan L2:                    0.5386121533458362
best leave-one-scan L2:              0.6672239886633535
acceptance L2 gate:                  0.75
repaired low-contrast ready:         true
extended ladder resynthesis ready:   true
extended layered stress ready:       false
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
```

| Case | target epsr | lower epsr | target cells | Best leave-one variant | Best leave-one L2 | Ready |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| low_contrast_epsr7p5 | 7.5 | 6.0 | 533 | product_no_div | 0.6672239886633535 | true |

## Interpretation

The degenerate low-contrast row from run `169` is now repaired. The corrected
case has a real target-cell set and passes the `0.75` leave-one-scan gate.

This result only repairs one row in the extended layered ladder. It does not
remove the larger-radius failure from run `169`, where the leave-one-scan L2 was
`0.7745663063852277`.

## Decision

Use run `171` as the corrected low-contrast evidence row in the next extended
layered ladder synthesis.

Keep broader layered-payload promotion, project-core bridge promotion, field
transfer, 3D validation, GPU/HPC, and field FWI blocked until the full corrected
ladder is synthesized and all gates pass.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_low_contrast_repair_contract.py
tests/test_project_core_bem_layered_payload_low_contrast_repair_execution.py
5 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_low_contrast_repair_execution.py: pass
tests/test_project_core_bem_layered_payload_low_contrast_repair_execution.py: pass
```

Figure check:

```text
2572x720, dynamic range=255
```
