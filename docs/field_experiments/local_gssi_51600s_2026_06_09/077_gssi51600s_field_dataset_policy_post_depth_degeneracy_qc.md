# Field Experiment 077: Dataset Policy After Depth/Degeneracy QC

Date: 2026-06-18

## Purpose

Refresh the dataset-level GSSI 51600S policy after the apparent-depth QC,
apparent-depth sensitivity, and hyperbola/time-zero degeneracy audits. This is
a CPU-only synthesis of existing field outputs; it does not launch FDTD, FWI,
GPU kernels, 3D inversion, radius recovery, or cover-depth recovery.

Superseded endpoint note: field experiment 078 moved these guardrails into the
publication bundle, and field experiment 079 / runs 090-092 then added the
early-time common-mode negative-control audit. Run 092 is now the current
dataset policy pointer.

## Output

```text
087_gssi51600s_field_dataset_policy_synthesis_post_depth_degeneracy_qc
```

Key artifacts:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/087_gssi51600s_field_dataset_policy_synthesis_post_depth_degeneracy_qc/data/field_dataset_policy_evidence.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/087_gssi51600s_field_dataset_policy_synthesis_post_depth_degeneracy_qc/data/field_dataset_policy_summary.json
outputs/field_experiments/local_gssi_51600s_2026_06_09/087_gssi51600s_field_dataset_policy_synthesis_post_depth_degeneracy_qc/figures/field_dataset_policy.png
```

## Result

Policy label:

```text
field_2d_qc_not_3d_or_fwi
```

Depth/degen guardrail rows now included:

```text
evidence rows:                         31
apparent-depth QC policy:              field_apparent_depth_qc_relative_scale_not_cover_depth
apparent-depth max corrected residual: 4.908 mm
time-zero depth-equivalent budget:     5.890 mm
apparent-depth sensitivity policy:     field_apparent_depth_sensitivity_not_calibrated_cover_depth
max apparent-depth sensitivity factor: 2.18x
hyperbola/time-zero policy:            field_hyperbola_timezero_degeneracy_not_calibrated_inversion
boundary best-fit surfaces:            3 / 4
max near-top epsr span:                4.085
cover-depth claim ready:               false
radius claim ready:                    false
field FWI ready:                       false
```

Publication pointer retained from run 082:

```text
field_publication_claim_bundle_2d_qc_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
```

## Interpretation

This refresh makes the dataset policy current through run 086. The new field
evidence is useful as measured-data QC: the short-pair corrected residuals
support a relative apparent-depth scale check, and the sensitivity/degeneracy
audits define why that should not be promoted to calibrated depth, radius, 3D,
or measured-data FWI recovery.

The paper-facing field bundle remains run 082. Runs 084-086 are candidate
supplemental field figures, and run 087 is the latest dataset-policy endpoint
that ties those supplemental candidates back to the no-FWI/no-3D boundary.

## Validation

Focused tests:

```text
tests/test_gssi_field_dataset_policy_synthesis.py
3 passed
```

Figure validation:

```text
087 field_dataset_policy.png: 12939x835, dynamic range=255
```
