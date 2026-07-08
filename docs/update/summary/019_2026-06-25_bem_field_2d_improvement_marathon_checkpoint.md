# BEM, Field, And 2D Improvement Marathon Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the current improvement block across the BEM,
field-side, and synthetic 2D tracks.

No broad GPU queue, field FWI, field 3D/HPC, or neural-network training was
launched.

## BEM Track

New BEM-side project-core bridge diagnostics:

```text
outputs/bem_experiments/027_project_core_direct_wave_effective_wavenumber_audit
outputs/bem_experiments/028_project_core_source_injection_mode_direct_wave_audit
```

Tracked notes:

```text
docs/bem_experiments/027_project_core_direct_wave_effective_wavenumber_audit.md
docs/bem_experiments/028_project_core_source_injection_mode_direct_wave_audit.md
```

Run `027` tested whether the project-core direct-wave mismatch is mainly an
FDTD numerical-dispersion problem by fitting a real effective wavenumber per
frequency:

```text
frequency count:                 17
mean analytic-k symmetric L2:     1.6246350401682335
mean fitted-k symmetric L2:       1.5074140243698353
median effective-k ratio:         0.835753777485865
effective wavenumber ready:       false
```

Run `028` tested whether the blocker is a simple project-core source-injection
choice:

```text
source/receiver pairs:            98
selected frequencies:             17
best source mode:                 pre_soft_field
best all-pair symmetric L2:        1.5877141638561911
best reference-transfer L2:        1.3021562348784914
best max per-offset L2:           0.4438290344803543
source-mode bridge ready:         false
```

Interpretation:

```text
The BEM-owned 2D ladder remains valid through run 016.
The project-core bridge remains blocked.
The blocker is not fixed by:
  - PEC-only geometry simplification
  - homogeneous target simplification
  - direct-wave path-length calibration
  - dense offset interpolation
  - arrival-window cleanup
  - simple real-k dispersion fitting
  - simple source-injection mode switching
```

Current BEM decision:

```text
Do not compare BEM to the historical outputs/experiments archive as a claim yet.
Do not move this bridge into 3D inversion yet.
Next useful BEM work is a discrete project-core Green-function model or a
controlled scattered-field calibration ladder.
```

## Field Track

New field-side planning artifact:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/164_gssi51600s_controlled_collection_intake_manifest_template
```

Tracked note:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/164_gssi51600s_controlled_collection_intake_manifest_template.md
```

Result:

```text
manifest rows:                    20
metadata values required:          11
real files required:               9
controlled profile files:          3
time-zero reference files:         3
amplitude reference files:         3
closure groups:                    6
ready for collection-day use:      true
ready for provenance acceptance:   false
ready for field FWI:               false
ready for GPU work:                false
```

Interpretation:

```text
The field blocker is now operational, not abstract.
The next field-day packet needs 11 real metadata values and 9 real files.
The dry-run archive still cannot be promoted to field evidence by relabeling.
```

Current field decision:

```text
Use run 164 as the collection-day intake sheet.
After collection, rerun structural validation and the provenance gate.
Do not launch field FWI, heavy GPU work, field 3D/HPC, or neural-network
training from the current dry-run packet.
```

## Synthetic 2D Track

Current 2D checkpoint:

```text
outputs/summary_tables/134_local_2d_detector_fixed_radius_locking_generalization_audit
docs/experiments/870_fixed_radius_locking_generalization_audit.md
```

Result:

```text
design runs audited:               3
candidate-table steps audited:      9
eligible lock opportunities:        1
validated lock opportunities:       1
unvalidated lock opportunities:     0
validation exact geometry:          true
validation final L-infinity:        0 mm
single-branch mechanism ready:      true
general locking-policy ready:       false
broad GPU queue ready:              false
detector-seeded FWI ready:          false
field transfer ready:               false
```

Current 2D decision:

```text
Do not launch another fixed-radius GPU probe from the current evidence.
Use the result as a narrow mechanism result only.
The next 2D improvement should either integrate this result into the report
evidence pack or define a new acquisition/physics hypothesis before running
new simulations.
```

## Next Defensible Improvements

1. BEM: build a discrete project-core Green-function audit that measures the
   FDTD response from every source grid point to every receiver grid point and
   uses that empirical Green table as the bridge baseline.
2. BEM: build a controlled scattered-field ladder with the simplest target
   family first: no target, weak dielectric cylinder, stronger dielectric
   cylinder, PEC cylinder. Only compare target scattering after the direct
   path is explicitly accounted for.
3. Field: use run `164` during collection and require file paths, SHA256
   checksums, operator initials, timestamps, and measured metadata before any
   field FWI claim.
4. 2D: refresh the local 2D/field/BEM evidence pack so the presentation does
   not imply that the fixed-radius mechanism is general or that the BEM bridge
   is ready for historical archive claims.
5. 2D: if new simulation work is desired, define a new acquisition hypothesis
   first, such as source/receiver spacing, direct-wave suppression, or
   target-coupling observability. The current fixed-radius branch has no
   unresolved eligible GPU case.

## Validation

Scripts compiled:

```text
run_project_core_direct_wave_effective_wavenumber_audit.py
run_project_core_source_injection_mode_direct_wave_audit.py
run_gssi_field_controlled_collection_intake_manifest_template.py
```

Focused tests:

```text
tests/test_gssi_field_controlled_collection_provenance_closure.py
tests/test_gssi_field_controlled_collection_provenance_gate.py
tests/test_gssi_field_controlled_collection_gate_sensitivity.py
tests/test_local_2d_detector_fixed_radius_locking_generalization_audit.py

13 passed
```

Figures checked:

```text
outputs/bem_experiments/027_project_core_direct_wave_effective_wavenumber_audit/figures/direct_wave_effective_wavenumber.png
outputs/bem_experiments/028_project_core_source_injection_mode_direct_wave_audit/figures/source_injection_mode_direct_wave_summary.png
outputs/field_experiments/local_gssi_51600s_2026_06_09/164_gssi51600s_controlled_collection_intake_manifest_template/figures/field_controlled_collection_intake_manifest.png
```
