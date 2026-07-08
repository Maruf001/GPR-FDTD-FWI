# Experiment 890: Local 2D Source-Factor CPU Micro-Smoke Naming Refresh

Date: 2026-06-25

## Purpose

Refresh the reduced source-factor CPU micro-smoke command after run `179`
showed that the optimizer runner auto-prefixes experiment IDs.

This run starts from a duplicated version of the run `178` micro-smoke design
script, keeps the reduced workload, and changes the command naming contract so
`--run-name` omits a numeric prefix.

It does not execute the optimizer command, run the full CPU batch, use GPU,
transfer to field, run field FWI, or train neural networks.

## Output

```text
outputs/summary_tables/180_local_2d_source_factor_cpu_micro_smoke_naming_refresh
```

Key artifacts:

```text
commands/run_local_2d_source_factor_cpu_micro_smoke_naming_refresh.sh
data/local_2d_source_factor_cpu_micro_smoke_naming_refresh_command.csv
data/local_2d_source_factor_cpu_micro_smoke_naming_refresh_validation.csv
data/local_2d_source_factor_cpu_micro_smoke_naming_refresh_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_CPU_MICRO_SMOKE_NAMING_REFRESH.md
figures/local_2d_source_factor_cpu_micro_smoke_naming_refresh.png
scripts/run_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py
scripts/test_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source run:                              178_local_2d_source_factor_cpu_micro_smoke_design
correction run:                          179_local_2d_source_factor_cpu_smoke_partial_output_correction
source cap seconds:                      3600
source observed elapsed seconds at cap:  3666
predicted runner experiment ID:          1360
requested run name:                      local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
expected runner output name:             1360_local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
command count:                           1
micro validation pass:                   true
recommended cap seconds:                 300
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
single geometry offset:                  true
base objective only:                     true
revisit disabled:                        true
no numeric run-name prefix:              true
output collision:                        false
commands generated:                      true
commands executed:                       false
micro-smoke execution ready:             true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

The corrected command keeps:

```text
--target-indices 0
--x-offsets-mm=0
--z-offsets-mm=0
--radius-offsets-mm=0
--diagnostic-objective-variants base:1.0,7.0,0.3,none,none,0.0
--progress-every 1
--run-name local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
```

It removes the revisit phase and lets the runner create:

```text
outputs/experiments/1360_local_2d_source_factor_micro_max_amplitude_stress_time_shift_only_cpu
```

## Interpretation

Run `178` had the right workload reduction but inherited the numeric-prefix
mistake from run `175`. Run `180` fixes the naming contract without broadening
the workload. This prevents another `1360_1360_...` style output folder.

## Decision

Use the corrected run `180` command, not the run `178` command, for the next
bounded execution smoke. The execution cap should remain five minutes. The full
nine-command CPU batch, GPU work, field transfer, and source-robustness claims
remain blocked.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py
sha256: 88996a07f9484f11c24f84302fbca04b2cbc8b116705fd2d083200a7365ca4a1

test_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py
sha256: 017c4dd3b5de7e8f9fc13d312d50f8835dd59f78d848da00895efa2f41a8598e
```

Subsequent local 2D source-factor execution runs should start from a duplicated
run-specific script and preserve the numeric-free optimizer `--run-name`
contract.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_micro_smoke_naming_refresh.py
3 passed
```

Figure check:

```text
local_2d_source_factor_cpu_micro_smoke_naming_refresh.png
1420x738, dynamic range=255
```
