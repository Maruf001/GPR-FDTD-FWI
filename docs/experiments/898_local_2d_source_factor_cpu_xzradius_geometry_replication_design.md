# Experiment 898: Local 2D Source-Factor CPU X/Z/Radius Geometry-Replication Design

Date: 2026-06-25

## Purpose

Design a bounded x/z/radius replication for
`max_geometry_instability/time_shift_only`, using the same source perturbation
type tested in run `188` but a different sensitive case category.

This run does not execute the optimizer command, run the full nine-command
batch, use GPU, transfer to field, run field FWI, or train neural networks.

## Output

```text
outputs/summary_tables/190_local_2d_source_factor_cpu_xzradius_geometry_replication_design
```

Key artifacts:

```text
commands/run_local_2d_source_factor_cpu_xzradius_geometry_replication.sh
data/local_2d_source_factor_cpu_xzradius_geometry_replication_command.csv
data/local_2d_source_factor_cpu_xzradius_geometry_replication_validation.csv
data/local_2d_source_factor_cpu_xzradius_geometry_replication_summary.json
docs/LOCAL_2D_SOURCE_FACTOR_CPU_XZRADIUS_GEOMETRY_REPLICATION_DESIGN.md
figures/local_2d_source_factor_cpu_xzradius_geometry_replication_design.png
scripts/run_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py
scripts/test_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py
scripts/script_snapshot_manifest.json
```

## Result

```text
source command run:                      175_local_2d_source_factor_numbered_cpu_command_design
source execution run:                    188_local_2d_source_factor_cpu_xzradius_local_execution_audit
source x/z/radius usable:                true
replication case category:               max_geometry_instability
replication variant:                     time_shift_only
predicted runner experiment ID:          1364
requested run name:                      local_2d_source_factor_xzradiusrep_max_geometry_instability_time_shift_only_cpu
expected runner output name:             1364_local_2d_source_factor_xzradiusrep_max_geometry_instability_time_shift_only_cpu
expected candidate count per case:       8
design validation pass:                  false
recommended cap seconds:                 3600
backend CPU:                             true
no-fit amplitude:                        true
single target:                           true
two x candidates:                        true
two z candidates:                        true
two radius candidates:                   true
base objective only:                     true
revisit disabled:                        false
no numeric run-name prefix:              true
output collision:                        false
commands executed:                       false
replication execution ready:             false
full counterfactual execution ready:     false
new FDTD run ready:                      false
GPU work ready:                          false
field transfer ready:                    false
```

## Interpretation

The selected source row from run `175` still contained revisit flags:

```text
--revisit-weak-high-radius-targets
--revisit-broad-radius-ambiguity-targets
--revisit-ambiguity-min-width-mm 0.2
--revisit-x-offsets-mm=-1:1:1
--revisit-z-offsets-mm=-2:2:1
--revisit-radius-step-mm 0.5
```

That violates the bounded local replication contract. The design correctly
blocked execution.

## Decision

Do not execute the run `190` command. Duplicate this run-specific script and
remove the revisit flags/options before generating the corrected replication
design.

## Milestone Snapshot

This is a result-driven local 2D milestone. It froze:

```text
run_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py
sha256: 950747e98c8041094b03abe33caceeabb22f72017c223b64e879ea9bd65a5ce3

test_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py
sha256: 0efdac7d532bd30923c946010a75aa9189ffdcefe26710e56e26d1164e10db9c
```

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_cpu_xzradius_geometry_replication_design.py
3 passed
```

Figure check:

```text
local_2d_source_factor_cpu_xzradius_geometry_replication_design.png
1420x738, dynamic range=255
```
