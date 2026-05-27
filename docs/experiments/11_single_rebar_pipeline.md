# Experiment 11: Single-Rebar Geometry Pipeline

## Goal

Build the simplest reliable inversion problem before returning to multiple
rebars: one circular rebar, three unknowns, and synthetic observed data from
the same forward model.

Unknown parameter vector:

```text
[x_center, z_center, radius]
```

All values are in meters internally and reported in millimeters by the CLI.

## Command

Quick local CPU run:

```bash
python run_single_rebar_inversion.py --sources 5 --max-evals 25
```

More complete local or DGX Spark run:

```bash
python run_single_rebar_inversion.py --backend auto --sources 15 --max-evals 120
```

Multi-frequency objective:

```bash
python run_single_rebar_inversion.py --frequencies-ghz 1.4,1.5,1.6 --sources 15
```

## Outputs

```text
outputs/single_rebar/
  data/single_rebar_results.npz
  data/single_rebar_summary.json
  figures/single_rebar_model_comparison.png
  figures/single_rebar_convergence.png
  figures/single_rebar_observed_bscan.png
  figures/single_rebar_recovered_bscan.png
```

## Frequency Plan

Start with a fixed 1.5 GHz source. A small multi-frequency objective
(for example 1.4, 1.5, 1.6 GHz) is useful once the single-frequency inversion
is stable because it can reduce geometry ambiguity and test robustness.

Do not start with a broad sweep. Each extra frequency multiplies the forward
simulation count, so it is better used as a second-stage validation knob.

## GPU Plan

The systematic path uses the CPU solver by default and the CPML-capable GPU
solver when requested with `--backend gpu-cpml` or `--backend auto` on a CUDA
machine. The older GPU solver without CPML should be treated as a benchmark
artifact, not the production scientific path.
