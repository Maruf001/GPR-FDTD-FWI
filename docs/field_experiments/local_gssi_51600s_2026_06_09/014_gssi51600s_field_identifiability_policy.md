# Field Experiment 014: GSSI 51600S Field Identifiability Policy

Date: 2026-06-17

## Purpose

CPU-only identifiability reduction of the experiment 011 waveform-family shift
surface under the accepted field timing policy from experiments 012 and 013:

```text
phase convention: top_envelope_35pct
synthetic time shift: +0.2 ns
```

This asks whether the stable timing policy also supports radius or epsr
identification, or whether the field waveform matches should remain
calibration/QC evidence.

No FDTD, FWI, or GPU command was run for this experiment.

## Output

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09/014_gssi51600s_field_identifiability_policy
```

Artifacts:

```text
data/accepted_timing_candidates.csv
data/event_identifiability_summary.csv
data/profile_identifiability_summary.csv
data/field_identifiability_policy_summary.json
data/figure_validation.csv
figures/field_identifiability_margins.png
figures/field_candidate_landscape.png
run_manifest.json
```

## Result

Accepted timing-policy scope:

```text
accepted candidate rows:       36
event families:                 6
short profiles:                 2
correlation floor:              0.7
events passing floor:           6 of 6
clear-margin threshold:         0.02 absolute correlation
clear radius-margin events:     0 of 6
clear epsr-source events:       5 of 6
mean radius margin:             0.00750
minimum radius margin:          0.00004
mean epsr-source margin:        0.03738
minimum epsr-source margin:     0.01577
```

Event-level summary:

| Event | Best `|corr|` | Best radius | Radius margin | Radius clear? | Best epsr source | Epsr margin | Epsr clear? |
| --- | ---: | ---: | ---: | --- | --- | ---: | --- |
| `014 g1` | 0.8586 | 6 mm | 0.00004 | no | fitted | 0.01577 | no |
| `014 g2` | 0.8895 | 8 mm | 0.01867 | no | fitted | 0.04122 | yes |
| `014 g3` | 0.8836 | 8 mm | 0.00994 | no | fitted | 0.02617 | yes |
| `016 g1` | 0.8340 | 5 mm | 0.00725 | no | fitted | 0.02675 | yes |
| `016 g2` | 0.8195 | 5 mm | 0.00607 | no | fitted | 0.04249 | yes |
| `016 g3` | 0.8103 | 5 mm | 0.00300 | no | fitted | 0.07190 | yes |

Profile-level summary:

| Profile | Events | Mean best `|corr|` | Radius mode | Radius consensus | Mean radius margin | Epsr mode | Min epsr margin |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `PROJECT001C__014.DZT` | 3 | 0.8772 | 8 mm | 2/3 | 0.00955 | fitted | 0.01577 |
| `PROJECT001C__016.DZT` | 3 | 0.8213 | 5 mm | 3/3 | 0.00544 | fitted | 0.02675 |

## Interpretation

The field timing result is stable, but radius identification is not. All six
top-envelope event families match the synthetic snippets above the 0.7
correlation floor, yet none clears the 0.02 radius-margin threshold. Profile
016 is internally consistent at 5 mm, but the radius margins are only
0.0030-0.0073, which is too narrow to treat as a measured radius result.

Fitted epsr is preferred in all six accepted events, and five of six events
clear the epsr-source margin threshold. This is useful for calibration, but it
is still not independent material validation because the fitted epsr comes from
the same field hyperbola calibration stream.

Current field policy:

```text
Use top_envelope_35pct with +0.2 ns as the short-profile timing anchor.
Use fitted epsr as a calibration hypothesis, not as independent material proof.
Do not report field radius, geometry, or FWI recovery from this dataset yet.
Require external cover-depth, bar diameter, layout, and survey metadata before
field inversion is treated as a physical result.
```

## Validation

Both figures were validated as nonblank:

```text
field_identifiability_margins.png nonwhite=0.3284
field_candidate_landscape.png nonwhite=0.0816
```
