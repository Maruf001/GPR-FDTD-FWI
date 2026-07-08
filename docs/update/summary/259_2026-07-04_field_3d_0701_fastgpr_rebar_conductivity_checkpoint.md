# 259 2026-07-04 Field 3D 0701 Fast-GPR Rebar-Scale Conductivity Checkpoint

## What Changed

- Extended `run_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py` with optional bounded conductivity parameters.
- Ran a rebar-scale conductivity-enabled candidate on the same aligned local 0701 field window.
- Regenerated the predictor scorecard so the current candidate includes conductivity.

## Key Artifacts

- Conductivity run: `outputs/validation_exp_on_field_data/3d_geometry_inventory/027_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer_rebar_scale_conductivity/`
- Updated scorecard: `outputs/validation_exp_on_field_data/3d_geometry_inventory/028_field_3d_0701_fastgpr_aligned_predictor_scorecard/`

## Key Numbers

Rebar-scale no-conductivity run `025`:

- best loss: `0.753234`
- best epsr: `4.063327`
- depth: `1.507816 m`
- diameter proxy: `30.0 mm`

Rebar-scale conductivity run `027`:

- best loss: `0.753158`
- loss gain vs no-conductivity rebar-scale run: `7.5817e-05`
- best epsr: `3.901583`
- background conductivity: `0.005568 S/m`
- anomaly conductivity: `0.050000 S/m`
- depth: `1.507817 m`
- diameter proxy: `30.0 mm`
- mean runtime: `0.210 s/iter`

Updated consolidated candidate from scorecard `028`:

- x: `9.665786 m`
- cover/depth z: `1.507821 m`
- epsr: Fast-GPR conductivity candidate `3.901583`, analytic event `3.830539`
- background conductivity: `0.005568 S/m`
- anomaly conductivity: `0.050000 S/m`
- supported diameter range: `8-30 mm`
- supported length-y range: `0.095178-0.191499 m`
- source shift/polarity: `+1.8 ns`, polarity `-1`

## Current Decision

`field_3d_0701_predictor_candidate_ready_with_diameter_degeneracy_flag`

Adding conductivity improves the rebar-scale candidate slightly and gives a
material parameter estimate, but it does not remove the diameter degeneracy.
The broad smooth anomaly remains the best Fast-GPR normalized-L1 fit by only
`0.000087` over the conductivity-enabled rebar-scale candidate and `0.000163`
over the no-conductivity rebar-scale candidate.

## Claim Boundary

The current predictor candidate is field-data based and optimizer based, but the
Fast-GPR geometry is still a Gaussian proxy, not a steel-cylinder FDTD model.
Conductivity is now parameterized, but its stability has not been validated
across neighboring windows/profiles.

## Next Defensible Task

Run the same aligned predictor over additional windows/profile subsets from the
0701 stack. A shippable predictor needs stability evidence: x/depth/epsr/sigma
should not be a single-window artifact.

## Validation

- `conda run -n gpr-fdtd-fwi python -m pytest tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py -q`
- Result: `14 passed`
- `conda run -n dev python -m pytest tests/test_field_3d_0701_fastgpr_local_window_time_polarity_ladder.py tests/test_field_3d_0701_fastgpr_local_window_aligned_scalar_epsr_optimizer.py tests/test_field_3d_0701_fastgpr_local_window_aligned_geometry_material_optimizer.py tests/test_field_3d_0701_fastgpr_aligned_predictor_scorecard.py -q`
- Result: `14 passed`
- `git diff --check` on the new/updated scripts, tests, and checkpoint docs
- Figure checks: scorecard and optimizer figures are nonblank PNGs.

## Marathon Status

The local field-data predictor marathon remains active; this is a checkpoint,
not a stop.
