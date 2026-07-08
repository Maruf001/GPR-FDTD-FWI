# Experiment 899: Local 2D Source-Factor CPU X/Z/Radius Corrected Geometry-Replication Design

Date: 2026-06-25

## Purpose

Correct the no-go run `190` replication design by stripping revisit
flags/options from the selected `max_geometry_instability/time_shift_only`
source row.

This run does not execute the optimizer command, run the full nine-command
batch, use GPU, transfer to field, run field FWI, or train neural networks.

## Output

```text
outputs/summary_tables/191_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design
```

Key artifacts:

```text
commands/run_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected.sh
data/local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_command.csv
data/local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_validation.csv
data/local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_CPU_XZRADIUS_GEOMETRY_REPLICATION_CORRECTED_DESIGN.md
figures/local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.png
scripts/run_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.py
scripts/test_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source command run:                      175_local_2d_source_factor_numbered_cpu_command_design
source execution run:                    188_local_2d_source_factor_cpu_xzradius_local_execution_audit
blocked design run:                      190_local_2d_source_factor_cpu_xzradius_geometry_replication_design
source x/z/radius usable:                true
replication case category:               max_geometry_instability
replication variant:                     time_shift_only
predicted runner experiment ID:          1364
requested run name:                      local_2d_source_factor_xzradiusrep_max_geometry_instability_time_shift_only_cpu
expected runner output name:             1364_local_2d_source_factor_xzradiusrep_max_geometry_instability_time_shift_only_cpu
expected candidate count per case:       8
design validation pass:                  true
recommended cap seconds:                 3600
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
two x candidates:                        true
two z candidates:                        true
two radius candidates:                   true
base objective only:                     true
revisit disabled:                        true
no numeric run-name prefix:              true
output collision:                        false
commands generated:                      true
commands executed:                       false
replication execution ready:             true
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Interpretation

Run `191` repairs the run `190` blocker. It keeps the geometry-instability
replication bounded to one target, two x candidates, two z candidates, two
radius candidates, base objective only, and no revisit phase.

## Decision

Execute this corrected geometry-instability replication command as the next
bounded CPU smoke with a 3600-second cap. Keep the full batch, GPU work, and
field transfer blocked.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.py
sha256: 61b4ed2ff4e41a9d53853eaad54f63eeac69ef11b65c4a5b0ac6025897b12a71

test_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.py
sha256: 50cc8a462f36e471545e2d6b5c058034a0a33ea1284be351ece6c5fc544f9cb0
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.py
3 passed
```

Figure check:

```text
local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.png
1420x738, dynamic range=255
```
