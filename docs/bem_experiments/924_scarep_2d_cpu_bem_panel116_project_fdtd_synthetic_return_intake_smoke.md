# BEM Experiment 924: Panel-116 Synthetic Return Intake Smoke

Date: 2026-07-01

## Purpose

Exercise the panel-116 FDTD return intake path with a complete synthetic
non-evidence return file.

This run fills all 325 receiver-frequency rows with deterministic synthetic
complex values and synthetic solver provenance. The purpose is to test the
intake mechanics, not to create FDTD evidence.

This is a CPU-only schema-smoke run. It does not execute FDTD, accept a real
return, complete a BEM/FDTD comparison, transfer to field evidence, or start
3D/HPC work.

## Output

```text
outputs/bem_experiments/924_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke
```

## Result

```text
source intake ready:                   true
source intake validation ready:        true
source intake sensitivity ready:       true
smoke gates:                           6
passed smoke gates:                    6
failed smoke gates:                    0
receiver-frequency rows:               325
complex FDTD value rows:               325
solver provenance rows:                325
synthetic return rows:                 325
real evidence rows:                    0
schema smoke passed:                   true
real return accepted:                  false
project FDTD execution authorized:     false
project FDTD executed now:             false
project FDTD comparison completed:     false
field transfer ready:                  false
real 3D validation ready:              false
gpu priority:                          none
```

The six smoke gates all pass:

```text
row identity complete
complex values complete
solver provenance complete
synthetic label complete
real evidence absent
real acceptance blocked
```

## Interpretation

The intake consumer can handle a fully populated 325-row return-shaped file.
The synthetic file has complete complex values and provenance-like hashes, but
it is explicitly labeled synthetic and contains zero real evidence rows.

This means the schema mechanics are usable. It does not mean that the BEM/FDTD
comparison has been completed.

## Decision

Use this as a schema smoke only. A real BEM/FDTD comparison still requires a
real FDTD return that passes the same row identity, complex-value, and solver
provenance requirements.

## Validation

Focused tests:

```text
tests/test_scarep_2d_cpu_bem_panel116_project_fdtd_synthetic_return_intake_smoke.py
4 passed
```

Figure check:

```text
3311x879, dynamic range=255
```
