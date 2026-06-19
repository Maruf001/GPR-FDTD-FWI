#!/usr/bin/env bash
set -euo pipefail

# Matched close-spacing source3 probe queue.
# Run only if spacing-only causality is needed for the manuscript.
# Launch at most one optimizer seed at a time; keep GPU <=90% and RAM <=80%.

# close14_source3_txrx40 seed 13: existing
# skip existing: outputs/experiments/1348_coordinate_optimizer_close14_seed13_sources3_txrx40_objectives

# close14_source3_txrx40 seed 21: existing
# skip existing: outputs/experiments/1349_coordinate_optimizer_close14_seed21_sources3_txrx40_objectives

# close14_source3_txrx40 seed 34: existing
# skip existing: outputs/experiments/1350_coordinate_optimizer_close14_seed34_sources3_txrx40_objectives

# close50_source3_txrx45 seed 13: missing
conda run -n gpr-fdtd-fwi python run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml --grid-step-mm 1 --sources 3 --tx-rx-offset-mm 45 --frequency-ghz 1.5 --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300 --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6 --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1 --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5 --replication-cases 'noise10_seed13:1.0,0.0,1.0,0.1,13|source_mismatch_noise10_seed13:1.1,-50,1.1,0.1,13' --update-case-label source_mismatch_noise10_seed13 --source-frequency-scales 0.9,1.0,1.1 --source-time-shift-ps-values=-50,0,50 --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' --top-k 20 --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets --revisit-ambiguity-min-width-mm 0.2 --revisit-x-offsets-mm=-1:1:1 --revisit-z-offsets-mm=-2:2:1 --revisit-radius-step-mm 0.5 --progress-every 25 --run-name coordinate_optimizer_close50_seed13_sources3_txrx45_objectives

# close50_source3_txrx45 seed 21: missing
conda run -n gpr-fdtd-fwi python run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml --grid-step-mm 1 --sources 3 --tx-rx-offset-mm 45 --frequency-ghz 1.5 --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300 --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6 --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1 --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5 --replication-cases 'noise10_seed21:1.0,0.0,1.0,0.1,21|source_mismatch_noise10_seed21:1.1,-50,1.1,0.1,21' --update-case-label source_mismatch_noise10_seed21 --source-frequency-scales 0.9,1.0,1.1 --source-time-shift-ps-values=-50,0,50 --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' --top-k 20 --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets --revisit-ambiguity-min-width-mm 0.2 --revisit-x-offsets-mm=-1:1:1 --revisit-z-offsets-mm=-2:2:1 --revisit-radius-step-mm 0.5 --progress-every 25 --run-name coordinate_optimizer_close50_seed21_sources3_txrx45_objectives

# close50_source3_txrx45 seed 34: missing
conda run -n gpr-fdtd-fwi python run_multi_rebar_coordinate_optimizer.py --backend gpu-cpml --grid-step-mm 1 --sources 3 --tx-rx-offset-mm 45 --frequency-ghz 1.5 --true-x-values-mm 190,250,300 --true-z-values-mm 90,90,90 --truth-radius-values-mm 5,6,8 --initial-x-values-mm 190,250,300 --initial-z-values-mm 90,90,85 --initial-radius-values-mm 6,6,6 --target-indices 2 --passes 1 --x-offsets-mm=-2:2:1 --z-offsets-mm=0,5,10 --radius-offsets-mm=-1:2:0.5 --replication-cases 'noise10_seed34:1.0,0.0,1.0,0.1,34|source_mismatch_noise10_seed34:1.1,-50,1.1,0.1,34' --update-case-label source_mismatch_noise10_seed34 --source-frequency-scales 0.9,1.0,1.1 --source-time-shift-ps-values=-50,0,50 --diagnostic-objective-variants 'base:1.0,7.0,0.3,none,none,0.0|highband:1.0,7.0,0.3,1.1,3.4,0.15' --top-k 20 --revisit-weak-high-radius-targets --revisit-broad-radius-ambiguity-targets --revisit-ambiguity-min-width-mm 0.2 --revisit-x-offsets-mm=-1:1:1 --revisit-z-offsets-mm=-2:2:1 --revisit-radius-step-mm 0.5 --progress-every 25 --run-name coordinate_optimizer_close50_seed34_sources3_txrx45_objectives

# Aggregate after all three seeds exist for a family:
conda run -n gpr-fdtd-fwi python run_coordinate_confidence_aggregate.py outputs/experiments/*_coordinate_optimizer_close14_seed13_sources3_txrx40_objectives/data/multi_rebar_coordinate_optimizer_summary.json outputs/experiments/*_coordinate_optimizer_close14_seed21_sources3_txrx40_objectives/data/multi_rebar_coordinate_optimizer_summary.json outputs/experiments/*_coordinate_optimizer_close14_seed34_sources3_txrx40_objectives/data/multi_rebar_coordinate_optimizer_summary.json --run-name coordinate_confidence_close14_sources3_txrx40_matched_seed_replicates
conda run -n gpr-fdtd-fwi python run_coordinate_confidence_aggregate.py outputs/experiments/*_coordinate_optimizer_close50_seed13_sources3_txrx45_objectives/data/multi_rebar_coordinate_optimizer_summary.json outputs/experiments/*_coordinate_optimizer_close50_seed21_sources3_txrx45_objectives/data/multi_rebar_coordinate_optimizer_summary.json outputs/experiments/*_coordinate_optimizer_close50_seed34_sources3_txrx45_objectives/data/multi_rebar_coordinate_optimizer_summary.json --run-name coordinate_confidence_close50_sources3_txrx45_matched_seed_replicates
