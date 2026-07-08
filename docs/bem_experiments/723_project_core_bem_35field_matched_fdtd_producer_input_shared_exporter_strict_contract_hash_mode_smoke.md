# BEM Experiment 723: Shared Exporter Strict Contract-Hash Mode Smoke

Date: 2026-07-01

## Purpose

Smoke-test the strict contract-hash mode in the shared matched-FDTD input-bound
exporter.

Runs `717-722` showed that exact contract-hash enforcement is needed and that a
prototype guard closes the arbitrary-hash gap. This run moves that capability
into the shared exporter as an opt-in strict mode and tests it on synthetic
producer-input probes.

This is CPU-only exporter-interface smoke testing. It does not run FDTD, accept
live producer files, create real evidence, run a real BEM/FDTD comparison,
launch GPU/HPC work, transfer to field evidence, or promote 3D validation
claims.

## Output

```text
outputs/bem_experiments/723_project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke
```

Key artifacts:

```text
data/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_probe_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_cli_smoke_rows.csv
data/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke_summary.json
figures/project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke.png
scripts/script_snapshot_manifest.json
```

## Result

```text
strict mode available:                true
probe cases:                             8
default-mode pass cases:                 4
strict-mode pass cases:                  2
strict-mode fail cases:                  6
canonical hashes accepted:               2
arbitrary hashes rejected:               2
blank or non-hex hashes rejected:        4
CLI smoke cases:                         2
CLI unexpected return codes:             0
synthetic accepted files:                1
real evidence files:                     0
exporter execution ready:            false
real BEM/FDTD comparison ready:       false
GPU/HPC ready:                       false
```

## Interpretation

The shared exporter now supports opt-in exact contract-hash enforcement. In
strict mode, canonical contract hashes pass and arbitrary valid-looking hashes
fail. The accepted file in this run is synthetic and stays inside the run
output folder.

## Decision

Use strict mode for future real matched-FDTD producer input acceptance. Keep
real BEM/FDTD comparison blocked until live producer files exist and pass the
strict acceptance path.

## Validation

Focused tests:

```text
tests/test_project_core_bem_fdtd_35field_input_bound_return_exporter.py
tests/test_project_core_bem_35field_matched_fdtd_producer_input_shared_exporter_strict_contract_hash_mode_smoke.py
12 passed
```

Figure check:

```text
2284x847, dynamic range=255
```
