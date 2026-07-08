# Experiment 894: Local 2D Source-Factor CPU X/Radius Mini-Neighborhood Design

Date: 2026-06-25

## Purpose

Design the next bounded CPU smoke after the two-candidate x-only run `183`
completed and selected x `189.0` mm in both source cases.

This run starts from a duplicated run-specific design script and adds the
smallest radius-aware neighborhood: two x offsets and two radius offsets for
the same target, with z fixed. The command keeps CPU backend, no amplitude
fitting, the base objective, no revisit phase, and a numeric-free `--run-name`.

It does not execute the optimizer command, run the full nine-command batch, use
GPU, transfer to field, run field FWI, or train neural networks.

## Output

```text
outputs/summary_tables/184_local_2d_source_factor_cpu_xradius_mini_neighborhood_design
```

Key artifacts:

```text
commands/run_local_2d_source_factor_cpu_xradius_mini_neighborhood.sh
data/local_2d_source_factor_cpu_xradius_mini_neighborhood_command.csv
data/local_2d_source_factor_cpu_xradius_mini_neighborhood_validation.csv
data/local_2d_source_factor_cpu_xradius_mini_neighborhood_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_CPU_XRADIUS_MINI_NEIGHBORHOOD_DESIGN.md
figures/local_2d_source_factor_cpu_xradius_mini_neighborhood_design.png
scripts/run_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py
scripts/test_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source command run:                      182_local_2d_source_factor_cpu_two_candidate_neighborhood_design
source execution run:                    183_local_2d_source_factor_cpu_two_candidate_execution_audit
source two-candidate elapsed seconds:    319.838
source two-candidate usable:             true
predicted runner experiment ID:          1362
requested run name:                      local_2d_source_factor_xradiusmini_max_amplitude_stress_time_shift_only_cpu
expected runner output name:             1362_local_2d_source_factor_xradiusmini_max_amplitude_stress_time_shift_only_cpu
expected candidate count per case:       4
design validation pass:                  true
recommended cap seconds:                 1800
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
two x candidates:                        true
single z offset:                         true
two radius candidates:                   true
base objective only:                     true
revisit disabled:                        true
no numeric run-name prefix:              true
output collision:                        false
commands generated:                      true
commands executed:                       false
x/radius mini execution ready:           true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

The mini-neighborhood command uses:

```text
--target-indices 0
--x-offsets-mm=0,1
--z-offsets-mm=0
--radius-offsets-mm=-1,0
--diagnostic-objective-variants base:1.0,7.0,0.3,none,none,0.0
--run-name local_2d_source_factor_xradiusmini_max_amplitude_stress_time_shift_only_cpu
```

## Interpretation

Run `183` gave a useful x-ranking signal but radius was fixed. Run `184`
creates the smallest radius-aware follow-up by adding candidate radius `5.0`
mm alongside the current `6.0` mm candidate for target `0`, while keeping z
fixed and avoiding the full batch.

## Decision

Execute this x/radius mini-neighborhood command as the next bounded CPU smoke
with an 1800-second cap. Do not run the full nine-command batch, GPU work, or
field transfer until this radius-aware smoke completes and is audited.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py
sha256: de477a726152c3080bc68f0d9dc670acd7e8eff5ba4a47ab2cb9674b60122860

test_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py
sha256: f610caa33a294957a4a01fdb009a1ddb5b513ac37544d6baba1b2d1670e73fdf
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xradius_mini_neighborhood_design.py
3 passed
```

Figure check:

```text
local_2d_source_factor_cpu_xradius_mini_neighborhood_design.png
1420x738, dynamic range=255
```
