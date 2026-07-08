# Field Experiment Index

## Dataset Families

| Dataset family | Trackers | Output root | Status |
| --- | --- | --- | --- |
| `local_gssi_51600s_2026_06_09` | `001-156` | `outputs/field_experiments/local_gssi_51600s_2026_06_09/` | CPU/GPU-bounded DZT import/QC, timing/repeatability QC, supported-interval visual QC, measured-event support tiers, field publication bundles, dataset-policy synthesis, measured cue/support cataloging, current source-figure notes, cue timing-envelope integration, spatial-transfer/interval/dimensionality guardrails, consolidated time-zero evidence, short-anchor leave-one redundancy audit, the post-leave-one time-zero evidence ladder, short-anchor spatial-consistency guardrails, field inversion/HPC readiness synthesis, short-anchor waveform-coherence QC, short-anchor radius-degeneracy guardrails, signed short-anchor morphology QC, signed-morphology threshold-margin sensitivity, field publication-bundle freshness auditing, signed-morphology timing-margin auditing, signal-contrast guardrail/sensitivity auditing, curated post-signal-contrast field publication-bundle refresh, source-figure note coverage, signal-contrast regime synthesis, field inversion blocker mapping, controlled-acquisition design from blockers, existing-data/control manifesting, time-zero control-gap manifesting, controlled 2D acquisition protocol design, controlled 2D packet-template generation, controlled 2D packet validation, current-archive packet prefill, current-archive packet validation, external time-zero reference requirement synthesis, type-aware controlled-packet validation/action planning, field-QC-to-controlled-collection bridging, controlled-collection handoff, and controlled-collection critical-path auditing. Current endpoints are the cue/support traceability catalog in run `113`, latest source-note backfill in run `134`, cue timing-envelope integration in run `115`, spatial-transfer/interval/dimensionality guardrails in runs `116-118`, the original time-zero evidence ladder in run `119`, the short-anchor leave-one audit in run `120`, the post-leave-one ladder in run `121`, the short-anchor spatial-consistency audit in run `122`, the inversion/HPC readiness synthesis in run `123`, the short-anchor waveform-coherence audit in run `124`, the short-anchor radius-degeneracy audit in run `125`, the short-anchor signed-morphology audit in run `126`, the signed-morphology threshold sensitivity in run `127`, the publication-bundle freshness audit in run `128`, the signed-morphology timing-margin audit in run `129`, signal-contrast audit/sensitivity in runs `131-132`, the curated field publication-claim bundle in run `133`, the signal-contrast regime synthesis in run `135`, the inversion blocker map in run `136`, the controlled 2D acquisition-design matrix in run `137`, the existing-data control manifest in run `138`, the time-zero control-gap manifest in run `139`, the controlled 2D acquisition protocol in run `140`, the generated controlled-acquisition packet in run `141`, the packet validator in run `142`, the current-archive packet prefill in run `143`, the prefill validation in run `144`, the external reference requirement in run `145`, the corrected type-aware packet/action chain in runs `152-153`, the current QC-to-controlled-collection bridge in run `154`, the controlled collection run sheet in run `155`, and the controlled-collection critical path in run `156`. The current field boundary remains scoped 2D line-profile calibration/QC and signed waveform-morphology timing QC, not absolute time-zero, conservative timing promotion, cover-depth recovery, radius recovery, radius seeding, amplitude calibration, strict window-invariant contrast, automatic bundle promotion, FWI, 3D inversion, HPC workload, or synthetic-policy relabeling. |

Runs `110`, `112`, `133`, and `134` are the current field event-support,
dataset-policy, curated publication-bundle, and source-note endpoints. Run
`110` supersedes run `109`, which had the same
numeric support table but cramped figure labels. Runs `111-112` promote the
refreshed event-support table, the `105` timing scorecard, and the `106`
2D-only/no-HPC decision into the structured field evidence chain while
preserving the no-field-FWI/no-3D/no-HPC boundary; run `130` supersedes run
`111` as the current curated publication bundle by adding the signed
morphology chain and timing-margin evidence from runs `124-129`, and run `133`
supersedes run `130` by adding the signal-contrast guardrail and sensitivity
caveat from runs `131-132`. Run `113` is the current
cue/support catalog endpoint: it separates 19 raw measured reflector cues from
11 derived support anchors for manuscript traceability without creating
known-truth field labels. Run `114` completes source-figure notes for the
then-current run `111` publication bundle: 22 source figures, 22 notes present,
and no missing figures. Run `115` overlays the run `113` support anchors with the
run `075` conservative short-pair timing envelope: 3/3 short anchors are inside
the envelope, while 8/8 long pattern anchors reject short-transfer. Runs
`116-118` keep long-profile transfer, 3D/HPC, and field-FWI blocked while
supporting short-profile 2D QC. Run `119` consolidates the initial time-zero
evidence ladder. Run `120` shows that the timing-only short anchor can be
removed and the two content-backed anchors still support a narrow relative
timing interval, but the claim is not leave-one-content redundant. Run `121`
promotes that leave-one/content-only result into the current time-zero evidence
ladder: short-profile relative timing QC remains supported, while long-transfer,
absolute time-zero, field FWI, 3D/HPC, and calibrated depth/radius recovery stay
blocked.
Run `122` checks whether the two content-backed short anchors can support a
single spatial translation between corrected-stack position and measured cue
position. The content residual range is 29.997 mm, the half-range is 14.9985
mm, and the minimum supported-interval margin is 13.332 mm, so a single
profile spatial calibration is not supported even though short-profile
relative timing QC remains supported.
Run `123` consolidates the field inversion/HPC readiness evidence after run
`122`: short-profile relative timing QC and apparent-depth scale QC are
supported, while long-profile transfer, profile spatial calibration,
cover-depth recovery, radius recovery, field FWI, and 3D/HPC remain blocked.
Run `124` audits short-anchor waveform coherence from saved field waveform and
alignment artifacts: both content-backed short anchors are morphology-coherent
after correction, but radius matches are 0/2, one spatial translation is not
supported, and leave-one-content redundancy remains absent. It supports
waveform-morphology QC only, not geometry/radius seeds, field FWI, or 3D/HPC.
Run `125` audits the saved radius sweep behind those two content-backed short
anchors. All four selected side-wise radii are local bests, but all four radius
gaps are weak, both selected pairs have repeat-profile radius mismatches, and
forced common-radius alternatives are near-tied. This keeps radius seeding,
radius recovery, geometry seeding, field FWI, 3D/HPC, and heavy field work
blocked.
Run `126` audits signed field-trace morphology behind those same two
content-backed short anchors. Both corrected pairs keep same polarity and pass
signed morphology QC, but the comparison remains robust-normalized and still
inherits the radius/spatial/depth guardrails from runs `122-125`. It supports
field supplement morphology QC, not amplitude calibration, radius/geometry
seeding, field FWI, 3D/HPC, or heavy field work.
Run `127` sweeps signed-morphology thresholds for those two content-backed
anchors. Default and moderate-tightening gates pass, but only 36/320 threshold
combinations support both pairs and strict morphology claims fail. This keeps
the field claim as threshold-margin supplement evidence, not amplitude
calibration, radius/geometry recovery, field FWI, 3D/HPC, or heavy field work.
Run `128` audits whether the curated field publication bundle should be
refreshed with the latest short-anchor morphology-chain figures. The current
22-figure bundle contains none of the four run `124-127` candidates; all four
figures exist and are QC-ready, with runs `126-127` as primary refresh
candidates and runs `124-125` as guardrail candidates. This supports a curated
refresh decision only, not automatic bundle promotion, field FWI, 3D/HPC,
radius/geometry recovery, or cover-depth claims.
Run `129` compares signed-morphology timing slack with the current time-zero
ladder. The default 0.05 ns timing cap leaves at least 0.030354 ns slack, which
covers the content-only half-range of 0.009823 ns for both content-backed pairs,
but it does not cover the conservative all-short half-width of 0.058939 ns.
This supports content-only morphology timing QC, not absolute time-zero,
conservative timing promotion, field FWI, 3D/HPC, or heavy field work.
Run `130` deliberately refreshes the field publication claim bundle after runs
`128-129`: it packages 27 figure rows and 24 claim boundaries, uses the current
run `110` event-support table, and adds the short-anchor waveform-coherence,
radius-degeneracy, signed-morphology, threshold-sensitivity, and timing-margin
figures. This is a curated field-supplement bundle only; field FWI, 3D/HPC,
absolute time-zero, conservative timing, radius/geometry/cover-depth recovery,
amplitude calibration, and synthetic-policy relabeling remain blocked.
Run `131` adds a local signal-contrast guardrail for those same content-backed
short anchors. All four reference/aligned-comparison side windows clear the
pre-event contrast gate, with minimum event/pre-event RMS ratio 4.129x and
minimum event peak/pre-event-p95 ratio 12.399x. This strengthens field
morphology QC but still blocks absolute amplitude calibration,
radius/geometry/cover-depth recovery, field FWI, 3D/HPC, and heavy field work.
Run `132` stress-tests that contrast gate over 27 aperture/event/noise-window
combinations. The default combination still passes, but only 13/27 combinations
support all four side windows and the worst tight/near-window setting supports
only 2/4. This keeps the signal-contrast result as a default-window morphology
QC guardrail, not a strict window-invariant or amplitude-calibrated field claim.
Run `133` refreshes the curated publication claim bundle after runs `131-132`.
It packages 29 figure rows and 25 claim boundaries, keeps the run `110`
event-support table, and adds the signal-contrast plus sensitivity figures to
the existing morphology/timing-margin chain. This is the current field
publication bundle endpoint and remains measured-field 2D QC only, not
absolute time-zero, conservative timing, amplitude calibration, strict
window-invariant contrast, radius/geometry/cover-depth recovery, field FWI,
3D/HPC, or synthetic-policy relabeling.
Run `134` audits source-figure notes for the run `133` bundle. All 29 source
figures already have notes, no figures are missing, and no existing notes were
rewritten. This is the current source-note endpoint for manuscript handoff.
Run `135` synthesizes the run `132` signal-contrast sensitivity table by
regime. The broad event window is supported across all 9 tested aperture/noise
settings with minimum RMS ratio 5.05x, while default windows are mixed and
tight windows fail. This supports a broad-window field morphology-contrast
regime only; strict window-invariant contrast, amplitude calibration, field
FWI, 3D/HPC, and heavy field work remain blocked.
Run `136` maps the latest timing, signed morphology, timing-margin, and
broad-window contrast evidence against the remaining inversion blockers. All
six positive evidence axes are ready for a scoped field morphology supplement,
but all nine blocker axes remain unresolved, including six critical blockers:
absolute time-zero, profile spatial calibration, radius/geometry seeding,
absolute amplitude calibration, cover-depth recovery, and field FWI. Field
3D/HPC remains blocked because the archive is independent 2D line profiles.
Run `137` translates those blockers into a future controlled 2D acquisition
design. It identifies five must-have controls before field inversion can be
defensible: absolute time-zero reference, surveyed profile/target geometry,
known target radius/diameter, known cover depth plus dielectric/velocity
calibration, and reference amplitude calibration. The current archive remains
QC-only, and field FWI/3D/HPC/heavy field work remain blocked.
Run `138` maps the actual existing local GSSI files and saved field QC outputs
against the run `137` controls. The archive contains four DZT/DZX 2D line
profiles with 7.215945 m of parsed profile length and useful relative
timing/morphology/spatial/contrast QC evidence, but it satisfies 0/5
must-have inversion controls. Current field FWI, heavy field GPU work, and
3D/HPC field claims remain blocked; the next field-facing work is controlled
2D acquisition protocol or metadata collection, not inversion.
Run `139` consolidates the current timing evidence against the absolute
time-zero control gap. It confirms 0 absolute time-zero candidates in the
current archive: short content-backed relative timing is supported at
0.127701 ns, while the early/direct component is a 0 ns common-mode negative
control and differs from the content timing by more than the conservative
half-width. Current field FWI and heavy field work remain blocked until an
external timing reference is collected.
Run `140` converts the current blockers into a controlled 2D acquisition
protocol. It defines 8 protocol steps, 5 metadata tables, 51 required metadata
fields, 7 acceptance gates, and a minimum of 3 short-profile repeats per
controlled target. The output includes a field-sheet template for collecting
session, target-truth, profile-geometry, acquisition-run, and reference
measurement metadata. Current-archive field FWI/heavy work remains blocked.
Run `141` turns that protocol into an executable field packet: five separate
CSV templates, 51 required-field validation rules, and a current-archive
prefill-limit table. The existing GSSI archive can partially prefill
session/profile/acquisition provenance, but target-truth and reference-
measurement tables remain blocked. Current-archive field FWI, heavy field GPU
work, and field 3D/HPC remain blocked until a future filled packet passes the
metadata and acceptance gates.
Run `142` validates the generated run `141` packet. The blank packet fails by
design: 0/5 rows are filled, all 51 required-field checks are blocking
findings, and all seven acceptance gates remain false. This makes the field
handoff rule executable: no field FWI, heavy GPU field work, or field 3D/HPC
until a filled controlled-acquisition packet passes the validator.
Run `143` pre-fills a packet copy from the existing archive where provenance is
defensible: one session row, four profile rows, and four acquisition rows. It
leaves target truth and reference-measurement rows blank because the archive
does not contain known target geometry, target crossings, Tx/Rx offset
confirmation, or external time-zero/amplitude references.
Run `144` validates that partially filled packet. It has 9 filled rows out of
11 total rows, no dtype or cross-table failures, but still has 67 blocking
missing required values and 0/7 acceptance gates ready. Field FWI, heavy field
GPU work, and field 3D/HPC remain blocked.
Run `145` quantifies the missing external time-zero reference requirement. At
the current archive dielectric setting `epsr=2.25`, the protocol gate of
`0.02 ns` reference uncertainty is about `1.9986 mm` two-way depth equivalent.
The existing conservative relative half-width is about `5.8898 mm`, and the
short-vs-early timing conflict is about `12.7613 mm`. The requirement is now
defined, but the current archive has zero external timing references, so
absolute time-zero, calibrated depth, field FWI, heavy field GPU work, and
field 3D/HPC remain blocked.
Run `146` collapses the run `144` packet-validation blockers and run `145`
reference requirement into a prioritized controlled-acquisition action set.
The 67 blocking findings become 7 action groups: target truth, time-zero
reference, amplitude reference, surveyed profile/target geometry, controlled
acquisition links, session metadata, and reference registry. Six groups require
new controlled data; only session metadata may be recoverable from notes. All
seven acceptance gates remain blocked, so current-archive field FWI, heavy
field GPU work, and field 3D/HPC remain blocked.
Run `147` converts that action set into a collection-ready controlled 2D packet
scaffold. It writes five packet CSVs with one planned session, one target, one
short-repeat profile, three acquisition repeats, three time-zero references,
and three amplitude references. The scaffold intentionally leaves 72 measured
or session fields blank and marks the validator as expected to fail until real
controlled data are entered. It is ready as a field-collection worksheet, not
as completed data or an inversion launch gate.
Run `148` validates that run `147` scaffold with the existing packet validator.
All 12 scaffold rows are filled enough to be recognized, dtype failures are
zero, and cross-table failures are zero. The packet still has 60 blocking
missing required values and 0/7 acceptance gates ready, so it remains a
collection worksheet rather than accepted field data.
Run `149` compares the scaffold validation against the current-archive prefill
validation from run `144`. Filled rows improve from 9 to 12, missing required
values drop from 67 to 60, target-truth evidence changes from 0 to 1 row, and
short-repeat target evidence changes from 0 to 1. Time-zero and amplitude
reference evidence remain 0, and all acceptance gates remain blocked. Field
FWI, heavy field GPU work, and field 3D/HPC remain blocked.
Run `150` recovers the only defensible extra current-archive session metadata
found in the raw DZX sidecars: antenna serial `3385` and display gain `0`.
The recovered packet drops missing required values from 67 to 65 and session
missing fields from 3 to 1, with no dtype or cross-table failures. Operator,
target truth, surveyed endpoints/crossings, controlled Tx/Rx/coupling, and
external timing/amplitude references remain missing, so field FWI, heavy field
GPU work, and field 3D/HPC remain blocked.
Run `151` applies the recovered same-system session metadata to the future
controlled-collection scaffold from run `147`. The scaffold now carries antenna
serial `3385`, software version `1.4.35`, gain setting `0`, and time range
`5.0 ns`, with a note to verify/update them on collection day. Validation
missing required values drop from 60 to 56 and session missing fields from 6
to 2. The worksheet remains unaccepted because target truth, surveyed geometry,
controlled Tx/Rx/coupling, and measured time-zero/amplitude references are
still absent; field FWI, heavy field GPU work, and field 3D/HPC remain blocked.
Run `152` reruns the recovered scaffold validation after making the packet
validator reference-type-aware. The previous validator counted time-zero fields
as required on `amplitude_reflector` rows and amplitude fields as required on
`metal_plate_t0` rows. The corrected validation preserves the same packet and
scientific state, but reduces the scaffold blocker count from 56 to 44 missing
required values: 2 session, 9 target-truth, 6 profile-geometry, 9 acquisition,
and 18 type-specific reference fields. All seven acceptance gates remain
blocked, so the current field archive and scaffold still do not support field
FWI, heavy field GPU work, or field 3D/HPC.
Run `153` regenerates the controlled-collection action plan from that
type-aware validation. The 44 blockers collapse into seven action groups:
target-truth geometry (9 fields), time-zero references (6), amplitude
references (6), profile-target geometry (6), acquisition-control links (9),
session metadata (2), and reference file registry (6). Six groups still require
new controlled field data; only session date/operator may be recovered or
recollected as metadata. The updated plan is ready for a future controlled 2D
field pass, not for current-archive field FWI, heavy field GPU work, or field
3D/HPC.
Run `154` bridges the current field-QC evidence to the corrected
controlled-collection action plan. Five current-archive axes are supported for
scoped 2D field-QC/manuscript supplement use: independent 2D line-profile
scope, short relative timing, waveform morphology, content-only timing margin,
and broad-window signal contrast. Four inversion blockers remain unresolved:
absolute time-zero, amplitude calibration, target truth/profile geometry, and
packet acceptance. The five critical new-data groups remain target truth,
time-zero references, amplitude references, surveyed profile geometry, and
controlled acquisition links; field FWI, heavy field GPU work, and field
3D/HPC remain blocked.
Run `155` packages that boundary into the current controlled-collection
handoff. It writes a run-sheet Markdown file, action CSV, packet fill map,
gate handoff table, and summary figure using runs `151-154` as sources. All
12 planned packet rows still need collection entry, all seven acceptance gates
remain blocked, and the five critical new-data groups are unchanged. This is
ready for a future controlled 2D field pass, not for current-archive field
FWI, heavy local GPU field work, field 3D/HPC, or neural-network training.
Run `156` audits the critical path from that run sheet to packet acceptance.
All seven gates remain blocked, zero gates can be unblocked by the current
archive alone, and the field-FWI/heavy-work path still requires target truth,
time-zero references, and amplitude references. The current field endpoint is
therefore a controlled-collection checklist, not an inversion or 3D/HPC launch.

Runs `098-100` remain the previous timing-anchor conflict publication/policy
chain and source-note audit, now superseded by `102-104`.

## Policy

Field trackers are dataset-local and should not consume IDs from
`docs/experiments/`, which remains the synthetic simulation and infrastructure
tracker stream.
