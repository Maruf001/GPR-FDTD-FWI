# Experiment 889: Local 2D Source-Factor CPU Smoke Partial Output Correction

Date: 2026-06-25

## Purpose

Correct the capped CPU smoke audit after discovering that the optimizer runner
auto-prefixed the requested run name and did create a partial output folder.

This is an output-integrity correction. It does not promote the capped run to
evidence, run another optimizer command, use GPU, transfer to field, run field
FWI, or train neural networks.

## Output

```text
outputs/summary_tables/179_local_2d_source_factor_cpu_smoke_partial_output_correction
```

Key artifacts:

```text
data/local_2d_source_factor_cpu_smoke_partial_output_correction.csv
data/local_2d_source_factor_cpu_smoke_partial_output_correction_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_CPU_SMOKE_PARTIAL_OUTPUT_CORRECTION.md
figures/local_2d_source_factor_cpu_smoke_partial_output_correction.png
scripts/run_local_2d_source_factor_cpu_smoke_partial_output_correction.py
scripts/test_local_2d_source_factor_cpu_smoke_partial_output_correction.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source run:                              177_local_2d_source_factor_cpu_smoke_cap_audit
cap summary said output folder exists:   false
partial output exists:                   true
candidate CSV count:                     2
run manifest exists:                     false
summary JSON exists:                     false
confidence CSV exists:                   false
objective diagnostics CSV exists:        false
figure file count:                       0
complete optimizer output:               false
usable evidence ready:                   false
runner auto-prefix detected:             true
future run name should omit numeric ID:  true
micro command naming refresh needed:     true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

The partial folder is:

```text
outputs/experiments/1359_1359_local_2d_source_factor_max_amplitude_stress_time_shift_only_cpu
```

It contains two candidate CSVs only. It does not contain the optimizer manifest,
summary, confidence table, objective diagnostics, or figures required for
usable evidence.

## Interpretation

Run `177` correctly decided that the one-hour capped smoke did not produce
usable evidence, but its output-folder check looked for the non-prefixed path.
The actual runner behavior auto-prefixes the next experiment ID. Because the
run name already included `1359`, the partial folder became
`1359_1359_local_2d_source_factor_max_amplitude_stress_time_shift_only_cpu`.

The scientific decision is unchanged: the capped output is incomplete and must
not be used as source-factor evidence.

## Decision

Supersede the specific "no output folder" statement in run `177` with this
partial-output correction. Do not use the partial folder as evidence.

The next source-factor execution design must refresh the micro-smoke command so
`--run-name` omits a numeric prefix and lets the optimizer runner allocate the
experiment ID.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_smoke_partial_output_correction.py
sha256: c2474eb6c162ec7c44ae0ecef7088c0431b11df9f2bafc5299143019f953fa51

test_local_2d_source_factor_cpu_smoke_partial_output_correction.py
sha256: ccf48c8a4731e14b83b468d161a4fdf4e22834d79f8603143ce768eb3d633aae
```

Subsequent local 2D source-factor execution runs should start from a duplicated
run-specific script and should omit numeric prefixes from `--run-name`.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_smoke_partial_output_correction.py
2 passed
```

Figure check:

```text
local_2d_source_factor_cpu_smoke_partial_output_correction.png
1456x736, dynamic range=255
```
