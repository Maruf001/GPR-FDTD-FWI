# Figure Notes

## 1. `coordinate_confidence_margins.png` - coordinate-update radius confidence

This figure shows the best-versus-next-radius objective gap for each
coordinate-search step and observed case. Larger bars mean the chosen
radius was more clearly separated from the next competing radius. Small
bars mean the radius is ambiguous even when the selected x/z location is
reasonable.

Bar colors encode the confidence label used by the reporting code:
`strong`, `moderate`, `weak`, or `ambiguous`. A weak row is not a
failure by itself; it means the result needs an interval, revisit, or
diagnostic check before the point radius should be trusted.

Rows in this run: 1 (moderate=1). The row is target1 for
`source_mismatch_ringdown050_noise10_seed3524578`, and the bar corresponds to
a base objective radius margin of 5.523984e-04.

Weak update-case rows to inspect first: none.

Broad radius-ambiguity rows to inspect first: none.

Interpretation for this run: the confidence figure supports a clean target1
acceptance at 5 sources and Tx/Rx=60. The objective diagnostic CSV confirms
that all six objective variants rank the true target1 geometry first and clear
the 5.0e-4 working cutoff.

<!-- system_scene_geometry:start -->
## `system_scene_geometry.png` - experiment scene geometry

This figure is the system/context view for the experiment. It shows the
scaled x-z cross-section, concrete surface, transmitter/receiver (Tx/Rx)
aperture, true rebar locations, selected/final rebar locations, and target
highlight. Inspect it before the objective-margin plots to confirm which
physical scene the run tested.

Validation metadata for this figure is saved in `../data/system_scene_geometry_summary.json`.
<!-- system_scene_geometry:end -->

<!-- source_pulse_noise_context:start -->
## `source_pulse_noise_context.png` - source pulse and noise context

This figure shows the configured Ricker source pulse, source mismatch,
delayed ringdown, additive Gaussian observed-data noise settings, and a
normalized pulse-plus-noise proxy. Inspect it when comparing seed-labelled
runs so the source/noise condition is visible before reading objective plots.

Validation and source/noise metadata are saved in `../data/source_pulse_noise_context_summary.json`.
<!-- source_pulse_noise_context:end -->

<!-- geometric_wave_propagation:start -->
## `geometric_wave_propagation.gif` - geometric wave propagation animation

This GIF is a lightweight travel-time schematic. It shows the selected
transmitter/receiver (Tx/Rx) pair, an outgoing forward wavefront, approximate
rebar reflection fronts, target highlight, and echo arrival timing. It is meant
to explain propagation paths and reflections without running a new FDTD/FWI
simulation.

Validation and travel-time metadata are saved in `../data/geometric_wave_propagation_summary.json`.
<!-- geometric_wave_propagation:end -->

<!-- fdtd_wavefield_amplitude:start -->
## `fdtd_wavefield_amplitude.gif` - true FDTD wavefield amplitude animation

This GIF shows sparse Ez wavefield snapshots from one representative forward
FDTD simulation using the saved experiment geometry and source settings. The
Tx/Rx pair is selected from the run's acquisition list near the target rebar,
so it is a physical wavefield view for that scenario, not the earlier
straight-ray schematic. Observed-data noise is not injected into this field
animation because that noise is added after forward simulation to B-scans.

Validation, source settings, grid settings, and selected Tx/Rx metadata are
saved in `../data/fdtd_wavefield_amplitude_summary.json`.
<!-- fdtd_wavefield_amplitude:end -->
