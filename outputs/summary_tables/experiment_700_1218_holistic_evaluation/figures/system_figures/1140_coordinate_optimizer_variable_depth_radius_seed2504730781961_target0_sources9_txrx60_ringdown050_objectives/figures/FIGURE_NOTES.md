# Figure Notes

## 1. `coordinate_radius_decision_panel.png` - radius decision context

This is the primary figure for a coordinate-optimizer run. It shows the
selected radius next to the closest competing radius, the margin relative
to the moderate-confidence cutoff, and the objective-variant margins.
It is intended to answer three questions directly: which radius won, what
radius nearly won, and whether the decision clears the cutoff.

Markers in the first panel use filled circles for the selected radius,
open circles for the next distinct-radius candidate, and diamonds for
the next candidate that changes x/z geometry when such a competitor
exists.

## 2. `coordinate_confidence_margins.png` - legacy confidence margins

This figure shows the best-versus-next-radius objective gap for each
coordinate-search step and observed case. Larger bars mean the chosen
radius was more clearly separated from the next competing radius. Small
bars mean the radius is ambiguous even when the selected x/z location is
reasonable.

Bar colors encode the confidence label used by the reporting code:
`strong`, `moderate`, `weak`, or `ambiguous`. A weak row is not a
failure by itself; it means the result needs an interval, revisit, or
diagnostic check before the point radius should be trusted.

Rows in this run: 1 (moderate=1).

Weak update-case rows to inspect first: none.

Broad radius-ambiguity rows to inspect first: none.

## 3. `coordinate_objective_radius_candidates.png` - ranked radius candidates

This figure shows the top ranked candidate radii for each diagnostic
objective variant. The x-axis is candidate rank, marker color is the
candidate radius in millimeters, and the first three ranks are labeled
with radius and depth. Use it to see whether the objectives agree on
the same point radius or are split across nearby alternatives.

Top-candidate rows included: 72.

Objective variants below moderate cutoff: late, late_high.

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
delayed ringdown, additive Gaussian observed-data noise settings, a
common-scale pulse-plus-noise proxy, and a standardized seed fingerprint.
Inspect it when comparing seed-labelled runs so the source/noise condition is
visible before reading objective plots. Seed-only changes should move the
fingerprint while leaving the pulse shape and noise distribution unchanged.

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
