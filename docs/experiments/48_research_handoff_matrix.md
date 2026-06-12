# Experiment 48: Research Handoff Matrix

## Purpose

Provide a compact handoff view that separates what is solved, what is only
interval-supported, which caveats matter, which visual artifacts should be
checked first, and where more GPU time is justified.

## Matrix

| Branch | Location accuracy | Radius confidence | Source/material caveat | Visualization evidence | Runtime/cost note | Handoff decision |
| --- | --- | --- | --- | --- | --- | --- |
| Single rebar, standard radius | Correct basin after staged/local refinement | Strongest with 1.5 GHz-only or carry-low-25 least squares; report top-k margins | Source amplitude/time/frequency profiling is required under mismatch | Frequency/source-profile plots in experiments 23 and 26; source branch GIFs in experiments 46/49 | Cheap enough for local profiling; avoid global search | Use source-profiled local radius evidence, not W2/OT or free material inversion |
| Single rebar, field-like source shape | Correct with source-basis coefficient fit across tested ringdown/noise/source rows | Existing amplitude/time/frequency profile and coarse ringdown grid can select r=7.8 mm | Delayed secondary-pulse source shape must be calibrated before field/lab radius claims | Experiment 50, runs 421-424 | Source-basis fit costs about the same as the modeled ringdown grid, around 1700 s for the 52-candidate matrix | Promote coefficient-fit source-shape diagnostics; multi-rebar gates 425-428 passed across all three targets |
| Multi-rebar source-shape compact/wide x/z gate | Left, center, and right targets correct over compact and dense Stage 4C radius windows; fixed-neighbor synthesis has 48/48 truth rows; coupled compact aggregate has 15/15 truth rows | Positive margins against 6.2 mm; weakest margin is 1.006e-04 in true-state center row; highband preserves truth but improves that gap only 1.139x; material profiling leaves the gap essentially unchanged at 1.019e-04; late_high improves the true-state center gap to 1.632e-04 but remains weak; veryhigh worsens that gap to 6.388e-05; coupled aggregate has 10 weak rows, 2 moderate rows, 3 strong rows, max z ambiguity 1 mm, max radius ambiguity 0.4 mm | Source-basis coefficients recovered injected ringdown 0.20 and about 0.25; material profile selects true concrete epsr and shows steel conductivity saturation; dense seed55 keeps z91/r6.8-7.0 branch secondary; coupled runs recover ringdown about 0.25; variable-depth veryhigh objective does not transfer to ringdown source-shape cases | Experiments 51/52/53/62/68, runs 425-450, 506-507, and 535 | 5 candidates cost 162 s; 18 material candidates cost 583 s; 27 candidates cost 849-882 s; coupled 3x27 pass costs 2420-2643 s; two-pass 6x27 costs 4904 s; 45 candidates cost 1472 s; 125 candidates cost about 4080 s; dense 325 candidates cost about 10200-10600 s; interval handoff is docs/JSON only | Avoid dense coupled sweep and report the weakest center radius as a 6.0-6.2 mm interval using run 535; do not add free material parameters or global veryhigh objective for this branch |
| Single rebar, shallow r=4 mm | Correct point estimate in tested high-band cases | Nominal point r=4.0 mm remains exact, but report material/source-aware interval 3.95-4.05 mm in the packaged flow and broader fine-grid diagnostic interval about 3.925-4.100 mm | Material/source changes can explain parts of the shallow objective valley; r=8 control is more stable but still gets an upper-side nuisance interval | Fine-radius and material/source tradeoff plots from experiments 189-201 plus run 536 handoff; material branch GIF in experiment 49 | More fine sampling adds cost without collapsing the interval; handoff is docs/JSON only | Report nominal point plus nuisance-aware interval using run 536; do not claim high-precision point size without calibrated material/source bounds |
| Same-depth multi-rebar local x/z/r | True x/z/r recovered across the Stage 6 matrix | Mostly weak margins before coordinate-confidence upgrades | Source mismatch does not change point recovery but tightens margins | Experiment 40 confidence matrix | Robustness matrix already run | Confidence labels and ambiguity intervals are mandatory in all reports |
| Variable-radius close60 staged pipeline | Final x/z/r exact across seeds after staged policy | Joint radius tuple ranks truth first | Standard 5-source focused target-2 stage has x intervals; 7-source refinement collapses them | Experiment 419 staged error plot and replay plan | Replay plan captures 15 stage commands; reruns are heavy GPU work | Use 5-source interval reporting by default; use 7-source focused refinement when point x is required |
| Variable-depth variable-radius staged coordinate | Detector and assignment recover physical seeds; staged coordinate path reaches exact truth x=[150,250,350], z=[80,100,120], r=[5,6,8] under source mismatch and 10% noise for seeds 13, 34, and 55 | Seed13 target-0 is moderate at r=5 mm with a 5.0-5.25 mm interval after local x/z coupling; seed34 and seed55 also reach point truth but retain weak fine target-0/target-2 intervals; three-seed staged weakest margin is 5.575e-05; 7-source checks modestly help target0 but not target2; 35/50 mm Tx/Rx narrows intervals; the three-seed 50 mm Tx/Rx aggregate has 12/12 truth rows, zero x/z ambiguity, and max radius ambiguity 0.25 mm; all-target veryhigh objective diagnostics preserve 18/18 truth rows, improve labels to weak=5/moderate=11/strong=2, and collapse x/z/r ambiguity widths to zero; fitted-ringdown seed55 all-target rows stay exact/moderate under base; target-0 ringdown is three-seed exact with veryhigh the only consistent improver; target-2 ringdown is three-seed exact with late_high strongest and late/late_high/veryhigh strong on all rows; target-1 ringdown is three-seed exact/moderate with late_high strongest on all rows; the all-target/all-seed ringdown aggregate has 9/9 exact rows, base weak=1/moderate=7/strong=1, and veryhigh moderate=6/strong=3 with ratio min/mean/max 1.058/1.231/1.403; the cross-condition aggregate has 27/27 exact rows, veryhigh ratio min/mean/max 1.058/1.612/2.563, and veryhigh labels weak=5/moderate=17/strong=5 with zero ambiguity | False shallow aliases appear at center/right, but assignment rejects them; sequential radius/z or x/z/r coupling matters; radius-only profiling is insufficient when a target carries a 1 mm geometry residual; source-count escalation alone is not a general interval fix; Tx/Rx geometry is the leading interval-shaping lever; veryhigh is currently diagnostic/reporting evidence, not yet a production update rule; veryhigh remains branch-specific and should not be promoted globally because experiment 62 failed to improve the older source-shape interval; late_high is strongest on targets 1 and 2 but weakens target-0 rows | Experiments 54/55/56/57/58/59/60/61/63/64/65/66, runs 451-505 and 508-533 | Seed13 detector costs 16 s, location-only costs 1723 s, focused stages cost 32-587 s; seed34 and seed55 location/radius/coupling stages add bounded 326-653 s runs; 7-source final-state checks cost 225-266 s; 35/50 mm Tx/Rx checks cost 162-197 s; 50 mm seed replications cost 162-197 s per target; objective-variant guardrails cost 163-439 s per target; fitted-ringdown target objective stresses cost 324-885 s depending candidate count; target-0 ringdown seed replications cost 387-393 s; target-2 ringdown seed replications cost 324-326 s; target-1 ringdown seed replications cost 875-885 s; cross-condition CPU report cost 0.85 s; reporting handoff is docs/JSON only; broad all-parameter command remains deferred | Use run 481 as the three-seed staged-coordinate evidence package, run 498 as the three-seed 50 mm Tx/Rx acquisition-interval package, run 505 as the all-target veryhigh objective-confidence package, run 514 as the seed55 all-target ringdown objective guardrail, run 520 as the three-seed target-0 ringdown report, run 525 as the three-seed target-2 ringdown report, run 530 as the three-seed target-1 ringdown report, run 531 as the all-target/all-seed fitted-ringdown guardrail, run 532 as the cross-condition objective-confidence report, and run 533 as the objective-use handoff; next inspect the handoff matrix for a concrete gap before launching more GPU work |
| Variable-radius close50 geometry | Close50 needed acquisition geometry changes to disambiguate target 2 | Radius remains strong while x ambiguity is the limiter | Legacy missing default Tx/Rx metadata is repaired in run 534 with an explicit 20 mm filled-default flag; future summaries should record `tx_rx_offset_mm` directly | Experiments 271, 273, 280, 284, 289, and 67 aggregates | 4 sources with 35-40 mm Tx/Rx is the practical region; metadata repair is CPU-only/reporting-only | Use acquisition-aware summaries; 35 mm Tx/Rx is robust, 30 mm is margin-aware minimum; run 534 is the repaired Tx/Rx20-vs-Tx/Rx40 comparison |
| Tight variable-radius spacing under 35 mm Tx/Rx | Close30 is the tightest replicated clean result | Close28/25 require interval or larger-offset reporting | The coupled shifted-x/radius branch becomes competitive | Experiments 305, 310, 314 | More bisection below close30 is not useful without acquisition changes | Keep close30 as standard clean limit; use larger Tx/Rx for tighter spacing |
| Close14 tangent under 45 mm Tx/Rx | Clean at 10% and replicated up to 15.3125% RMS noise | Strong, zero-ambiguity at promoted clean levels | Higher noise becomes point-correct but x-interval-supported | Experiments 335, 349, 356 | Source-count escalation did not rescue the boundary | Use 4 sources; do not spend more GPU time on source-count escalation |
| Close14 tangent under 50 mm Tx/Rx | Clean replicated endpoint at 19.642333984375% RMS | Strong radius margins; boundary failure is lateral x ambiguity | Final seed34 upper is numerical-edge ambiguous at 19.642372131347656% RMS | Experiment 418 cutoff-margin and x-width plots | Single target-2 sweeps cost roughly 20-25 min each on GPU | Promote 19.642333984375% RMS; stop scalar bisection unless the ambiguity rule changes |

## Immediate Next Actions

```text
1. Do not run more close14 scalar bisection.
2. Do not spend GPU time on 5/7-source escalation for the closed close14 branch.
3. Use experiment 419's replay plan when a new staged variable-radius seed or
   geometry variation is needed.
4. Material/source branch animations are packaged in experiment 49/420; add
   more only when a new matrix exposes another actual competing branch.
5. For source-shape calibration, fixed-x/z, compact all-target, compact
   center hard-noise/high-radius, dense all-target, synthesis, compact seed
   replication, sparse seed55, dense seed55, seed synthesis, first coupled
   radius-only seed, harder coupled x/z/r seed, independent coupled order
   replication, two-pass compact check, coupled aggregate, and true-state
   highband diagnostic checks pass; material profiling does not collapse the
   remaining center radius interval, so next avoid dense coupled sweeps and
   keep the remaining center radius as an interval unless a new branch-level
   objective changes the evidence.
6. For experiment 54's variable-depth/variable-radius branch, the staged
   detector/assignment and location/radius/focused-coupling coordinate path
   reaches exact truth under source mismatch and 10% noise across seeds 13,
   34, and 55. Target-0 and target-2 radii should still be reported with local
   intervals when their confidence rows are weak.
7. The combined seed13/seed34/seed55 summary is packaged in run 481. Keep the
   broad all-parameter command deferred; spend the next GPU block on a new
   branch or a specific acquisition/objective variation.
8. The 7-source final-state acquisition check is packaged in run 484. It
   improves target-0 separation modestly but does not collapse the target-2
   interval, so do not promote source count alone as the default interval fix.
9. The 35 mm Tx/Rx final-state acquisition check is packaged in run 487. It
   narrows ambiguity intervals more clearly than source count but keeps weak
   or moderate margins, so the next bounded geometry check is 50 mm Tx/Rx or
   else a weighted-objective variant.
10. The 50 mm Tx/Rx final-state acquisition check is packaged in runs 490,
    493, 494, 497, and 498. Across seeds 13, 34, and 55, the combined run 498
    has 12/12 truth-geometry rows, zero x/z ambiguity, and maximum radius
    ambiguity width 0.25 mm, but confidence labels remain weak or moderate.
    Treat Tx/Rx=50 mm as the leading tested acquisition geometry for
    final-state interval narrowing, not as strong point-radius evidence.
11. The Tx/Rx=50 objective-lever diagnostic is packaged in runs 499-505. The
    veryhigh objective keeps all target-0, target-1, and target-2 rows at
    truth, raises the all-target mean margin ratio to 1.803, improves
    objective-specific labels to weak=5, moderate=11, strong=2, and collapses
    x/z/r ambiguity widths to zero. Keep it as diagnostic/reporting evidence
    unless the update rule is explicitly changed and re-tested.
12. The seed55 fitted-ringdown variable-depth/radius objective stress is
    packaged in runs 508-514. Base recovers exact x/z/r for all three targets
    with moderate labels and zero ambiguity width. Veryhigh is the only
    diagnostic variant with margin ratio above 1.0 on every target, with
    ratio min/mean/max 1.058/1.213/1.299, but late_high is stronger on targets
    1 and 2.
13. The target-0 ringdown seed replication is packaged in runs 515-520.
    Seeds 13, 34, and 55 all stay exact. Base has weak=1 and moderate=2,
    while veryhigh has moderate=3 and is the only diagnostic with consistent
    target-0 margin improvement.
14. The target-2 ringdown seed replication is packaged in runs 521-525. Seeds
    13, 34, and 55 all stay exact. Late, late_high, and veryhigh are strong on
    all three rows, with late_high the largest consistent margin ratio.
15. The target-1 ringdown seed replication is packaged in runs 526-530. Seeds
    13, 34, and 55 all stay exact and moderate. Late_high is the strongest
    target-1 diagnostic on every row, with ratio 1.250-1.443x.
16. The all-target/all-seed fitted-ringdown objective guardrail is packaged in
    run 531. All nine target/seed rows stay exact. Veryhigh is the only tested
    objective with ratio above 1.0 on every row, ratio min/mean/max
    1.058/1.231/1.403 and labels moderate=6/strong=3; late_high is stronger
    on targets 1 and 2 but weakens target 0.
17. The CPU-only cross-condition objective-confidence report is packaged in
    run 532. Across 27 selected non-ringdown and fitted-ringdown rows, every
    objective preserves truth geometry, but veryhigh is the only objective
    with ratio above 1.0 on every row. Veryhigh has ratio min/mean/max
    1.058/1.612/2.563 and objective labels weak=5, moderate=17, strong=5.
18. The lightweight objective-use handoff is packaged in run 533. It records
    base as the production update objective, veryhigh as the Tx/Rx=50
    variable-depth/radius reporting diagnostic, and global veryhigh promotion
    as rejected because experiment 62 failed the transfer check.
19. Inspect the handoff matrix for the next concrete research gap before
    launching additional GPU work.
20. Close50 acquisition metadata repair is packaged in run 534. The legacy
    default-offset rows are now explicitly labelled as Tx/Rx offset 20 mm
    filled defaults, while Tx/Rx=40 mm remains directly recorded.
21. Source-shape center interval reporting is packaged in run 535. The center
    target should be reported as r=6.0-6.2 mm; late_high is only a weak
    diagnostic improvement and veryhigh fails transfer.
22. Single-rebar shallow r=4 reporting is packaged in run 536. Report nominal
    r=4.0 mm with a material/source-aware interval, not an unqualified
    high-precision point radius.
23. Marathon recovery checkpoint is packaged in run 537. If the session is
    interrupted again, resume from that checkpoint before scheduling GPU work.
24. Current evidence synthesis is packaged in run 538. Use it as the seed for
    concise paper/report writing before adding new experiment branches.
25. Results-section draft is packaged in run 539. If continuing in reporting
    mode, add a methods paragraph and evidence table before any GPU work.
26. Methods paragraph and evidence table are packaged in run 540. If continuing
    in reporting mode, combine runs 539 and 540 into a single draft.
27. Combined report draft is packaged in run 541. Next reporting step is a
    decision-grade figure map, not GPU work.
28. Decision-grade figure map is packaged in run 542. Review existing mapped
    figures before creating any new plots.
29. Compact objective summary figure is packaged in run 543. Use it in report
    layouts instead of the ultra-wide run 532 objective plot, while keeping run
    532 as the row-level audit artifact. This does not change the objective-use
    decision: base remains the production update rule and veryhigh remains a
    Tx/Rx=50 variable-depth/radius reporting diagnostic.
30. Decision figure readiness audit is packaged in run 544. Ten of the eleven
    mapped figures are report-ready candidates; the only layout flag is the
    run 531 fitted-ringdown detail plot, which is superseded for report layout
    by run 543. No additional compact figure is queued.
31. Report figure caption package is assembled in run 545. Use its symlinked
    figure paths and captions for report assembly, while preserving the
    original experiment folders as the source of record.
32. Report claim consistency audit is packaged in run 546. The report draft,
    figure captions, handoff matrix, and master plan agree on run numbers,
    intervals, objective scope, and non-claims; no inconsistency is queued.
33. Reporting reproducibility bundle is packaged in run 547. Use it as the
    stable index for final report assembly; it links the report draft, figure
    captions, figures, claim audit, figure audit, evidence synthesis, handoff
    matrix, and master plan.
34. Final report markdown is assembled in run 548. Use
    `outputs/experiments/548_final_report_markdown/final_report.md` for
    manuscript editing or formatting; no new experiment claim is introduced.
35. Final report editorial lint is packaged in run 549. The final report has
    no missing run references, no broken embedded image links, and no unresolved
    editing markers.
36. Archive status checkpoint is packaged in run 550. Full tests pass, the
    final report lint passes, GPU load is low, RAM headroom is high, and no GPU
    experiment is queued.
37. Commit/archive inventory is packaged in run 551. Code/test changes,
    research trackers, and ignored output artifacts are separated for cleanup
    planning; no commit was made.
38. Code self-review hardening is packaged in run 552. Objective diagnostic
    figure notes now tolerate missing optional numeric values, with focused and
    full tests passing.
39. Post-hardening resume checkpoint is packaged in run 553. It supersedes run
    550 as the current restart point: full tests pass at 257/257 and no GPU
    experiment is queued.
40. Report dependency size audit is packaged in run 554. The final-report
    dependency set has 48 existing output folders, zero missing folders, and a
    total size of 9.244 MiB, so archiving it is low-risk if requested.
41. Report dependency archive is packaged in run 555. The archive uses an
    explicit 89-path file list, contains 466 entries, is 4.0M compressed, and
    has SHA-256 c5560c13846b501f0c3e67c8dd4b895baa90c2863036cbec27181b15703d5de0.
42. Post-archive resume checkpoint is packaged in run 556. It supersedes run
    553 as the current restart point and records the validated archive plus
    stable GPU/RAM state.
43. Commit/PR summary draft is packaged in run 557. It separates runtime code,
    tests, reporting artifacts, and ignored archive handoff; no commit was made.
44. Next-action queue is packaged in run 558. Default next work is manuscript,
    archive, or commit preparation; GPU work remains gated on a concrete bounded
    question.
45. Final report reproducibility refresh is packaged in run 559. It supersedes
    run 548 for manuscript use by citing the current run 556 checkpoint and run
    555 archive while preserving the same scientific claims.
46. Revised final report lint is packaged in run 560. The run 559 report has
    42 referenced runs, no missing output folders, seven resolved embedded
    images, and no unresolved editing markers.
47. Next-action queue refresh is packaged in run 561. It points manuscript
    editing to the current run 559 revised report and keeps GPU work gated on a
    concrete bounded question.
48. IMRAD manuscript draft is packaged in run 562. It reorganizes the validated
    report into manuscript sections without changing scientific claims.
49. IMRAD manuscript lint is packaged in run 563. The manuscript has 42
    referenced runs, no missing output folders, seven resolved embedded images,
    and no unresolved editing markers.
50. Post-IMRAD resume checkpoint is packaged in run 564. It supersedes run 556
    as the current restart point and records the validated revised report and
    IMRAD manuscript draft.
51. Manuscript balance/guardrail audit is packaged in run 565. The IMRAD draft
    now explicitly states the non-claims and interval guardrails and passes the
    section/phrase audit.
52. Next-action queue manuscript refresh is packaged in run 566. It points
    manuscript editing to run 562 and keeps GPU work gated.
53. Manuscript guardrail prose polish is packaged in run 567. It removes a
    duplicated limitations phrase, restores readable guardrail wrapping, and
    reruns the manuscript lint and balance audit.
54. Post-manuscript polish checkpoint is packaged in run 568. It supersedes run
    564 as the current restart point and records the validated guardrail audit
    plus stable GPU/RAM state.
55. Next-action queue post-polish is packaged in run 569. It points future
    resumes to run 568, keeps manuscript editing on run 562 as polished in run
    567, and keeps GPU work gated.
56. Commit/PR summary refresh is packaged in run 570. It updates the commit
    grouping and inventory through docs/experiments/103 and
    outputs/experiments/570 without making a commit.
57. Coordinate aggregate note hardening is packaged in run 571. Missing
    aggregate ambiguity-width note values now render as `not_recorded`, and
    focused/full tests pass at 17/17 and 258/258.
58. Commit/PR summary post-hardening is packaged in run 572. It supersedes run
    570 as the current commit summary and includes run 571 plus the 258-test
    validation state.
59. Post-hardening resume checkpoint is packaged in run 573. It supersedes run
    568 as the current restart point and records the low GPU/RAM pressure.
60. Next-action queue post-hardening is packaged in run 574. It points future
    resumes to run 573, points commit preparation to run 572, and keeps GPU
    work gated.
61. IMRAD manuscript validation refresh is packaged in run 575. It updates the
    manuscript validation/data-availability state to run 573/577/580/581 and
    passes a 51-run structural lint plus guardrail audit.
62. Next-action queue manuscript validation refresh is packaged in run 576. It
    points manuscript editing to run 562 with current validation in run 575,
    commit preparation to run 572, and keeps GPU work gated.
63. Commit/PR summary current refresh is packaged in run 577. It supersedes
    run 572 as the current commit summary and updates inventory ranges through
    docs/experiments/115 and outputs/experiments/582.
64. Next-action queue commit summary refresh is packaged in run 578. It points
    commit preparation to run 577 while keeping manuscript validation on run
    575 and GPU work gated.
65. Current handoff archive size audit is packaged in run 579. It finds 115
    dependency paths, 351 files, zero missing paths, 13.7 MiB total size, and
    36 current paths not covered by the old run 555 archive.
66. Current handoff archive is packaged in run 580. It contains 116 input
    paths, 487 archive entries, is 7.9M compressed, and records its SHA-256 in
    run 580 metadata.
67. Next-action queue current archive refresh is packaged in run 581. It points
    optional current archive handoff to run 580 while keeping manuscript
    validation on run 575, commit preparation on run 577, and GPU work gated.
68. Current pre-commit validation checkpoint is packaged in run 582. Focused
    objective/confidence tests pass at 17/17, the full suite passes at
    258/258, `git diff --check` is clean, and GPU/RAM pressure remains low.
69. Next-action queue pre-commit validation refresh is packaged in run 583. It
    points local validation to run 582 while keeping run 580 as the current
    packaged archive and GPU work gated.
70. Objective confidence sparse-result hardening is packaged in run 584.
    Sparse objective-result metadata without complete top-candidate geometry
    now emits missing geometry/error fields instead of raising a reporting
    exception. Focused tests pass at 18/18, the full suite passes at 259/259,
    and run 580 remains the current packaged archive.
71. Next-action queue objective sparse-hardening refresh is packaged in run
    585. It points local validation to run 584 while keeping run 580 as the
    current packaged archive, run 577 as the current commit-preparation
    artifact, and GPU work gated.
72. Commit/PR summary sparse-hardening refresh is packaged in run 586. It
    supersedes run 577 for commit preparation, includes the sparse-result
    reporting hardening, and records the 18/18 focused and 259/259 full test
    validation state.
73. Next-action queue commit-summary sparse-hardening refresh is packaged in
    run 587. It points commit preparation to run 586, local validation to run
    584, and keeps run 580 as the current packaged archive.
74. Post-sparse-hardening resume checkpoint is packaged in run 588. It
    supersedes run 573 as the current restart checkpoint, records run 584
    validation, run 586 commit preparation, run 587 queue state, and low GPU/RAM
    pressure.
75. Next-action queue post-sparse-hardening resume refresh is packaged in run
    589. It points future resumes to run 588 while keeping local validation on
    run 584, commit preparation on run 586, and the packaged archive on run 580.
76. Current artifact consistency audit is packaged in run 590. It validates
    run 584-589 manifests/artifacts, docs/experiments/117-122, infrastructure
    symlinks, and the run 580 archive checksum/entry count. It finds no stale
    current pointers and no new bounded GPU question.
77. IMRAD manuscript current validation refresh is packaged in run 591. The
    manuscript now points to run 584 validation, run 586 commit preparation,
    run 588 resume, run 589 queue, and run 590 audit state. Structural lint
    passes with 54 referenced runs, seven resolved figures, and all guardrails
    present.
78. Commit/PR summary current manuscript-validation refresh is packaged in run
    592. It supersedes run 586 for commit preparation and records the current
    run 591 manuscript validation state plus the 259/259 full-test state.
79. Next-action queue current manuscript-validation refresh is packaged in run
    593. It points manuscript validation to run 591, commit preparation to run
    592, restart to run 588, local code validation to run 584, and the archive
    to run 580.
80. Current handoff archive refresh size audit is packaged in run 594. It finds
    138 base dependency paths, 402 files, zero missing paths, 21.6 MiB total
    size, and 27 current paths not covered by the run 580 archive, so a
    refreshed archive is justified.
81. Current handoff archive refresh is packaged in run 595. It contains 139
    input paths, 554 archive entries, is 16M compressed, has SHA-256
    a55cbf6c6540223bdb01874ca51bb2ab1063057833006e06a318f66ce84be280, includes
    the run 594 audit folder, and excludes the run 595 self folder.
82. Commit/PR summary current archive refresh is packaged in run 596. It
    supersedes run 592 for commit preparation and records run 595 as the
    current handoff archive with the validated SHA-256.
83. Next-action queue current archive refresh is packaged in run 597. It points
    optional archive handoff to run 595, commit preparation to run 596,
    manuscript validation to run 591, restart to run 588, and local code
    validation to run 584.
84. Current pre-commit validation after archive refresh is packaged in run 598.
    Focused objective/confidence tests pass at 18/18, the full suite passes at
    259/259, `git diff --check` is clean, and GPU/RAM pressure remains low.
85. Next-action queue current validation refresh is packaged in run 599. It
    points local code validation to run 598 while keeping archive handoff on run
    595, commit preparation on run 596, manuscript validation on run 591, and
    restart on run 588.
86. Commit/PR summary current validation refresh is packaged in run 600. It
    supersedes run 596 for commit preparation, includes the run 598 validation
    checkpoint and run 599 queue, and preserves run 595 as the current handoff
    archive.
87. Next-action queue commit-summary validation refresh is packaged in run 601.
    It points commit preparation to run 600 while keeping local code validation
    on run 598, manuscript validation on run 591, archive handoff on run 595,
    and restart on run 588.
88. Objective diagnostic sparse-geometry hardening is packaged in run 602. It
    hardens diagnostic enrichment and ratio rows when best-candidate geometry
    is missing, records unavailable geometry comparisons explicitly, and
    validates with 19/19 focused tests, 260/260 full tests, and clean
    `git diff --check`.
89. Commit/PR summary current diagnostic-hardening refresh is packaged in run
    603. It supersedes run 600 for commit preparation, includes run 602 and the
    260/260 full-test state, and preserves run 595 as the current packaged
    archive.
90. Next-action queue diagnostic-hardening refresh is packaged in run 604. It
    points local code validation to run 602, commit preparation to run 603,
    manuscript validation to run 591, archive handoff to run 595, and restart
    to run 588.
91. Current diagnostic-hardening state audit is packaged in run 605. It
    verifies run 602-604 manifests/artifacts/docs/symlinks, confirms the run
    595 archive SHA-256 and 554-entry count, and finds no stale current
    pointers.
92. Optional numeric non-finite reporting hardening is packaged in run 606. It
    treats malformed or non-finite optional metrics as missing in coordinate
    aggregate and objective diagnostic reporting, with 21/21 focused tests,
    262/262 full tests, and clean `git diff --check`.
93. Commit/PR summary current non-finite-hardening refresh is packaged in run
    607. It supersedes run 603 for commit preparation, includes run 606 and the
    262/262 full-test state, and preserves run 595 as the current packaged
    archive.
94. Next-action queue non-finite-hardening refresh is packaged in run 608. It
    points local code validation to run 606, commit preparation to run 607,
    state audit to run 605, manuscript validation to run 591, archive handoff
    to run 595, and restart to run 588.
95. Reporting CLI non-finite smoke is packaged in run 609. It runs the real
    coordinate confidence aggregate CLI on malformed optional metrics, produces
    CSV/JSON/two PNG figures/figure notes, verifies zero non-finite numeric
    values in aggregate statistics, and confirms nonblank 1719 x 971 figures.
96. Objective ratio null-serialization hardening is packaged in run 610. It
    serializes unavailable objective diagnostic base/variant margins and margin
    ratios as null instead of NaN, with 21/21 focused tests, 262/262 full
    tests, and clean `git diff --check`.
97. Objective CLI sparse/non-finite smoke is packaged in run 611. It runs the
    real objective diagnostic CLI on sparse geometry and non-finite margin
    input, writes CSV/JSON/PNG/figure notes, verifies zero non-finite numeric
    values in the generated report, and confirms null unavailable geometry and
    margin-ratio fields.
98. Current non-finite-hardening state audit is packaged in run 612. It
    validates run 606-611 manifests/artifacts/docs/symlinks, confirms zero
    non-finite numeric values in the run 609 aggregate and run 611 report, and
    verifies the run 595 archive checksum and 554-entry count.
99. Commit/PR summary current smoke-audit refresh is packaged in run 613. It
    supersedes run 607 for commit preparation, includes runs 609-612 and the
    262/262 full-test state, and preserves run 595 as the current packaged
    archive.
100. Next-action queue smoke-audit refresh is packaged in run 614. It points
     local code validation to run 610, CLI smokes to runs 609 and 611, state
     audit to run 612, commit preparation to run 613, manuscript validation to
     run 591, archive handoff to run 595, and restart to run 588.
101. Current smoke-audit archive size audit is packaged in run 615. It finds
     180 base dependency paths, 507 files, 38.1 MiB total size, zero missing
     paths, and 41 current paths not covered by the run 595 archive, so a
     refreshed handoff archive is justified.
102. Current handoff archive smoke-audit refresh is packaged in run 616. It
     contains 181 input paths, 696 archive entries, is 32M compressed, has
     SHA-256 a88eaef65502afa60555c11ed7baa3876129161e4fc5cb7f7ce7d155cc5f7b98,
     includes the run 615 audit folder, and excludes the run 616 self folder.
103. Commit/PR summary current archive smoke-audit refresh is packaged in run
     617. It supersedes run 613 for commit preparation, records run 616 as the
     current handoff archive, and preserves the 262/262 full-test state.
104. Next-action queue archive smoke-audit refresh is packaged in run 618. It
     points archive handoff to run 616, commit preparation to run 617, local
     validation to run 610, CLI smokes to runs 609 and 611, state audit to run
     612, manuscript validation to run 591, and restart to run 588.
105. IMRAD manuscript current archive validation refresh is packaged in run
     619. The run 562 manuscript now points to the current run 610-618
     validation, smoke, audit, archive, commit, and queue state. Structural
     lint passes with 50 referenced runs, zero missing runs, seven resolved
     figures, and all five guardrails present.
106. Commit/PR summary current manuscript-archive refresh is packaged in run
     620. It supersedes run 617 for commit preparation, records run 619 as the
     current manuscript validation artifact, and preserves run 616 as the
     current packaged archive.
107. Next-action queue manuscript-archive refresh is packaged in run 621. It
     points manuscript validation to run 619, commit preparation to run 620,
     archive handoff to run 616, local validation to run 610, CLI smokes to
     runs 609 and 611, state audit to run 612, and restart to run 588.
108. Current manuscript archive size audit is packaged in run 622. It finds
     194 base dependency paths, 540 files, 69.9 MiB total size, zero missing
     paths, 13 paths not covered by run 616, 37 files missing from run 616, and
     four changed files including the run 562 manuscript draft, so a refreshed
     archive is justified.
109. Current handoff archive manuscript refresh is packaged in run 623. It
     contains 195 input paths, 742 archive entries, is 64M compressed, has
     SHA-256 d60e899a45b3528d773b9125a0654686f0554bb8bdf6f2e6b02b7d3c24cbcc18,
     includes the run 622 audit folder and updated run 562 manuscript, and
     excludes the run 623 self folder.
110. Commit/PR summary current manuscript-archive handoff refresh is packaged
     in run 624. It supersedes run 620 for commit preparation, records run 623
     as the current handoff archive, and preserves run 619 as the current
     manuscript validation artifact.
111. Next-action queue manuscript-archive handoff refresh is packaged in run
     625. It points archive handoff to run 623, commit preparation to run 624,
     manuscript validation to run 619, local validation to run 610, CLI smokes
     to runs 609 and 611, state audit to run 612, and restart to run 588.
112. Post-manuscript-archive resume checkpoint is packaged in run 626. It
     supersedes run 588 as the current restart checkpoint, points archive
     handoff to run 623, commit preparation to run 624, manuscript validation
     to run 619, local validation to run 610, CLI smokes to runs 609 and 611,
     and state audit to run 612.
113. Commit/PR summary current resume refresh is packaged in run 627. It
     supersedes run 624 for commit preparation, records run 626 as the current
     restart checkpoint, keeps run 623 as the current handoff archive, and
     preserves run 619 as the current manuscript validation artifact.
114. Next-action queue resume refresh is packaged in run 628. It points
     restart to run 626, commit preparation to run 627, archive handoff to run
     623, manuscript validation to run 619, local validation to run 610, CLI
     smokes to runs 609 and 611, and state audit to run 612.
115. Current resume state audit is packaged in run 629. It validates run
     626-628 manifests/artifacts/docs/symlinks, confirms run 628 points
     restart to run 626 and commit preparation to run 627, and verifies the
     run 623 archive checksum and 742-entry count.
116. Commit/PR summary current resume-audit refresh is packaged in run 630. It
     supersedes run 627 for commit preparation, records run 629 as the current
     state audit, keeps run 626 as the current restart checkpoint, and keeps
     run 623 as the current handoff archive.
117. Next-action queue resume-audit refresh is packaged in run 631. It points
     state audit to run 629, commit preparation to run 630, restart to run 626,
     archive handoff to run 623, manuscript validation to run 619, local
     validation to run 610, and CLI smokes to runs 609 and 611.
118. Current resume archive size audit is packaged in run 632. It finds 214
     base dependency paths, 586 files, 133.6 MiB total size, zero missing
     paths, 19 paths not covered by run 623, 49 files missing from run 623,
     and three changed planning files, so a refreshed archive is justified.
119. Current handoff archive resume refresh is packaged in run 633. It contains
     215 input paths, 805 archive entries, is 128M compressed, has SHA-256
     00637efb4a579591b0f529f693a7e722b94361b0a3ea129cde5695ba35e49aef,
     includes the run 632 audit folder and current resume/audit queue state,
     and excludes the run 633 self folder.
120. Commit/PR summary current archive-resume refresh is packaged in run 634.
     It supersedes run 630 for commit preparation, records run 633 as the
     current handoff archive, keeps run 626 as the current restart checkpoint,
     and keeps run 629 as the current state audit.
121. Next-action queue archive-resume refresh is packaged in run 635. It
     points archive handoff to run 633, commit preparation to run 634, restart
     to run 626, state audit to run 629, manuscript validation to run 619,
     local validation to run 610, and CLI smokes to runs 609 and 611.
122. IMRAD manuscript current resume-archive validation refresh is packaged in
     run 636. The run 562 manuscript now points to the current run 626 restart,
     run 629 audit, run 633 archive, run 634 commit, and run 635 queue state.
     Structural lint passes with 57 referenced runs, zero missing runs, seven
     resolved figures, and all five guardrails present.
123. Commit/PR summary current manuscript resume-archive refresh is packaged in
     run 637. It supersedes run 634 for commit preparation, records run 636 as
     the current manuscript validation artifact, keeps run 633 as the current
     handoff archive, and keeps run 626 as the current restart checkpoint.
124. Next-action queue manuscript resume-archive refresh is packaged in run
     638. It points manuscript validation to run 636, commit preparation to run
     637, archive handoff to run 633, restart to run 626, state audit to run
     629, local validation to run 610, and CLI smokes to runs 609 and 611.
125. Objective diagnostic manifest artifact hardening is packaged in run 639.
     It omits optional confidence CSV manifest entries when no confidence CSV
     is written, adds a regression test for that no-confidence-row path, and
     validates with 13/13 objective diagnostic tests, 22/22 reporting focused
     tests, and 263/263 full tests.
126. Commit/PR summary current manifest-validation refresh is packaged in run
     640. It supersedes run 637 for commit preparation, records run 639 as the
     current local validation checkpoint, preserves run 636 as the manuscript
     validation artifact, and keeps run 633 as the current handoff archive.
127. Next-action queue manifest-validation refresh is packaged in run 641. It
     points local validation to run 639, commit preparation to run 640,
     manuscript validation to run 636, archive handoff to run 633, restart to
     run 626, state audit to run 629, and CLI smokes to runs 609 and 611.
128. Objective diagnostic no-confidence manifest smoke is packaged in run 642.
     It runs the real objective diagnostic CLI on a summary with no saved
     objective confidence rows, verifies the manifest omits `confidence_csv`,
     confirms zero non-finite numeric report values, and validates a nonblank
     2059 x 1005 plot with figure notes.
129. Commit/PR summary current manifest-smoke refresh is packaged in run 643.
     It supersedes run 640 for commit preparation, records run 642 as the
     current no-confidence manifest CLI smoke, preserves run 639 as current
     local validation, and keeps run 633 as the current handoff archive.
130. Next-action queue manifest-smoke refresh is packaged in run 644. It points
     objective CLI smokes to runs 611 and 642, aggregate CLI smoke to run 609,
     local validation to run 639, commit preparation to run 643, manuscript
     validation to run 636, archive handoff to run 633, and restart to run 626.
131. Current manifest-smoke state audit is packaged in run 645. It validates
     run 639-644 manifests/artifacts/docs/symlinks, confirms run 642 omits the
     confidence CSV manifest artifact and has zero non-finite report values,
     confirms the run 642 plot is nonblank, and verifies the run 633 archive
     checksum and 805-entry count.
132. Commit/PR summary current manifest-audit refresh is packaged in run 646.
     It supersedes run 643 for commit preparation, records run 645 as the
     current state audit, preserves run 642 as the no-confidence manifest CLI
     smoke, and keeps run 633 as the current handoff archive.
133. Next-action queue manifest-audit refresh is packaged in run 647. It
     points state audit to run 645, commit preparation to run 646, local
     validation to run 639, objective CLI smokes to runs 611 and 642,
     manuscript validation to run 636, archive handoff to run 633, and restart
     to run 626.
134. Post-manifest-audit resume checkpoint is packaged in run 648. It
     supersedes run 626 as the current restart checkpoint after validating run
     647, while preserving run 639 as local validation, run 636 as manuscript
     validation, run 645 as state audit, run 646 as commit preparation, run
     647 as next-action queue, and run 633 as the current packaged archive.
135. Commit/PR summary current resume-checkpoint refresh is packaged in run
     649. It supersedes run 646 for commit preparation, records run 648 as the
     current restart checkpoint, preserves run 645 as the state audit, and
     keeps run 633 as the current packaged archive.
136. Next-action queue resume-checkpoint refresh is packaged in run 650. It
     points restart to run 648, commit preparation to run 649, local validation
     to run 639, objective CLI smokes to runs 611 and 642, manuscript
     validation to run 636, state audit to run 645, and archive handoff to run
     633.
137. Current resume-checkpoint state audit is packaged in run 651. It validates
     run 647-650 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 650 points restart to run 648 and
     commit preparation to run 649, and verifies the run 633 archive checksum
     and 805-entry count.
138. Commit/PR summary current state-audit refresh is packaged in run 652. It
     supersedes run 649 for commit preparation, records run 651 as the current
     state audit, preserves run 648 as restart, and keeps run 633 as the
     current packaged archive.
139. Next-action queue state-audit refresh is packaged in run 653. It points
     state audit to run 651, commit preparation to run 652, restart to run 648,
     local validation to run 639, objective CLI smokes to runs 611 and 642,
     manuscript validation to run 636, and archive handoff to run 633.
140. Current state archive coverage audit is packaged in run 654. It confirms
     the run 633 archive is checksum-valid with 805 entries but stale for the
     current local state: 42 paths are not covered, 99 files are missing from
     the archive, 6 covered files changed, and the current candidate handoff
     set is about 260.7 MiB before compression.
141. Commit/PR summary current archive-coverage refresh is packaged in run 655.
     It supersedes run 652 for commit preparation, records run 654 as the
     current archive coverage audit, preserves run 648 as restart, and keeps
     run 633 as the checksum-valid but stale packaged archive.
142. Next-action queue archive-coverage refresh is packaged in run 656. It
     points archive coverage to run 654, commit preparation to run 655, state
     audit to run 651, restart to run 648, local validation to run 639,
     objective CLI smokes to runs 611 and 642, manuscript validation to run
     636, and archive handoff to run 633.
143. Candidate confidence non-finite hardening is packaged in run 657. It makes
     confidence labels treat NaN, infinity, and non-numeric margins as missing,
     makes ambiguity intervals ignore non-finite candidate misfits, and
     validates with 7/7 candidate-confidence tests, 22/22 reporting-focused
     tests, and 265/265 full-suite tests.
144. Commit/PR summary candidate-confidence refresh is packaged in run 658. It
     supersedes run 655 for commit preparation, records run 657 as the current
     local validation checkpoint, preserves run 654 as archive coverage audit,
     run 651 as state audit, and run 648 as restart.
145. Next-action queue candidate-confidence refresh is packaged in run 659. It
     points local validation to run 657, commit preparation to run 658, archive
     coverage to run 654, state audit to run 651, restart to run 648,
     objective CLI smokes to runs 611 and 642, manuscript validation to run
     636, and archive handoff to run 633.
146. Current candidate-confidence state audit is packaged in run 660. It
     validates run 657-659 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 659 points local validation to run
     657 and commit preparation to run 658, and confirms run 657 records
     265/265 full-suite validation.
147. Commit/PR summary candidate-confidence audit refresh is packaged in run
     661. It supersedes run 658 for commit preparation, records run 660 as the
     current state audit, preserves run 657 as local validation, run 654 as
     archive coverage audit, and run 648 as restart.
148. Next-action queue candidate-confidence audit refresh is packaged in run
     662. It points state audit to run 660, commit preparation to run 661,
     local validation to run 657, archive coverage to run 654, restart to run
     648, objective CLI smokes to runs 611 and 642, manuscript validation to
     run 636, and archive handoff to run 633.
149. Candidate confidence row-sanitization hardening is packaged in run 663. It
     nulls non-finite optional numeric fields in flattened confidence rows,
     hardens competing-geometry comparison against malformed x/z fields, and
     validates with 8/8 candidate-confidence tests, 22/22 reporting-focused
     tests, and 266/266 full-suite tests.
150. Commit/PR summary candidate row-sanitization refresh is packaged in run
     664. It supersedes run 661 for commit preparation, records run 663 as the
     current local validation checkpoint, preserves run 660 as state audit,
     run 654 as archive coverage audit, and run 648 as restart.
151. Next-action queue candidate row-sanitization refresh is packaged in run
     665. It points local validation to run 663, commit preparation to run 664,
     state audit to run 660, archive coverage to run 654, restart to run 648,
     objective CLI smokes to runs 611 and 642, manuscript validation to run
     636, and archive handoff to run 633.
152. Current candidate row-sanitization state audit is packaged in run 666. It
     validates run 663-665 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 665 points local validation to run
     663 and commit preparation to run 664, and confirms run 663 records
     266/266 full-suite validation.
153. Commit/PR summary candidate row-sanitization audit refresh is packaged in
     run 667. It supersedes run 664 for commit preparation, records run 666 as
     the current state audit, preserves run 663 as local validation, run 654 as
     archive coverage audit, and run 648 as restart.
154. Next-action queue candidate row-sanitization audit refresh is packaged in
     run 668. It points state audit to run 666, commit preparation to run 667,
     local validation to run 663, archive coverage to run 654, restart to run
     648, objective CLI smokes to runs 611 and 642, manuscript validation to
     run 636, and archive handoff to run 633.
155. Objective diagnostic non-finite confidence smoke is packaged in run 669.
     It runs the real objective diagnostic CLI on a synthetic summary with
     non-finite objective-confidence values, confirms zero invalid JSON tokens
     and zero non-finite numeric report values, confirms `confidence_csv` is
     present in the manifest, and validates a nonblank 2059 x 1005 plot.
156. Commit/PR summary non-finite confidence smoke refresh is packaged in run
     670. It supersedes run 667 for commit preparation, records run 669 as the
     current non-finite objective confidence CLI smoke, preserves run 663 as
     local validation, and keeps run 666 as state audit.
157. Next-action queue non-finite confidence smoke refresh is packaged in run
     671. It points objective CLI smokes to runs 611, 642, and 669, commit
     preparation to run 670, local validation to run 663, state audit to run
     666, archive coverage to run 654, restart to run 648, manuscript
     validation to run 636, and archive handoff to run 633.
158. Current non-finite confidence smoke state audit is packaged in run 672. It
     validates run 669-671 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 669 smoke validation passes, and
     confirms run 671 points objective CLI smokes to runs 611, 642, and 669.
159. Commit/PR summary non-finite confidence audit refresh is packaged in run
     673. It supersedes run 670 for commit preparation, records run 672 as the
     current state audit, preserves run 669 as objective confidence CLI smoke,
     run 663 as local validation, and run 648 as restart.
160. Next-action queue non-finite confidence audit refresh is packaged in run
     674. It points state audit to run 672, commit preparation to run 673,
     objective CLI smokes to runs 611, 642, and 669, local validation to run
     663, archive coverage to run 654, restart to run 648, manuscript
     validation to run 636, and archive handoff to run 633.
161. Coordinate aggregate row-sanitization hardening is packaged in run 675. It
     finite-normalizes summary metadata and optional numeric confidence-row
     fields before aggregation/serialization, adds JSON-safe row regression
     coverage, and validates with 9/9 aggregate tests, 21/21 related reporting
     tests, and 266/266 full-suite tests.
162. Coordinate aggregate non-finite row smoke is packaged in run 676. It runs
     the real aggregate CLI on a synthetic malformed summary, confirms zero
     invalid JSON/CSV/manifest tokens and zero non-finite output numerics,
     verifies blank CSV cells for non-finite optional row fields, keeps the
     valid row as truth geometry, and validates both aggregate plots as
     nonblank.
163. Commit/PR summary coordinate aggregate smoke refresh is packaged in run
     677. It supersedes run 673 for commit preparation, records run 675 as
     local validation and aggregate row hardening, records run 676 as the
     current aggregate non-finite row CLI smoke, and preserves run 672 as state
     audit, run 654 as archive coverage audit, run 648 as restart, and run 633
     as the checksum-valid but stale archive.
164. Next-action queue coordinate aggregate smoke refresh is packaged in run
     678. It points local validation to run 675, aggregate CLI smokes to runs
     609 and 676, objective CLI smokes to runs 611, 642, and 669, commit
     preparation to run 677, state audit to run 672, archive coverage to run
     654, restart to run 648, manuscript validation to run 636, and archive
     handoff to run 633.
165. Current coordinate aggregate smoke state audit is packaged in run 679. It
     validates run 675-678 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 676 smoke validation passes, and
     confirms run 678 points aggregate CLI smokes to runs 609 and 676 and
     commit preparation to run 677.
166. Commit/PR summary coordinate aggregate audit refresh is packaged in run
     680. It supersedes run 677 for commit preparation, records run 679 as the
     current state audit, preserves run 675 as local validation, run 676 as
     aggregate non-finite row CLI smoke, run 654 as archive coverage audit, run
     648 as restart, and run 633 as the checksum-valid but stale archive.
167. Next-action queue coordinate aggregate audit refresh is packaged in run
     681. It points local validation to run 675, aggregate CLI smokes to runs
     609 and 676, objective CLI smokes to runs 611, 642, and 669, state audit
     to run 679, commit preparation to run 680, archive coverage to run 654,
     restart to run 648, manuscript validation to run 636, and archive handoff
     to run 633.
168. Current state archive coverage audit refresh is packaged in run 682. It
     compares the run 633 archive against the current base state through run
     681, confirms the archive SHA-256 and 805-entry count, finds 0 missing
     base paths, 100 paths not covered by run 633, 235 files missing from run
     633, and 8 already-covered files changed, and keeps archive rebuilds gated
     to external handoff needs.
169. Commit/PR summary current archive coverage refresh is packaged in run
     683. It supersedes run 680 for commit preparation, records run 682 as the
     current archive coverage audit, preserves run 679 as state audit, run 675
     as local validation, run 676 as aggregate non-finite row CLI smoke, run
     648 as restart, and run 633 as the checksum-valid but stale archive.
170. Next-action queue current archive coverage refresh is packaged in run
     684. It points local validation to run 675, aggregate CLI smokes to runs
     609 and 676, objective CLI smokes to runs 611, 642, and 669, state audit
     to run 679, archive coverage to run 682, commit preparation to run 683,
     restart to run 648, manuscript validation to run 636, and archive handoff
     to run 633.
171. IMRAD manuscript current archive-coverage validation refresh is packaged
     in run 685. It updates only manuscript validation/archive pointers to the
     current run 675/676/679/682/683/684 state, validates 63 referenced runs
     with 0 missing, resolves 7/7 embedded images, preserves 5/5 guardrails,
     and changes no scientific claim.
172. Commit/PR summary current manuscript validation refresh is packaged in
     run 686. It supersedes run 683 for commit preparation, records run 685 as
     the current manuscript validation, preserves run 682 as archive coverage
     audit, run 679 as state audit, run 675 as local validation, run 676 as
     aggregate non-finite row CLI smoke, run 648 as restart, and run 633 as the
     checksum-valid but stale archive.
173. Next-action queue current manuscript validation refresh is packaged in run
     687. It points local validation to run 675, aggregate CLI smokes to runs
     609 and 676, objective CLI smokes to runs 611, 642, and 669, state audit
     to run 679, archive coverage to run 682, manuscript validation to run 685,
     commit preparation to run 686, restart to run 648, and archive handoff to
     run 633.
174. Current manuscript/archive state audit is packaged in run 688. It
     validates run 682-687 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 682 archive coverage and run 685
     manuscript validation pass, and confirms run 687 points manuscript
     validation to run 685, archive coverage to run 682, and commit
     preparation to run 686.
175. Commit/PR summary current manuscript/archive audit refresh is packaged in
     run 689. It supersedes run 686 for commit preparation, records run 688 as
     the current state audit, preserves run 685 as manuscript validation, run
     682 as archive coverage audit, run 675 as local validation, run 676 as
     aggregate non-finite row CLI smoke, run 648 as restart, and run 633 as the
     checksum-valid but stale archive.
176. Next-action queue current manuscript/archive audit refresh is packaged in
     run 690. It points local validation to run 675, aggregate CLI smokes to
     runs 609 and 676, objective CLI smokes to runs 611, 642, and 669, archive
     coverage to run 682, manuscript validation to run 685, state audit to run
     688, commit preparation to run 689, restart to run 648, and archive
     handoff to run 633.
177. Current precommit validation after manuscript/archive refresh is packaged
     in run 691. It runs the full suite at 266/266 passing in 24.28 s, confirms
     `git diff --check` is clean, records low resource pressure, and supersedes
     run 675 as the current local validation checkpoint.
178. Commit/PR summary current validation refresh is packaged in run 692. It
     supersedes run 689 for commit preparation, records run 691 as the current
     local validation checkpoint, preserves run 688 as state audit, run 685 as
     manuscript validation, run 682 as archive coverage audit, run 648 as
     restart, and run 633 as the checksum-valid but stale archive.
179. Next-action queue current validation refresh is packaged in run 693. It
     points local validation to run 691, aggregate CLI smokes to runs 609 and
     676, objective CLI smokes to runs 611, 642, and 669, archive coverage to
     run 682, manuscript validation to run 685, state audit to run 688, commit
     preparation to run 692, restart to run 648, and archive handoff to run
     633.
180. Coordinate confidence metadata/default hardening is packaged in run 694.
     It rejects non-finite or negative aggregate default Tx/Rx offsets,
     finite-normalizes candidate-confidence metadata fields before
     serialization, adds regression coverage, and validates with 19/19 focused
     candidate/aggregate tests, 13/13 objective diagnostic tests, and 268/268
     full-suite tests.
181. Coordinate aggregate invalid default smoke is packaged in run 695. It
     validates the real aggregate CLI rejects `nan`, `inf`, and negative
     default Tx/Rx offsets before output allocation, confirms a finite default
     still produces strict JSON/CSV/manifest output with zero non-finite
     numerics, and validates both generated plots as nonblank.
182. Commit/PR summary coordinate default smoke refresh is packaged in run 696.
     It supersedes run 692 for commit preparation, records run 694 as local
     validation and metadata/default hardening, records run 695 as the current
     aggregate invalid-default CLI smoke, and preserves run 688 as state audit,
     run 685 as manuscript validation, run 682 as archive coverage audit, run
     648 as restart, and run 633 as the checksum-valid but stale archive.
183. Next-action queue coordinate default smoke refresh is packaged in run 697.
     It points local validation and metadata/default hardening to run 694,
     aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to
     runs 611, 642, and 669, archive coverage to run 682, manuscript validation
     to run 685, state audit to run 688, commit preparation to run 696, restart
     to run 648, and archive handoff to run 633.
184. Current coordinate default smoke state audit is packaged in run 698. It
     validates runs 694-697 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 694 local validation and run 695
     invalid-default CLI smoke pass, and confirms run 697 points local
     validation to run 694, aggregate CLI smokes to runs 609/676/695, and
     commit preparation to run 696.
185. Commit/PR summary coordinate default audit refresh is packaged in run 699.
     It supersedes run 696 for commit preparation, records run 698 as the
     current state audit, preserves run 694 as local validation and
     metadata/default hardening, run 695 as the current aggregate
     invalid-default CLI smoke, run 685 as manuscript validation, run 682 as
     archive coverage audit, run 648 as restart, and run 633 as the
     checksum-valid but stale archive.
186. Next-action queue coordinate default audit refresh is packaged in run 700.
     It points local validation and metadata/default hardening to run 694,
     aggregate CLI smokes to runs 609, 676, and 695, objective CLI smokes to
     runs 611, 642, and 669, archive coverage to run 682, manuscript validation
     to run 685, state audit to run 698, commit preparation to run 699, restart
     to run 648, and archive handoff to run 633.
187. Current coordinate default audit refresh state audit is packaged in run
     701. It validates runs 698-700 manifests, declared artifacts, docs
     trackers, and infrastructure symlinks, confirms run 698 state audit and
     run 699 inventory are valid, and confirms run 700 points state audit to
     run 698 and commit preparation to run 699.
188. Current precommit validation after coordinate default audit refresh is
     packaged in run 702. It refreshes local validation after the run698-701
     audit/commit/queue chain, passes the full suite at 268/268 in 24.60 s,
     confirms `git diff --check` is clean, and supersedes run 694 as the
     current local validation checkpoint.
189. Commit/PR summary current validation after coordinate default audit
     refresh is packaged in run 703. It supersedes run 699 for commit
     preparation, records run 702 as the current local validation checkpoint,
     preserves run 701 as state audit, run 695 as aggregate invalid-default CLI
     smoke, run 685 as manuscript validation, run 682 as archive coverage
     audit, run 648 as restart, and run 633 as the checksum-valid but stale
     archive.
190. Next-action queue current validation after coordinate default audit
     refresh is packaged in run 704. It points local validation to run 702,
     metadata/default hardening to run 694, aggregate CLI smokes to runs 609,
     676, and 695, objective CLI smokes to runs 611, 642, and 669, archive
     coverage to run 682, manuscript validation to run 685, state audit to run
     701, commit preparation to run 703, restart to run 648, and archive
     handoff to run 633.
191. Current validation after coordinate default audit state audit is packaged
     in run 705. It validates runs 702-704 manifests, declared artifacts, docs
     trackers, and infrastructure symlinks, confirms run 702 local validation
     and run 703 inventory are valid, and confirms run 704 points local
     validation to run 702, state audit to run 701, and commit preparation to
     run 703.
192. Code self-review current validation checkpoint is packaged in run 706. It
     reviews the current candidate-confidence, coordinate aggregate, objective
     diagnostic, and test diffs after run 702 validation and run 705 audit,
     finds zero blocking runtime defects, makes no code edits, and records the
     remaining manifest-helper JSON strictness note as covered by focused tests
     and CLI smokes for the changed reporting paths.
193. Commit/PR summary current review refresh is packaged in run 707. It
     supersedes run 703 for commit preparation, records run 706 as the current
     focused code self-review checkpoint, preserves run 702 as local
     validation, run 705 as state audit, run 685 as manuscript validation, run
     682 as archive coverage audit, run 648 as restart, and run 633 as the
     checksum-valid but stale archive.
194. Next-action queue current review refresh is packaged in run 708. It points
     local validation to run 702, code self-review to run 706, metadata/default
     hardening to run 694, aggregate CLI smokes to runs 609, 676, and 695,
     objective CLI smokes to runs 611, 642, and 669, archive coverage to run
     682, manuscript validation to run 685, state audit to run 705, commit
     preparation to run 707, restart to run 648, and archive handoff to run
     633.
195. Current review refresh state audit is packaged in run 709. It validates
     runs 706-708 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 706 code self-review has zero
     blocking findings and run 707 inventory is valid, and confirms run 708
     points code self-review to run 706 and commit preparation to run 707.
196. Current state archive coverage audit refresh is packaged in run 710. It
     verifies the run 633 archive checksum and 805-entry count, audits current
     local state through run 709 and docs/experiments/242, records 371 base
     paths, 947 base files, 156 paths and 364 files not covered by run 633, and
     keeps archive rebuilding gated to explicit external handoff need.
197. Commit/PR summary current archive coverage refresh is packaged in run 711.
     It supersedes run 707 for commit preparation, records run 710 as the
     current archive coverage audit, preserves run 702 as local validation, run
     706 as code self-review, run 709 as state audit, run 685 as manuscript
     validation, run 648 as restart, and run 633 as the checksum-valid but
     stale packaged archive.
198. Next-action queue current archive coverage refresh is packaged in run 712.
     It points local validation to run 702, code self-review to run 706,
     metadata/default hardening to run 694, aggregate CLI smokes to runs 609,
     676, and 695, objective CLI smokes to runs 611, 642, and 669, archive
     coverage to run 710, manuscript validation to run 685, state audit to run
     709, commit preparation to run 711, restart to run 648, and archive
     handoff to run 633.
199. Current archive coverage refresh state audit is packaged in run 713. It
     validates runs 710-712 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 710 archive coverage remains pass
     with the run 633 checksum verified, confirms run 711 inventory is valid,
     and confirms run 712 points archive coverage to run 710 and commit
     preparation to run 711.
200. Current precommit validation after archive coverage refresh is packaged in
     run 714. It refreshes local validation after the run710-713 archive
     coverage audit chain, passes the full suite at 268/268 in 24.41 s,
     confirms `git diff --check` is clean, and supersedes run 702 as the
     current local validation checkpoint.
201. Commit/PR summary current validation refresh is packaged in run 715. It
     supersedes run 711 for commit preparation, records run 714 as the current
     local validation checkpoint, preserves run 706 as code self-review, run
     713 as state audit, run 710 as archive coverage audit, run 685 as
     manuscript validation, run 648 as restart, and run 633 as the
     checksum-valid but stale archive.
202. Next-action queue current validation refresh is packaged in run 716. It
     points local validation to run 714, code self-review to run 706,
     metadata/default hardening to run 694, aggregate CLI smokes to runs 609,
     676, and 695, objective CLI smokes to runs 611, 642, and 669, archive
     coverage to run 710, manuscript validation to run 685, state audit to run
     713, commit preparation to run 715, restart to run 648, and archive
     handoff to run 633.
203. Current validation refresh state audit is packaged in run 717. It
     validates runs 714-716 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 714 local validation passes 268/268
     with clean diff check, confirms run 715 inventory is valid, and confirms
     run 716 points local validation to run 714 and commit preparation to run
     715.
204. Code self-review current validation refresh is packaged in run 718. It
     reviews the current candidate-confidence, coordinate aggregate, objective
     diagnostic, and test diffs after run 714 validation and run 717 audit,
     reruns the focused tests at 32/32 in 0.30 s, finds zero blocking runtime
     defects, and makes no code edits.
205. Commit/PR summary current review refresh is packaged in run 719. It
     supersedes run 715 for commit preparation, records run 718 as the current
     focused code self-review checkpoint, preserves run 714 as local
     validation, run 717 as state audit, run 710 as archive coverage audit, run
     685 as manuscript validation, run 648 as restart, and run 633 as the
     checksum-valid but stale archive.
206. Next-action queue current review refresh is packaged in run 720. It points
     local validation to run 714, code self-review to run 718, metadata/default
     hardening to run 694, aggregate CLI smokes to runs 609, 676, and 695,
     objective CLI smokes to runs 611, 642, and 669, archive coverage to run
     710, manuscript validation to run 685, state audit to run 717, commit
     preparation to run 719, restart to run 648, and archive handoff to run
     633.
207. Current review refresh state audit is packaged in run 721. It validates
     runs 718-720 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 718 code self-review has zero
     blocking findings and run 719 inventory is valid, and confirms run 720
     points code self-review to run 718 and commit preparation to run 719.
208. Current state archive coverage audit refresh is packaged in run 722. It
     verifies the run 633 archive checksum and 805-entry count, audits current
     local state through run 721 and docs/experiments/254, records 395 base
     paths, 1003 base files, 180 paths and 420 files not covered by run 633,
     and keeps archive rebuilding gated to explicit external handoff need.
209. Commit/PR summary current archive coverage refresh is packaged in run 723.
     It supersedes run 719 for commit preparation, records run 722 as the
     current archive coverage audit, preserves run 714 as local validation, run
     718 as code self-review, run 721 as state audit, run 685 as manuscript
     validation, run 648 as restart, and run 633 as the checksum-valid but
     stale packaged archive.
210. Next-action queue current archive coverage refresh is packaged in run 724.
     It points local validation to run 714, code self-review to run 718,
     metadata/default hardening to run 694, aggregate CLI smokes to runs 609,
     676, and 695, objective CLI smokes to runs 611, 642, and 669, archive
     coverage to run 722, manuscript validation to run 685, state audit to run
     721, commit preparation to run 723, restart to run 648, and archive
     handoff to run 633.
211. Current archive coverage refresh state audit is packaged in run 725. It
     validates runs 722-724 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 722 archive coverage remains pass
     with the run 633 checksum verified, confirms run 723 inventory is valid,
     and confirms run 724 points archive coverage to run 722 and commit
     preparation to run 723.
212. Current precommit validation after archive coverage audit refresh is
     packaged in run 726. It refreshes local validation after the run722-725
     archive coverage audit chain, passes the full suite at 268/268 in 24.43 s,
     confirms `git diff --check` is clean, and supersedes run 714 as the
     current local validation checkpoint.
213. Commit/PR summary current validation refresh is packaged in run 727. It
     supersedes run 723 for commit preparation, records run 726 as the current
     local validation checkpoint, preserves run 718 as code self-review, run
     725 as state audit, run 722 as archive coverage audit, run 685 as
     manuscript validation, run 648 as restart, and run 633 as the
     checksum-valid but stale archive.
214. Next-action queue current validation refresh is packaged in run 728. It
     points local validation to run 726, code self-review to run 718,
     metadata/default hardening to run 694, aggregate CLI smokes to runs 609,
     676, and 695, objective CLI smokes to runs 611, 642, and 669, archive
     coverage to run 722, manuscript validation to run 685, state audit to run
     725, commit preparation to run 727, restart to run 648, and archive
     handoff to run 633.
215. Current validation refresh state audit is packaged in run 729. It
     validates runs 726-728 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 726 local validation passes 268/268
     with clean diff check, confirms run 727 inventory is valid, and confirms
     run 728 points local validation to run 726 and commit preparation to run
     727.
216. IMRAD manuscript current validation refresh is packaged in run 730. It
     updates the run 562 manuscript validation/archive and Data And Code
     Availability pointers to run 718 code self-review, run 722 archive
     coverage, run 726 local validation, run 727 commit preparation, run 728
     queue, and run 729 state audit; lint passes with 68 referenced runs, 0
     missing runs, 7 resolved embedded figures, and all five guardrails
     present.
217. Commit/PR summary current manuscript validation refresh is packaged in
     run 731. It supersedes run 727 for commit preparation, records run 730 as
     current manuscript validation and run 729 as current state audit, and
     preserves run 726 local validation, run 718 code self-review, run 722
     archive coverage, run 648 restart, and run 633 as checksum-valid but
     stale packaged archive.
218. Next-action queue current manuscript validation refresh is packaged in
     run 732. It points manuscript validation to run 730, local validation to
     run 726, code self-review to run 718, state audit to run 729, archive
     coverage to run 722, commit preparation to run 731, restart to run 648,
     archive handoff to run 633, and leaves GPU work gated.
219. Current manuscript validation refresh state audit is packaged in run 733.
     It validates runs 730-732 manifests, declared artifacts, docs trackers,
     and infrastructure symlinks, confirms run 730 manuscript checks pass
     7/7, run 731 summary checks pass 5/5, run 732 queue pointer checks pass
     11/11, and planning doc pointer checks pass 3/3.
220. Current state archive coverage audit refresh is packaged in run 734. It
     verifies the run 633 archive checksum and 805-entry count, audits current
     local state through run 733 and docs/experiments/266, records 419 base
     paths, 1060 base files, 204 paths and 477 files not covered by run 633,
     and keeps archive rebuilding gated to explicit external handoff need.
221. Commit/PR summary current archive coverage refresh is packaged in run
     735. It supersedes run 731 for commit preparation, records run 734 as the
     current archive coverage audit and run 733 as current state audit, keeps
     run 726 as local validation, run 718 as code self-review, run 730 as
     manuscript validation, run 648 as restart, and run 633 as the
     checksum-valid but stale packaged archive.
222. Next-action queue current archive coverage refresh is packaged in run
     736. It points archive coverage to run 734, commit preparation to run
     735, manuscript validation to run 730, local validation to run 726, code
     self-review to run 718, state audit to run 733, restart to run 648,
     archive handoff to run 633, and leaves GPU work gated.
223. Current archive coverage refresh state audit is packaged in run 737. It
     validates runs 734-736 manifests, declared artifacts, docs trackers, and
     infrastructure symlinks, confirms run 734 archive checks pass 9/9, run
     735 summary checks pass 5/5, run 736 queue pointer checks pass 11/11, and
     planning doc pointer checks pass 3/3.
224. Post-archive-coverage audit resume checkpoint is packaged in run 738. It
     supersedes run 648 as the current crash-recovery checkpoint, points local
     validation to run 726, code self-review to run 718, manuscript validation
     to run 730, archive coverage to run 734, state audit to run 737, commit
     preparation to run 735, next-action queue to run 736, and archive handoff
     to run 633.
225. Experiment archive health report current is packaged in run 739. It audits
     738 numbered output folders and confirms the post-run-535 pace change was
     mostly reporting/checkpoint inflation rather than faster physics:
     runs 431-534 have 104/104 data dirs, 101/104 figure dirs, and 101/104
     figure-note coverage, while runs 535-730 contain 169/196
     reporting/audit/checkpoint records, only 8 figure dirs, and only 7 figure
     note folders. It establishes the current guardrail that physical or
     diagnostic runs must carry data and figure notes when images exist, and
     pointer-only numbered runs should be rare.
```

## Plain Summary

The current result is not "we can always identify every rebar point exactly."
The result is more specific:

```text
When acquisition geometry is adequate, the pipeline recovers the correct
locations and radii in the tested synthetic multi-rebar cases. When the
objective has a near-tie, the system now reports that as an interval instead
of hiding it behind a single best point.
```

The strongest current engineering product is therefore:

```text
detector/assignment -> location-only correction -> focused target polish with
ambiguity reporting -> optional acquisition refinement -> joint radius tuple
estimation -> replayable summary package.
```
