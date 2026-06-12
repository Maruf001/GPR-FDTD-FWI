# Experiment 70: Marathon Checkpoint Reporting Handoff

## Purpose

Create a compact recovery checkpoint after the resumed autonomous marathon work.
This is meant to make another crash recoverable without rereading every tracker.

## 537: Marathon Checkpoint

Output:

```text
outputs/experiments/537_marathon_checkpoint_reporting_handoff
```

Artifacts:

```text
README.md
data/marathon_checkpoint.json
run_manifest.json
```

Checkpoint summary:

| Runs | Result |
| --- | --- |
| 528-531 | Fitted-ringdown seed replication is closed; all nine target/seed rows are exact. |
| 532 | Cross-condition objective report identifies veryhigh as the only all-row margin improver. |
| 533 | Variable-depth/radius objective-use handoff separates base update from veryhigh reporting. |
| 534 | Close50 acquisition metadata repair labels legacy default Tx/Rx rows explicitly. |
| 535 | Source-shape center interval handoff records r=6.0-6.2 mm reporting. |
| 536 | Shallow r=4 single-rebar handoff records nominal point plus nuisance-aware interval. |

Validation:

```text
focused aggregate tests: 6 passed in 0.18 s
full test suite: 255 passed in 24.14 s
latest git diff --check: clean
```

## Next Decision

No GPU run is currently justified by the handoff matrix. Continue with
CPU/reporting work or prepare a concise paper/report synthesis unless a new
concrete physics gap is identified.
