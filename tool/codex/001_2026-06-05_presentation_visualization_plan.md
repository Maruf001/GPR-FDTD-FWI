# Presentation Visualization Plan

Document number: 001

Date: 2026-06-05

Script: `tool/codex/presentation_visuals.py`

Output folder: `outputs/presentation_figures/2026_06_05_context_figures`

## Purpose

This plan documents a reusable presentation/context visualization layer for the
GPR-FDTD-FWI project. The new figures are meant to explain the experiment setup,
geometry, scan layout, campaign progression, and selected inversion behavior.
They do not replace the existing experiment-native diagnostic figures.

The script reads archived experiment summaries and CSV files only. It does not
run new FDTD simulations and does not modify any existing experiment folder.

## Existing Figures Found

Inspection of `outputs/experiments/**/figures` found 1,160 figure-related files:

| File type | Count | Notes |
| --- | ---: | --- |
| PNG | 724 | Main experiment diagnostics and result plots |
| GIF | 51 | Wavefield/comparison animations |
| Markdown notes | 385 | Mostly `FIGURE_NOTES.md` files |

Common existing experiment figure names include:

| Existing figure type | Count found | Interpretation |
| --- | ---: | --- |
| `coordinate_confidence_margins.png` | 155 | Per-run confidence and margin diagnostics |
| `source_profiled_radius_profile.png` | 87 | Radius objective profiles from source-profiled runs |
| `coordinate_confidence_aggregate.png` | 48 | Aggregate confidence summaries |
| `coordinate_ambiguity_widths.png` | 41 | Ambiguity interval summaries |
| `single_rebar_convergence.png` | 34 | Earlier single-rebar inversion convergence |
| `single_rebar_observed_bscan.png` | 34 | Earlier observed B-scan plots |
| `single_rebar_recovered_bscan.png` | 34 | Earlier recovered B-scan plots |
| `single_rebar_model_comparison.png` | 34 | Earlier model comparisons |
| `detection_overlay.png` | 31 | Detection-stage target overlays |
| `multi_rebar_local_geometry_radius_profiles.png` | 26 | Multi-rebar local-geometry radius profiles |
| `multi_rebar_objective_variant_radius_profiles.png` | 19 | Objective-variant comparisons |

Existing presentation-style folders were also found:

- `outputs/presentation_figures`
- `outputs/presentation_figures_v2`
- `outputs/presentation_figures_single_rebar`
- `outputs/presentation_figures_single_rebar_next`

Those existing outputs were left untouched. The new figures were written to a
dated subfolder so they can be distinguished from earlier presentation assets.

Existing reusable plotting utilities inspected:

- `visualization/plot_style.py`: validated figure saving and shared plotting helpers.
- `visualization/plot_bscan.py`: B-scan plotting for arrays shaped `(nt, n_scans)`.
- `visualization/plot_geometry.py`: material-model plotting.
- `visualization/plot_wavefield.py`: wavefield frame/animation helper.

## Source Meaning Confirmed

The word "source" in the recent experiment commands means one Tx/Rx scan
position, not an independent wavelet family and not a whole B-scan.

Evidence:

- `core/scan.py`: each scan position runs one forward simulation and stores one
  receiver trace in one B-scan column.
- `run_multi_rebar_common_radius_profile.py`: `build_scan_positions(...)`
  creates `(src_iz, src_ix, rec_iz, rec_ix)` tuples, and `simulate_bscan(...)`
  returns a `bscan` with shape `(cfg.NT, len(scan_positions))`.
- Recent summaries such as
  `outputs/experiments/440_multi_rebar_coupled_source_shape_seed55_compact_pass/data/multi_rebar_coordinate_optimizer_summary.json`
  record `sources = 5` and `scan_x_values_mm = [50, 146, 250, 346, 450]`.

Diagram interpretation:

- Draw Tx and Rx as a fixed-offset pair above the concrete surface.
- Move the pair along x.
- One pair position produces one A-scan.
- Stack A-scans side-by-side to form one B-scan.

## Campaign Selection

The new figures were selected around representative campaign endpoints rather
than every experiment.

| Campaign | Experiment range | Representative files used | Reason for visualization |
| --- | --- | --- | --- |
| Close-spacing acquisition design | ~270-305 | Exp 276 and 302 summaries/manifests | Explains close50 to close30 geometry and the role of 4-source offset selection |
| Tight close-spacing and noise boundary | ~311-418 | Exp 332, 409, 418 summaries | Explains close14 tangent geometry and the transition from clean to x-ambiguous under noise |
| Source-shape basis fitting | ~430-439 | Exps 432, 433, 434 objective candidate CSVs | Shows the dense candidate landscape and high-radius/depth ambiguity branches |
| Coupled source-shape coordinate optimizer | ~440-444 | Exps 440, 441, 443 state histories and summaries; exp 444 aggregate | Shows that the coupled coordinate branch reaches the exact target state, while confidence intervals remain part of reporting |

Campaigns not given a separate new visual:

- Experiment 420 material/source animation summary already has animation-related
  products, so the new layer does not duplicate those GIFs.
- Full B-scan residual comparisons for recent coordinate runs were not
  generated because the recent lightweight summaries do not archive observed and
  predicted B-scan arrays. Recreating them would require rerunning forward
  simulations, which is unnecessary for this presentation-context layer.

## Generated Figure Index

| Figure filename | Experiment / campaign | Figure type | What it shows | Source data/config | Existing or newly generated | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `outputs/presentation_figures/2026_06_05_context_figures/campaign_close_spacing/close_spacing_geometry_series.png` | Close-spacing campaign, ~270-418 | Engineering cross-section series | `close50`, `close40`, `close30`, `close28`, and `close14` variable-radius geometries | Confirmed from exp 276, 302, 332, and 409 `multi_rebar_coordinate_optimizer_summary.json` files | Newly generated | Uses true x/z/r values; close14 labels tangent 6+8=14 mm |
| `outputs/presentation_figures/2026_06_05_context_figures/common/tx_rx_offset_35_40_45_50mm_comparison.png` | Acquisition design campaigns | Tx/Rx layout schematic | Four common-offset cases: 35, 40, 45, and 50 mm | `run_multi_rebar_common_radius_profile.py`, `config.py`, and summaries from 302, 276, 332, 409 | Newly generated | Shows four source positions at Tx x = 50, 178, 314, 450 mm |
| `outputs/presentation_figures/2026_06_05_context_figures/common/source_scan_layout_ascan_bscan_explanation.png` | General acquisition setup | Source/A-scan/B-scan explanatory diagram | One source position becomes one A-scan; stacked A-scans become a B-scan | `core/scan.py`, `run_multi_rebar_common_radius_profile.py`, exp 440 scan positions | Newly generated | Uses stylized synthetic traces for explanation, not measured experiment traces |
| `outputs/presentation_figures/2026_06_05_context_figures/common/fdtd_fwi_local_geometry_pipeline.png` | General workflow | Pipeline diagram | Candidate parameters -> geometry builder -> GPU FDTD -> predicted B-scan -> objective -> confidence/update | `run_multi_rebar_coordinate_optimizer.py`, `run_multi_rebar_local_geometry_profile.py`, `gpu/fdtd_gpu_v2.py` | Newly generated | Clarifies that recent campaigns are deterministic candidate-grid searches, not neural-network training |
| `outputs/presentation_figures/2026_06_05_context_figures/exp418/exp418_close14_noise_boundary_context.png` | Exp 418 noise-boundary summary | Geometry plus boundary chart | close14 tangent geometry, 50 mm offset, clean/ambiguous boundary at ~19.642% RMS noise | `outputs/experiments/418_coordinate_confidence_close14_txrx50_noise_boundary_summary/data/noise_boundary_rows.csv` and `noise_boundary_summary.json` | Newly generated | Complements existing exp 418 cutoff-margin, x-width, and radius-margin plots |
| `outputs/presentation_figures/2026_06_05_context_figures/exp418/exp418_close14_geometry_context_v2.png` | Exp 418 noise-boundary summary | Standalone engineering cross-section | close14 tangent pair, local 50 mm Tx/Rx offset, surface, and rebar geometry key | Same exp 418 files plus confirmed geometry from linked summaries | Newly generated refined figure | Replaces the cramped geometry panel from the combined exp 418 context figure for presentation use |
| `outputs/presentation_figures/2026_06_05_context_figures/exp418/exp418_noise_boundary_cutoff_margin_v2.png` | Exp 418 noise-boundary summary | Standalone boundary chart | competitor margin to the ambiguity cutoff as noise increases above the clean endpoint | `noise_boundary_rows.csv` and `noise_boundary_summary.json` | Newly generated refined figure | Uses scaled y-axis units and delta-noise x-axis to avoid unreadable scientific offsets |
| `outputs/presentation_figures/2026_06_05_context_figures/exp418/exp418_noise_boundary_x_ambiguity_v2.png` | Exp 418 noise-boundary summary | Standalone ambiguity chart | reported x-ambiguity width changes from 0 mm to 1 mm while the best point remains correct | `noise_boundary_rows.csv` and `noise_boundary_summary.json` | Newly generated refined figure | Splits the ambiguity story from the geometry and cutoff-margin panels |
| `outputs/presentation_figures/2026_06_05_context_figures/exp432_434/source_shape_dense_candidate_landscape.png` | Exps 432-434 Stage 4C source-shape dense runs | Candidate landscape | Radius/depth candidate clouds for left, center, and right targets under source mismatch/noise | `multi_rebar_local_geometry_objective_candidates.csv` from exps 432, 433, 434 | Newly generated | Shows true radius/depth and top candidates; useful for explaining high-radius/depth ambiguity branches |
| `outputs/presentation_figures/2026_06_05_context_figures/exp440_444/coupled_coordinate_state_evolution.png` | Exps 440, 441, 443 and aggregate context 444 | Convergence/progress chart | Max x/z/r error and RMS geometry error versus coordinate step | `coordinate_state_history.csv` from exps 440, 441, 443 | Newly generated | Shows one-pass collapse to zero geometry error |
| `outputs/presentation_figures/2026_06_05_context_figures/exp440_444/coupled_coordinate_percent_error.png` | Exps 440, 441, 443 and aggregate context 444 | Percentage-error companion chart | Max x/z/r error and RMS normalized error versus coordinate step, expressed as percent relative to each target value | `coordinate_state_history.csv` from exps 440, 441, 443 | Newly generated refined figure | Complements the millimeter-error chart; radius errors are easier to interpret in percent because the radius target is only 6 mm |
| `outputs/presentation_figures/2026_06_05_context_figures/exp440_444/coupled_target_vs_recovered_final_states.png` | Exps 440, 441, 443 | Target-vs-recovered geometry overlay | Initial, truth, and final rebar geometry overlays | `multi_rebar_coordinate_optimizer_summary.json` from exps 440, 441, 443 | Newly generated | Final blue outline overlaps truth in all three runs |
| `outputs/presentation_figures/2026_06_05_context_figures/exp440_444/coupled_target_vs_recovered_final_states_v2.png` | Exps 440, 441, 443 | Refined target-vs-recovered geometry overlay | Same initial, truth, and final geometry overlays with explicit legend | `multi_rebar_coordinate_optimizer_summary.json` from exps 440, 441, 443 | Newly generated refined figure | Use this version for presentation; it explicitly labels dashed red, gray target, and blue final outlines |
| `outputs/presentation_figures/2026_06_05_context_figures/common/scan_path_5source_txrx20mm.gif` | Current 5-source source-shape setup | Animation | Tx/Rx pair stepping through five scan positions | `config.py` and exp 440 scan-position convention | Newly generated | Simple explanatory GIF; does not simulate wave propagation |

## Reusable Script Functions

`tool/codex/presentation_visuals.py` includes reusable functions for:

- Rebar geometry cross-sections: `_setup_geometry_axis(...)`, `_draw_rebars(...)`.
- Tx/Rx offset diagrams: `_draw_tx_rx_pair(...)`, `plot_tx_rx_offset_comparison(...)`.
- Source/A-scan/B-scan layout: `plot_source_scan_layout(...)`.
- Forward/inversion pipeline diagrams: `plot_inversion_pipeline(...)`.
- Noise-boundary context: `plot_noise_boundary_context(...)`.
- Split noise-boundary presentation charts:
  `plot_noise_boundary_geometry_v2(...)`,
  `plot_noise_boundary_cutoff_margin_v2(...)`, and
  `plot_noise_boundary_x_ambiguity_v2(...)`.
- Candidate landscape plots: `plot_source_shape_candidate_landscape(...)`.
- Coordinate-evolution plots: `plot_coupled_coordinate_evolution(...)`.
- Coordinate percentage-error plots:
  `plot_coupled_coordinate_percent_error(...)`.
- Target-vs-recovered overlays: `plot_coupled_target_vs_recovered(...)`.
- Refined target-vs-recovered overlays with explicit legends:
  `plot_coupled_target_vs_recovered_v2(...)`.
- Scan-path animation: `animate_scan_path(...)`.

To regenerate the selected figure set:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python tool/codex/presentation_visuals.py --all
```

To use a different output folder:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python tool/codex/presentation_visuals.py --all --output-root outputs/presentation_figures/my_new_context_set
```

## Validation

Validation commands run:

```bash
/home/lam001/miniforge3/envs/FNO/bin/python -m py_compile tool/codex/presentation_visuals.py
/home/lam001/miniforge3/envs/FNO/bin/python tool/codex/presentation_visuals.py --all
```

Image validation results:

- All generated PNG files have nonzero dynamic range and visible pixel variation.
- The generated GIF has 5 frames.
- The revised coupled geometry overlay was visually inspected after generation.

## Useful Figures Not Generated Yet

These are reasonable future additions, but were not generated in this pass:

| Potential figure | Why useful | Why not generated now |
| --- | --- | --- |
| Recent observed/predicted/residual B-scan comparisons for exps 440-443 | Would show waveform fit quality for coupled coordinate runs | Lightweight summaries do not archive the B-scan arrays; recreating them would require new forward simulations |
| Candidate trajectory animation over every trial | Could show optimizer search behavior | Candidate-grid sweeps are not temporal optimizer trajectories; only accepted coordinate states are meaningful as a sequence |
| Full noise/seed comparison across all campaigns | Could show repeatability over seeds and noise | Campaigns use different geometries, offsets, cases, and reporting fields; a single chart risks mixing unlike conditions |
| Four- or five-rebar structure diagrams | Useful if future campaigns add more targets | Recent confirmed campaign files in the inspected range focus on three-rebar geometries |
| Hardware/runtime presentation chart | Useful in a methods/results presentation | Already covered in prior written reports; this pass focused on physical/computational setup visuals |

## Notes For Future Extension

- Keep presentation figures separate from experiment-native figures.
- Prefer reading `multi_rebar_coordinate_optimizer_summary.json`,
  `multi_rebar_local_geometry_summary.json`, and CSV result files rather than
  parsing notebook prose.
- If new experiments archive B-scan arrays, add residual/B-scan comparison
  functions without rerunning FDTD.
- For future diagrams, use equal x/z scaling for physical cross-sections unless
  the figure is explicitly a schematic.
