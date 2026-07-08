# BEM Experiment 241: Half-Space Finite-Rebar FDTD Frequency Input Contract

Date: 2026-06-28

## Purpose

Define the FDTD-side time-trace input contract needed before future traces can
be extracted into the scalar BEM/FDTD comparison schema from run `235`.

Runs `238`-`240` guarded the BEM-side export. This run defines what the FDTD
side must provide next: target/background time traces, receiver keys, frequency
keys, time-zero references, amplitude references, and scalar projection
convention.

This is a CPU-only contract run. It does not run FDTD, extract frequency bins,
compare real paired files, implement full 3D Maxwell BEM, run inversion, launch
GPU/HPC work, run field FWI, or promote field transfer.

## Output

```text
outputs/bem_experiments/241_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract
```

Key artifacts:

```text
data/project_core_bem_halfspace_finite_rebar_fdtd_time_trace_schema.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_required_frequency_keys.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_required_receiver_keys.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_requirements.csv
data/project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract_summary.json
figures/project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract.png
docs/PROJECT_CORE_BEM_HALFSPACE_FINITE_REBAR_FDTD_FREQUENCY_INPUT_CONTRACT.md
scripts/script_snapshot_manifest.json
```

## Result

```text
time-trace schema columns:          13
receiver keys:                      13
frequency keys:                     9
requirements:                       10
ready / implementation / blocked:   6 / 2 / 2
FDTD extraction blockers:           3
input contract ready:               true
scalar projection convention ready: false
complex extractor ready:            false
paired trace files present:         false
FDTD frequency extraction ready:    false
real BEM/FDTD comparison ready:     false
3D validation ready:                false
field transfer ready:               false
GPU ready:                          false
field FWI ready:                    false
```

The contract-ready items are the source BEM export guard, time-trace schema,
target/background roles, receiver-key lock, frequency-key lock, and required
time-zero/amplitude references.

The extraction blockers are the scalar projection convention, complex frequency
extractor implementation, and missing paired target/background FDTD trace
files.

## Interpretation

The FDTD side now has an explicit input contract for the scalar comparison.
Future target/background time traces need 13 required columns, 13 receiver keys,
nine frequency keys for extraction, explicit time-zero and amplitude references,
and a scalar projection convention.

Frequency extraction remains blocked because the projection convention, complex
extractor, and paired trace files are not present.

## Decision

Use run `241` as the input contract for future FDTD frequency extraction. The
next BEM task can validate and stress-test this contract. FDTD frequency
extraction, real BEM/FDTD comparison, 3D validation, inversion, field transfer,
GPU/HPC readiness, and field FWI remain blocked.

## Validation

Focused tests:

```text
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract.py
5 passed
```

Compile check:

```text
run_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract.py: pass
tests/test_project_core_bem_halfspace_finite_rebar_fdtd_frequency_input_contract.py: pass
```

Figure check:

```text
2897x847, dynamic range=255
```
