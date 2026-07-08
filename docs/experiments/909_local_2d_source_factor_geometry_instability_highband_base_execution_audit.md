# Experiment 909: Local 2D Source-Factor Geometry-Instability Highband/Base Execution Audit

Date: 2026-06-25

## Purpose

Execute the corrected base-plus-highband geometry-instability command designed
in run `228`.

Run `226` showed that the highband-only command was invalid because
`run_multi_rebar_coordinate_optimizer.py` requires the first diagnostic
objective variant to be labelled `base`. Run `228` corrected the command. This
run answers the actual physics/objective question:

```text
Does the highband diagnostic objective move the geometry-instability case from
the lower-x preference at 188 mm to the 190 mm truth?
```

This is a bounded CPU-only optimizer execution. It does not launch a broad
source-factor batch, GPU work, field transfer, field FWI, 3D/HPC, or
neural-network training.

## Output

```text
outputs/summary_tables/230_local_2d_source_factor_geometry_instability_highband_base_execution_audit
outputs/experiments/1369_local_2d_source_factor_geomxdisc_shifted_source_base_highband_cpu
```

Key audit artifacts:

```text
data/local_2d_source_factor_geometry_instability_highband_base_execution_summary.json
data/local_2d_source_factor_geometry_instability_highband_base_execution_objectives.csv
data/local_2d_source_factor_geometry_instability_highband_base_execution_confidence.csv
data/local_2d_source_factor_geometry_instability_highband_base_execution_required_artifacts.csv
docs/LOCAL_2D_SOURCE_FACTOR_GEOMETRY_INSTABILITY_HIGHBAND_BASE_EXECUTION_AUDIT.md
figures/local_2d_source_factor_geometry_instability_highband_base_execution_audit.png
scripts/run_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py
scripts/test_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py
scripts/script_snapshot_manifest.json
```

## Result

```text
commands executed:               true
timed out:                       false
exit code:                       0
elapsed seconds:                 454.508
complete optimizer output:       true
usable evidence ready:           true
required artifacts present:      6 / 6
candidate CSV count:             1
figure file count:               4
confidence best x:               188.0 mm
confidence truth x selected:     false
base best x:                     188.0 mm
highband best x:                 188.0 mm
highband truth x selected:       false
full batch ready:                false
GPU work ready:                  false
field transfer ready:            false
```

Objective diagnostics:

| Objective | Best x mm | Best z mm | Best radius mm | Best misfit | Truth x | Truth xyz |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| `base` | 188.0 | 90.0 | 5.0 | 0.7270403815749271 | false | false |
| `highband` | 188.0 | 90.0 | 5.0 | 0.5538109095852684 | false | false |

## Interpretation

The corrected highband objective is now tested. It reduces the reported misfit
relative to the base objective, but it does not change the selected geometry.
Both objectives still prefer `x=188 mm` with truth `z=90 mm` and truth radius
`5 mm`.

This means the geometry-instability lower-x preference is not an artifact of
the invalid highband-only command. It also is not fixed by adding a valid
highband diagnostic alongside the required base objective.

## Decision

Do not promote the highband objective as a solution for this geometry branch.
Keep broad source-factor batch execution, GPU work, field transfer, and
claim-making blocked.

The next useful local 2D branch is an objective/observable discriminant that can
explain why the geometry case prefers lower x even when z and radius are fixed
to truth.

## Milestone Snapshot

This is a result-driven local 2D execution milestone. It froze:

```text
run_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py
sha256: e82b9c6a58eb92c4adbb05f63c259c17f3dde4f0f5eff39959335b2f5da5a12a

test_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py
sha256: 3b6b12345bfd185a3db6103a8bfe00d51210fb60056992079003f6471d584186
```

Subsequent related local 2D source-factor experiments should start from a
duplicated run-specific script.

## Validation

Focused tests:

```text
tests/test_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py
3 passed
```

Compile check:

```text
run_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py: pass
tests/test_local_2d_source_factor_geometry_instability_highband_base_execution_audit.py: pass
```

Figure check:

```text
1672x738, dynamic range=255
```
