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

# close50_source3_txrx45 seed 13: existing
# skip existing: outputs/experiments/1352_coordinate_optimizer_close50_seed13_sources3_txrx45_objectives

# close50_source3_txrx45 seed 21: existing
# skip existing: outputs/experiments/1353_coordinate_optimizer_close50_seed21_sources3_txrx45_objectives

# close50_source3_txrx45 seed 34: existing
# skip existing: outputs/experiments/1354_coordinate_optimizer_close50_seed34_sources3_txrx45_objectives

# Aggregate after all three seeds exist for a family:
conda run -n gpr-fdtd-fwi python run_coordinate_confidence_aggregate.py outputs/experiments/*_coordinate_optimizer_close14_seed13_sources3_txrx40_objectives/data/multi_rebar_coordinate_optimizer_summary.json outputs/experiments/*_coordinate_optimizer_close14_seed21_sources3_txrx40_objectives/data/multi_rebar_coordinate_optimizer_summary.json outputs/experiments/*_coordinate_optimizer_close14_seed34_sources3_txrx40_objectives/data/multi_rebar_coordinate_optimizer_summary.json --run-name coordinate_confidence_close14_sources3_txrx40_matched_seed_replicates
conda run -n gpr-fdtd-fwi python run_coordinate_confidence_aggregate.py outputs/experiments/*_coordinate_optimizer_close50_seed13_sources3_txrx45_objectives/data/multi_rebar_coordinate_optimizer_summary.json outputs/experiments/*_coordinate_optimizer_close50_seed21_sources3_txrx45_objectives/data/multi_rebar_coordinate_optimizer_summary.json outputs/experiments/*_coordinate_optimizer_close50_seed34_sources3_txrx45_objectives/data/multi_rebar_coordinate_optimizer_summary.json --run-name coordinate_confidence_close50_sources3_txrx45_matched_seed_replicates
