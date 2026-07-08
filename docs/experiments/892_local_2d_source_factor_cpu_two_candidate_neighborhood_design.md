# Experiment 892: Local 2D Source-Factor CPU Two-Candidate Neighborhood Design

Date: 2026-06-25

## Purpose

Design the next bounded CPU smoke after the corrected one-candidate
micro-smoke completed in run `181`.

This run starts from a duplicated run-specific design script and widens only
one axis: target `0` now has two x candidates, `0` and `+1` mm. The command
keeps one z offset, one radius offset, the base objective, no revisit phase,
CPU backend, no amplitude fitting, and a numeric-free `--run-name`.

It does not execute the optimizer command, run the full nine-command batch, use
GPU, transfer to field, run field FWI, or train neural networks.

## Output

```text
outputs/summary_tables/182_local_2d_source_factor_cpu_two_candidate_neighborhood_design
```

Key artifacts:

```text
commands/run_local_2d_source_factor_cpu_two_candidate_neighborhood.sh
data/local_2d_source_factor_cpu_two_candidate_neighborhood_command.csv
data/local_2d_source_factor_cpu_two_candidate_neighborhood_validation.csv
data/local_2d_source_factor_cpu_two_candidate_neighborhood_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_CPU_TWO_CANDIDATE_NEIGHBORHOOD_DESIGN.md
figures/local_2d_source_factor_cpu_two_candidate_neighborhood_design.png
scripts/run_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py
scripts/test_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source command run:                      180_local_2d_source_factor_cpu_micro_smoke_naming_refresh
source execution run:                    181_local_2d_source_factor_cpu_micro_smoke_execution_audit
source micro elapsed seconds:            262.859
source micro candidate count:            1
source micro usable:                     true
predicted runner experiment ID:          1361
requested run name:                      local_2d_source_factor_twocandidate_max_amplitude_stress_time_shift_only_cpu
expected runner output name:             1361_local_2d_source_factor_twocandidate_max_amplitude_stress_time_shift_only_cpu
expected candidate count per case:       2
design validation pass:                  true
recommended cap seconds:                 900
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
two x candidates:                        true
single z offset:                         true
single radius offset:                    true
base objective only:                     true
revisit disabled:                        true
no numeric run-name prefix:              true
output collision:                        false
commands generated:                      true
commands executed:                       false
two-candidate execution ready:           true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

The widened command uses:

```text
--target-indices 0
--x-offsets-mm=0,1
--z-offsets-mm=0
--radius-offsets-mm=0
--diagnostic-objective-variants base:1.0,7.0,0.3,none,none,0.0
--run-name local_2d_source_factor_twocandidate_max_amplitude_stress_time_shift_only_cpu
```

## Interpretation

Run `181` validated command execution and output completeness, but its
one-candidate grid could not produce a ranking margin. Run `182` is the
smallest useful widening: two x candidates per case. It is still a smoke test,
not the full source-factor counterfactual batch.

## Decision

Execute this two-candidate command as the next bounded CPU smoke with a
900-second cap. Do not run the full nine-command batch, GPU work, or field
transfer until this small neighborhood run completes and is audited.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py
sha256: 762e4c1ea111cb9533d34072413b04fafa0a9d67ae10f76b7284ebafc30d0851

test_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py
sha256: 1d99def154d7ef4fdbb38c323f18349457f54c13994d06a3da9b98f38545f12e
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_two_candidate_neighborhood_design.py
3 passed
```

Figure check:

```text
local_2d_source_factor_cpu_two_candidate_neighborhood_design.png
1420x738, dynamic range=255
```
