# Experiment 840: Exact-Radius Detector Seed Repair Design

Date: 2026-06-18

## Purpose

Design truth-free geometric repairs for the three exact-radius detector seeds
that run `091` found to be overlapping.

This is a CPU geometry-only design step. It does not run FDTD, does not use
truth to choose a waveform winner, does not infer radii/materials, and does
not authorize broad GPU work or FWI.

## Output

```text
outputs/summary_tables/092_local_2d_detector_exact_radius_seed_repair_design
```

Key artifacts:

```text
data/local_2d_detector_exact_radius_seed_repair_design_rows.csv
data/local_2d_detector_exact_radius_seed_repair_design_gates.csv
data/local_2d_detector_exact_radius_seed_repair_design_summary.json
figures/local_2d_detector_exact_radius_seed_repair_design.png
figures/FIGURE_NOTES.md
```

## Result

```text
policy label:                         local_2d_detector_exact_radius_seed_repair_design_cpu_no_fwi
overlap-blocked cases:                 3
repair found:                          3
all overlap-blocked cases repairable:  true
max component shift:                   2.0 mm
minimum clearance after repair:        0.0 mm
repaired pilot subset ready:           true
broad GPU queue ready:                 false
detector-seeded FWI ready:             false
gpu priority:                          none
```

Repair rows:

| Case | Repair | Clearance after |
| --- | --- | ---: |
| `target2_close14|seed13|source_mismatch` | move middle x by `-2` mm | 1.232 mm |
| `target2_close14|seed21|nominal` | move middle x by `-2` mm | 0.000 mm |
| `target2_close14|seed34|nominal` | move middle x by `-2` mm | 0.866 mm |

## Interpretation

All three overlap-blocked close14 seeds have a simple truth-free repair inside
the same 2 mm coordinate scale used by the local pilot windows. The repair is
purely geometric: it creates physically admissible exact-radius starting
states, but it does not prove that the repaired seeds are waveform-optimal.

The next allowed work is still one-case-at-a-time fixed-radius pilots from
direct-ready or repaired seeds. Broad GPU campaigns, detector-inferred
radius/material claims, field transfer, and detector-seeded FWI remain blocked.

## Validation

```text
tests/test_local_2d_detector_exact_radius_seed_repair_design.py
2 passed
```

Figure validation:

```text
local_2d_detector_exact_radius_seed_repair_design.png: 1685x869,
nonwhite=0.1833, dynamic range=255
```
