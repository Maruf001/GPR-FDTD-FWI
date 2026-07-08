# Local 2D Source-Factor CPU X/Z/Radius Corrected Geometry-Replication Design

Date: 2026-06-25

## Scope

This checkpoint records output `191`, the corrected execution-ready
geometry-instability replication design.

## Output

```text
outputs/summary_tables/191_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design
```

Tracked note:

```text
docs/experiments/899_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.md
```

## Result

```text
replication case category:               max_geometry_instability
replication variant:                     time_shift_only
expected candidate count per case:       8
design validation pass:                  true
revisit disabled:                        true
commands executed:                       false
replication execution ready:             true
full counterfactual execution ready:     false
GPU work ready:                          false
field transfer ready:                    false
```

## Decision

Run `191` supersedes the blocked run `190` command. Use run `191` for the
bounded geometry-instability execution audit.

## Milestone Snapshot

This milestone froze:

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

Python compile check:

```text
run_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.py: pass
tests/test_local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.py: pass
```

Figure check:

```text
local_2d_source_factor_cpu_xzradius_geometry_replication_corrected_design.png
1420x738, dynamic range=255
```

Marathon status: active. The next branch is the capped corrected replication
execution audit.
