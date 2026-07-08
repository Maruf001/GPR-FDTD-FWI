# BEM Experiment 811: Complex FDTD Adapter Input External Handoff Guard

Date: 2026-07-01

## Purpose

Guard the boundary between the output-local complex FDTD input template and the
real external filled-input path.

Runs `808-810` created and guarded the fill-in template. This run checks that
the template remains output-local and that the expected external filled-input
file is still absent.

## Output

```text
outputs/bem_experiments/811_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_guard
```

## Result

```text
source template ready:                     true
source validator ready:                    true
source sensitivity ready:                  true
handoff items:                             2
output-local template present:             true
output-local template rows:                279
template under external return root:       false
external input parent present:             true
external input file present:               false
external input rows:                       0
external input accepted:                   false
completed stage files ready:               false
real BEM/FDTD comparison ready:            false
field transfer ready:                      false
3D/HPC ready:                              false
gpu priority:                              none
```

Expected external filled-input path:

```text
outputs/bem_experiments/_external_fdtd_returns/project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input.csv
```

## Interpretation

The fill-in template and the real external input path are separate. The template
contains 279 row identities but remains a template. The external filled-input
file is absent, so completed comparison files cannot be written.

## Decision

Accept only a filled external input file at the guarded external path. Do not
treat the output-local template as real FDTD evidence.

## Validation

Focused tests:

```text
tests/test_project_core_bem_35field_matched_fdtd_complex_metric_fdtd_complex_adapter_input_external_handoff_guard.py

3 passed
```

Figure check:

```text
2681x878, dynamic range=255
```
