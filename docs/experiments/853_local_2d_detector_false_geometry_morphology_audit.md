# Experiment 853: Local 2D Detector False-Geometry Morphology Audit

Date: 2026-06-18

## Purpose

Explain what the refreshed detector selector is choosing when it does not
choose the all-truth triple. Experiment `852` / summary table `108` showed
that the robust component-only selector keeps all 12 cases within the top 200
but has 0/12 top-1 all-truth cases. This audit compares each selected top
false x-geometry against a representative all-truth candidate triple from the
saved component-gate rows.

This is CPU-only synthesis over saved detector rows. It does not run FDTD,
FWI, detector scoring, GPU kernels, field FWI, 3D/HPC work, or neural-network
training.

## Output

```text
outputs/summary_tables/109_local_2d_detector_false_geometry_morphology_audit_post_refreshed_gap
```

Key artifacts:

```text
data/local_2d_detector_false_geometry_morphology_summary.json
data/local_2d_detector_false_geometry_morphology_cases.csv
data/local_2d_detector_false_geometry_morphology_branch_summary.csv
figures/local_2d_detector_false_geometry_morphology_audit.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_detector_false_geometry_morphology_audit_cpu_no_fwi
source gap policy label:               local_2d_detector_refreshed_selector_gap_audit_cpu_no_fwi
case count:                            12
truth reference available:             12 / 12
top-1 all-truth cases:                 0 / 12
top-50 all-truth cases:                10 / 12
top-200 all-truth cases:               12 / 12
positive false-over-truth gaps:        12 / 12
compressed-span cases:                 3 / 12
compressed-span fraction:              0.25
median selected/truth x-span ratio:    0.9961
min selected/truth x-span ratio:       0.6571
max selected/truth x-span ratio:       1.1888
median max assignment error:           14.0 mm
max assignment error:                  35.0 mm
dominant false geometry mode:          single_truth_only_target2
dominant missing targets:              target0,target1
ready for morphology claim:            true
ready for rank-gated selector claim:   true
ready for detector-seeded FWI:         false
gpu priority:                          none
```

Branch summary:

```text
target2_close14:
  top50 = 6/6, top200 = 6/6, compressed-span cases = 3/6,
  median selected/truth x-span ratio = 0.8427,
  median max assignment error = 19.25 mm,
  dominant false mode = single_truth_only_target2

target2_close50_linear29p5:
  top50 = 4/6, top200 = 6/6, compressed-span cases = 0/6,
  median selected/truth x-span ratio = 1.0262,
  median max assignment error = 10.0 mm,
  dominant false mode = single_truth_only_target2
```

## Interpretation

The top detector failures are structured false geometries rather than random
candidate mistakes. All 12 selected top rows beat the best all-truth row under
the selected feature, but every case still contains an all-truth triple within
the top 200.

The morphology differs by branch. The close14 cases often collapse or shift
the lateral span, while the close50 linear29p5 cases mostly preserve the x-span
but assign the wrong branch/target subset. This is useful for the paper because
it separates two claims:

```text
The detector can provide rank-gated candidate lists.
It cannot serve as an automatic inversion initializer because the top-ranked
false geometries are physically structured partial-branch alternatives.
```

This supports a detector ambiguity/morphology claim and still blocks
detector-seeded FWI.

## Validation

Focused test:

```text
tests/test_local_2d_detector_false_geometry_morphology_audit.py
5 passed
```

Figure validation:

```text
local_2d_detector_false_geometry_morphology_audit.png: 2739x1005,
nonwhite=0.3045, dynamic range=255
```
