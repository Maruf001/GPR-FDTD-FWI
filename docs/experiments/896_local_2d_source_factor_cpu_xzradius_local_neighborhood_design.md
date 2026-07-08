# Experiment 896: Local 2D Source-Factor CPU X/Z/Radius Local-Neighborhood Design

Date: 2026-06-25

## Purpose

Design a depth-aware bounded CPU smoke after the x/radius mini run `185`
selected x `189.0` mm and radius `5.0` mm with strong radius margins.

This run starts from a duplicated run-specific design script and adds one z
competitor. It keeps the same target, source-factor family, CPU backend,
no-fit-amplitude setting, base objective, no revisit phase, and numeric-free
`--run-name`.

It does not execute the optimizer command, run the full nine-command batch, use
GPU, transfer to field, run field FWI, or train neural networks.

## Output

```text
outputs/summary_tables/187_local_2d_source_factor_cpu_xzradius_local_neighborhood_design
```

Key artifacts:

```text
commands/run_local_2d_source_factor_cpu_xzradius_local_neighborhood.sh
data/local_2d_source_factor_cpu_xzradius_local_neighborhood_command.csv
data/local_2d_source_factor_cpu_xzradius_local_neighborhood_validation.csv
data/local_2d_source_factor_cpu_xzradius_local_neighborhood_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_CPU_XZRADIUS_LOCAL_NEIGHBORHOOD_DESIGN.md
figures/local_2d_source_factor_cpu_xzradius_local_neighborhood_design.png
scripts/run_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py
scripts/test_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source command run:                      184_local_2d_source_factor_cpu_xradius_mini_neighborhood_design
source execution run:                    185_local_2d_source_factor_cpu_xradius_mini_execution_audit
source x/radius elapsed seconds:         426.060
source x/radius usable:                  true
predicted runner experiment ID:          1363
requested run name:                      local_2d_source_factor_xzradiuslocal_max_amplitude_stress_time_shift_only_cpu
expected runner output name:             1363_local_2d_source_factor_xzradiuslocal_max_amplitude_stress_time_shift_only_cpu
expected candidate count per case:       8
design validation pass:                  true
recommended cap seconds:                 3600
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
two x candidates:                        true
two z candidates:                        true
two radius candidates:                   true
base objective only:                     true
revisit disabled:                        true
no numeric run-name prefix:              true
output collision:                        false
commands generated:                      true
commands executed:                       false
x/z/radius local execution ready:        true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

The local-neighborhood command uses:

```text
--target-indices 0
--x-offsets-mm=0,1
--z-offsets-mm=0,5
--radius-offsets-mm=-1,0
--diagnostic-objective-variants base:1.0,7.0,0.3,none,none,0.0
--run-name local_2d_source_factor_xzradiuslocal_max_amplitude_stress_time_shift_only_cpu
```

## Interpretation

Run `185` was radius-aware but held z fixed at `85.0` mm. Run `187` adds z
`90.0` mm as a candidate for target `0`, which is the known true depth in this
synthetic setup. This is the smallest local-neighborhood completion before
replicating or broadening to other source-factor rows.

## Decision

Execute this x/z/radius local-neighborhood command as the next bounded CPU
smoke with a 3600-second cap. Do not run the full nine-command batch, GPU work,
or field transfer until this local depth-aware run completes and is audited.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py
sha256: eba4f241f5cc5acfc03fd2b7ce7e2fd9f5dd40f33bc707c58cd21c05728d0d2a

test_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py
sha256: 74880afbd8985084902bf5692975526251fc7a101233178c01a96887b8b4d598
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xzradius_local_neighborhood_design.py
3 passed
```

Figure check:

```text
local_2d_source_factor_cpu_xzradius_local_neighborhood_design.png
1420x738, dynamic range=255
```
