# BEM Green-Surface Bridge Marathon Checkpoint

Date: 2026-06-25

## Scope

This checkpoint records the BEM/project-core bridge progress from runs `039`
through `074`.

This is a progress checkpoint, not a marathon stop condition.

## Key Finding

Raw continuous analytic/free-space Green fields are not the supported bridge.
The supported bridge is now:

```text
project-domain target-cell Green surface
plus discrete project-grid scattering operator
plus held-out adapter gates
```

## Negative Gates

Run `039`:

```text
best analytic/BEM-compatible Green L2: 0.8309901396143111
adapter ready:                         false
```

Run `040`:

```text
worst all-scan analytic mixture L2:    0.6280658438481003
worst leave-one-scan mixture L2:       0.9869554402632811
field-map calibration ready:           false
```

Interpretation:

```text
The analytic/free-space Green mismatch is not closed by a transferable
two-term convention mixture.
```

## Positive Gates

Run `041`:

```text
project-domain Green surface, epsr ladder
worst interpolated-surface L2:          0.5573625471027422
ready:                                  true
```

Run `042`:

```text
fresh high-contrast denser/shifted cases
worst interpolated-surface L2:          0.5974979747759482
ready:                                  true
```

Run `044`:

```text
depth and radius stress at epsr 4.0
worst interpolated-surface L2:          0.6390901970749561
ready:                                  true
```

Run `045`:

```text
10, 30, and 40 mm Tx/Rx offset stress at epsr 4.0
worst interpolated-surface L2:          0.6858047703122613
ready:                                  true
```

Run `046`:

```text
air/concrete layered dielectric probe
sparse interpolated-surface L2:         1.1770012780031571
ready:                                  false
```

Run `047`:

```text
layered dense target-cell surface probe
dense surface samples:                  19
dense interpolated-surface L2:          0.697021169360853
ready:                                  true
edge extrapolated points:               0
```

## Contract Pack

Run `043` packages the current adapter contract:

```text
usable bridge:             project-domain target-cell Green surface
not usable bridge:         raw continuous analytic/free-space Green fields
numeric gates passed:      4
numeric gates failed:      2
blocked claim gates:       2
```

Run `048` refreshes the contract:

```text
homogeneous extension ready:             true
layered conditional ready:               true
field claim ready:                       false
3D claim ready:                          false
```

Run `049`:

```text
raw analytic field-table replacement
global scaled field L2:                  1.0419444002374967
per-source scaled field L2:              0.817994101096804
leave-one-source field L2:               1.0723419515425194
replacement ready:                       false
```

Run `050`:

```text
per-cell finite-domain field map
per-cell all-source field L2:            0.7242401633347877
per-cell leave-one-source field L2:      0.8005360330027802
replacement ready:                       false
```

Run `051`:

```text
dense per-cell finite-domain field map
dense leave-one-source field L2:         0.9392735973185401
replacement ready:                       false
```

Run `052`:

```text
reusable helper module:                  bem_green_surface_adapter.py
focused tests:                           4 passed
purpose:                                 dense-grid and per-cell leave-one-source utilities
```

Run `053`:

```text
replacement requirements:                6
missing requirements:                    2
blocked requirements:                    3
field claim ready:                       false
3D claim ready:                          false
```

Run `054`:

```text
source-convention variants checked:      48
best per-cell leave-one-source L2:       0.7871631960439586
source convention ready:                 false
```

Run `055`:

```text
boundary-image variants checked:         36
best global image leave-one-source L2:   0.3301113956330722
best per-cell image leave-one-source L2: 0.1228536659883146
boundary image ready:                    true
```

Run `056`:

```text
boundary-image scattering replay
worst all-scan replay L2:                0.4375137396284387
worst leave-one-scan replay L2:          0.5620892946687726
scattering ready:                        true
```

Run `057`:

```text
boundary-image stress replay
stress cases:                            10
worst all-scan replay L2:                0.543696265768155
worst leave-one-scan replay L2:          0.667995713341894
stress replay ready:                     true
```

Run `058`:

```text
boundary-image layered replay
variants checked:                        60
surface samples:                         19
best field-table LOO L2:                 1.2033632008026727
best scattering all-scan L2:             0.8085674766282847
best scattering leave-one-scan L2:       0.9920836859251249
layered boundary-image ready:            false
```

Run `059`:

```text
layer-aware basis ladder
variants checked:                        81
best field-table LOO L2:                 1.1925655903879098
best scattering all-scan L2:             0.8083671696254245
best scattering leave-one-scan L2:       1.0946737347877629
layer-aware basis ready:                 false
```

Run `060`:

```text
boundary-image contract refresh
contract rows:                           8
homogeneous boundary-image ready:        true
layered boundary-image ready:            false
dense layered surface required:          true
field claim ready:                       false
3D/FWI/GPU ready:                        false
```

Run `061`:

```text
layered dense-surface cache
surface shape:                           19x533x17
cache size bytes:                        2710904
best interpolated-surface L2:            0.697021169360853
cache replay ready:                      true
```

Run `062`:

```text
layered dense-surface cache consumer
cache validation findings:               0
cache load seconds:                      0.01241654809564352
best interpolated-surface L2:            0.697021169360853
cache replay ready:                      true
```

Run `063`:

```text
layered surface decimation ladder
policies checked:                        6
ready policies:                          3
minimum ready sample count:              7
best policy:                             full_10mm_cache
best leave-one-scan L2:                  0.697021169360853
```

Run `064`:

```text
layered 30 mm surface stress
cases checked:                           4
ready cases:                             3
worst leave-one-scan L2:                 0.8468025283677086
30 mm layered stress ready:              false
```

Run `065`:

```text
layered Sommerfeld proxy probe
field leave-one-x L2:                    0.3928483810786592
scattering all-scan L2:                  0.5236861579717635
scattering leave-one-scan L2:            0.6497571611891658
Sommerfeld proxy ready:                  true
```

Run `066`:

```text
layered Sommerfeld proxy stress
cases checked:                           4
ready cases:                             4
worst field leave-one-x L2:              0.3928483810786592
worst scattering leave-one-scan L2:      0.6497571611891657
Sommerfeld stress ready:                 true
```

Run `067`:

```text
BEM replacement contract refresh
homogeneous replacement ready:           true
layered Sommerfeld ready:                true
layered tabulated fallback ready:        true
compact 30 mm layered ready:             false
field claim ready:                       false
3D/FWI/GPU ready:                        false
```

Run `068`:

```text
3D transition contract
requirements:                            10
partial requirements:                    4
blocked requirements:                    6
3D transition ready:                     false
field transfer ready:                    false
GPU/HPC ready:                           false
```

Run `069`:

```text
minimal 3D reference design
cells with PML:                          268800
time steps for 6 ns:                     630
cells per 3 GHz concrete wavelength:     8.159317231497297
padded memory estimate GiB:              0.16021728515625
ready for design review:                 true
ready for 3D launch:                     false
```

Run `070`:

```text
Bempp minimal 3D reference backend probe
finite rebar:                            length 0.12 m, radius 0.01 m
mesh vertices/elements:                  114 / 224
RWG DOFs:                                336
frequencies checked:                     4
wavenumber range rad/m:                  25.668754418669145 to 154.01252651201483
finite all responses:                    true
Bempp backend reference ready:           true
3D FDTD validation ready:                false
```

Run `071`:

```text
matched 3D FDTD comparison contract
contract items:                          10
ready / partial / blocked:               7 / 1 / 2
launch blockers:                         3
frequencies:                             0.5, 1.0, 1.5, 3.0 GHz
receiver count:                          31
plane-wave source mismatch:              true
plane-wave FDTD design ready:            true
GPR-like FDTD design ready:              false
3D FDTD launch ready:                    false
3D validation claim ready:               false
```

Run `072`:

```text
Bempp dipole source probe
source position:                         [-0.04, 0.0, 0.09] m
dipole moment:                           [0.0, 1.0, 0.0]
mesh vertices/elements:                  114 / 224
RWG DOFs:                                336
frequencies checked:                     4
finite all responses:                    true
max scattered norm range:                29.513832034532605 to 3373.3467929303047
dipole Bempp reference ready:            true
GPR-like FDTD design ready:              true
3D FDTD validation ready:                false
```

Run `073`:

```text
paired 3D FDTD manifest contract
manifest templates:                      2
receiver count:                          31
frequency count:                         4
comparison requirements:                 7
missing external FDTD runs:              2
blocked requirements:                    3
grid cells with PML:                     268800
time steps:                              630
paired manifest templates ready:         true
paired FDTD data ready:                  false
3D FDTD launch ready:                    false
3D validation claim ready:               false
```

Run `074`:

```text
3D FDTD manifest validator
validation checks:                       9
passed checks:                           9
failed checks:                           0
manifest templates valid:                true
paired FDTD data ready:                  false
3D validation claim ready:               false
```

Current blocked claims:

```text
historical outputs/experiments archive claim
field claim
3D claim
FWI/GPU/HPC claim
```

## Current Decision

Use the boundary-image model as the active homogeneous 2D BEM replacement
candidate for the tested project-core cases.

Do not replace the project-domain field table with raw or simply calibrated
analytic Green fields. Do not use the homogeneous boundary-image replacement
for layered claims. Do not promote this to field, 3D, FWI, GPU, or
historical-archive claims until those branches have their own matched
validation gates.

## Next Branch

Continue immediately to one of:

```text
1. field-side intake/provenance improvement while field FWI remains blocked
2. implement or import paired FDTD target/background outputs that satisfy the
   run `073` manifest contract and pass run `074` validation
3. presentation material using the run `067` replacement contract and runs
   `069`-`074` 3D progression
4. keep the full 10 mm layered cache as default until new stress evidence changes it
5. keep field and 3D claims blocked until their own gates exist
```

Field side remains gated by run `163` closure requirements:

```text
3 controlled profile-repeat files
3 time-zero reference files
3 amplitude-reference files
real session/target/geometry provenance
```

## Validation

Focused compile checks:

```text
run_project_core_bem_compatible_field_adapter_probe.py
run_project_core_bem_field_map_calibration_probe.py
run_project_core_bem_project_domain_green_surface_probe.py
run_project_core_bem_project_domain_green_surface_stress.py
run_project_core_bem_green_surface_contract_pack.py
run_project_core_bem_green_surface_geometry_stress.py
run_project_core_bem_green_surface_offset_stress.py
run_project_core_bem_green_surface_layered_dielectric_probe.py
run_project_core_bem_green_surface_layered_dense_probe.py
run_project_core_bem_green_surface_contract_refresh.py
run_project_core_bem_field_table_replacement_gap_audit.py
run_project_core_bem_finite_domain_field_map_probe.py
run_project_core_bem_finite_domain_field_map_dense_probe.py
run_project_core_bem_green_surface_adapter_module_audit.py
run_project_core_bem_replacement_model_requirements.py
run_project_core_bem_source_convention_ladder.py
run_project_core_bem_boundary_image_ladder.py
run_project_core_bem_boundary_image_scattering_replay.py
run_project_core_bem_boundary_image_stress_replay.py
run_project_core_bem_boundary_image_layered_replay.py
run_project_core_bem_layered_interface_basis_ladder.py
run_project_core_bem_boundary_image_contract_refresh.py
run_project_core_bem_layered_dense_surface_cache.py
bem_layered_surface_cache.py
run_project_core_bem_layered_dense_surface_cache_consumer.py
run_project_core_bem_layered_surface_decimation_ladder.py
run_project_core_bem_layered_30mm_surface_stress.py
run_project_core_bem_layered_sommerfeld_proxy_probe.py
run_project_core_bem_layered_sommerfeld_proxy_stress.py
bem_layered_sommerfeld.py
run_project_core_bem_replacement_contract_refresh.py
run_project_core_bem_3d_transition_contract.py
run_project_core_bem_minimal_3d_reference_design.py
run_project_core_bem_bempp_minimal_3d_reference_probe.py
bem_green_surface_adapter.py
tests/test_bem_green_surface_adapter.py
tests/test_bem_layered_surface_cache.py
tests/test_bem_layered_sommerfeld.py
pytest.ini
```

All compiled successfully during the marathon block.

Focused helper tests:

```text
tests/test_bem_green_surface_adapter.py
4 passed
```

Project regression suite:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
1040 passed in 29.35s
```

Root-level pytest was configured with `pytest.ini` so generated external repos
under `outputs/` are not collected as project tests.

Figure checks:

```text
run 039: 1852x805, dynamic range=255
run 040: 1925x769, dynamic range=255
run 041: 1925x769, dynamic range=255
run 042: 1979x843, dynamic range=255
run 043: 1853x841, dynamic range=255
run 044: 2022x861, dynamic range=255
run 045: 1925x823, dynamic range=255
run 046: 1817x770, dynamic range=255
run 047: 1911x788, dynamic range=255
run 048: 1747x787, dynamic range=255
run 049: 1817x770, dynamic range=255
run 050: 1673x788, dynamic range=255
run 051: 1732x771, dynamic range=255
run 052: 1535x735, dynamic range=255
run 053: 1872x842, dynamic range=255
run 054: 1873x1093, dynamic range=255
run 055: 1891x1093, dynamic range=255
run 056: 1745x787, dynamic range=255
run 057: 2125x919, dynamic range=255
run 058: 2231x1008, dynamic range=255
run 059: 2392x1098, dynamic range=255
run 060: 1888x846, dynamic range=255
run 061: 1985x846, dynamic range=255
run 062: 1924x792, dynamic range=255
run 063: 2140x842, dynamic range=255
run 064: 1888x846, dynamic range=255
run 065: 1564x810, dynamic range=255
run 066: 1924x846, dynamic range=255
run 067: 2104x842, dynamic range=255
run 068: 1924x806, dynamic range=255
run 069: 1925x792, dynamic range=255
run 070: 2104x845, dynamic range=255
run 071: 2500x808, dynamic range=255
run 072: 2500x845, dynamic range=255
run 073: 2104x840, dynamic range=255
run 074: 2106x844, dynamic range=255
```

Resource state stayed within limits; no GPU work was launched.
