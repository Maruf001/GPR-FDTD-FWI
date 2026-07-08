# Local 2D And Field Marathon Checkpoint

Date: 2026-06-22

## Scope

This checkpoint records the current local synthetic 2D and field-side state
after the latest marathon block. No broad GPU queue, field FWI, field 3D/HPC,
or neural-network training was launched.

The resource rule remained:

```text
RAM cap: <= 80%
GPU utilization cap: <= 90%
```

## Synthetic 2D: Fixed-Radius Locking Generalization

New CPU-side audit:

```text
outputs/summary_tables/134_local_2d_detector_fixed_radius_locking_generalization_audit
```

Tracked note:

```text
docs/experiments/870_fixed_radius_locking_generalization_audit.md
```

Result:

```text
design runs audited:             3
candidate-table steps audited:    9
eligible lock opportunities:      1
validated lock opportunities:     1
unvalidated lock opportunities:   0
validation final L-infinity:      0 mm
new guarded GPU probe ready:      false
broad GPU queue ready:            false
detector-seeded FWI ready:        false
field transfer ready:             false
```

Interpretation:

The target-locking mechanism validated in run `1358` is real but narrow. The
saved candidate tables expose exactly one eligible lock opportunity, and it is
already the one validated by the guarded unlock probe. This supports a
single-branch mechanism claim, not a general detector policy.

Current synthetic 2D decision:

```text
Do not start another fixed-radius detector GPU probe from the current evidence.
Use the result as mechanism evidence and preserve the broader detector/FWI
guardrails.
```

## Field Side: Provenance Closure

New field-side run:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/163_gssi51600s_controlled_collection_provenance_closure
```

Tracked note:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/163_gssi51600s_controlled_collection_provenance_closure.md
```

Result:

```text
source structural ready:                  true
source provenance ready:                  false
provenance findings grouped:              42
closure action groups:                    6
real files required:                      9
controlled profile files required:        3
time-zero reference files required:        3
amplitude-reference files required:       3
current archive can close without data:   false
provenance acceptance ready:              false
field FWI ready:                          false
field 3D/HPC ready:                       false
gpu priority:                             none
```

The six closure actions are:

| Priority | Closure group | Findings | Files required |
| ---: | --- | ---: | ---: |
| 1 | session metadata real values | 9 | 0 |
| 2 | target truth provenance | 2 | 0 |
| 3 | profile geometry provenance | 1 | 0 |
| 4 | acquisition profile files | 12 | 3 |
| 5 | time-zero reference files | 9 | 3 |
| 6 | amplitude reference files | 9 | 3 |

Interpretation:

The field-side blocker is now concrete. The dry-run packet cannot become
field evidence by relabeling. It needs real measured files and measured
metadata, then both structural packet validation and provenance validation
must pass.

Current field decision:

```text
Use run 163 as the collection-day acceptance checklist.
Do not launch current-archive field FWI, heavy GPU work, field 3D/HPC,
or neural-network training from the dry-run packet.
```

## Validation

Focused tests:

```text
tests/test_local_2d_detector_fixed_radius_locking_generalization_audit.py
tests/test_gssi_field_controlled_collection_provenance_closure.py
tests/test_gssi_field_controlled_collection_provenance_gate.py
tests/test_gssi_field_controlled_collection_gate_sensitivity.py

13 passed
```

Full test suite:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
1027 passed in 31.68s
```

Python compile check:

```text
run_local_2d_detector_fixed_radius_locking_generalization_audit.py: pass
run_gssi_field_controlled_collection_provenance_closure.py: pass
tests/test_local_2d_detector_fixed_radius_locking_generalization_audit.py: pass
tests/test_gssi_field_controlled_collection_provenance_closure.py: pass
```

## Current Next Step

The next useful work is not another immediate GPU run. The clean next options
are:

1. Prepare the next PI-facing report/update around the current synthetic 2D
   mechanism result and the field run `163` provenance-closure checkpoint.
2. If field collection is possible, fill the controlled packet with real
   session metadata, target truth, profile geometry, three controlled profile
   files, three time-zero references, and three amplitude references, then
   rerun the structural validator and provenance gate.
3. If a new synthetic question is desired, define a new objective or acquisition
   hypothesis first. The current fixed-radius locking branch has no unresolved
   eligible GPU probe.
