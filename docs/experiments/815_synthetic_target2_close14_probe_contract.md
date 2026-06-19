# Experiment 815: Synthetic Target2 Close14 Probe Contract

Date: 2026-06-18

## Purpose

CPU-only contract for the only currently defensible synthetic GPU follow-up:
target2, close14, source5, Tx/Rx=45 mm, fixed noise fraction
0.15361328125, and skip-existing seed reuse.

This run does not launch FDTD, FWI, GPU kernels, or a new optimizer experiment.
It only records the exact seed commands, existing-output status, aggregation
command, resource policy, and manuscript decision rule.

## Output

```text
outputs/experiments/1293_synthetic_target2_close14_probe_contract
```

Artifacts:

```text
data/synthetic_target2_close14_probe_contract_rows.csv
data/synthetic_target2_close14_probe_contract_summary.json
data/synthetic_target2_close14_probe_contract_commands.sh
data/figure_validation.csv
figures/synthetic_target2_close14_probe_contract.png
run_manifest.json
```

## Result

Policy label:

```text
target2_close14_source5_txrx45_probe_contract_skip_existing_cpu_no_gpu
```

Summary:

```text
contract status:                 ready_but_not_launched
probe target:                    target2_close14_source5_txrx45
seed count:                      3
existing seeds:                  34
missing seeds:                   13,21
source5 Tx/Rx45 near ties 0.5x:  2
source5 Tx/Rx45 near ties 1.0x:  2
next question:                   target2_close14_source5_threshold_gate
gpu priority:                    low_conditional_not_launched
```

Seed34 already exists at:

```text
outputs/experiments/354_coordinate_optimizer_close14_seed34_sources5_txrx45_noise15p361328125_objectives
```

The generated command file leaves seed34 commented as existing and includes
only seeds 13 and 21 as missing launch commands. It also includes the aggregate
command to run after those missing summaries exist.

## Decision Rule

After missing seeds are run and aggregated, evaluate target2 close14
source5/TxRx45 x near ties at fixed threshold scales 0.5 and 1.0.

If near ties persist across multiple seeds at 0.5x, report a robust
objective-uniqueness limitation. If they disappear outside seed34, report a
seed-specific caveat. Do not broaden this into a source-count, Tx/Rx, target,
or geometry sweep without a new CPU-side question.

Resource policy for any later launch:

```text
Run at most one missing seed at a time; keep GPU <=90% and RAM <=80%.
```

## Validation

Focused tests:

```text
tests/test_synthetic_target2_close14_probe_contract.py: 5 passed
```

Figure validation:

```text
synthetic_target2_close14_probe_contract.png: 2195x835,
nonwhite=0.3633, dynamic range=255
```
