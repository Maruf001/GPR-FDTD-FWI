# Field Experiment 124: GSSI 51600S Short-Anchor Waveform-Coherence Audit

Date: 2026-06-18

## Purpose

Audit whether the two content-backed short-profile anchors support
waveform-morphology QC after the relative timing correction, while keeping
geometry, radius, cover-depth, field FWI, 3D/HPC, and absolute time-zero claims
separate.

This was a CPU saved-artifact audit. It read existing field waveform panel,
field-trace alignment, leave-one, spatial-consistency, and inversion-readiness
tables. It did not run DZT preprocessing, FDTD, FWI, GPU kernels, 3D/HPC jobs,
or neural-network training.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/124_gssi51600s_field_short_anchor_waveform_coherence_audit
```

Key artifacts:

```text
data/field_short_anchor_waveform_coherence_rows.csv
data/field_short_anchor_waveform_coherence_gates.csv
data/field_short_anchor_waveform_coherence_summary.json
figures/field_short_anchor_waveform_coherence_audit.png
```

## Result

```text
policy label:                         gssi51600s_field_short_anchor_waveform_coherence_qc_only
content-backed pairs:                 2
waveform-coherent pairs:              2 / 2
min corrected field-trace correlation: 0.939469
mean corrected field-trace correlation: 0.963803
min event-local field-trace correlation: 0.988138
min correlation improvement:          0.585637
max corrected timing residual:        0.019646 ns
min panel absolute correlation:       0.819494
radius-match pairs:                   0 / 2
content spatial residual range:       29.997 mm
single spatial translation supported: false
leave-one content-anchor claim ready: false
ready for waveform morphology QC:     true
ready for relative timing QC:         true
ready for geometry seed:              false
ready for radius recovery:            false
ready for field FWI:                  false
ready for 3D/HPC:                     false
gpu priority:                         none
```

Gate summary:

```text
waveform_morphology_qc: true
relative_timing_qc:     true
geometry_seed:          false
radius_recovery:        false
field_fwi:              false
```

Interpretation: the two content-backed short anchors are waveform-coherent
after the relative timing correction, so they support a measured-field
waveform-morphology QC claim. They do not support a geometry/radius seed or
field inversion launch because the paired radius choices disagree, the short
anchors do not support one spatial translation, and leave-one-content
redundancy is absent.

## Validation

```text
tests/test_gssi_field_short_anchor_waveform_coherence_audit.py
2 passed
```

Figure validation:

```text
field_short_anchor_waveform_coherence_audit.png: 2263x835,
nonwhite=0.3725, dynamic range=255
```
