# Local 2D Field-176 Hypothesis Refresh

Date: 2026-06-25

## Scope

Refresh the local 2D hypothesis queue after the field run `176` real-archive
acceptance contract and the run `139` presentation evidence pack.

This is a CPU-only planning artifact. It does not run FDTD, GPU kernels, field
FWI, 3D/HPC work, or neural-network training.

## Output

```text
outputs/summary_tables/142_local_2d_new_hypothesis_candidate_pack_field176_refresh
```

Tracked experiment note:

```text
docs/experiments/873_local_2d_new_hypothesis_candidate_pack_field176_refresh.md
```

## Result

```text
hypothesis candidates:               7
run-next CPU candidates:             4
design-first candidates:             2
field-blocked candidates:            1
CPU-design-ready candidates:         6
CPU-adapter-ready candidates:        2
recommended next hypothesis:         matched_2d_bem_fdtd_dielectric_cylinder_adapter
new local 2D GPU ready:              false
broad GPU queue ready:               false
detector-seeded FWI ready:           false
field transfer ready:                false
field FWI ready:                     false
GPU work ready:                      false
field real archive acceptance ready: false
presentation claim count:            44
```

## Interpretation

The local 2D recommendation remains stable: the next best branch is a CPU-only
matched 2D BEM/FDTD dielectric-cylinder adapter. The changed part is the field
bridge. Field-to-2D prior replay is now explicitly blocked on run `176` real
archive acceptance, not merely on the older synthetic archive/checksum bridge.

## Decision

Start the next local 2D branch from a duplicated matched-adapter script and keep
it CPU-scoped. Do not launch a new GPU/FWI branch from the fixed-radius result,
and do not use field priors until the run `176` real archive acceptance
contract passes.

## Validation

Focused tests:

```text
tests/test_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
5 passed
```

Figure check:

```text
2637x954, dynamic range=255
```

Script snapshots:

```text
run_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
sha256=e4e523307d18932c304ff49fc9a0c2cda8a9614c1ce26d2d73b93f13d0269f03

test_local_2d_new_hypothesis_candidate_pack_field176_refresh.py
sha256=8b43582645b14980dad45eb55ff31f85cbcab32fbcebb2e71046957eb0fd51f4
```

## Next Marathon Branch

The marathon remains active. The next defensible work is to start the
recommended matched 2D BEM/FDTD adapter branch from a duplicated matched-adapter
script and keep it CPU-scoped.
