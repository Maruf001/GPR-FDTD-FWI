# Local 2D and Field Marathon Update

Date: 2026-06-17

## Scope

This update summarizes the local DGX-side work after the 3D/HPC branch was
split off. It covers CPU-side 2D policy synthesis and measured GSSI field-data
QC. No broad synthetic GPU sweep was launched.

## Synthetic 2D Status

The target0 weak-exact exception from run 1136 is closed by existing follow-up
evidence:

```text
1136: 8 sources, Tx/Rx=60.0 mm, base margin 3.872998e-04
1139: 8 sources, Tx/Rx=45.0 mm, base margin 4.842585e-04
1140: 9 sources, Tx/Rx=60.0 mm, base margin 5.296469e-04
```

Run 1276 / experiment 798 records the closure policy:

```text
target0_exception_closed_by_source_density
gpu priority: none
```

Run 1277 / experiment 799 records the modern ringdown050 exception status:

```text
modern_ringdown050_no_open_exception_gpu_priority_none
modern ringdown050 exceptions: 1 closed, 0 open
legacy exceptions: ringdown025 run 785 remains an archive caveat
```

Run 1278 / experiment 800 records the synthetic 2D publication figure bundle:

```text
synthetic_2d_publication_bundle_ready_gpu_priority_none
figure count:             5
validated figure count:   5
claim boundary count:     4
ready for manuscript:     true
```

Run 1279 / experiment 801 records the synthetic 2D next-question matrix:

```text
synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate count:              5
immediate GPU priority:       0
conditional GPU candidates:   1
top question:                 x_ambiguity_objective_design
top readiness:                cpu_first
```

Run 1280 / experiment 802 records the close50 sub-30 x-ambiguity metric:

```text
close50_sub30_x_ambiguity_reporting_metric_ready_cpu_no_gpu
rows:                       6
exact strong rows:          6
paper-clean rows:           4
x-ambiguous rows:           2
max x-ambiguity width:      1.000 mm
gpu priority:               none_now
```

Run 1281 / experiment 803 applies the strict location-clean metric across
existing non-smoke coordinate-confidence aggregate CSVs:

```text
archive_location_clean_metric_x_ambiguity_present_cpu_no_gpu
aggregate files audited:            67
rows audited:                       687
exact strong rows:                  323
strict location-clean strong rows:  302
exact strong x-ambiguous rows:      19
exact strong z-ambiguous rows:      2
exact strong radius-ambiguous rows: 2
location-clean fraction:            0.934985
gpu priority:                       none_now
```

Run 1282 / experiment 804 breaks those ambiguous archive rows down by family:

```text
archive_location_ambiguity_target2_family_breakdown_cpu_no_gpu
exact-strong ambiguous rows:        21
family count:                       4
target indices:                     2
x-ambiguous rows:                   19
z-ambiguous rows:                   2
radius-ambiguous rows:              2
target2_variable_radius_legacy:     12 rows, x only
target2_close14:                    4 rows, x only
target2_close50:                    3 rows, x only
target2_variable_depth_radius:      2 rows, z + radius
gpu priority:                       none_now
```

Run 1283 / experiment 805 diagnoses the target2 archive ambiguity at the
objective-near-tie level:

```text
target2_archive_ambiguity_near_tie_diagnostic_cpu_no_gpu
rows:                                21
competitors within threshold:        21
one-mm lateral near ties:            19
depth/radius coupled near ties:      2
mixed objective near ties:           0
min competitor objective gap:        2.210812e-05
min margin inside threshold:         3.491030e-07
gpu priority:                        none_now
```

Run 1284 / experiment 806 audits target2 objective margins across all
exact-strong target2 rows:

```text
target2_objective_margin_geometry_clean_but_near_ties_present_cpu_no_gpu
target2 exact-strong rows:           267
strict location-clean rows:          246
geometry-ambiguous rows:             21
zero-width objective near ties:      9
strict-clean margin-separated rows:  237
competitors within threshold:        30
strict location-clean fraction:      0.921348
min separated competitor gap:        1.083986e-03
gpu priority:                        none_now
```

Run 1285 / experiment 807 applies the reporting tiers across targets:

```text
cross_target_reporting_tiers_target2_geometry_target1_target2_zero_width_cpu_no_gpu
exact-strong rows:                   323
geometry-ambiguous rows:             21
zero-width objective near ties:      18
strict-clean margin-separated rows:  284
geometry-ambiguous targets:          2
zero-width near-tie targets:         1;2
gpu priority:                        none_now
```

Run 1286 / experiment 808 refreshes synthetic manuscript claim boundaries:

```text
synthetic_2d_publication_claim_boundaries_refreshed_cpu_no_gpu
claim boundary count:                7
reporting-tier policy:               cross_target_reporting_tiers_target2_geometry_target1_target2_zero_width_cpu_no_gpu
geometry-ambiguous targets:          2
zero-width near-tie targets:         1;2
ready for manuscript claim table:    true
gpu priority:                        none
```

Run 1287 / experiment 809 audits raw competing-geometry near ties:

```text
competing_geometry_near_tie_zero_width_metric_gap_cpu_no_gpu
exact-strong rows:                   323
reported-width near ties:            21
zero-width competing-geometry ties:  18
competitor-separated rows:           284
hidden near-tie targets:             1;2
objective-unique eligible fraction:  0.879257
recommended metric:                  objective_unique_candidate = exact_strong and not competitor_within_ambiguity_threshold
gpu priority:                        none_now
```

Run 1288 / experiment 810 builds the manuscript claim-tier table:

```text
synthetic_claim_tiers_geometry_clean_and_objective_unique_separated_cpu_no_gpu
exact-strong rows:                   323
geometry-clean rows:                 302
objective-unique rows:               284
geometry-clean fraction:             0.934985
objective-unique fraction:           0.879257
target0:                             exact strong 3, geometry clean 3, objective unique 3
target1:                             exact strong 53, geometry clean 53, objective unique 44
target2:                             exact strong 267, geometry clean 246, objective unique 237
gpu priority:                        none_now
```

Run 1289 / experiment 811 maps objective-uniqueness caveats to acquisition
metadata:

```text
objective_uniqueness_gap_map_known_target2_x_gaps_cpu_no_gpu
exact-strong rows:                    323
near-tie rows:                        39
known-acquisition near-tie rows:       6
archive-metadata near-tie rows:       33
target1 known-acquisition near ties:   0
target2 known-acquisition near ties:   6
known actionable x-gap cells:          3
top actionable target:                 target2
top actionable sources/TxRx:           5 sources, Tx/Rx=45 mm
gpu priority:                          none_now
```

Run 1290 / experiment 812 adds family context to those objective-uniqueness
caveats:

```text
objective_uniqueness_family_context_close14_target2_cpu_no_gpu
family cells:                         13
near-tie rows:                        39
known close14 target2 x near ties:     4
known target2 depth/radius near ties:  2
target1 legacy archive near ties:      9
target2 close50 known near ties:       0
gpu priority:                          none_now
```

Run 1291 / experiment 813 tests close14 target2 objective-threshold
sensitivity:

```text
close14_target2_objective_threshold_sensitivity_source5_persistent_cpu_no_gpu
default-scale row count:              102
near ties at 0.5x threshold:            2
near ties at 0.75x threshold:           2
near ties at 1.0x threshold:            4
near ties at 1.25x threshold:          48
source5 Tx/Rx45 near ties at 0.5x:      2
source5 Tx/Rx45 near ties at 1.0x:      2
source4 Tx/Rx45 default edge count:     1
source7 Tx/Rx45 default edge count:     1
source4 Tx/Rx50 default near ties:      0
source4 Tx/Rx50 near ties at 1.25x:    38
gpu priority:                          none_now
```

Run 1292 / experiment 814 refreshes the synthetic next-question matrix:

```text
synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate count:                   8
cpu-first count:                   1
immediate GPU-priority count:      0
conditional GPU candidates:        2
top question:                      target2_close14_source5_threshold_gate
top question GPU readiness:        cpu_first
gpu priority:                      none_now
```

Run 1293 / experiment 815 builds the fixed target2 close14 probe contract:

```text
target2_close14_source5_txrx45_probe_contract_skip_existing_cpu_no_gpu
contract status:                 ready_but_not_launched
probe target:                    target2_close14_source5_txrx45
seed count:                      3
existing seeds:                  34
missing seeds:                   13,21
source5 Tx/Rx45 near ties 0.5x:  2
source5 Tx/Rx45 near ties 1.0x:  2
next question:                   target2_close14_source5_threshold_gate
gpu priority:                    low_conditional_not_launched
```

Runs 1294-1295 complete the missing target2 close14 source5 / Tx/Rx=45 mm
probe seeds one at a time under the local resource policy:

```text
1294 seed13:
  runtime:                       1853.6 s
  truth geometry selected:       2 / 2 cases
  strong radius confidence:      2 / 2 cases
  x=265 mm competitor:           inside 0.5x gate in 2 / 2 cases
  measured GPU utilization:      about 87%

1295 seed21:
  runtime:                       1860.8 s
  truth geometry selected:       2 / 2 cases
  strong radius confidence:      2 / 2 cases
  x=265 mm competitor:           inside 0.5x gate in 2 / 2 cases
  measured GPU utilization:      about 86-87%
```

Run 1296 aggregates seed13, seed21, and the existing seed34 result:

```text
coordinate_confidence_close14_target2_sources5_txrx45_seed13_21_34_probe_aggregate
rows:                          6
truth geometry selected:       6 / 6
strong confidence rows:        6 / 6
x-ambiguity rows:              6 / 6
max x-ambiguity width:         1.000 mm
radius margin min/max:         0.001500 / 0.002458
```

Run 1297 / experiment 816 synthesizes the three-seed decision:

```text
target2_close14_source5_txrx45_three_seed_persistent_x_near_tie
seeds:                         13,21,34
near ties at 0.5x gate:        6 / 6
near ties at 1.0x gate:        6 / 6
competing x geometry:          265.0 mm
decision:                      robust objective-uniqueness limit
gpu priority for exact probe:  none
```

Runs 1298-1299 / experiment 817 refresh the synthetic decision matrix and
claim boundaries after the close14 probe:

```text
1298 post-close14 next-question matrix:
  candidate count:                8
  top question:                   post_close14_claim_boundary_refresh
  immediate GPU-priority count:   0
  conditional GPU candidates:     1
  gpu priority:                   none_now

1299 post-close14 claim-boundary refresh:
  policy label:                   synthetic_2d_publication_claim_boundaries_close14_limit_cpu_no_gpu
  claim boundary count:           8
  close14 probe included:         true
  close14 0.5x near-tie count:    6
  ready for manuscript table:     true
  gpu priority:                   none
```

Runs 1300-1303 / experiment 818 close the close50 target2 linear 29.5 mm
seed-frequency question:

```text
1300 post-claim next-question matrix:
  top question:                   close50_sub30_seed_frequency_contract
  conditional GPU candidates:     1
  gpu priority:                   none_now

1301 close50 linear 29.5 mm contract:
  existing seeds:                 13,21
  missing seeds:                  34
  resource policy:                run only seed34, GPU <=90%, RAM <=80%
  decision rule:                  estimate ambiguity frequency, not threshold promotion

1302 seed34 close50 linear 29.5 mm GPU probe:
  runtime:                        1536.1 s
  truth geometry selected:        2 / 2 cases
  strong confidence rows:         2 / 2 cases
  x-ambiguity rows:               0 / 2 cases
  highband truth rows:            2 / 2 cases
  measured GPU utilization:       about 85-86%

1303 three-seed frequency policy:
  policy label:                   close50_linear29p5_three_seed_exact_strong_not_clean_replicated
  seeds:                          seed13,seed21,seed34
  truth geometry rows:            6 / 6
  strong confidence rows:         6 / 6
  strict-clean rows:              5 / 6
  x-ambiguity rows:               1 / 6
  strict-clean seeds:             seed21,seed34
  ambiguous seeds:                seed13
```

The legacy close50 270/280 concern remains resolved by later close50 threshold
evidence. Do not repeat the old Tx/Rx=40 target2 branch. Run 1308 now refreshes
that conclusion with the 27.5 mm and 28.75 mm single-seed midpoint pilots.
The current close50 policy remains:

```text
nearest-sampled first clean replicated offset: 30 mm
27.5/28.75 mm nearest-sampled midpoint pilots: exact but non-clean
29.5 mm linear branch: exact and strong in 3/3 seeds, but not clean-replicated
seed-frequency caveat: seed13 is x-ambiguous; seed21 and seed34 are strict-clean
```

Runs 1304-1306 / experiment 819 refresh the synthetic policy after the close50
seed-frequency branch:

```text
1304 post-close50 next-question matrix:
  top question:                   post_close50_claim_boundary_refresh
  conditional GPU candidates:     0
  gpu priority:                   none_now

1305 post-close50 claim-boundary refresh:
  policy label:                   synthetic_2d_publication_claim_boundaries_close14_close50_limits_cpu_no_gpu
  claim boundary count:           9
  close14 probe included:         true
  close50 seed policy included:   true
  close50 ambiguous seeds:        seed13
  gpu priority:                   none

1306 post-refresh next-question matrix:
  top question:                   synthetic_claim_boundaries_current
  cpu-first candidates:           0
  conditional GPU candidates:     0
  gpu priority:                   none_now
```

Run 1307 / experiment 820 builds the current synthetic 2D resolution-claim map:

```text
policy label:                     synthetic_2d_resolution_claim_map_close14_close50_current_cpu_no_gpu
map rows:                         8
physical non-overlap guardrail:   14 mm
overlap-stress min clean spacing: 10 mm
target2 close14 0.5x near ties:   6
target2 close50 strict-clean seeds: 2 / 3
target2 close50 ambiguous seed:   seed13
conditional GPU candidates:       0
gpu priority:                     none_now
```

Run 1308 / experiment 821 refreshes the close50 legacy 270/280 audit against
the later midpoint evidence:

```text
policy label:                     close50_target2_threshold_refined_midpoint_not_clean
first clean replicated offset:    30 mm
ambiguous replicated offset:      25 mm
single-seed non-clean midpoints:  27.5, 28.75 mm
clean replicated offsets:         30, 35, 40 mm
threshold rows:                   36
single-seed midpoint rows:        6
gpu priority:                     none
```

Run 1309 / experiment 822 refreshes the paper-facing synthetic 2D publication
bundle so it includes the current resolution map and the midpoint-aware 270/280
answer:

```text
policy label:                     synthetic_2d_publication_bundle_current_resolution_map_ready_gpu_priority_none
figure rows:                      7
validated figures:                7 / 7
claim boundaries:                 5
current resolution map included:  true
close50 legacy refresh included:  true
gpu priority:                     none
ready for manuscript draft:       true
```

Run 1310 / experiment 823 refreshes the synthetic next-question matrix after
the paper-facing bundle was made current:

```text
policy label:                     synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate rows:                   8
cpu-first candidates:             0
conditional GPU candidates:       0
top question:                     synthetic_publication_bundle_current
top readiness:                    no_gpu_required
gpu priority:                     none_now
```

Run 1311 / experiment 824 builds the current synthetic 2D acquisition tradeoff
map from existing resolution, Tx/Rx, source-count, and next-question evidence:

```text
policy label:                     synthetic_2d_acquisition_tradeoff_cpu_no_gpu
tradeoff rows:                    12
tight-spacing reference Tx/Rx:    45 mm
close14 minimum clean Tx/Rx:      45 mm
target1 best source-count setting target1 sources=5
target1 source-density status:    source_density_nonmonotonic
target2 archive best Tx/Rx:       target2 Tx/Rx=50 mm
nonmonotonic source-count targets:3
conditional GPU candidates:       0
gpu priority:                     none_now
```

Run 1312 / experiment 825 builds a target1 acquisition-confidence surface from
the existing 700-1259 archive tables:

```text
policy label:                     target1_acquisition_confidence_surface_exact_but_nonmonotonic_cpu_no_gpu
canonical target1 rows:           133
exact target1 geometry rows:      133
base accepted rows:                90
base weak-exact rows:              43
late_high truth rows:             133
late_high accepted rows:          132
best source count, min n=5:         5 sources
best Tx/Rx, min n=3:               60 mm
source-density series:             17
source escalation helped:          10
lower source count was best:        7
terminal 11-source branches worse:  2 / 2
gpu priority:                      none_now
```

Run 1313 / experiment 826 refreshes the synthetic next-question matrix after
the target1 acquisition-confidence surface:

```text
policy label:                     synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate rows:                   9
cpu-first candidates:             0
conditional GPU candidates:       0
target1 surface included:         true
top question:                     synthetic_publication_bundle_current
top readiness:                    no_gpu_required
gpu priority:                     none_now
```

Run 1314 / experiment 827 maps target1 source-density exceptions to branch
actions:

```text
policy label:                     target1_source_density_exception_map_no_gpu
source-density series:            17
source-density run rows:          42
all late_high-confirmed series:   16
legacy exception series:           1
modern exception series:           0
terminal 11-source series:         2
terminal 11-source worse:          2
terminal 11-source confirmed:      2
source escalation helped:         10
lower source count best/equal:     7
legacy exception run IDs:        785
recommended GPU action:          none_target1_source_density
gpu priority:                    none
```

Run 1315 / experiment 828 refreshes the synthetic next-question matrix after
the target1 source-density exception map:

```text
policy label:                    synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate rows:                  10
cpu-first candidates:             0
immediate GPU candidates:         0
conditional GPU candidates:       0
target1 surface included:         true
target1 exception map included:   true
top question:                    synthetic_publication_bundle_current
top readiness:                   no_gpu_required
gpu priority:                    none_now
```

Run 1316 / experiment 829 runs one bounded close50 target2 nearest-sampled
Tx/Rx=28.75 mm seed13 replicate:

```text
run name:                        coordinate_optimizer_close50_seed13_sources4_txrx28p75_objectives
backend:                         gpu-cpml
receiver sampling:               nearest
target:                          target2
final geometry:                  x=300 mm, z=90 mm, r=8.0 mm
nominal margin:                  1.8985e-03, strong
source-mismatch margin:          1.7138e-03, strong
highband diagnostic:             truth geometry for both cases
strict clean:                    no; nominal x ambiguity spans 300-301 mm
elapsed:                         1527.5 s
```

Run 1317 / experiment 829 refreshes the close50 270/280 legacy audit with the
new seed13 28.75 mm replicate:

```text
policy label:                    close50_target2_threshold_refined_replicated_midpoint_not_clean
first clean Tx/Rx:                30 mm
non-clean offsets:                25, 27.5, 28.75 mm
clean offsets:                    30, 35, 40 mm
replicated non-clean midpoint:    28.75 mm
threshold scope:                  target2 only
```

Run 1318 / experiment 829 refreshes the paper-facing synthetic 2D publication
bundle so it points at run 1317 instead of the older run 1308 close50 legacy
refresh:

```text
policy label:                    synthetic_2d_publication_bundle_current_resolution_map_ready_gpu_priority_none
figure count:                    7
validated figures:               7 / 7
claim boundaries:                5
ready for manuscript draft:      true
gpu priority:                    none
```

Run 1319 / experiment 829 refreshes the synthetic next-question matrix after
the replicated-midpoint publication-bundle refresh:

```text
policy label:                    synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate rows:                  10
cpu-first candidates:             0
immediate GPU candidates:         0
conditional GPU candidates:       0
target1 surface included:         true
target1 exception map included:   true
top question:                    synthetic_publication_bundle_current
top readiness:                   no_gpu_required
gpu priority:                    none_now
```

Run 1320 / experiment 830 refreshes the paper-facing synthetic publication
bundle so it includes the current target1 acquisition-confidence and
source-density policy figures:

```text
policy label:                    synthetic_2d_publication_bundle_current_resolution_target1_ready_gpu_priority_none
figure count:                    9
validated figures:               9 / 9
claim boundaries:                6
target1 policy figures included: true
ready for manuscript draft:      true
gpu priority:                    none
```

Run 1321 / experiment 830 refreshes the synthetic next-question matrix after
the target1-aware publication-bundle refresh:

```text
policy label:                    synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate rows:                  10
cpu-first candidates:             0
immediate GPU candidates:         0
conditional GPU candidates:       0
target1 surface included:         true
target1 exception map included:   true
top question:                    synthetic_publication_bundle_current
top readiness:                   no_gpu_required
gpu priority:                    none_now
```

Run 1322 / experiment 831 reconciles the current synthetic paper-facing bundle
with the detailed claim-boundary rows from the older close14/close50 claim
refresh:

```text
policy label:                    synthetic_2d_publication_bundle_current_resolution_target1_claims_ready_gpu_priority_none
figure count:                    9
validated figures:               9 / 9
claim boundaries:                11
target1 policy figures included: true
detailed claim boundaries:       true
ready for manuscript draft:      true
gpu priority:                    none
```

Run 1323 / experiment 831 refreshes the synthetic next-question matrix after
claim-boundary reconciliation:

```text
policy label:                    synthetic_2d_next_question_matrix_cpu_first_no_gpu
candidate rows:                  10
cpu-first candidates:             0
immediate GPU candidates:         0
conditional GPU candidates:       0
top question:                    synthetic_publication_bundle_current
top readiness:                   no_gpu_required
gpu priority:                    none_now
```

Current synthetic GPU posture:

```text
No immediate synthetic GPU run is justified by the current policy evidence.
The target0 modern ringdown050 exception is closed by existing source-density
follow-up, and the remaining target1 exception is legacy ringdown025 archive
evidence rather than a GPU-priority branch. Run 1314 makes this explicit:
there are zero modern target1 source-density exceptions and both terminal
11-source branches are worse than their first setting, so source-density
escalation should not be extended as a rescue rule. The synthetic publication bundle
keeps this at gpu_priority=none. The refreshed run 1310 next-question matrix
ranks the current synthetic publication bundle as the top completed endpoint
and shows zero CPU-first or conditional GPU candidates. Run 1315 is the current
next-question matrix after adding both the target1 acquisition-confidence
surface and the target1 source-density exception map; it still has zero
CPU-first or conditional GPU candidates. Run 1311 adds an
acquisition-design tradeoff map: Tx/Rx=45 mm is the current tight-spacing
reference, Tx/Rx=35 mm supports mid-spacing branches, and source-count effects
are nonmonotonic across all three targets. Runs 1316-1319 add one narrow
close50 replicated-midpoint check: nearest-sampled 28.75 mm is now replicated
non-clean, but 30 mm remains the first clean replicated close50 target2 offset,
and the refreshed matrix still has zero immediate or conditional GPU
candidates. Run 1307 adds a resolution-claim map
for manuscript wording: close14 is the tangent
non-overlap guardrail for the current 6 mm + 8 mm target1/target2 pair,
close10/close12 remain overlap stress tests, close14 source5 / TxRx45 is a
robust objective-uniqueness limit, and close50 linear 29.5 mm remains
exact/strong but not clean-replicated.
Run 1280 implements the reporting metric: paper_clean_candidate requires truth,
strong confidence, zero x-ambiguity width, and zero radius-ambiguity width.
Run 1281 shows that this is not only a close50 sub-30 caveat: 19 exact-strong
archive rows have nonzero x ambiguity and should not be reported as strict
location-clean thresholds. Run 1282 further shows that all strict-clean
exceptions are target2 archive-family caveats, not target0/target1 modern open
exceptions. Run 1283 shows those target2 caveats are objective near-ties inside
the ambiguity threshold, mostly one-grid-cell lateral competitors. Run 1284
separates strict location-clean geometry from objective-margin separation:
9 target2 rows are location-clean but still have zero-width objective near-ties.
Run 1285 shows the zero-width near-tie caveat also affects target1, while
geometry ambiguity remains target2-only.
Run 1286 packages those distinctions into a refreshed manuscript claim-boundary
table.
Run 1287 further tightens objective-uniqueness wording: ambiguity-width-only
metrics miss 18 zero-width rows with raw competing-geometry deltas.
Run 1288 is the current synthetic manuscript table endpoint for exact-strong,
geometry-clean, and objective-unique tiers.
Run 1289 shows the actionable known-acquisition objective-uniqueness gaps are
target2-only; target1 caveats are archive rows with missing source/TxRx
metadata. Any future GPU work should therefore be a narrow target2 x-resolution
probe after CPU objective scope is fixed, not a broad sweep.
Run 1290 further narrows that target2 x-resolution caveat to the close14
family, not close50, and separates the variable-depth/radius caveat from
close-spacing x-resolution.
Run 1291 shows that the source5/TxRx45 close14 target2 x caveat persists under
a 0.5x ambiguity threshold, while source4/source7 TxRx45 are default-threshold
edge cases and TxRx50 is clean at the default threshold but sensitive if the
threshold is loosened. This fixes the current objective gate before any
possible narrow GPU probe.
Run 1292 makes that the current synthetic next-question matrix: define a fixed
probe contract and manuscript decision rule before any GPU run; no candidate
currently justifies immediate or broad GPU execution.
Run 1293 defines that fixed contract. Seed34 is already present, seeds 13 and
21 are the only missing commands, and any later launch should run at most one
missing seed at a time with GPU <=90% and RAM <=80%. The decision rule is
fixed before launch: persistent 0.5x-threshold near ties across multiple seeds
support a robust objective-uniqueness limitation; disappearance outside seed34
supports a seed-specific caveat.
Runs 1294-1297 executed that fixed contract. The outcome is not a seed34-only
caveat: all six seed/case rows select truth with strong radius confidence, but
all six retain the +1 mm x competitor inside the 0.5x ambiguity gate. Treat
target2 close14 source5 / Tx/Rx=45 mm as a robust objective-uniqueness limit,
not as clean lateral resolution. No more GPU work is justified for this exact
probe.
Runs 1298-1299 move that result into the current synthetic next-question and
manuscript claim-boundary tables. The top synthetic action is now CPU-side
claim discipline, and the exact close14 source5 / Tx/Rx=45 mm GPU probe is
closed unless the research question changes.
Runs 1300-1303 close the only post-claim-refresh close50 conditional branch:
the single missing seed34 probe is strict-clean, so the close50 linear 29.5 mm
evidence is exact and strong across three seeds but not clean-replicated because
seed13 remains an x-ambiguity caveat. Keep the paper-safe clean threshold at
the nearest-sampled 30 mm result.
Runs 1304-1306 move that close50 caveat into the manuscript claim-boundary
table alongside the close14 objective-limit result. The current synthetic
next-question matrix now has zero CPU-first and zero conditional GPU
candidates under the already-posed local 2D questions.
Run 1307 packages these boundaries into the current synthetic resolution table:
physical spacing guardrails, archive claim tiers, objective-uniqueness limits,
and seed-frequency caveats stay separate.
Run 1308 answers the 270/280 close50 legacy concern with current midpoint
evidence: the old Tx/Rx=40 target2 branch does not need to be repeated, and
sub-30 nearest-sampled midpoint pilots remain non-clean under the current
confidence/ambiguity policy.
Run 1309 makes the synthetic paper-facing bundle current again by adding the
1307 resolution map and 1308 close50 legacy refresh to the older figure bundle.
Run 1310 makes the synthetic next-question matrix current after that bundle
refresh: the top row is now the completed publication-bundle endpoint, with
zero CPU-first and zero conditional GPU candidates under the already-posed
local 2D questions. Run 1311 adds a current acquisition tradeoff synthesis:
the paper can discuss acquisition-specific behavior, but source-count
escalation is not a monotonic rescue policy and Tx/Rx patterns are target and
spacing dependent. Run 1312 deepens the target1 part of that statement: all
canonical target1 rows preserve exact geometry, while base confidence remains
acquisition-sensitive and source-density escalation is nonmonotonic. Run 1313
keeps that target1 result in the current next-question endpoint without turning
it into a GPU queue item. Only launch a new GPU run if a new question is
specified, such as a different objective definition, a new geometry, or a
deliberately narrow exception probe.
Run 1320 makes the paper-facing synthetic bundle current for target1 as well:
it now includes the 1312 target1 acquisition-confidence surface and the 1314
source-density exception map. Run 1321 keeps the queue unchanged after that
publication refresh: zero CPU-first, zero immediate GPU, and zero conditional
GPU candidates. Target1 source-count reruns remain closed unless a new
objective definition, geometry, or acquisition hypothesis is introduced.
```

## Field-Data Status

Field work remains separate from synthetic trackers under:

```text
outputs/field_experiments/local_gssi_51600s_2026_06_09
docs/field_experiments/local_gssi_51600s_2026_06_09
```

New field runs 043-054 extended the content-anchor time-zero work from
trace-level checks to B-scan-level profile QC:

```text
043 corrected profile stack:
  raw matrix abs corr        0.535682
  corrected matrix abs corr  0.812268
  matrix improvement         0.276586
  improved columns           161 / 249

045 corrected stack sensitivity:
  robust windows             3 / 3
  min matrix improvement     0.263036
  min corrected matrix corr  0.799200
  min improved-column frac   0.606426

047 spatial support:
  majority-supported columns 105 / 249
  all-window-supported cols   70 / 249
  largest supported interval  0.069993 m

049 supported interval visual QC:
  selected all-window intervals 3
  total selected length         0.166650 m
  min corrected interval corr   0.909285
  min interval improvement      0.363612

051 long-profile transfer audit:
  raw matrix abs corr           0.763452
  corrected matrix abs corr     0.732421
  matrix change                -0.031031
  stable anchor windows         6
  improved anchor windows       0

053 long-profile shift scan:
  zero-offset matrix abs corr    0.763452
  short-pair offset matrix corr  0.719581
  short-pair gain vs zero       -0.043871
  best pattern-only offset       0.060000 ns
  best matrix abs corr           0.938531
  best improved anchor windows   6

055 long-profile shift sensitivity:
  tested windows                  3
  rejecting short transfer        3
  best offset median              0.060000 ns
  best offset spread              0.000000 ns
  min best gain vs zero           0.150305
  max short-pair gain vs zero    -0.034047

057 long-profile pattern visual QC:
  pattern shift                   0.060000 ns
  selected anchor windows         6
  supported anchor windows        6
  min pattern-shift gain          0.019532
  min shifted abs corr            0.889509

058 long-profile pattern holdout QC:
  candidate anchor windows         8
  stable supported windows         6 / 6
  repeat-limited supported windows 2 / 2
  min stable gain                  0.019532
  min repeat-limited gain          0.172819
  min repeat-limited shifted corr  0.961006

059 field publication claim bundle:
  figure rows                       5
  claim boundaries                  5
  geometry classification           independent_2d_line_profiles
  ready for manuscript supplement   true
  gpu priority                      none

060 long-profile pattern holdout sensitivity:
  tested windows                    3
  candidate anchors                 8
  all-window supported anchors      8
  stable all-window supported       6 / 6
  repeat-limited all-window support 2 / 2
  supported rows                    24 / 24
  min pattern-shift gain            0.001818
  min shifted abs corr              0.873226

061 long-profile pattern holdout width sensitivity:
  tested half-widths                 35, 50, 75 mm
  candidate anchors                 8
  all-width supported anchors        8
  widths with all anchors supported  3 / 3
  stable all-width supported         6 / 6
  repeat-limited all-width support   2 / 2
  supported rows                     24 / 24
  min pattern-shift gain             0.019532
  min shifted abs corr               0.888491

062 field publication claim bundle refresh:
  figure rows                        7
  claim boundaries                   6
  geometry classification            independent_2d_line_profiles
  long time-window sensitivity ready true
  long spatial-width sensitivity     true
  ready for manuscript supplement    true
  gpu priority                       none

063 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  survey classification              independent_2d_line_profiles
  embedded segment candidates         0
  long visual supported anchors       6 / 6
  long holdout supported anchors      8 / 8
  long window supported rows          24 / 24
  long width supported rows           24 / 24
  publication bundle ready            true
  field gpu/fwi priority              none

064 relaxed long-profile phase-anchor audit:
  requested profiles                  2
  profiles with relaxed picks          2
  relaxed phase-anchor picks          10
  low-SNR picks                       10 / 10
  best phase convention               cue_time
  best median depth                   102.5 mm
  best boundary solution count          1

065 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  relaxed-anchor policy              long_profile_relaxed_phase_anchor_low_snr_not_time_zero
  relaxed pick count                  10
  relaxed low-SNR pick count          10
  relaxed boundary solution count      1
  field gpu/fwi priority              none

066 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_relaxed_anchor_negative_ready_not_fwi
  figure rows                        8
  claim boundaries                   7
  relaxed phase-anchor included      true
  relaxed low-SNR pick count         10 / 10
  ready for manuscript supplement    true
  field gpu/fwi priority             none

067 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_relaxed_anchor_negative_ready_not_fwi
  publication figure rows            8
  publication claim boundaries       7
  relaxed-anchor policy              long_profile_relaxed_phase_anchor_low_snr_not_time_zero
  field gpu/fwi priority             none

068 field band-limited repeatability audit:
  policy label                       field_bandlimited_repeatability_short_pair_supported_long_pattern_only
  short raw/corrected abs corr        0.545551 -> 0.771287
  short supported bands               low, mid_low, mid_high, broad
  long raw/pattern abs corr           0.789502 -> 0.905584
  long pattern-supported bands        mid_low, mid_high, high, broad
  field gpu/fwi priority              none

069 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  band policy included                field_bandlimited_repeatability_short_pair_supported_long_pattern_only
  short band-supported count          4
  long pattern band-supported count   4
  survey classification               independent_2d_line_profiles
  field gpu/fwi priority              none

070 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_bandlimited_relaxed_anchor_ready_not_fwi
  figure rows                        9
  claim boundaries                   8
  bandlimited figure included        true
  ready for manuscript supplement    true
  field gpu/fwi priority             none

071 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_bandlimited_relaxed_anchor_ready_not_fwi
  publication figure rows            9
  publication claim boundaries       8
  band policy included                field_bandlimited_repeatability_short_pair_supported_long_pattern_only
  field gpu/fwi priority             none

072 field event-support tier table:
  policy label                       field_event_support_tiers_2d_qc_ready_not_fwi
  tier rows                          9
  short content-backed anchors       2 / 3 event pairs
  long pattern-supported anchors     8 total
  blocked rows                       1
  field gpu/fwi priority             none

073 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_event_tiers_bandlimited_relaxed_ready_not_fwi
  figure rows                        10
  claim boundaries                   9
  event-support tiers included       true
  ready for manuscript supplement    true
  field gpu/fwi priority             none

074 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_event_tiers_bandlimited_relaxed_ready_not_fwi
  publication figure rows            10
  publication claim boundaries       9
  survey classification              independent_2d_line_profiles
  field gpu/fwi priority             none

075 field time-zero uncertainty budget:
  policy label                       field_time_zero_uncertainty_budget_short_pair_relative_qc_not_absolute
  budget rows                        13
  relative anchor offset              0.127701 ns
  bootstrap CI                        0.108055 to 0.147348 ns
  conservative half-width             0.058939 ns
  content anchor support              2 / 3 event pairs
  trace-window support                6 / 6
  absolute time-zero ready            false
  field gpu/fwi priority              none

076 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_time_zero_event_tiers_bandlimited_relaxed_ready_not_fwi
  figure rows                        11
  claim boundaries                   10
  time-zero uncertainty included      true
  time-zero conservative half-width   0.058939 ns
  ready for manuscript supplement     true
  field gpu/fwi priority              none

077 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_time_zero_event_tiers_bandlimited_relaxed_ready_not_fwi
  publication figure rows            11
  publication claim boundaries       10
  publication time-zero budget        true
  publication absolute ready          false
  survey classification              independent_2d_line_profiles
  field gpu/fwi priority             none

078 field time-zero perturbation sensitivity:
  policy label                       field_time_zero_ci_perturbation_stack_robust
  tested offsets                     7
  tested windows                     3
  supported rows                     18 / 21
  raw/no-correction support           0 / 3
  nominal support                     3 / 3
  bootstrap-CI support                9 / 9
  conservative-envelope support       6 / 6
  minimum nonraw matrix improvement   0.125152
  field gpu/fwi priority              none

079 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  figure rows                        12
  claim boundaries                   11
  time-zero perturbation included     true
  perturbation bootstrap support      9 / 9
  perturbation conservative support   6 / 6
  ready for manuscript supplement     true
  field gpu/fwi priority              none

080 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  publication figure rows            12
  publication claim boundaries       11
  publication perturbation policy     field_time_zero_ci_perturbation_stack_robust
  survey classification              independent_2d_line_profiles
  field gpu/fwi priority             none

081 field acquisition/HPC readiness audit:
  policy label                       field_acquisition_readiness_2d_qc_not_hpc_fwi
  scan spacing                       3.333 mm
  nominal in-medium wavelength       124.914 mm
  samples per wavelength             37.478
  time-zero half-width               0.058939 ns
  two-way depth equivalent           5.890 mm
  all-window spatial support          70 / 249 columns
  ready for 2D QC                    true
  ready for 3D HPC                   false
  ready for field FWI                false
  field HPC priority                 none

082 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  figure rows                        13
  claim boundaries                   12
  acquisition readiness included     true
  ready for 3D HPC                   false
  ready for field FWI                false
  ready for manuscript supplement    true
  field gpu/fwi priority             none

083 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  publication figure rows            13
  publication claim boundaries       12
  publication acquisition readiness  true
  publication ready for 3D HPC       false
  publication ready for field FWI    false
  field HPC priority                 none
  field gpu/fwi priority             none

084 field apparent-depth scale QC:
  policy label                       field_apparent_depth_qc_relative_scale_not_cover_depth
  reflector cue count                19
  short-profile cue count             9
  long-profile cue count             10
  apparent depth scale                69.696 to 276.822 mm
  content-backed short pairs           2 / 3
  corrected rows inside depth budget   3 / 3
  mean raw depth residual             13.743 mm
  mean corrected depth residual        2.290 mm
  max corrected depth residual         4.908 mm
  conservative depth-equivalent budget 5.890 mm
  cover-depth recovery ready           false
  field FWI ready                     false
  gpu priority                        none

085 field apparent-depth sensitivity:
  policy label                       field_apparent_depth_sensitivity_not_calibrated_cover_depth
  sensitivity scenarios               5
  epsr range                          2.25 to 11.10
  max apparent cue depth range         126.906 to 276.822 mm
  max apparent cue depth span          149.916 mm
  max apparent cue depth factor        2.18x
  residual support across scenarios    5 / 5
  cover-depth claim ready              false
  field FWI ready                      false
  gpu priority                         none

086 field hyperbola/time-zero degeneracy audit:
  policy label                       field_hyperbola_timezero_degeneracy_not_calibrated_inversion
  surface summary rows                4
  offset summary rows                 2
  boundary best-fit surfaces          3 / 4
  max near-top epsr span              4.085
  max near-top time-zero span         0.300 ns
  max near-top offset count, 5% gate  5
  cover-depth claim ready             false
  radius claim ready                  false
  field FWI ready                     false
  gpu priority                        none

087 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  evidence rows                       31
  apparent-depth QC policy            field_apparent_depth_qc_relative_scale_not_cover_depth
  apparent-depth max residual         4.908 mm
  time-zero depth-equivalent budget   5.890 mm
  apparent-depth sensitivity policy   field_apparent_depth_sensitivity_not_calibrated_cover_depth
  apparent-depth sensitivity factor   2.18x
  hyperbola/time-zero policy          field_hyperbola_timezero_degeneracy_not_calibrated_inversion
  boundary best-fit surfaces          3 / 4
  cover-depth claim ready             false
  radius claim ready                  false
  field FWI ready                     false

088 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  figure rows                        16
  claim boundaries                   15
  apparent-depth QC included         true
  apparent-depth sensitivity included true
  hyperbola/time-zero degen included true
  ready for manuscript supplement    true
  field gpu/fwi priority             none

089 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  publication figure rows            16
  publication claim boundaries       15
  apparent-depth QC policy           field_apparent_depth_qc_relative_scale_not_cover_depth
  hyperbola/time-zero policy         field_hyperbola_timezero_degeneracy_not_calibrated_inversion
  field gpu/fwi priority             none

090 field early-time anchor audit:
  policy label                       field_early_time_common_mode_not_content_time_zero
  primary early window                0.00-0.55 ns
  early peak median time              0.235756 ns
  early peak span across profiles     0.000000 ns
  short-pair early lag                0.000000 ns
  short-pair early correlation        0.999798
  content-backed short offset         0.127701 ns
  conservative half-width             0.058939 ns
  early/content delta                 0.127701 ns
  absolute time-zero ready            false
  field FWI ready                     false
  gpu priority                        none

091 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  figure rows                        17
  claim boundaries                   16
  early-time anchor included          true
  ready for manuscript supplement    true
  field gpu/fwi priority             none

092 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  publication figure rows            17
  publication claim boundaries       16
  early-time absolute ready           false
  field gpu/fwi priority             none

093 field cue-spacing context audit:
  policy label                       field_cue_spacing_context_not_resolution_benchmark
  cue count                          19
  same-time lateral pairs             21
  min same-time lateral spacing       269.973 mm
  min distinct-x spacing, any time    96.657 mm
  resolution benchmark ready          false
  field FWI ready                     false
  3D HPC ready                        false
  gpu priority                        none

094 field cue-spacing threshold sensitivity:
  policy label                       field_cue_spacing_context_threshold_robust_not_resolution_benchmark
  thresholds                          0.050,0.100,0.150,0.200,0.300,0.500,1.000 ns
  min same-time spacing across gates  96.657 mm
  max same-time lateral pairs         32
  all thresholds wider than close scale true
  resolution benchmark ready          false
  field FWI ready                     false
  3D HPC ready                        false
  gpu priority                        none

095 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  figure rows                        18
  claim boundaries                   17
  cue-spacing context included       true
  cue context ready                  true
  cue resolution benchmark ready     false
  cue field FWI ready                false
  ready for manuscript supplement    true
  field gpu/fwi priority             none

096 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  publication figure rows            18
  publication claim boundaries       17
  publication cue min spacing        96.657 mm
  publication cue field FWI ready    false
  field gpu/fwi priority             none

097 field timing-anchor conflict synthesis:
  policy label                       field_timing_anchor_conflict_short_relative_not_absolute
  anchor rows                        7
  guardrail rows                     7
  claim boundaries                   4
  short content-backed offset        0.127701 ns
  short conservative half-width      0.058939 ns
  early/common-mode shift            0.000000 ns
  long pattern-only offset           0.060000 ns
  early vs short delta / half-width  2.167
  long vs short delta / half-width   1.149
  long rejects short transfer        true
  perturbation budget supported      true
  absolute time-zero ready           false
  field FWI ready                    false
  gpu priority                       none

098 field publication bundle refresh:
  policy label                       field_publication_claim_bundle_2d_qc_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  figure rows                        19
  claim boundaries                   18
  timing-anchor conflict included    true
  timing early/short delta halfwidth 2.167
  timing long/short delta halfwidth  1.149
  timing absolute time-zero ready    false
  timing field FWI ready             false
  ready for manuscript supplement    true
  field gpu/fwi priority             none

099 field dataset policy refresh:
  policy label                       field_2d_qc_not_3d_or_fwi
  publication bundle policy          field_publication_claim_bundle_2d_qc_timing_anchor_cue_spacing_early_time_depth_degen_acquisition_time_zero_perturbation_event_tiers_bandlimited_relaxed_ready_not_fwi
  publication figure rows            19
  publication claim boundaries       18
  publication timing boundary ready  true
  publication timing field FWI ready false
  field gpu/fwi priority             none
```

Latest dataset policy refresh 099 is now:

```text
field_2d_qc_not_3d_or_fwi
```

Latest field acquisition/HPC readiness audit 081 records:

```text
field_acquisition_readiness_2d_qc_not_hpc_fwi
```

Latest standalone field cue-spacing context audits 093-094 record:

```text
field_cue_spacing_context_not_resolution_benchmark
field_cue_spacing_context_threshold_robust_not_resolution_benchmark
```

Paper-facing field figure bundle:

```text
docs/field_experiments/local_gssi_51600s_2026_06_09/paper_field_figure_bundle_2026_06_17.md
outputs/field_experiments/local_gssi_51600s_2026_06_09/095_gssi51600s_field_publication_claim_bundle_post_cue_spacing_context/data/field_publication_claim_boundaries.csv
outputs/field_experiments/local_gssi_51600s_2026_06_09/098_gssi51600s_field_publication_claim_bundle_post_timing_anchor_conflict/data/field_publication_claim_boundaries.csv
```

Paper-facing synthetic 2D figure bundle:

```text
outputs/experiments/1322_synthetic_2d_publication_figure_bundle_post_claim_boundary_reconciliation
docs/experiments/831_synthetic_2d_claim_boundary_reconciliation.md
```

Cross-bundle manuscript evidence audit:

```text
outputs/summary_tables/006_local_2d_field_manuscript_evidence_audit
policy label:                      local_2d_field_manuscript_evidence_ready_no_gpu
domains:                           2
constituent figure files:          28 / 28 validated
claim boundaries:                  29 / 29 complete
synthetic ready:                   true
field ready:                       true
cross-domain guards present:       true
gpu priority:                      none
```

Manuscript table pack:

```text
outputs/summary_tables/007_local_2d_field_manuscript_table_pack
policy label:                      local_2d_field_manuscript_table_pack_ready_no_gpu
claim table rows:                  29
figure inventory rows:             28
metric rows:                       13
synthetic claims / figures:        11 / 9
field claims / figures:            18 / 19
synthetic source figure notes:     9 / 9
field cue-spacing included:        true
field cue resolution ready:        false
field cue FWI ready:               false
field timing conflict included:    true
field timing absolute ready:       false
field timing FWI ready:            false
field source figure notes:         19 / 19
gpu priority:                      none
```

Archive health refresh:

```text
outputs/experiments/1324_experiment_archive_health_report_post_field_timing_refresh
numbered experiment output dirs audited: 1325
figure-notes issues:                  125
missing run manifests:                5
gpu priority:                         none
```

The current paper-facing generators were then updated to write
`figures/FIGURE_NOTES.md`, and the active endpoint folders were refreshed in
place: synthetic runs 1322 and 1323, field run 098, and summary-table outputs
006 and 007. This fixed the active manuscript endpoints without
broad-regenerating historical figures or optional animations.
Run 1325 then backfilled the 9 synthetic source figures referenced by run 1322:
8 notes generated, 1 existing note skipped, and 0 missing figures.

Interpretation:

```text
The local GSSI data now have stronger relative time-zero and corrected-stack
QC evidence for the 014/016 short-profile pair, but the spatial support mask is
sparse. The supported-interval visual QC package is the preferred corrected
stack figure endpoint because it shows only all-window-supported regions. Do
not transfer the short-pair correction to the 015/013 long pair: the transfer
audit reduced whole-window agreement and improved 0/6 stable anchor windows.
The long pair does have its own strong pattern-only shift near +0.06 ns, but
profile 013 still lacks nominal phase-anchor picks. That +0.06 ns pattern shift
is stable across the tested shallow windows, while the inherited short-pair
offset is negative in every window. The long-profile visual-QC package now
shows that pattern alignment on all six stable anchor windows, and the holdout
QC shows that both repeat-limited anchors also improve at the same shift. The
all-anchor holdout sensitivity further shows support across all three tested
shallow time windows and all three tested anchor half-widths. A relaxed
late-window phase-anchor audit admits profile 013 candidates, but all relaxed
picks are low-SNR and the best relaxed hypothesis remains boundary-limited, so
the long pair remains pattern-only QC. The refreshed dataset policy incorporates
that evidence and still keeps field GPU/FWI priority at none. Runs 066-067
also move the relaxed-anchor audit into the paper-facing field bundle as
negative QC, so the current manuscript supplement package now has 8 figure rows
and 7 claim boundaries. Runs 068-069 add band-limited measured-repeatability
QC: the short-pair relative correction is supported in low through mid-high and
broad bands, while the highest short band is energy-limited; the long-pair
band support remains pattern-only. Runs 070-071 move that band-limited figure
into the paper-facing field bundle, now 9 figure rows and 8 claim boundaries.
Runs 072-074 add a measured-event support tier table and move it into the
paper-facing field bundle, now 10 figure rows and 9 claim boundaries.
Runs 075-077 add a manuscript-ready relative time-zero uncertainty budget for
the short 014/016 pair, then move it into the paper-facing field bundle, now
11 figure rows and 10 claim boundaries. The budget half-width is 0.058939 ns
and remains relative QC only, not absolute time-zero calibration.
Runs 078-080 stress-test that budget by perturbing the applied short-pair
offset across the bootstrap CI and conservative envelope. All 9 bootstrap-CI
rows and all 6 conservative-envelope rows remain supported across the three
tested shallow B-scan windows, while raw/no-correction has 0/3 supported rows.
The paper-facing field bundle now has 12 figure rows and 11 claim boundaries.
This is not a field time-zero calibration and must stay out of FWI/3D claims.
Run 081 quantifies the field-side HPC boundary: the profiles are densely
sampled along line, but missing crossline/grid metadata, relative-only
time-zero support, sparse all-window spatial support, and long-profile
pattern-only evidence block field FWI and 3D HPC submission from this dataset.
Runs 082-083 move that acquisition/HPC-readiness boundary into the current
paper-facing field bundle and dataset policy endpoint. The field bundle now has
13 figure rows and 12 claim boundaries. Do not treat this dataset as a 3D
survey or measured-data FWI benchmark. Run 084 adds a real field-side scale
check without promoting the claim: the short-pair relative correction reduces
depth-equivalent residuals by a factor of 6 and all three paired phase
residuals fall inside the conservative 5.890 mm depth-equivalent budget, but
the figure remains apparent-depth QC only, not cover-depth recovery. Run 085
adds the important sensitivity guardrail: the residual/budget support survives
all five archived dielectric/time-zero scenarios, but the apparent cue-depth
scale itself shifts by about 150 mm, or 2.18x. That makes the boundary sharper:
field depth-scale QC is useful, calibrated cover-depth recovery is not
supported. Run 086 adds the matching score-surface non-identifiability audit:
near-top score regions span multiple dielectric/time-zero choices, common-offset
scores keep several Tx/Rx offsets plausible, and 3/4 best-fit surfaces sit on
grid boundaries. Hyperbola/common-offset overlays therefore stay QC overlays,
not calibrated depth/radius inversion evidence. Run 087 makes the dataset
policy current through those three guardrails: apparent-depth QC is allowed,
but calibrated cover-depth, radius, field FWI, and 3D claims remain blocked.
Runs 088-089 then move those guardrails into the structured paper-facing field
bundle and refresh the dataset policy pointer. Runs 090-092 add an early-time
common-mode negative-control audit and move it into the current paper-facing
bundle. The direct/ringdown component is repeatable and aligns near zero lag,
but it does not reproduce the content-backed 0.127701 ns short-pair offset, so
it should not be used as absolute time-zero. The current field publication
bundle has 18 figure rows and 17 claim boundaries, with 084-086 included as
supplemental apparent-depth and degeneracy guardrails and 090 included as the
early-time absolute-time-zero boundary. Run 093 adds standalone measured
cue-spacing context: similar-time cue spacings are much wider than the
synthetic close25-close50 stress scale, and the closest distinct-x cue pair is
time-separated. Run 094 stress-tests that boundary across same-time thresholds
from 0.05 to 1.00 ns; the minimum admitted same-time spacing remains
96.657 mm. That makes the field dataset useful context, not a known-truth
close-spacing resolution benchmark. Runs 095-096 move that cue-spacing context
into the structured paper-facing field bundle and latest dataset policy while
preserving the no-resolution-benchmark/no-FWI/no-3D claim boundary. Run 097
then consolidates the field timing-anchor conflict: the short content-backed
relative offset, early/common-mode zero-lag alignment, and long-profile
pattern-only +0.06 ns shift are all real QC signals, but they are scoped
differently and cannot be reconciled into one absolute time-zero. This makes
the no-field-FWI/no-3D timing boundary more quantitative rather than merely
descriptive. Runs 098-099 promote that timing-anchor conflict into the current
structured field publication bundle and dataset policy. The current field
publication bundle now has 19 figure rows and 18 claim boundaries, while the
policy remains `field_2d_qc_not_3d_or_fwi`. Run 100 then performs a targeted
skip-existing source-figure notes backfill for that bundle: 19 source figures
audited, 18 notes generated, 1 existing note skipped, 0 missing figures, and
19/19 source figures with `FIGURE_NOTES.md` after the pass.
```

## Validation

Latest full validation:

```text
conda run -n gpr-fdtd-fwi python -m pytest -q
663 passed
```

Diff hygiene:

```text
git diff --check
pass
```

Resource posture during the work:

```text
The bounded GPU runs in this slice were run 1302 and run 1316. Run 1302 was
observed at about 85-86% GPU utilization with RAM around 14 GiB. Run 1316 was
observed at about 84-86% GPU utilization with RAM around 15 GiB. Later
synthetic policy and field readiness work, including runs 1310, 1311, 1312,
1313, 1314, 1315, 1317, 1318, 1319, 1320, 1321, 1322, 1323, 1325, 081, 082, 083,
084, 085, 086, 087, 088, 089, 090, 091, 092, 093, 094, 095, 096, 097, 098,
099, and 100, stayed CPU-only and kept GPU
utilization near idle. The cross-bundle manuscript evidence audit in
`outputs/summary_tables/006_local_2d_field_manuscript_evidence_audit` also
stayed CPU-only, as did the table pack in
`outputs/summary_tables/007_local_2d_field_manuscript_table_pack` and the
archive health refresh in
`outputs/experiments/1324_experiment_archive_health_report_post_field_timing_refresh`.
RAM stayed
far below the requested 80% cap.
```

## Next Useful Local Work

The best local next step is not a broad GPU sweep. Stronger options are:

```text
1. Field side: treat run 081 as the field acquisition/HPC-readiness endpoint,
   run 090 as the early-time absolute-time-zero negative-control audit, run
   097 as the timing-anchor conflict synthesis, run 098 as the current
   paper-facing field bundle, run 099 as the latest dataset policy synthesis,
   and run 100 as the source-figure notes/provenance backfill for the current
   bundle. Runs 084-086 are structured supplemental field
   guardrails inside the publication bundle for apparent-depth scale,
   apparent-depth sensitivity, and score-surface degeneracy QC. The
   paper-facing bundle now includes band-limited repeatability, event-support
   tiers, the relative time-zero uncertainty budget, the perturbation
   sensitivity audit, acquisition/HPC-readiness, the depth/degen guardrails,
   the early-time common-mode negative boundary, cue-spacing context, and the
   timing-anchor conflict boundary with the same no-FWI/no-3D claim boundary.
   Runs 093-094 remain useful for describing the measured dataset, robust
   across tested same-time thresholds, but not a known-truth close-spacing
   resolution benchmark.
2. Synthetic side: treat run 1323 as the current local 2D next-question
   endpoint, run 1322 as the current synthetic paper-facing figure bundle, run
   1317 as the refreshed close50 270/280 replicated-midpoint legacy answer,
   and run 1316 as the bounded close50 seed13 28.75 mm replicate. Run 1314
   remains the target1 source-density exception closure, run 1312 remains the
   target1 acquisition-confidence surface, run 1311 remains the acquisition
   tradeoff map, and run 1307 remains the manuscript resolution-claim map.
   These preserve zero immediate or conditional GPU candidates under the
   current questions.
3. Manuscript planning: use
   `outputs/summary_tables/006_local_2d_field_manuscript_evidence_audit` as
   the current neutral cross-bundle evidence audit. It validates 28/28
   constituent figure files and 29/29 claim boundaries while keeping synthetic
   and measured-field scopes separate. Use
   `outputs/summary_tables/007_local_2d_field_manuscript_table_pack` for the
   compact paper-planning CSVs: combined claim table, figure inventory, and
   result-metric table. The table pack now also records that 9/9 paper-facing
   synthetic source figures and 19/19 paper-facing field source figures have
   `FIGURE_NOTES.md` after runs 1325 and 100.
4. Any future GPU work should require a genuinely new objective, geometry, or
   narrowly specified exception probe. The current local policy endpoint does
   not justify a broad sweep.
```
