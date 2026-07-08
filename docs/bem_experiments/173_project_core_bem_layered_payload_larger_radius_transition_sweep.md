# BEM Experiment 173: Layered Payload Larger-Radius Transition Sweep

Date: 2026-06-28

## Purpose

Locate the radius boundary behind the remaining larger-radius failure from run
`172`.

The corrected extended ladder from run `172` showed that the low-contrast row
was repaired, but the larger-radius row still failed. This run sweeps target
radii from 25 mm to 35 mm using the same local CPU project-core FDTD/BEM adapter
path used by runs `169` and `171`.

This run does not compare against field data, launch GPU/HPC work, run 3D
validation, or run field FWI.

## Output

```text
outputs/bem_experiments/173_project_core_bem_layered_payload_larger_radius_transition_sweep
```

Key artifacts:

```text
data/project_core_bem_layered_payload_larger_radius_transition_cases.csv
data/project_core_bem_layered_payload_larger_radius_transition_all_scan_metrics.csv
data/project_core_bem_layered_payload_larger_radius_transition_leave_one_metrics.csv
data/project_core_bem_layered_payload_larger_radius_transition_worst_payload_arrays.npz
data/project_core_bem_layered_payload_larger_radius_transition_sweep_summary.json
figures/project_core_bem_layered_payload_larger_radius_transition_sweep.png
docs/PROJECT_CORE_BEM_LAYERED_PAYLOAD_LARGER_RADIUS_TRANSITION_SWEEP.md
scripts/run_project_core_bem_layered_payload_larger_radius_transition_sweep.py
scripts/test_project_core_bem_layered_payload_larger_radius_transition_sweep.py
```

## Result

```text
case count:                          5
passed cases:                        4
failed cases:                        1
acceptance L2 gate:                  0.75
max ready radius:                    0.0325 m
min failed radius:                   0.035 m
worst case:                          radius_35mm
worst leave-one L2:                  0.7745663063852277
larger-radius boundary identified:   true
larger-radius model repair ready:    true
layered contract refresh ready:      false
field transfer ready:                false
3D validation ready:                 false
GPU/HPC ready:                       false
```

| Case | Radius | Target cells | Best all-scan L2 | Best leave-one L2 | Ready |
| --- | ---: | ---: | ---: | ---: | --- |
| radius_25mm | 0.025 | 533 | 0.5236861579717635 | 0.6497571611891657 | true |
| radius_27p5mm | 0.0275 | 641 | 0.5207058098156682 | 0.6442395473420942 | true |
| radius_30mm | 0.03 | 753 | 0.5417081347234763 | 0.6861865511332141 | true |
| radius_32p5mm | 0.0325 | 877 | 0.548170993731047 | 0.7137722378850567 | true |
| radius_35mm | 0.035 | 1013 | 0.5723932793988704 | 0.7745663063852277 | false |

## Interpretation

The current layered payload adapter remains inside the `0.75` leave-one-scan
gate through a 32.5 mm target radius. It fails at 35 mm. The failure is
therefore a near-boundary larger-footprint problem, not a broad collapse across
the radius sweep.

The all-scan L2 values remain below the gate, while the leave-one-scan value
fails at 35 mm. That points to a generalization problem under larger target
support rather than a complete same-case fitting failure.

## Decision

Do not promote the extended layered payload ladder.

Use this boundary as the next repair target. The next BEM branch should test a
larger-radius support/modeling adjustment around the 35 mm case while keeping
project-core bridge promotion, field transfer, 3D validation, GPU/HPC, and field
FWI blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_layered_payload_corrected_ladder_synthesis.py
tests/test_project_core_bem_layered_payload_larger_radius_transition_sweep.py
7 passed
```

Python compile check:

```text
run_project_core_bem_layered_payload_larger_radius_transition_sweep.py: pass
tests/test_project_core_bem_layered_payload_larger_radius_transition_sweep.py: pass
```

Figure check:

```text
2914x755, dynamic range=255
```
