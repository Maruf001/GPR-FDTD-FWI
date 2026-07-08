# Experiment 871: Local 2D Next-Experiment Design Matrix

Date: 2026-06-25

## Purpose

Reconcile the local 2D fixed-radius locking audit with the latest BEM and field
gates, then decide which local 2D-side branches are actually justified.

This is a CPU-only summary/design artifact. It does not run FDTD, GPU kernels,
field FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/136_local_2d_next_experiment_design_matrix
```

Key artifacts:

```text
data/local_2d_next_experiment_design_matrix.csv
data/local_2d_next_experiment_design_matrix_summary.json
figures/local_2d_next_experiment_design_matrix.png
docs/LOCAL_2D_NEXT_EXPERIMENT_DESIGN_MATRIX.md
```

## Result

```text
candidate branches:                  7
ready branches:                      3
blocked branches:                    3
design-needed branches:              1
presentation claim count:            37
new local 2D GPU ready:              false
broad GPU queue ready:               false
detector-seeded FWI ready:           false
field transfer ready:                false
field FWI ready:                     false
GPU work ready:                      false
```

The ready or usable branches are:

```text
paper claim-boundary refresh
BEM/FDTD paired-data import preflight
field controlled-collection execution checklist
```

The blocked local 2D branches are:

```text
fixed-radius broad GPU probe
detector-seeded FWI
field transfer from current 2D evidence
```

The only local 2D compute path is design-needed, not launch-ready:

```text
define a new synthetic 2D acquisition/source/material hypothesis before any
new FDTD/GPU work.
```

## Interpretation

The current local 2D branch is not compute-ready for another fixed-radius GPU
probe. The useful near-term work is report claim-boundary refresh, BEM/FDTD
import preflight, or real field collection.

## Decision

Do not launch a new local 2D GPU/FWI branch from the fixed-radius result. Use
the existing mechanism result in reporting, and require a new acquisition,
source, or material hypothesis before future 2D compute.

## Validation

Figure check:

```text
2464x880, dynamic range=255
```
