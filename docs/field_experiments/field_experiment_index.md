# Field Experiment Index

## Dataset Families

| Dataset family | Trackers | Output root | Status |
| --- | --- | --- | --- |
| `local_gssi_51600s_2026_06_09` | `001-544` | `outputs/field_experiments/local_gssi_51600s_2026_06_09/` | CPU/GPU-bounded DZT import/QC, timing/repeatability QC, supported-interval visual QC, measured-event support tiers, field publication bundles, dataset-policy synthesis, measured cue/support cataloging, current source-figure notes, cue timing-envelope integration, spatial-transfer/interval/dimensionality guardrails, consolidated time-zero evidence, short-anchor leave-one redundancy audit, the post-leave-one time-zero evidence ladder, short-anchor spatial-consistency guardrails, field inversion/HPC readiness synthesis, short-anchor waveform-coherence QC, short-anchor radius-degeneracy guardrails, signed short-anchor morphology QC, signed-morphology threshold-margin sensitivity, field publication-bundle freshness auditing, signed-morphology timing-margin auditing, signal-contrast guardrail/sensitivity auditing, curated post-signal-contrast field publication-bundle refresh, source-figure note coverage, signal-contrast regime synthesis, field inversion blocker mapping, controlled-acquisition design from blockers, existing-data/control manifesting, time-zero control-gap manifesting, controlled 2D acquisition protocol design, controlled 2D packet-template generation, controlled 2D packet validation, current-archive packet prefill, current-archive packet validation, external time-zero reference requirement synthesis, type-aware controlled-packet validation/action planning, field-QC-to-controlled-collection bridging, controlled-collection handoff, controlled-collection critical-path auditing, execution-packet dry-run validation, gate-sensitivity mapping, provenance gating, real-archive acceptance, and real-archive operator worksheeting. Current endpoints are the cue/support traceability catalog in run `113`, latest source-note backfill in run `134`, cue timing-envelope integration in run `115`, spatial-transfer/interval/dimensionality guardrails in runs `116-118`, the original time-zero evidence ladder in run `119`, the short-anchor leave-one audit in run `120`, the post-leave-one ladder in run `121`, the short-anchor spatial-consistency audit in run `122`, the inversion/HPC readiness synthesis in run `123`, the short-anchor waveform-coherence audit in run `124`, the short-anchor radius-degeneracy audit in run `125`, the short-anchor signed-morphology audit in run `126`, the signed-morphology threshold sensitivity in run `127`, the publication-bundle freshness audit in run `128`, the signed-morphology timing-margin audit in run `129`, signal-contrast audit/sensitivity in runs `131-132`, the curated field publication-claim bundle in run `133`, the signal-contrast regime synthesis in run `135`, the inversion blocker map in run `136`, the controlled 2D acquisition-design matrix in run `137`, the existing-data control manifest in run `138`, the time-zero control-gap manifest in run `139`, the controlled 2D acquisition protocol in run `140`, the generated controlled-acquisition packet in run `141`, the packet validator in run `142`, the current-archive packet prefill in run `143`, the prefill validation in run `144`, the external reference requirement in run `145`, the corrected type-aware packet/action chain in runs `152-153`, the current QC-to-controlled-collection bridge in run `154`, the controlled collection run sheet in run `155`, the controlled-collection critical path in run `156`, the prelinked controlled-collection execution packet in run `158`, the corrected dry-run acceptance test in run `160`, the gate-sensitivity map in run `161`, the provenance gate in run `162`, the real-archive acceptance contract in run `176`, and the real-archive operator worksheet in run `177`. The current field boundary remains scoped 2D line-profile calibration/QC and signed waveform-morphology timing QC plus real-archive collection readiness, not absolute time-zero, conservative timing promotion, cover-depth recovery, radius recovery, radius seeding, amplitude calibration, strict window-invariant contrast, automatic bundle promotion, FWI, 3D inversion, HPC workload, or synthetic-policy relabeling. |

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
Run `158` turns that checklist into a prelinked execution packet for a future
controlled 2D collection. It writes 12 planned packet rows across session,
target-truth, profile-geometry, acquisition-repeat, and reference-measurement
tables; cross-table failures are zero because target/profile/reference IDs are
prefilled. The packet is ready as a collection scaffold but not accepted:
51 real measurement/metadata values remain missing, all seven acceptance gates
remain blocked, and field FWI, heavy GPU work, and field 3D/HPC remain blocked.
Run `160` fills a copy of the run `158` packet with explicitly artificial
`DRY_RUN` values and reruns the validator. The dry-run packet has zero missing
required values, zero cross-table failures, and seven of seven ready acceptance
gates, proving that the packet structure and validator can accept a complete
packet. The dry-run values are not field data and do not support field FWI,
heavy GPU work, field 3D/HPC, or publication claims. Run `159` was a same-turn
draft superseded by run `160` because its delta JSON used stale key names.
Run `161` removes one control family at a time from the accepted dry-run
packet. The complete dry-run baseline passes, while all 11 single-blocker
variants fail packet acceptance. The `only_two_controlled_repeats` variant has
zero missing required values and zero cross-table failures but still fails the
repeat redundancy and heavy-work gates, confirming that the repeat gate is not
just a metadata-completeness proxy.
Run `162` adds the provenance gate above structural packet validation. The
run `160` dry-run packet still passes structural validation with zero missing
required values, zero cross-table failures, and seven of seven ready acceptance
gates, but provenance validation blocks it with 42 findings: 32 dry-run or
placeholder-token hits, nine unresolved file references, and one future-date
finding. This creates the required two-stage field policy: a packet must pass
both structural validation and provenance validation before any measured-field
scientific claim, field FWI, heavy GPU work, or field 3D/HPC escalation.
Run `163` collapses those 42 provenance findings into six field-day closure
actions: real session metadata, target-truth provenance, profile-geometry
provenance, three controlled profile-repeat files, three time-zero reference
files, and three amplitude-reference files. The current dry-run archive cannot
close the provenance gate without real measured files and measured metadata.
This is now the current field checkpoint: ready as a collection-day acceptance
checklist, still blocked for provenance acceptance, field FWI, heavy GPU work,
field 3D/HPC, and neural-network training.
Run `164` turns that closure checklist into a fillable field-day intake
manifest. It writes 20 manifest rows: 11 measured metadata values and nine
real-file rows covering three controlled profile repeats, three time-zero
references, and three amplitude references. The manifest is ready for
collection-day use, but provenance acceptance, field FWI, heavy GPU work,
field 3D/HPC, and neural-network training remain blocked until real values,
file paths, and checksums are collected and the structural/provenance gates are
rerun.
Run `165` adds a reusable preflight check for that intake manifest. The blank
run `164` template fails as expected with 89 blocking findings and zero
accepted rows. The preflight now defines the required collection-day evidence
state before structural/provenance reruns: every row accepted, real values or
file paths entered, operator initials and UTC timestamps present, expected
filenames matched, and SHA-256 checksums recorded for all nine measured files.
Field FWI, heavy GPU work, field 3D/HPC, and neural-network training remain
blocked.
Run `166` adds a synthetic pass-case smoke for the run `165` preflight. A
synthetically filled 20-row manifest passes with zero findings, proving the
preflight rule set is achievable. The run is explicitly not measured field
evidence: provenance acceptance, scientific field claims, field FWI, heavy GPU
work, field 3D/HPC, and neural-network training remain blocked until real
collection files and metadata pass the real gates.
Run `167` packages the controlled-collection day work into an operator-facing
checklist. It writes 20 checklist rows: 11 real metadata values and nine real
files, covering three controlled profile repeats, three time-zero references,
and three amplitude references. Six gates are listed before any field-FWI path
can reopen: fill the manifest, record operator/UTC, hash the nine files, run
intake preflight, confirm the synthetic smoke rule remains achievable, and
rerun structural plus provenance gates on real data. This is ready for
collection-day use, not measured field evidence; provenance acceptance, field
FWI, heavy GPU work, field 3D/HPC, and neural-network training remain blocked.
Run `168` turns the nine real-file requirements from run `167` into a checksum
ledger template and command sheet. It writes nine ledger rows and nine
`sha256sum` command templates for the three controlled profile repeats, three
time-zero references, and three amplitude references. This reduces
collection-day transcription ambiguity but is still not measured field
evidence; provenance acceptance, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training remain blocked until real paths and SHA-256 values pass
preflight.
Run `169` adds that checksum-ledger preflight. The current blank ledger fails
with 45 blocking findings: nine rows each missing accepted ledger status, real
file path, SHA-256, operator initials, and UTC timestamp. The preflight is now
ready to verify real paths, file existence, filename agreement, SHA-256 format,
computed hash equality, operator initials, and UTC timestamps before structural
and provenance reruns. Field FWI, heavy GPU work, field 3D/HPC, and
neural-network training remain blocked until a real ledger passes.
Run `170` adds a synthetic pass-case smoke for the checksum-ledger preflight.
It creates nine tiny synthetic files, fills all nine ledger rows with accepted
status, real paths, computed SHA-256 values, operator initials, and UTC
timestamps, and passes the run `169` preflight with zero findings. This proves
the checksum gate is achievable, but it is explicitly synthetic and does not
create measured field evidence. Provenance acceptance, structural rerun, field
FWI, heavy GPU work, field 3D/HPC, and neural-network training remain blocked
until the real controlled-collection files pass the same gate.
Run `171` defines the archive folder layout for those real controlled-
collection files. It maps the nine required DZT files into `raw/profiles`,
`raw/references/time_zero`, and `raw/references/amplitude`, and defines six
metadata artifacts under `metadata/`: session log, target truth, profile
geometry, intake manifest, checksum ledger, and provenance notes. The layout is
ready for collection-day use but still contains no measured evidence. Field FWI,
heavy GPU work, field 3D/HPC, and neural-network training remain blocked until
real files and metadata fill the layout and pass checksum, intake, structural,
and provenance gates.
Run `172` consolidates the collection-day checklist, checksum ledger, and
archive layout into one operator handoff pack. It writes eight operator
sequence steps, nine file handoff rows, 11 metadata-value handoff rows, and a
six-row gate crosswalk. This is now the current operator-facing collection
packet, but it is still not measured field evidence. Field FWI, heavy GPU work,
field 3D/HPC, and neural-network training remain blocked until the real archive
is filled and checksum, intake, structural, and provenance gates all pass.
Run `173` adds an archive-root preflight before checksum and intake. The
current pending archive fails all 23 checks because no real archive exists:
seven directories, nine nonempty DZT files, and six nonempty metadata artifacts
are missing. This is a useful gate, not measured field evidence. Field FWI,
heavy GPU work, field 3D/HPC, and neural-network training remain blocked until
a real archive passes this preflight and then passes checksum, intake,
structural, and provenance gates.
Run `174` adds a synthetic pass-case smoke for the run `173` archive preflight.
It creates a synthetic archive with the seven directories, nine DZT placeholders,
and six metadata artifacts required by run `171`, then passes all 23 archive
preflight checks. This proves the archive gate is achievable but remains
synthetic only: it is not measured field evidence and does not unblock field
FWI, heavy GPU work, field 3D/HPC, or neural-network training.
Run `175` links the synthetic archive layout to the checksum ledger. It fills
the run `168` checksum ledger from the archived synthetic files and passes both
the archive preflight and checksum validation with zero blocking findings. This
is an integration smoke for the archive-to-ledger workflow, not measured field
evidence.
Run `176` consolidates runs `163-175` into one real-archive acceptance
contract. The field path is operationally designed, and the synthetic
archive-to-ledger bridge passes, but real acceptance is still blocked: 11
measured metadata values, nine measured files, six metadata artifacts,
matching SHA-256 checksums, and structural/provenance reruns are still needed.
This is the current field-side decision boundary: no measured-field claim,
field FWI, heavy GPU work, field 3D/HPC, or neural-network training until a
real archive passes the archive, checksum, intake, structural, and provenance
gates.
Run `177` converts that acceptance contract into a single operator-facing
fillable worksheet. It writes 20 worksheet rows: nine measured files and 11
metadata values, tied to eight operator gate phases and the current checksum,
intake, structural, and provenance blockers. This reduces collection-day
ambiguity but does not close the real-data gate. Real archive acceptance,
measured-field claims, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training remain blocked until the worksheet is filled with real
files/metadata and the run `176` gates pass.
Run `178` packages that worksheet and its supporting archive layout, checksum
ledger, intake manifest, acceptance contract, and operator references into a
portable collection-day bundle. The bundle has 16 source files, 19 unique
archive members, and SHA-256
`dd6ed7c7900d75077840c8ab2292c67465282a48e497b2e93c713aefed19ce2a`. It is
ready for collection-day handoff, but it contains no real measured files or
real metadata; real archive acceptance, measured-field claims, field FWI,
heavy GPU work, field 3D/HPC, and neural-network training remain blocked until
the real archive passes archive, checksum, intake, structural, and provenance
gates.
Run `179` verifies that collection-day bundle from the consumer side. The
archive unpacks into one safe root, all 19 members are path-safe, and all 18
checksum entries match the extracted files. This proves the handoff archive is
transport-readable and checksum-consistent, but it still contains forms and
contracts only; real archive acceptance, measured-field claims, field FWI,
heavy GPU work, field 3D/HPC, and neural-network training remain blocked until
real measured files and metadata pass the gates.
Run `180` inventories the current local data folder
`data/2026-06-09_GSSI_model_51600S` against the run `176` acceptance contract.
It finds four DZT files and four DZX sidecars, but zero accepted controlled
files and zero accepted metadata artifacts. Those current-archive files remain
QC context only; they do not satisfy the nine-file controlled archive,
metadata, checksum, intake, structural, or provenance gates. Field FWI, heavy
GPU work, field 3D/HPC, and measured-field claims remain blocked.
Run `181` parses the four current DZX sidecars. They are useful QC metadata:
12 acquisition settings are uniform, and all four sidecars have paired DZT
files. They are not controlled geometry evidence. The sidecars split into
three scan-interval groups (`273`, `806`, and `813`), and the waypoint span is
only `0.003332 m` while scan-derived profile lengths are about `0.91 m`,
`2.69 m`, and `2.71 m`. Use the sidecars as current-archive QC context only;
do not use them as substitutes for controlled profile geometry, target truth,
checksum ledger, provenance notes, or measured reference files.
Run `182` cross-checks the current DZT import records against those DZX
sidecars. All four trace counts match exactly, scan-derived profile lengths
match exactly, and the DZX/header `512` samples per scan versus read `510`
samples has a consistent two-sample delta matching the stored time-zero sample
offset. This strengthens the current archive as internally readable QC data,
but it still does not satisfy controlled archive acceptance or measured-field
claim gates.
Run `183` classifies that boundary explicitly. Four QC-supported gates pass:
raw file inventory, sidecar pairing, uniform acquisition-setting QC, and
DZT/DZX internal consistency. Six controlled-evidence gates still fail:
controlled file roles, controlled metadata artifacts, controlled profile
geometry, target-truth provenance, checksum/intake/structural/provenance
reruns, and field-FWI input readiness. The current archive is therefore QC
ready but not controlled-evidence ready; measured-field claims, field FWI,
heavy GPU work, field 3D/HPC, and neural-network training remain blocked.
Run `184` computes signal-level QC fingerprints from the four current DZT
profiles. All profiles are finite, median-removed corrected RMS spans roughly
`6.7e5` to `1.17e6` counts, and the only same-shape pair
(`PROJECT001C__014.DZT`/`PROJECT001C__016.DZT`) has corrected correlation
`0.3740795978167496` and symmetric L2 `1.11957899163086`. This strengthens the
current archive as readable QC context, but it does not make the short pair a
controlled repeat and does not close controlled file roles, surveyed geometry,
target truth, time-zero references, amplitude references, checksum ledger, or
provenance reruns.
Run `185` extends that QC comparison by normalizing the trace axis before
pairwise comparison. All six profile pairs become comparable for QC, but the
best normalized correlation is still only `0.3740795978167496` and the lowest
symmetric L2 is `1.11957899163086`, again for
`PROJECT001C__014.DZT`/`PROJECT001C__016.DZT`. Treat these as descriptive
signal-QC metrics only, not controlled repeat evidence, measured-field proof,
field FWI readiness, heavy GPU readiness, field 3D/HPC readiness, or
neural-network training readiness.
Run `186` synthesizes the current archive boundary and signal-QC evidence from
runs `183-185`. Four QC-context items pass: archive QC gates, finite signal
fingerprints, the available same-shape signal pair, and normalized pairwise
signal QC. Three controlled blockers still fail: controlled evidence,
controlled repeat evidence, and field-FWI input readiness. The current archive
is therefore useful as QC context only; measured-field claims, field FWI, heavy
GPU work, field 3D/HPC, and neural-network training remain blocked until a real
controlled archive passes the acceptance gates.
Run `187` combines the provenance closure, current archive inventory, and QC
evidence synthesis into one gap matrix. The current archive has four DZT files
and four DZX sidecars and can support QC context, but zero files are promoted
to controlled evidence. Three metadata/provenance gaps and three file gaps
remain open, including nine required real controlled files: three profile
repeats, three time-zero references, and three amplitude references. Measured
field claims, field FWI, heavy GPU work, field 3D/HPC, and neural-network
training remain blocked.
Run `188` validates that gap matrix from a consumer perspective: nine of nine
checks pass, the matrix has six closure groups, three open metadata gaps, three
open file gaps, nine remaining real files, and zero promoted current files.
The current archive remains QC context only; controlled evidence, measured
field claims, field FWI, heavy GPU work, field 3D/HPC, and neural-network
training remain blocked.
Run `189` checks whether the older run `177` operator worksheet still covers
that current gap matrix. It does: all six gap groups are covered, all 20
worksheet rows map to current gaps, and there are zero missing or stale worksheet
groups. This keeps the worksheet valid for collection-day handoff, but it does
not close any evidence gate because the nine real files and measured metadata
are still absent. Controlled evidence, measured-field claims, field FWI, heavy
GPU work, field 3D/HPC, and neural-network training remain blocked.
Run `190` adds a sensitivity smoke for that coverage audit. The exact worksheet
passes, while four mutated worksheets fail as expected: missing profile file
row, missing session metadata group, stale unmapped row, and misclassified
time-zero role. This validates the worksheet coverage audit as a guard, but
does not close any real-data gate. Controlled evidence, measured-field claims,
field FWI, heavy GPU work, field 3D/HPC, and neural-network training remain
blocked.
Run `191` converts the worksheet into staged completion states. Seven scenarios
show that no partial completion path reaches field-FWI input readiness:
metadata-only, profile-repeat-only, reference-file-only, all-files-without-
metadata, and all-rows-without-gate-rerun all remain blocked. The only ready
row is a synthetic full completion in which all nine real files, all 11
metadata items, and checksum/intake/structural/provenance reruns all pass. This
validates the collection-day readiness path but does not promote the current
archive; real archive acceptance, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training remain blocked until real files and metadata pass every
gate.
Run `192` validates that staged-completion map from the consumer side: seven of
seven checks pass, no partial scenario is ready, the all-rows-without-gate-rerun
scenario remains blocked, and only the synthetic full-completion plus gate-pass
row reaches field-FWI input readiness. The current archive remains QC context
only; controlled evidence, real archive acceptance, field FWI, heavy GPU work,
field 3D/HPC, and neural-network training remain blocked.
Run `193` audits the concrete real-file intake slots in the operator worksheet.
The handoff template is clean: nine unique DZT slots are present, with three
controlled profile repeats, three time-zero references, and three amplitude
references. All slots have unique archive paths, copy/checksum templates,
required ledger fields, and field-FWI blocking status. This prepares the
checksum/intake handoff but does not supply real measured files; controlled
evidence, real archive acceptance, field FWI, heavy GPU work, field 3D/HPC, and
neural-network training remain blocked until the files are collected, hashed,
recorded, and all gates pass.
Run `194` stress-tests that slot audit. The exact template passes, while five
damaged-template cases fail as expected: missing profile slot, duplicate
archive path, wrong time-zero archive prefix, missing ledger field, and current
archive reuse allowed. This validates the slot map as a collection-day guard,
but controlled evidence, real archive acceptance, field FWI, heavy GPU work,
field 3D/HPC, and neural-network training remain blocked until real files and
gates pass.
Run `195` checks that the newer run `193` file-slot map is consistent with the
older run `168` checksum ledger template. Nine of nine consistency checks pass:
the artifacts share the same manifest IDs, roles, filenames, closure groups,
pending statuses, checksum command targets, and blocking flags. The existing
ledger should be reused with the slot map; controlled evidence, real archive
acceptance, field FWI, heavy GPU work, field 3D/HPC, and neural-network
training remain blocked until real files and gates pass.
Run `196` hardens the controlled archive intake gate with a DZT signature
guard. The guard requires the expected `.DZT` extension, a conservative
`65536` byte size floor, and the observed GSSI DZT binary header prefix
`ff07`. It accepts all four observed real current-archive GSSI files and
rejects all nine tiny synthetic placeholder `.DZT` files from earlier smoke
tests. The pending controlled archive still has zero passing file slots because
the nine required files are absent. Use this guard before checksum/intake
acceptance; controlled evidence, real archive acceptance, field FWI, heavy GPU
work, field 3D/HPC, and neural-network training remain blocked until real files
pass this guard and all downstream gates.
Run `197` stress-tests that signature guard with six controlled synthetic
scenarios. The valid binary case passes, and five invalid cases fail as
expected: tiny valid-prefix file, text placeholder, wrong binary prefix, wrong
extension, and missing file. There are zero unexpected outcomes, so the guard
is ready for controlled archive preflight use. Field FWI, GPU work, field
3D/HPC, and neural-network training remain blocked until real controlled files
pass the guard and all downstream gates.
Run `198` checks that guard in the archive preflight path. The older
shape-only preflight marks the run `174` synthetic placeholder archive as
checksum/intake ready because all 23 expected paths exist and are nonempty.
The integrated shape-plus-signature preflight rejects that same archive because
zero of nine expected DZT slots pass the signature guard. This prevents one
false-ready archive decision and confirms that controlled archive preflight
should require both shape and DZT signature checks. Controlled evidence, real
archive acceptance, field FWI, GPU work, field 3D/HPC, and neural-network
training remain blocked until real files pass this integrated preflight and all
downstream gates.
Run `199` validates that integrated preflight from a consumer perspective.
Seven of seven checks pass: both candidate archive rows are present, the
synthetic placeholder archive is correctly blocked despite passing the old
shape-only preflight, all nine synthetic DZT signature slots fail, the pending
archive remains blocked, and zero candidates are integrated-ready. Use run
`198` as the controlled archive gate; checksum/intake, controlled evidence,
real archive acceptance, field FWI, GPU work, field 3D/HPC, and neural-network
training remain blocked until a real archive passes it and all downstream
gates.
Run `200` refreshes the real-archive acceptance contract with that integrated
preflight. The contract now has 10 stages, explicitly adding DZT signature
preflight and integrated shape-plus-signature archive preflight after archive
layout. The DZT guard requires nine controlled DZT slots, a `65536` byte size
floor, and the observed GSSI header prefix `ff07`. The refreshed contract
prevents one false-ready placeholder archive decision, but zero archive
candidates are currently integrated-ready. Checksum/intake, controlled
evidence, real archive acceptance, field FWI, GPU work, field 3D/HPC, and
neural-network training remain blocked until a real archive passes the
integrated gate and all downstream checks.
Run `201` validates the refreshed contract from a consumer perspective. Eight
of eight checks pass: the 10-stage count matches, both new preflight stages are
present, the DZT signature stage requires nine slots, the integrated stage
blocks current candidates, one false-ready prevention is recorded, zero
candidates are integrated-ready, and field FWI remains blocked. Use run `200` as
the current field archive acceptance contract; checksum/intake, controlled
evidence, real archive acceptance, field FWI, GPU work, field 3D/HPC, and
neural-network training remain blocked until a real archive passes the
integrated gate.
Run `202` stress-tests that validator. The exact refreshed contract passes, and
six damaged contracts fail as expected: missing DZT signature stage, wrong DZT
slot count, integrated preflight incorrectly marked ready, missing integrated
archive stage, field FWI incorrectly marked ready, and stage-count mismatch.
There are zero unexpected outcomes. Keep run `200` as the current archive
acceptance contract and use runs `201-202` as guards; real archive acceptance,
field FWI, GPU work, field 3D/HPC, and neural-network training remain blocked
until real files pass the integrated gate.
Run `203` converts the current field-side gate into an execution packet by
joining the 10-stage integrated archive acceptance contract from run `200` with
the nine required DZT intake slots from run `193`. The packet is template-ready:
it lists three controlled profile repeats, three time-zero references, and
three amplitude references, and attaches the DZT size/header guard of at least
`65536` bytes and GSSI header prefix `ff07` to every slot. No real files are
present and zero stages are real-accepted, so this is not archive acceptance.
Use this packet for future real controlled archive intake; checksum/intake,
controlled evidence, real archive acceptance, field FWI, GPU work, field
3D/HPC, and neural-network training remain blocked until the nine real files
and required metadata pass the integrated gate.
Run `204` validates that execution packet from a consumer perspective. Nine of
nine checks pass: stage count, file-slot count, role counts, all DZT signature
requirements, matching size/header guard fields, pending file statuses,
template-ready status, zero real-accepted stages, and blocked downstream states.
Use run `203` as the execution packet and run `204` as its validator. This
validates the template only; real archive acceptance, checksum/intake, field
FWI, GPU work, field 3D/HPC, and neural-network training remain blocked until
real files and metadata pass the integrated gate.
Run `205` adds negative-control sensitivity for the execution packet validator.
The exact packet passes, while nine damaged packets fail as expected: missing
file slot, wrong role count, missing DZT signature requirement, wrong DZT
header guard, non-pending slot status, packet template not ready, premature
real-archive readiness, premature field-FWI readiness, and stage-count mismatch.
There are zero unexpected outcomes. Use runs `203`-`205` as the current
controlled archive execution-packet guard package; real archive acceptance,
checksum/intake, field FWI, GPU work, field 3D/HPC, and neural-network training
remain blocked until real files and metadata pass the integrated gate.
Run `206` converts the execution packet from run `203` into an explicit command
plan for future real archive intake. It creates 27 command templates: file
existence, DZT size/header signature guard, and SHA-256 checksum for each of the
nine required DZT slots. No commands are executed and no real files are present,
so this is not evidence acceptance. Use run `206` as the command-template
companion to the execution packet; real archive acceptance, checksum intake,
controlled evidence, field FWI, GPU work, field 3D/HPC, and neural-network
training remain blocked until the commands are executed on real files and all
integrated gates pass.
Run `207` validates that command-plan package from a consumer perspective.
Eleven of eleven checks pass with zero blocking failures: command count, file
slot count, required command groups, exactly three commands per slot, coverage
for file-existence/DZT-signature/checksum commands, `${ARCHIVE_ROOT}` template
scoping, DZT size/header guard content, command-plan readiness, and no premature
execution or downstream readiness. Use runs `206-207` as the current command
plan package; real archive acceptance, checksum intake, controlled evidence,
field FWI, GPU work, field 3D/HPC, and neural-network training remain blocked
until the commands are executed on real files and all integrated gates pass.
Run `208` stress-tests that command-plan validator. The exact command plan
passes, while nine damaged variants fail as expected: missing command row,
wrong command group, missing archive-root scope, wrong DZT header guard, wrong
DZT size guard, command-count mismatch, command plan not ready, commands marked
executed, and field FWI marked ready. There are zero unexpected outcomes. Use
runs `206-208` as the current command-plan guard package; real archive
acceptance, checksum intake, controlled evidence, field FWI, GPU work, field
3D/HPC, and neural-network training remain blocked until the commands are
executed on real files and all integrated gates pass.
Run `209` evaluates the command plan against an empty run-local archive root as
a fail-closed dry run. All 27 dry-run checks fail because the nine required DZT
files are absent: nine file-existence checks, nine DZT size/header checks, and
nine SHA-256 checksum checks. No shell command templates are executed and no
archive acceptance is inferred. Use run `209` as the fail-closed precheck
harness before real archive intake; real archive acceptance, checksum intake,
controlled evidence, field FWI, GPU work, field 3D/HPC, and neural-network
training remain blocked until the same checks pass on real measured files.
Run `210` validates that fail-closed dry run from a consumer perspective. Nine
of nine checks pass with zero blocking failures: dry-run command count,
expected command groups, nine required file slots, zero dry-run passes, all
failures being missing files, nine failures per command group, dry-run
evaluated and fail-closed state, no shell command template execution, and
blocked real-archive/downstream states. Use runs `209-210` as the current
fail-closed dry-run guard before real archive intake; real archive acceptance,
checksum intake, controlled evidence, field FWI, GPU work, field 3D/HPC, and
neural-network training remain blocked until real files pass.
Run `211` stress-tests that validator. The exact fail-closed dry run passes,
while ten damaged variants fail as expected: missing dry-run row, wrong command
group, unexpected dry-run pass, non-missing-file failure reason, missing-file
count drift, fail-closed flag false, row-level shell execution true, summary
shell execution true, real archive marked ready, and field FWI marked ready.
There are zero unexpected outcomes. Use runs `209-211` as the guarded
fail-closed dry-run package before real archive intake; real archive
acceptance, checksum intake, controlled evidence, field FWI, GPU work, field
3D/HPC, and neural-network training remain blocked until real files pass.
Run `212` adds the positive-control side of the command-plan evaluator. It
creates nine run-local synthetic DZT files, each `65536` bytes with `ff07`
header prefix, then evaluates the same 27 command-plan checks without executing
shell command templates. All 27 checks pass: nine file-existence checks, nine
DZT size/header checks, and nine SHA-256 checks. These are synthetic fixtures,
not real measured files, so real archive acceptance, checksum intake,
controlled evidence, field FWI, GPU work, field 3D/HPC, and neural-network
training remain blocked until real measured files pass the same checks.
Run `213` validates that positive-control result from a consumer perspective.
Eight of eight checks pass with zero blocking failures: command count, all 27
commands passing, nine synthetic files, nine passes in each command group,
positive-control ready state, synthetic files not being real data, no shell
command execution, and blocked real-archive/downstream states. Sensitivity
remains required before treating the positive-control harness as fully guarded.
Run `214` stress-tests that validator. The exact positive-control summary
passes, while thirteen damaged variants fail as expected: command-count drift,
command failure, synthetic-file count drift, file/signature/checksum group pass
count drift, positive-control not ready, synthetic files marked real, real
files present, shell command execution, real archive marked ready, checksum
intake marked ready, and field FWI marked ready. There are zero unexpected
outcomes. Use runs `212-214` as the guarded synthetic positive-control harness
for the command-plan evaluator. Together with runs `209-211`, the evaluator has
both fail-closed and expected-pass coverage. Real archive acceptance, checksum
intake, controlled evidence, field FWI, GPU work, field 3D/HPC, and
neural-network training remain blocked until real measured files pass.
Run `215` combines those two sides into a command-plan evaluator contract. It
records two ready guards: an empty archive fails closed with 0 passes and 27
failures, while a synthetic valid archive passes all 27 checks with 0 failures.
The evaluator contract is ready for future real archive intake, but this is not
real archive acceptance. Real archive acceptance, checksum intake, controlled
evidence, field FWI, GPU work, field 3D/HPC, and neural-network training remain
blocked until real measured files pass the same checks.
Run `216` validates that evaluator contract from a consumer perspective. Six of
six checks pass with zero blocking failures: guard counts, fail-closed guard
shape, positive-control guard shape, both guard-ready flags, evaluator-contract
ready state, and blocked real-archive/downstream states. Sensitivity remains
required before treating the evaluator contract as fully guarded.
Run `217` stress-tests that validator. The exact evaluator contract passes,
while twelve damaged variants fail as expected: missing guard row, guard-count
drift, fail-closed unexpected pass, fail-closed not ready, positive-control
failure, positive-control not ready, fail-closed flag false, positive flag
false, contract not ready, real archive ready, checksum intake ready, and field
FWI ready. There are zero unexpected outcomes. Use runs `215-217` as the
guarded field command-plan evaluator contract. Real archive acceptance,
checksum intake, controlled evidence, field FWI, GPU work, field 3D/HPC, and
neural-network training remain blocked until real measured files pass.
Run `218` combines that guarded evaluator with the run `163` provenance-closure
checklist into a real-intake boundary. It finds nine boundary items, two ready
items, and seven real-acceptance blockers. The collection-day checklist and
command-plan evaluator are ready, but the archive still needs nine real DZT
files, real session/provenance values, future-date cleanup, checksum intake on
real files, controlled evidence acceptance, and blocked field-FWI/3D/GPU
states. Use run `218` as the current real-intake boundary before any archive
acceptance claim.
Run `219` validates that real-intake boundary from a consumer perspective.
Eight of eight checks pass with zero blocking failures, confirming the
nine-item boundary table, collection checklist readiness, nine real-file
requirement with three profile, three time-zero, and three amplitude-reference
files, real provenance blockers, evaluator readiness, synthetic positive-control
limits, checksum/evidence blockers, and blocked downstream field states.
Sensitivity remains required before treating the boundary as fully guarded.
Run `220` stress-tests that validator. The exact real-intake boundary passes,
while 18 damaged variants fail as expected for boundary-count drift, collection
readiness drift, real-file count or role drift, real-file row promotion,
provenance placeholder drift, future-date drift, evaluator readiness drift,
synthetic guardrail removal, checksum/evidence readiness, real archive intake
readiness, provenance acceptance readiness, field-FWI readiness, and
field-3D/HPC readiness. There are zero unexpected outcomes. Use runs `218-220`
as the guarded field real-intake boundary package.
Run `221` turns that boundary into a single operator-facing archive manifest:
nine real DZT file slots across three archive directories, with 27 planned
intake checks. The required files remain three controlled profile repeats,
three time-zero references, and three amplitude references. The manifest is
ready for operator collection and archive staging, but it does not contain real
files and does not execute the checks. Real archive acceptance, checksum intake,
controlled evidence, field FWI, GPU work, field 3D/HPC, and neural-network
training remain blocked until real measured files are placed at the manifest
paths and all checks pass.
Run `222` validates that manifest from a consumer perspective. Eight of eight
checks pass with zero blocking failures: nine file slots, three files per role,
three archive directories, 27 planned checks, fixed DZT guard values, operator
collection readiness separated from archive acceptance, no real files or
executed checks, and blocked checksum/evidence/FWI/3D states.
Run `223` stress-tests the manifest validator. The exact manifest passes, while
24 damaged variants fail as expected for file-slot drift, role-count drift,
directory drift, check-group drift, DZT guard drift, readiness flag drift,
command-execution drift, real archive acceptance promotion, checksum/evidence
promotion, field-FWI promotion, and field-3D/HPC promotion. There are zero
unexpected outcomes. Use runs `221-223` as the guarded field
operator-manifest package for collection and archive staging.
Run `224` converts that guarded manifest into a collection-day worksheet. It
preserves nine required real DZT file slots, three archive directories, three
file-role groups, the `65536` byte DZT minimum-size guard, the `ff07` DZT header
prefix guard, and 27 planned checks, while adding four operator signoff fields
per row: initials, local collection time, staged-file SHA-256, and notes. Use
run `224` as the printable worksheet companion to the operator manifest. Real
archive acceptance, checksum intake, controlled evidence, field FWI, GPU work,
field 3D/HPC, and neural-network training remain blocked until real files are
staged and checks pass.
Run `225` validates that worksheet from a consumer perspective. Eight of eight
checks pass with zero blocking failures: worksheet row count, file-role counts,
six-stage collection sequence, blank signoff fields on pending rows, archive
and DZT guards, worksheet readiness without archive acceptance, no real files
or executed commands, and blocked downstream field states. Sensitivity remains
required before treating the worksheet validator as fully guarded.
Run `226` stress-tests that worksheet validator. The exact worksheet passes,
while 27 damaged variants fail as expected for row-count drift, missing rows,
role-count drift, stage drift, premature signoff or completion, archive
directory and DZT guard drift, planned-check drift, readiness drift, real-file
or command-execution promotion, archive-acceptance promotion, checksum/evidence
promotion, field-FWI promotion, and field-3D/HPC promotion. A role-directory
guard gap was found and fixed during this run; the corrected sensitivity result
has zero unexpected outcomes. Use runs `224-226` as the guarded field operator
worksheet package for collection-day execution.
Run `227` converts the blank worksheet signoff fields into a completed-
worksheet intake contract. It defines 36 signoff cells across nine file rows:
27 required cells for operator initials, local collection time, and staged
SHA-256, plus nine optional notes cells. The contract is ready for future
completed worksheet intake, but the current worksheet remains blank and pending
real files. Real files, real signoff values, archive acceptance, checksum
intake, controlled evidence, field FWI, field 3D/HPC, and GPU work remain
blocked.
Run `228` validates that signoff contract from a consumer perspective. Six of
six checks pass with zero blocking failures, confirming source readiness, 36
signoff cells, 27 required cells, nine optional notes cells, complete worksheet
row and role coverage, expected validation rules, blank current values, and
blocked real-file/archive/checksum/evidence/FWI/3D states. Sensitivity remains
required before treating the signoff contract as fully guarded.
Run `229` stress-tests that validator. The exact signoff contract passes,
while 22 damaged variants fail as expected for source-readiness drift,
cell-count drift, missing rows, required-flag drift, field/rule drift,
worksheet row and file-role drift, prefilled-value drift, intake-readiness
drift, and false real-file/signoff/archive/checksum/evidence/FWI/3D promotion.
There are zero unexpected outcomes. Use runs `227-229` as the guarded
completed-worksheet signoff package for future real archive intake.
Run `230` adds a positive synthetic completed-worksheet intake smoke. The nine
worksheet rows are filled with synthetic initials, local timestamps, unique
64-character SHA-256 strings, and optional notes. All 27 required signoff
checks and nine optional signoff checks pass, while real measured files, real
completed signoff values, archive acceptance, checksum intake, controlled
evidence, field FWI, and field 3D/HPC remain blocked. Validator and sensitivity
coverage remain required before treating this synthetic completed-worksheet
intake path as fully guarded.
Run `231` validates that synthetic completed-worksheet smoke from a consumer
perspective. Five of five checks pass with zero blocking failures, confirming
source readiness, nine completed rows across the three required file roles, 36
passing signoff checks, nine unique synthetic SHA-256 values, and a clear
synthetic-vs-real boundary with archive/checksum/evidence/FWI/3D states still
blocked. Sensitivity remains required before treating this intake path as fully
guarded.
Run `232` stress-tests that validator. The exact synthetic completed-worksheet
smoke passes, while 35 damaged variants fail as expected for source-readiness
drift, row-coverage drift, signoff-check coverage drift, signoff-field drift,
synthetic value drift, SHA-256 drift, synthetic/real boundary drift, and false
archive/checksum/evidence/FWI/3D promotion. There are zero unexpected outcomes.
Use runs `230-232` as the guarded synthetic completed-worksheet intake package.
Real measured files and real operator signoff values remain required before
archive acceptance can be tested.
Run `233` refreshes the real archive-acceptance boundary after that synthetic
worksheet package. Two items are ready, one item is synthetic-only ready, and
five real-acceptance blockers remain: nine real measured DZT files, real
operator signoff values, measured provenance values, checksum intake on staged
real files, and controlled-evidence acceptance after rerunning the real-data
gates. Field FWI, field 3D/HPC, GPU work, and field evidence promotion remain
blocked.
Run `234` validates that refreshed boundary from a consumer perspective. Five
of five checks pass with zero blocking failures, confirming the expected nine
items, two ready items, one synthetic-only item, five real blockers, synthetic
worksheet support that cannot count as real archive acceptance, and blocked
archive/checksum/evidence/FWI/3D states. Sensitivity remains required before
treating this boundary as fully guarded.
Run `235` stress-tests that validator. The exact run `233` boundary passes,
while 20 damaged variants fail as expected for boundary-count drift, item-name
drift, synthetic-intake promotion, missing real blockers, missing next-action
fields, and false archive/checksum/evidence/FWI/3D readiness. There are zero
unexpected outcomes. Use runs `233-235` as the guarded current real archive-
acceptance boundary. Real measured files, real operator signoff values,
measured provenance values, checksum intake, and controlled evidence acceptance
remain required before any field evidence promotion or field FWI.
Run `236` joins the guarded operator manifest, signoff contract, provenance
closure actions, and real-acceptance boundary into one real-return intake
contract. It defines nine DZT file slots, 27 planned file checks, 27 required
signoff cells, six provenance closure action groups, and 10 return gates. The
contract is ready as an intake shape, but real measured files, real signoff
values, measured provenance values, checksum intake, and controlled evidence
acceptance remain missing. Real archive acceptance, field FWI, field 3D/HPC,
GPU work, and field evidence promotion remain blocked.
Run `237` validates that real-return intake contract from a consumer
perspective. Five of five checks pass with zero blocking failures, confirming
the nine file rows, 27 checks, 27 required signoff cells, six provenance
closure groups, 10 gates, five real-acceptance blockers, and blocked real
archive/downstream states. Sensitivity remains required before treating this
contract as fully guarded.
Run `238` stress-tests that validator. The exact run `236` contract passes,
while 31 damaged variants fail as expected for count drift, missing
file/provenance/gate rows, file role drift, signoff/check drift, DZT guard
drift, premature file/provenance readiness, missing real blockers, and false
archive/downstream readiness. There are zero unexpected outcomes. Use runs
`236-238` as the guarded real-return intake contract. Real measured files and
measured signoff/provenance values remain required before archive acceptance
can be tested.
Run `239` turns that guarded contract into an empty real-return archive
skeleton. It creates the expected directory structure for profiles,
time-zero references, and amplitude references, plus blank expected-file,
signoff, and provenance CSV templates. It creates zero placeholder DZT files.
The skeleton is ready as a staging aid only; real measured files, measured
signoff values, measured provenance values, checksum intake, controlled
evidence, archive acceptance, field FWI, and field 3D/HPC remain blocked.
Run `240` validates that empty skeleton pack from a consumer perspective. Five
of five checks pass with zero blocking failures, confirming nine expected file
slots, three template directories, nine blank signoff rows, six provenance
template rows, zero placeholder files, expected empty directories, and blocked
real archive/downstream states. Sensitivity remains required before treating
the skeleton pack as fully guarded.
Run `241` stress-tests that validator. The exact run `239` skeleton passes,
while 25 damaged variants fail as expected for count drift, missing expected-
file rows, directory drift, placeholder-file creation, prefilled signoff/
provenance templates, and false archive/downstream readiness. There are zero
unexpected outcomes. Use runs `239-241` as the guarded empty real-return
archive skeleton pack.
Run `242` provides a positive synthetic populated-archive smoke for that
skeleton. It creates nine deterministic synthetic DZT-like files, fills 27
synthetic signoff cells, fills six synthetic provenance rows, and passes all 45
file/header/size/SHA checks. The smoke proves the archive intake mechanics can
pass when correctly shaped files are present, but it remains synthetic only:
real measured files, real signoff values, real provenance values, real checksum
intake, controlled evidence, field FWI, field 3D/HPC, and GPU escalation remain
blocked.
Run `243` validates that populated synthetic archive smoke from saved artifacts.
Six of six checks pass with zero blocking failures: synthetic files are
complete and not promoted as real, signoff rows match staged SHA-256 values,
provenance rows remain synthetic, all 45 archive checks pass, summary counts
are consistent, and real archive/downstream states remain blocked. Use runs
`242-243` as the guarded positive-control archive-intake smoke.
Run `244` stress-tests that validator. The exact run `242` smoke passes, while
36 damaged variants fail as expected for file-table drift, signoff drift,
provenance drift, archive-check drift, summary-count drift, and false
real/downstream readiness. There are zero unexpected outcomes. Use runs
`242-244` as the guarded positive-control archive-intake smoke; real measured
files and real metadata remain required before archive acceptance or field
evidence promotion.
Run `245` refreshes the real-return archive acceptance boundary after that
guarded positive control. Two support items are ready: the empty real-return
archive skeleton and the populated synthetic archive smoke. Six acceptance
blockers remain: real measured DZT files, real operator signoff values, real
provenance values, real checksum intake, controlled-evidence acceptance, and
field-FWI/3D/HPC/GPU escalation. Do not promote field evidence or launch field
FWI/3D/HPC/GPU routes until real files pass the guarded intake path.
Run `246` validates that refreshed boundary from saved artifacts. Five of five
checks pass with zero blocking failures, confirming boundary counts, ready
synthetic support, real acceptance blockers, recorded next actions, and blocked
real archive/downstream states. Sensitivity remains required before treating
the boundary as fully guarded.
Run `247` stress-tests that validator. The exact run `245` boundary passes,
while 21 damaged variants fail as expected for boundary-row drift, support and
blocker count drift, missing real-data requirements, unready support rows,
false real-file readiness, missing blocker flags, missing next actions, and
false real/downstream readiness. There are zero unexpected outcomes. Use runs
`245-247` as the guarded real-return acceptance boundary.
Run `248` converts that guarded boundary into a non-executed real-return
command plan. The plan has six commands: three current guard validations that
can run now, and three future real-archive commands that require a real archive
root and real measured files. No commands are executed in this run. Use it as
the real-return command checklist; real archive acceptance, field FWI, field
3D/HPC, and GPU escalation remain blocked.
Run `249` validates that command plan from saved artifacts. Six of six checks
pass with zero blocking failures, confirming source readiness, command
partition counts, executable current guard commands, blocked future real-
archive gates, summary/table count consistency, and blocked real archive/
downstream states. Sensitivity remains required before treating the command
checklist as fully guarded.
Run `250` stress-tests that validator. The exact run `248` command plan
passes, while 26 damaged variants fail as expected for command-row drift,
command-order drift, command-group drift, current guard executability drift,
future real-archive gate blocking drift, summary-count drift, command-execution
promotion, real-file promotion, real-archive acceptance promotion, and false
field FWI/3D/GPU readiness. There are zero unexpected outcomes. Use runs
`248-250` as the guarded real-return archive command checklist.
Run `251` executes only the three current guard-validation commands from that
checklist. All three pass: the real-return boundary focused tests, the empty
skeleton validator, and the synthetic positive-control validator. The three
future real-archive commands remain unexecuted because real measured files are
still missing. Use run `251` as the current-guard execution smoke; real archive
acceptance, field evidence promotion, field FWI, field 3D/HPC, and GPU
escalation remain blocked.
Run `252` validates the run `251` current-guard execution smoke from saved
artifacts. Six of six checks pass with zero blocking failures, confirming that
the saved execution rows match the runnable current-guard subset of the run
`248` command plan, all three commands passed, summary counts match the
execution table, and future real-archive plus downstream states remain blocked.
Sensitivity remains required before treating the execution smoke as fully
guarded.
Run `253` stress-tests that execution-smoke validator. The exact run `251`
smoke passes, while 27 damaged variants fail as expected for execution-row
drift, command-template drift, real-archive requirement drift, command failure,
elapsed-time corruption, source command-plan mismatch, summary-count drift,
future real-archive execution promotion, real-file promotion, archive-acceptance
promotion, and false field FWI/3D/GPU readiness. There are zero unexpected
outcomes. Use runs `251-253` as the guarded current-guard execution smoke for
the real-return archive checklist.
Run `254` synthesizes the current post-execution real-return boundary. Two
support items are ready: the guarded real-return command checklist and the
guarded current-guard execution smoke. Five real-data blockers remain: future
real-archive command execution, real measured files, real archive acceptance,
controlled field evidence promotion, and field FWI/3D/HPC/GPU escalation. Use
run `254` as the current field real-return boundary; do not execute future
real-archive commands or promote field evidence until real measured files are
staged.
Run `255` validates that post-execution boundary from saved artifacts. Six of
six checks pass with zero blocking failures, confirming the two-support/five-
blocker row partition, guarded support rows, real-data blocker rows, summary/
table count consistency, and blocked real archive, controlled evidence, field
FWI, field 3D/HPC, and GPU states. Sensitivity remains required before treating
the boundary as fully guarded.
Run `256` stress-tests that post-execution boundary validator. The exact run
`254` boundary passes, while 23 damaged variants fail as expected for boundary-
row drift, support/blocker status drift, missing real-data blocker flags,
summary-count drift, unguarded command/execution support, future real-archive
execution promotion, real-file promotion, archive-acceptance promotion,
controlled-evidence promotion, and false field FWI/3D/GPU readiness. There are
zero unexpected outcomes. Use runs `254-256` as the guarded current field real-
return post-execution boundary.
Run `257` combines the run `163` controlled-collection provenance closure with
the guarded real-return boundary from runs `254-256`. The resulting handoff
table has 13 rows: six collection actions, two guarded return supports, and
five post-return real-data blockers. The six collection actions require nine
real files total: three controlled profile repeats, three time-zero references,
and three amplitude-reference files. The readiness pack itself is coherent and
ready as a checklist, but the current dry-run archive still has no real files,
does not pass provenance acceptance, is not accepted field evidence, and does
not justify field FWI, field 3D/HPC, heavy GPU work, or neural-network
training.
Run `258` validates the run `257` collection-return readiness pack from saved
artifacts. Seven of seven checks pass with zero blocking failures, confirming
the six collection actions, nine required real files, two guarded return
supports, five post-return blockers, guard summary readiness, and false real-
file/provenance/archive/evidence/FWI/3D/GPU states. Sensitivity remains
required before treating the pack validator as guarded.
Run `259` stress-tests that validator. The exact run `257` pack passes, while
47 damaged variants fail as expected for collection-row drift, support/blocker
drift, real-file count drift, guard-readiness drift, premature real-file or
provenance acceptance, real-archive acceptance, controlled-field evidence
promotion, field-FWI promotion, field-3D/HPC promotion, and GPU promotion.
There are zero unexpected outcomes. Use runs `257-259` as the guarded
controlled field collection-return readiness pack.
Run `260` converts that readiness pack into a concrete real-return staging
contract. It defines nine measured DZT file slots, eleven global metadata
fields, twenty-one per-file metadata cells, nine checksum requirements, and
seven ordered acceptance gates. The contract is ready as a future intake shape,
but real files, real metadata, checksums, structural validation, provenance
validation, real archive acceptance, controlled field evidence, field FWI,
field 3D/HPC, and GPU escalation all remain blocked.
Run `261` validates the run `260` staging contract from saved artifacts. Seven
of seven checks pass with zero failures, confirming the nine-file slot
partition, eleven global metadata fields, twenty-one file metadata cells, nine
checksum requirements, seven ordered gates, valid figure output, script
snapshots, and false real-file/provenance/archive/evidence/FWI/3D/GPU states.
Sensitivity remains required before treating the staging-contract validator as
guarded.
Run `262` stress-tests that validator. The exact run `260` contract passes,
while 36 damaged variants fail as expected for file-slot drift, metadata-slot
drift, gate-order drift, summary-count drift, premature real-data or downstream
promotion, figure-validation drift, and script-snapshot drift. There are zero
unexpected outcomes. Use runs `260-262` as the guarded controlled field
real-return staging contract.
Run `263` materializes that contract as an empty real-return intake layout. It
creates six required directories, a nine-slot required-file manifest, eleven
global metadata template rows, twenty-one per-file metadata rows, nine checksum
template rows, and a README. It creates zero placeholder DZT files. Real files,
measured metadata, checksums, provenance acceptance, real archive acceptance,
controlled field evidence, field FWI, field 3D/HPC, and GPU escalation remain
blocked.
Run `264` validates the run `263` empty intake layout from saved artifacts.
Nine of nine checks pass with zero failures, confirming the directory and
template layout, empty required-file manifest, absence of DZT placeholders,
empty metadata templates, empty checksum template, blocked archive/evidence/
downstream states, valid figure output, and script snapshots. Sensitivity
remains required before treating the empty-layout validator as guarded.
Run `265` stress-tests that validator. The exact run `263` empty layout passes,
while 40 damaged variants fail as expected for required-file drift, placeholder
permission, false file presence, metadata prefill, checksum prefill, summary
drift, downstream promotion, figure-validation drift, and script-snapshot
drift. There are zero unexpected outcomes. Use runs `263-265` as the guarded
empty real-return intake layout.
Run `266` scans the guarded real-return inbox after that empty-layout guard.
The inbox still contains only README and template files: zero of nine required
DZT files are present, zero of 32 metadata values are filled, zero of nine
checksums are present, and there are no unexpected files. Provenance
acceptance, real archive acceptance, controlled field evidence, field FWI,
field 3D/HPC, and GPU escalation remain blocked until real measured files,
metadata, and checksums are staged.
Run `267` validates that saved inbox scan. Eight of eight checks pass,
confirming the scan policy/source guard, required-file counts, metadata counts,
checksum counts, absence of unexpected files, blocked acceptance/downstream
states, valid figure output, and script snapshots. Sensitivity remains required
before treating the scan validator as guarded.
Run `268` stress-tests that validator. The exact run `266` inbox scan passes,
while 34 damaged variants fail as expected for required-file drift, metadata
drift, checksum drift, unexpected-file rows, summary-count drift, premature
acceptance/downstream promotion, figure-validation drift, and script-snapshot
drift. There are zero unexpected outcomes. Use runs `266-268` as the guarded
current field intake status checkpoint: the real-return inbox has no required
DZT files, no measured metadata values, no checksums, and no unexpected files.
Run `269` converts that guarded empty-inbox status into a collection-day fill
packet. It writes exact worklists for nine measured DZT files, 32 measured
metadata values, nine checksums, and seven acceptance gates. The fill packet is
ready as an operational worklist, but the current archive still contains zero
required real files, zero measured metadata values, and zero checksums. Do not
promote provenance acceptance, real archive acceptance, controlled field
evidence, field FWI, field 3D/HPC, or GPU work until the worklist is completed
with real measured files and values.
Run `270` validates that fill packet from saved artifacts. Eight of eight
checks pass, confirming worklist row counts, required real DZT files,
placeholder prohibition, required measured metadata values, required checksums,
blocked acceptance gates, nonblank figure output, and script snapshots. The
packet is guarded as a collection-day worklist only; provenance acceptance,
real archive acceptance, controlled field evidence, field FWI, field 3D/HPC,
and GPU work remain blocked.
Run `271` stress-tests that fill-packet validator. The exact run `269`
worklist passes, while 13 damaged variants fail as expected for file-row drift,
false file presence, placeholder permission, metadata-row drift, false metadata
fill, checksum-row drift, false checksum fill, acceptance-gate promotion,
downstream summary promotion, blank figure output, and missing script
snapshots. There are zero unexpected outcomes. Use runs `269-271` as the
guarded collection-day fill-packet block; the packet still requires nine real
DZT files, 32 measured metadata values, and nine checksums before provenance
acceptance, real archive acceptance, controlled evidence, field FWI, field
3D/HPC, or GPU work can proceed.
Run `272` converts that guarded fill-packet block into a non-executed
collection-day execution plan. The plan has eight phases: session metadata
capture, three controlled profile repeats, three time-zero references, three
amplitude references, return-inbox copy, checksum recording, per-file metadata
fill, and validator reruns. It defines the work needed for nine real DZT
files, 32 measured metadata values, nine checksums, and seven acceptance gates.
No command executes now, no real files are present, and provenance acceptance,
real archive acceptance, controlled evidence, field FWI, field 3D/HPC, and GPU
work remain blocked.
Run `273` validates that execution command plan from saved artifacts. Seven of
seven checks pass, confirming source counts, exact phase order, non-executed
commands, comment-only command script, blocked field downstream states,
nonblank figure output, and script snapshots. The collection-day execution
plan is guarded but remains non-evidence until real DZT files, measured
metadata, and checksums are staged and accepted.
Run `274` stress-tests that command-plan validator. The exact run `272` plan
passes, while 15 damaged variants fail as expected for source-count drift,
phase drift, accidental command execution, command-script drift, downstream
promotion, figure-validation drift, and script-snapshot drift. There are zero
unexpected outcomes. Use runs `272-274` as the guarded non-executed
collection-day command-plan block; real files, measured metadata, and
checksums remain required before any field evidence, field FWI, 3D/HPC, or GPU
escalation.
Run `275` maps the collection-day phases to acceptance gates. The eight-phase
dependency chain covers 9 required real DZT files, 11 global metadata values,
21 file metadata values, 9 checksums, and 7 currently blocked acceptance gates.
The audit shows that metadata capture, real file collection/copy, checksum
recording, file metadata fill, and validator reruns must all complete before
field evidence, field FWI, 3D/HPC, or GPU work can be considered.
Run `276` validates that dependency map from saved artifacts. Seven of seven
checks pass, confirming the source counts, exact phase order, dependency
counts, blocked phase/gate state, blocked downstream field states, figure
output, and script snapshots. Use run `276` as the validator for the field
phase-gate dependency map.
Run `277` stress-tests that validator. The exact run `275` dependency map
passes, while 18 damaged variants fail as expected for source count drift,
phase-order drift, required file/metadata/checksum/gate-count drift, phase
execution drift, downstream block-flag drift, false provenance/evidence/FWI/GPU
promotion, figure-validation drift, and missing script snapshots. There are
zero unexpected outcomes. Use runs `275-277` as the guarded field phase-gate
dependency block; real files, measured metadata values, and checksums remain
required before provenance acceptance, real archive acceptance, controlled
field evidence, field FWI, 3D/HPC, or GPU work can proceed.
Run `278` converts that guarded phase-gate block into a three-stage critical
path: field-day capture/acquisition, post-return archive completion, and
validation/acceptance. The packet has 57 total requirement rows: 50 measured
requirements plus seven acceptance gates. The measured requirements are nine
real DZT files, 32 metadata values, and nine checksums. Zero measured
requirements and zero gates are complete in the current archive, so provenance
acceptance, real archive acceptance, controlled field evidence, field FWI,
field 3D/HPC, and GPU work remain blocked.
Run `279` validates the run `278` critical-path audit from saved artifacts.
Eight of eight checks pass, confirming the three-stage split, 57 requirement
rows, 50 measured requirements, zero-complete current archive state, guarded
source readiness, blocked downstream field states, figure output, and script
snapshots. Use runs `278-279` as the guarded field critical-path block.
Run `280` stress-tests the run `279` critical-path validator. The exact run
`278` audit passes, while eight damaged variants fail as expected for
requirement-count drift, measured-requirement count drift, stage-split drift,
false measured completion, source-guard loss, downstream promotion,
figure-validation drift, and script-snapshot drift. There are zero unexpected
outcomes. Use runs `278-280` as the guarded field critical-path block; real
files, measured metadata values, and checksums remain required before
provenance acceptance, field evidence, field FWI, 3D/HPC, or GPU work can
proceed.
Run `281` rescans the current return inbox against the guarded critical-path
block. The inbox still contains zero of nine required real DZT files, zero of
32 measured metadata values, zero of nine checksums, and zero unexpected files.
The guarded critical path therefore remains at zero of 50 measured
requirements and zero of seven acceptance gates complete. Provenance
acceptance, real archive acceptance, controlled field evidence, field FWI,
3D/HPC, and GPU work remain blocked until real measured files, metadata, and
checksums are staged.
Run `282` validates that saved current rescan from artifacts. Seven of seven
checks pass, confirming the nine file slots, 32 metadata values, nine checksum
rows, zero measured completions, zero acceptance gates ready, no unexpected
files or placeholders, blocked downstream field states, figure output, and
script snapshots. Use runs `281-282` as the guarded current field inbox state.
Run `283` stress-tests the run `282` current-rescan validator. The exact run
`281` rescan passes, while eight damaged variants fail as expected for
file-count drift, metadata-count drift, false file presence, checksum-count
drift, unexpected files, downstream promotion, figure-validation drift, and
script-snapshot drift. There are zero unexpected outcomes. Use runs `281-283`
as the guarded current field inbox state.
Run `284` creates a private synthetic positive-control return inbox inside its
own output folder. It stages nine non-empty DZT-shaped files, 32 metadata
values, and nine matching checksums, and confirms that the current return-inbox
mechanics can count a complete packet. The run is synthetic only and does not
modify the real return inbox; real provenance acceptance, real archive
acceptance, controlled field evidence, field FWI, 3D/HPC, and GPU work remain
blocked until actual measured files and values arrive.
Run `285` validates the saved run `284` positive-control smoke from artifacts.
Six of six checks pass, confirming the synthetic packet counts, checksum
matches, positive-control mechanics pass, synthetic-only boundary, blocked
downstream field states, figure output, and script snapshots. Sensitivity
hardening remains required before treating the positive-control block as
guarded.
Run `286` stress-tests the run `285` validator. The exact run `284` positive
control passes, while 12 damaged variants fail as expected for file-count
drift, metadata-count drift, checksum-count drift, checksum-match drift,
unexpected files, zero-byte placeholders, extension failures, mechanics failure,
synthetic-boundary loss, downstream promotion, figure-validation drift, and
script-snapshot drift. There are zero unexpected outcomes. Use runs `284-286`
as the guarded positive-control mechanics block; the real field archive remains
blocked until actual measured DZT files, metadata, and checksums arrive.
Run `287` synthesizes the field claim boundary after that positive-control
block. Three claims are guarded: the collection-day critical path is defined,
the current real return inbox is still empty, and the private synthetic
positive-control scan works mechanically. Four claims remain blocked: real
packet completion, provenance/archive acceptance, controlled field evidence or
field FWI, and field 3D/HPC or GPU escalation. The current real archive still
has zero of 50 measured requirements complete, zero of nine real DZT files,
zero of 32 metadata values, zero of nine checksums, and zero of seven
acceptance gates ready.
Run `288` validates the saved run `287` field claim boundary from artifacts.
Seven of seven checks pass, confirming claim counts, current real-packet
counts, the synthetic-only positive-control boundary, blocked broader claims,
downstream guardrails, figure output, and script snapshots. Sensitivity
hardening remains required before treating the post-positive-control field
claim-boundary validator as guarded.
Run `289` stress-tests that validator. The exact run `287` claim boundary
passes, while 15 damaged variants fail as expected for claim-count drift,
current-packet count drift, false measured completion, false real-file,
metadata, checksum, or acceptance-gate completion, synthetic-boundary loss,
blocked-claim false promotion, downstream promotion, figure-validation drift,
and script-snapshot drift. There are zero unexpected outcomes. Use runs
`287-289` as the guarded post-positive-control field claim-boundary block.
Run `290` audits whether the guarded positive-control mechanics make the real
field return executable. Four support gates are ready: the guarded critical
path, the current-rescan mechanics, the synthetic positive control, and the
claim-boundary sensitivity block. Nine gates remain blocked: three real-file
groups, two metadata groups, checksums, structural/provenance acceptance,
field evidence/FWI, and field 3D/HPC or GPU escalation. The archive still has
zero of 50 measured requirements complete: zero of nine real DZT files, zero
of 32 metadata values, zero of nine checksums, and zero of seven acceptance
gates ready. Use run `290` as the post-positive-control real-return execution
gate.
Run `291` validates the saved run `290` real-return execution readiness audit
from artifacts. Eight of eight checks pass, confirming gate counts, blocker
category counts, measured requirement counts, the synthetic-only positive
control boundary, blocked field states, blocker reasons, figure output, and
script snapshots. Use run `291` as the validator for the post-positive-control
real-return execution gate.
Run `292` stress-tests that validator. The exact run `290` audit passes, while
16 damaged variants fail as expected for gate-count drift, measured-requirement
count drift, false real-file/metadata/checksum/acceptance completion,
synthetic-boundary loss, false real-return/provenance/GPU promotion, missing
blocker reasons, figure-validation drift, and script-snapshot drift. There are
zero unexpected outcomes. Use runs `290-292` as the guarded
post-positive-control field real-return execution gate.
Run `293` converts that gate into a current real-return packet contract: 57
packet items, 50 measured requirements, nine real DZT files, 32 metadata
values, nine checksums, seven acceptance gates, and 189 acceptance checks. The
contract is ready, but the current real archive still has zero measured packet
items complete.
Run `294` validates the saved run `293` field return packet contract from
artifacts. Seven of seven checks pass, confirming packet counts,
requirement-type counts, stage split, current empty archive state, blocked
field states, figure output, and script snapshots.
Run `295` stress-tests that validator. The exact run `293` packet contract
passes, while 13 damaged variants fail as expected for packet-count drift, row
loss, requirement-type drift, stage drift, false measured completion, false
field-state promotion, synthetic-boundary loss, GPU-priority drift,
figure-validation drift, and script-snapshot drift. Use runs `293-295` as the
guarded field real-return packet contract.
Run `296` converts that guarded contract into an ordered non-executed staging
command plan with eight phases: directory creation, three controlled profile
repeat files, three time-zero reference files, three amplitude-reference files,
32 measured metadata values, nine checksums, 189 packet acceptance checks, and
seven acceptance-gate result files. All commands are intentionally commented
out. Use run `296` as the handoff staging plan, not as evidence that measured
field files have been staged.
Run `297` validates the saved run `296` command plan from artifacts. Nine of
nine checks pass, confirming plan counts, phase order and dependencies,
expected output counts, non-executed command semantics, source-contract
linkage, current empty-archive state, blocked field states, figure output, and
script snapshots.
Run `298` stress-tests that validator. The exact run `296` plan passes, while
15 damaged variants fail as expected for plan-count drift, phase-order drift,
dependency drift, output-count drift, command execution promotion, uncommented
command text, source-link drift, false measured completion, false field-state
promotion, GPU-priority drift, figure-validation drift, and script-snapshot
drift. Use runs `296-298` as the guarded field real-return packet staging
command-plan block.
Run `299` audits the current dataset-local return inbox against that guarded
packet contract and staging command-plan block. The inbox contains zero of 57
required packet items: zero of nine measured DZT files, zero of 32 metadata
requirements, zero of nine checksum rows, and zero of seven acceptance gates.
The open work is now split into seven field-side action groups: controlled
profile repeats, time-zero references, amplitude references, global metadata,
per-file metadata, checksums, and acceptance gates. Provenance acceptance, real
archive acceptance, controlled field evidence, field FWI, field 3D/HPC, and GPU
work remain blocked until the measured packet is staged and revalidated.
Run `300` validates the saved run `299` filesystem gap audit from artifacts.
Eight of eight checks pass, confirming the guarded packet contract, 57 missing
packet items, nine missing measured DZT files, 32 missing metadata requirements,
nine missing checksum rows, seven missing acceptance gates, seven open action
groups, blocked downstream field states, figure output, and script snapshots.
Run `301` stress-tests that validator. The exact run `299` gap audit passes,
while 15 damaged variants fail as expected for source identity drift,
contract-guard drift, packet-count drift, false file presence, missing
requirement-count drift, action-row drift, downstream promotion, GPU-priority
drift, figure-validation drift, and script-snapshot drift. Use runs `299-301`
as the guarded field real-return packet filesystem gap-audit block.
Run `302` refreshes the field claim boundary after that filesystem gap audit.
The current boundary contains 11 claims: seven guarded and four blocked. The
real-return execution gate, packet contract, staging plan, and filesystem gap
audit are guarded, but all 57 expected packet items remain missing: nine
measured DZT files, 32 metadata requirements, nine checksum rows, and seven
acceptance gates. Provenance acceptance, real archive acceptance, controlled
field evidence, field FWI, field 3D/HPC, and GPU work remain blocked until the
measured packet is staged and revalidated.
Run `303` validates that saved run `302` claim boundary from artifacts. Nine of
nine checks pass, confirming the claim counts, guarded support claims, blocked
claim rows, packet gap counts, downstream blocked states, figure output, and
script snapshots.
Run `304` stress-tests that validator. The exact run `302` claim boundary
passes, while 25 damaged variants fail as expected for claim-count drift,
guarded support drift, claim-row drift, packet-gap drift, false field-state
promotion, GPU-priority drift, figure-validation drift, and script-snapshot
drift. There are zero unexpected outcomes. Use runs `302-304` as the guarded
field real-return packet gap claim-boundary block.
Run `305` converts that guarded packet gap boundary into a rerunnable
real-return packet acceptance gate. Two source/inventory gates are ready:
guarded source contracts are available, and the expected 57-item packet
inventory is known. Seven measured-data/execution gates remain blocked because
the return inbox contains zero required measured packet items: nine measured
DZT files, 32 metadata requirements, nine checksum rows, and seven acceptance
result files are missing. Use run `305` as the acceptance gate for future
measured field return packets; do not run provenance acceptance, archive
acceptance, controlled field evidence, field FWI, GPU work, or field 3D/HPC
until it passes.
Run `306` validates the saved run `305` acceptance gate from artifacts. Seven
of seven checks pass, confirming acceptance-gate counts, gate order, packet
item rows, action-group rows, downstream blocked states, figure validation, and
script snapshots. Sensitivity hardening remains required before treating the
acceptance gate as fully guarded.
Run `307` stress-tests that validator. The exact run `305` gate passes, while
15 damaged variants fail as expected for gate-count drift, measured-packet
promotion, gate-order drift, blocked-reason removal, packet-row drift,
action-count drift, downstream promotion, GPU-priority drift, figure-validation
drift, and script-snapshot drift. Use runs `305-307` as the guarded field
real-return packet acceptance gate. Field evidence, field FWI, GPU work, and
field 3D/HPC remain blocked until a complete measured packet is present and
passes this gate.
Run `308` folds that guarded acceptance gate into the field claim boundary.
The boundary now has 12 claims: eight guarded and four blocked. The new guarded
claim states that the real-return packet acceptance gate is available; real
packet completion, provenance/archive acceptance, controlled field evidence,
field FWI, GPU work, and field 3D/HPC remain blocked until a complete measured
packet is present and passes the gate.
Run `309` validates the saved run `308` field post-acceptance claim boundary
from artifacts. Seven of seven checks pass, confirming claim counts, the
acceptance-gate claim row, acceptance-gate metrics, blocked claim rows,
downstream blocked states, figure validation, and script snapshots.
Run `310` stress-tests that validator. The exact run `308` boundary passes,
while 10 damaged variants fail as expected for source identity drift,
claim-count drift, acceptance-gate claim drift, acceptance metric drift,
blocked-row drift, downstream promotion, GPU-priority drift, figure-validation
drift, and script-snapshot drift. Use runs `308-310` as the guarded field
post-acceptance claim-boundary block.
Run `311` creates a non-evidence intake worksheet for the future measured
controlled collection return packet. It writes 57 packet-item templates plus a
README inside the run folder only: nine measured DZT templates, 32 metadata
templates, nine checksum templates, and seven acceptance-result templates. No
measured packet items are staged; provenance acceptance, archive acceptance,
controlled field evidence, field FWI, GPU work, and field 3D/HPC remain
blocked until real measured files are staged and the return-packet acceptance
gate passes.
Run `312` validates the saved run `311` field intake worksheet from artifacts.
Seven of seven checks pass, confirming worksheet counts, directory coverage,
action-group coverage, template non-evidence status, blocked measured-packet
state, downstream field guardrails, figure validation, and script snapshots.
Sensitivity hardening remains required before treating the worksheet as a
guarded handoff artifact.
Run `313` stress-tests that validator. The exact run `311` worksheet passes,
while 15 damaged variants fail as expected for count drift, action drift,
template evidence promotion, false measured packet presence, downstream
promotion, GPU-priority drift, figure drift, and script-snapshot drift. Use
runs `311-313` as the guarded field return-packet intake worksheet block; field
evidence remains blocked until measured packet files pass the acceptance gate.
Run `314` folds that guarded intake worksheet into the field claim boundary.
The boundary now has 13 claims: nine guarded and four blocked. The new guarded
claim states that the 57-item controlled-field return-packet worksheet is
generated, validated, and sensitivity-hardened as a non-evidence handoff
artifact. Measured packet completion, provenance/archive acceptance, controlled
field evidence, field FWI, GPU work, and field 3D/HPC remain blocked until the
measured packet passes the acceptance gate.
Run `315` validates the saved run `314` field post-intake claim boundary from
artifacts. Seven of seven checks pass, confirming claim counts, the
intake-worksheet claim row, worksheet metrics, blocked claim rows, downstream
blocked states, figure validation, and script snapshots.
Run `316` stress-tests that validator. The exact run `314` boundary passes,
while 10 damaged variants fail as expected for source identity drift,
claim-count drift, intake-worksheet claim drift, worksheet-metric drift,
blocked-row drift, downstream promotion, GPU-priority drift, figure-validation
drift, and script-snapshot drift. Use runs `314-316` as the guarded field
post-intake claim-boundary block.
Run `317` converts the guarded field return-packet worksheet into a seven-stage
dependency plan: three controlled profile repeats, three time-zero references,
three amplitude references, 11 global metadata values, 21 per-file metadata
values, nine checksum rows, and seven acceptance-result files. The current
archive still has zero measured packet items, so the acceptance gate,
provenance/archive acceptance, controlled field evidence, field FWI, GPU work,
and field 3D/HPC remain blocked.
Run `318` validates the saved run `317` staging dependency plan from artifacts.
Seven of seven checks pass, confirming source identity, stage order, dependency
graph, missing-item classes, blocked downstream states, figure validation, and
script snapshots. Sensitivity hardening remains required before closing this
field staging-plan block.
Run `319` stress-tests that validator. The exact run `317` plan passes, while
15 damaged variants fail as expected for stage-count drift, stage-order drift,
missing-count drift, dependency-graph drift, readiness promotion, field-state
promotion, GPU-priority drift, figure-validation drift, and script-snapshot
drift. Use runs `317-319` as the guarded controlled-field return-packet staging
dependency block.
Run `320` folds that guarded staging dependency block into the field claim
boundary. The boundary now has 14 claims: 10 guarded and four blocked. The new
guarded claim states that the 57 required controlled-field return-packet items
are organized into a seven-stage dependency plan: controlled profile repeats,
time-zero references, amplitude references, global metadata, per-file metadata,
checksum rows, and acceptance-result files. Measured packet completion,
provenance/archive acceptance, controlled field evidence, field FWI, GPU work,
and field 3D/HPC remain blocked until the measured packet passes the
acceptance gate.
Run `321` validates the saved run `320` field post-staging claim boundary from
artifacts. Seven of seven checks pass, confirming claim counts, the staging
dependency claim row, seven stages, nine dependency edges, 57 missing packet
items, blocked downstream field states, figure validation, and script
snapshots. Sensitivity hardening remains required before closing this
claim-boundary block.
Run `322` stress-tests that validator. The exact run `320` claim boundary
passes, while 13 damaged variants fail as expected for claim drift, staging
row drift, staging metric drift, blocked-row drift, field-state promotion,
GPU-priority drift, figure-validation drift, and script-snapshot drift. Use
runs `320-322` as the guarded field post-staging claim-boundary block. Field
evidence remains blocked until the 57-item measured packet is present and
passes the acceptance gate.
Run `323` adds antenna aperture, footprint, coupling, and positioning metadata
requirements to the controlled field return packet contract. The source packet
had 57 items and 32 metadata requirements. The addendum adds four blocking
global metadata records for antenna identity, footprint/phase-center geometry,
ground coupling/lift-off, and positioning/polarization control. The updated
packet target is 61 items, 54 measured requirements, 36 metadata requirements,
and 201 acceptance checks. This update is motivated by the guarded BEM
receiver-aperture audit, where a 10.67 mm non-point aperture changed the
high-frequency scattered line by `0.08009547612144642` relative L2. Provenance
acceptance, real archive acceptance, controlled field evidence, field FWI,
GPU work, and field 3D/HPC remain blocked until the updated measured packet is
staged and validated.
Runs `324-325` validate and sensitivity-harden that addendum: seven validator
checks pass, the exact run `323` artifacts pass, and 13 damaged variants fail
as expected for packet-count drift, metadata-count drift, antenna-row drift,
BEM aperture-motivation drift, downstream promotion, GPU-priority drift,
figure-validation drift, and script-snapshot drift. Use runs `323-325` as the
guarded field antenna aperture metadata-addendum block.
Run `326` folds the guarded antenna metadata addendum into the field claim
boundary. The boundary now has 15 claims: 11 guarded and four blocked. The
current measured-packet target is updated from 57 to 61 items, including 36
metadata requirements and four blocking antenna aperture/coupling metadata
records. Runs `327-328` validate and sensitivity-harden that boundary: seven
validator checks pass, the exact run `326` artifacts pass, and 13 damaged
variants fail as expected for claim drift, antenna-row drift, packet-count
drift, missing-count drift, downstream promotion, GPU-priority drift,
figure-validation drift, and script-snapshot drift. Use runs `326-328` as the
current guarded field post-antenna-metadata claim-boundary block.
Run `329` refreshes the field return-packet acceptance gate for that 61-item
antenna-aware packet. Two setup gates pass because the source contracts and
inventory are known; seven measured-data/execution gates remain blocked because
all 61 packet items are absent. Runs `330-331` validate and sensitivity-harden
the refreshed gate: seven validator checks pass, the exact run `329` artifacts
pass, and 13 damaged variants fail as expected for count drift, gate drift,
packet-row drift, action-row drift, downstream promotion, GPU-priority drift,
figure-validation drift, and script-snapshot drift. Use runs `329-331` as the
current guarded antenna-aware field return-packet acceptance gate.
Run `332` refreshes the staging dependency plan against that current 61-item
antenna-aware packet. The seven-stage sequence remains measured profile
repeats, time-zero references, amplitude references, global metadata, per-file
metadata, checksum rows, and acceptance-result files. The material change from
the older run `317` plan is the global metadata stage: it now requires 15
records, including four blocking antenna aperture/coupling records, so the
packet target is 61 missing items rather than 57.
Runs `333-334` validate and sensitivity-harden the refreshed staging plan:
seven validator checks pass, the exact run `332` artifacts pass, and 16 damaged
variants fail as expected for source-gate drift, packet-count drift,
stage-count drift, stage-order drift, metadata-count drift, antenna-row drift,
readiness promotion, dependency-graph drift, downstream promotion,
GPU-priority drift, figure-validation drift, and script-snapshot drift. Use
runs `332-334` as the guarded antenna-aware field staging dependency block.
Field evidence remains blocked until the 61-item measured packet is present and
passes the refreshed acceptance gate.
Run `335` refreshes the filesystem gap audit for the same 61-item
antenna-aware packet. The current return inbox still contains zero packet
items, so all 61 items are missing: nine measured DZT files, 36 metadata
requirements, nine checksum rows, and seven acceptance-result files. Runs
`336-337` validate and sensitivity-harden the refreshed gap audit: eight
validator checks pass, the exact run `335` artifacts pass, and 15 damaged
variants fail as expected for contract drift, packet-count drift,
present-item drift, metadata-count drift, antenna-metadata drift, action-row
drift, downstream promotion, GPU-priority drift, figure-validation drift, and
script-snapshot drift. Use runs `335-337` as the guarded antenna-aware field
filesystem gap audit block.
Run `338` refreshes the field claim boundary so the current gap, acceptance
gate, and staging rows all cite the 61-item antenna-aware blocks: gap audit
`335-337`, acceptance gate `329-331`, and staging dependency plan `332-334`.
The boundary has 15 claims: 11 guarded and four blocked. The current packet
target remains 61 missing items, including nine DZT files, 36 metadata
requirements, nine checksum rows, and seven acceptance results. Runs `339-340`
validate and sensitivity-harden that boundary: seven validator checks pass, the
exact run `338` artifacts pass, and 14 damaged variants fail as expected for
claim drift, refreshed-row drift, packet-count drift, source-readiness drift,
downstream promotion, GPU-priority drift, figure-validation drift, and
script-snapshot drift. Use runs `338-340` as the current guarded 61-item field
claim-boundary block.
Run `341` creates a corrected non-evidence template pack for the current
61-item antenna-aware field packet. The important clarification is that 61
packet requirements correspond to 49 unique return paths, because several
per-file metadata requirements share one metadata JSON path for the same DZT
item. The pack writes 50 template files including the README: nine measured DZT
templates, 24 metadata templates, nine checksum templates, and seven
acceptance-result templates. Runs `342-343` validate and sensitivity-harden
that corrected pack: eight validator checks pass, exact run `341` artifacts
pass, and 12 damaged variants fail as expected for source-label drift,
packet-count drift, unique-path count drift, false template evidence
promotion, duplicate-count drift, requirement-type drift, antenna-count drift,
downstream promotion, GPU-priority drift, figure-validation drift,
script-snapshot drift, and written-template hash drift. Use runs `341-343` as
the guarded corrected 61-item field template-pack block. Field evidence remains
blocked until real measured items replace the templates and pass the
antenna-aware acceptance gate.
Run `344` refreshes the field claim boundary after that corrected template
pack. The boundary still has 15 claims: 11 guarded and four blocked. The
intake handoff row now points to runs `341-343` and records the clarified
mapping: 61 packet requirements, 49 unique return paths, 50 template files, and
12 duplicate-path requirements. Runs `345-346` validate and sensitivity-harden
that boundary: seven validator checks pass, exact run `344` artifacts pass,
and 14 damaged variants fail as expected for source-label drift, claim-count
drift, template-support drift, template-evidence drift, packet-count drift,
unique-path drift, template-file-count drift, duplicate-count drift,
source-readiness demotion, blocked-support drift, downstream promotion,
GPU-priority drift, figure-validation drift, and script-snapshot drift. Use
runs `344-346` as the current guarded field claim-boundary block. Field
evidence, field FWI, GPU work, and field 3D/HPC remain blocked until real
measured items pass the antenna-aware acceptance gate.
Run `347` tests the corrected 61-item field return-template pack as a consumer
artifact by filling an isolated synthetic packet. The synthetic packet writes
49 files that cover all 61 requirements because 12 requirements share metadata
paths; all seven action groups close, and eight of nine gate rows are ready,
with the field-evidence execution gate still blocked. Runs `348-349` validate
and sensitivity-harden that smoke: seven validator checks pass, the exact run
`347` artifacts pass, and 12 damaged variants fail as expected for count drift,
packet-presence drift, false evidence promotion, field-evidence gate promotion,
real-packet promotion, figure drift, and script-snapshot drift. Use runs
`347-349` as the guarded synthetic consumer-smoke block only; it is not
measured evidence.
Run `350` folds that guarded synthetic consumer-smoke result into the field
claim boundary. The boundary now has 16 claims: 12 guarded and four blocked.
The new guarded claim says the 61-item return templates are structurally
fillable in an isolated synthetic packet; it does not promote synthetic files
to measured evidence. Runs `351-352` validate and sensitivity-harden that
boundary: seven validator checks pass, exact run `350` artifacts pass, and 15
damaged variants fail as expected for claim drift, packet-count drift, false
evidence promotion, blocked-support drift, downstream promotion, GPU-priority
drift, figure drift, and script-snapshot drift. Use runs `350-352` as the
current guarded field post-synthetic-fill-smoke claim-boundary block.
Run `353` consumes the run `347` synthetic packet as a downstream manifest:
all 49 synthetic files parse, account for all 61 packet requirements, and keep
all payloads explicitly marked as synthetic non-evidence. Runs `354-355`
validate and sensitivity-harden that smoke: eight validator checks pass, exact
run `353` artifacts pass, and 13 damaged variants fail as expected for count
drift, payload-parse drift, hash drift, measured-payload promotion, downstream
promotion, figure drift, and script-snapshot drift. Use runs `353-355` as a
guarded field synthetic manifest-consumer block only; measured field evidence,
provenance acceptance, field FWI, GPU work, and field 3D/HPC remain blocked.
Run `356` folds that guarded manifest-consumer block into the field claim
boundary. The boundary now has 17 claims: 13 guarded and four blocked. The new
guarded claim says 49 synthetic files parse into a manifest accounting for all
61 packet requirements with zero measured-evidence payloads. Runs `357-358`
validate and sensitivity-harden that boundary: seven validator checks pass,
exact run `356` artifacts pass, and 13 damaged variants fail as expected for
claim drift, manifest-metric drift, measured-payload promotion, downstream
promotion, figure drift, and script-snapshot drift. Use runs `356-358` as the
current guarded field post-synthetic-manifest-consumer claim-boundary block.
Run `359` audits the anatomy of the run `353` synthetic manifest and explains
the 61-requirement/49-file mapping: metadata carries all 12 duplicate-path
requirements. The current packet has nine measured DZT payloads, 24 metadata
payloads representing 36 metadata requirements, nine checksum payloads, and
seven acceptance-result payloads, all synthetic non-evidence. Runs `360-361`
validate and sensitivity-harden that audit: seven validator checks pass, exact
run `359` artifacts pass, and 18 damaged variants fail as expected for
source-readiness drift, packet-count drift, duplicate-metadata drift,
measured-evidence promotion, downstream promotion, figure drift, and
script-snapshot drift. Use runs `359-361` as the guarded field synthetic
manifest-anatomy block only; measured evidence, provenance acceptance, archive
acceptance, field FWI, GPU work, and field 3D/HPC remain blocked until real
measured files replace the synthetic payloads.
Run `362` folds that guarded manifest-anatomy result into the field claim
boundary. The boundary now has 18 claims: 14 guarded and four blocked. The new
guarded claim explains that 61 packet requirements map to 49 synthetic files
because metadata carries all 12 duplicate-path requirements; it does not
promote synthetic files into measured evidence. Runs `363-364` validate and
sensitivity-harden that boundary: six validator checks pass, exact run `362`
artifacts pass, and 17 damaged variants fail as expected for claim-count
drift, source-readiness drift, anatomy-readiness drift, packet-metric drift,
measured-evidence promotion, downstream promotion, GPU-priority drift, figure
drift, and script-snapshot drift. Use runs `362-364` as the current guarded
field post-synthetic-manifest-anatomy claim-boundary block. Measured evidence,
provenance acceptance, archive acceptance, field FWI, GPU work, and field
3D/HPC remain blocked.
Run `365` converts the guarded synthetic manifest anatomy into a real-return
replacement ledger. The 49-file packet has 33 direct collection inputs to
replace with real files: nine DZT files and 24 metadata files. The remaining
16 files are generated after those real inputs exist: nine checksum files and
seven acceptance-result files. The ledger still covers 61 requirements because
metadata paths carry 12 duplicate-path requirements. Runs `366-367` validate
and sensitivity-harden that ledger: five validator checks pass, exact run
`365` artifacts pass, and 17 damaged variants fail as expected for source
readiness drift, file-count drift, requirement-count drift, replacement-split
drift, action-row drift, measured-payload promotion, downstream promotion,
GPU-priority drift, figure drift, and script-snapshot drift. Use runs
`365-367` as the guarded field real-return replacement-ledger block. Measured
evidence, provenance acceptance, archive acceptance, field FWI, GPU work, and
field 3D/HPC remain blocked until real packet files replace the synthetic
payloads and the generated outputs are regenerated from them.
Run `368` folds that guarded replacement-ledger result into the field claim
boundary. The boundary now has 19 claims: 15 guarded and four blocked. The new
guarded claim records the 33 direct collection inputs, 16 generated
verification outputs, 49 unique packet files, and 61 packet requirements.
Runs `369-370` validate and sensitivity-harden that boundary: five validator
checks pass, exact run `368` artifacts pass, and 21 damaged variants fail as
expected for claim-count drift, ledger-metric drift, evidence-state drift,
blocked-row drift, downstream promotion, GPU-priority drift, figure drift, and
script-snapshot drift. Use runs `368-370` as the current guarded field
post-replacement-ledger claim-boundary block. Measured evidence, provenance
acceptance, archive acceptance, field FWI, GPU work, and field 3D/HPC remain
blocked.
Run `371` converts the 61-item replacement ledger into a four-stage collection
execution checklist: collect nine controlled DZT files, record 24 measured
metadata files carrying 36 metadata requirements, regenerate nine checksum
files, and rerun seven structural/provenance/acceptance outputs. The checklist
has six dependency edges, 33 direct collection inputs, 16 generated
verification outputs, 49 unique packet files, 61 packet requirements, and 12
duplicate-path requirements. Runs `372-373` validate and sensitivity-harden
that checklist: five validator checks pass, exact run `371` artifacts pass,
and 22 damaged variants fail as expected for source-readiness drift,
stage/count drift, dependency drift, downstream promotion, GPU-priority drift,
figure drift, and script-snapshot drift. Use runs `371-373` as the guarded
field collection-execution checklist block. This clarifies execution order but
does not promote measured evidence, provenance acceptance, archive acceptance,
field FWI, GPU work, or field 3D/HPC.
Run `374` folds the guarded collection-execution checklist into the field claim
boundary. The boundary now has 20 claims: 16 guarded and four blocked. The new
guarded claim records four ordered execution stages, six dependency edges, 33
direct collection input files, and 16 generated verification files. Runs
`375-376` validate and sensitivity-harden that boundary: five validator checks
pass, exact run `374` artifacts pass, and 21 damaged variants fail as expected
for claim-count drift, checklist-metric drift, evidence-text drift,
blocked-row drift, downstream promotion, GPU-priority drift, figure drift, and
script-snapshot drift. Use runs `374-376` as the current guarded field
post-checklist claim-boundary block. Measured evidence, provenance acceptance,
archive acceptance, field FWI, GPU work, and field 3D/HPC remain blocked.
Run `377` turns the guarded collection checklist into a file-level operator
handoff manifest. It preserves all 49 packet paths and separates the 33 direct
collection inputs from the 16 generated follow-up files. The first 33 rows are
operator-numbered direct inputs: nine DZT files and 24 metadata files. The
remaining generated rows are nine checksum files and seven acceptance outputs
to rerun only after the real inputs exist. Runs `378-379` validate and
sensitivity-harden that handoff: five validator checks pass, exact run `377`
artifacts pass, and 24 damaged variants fail as expected for source-readiness
drift, handoff-shape drift, direct/generated count drift, operator-sequence
drift, type/count drift, measured-evidence promotion, downstream promotion,
GPU-priority drift, figure drift, and script-snapshot drift. Use runs
`377-379` as the guarded field operator-handoff manifest block. Measured
evidence, provenance acceptance, archive acceptance, field FWI, GPU work, and
field 3D/HPC remain blocked.
Run `380` folds the guarded operator handoff into the field claim boundary.
The boundary now has 21 claims: 17 guarded and four blocked. The new guarded
claim records 49 handoff rows, 33 direct operator items, 16 generated
follow-up items, 61 packet requirements, and 12 duplicate-path requirements.
Runs `381-382` validate and sensitivity-harden that boundary: five validator
checks pass, exact run `380` artifacts pass, and 25 damaged variants fail as
expected for claim-count drift, handoff-claim support drift, handoff-metric
drift, measured-payload promotion, blocked-row drift, downstream promotion,
GPU-priority drift, figure drift, and script-snapshot drift. Use runs
`380-382` as the current guarded field post-handoff claim-boundary block.
Measured evidence, provenance acceptance, archive acceptance, field FWI, GPU
work, and field 3D/HPC remain blocked.
Run `383` converts the guarded operator handoff into a fillable real-return
packet intake worksheet. The worksheet preserves 49 packet rows, 33 direct
real-input rows, 16 generated follow-up rows, 61 packet requirements, and 12
duplicate-path requirements. It deliberately leaves 294 completion cells blank
and has zero measured-evidence rows. Runs `384-385` validate and
sensitivity-harden that worksheet: six validator checks pass, exact run `383`
artifacts pass, and 29 damaged variants fail as expected for worksheet-shape
drift, blank-cell drift, completed-row drift, measured-evidence promotion,
default-status drift, packet-count drift, downstream promotion, GPU-priority
drift, figure drift, and script-snapshot drift. Use runs `383-385` as the
guarded field real-return intake-worksheet block. Measured evidence,
provenance acceptance, archive acceptance, field FWI, GPU work, and field
3D/HPC remain blocked until the worksheet is filled from real packet files.
Run `386` folds the guarded intake worksheet into the field claim boundary.
The boundary now has 22 claims: 18 guarded and four blocked. The new guarded
claim records 49 worksheet rows, 33 direct real-input rows, 16 generated
follow-up rows, 294 blank completion cells, zero completed rows, and zero
measured-evidence rows. Runs `387-388` validate and sensitivity-harden that
boundary: five validator checks pass, exact run `386` artifacts pass, and 28
damaged variants fail as expected for claim-count drift, intake-claim support
drift, worksheet metric drift, completed-row and evidence-row promotion,
downstream promotion, figure drift, and script-snapshot drift. Use runs
`386-388` as the current guarded field post-intake-worksheet claim-boundary
block. Measured evidence, provenance acceptance, archive acceptance, field
FWI, GPU work, and field 3D/HPC remain blocked.
Run `389` defines the parser contract for a future filled intake worksheet.
It keeps the current 49 worksheet rows rejected as blank, requires five
completion fields per row before parsing can accept a row, leaves the intake
note optional, and records zero current measured-evidence rows. Runs `390-391`
validate and sensitivity-harden that contract: five validator checks pass,
exact run `389` artifacts pass, and 28 damaged variants fail as expected for
worksheet readiness drift, row-count drift, completion-rule drift,
parser-state promotion, current evidence promotion, downstream promotion,
GPU-priority drift, figure drift, and script-snapshot drift. Use runs
`389-391` as the guarded field intake-completion parser-contract block.
Measured evidence, provenance acceptance, archive acceptance, field FWI, GPU
work, and field 3D/HPC remain blocked until a filled worksheet passes this
parser contract with real files, hashes, byte counts, timestamps, and operator
identifiers.
Run `392` folds that guarded parser contract into the field claim boundary.
The boundary now has 23 claims: 19 guarded and four blocked. The new guarded
claim records 49 worksheet rows, six completion rules, five required
completion fields, eight parser states, zero parser-accepted current rows, and
zero current measured-evidence rows. Runs `393-394` validate and
sensitivity-harden that boundary: five validator checks pass, exact run `392`
artifacts pass, and 32 damaged variants fail as expected for claim-count
drift, parser-claim support drift, parser-metric drift, current-row acceptance
promotion, measured-evidence promotion, downstream promotion, GPU-priority
drift, figure drift, and script-snapshot drift. Use runs `392-394` as the
current guarded field post-parser-contract claim-boundary block. Measured
evidence, provenance acceptance, archive acceptance, field FWI, GPU work, and
field 3D/HPC remain blocked.
Run `395` tests the parser acceptance path with a fully filled synthetic
worksheet. It fills all 245 required completion cells across the 49 rows, plus
49 optional notes, using deterministic synthetic paths, hashes, byte counts,
timestamps, and operator identifiers. The parser accepts all 49 rows
syntactically, but the run records zero measured-evidence rows and keeps real
packet files, provenance acceptance, archive acceptance, field FWI, GPU work,
and field 3D/HPC blocked. Runs `396-397` validate and sensitivity-harden that
acceptance-path smoke: five validator checks pass, exact run `395` artifacts
pass, and 30 damaged variants fail as expected for count drift,
source-readiness drift, completion syntax drift, evidence-state drift,
downstream promotion, figure drift, and script-snapshot drift. Use runs
`395-397` as the guarded synthetic field intake acceptance-path smoke block.
This proves the parser can accept a complete worksheet shape; it does not
promote the current archive to field evidence.
Run `398` folds that guarded synthetic acceptance-path smoke into the field
claim boundary. The boundary now has 24 claims: 20 guarded and four blocked.
The new guarded claim records 49 filled synthetic rows, 245 filled required
completion cells, 49 syntactically accepted rows, zero rejected rows, and zero
measured-evidence rows. Runs `399-400` validate and sensitivity-harden that
boundary: five validator checks pass, exact run `398` artifacts pass, and 29
damaged variants fail as expected for claim-count drift, smoke-readiness
drift, metric drift, claim-support drift, downstream promotion, figure drift,
and script-snapshot drift. Use runs `398-400` as the current guarded field
post-synthetic-acceptance claim-boundary block. Real packet files, measured
field evidence, provenance acceptance, archive acceptance, field FWI, GPU work,
and field 3D/HPC remain blocked.
Run `401` adds an explicit evidence firewall around the synthetic acceptance
path: all 49 accepted synthetic rows are allowed for parser-regression testing,
zero are allowed as measured field evidence, provenance acceptance, archive
acceptance, or field FWI inputs, and all 49 require real replacement before
evidence. Runs `402-403` validate and sensitivity-harden that firewall: five
validator checks pass, exact run `401` artifacts pass, and 24 damaged variants
fail as expected for source-readiness drift, parser/evidence firewall drift,
downstream promotion, GPU-priority drift, figure drift, and script-snapshot
drift. Use runs `401-403` as the guarded synthetic-acceptance evidence-firewall
block. Real packet files, measured field evidence, provenance acceptance,
archive acceptance, field FWI, GPU work, and field 3D/HPC remain blocked.
Run `404` folds that guarded evidence firewall into the field claim boundary.
The boundary now has 25 claims: 21 guarded and four blocked. The new guarded
claim records 49 firewall rows, 49 parser-regression rows, zero rows allowed
as measured evidence, provenance acceptance, archive acceptance, or field-FWI
inputs, and 49 real replacements required before evidence promotion. Runs
`405-406` validate and sensitivity-harden that boundary: five validator checks
pass, exact run `404` artifacts pass, and 32 damaged variants fail as expected
for claim-count drift, firewall-readiness drift, firewall metric drift,
claim-support drift, downstream promotion, GPU-priority drift, figure drift,
and script-snapshot drift. Use runs `404-406` as the current guarded field
post-synthetic-acceptance-firewall claim-boundary block. Real packet files,
measured field evidence, provenance acceptance, archive acceptance, field FWI,
GPU work, and field 3D/HPC remain blocked.
Run `407` converts that evidence firewall into a release-gate checklist for a
future real packet. The gate has 49 blocked rows: 33 direct real-input rows and
16 generated follow-up rows. It defines six ordered actions: replace direct
real inputs, regenerate follow-up outputs, rerun the intake parser contract,
rerun the provenance gate, rerun archive acceptance, and only then evaluate
field FWI, GPU work, or 3D/HPC. Runs `408-409` validate and
sensitivity-harden that release gate: five validator checks pass, exact run
`407` artifacts pass, and 26 damaged variants fail as expected for count
drift, row promotion, action-order drift, dependency drift, downstream
promotion, GPU-priority drift, figure drift, and script-snapshot drift. Use
runs `407-409` as the guarded field evidence-firewall release-gate block. Real
packet files, measured field evidence, provenance acceptance, archive
acceptance, field FWI, GPU work, and field 3D/HPC remain blocked.
Run `410` folds the guarded release gate into the field claim boundary. The
boundary now has 26 claims: 22 guarded and four blocked. The new guarded claim
records 49 release-gate rows, 33 direct real-input rows, 16 generated follow-up
rows, six release actions, six dependency edges, zero release-ready rows, and
49 still-blocked rows. Runs `411-412` validate and sensitivity-harden that
boundary: five validator checks pass, exact run `410` artifacts pass, and 32
damaged variants fail as expected for claim-count drift, release-gate claim
drift, release-gate metric drift, blocked-row drift, downstream promotion,
GPU-priority drift, figure drift, and script-snapshot drift. Use runs
`410-412` as the current guarded field post-release-gate claim-boundary block.
Real packet files, measured field evidence, provenance acceptance, archive
acceptance, field FWI, GPU work, and field 3D/HPC remain blocked.
Run `413` defines the real packet acceptance gate after that release-gate
boundary. The gate has 49 acceptance rows: 33 direct real-input rows and 16
generated follow-up rows. It records zero real-source accepted rows, zero
parser-accepted real rows, zero provenance-accepted rows, zero archive-accepted
rows, zero measured-evidence rows, and 49 rows still blocking field FWI. Runs
`414-415` validate and sensitivity-harden that gate: four validator checks
pass, exact run `413` artifacts pass, and 28 damaged variants fail as expected
for count drift, premature real-source acceptance, parser/provenance/archive
promotion, measured-evidence promotion, downstream promotion, GPU-priority
drift, figure drift, and script-snapshot drift. Use runs `413-415` as the
guarded field real-packet acceptance-gate block.
Run `416` folds that guarded real-packet acceptance gate into the field claim
boundary. The boundary now has 27 claims: 23 guarded and four blocked. The new
guarded claim records 49 acceptance rows, 33 direct real-input rows, 16
generated follow-up rows, zero real-source accepted rows, zero parser-accepted
real rows, zero provenance-accepted rows, zero archive-accepted rows, zero
measured-evidence rows, and 49 blocked acceptance rows. Runs `417-418`
validate and sensitivity-harden that boundary: five validator checks pass,
exact run `416` artifacts pass, and 34 damaged variants fail as expected for
claim-count drift, acceptance-gate readiness drift, acceptance-gate metric
drift, premature field-evidence promotion, downstream promotion, GPU-priority
drift, figure drift, and script-snapshot drift. Use runs `416-418` as the
current guarded field post-real-packet-acceptance claim-boundary block.
Run `419` audits the filesystem against the 33 direct real-input slots required
by the 61-item real-packet acceptance gate. All 33 direct slots remain open
gaps. The scan finds zero real-return candidates, 62 blank-template matches,
and 33 synthetic-reference matches. Runs `420-421` validate and
sensitivity-harden that audit: four validator checks pass, exact run `419`
artifacts pass, and 23 damaged variants fail as expected for scan-count drift,
real-file promotion, template/synthetic misclassification, measured-evidence
promotion, downstream promotion, GPU-priority drift, figure damage, and
script-snapshot damage. Use runs `419-421` as the guarded field filesystem
gap-audit block. Controlled field evidence, provenance acceptance, archive
acceptance, field FWI, GPU work, and field 3D/HPC remain blocked.
Run `422` folds that guarded filesystem gap audit into the field claim
boundary. The boundary now has 28 claims: 24 guarded and four blocked. The new
guarded claim records 33 direct real-input slots, 33 open filesystem gaps, zero
real-return candidates, 62 blank-template matches, 33 synthetic-reference
matches, and zero accepted measured-evidence files. Runs `423-424` validate and
sensitivity-harden that boundary: five validator checks pass, exact run `422`
artifacts pass, and 31 damaged variants fail as expected for claim-count drift,
gap-audit metric drift, source sensitivity drift, premature real-file and
evidence promotion, downstream promotion, GPU-priority drift, claim-row damage,
blocked-row damage, figure damage, and script-snapshot damage. Use runs
`422-424` as the current guarded field post-filesystem-gap claim-boundary
block. Real packet files, measured field evidence, provenance acceptance,
archive acceptance, field FWI, GPU work, and field 3D/HPC remain blocked.
Run `425` converts those 33 open direct real-input slots into a concrete
staging manifest: nine measured DZT files, fifteen global metadata JSON files,
and nine per-file metadata JSON files. The manifest records five ordered
actions: stage DZT files, stage global metadata, stage per-file metadata, rerun
the intake parser, and rerun provenance/archive gates. It stages zero real
files, accepts zero measured-evidence files, and disallows all template or
synthetic substitutions. Real packet files, measured field evidence,
provenance acceptance, archive acceptance, field FWI, GPU work, and field
3D/HPC remain blocked.
Run `426` validates that staging manifest with five passing checks, confirming
the 33 direct slots, the 9/15/9 DZT/global-metadata/file-metadata split, the
non-evidence staging rows, the ordered parser/provenance/archive actions, and
blocked downstream states.
Run `427` sensitivity-hardens that validator: exact run `425` artifacts pass,
and eight damaged variants fail as expected for slot-count drift, DZT
group-count drift, template substitution, staged-file promotion, action-order
drift, downstream evidence promotion, figure damage, and script-snapshot
damage. Use runs `425-427` as the guarded direct-intake staging-manifest block.
Run `428` folds that guarded direct-intake staging manifest into the field
claim boundary. The boundary now has 29 claims: 25 guarded and four blocked.
The new guarded claim records 33 direct real-input slots split into nine
measured DZT files, fifteen global metadata JSON files, and nine per-file
metadata JSON files; five ordered staging/parser/provenance/archive actions;
zero staged real files; zero accepted measured-evidence files; and zero
template or synthetic substitutions allowed. Real packet files, measured field
evidence, provenance acceptance, archive acceptance, field FWI, GPU work, and
field 3D/HPC remain blocked.
Run `429` validates that boundary with five passing checks, confirming the new
guarded claim, the 9/15/9 direct-intake split, zero staged real files, zero
accepted measured-evidence files, four blocked field-evidence claims, and no
downstream promotion.
Run `430` sensitivity-hardens that validator: exact run `428` artifacts pass,
and nine damaged variants fail as expected for claim-count drift,
claim-support drift, DZT-count drift, staged-file promotion, measured-evidence
promotion, field-FWI promotion, blocked-row support drift, figure damage, and
script-snapshot damage. Use runs `428-430` as the guarded post-direct-intake
field claim-boundary block.
Run `431` converts the 33 latest direct staging paths into a strict pre-ingest
contract. The contract records five required staging directories, nine DZT
signature checks, 24 JSON parse checks, 33 SHA-256 requirements, zero current
files, zero current hashes, and six ordered actions before parser/provenance
reruns. It keeps real packet acceptance, controlled field evidence, field FWI,
GPU work, and field 3D/HPC blocked.
Run `432` validates that pre-ingest contract with six passing checks,
confirming the 33-row shape, 9/15/9 file split, path-extension rules, required
DZT/JSON/SHA-256 checks, five absent staging directories, six ordered actions,
zero current files, zero current hashes, blocked downstream states, and
nonblank figure/script snapshots.
Run `433` sensitivity-hardens that validator. The exact run `431` artifacts
pass, while eleven damaged variants fail as expected for pre-ingest row-count
drift, DZT-count drift, extension damage, file promotion, SHA-256 promotion,
directory promotion, action-order damage, controlled-evidence promotion,
field-FWI promotion, figure damage, and script-snapshot damage. Use runs
`431-433` as the guarded direct-intake pre-ingest contract block.
Run `434` closes only the first pre-ingest action by materializing the five
empty staging directories required by run `431`. It creates directories for
metadata files, global metadata, amplitude references, controlled profile
repeats, and time-zero references. It creates zero DZT files, zero JSON files,
zero hashes, and zero template or synthetic files, so field evidence, parser
acceptance, provenance acceptance, archive acceptance, field FWI, GPU work, and
field 3D/HPC remain blocked. Runs `435-436` validate and sensitivity-harden
that scaffold: six validator checks pass, exact run `434` artifacts pass, and
eleven damaged variants fail as expected for source damage, directory damage,
file/hash/template promotion, evidence promotion, action damage, figure damage,
and script-snapshot damage. Use runs `434-436` as the guarded empty-directory
scaffold block before copying measured field files. Run `437` performs a
read-only live receipt audit over that scaffold. The five required directories
are present and no unexpected files are found, but all 33 expected direct
intake files remain missing: nine measured DZT files and 24 metadata JSON
files. Parser acceptance, provenance acceptance, archive acceptance, controlled
field evidence, field FWI, GPU work, and field 3D/HPC remain blocked. Run
`438` validates that live audit with five passing checks. Run `439`
sensitivity-hardens the validator: exact run `437` artifacts pass, while 11
damaged variants fail as expected for source readiness damage, directory
damage, file/receipt promotion, unexpected-file promotion, parser/downstream
promotion, action damage, figure damage, and script-snapshot damage. Use runs
`437-439` as the guarded live-receipt audit block before any parser,
provenance, archive, field FWI, or field 3D/HPC rerun. Run `440` defines the
metadata JSON schema contract for the 24 missing metadata files: 15 global
metadata JSON files, nine per-file metadata JSON files, and 129 required
top-level field entries. It writes no live metadata files and accepts no
metadata, so parser acceptance, provenance acceptance, archive acceptance,
controlled field evidence, field FWI, GPU work, and field 3D/HPC remain
blocked. Run `441` validates that schema contract with five passing checks.
Run `442` sensitivity-hardens the validator: exact run `440` artifacts pass,
while eleven damaged variants fail as expected for source damage, count drift,
schema-family damage, live-file promotion, schema-acceptance promotion,
template/synthetic allowance, downstream promotion, action damage, figure
damage, and script-snapshot damage. Use runs `440-442` as the guarded metadata
JSON schema contract block. Run `443` defines the companion DZT file schema
contract for the measured data side: nine DZT files in three families
(`amplitude_reference`, `controlled_profile_repeat`, and `time_zero_reference`),
54 required receipt/parser/metadata-link checks, zero live DZT files, zero
accepted DZT schemas, and no parser, provenance, archive, field-FWI, or
field-3D/HPC promotion. Run `444` validates that DZT contract with five
passing checks: source readiness, exact nine-file/three-family/54-check shape,
contract-only zero-DZT state, blocked actions/downstream states, and
figure/script snapshots. Run `445` sensitivity-hardens that validator: exact
run `443` artifacts pass, while 16 damaged variants fail as expected for source
readiness damage, DZT file/family/check count drift, family-shape and check-name
damage, live-DZT/checksum/parser/metadata-link/schema-acceptance promotion,
template substitution, action/downstream promotion, figure damage, and
script-snapshot damage. Use runs `443-445` as the guarded DZT file schema block.
Run `446` combines the guarded metadata JSON and DZT contracts into one
33-file acceptance gate. The gate requires nine DZT files, 24 metadata JSON
files, 54 DZT receipt/parser/metadata-link checks, and 129 metadata field
requirements. No real files are present or accepted, so parser acceptance,
provenance acceptance, archive acceptance, controlled field evidence, field FWI,
and field 3D/HPC remain blocked. Run `447` validates that combined gate with
five passing checks: source readiness, exact 33-file/216-requirement shape,
contract-only zero-file state, blocked actions/downstream states, and
figure/script snapshots. Run `448` sensitivity-hardens that validator: exact
run `446` artifacts pass, while 17 damaged variants fail as expected for source
readiness damage, file/check/field/total-requirement count drift, live-file and
accepted-file promotion, parser/provenance/archive promotion,
action/downstream promotion, figure damage, and script-snapshot damage. Use
runs `446-448` as the guarded combined direct-intake acceptance-gate block.
Run `449` checks the live staged return filesystem against that combined gate.
The five required staging directories are present, no unexpected files are
found, and all 33 required files remain missing: nine DZT files and 24 metadata
JSON files. Parser acceptance, provenance acceptance, archive acceptance,
controlled field evidence, field FWI, and field 3D/HPC remain blocked. Run
`450` validates that filesystem gap with five passing checks: source readiness,
directory scaffold presence, 33 missing required files, blocked
actions/downstream states, and figure/script snapshots. Run `451`
sensitivity-hardens that validator: exact run `449` artifacts pass, while 15
damaged variants fail as expected for source-chain damage, directory damage,
unexpected-file promotion, file count/presence/nonempty drift, DZT/metadata
missing-count drift, schema-acceptance promotion, action damage, downstream
promotion, figure damage, and script-snapshot damage. Run `452` locks the
expected receipt manifest for those future measured returns: 33 unique receipt
identities, nine DZT files, 24 metadata JSON files, 183 file-level checks, and
five present staging directories, while accepting zero files. Run `453`
validates that receipt manifest with five passing checks. Run `454`
sensitivity-hardens the validator: exact run `452` artifacts pass, while
eleven damaged variants fail as expected for source damage, missing or
duplicate receipts, extension damage, directory damage, file and schema
promotion, action promotion, downstream promotion, figure damage, and
script-snapshot damage. Use runs `449-454` as the current live filesystem gap
and guarded receipt-manifest lock before copying measured field files. Run
`455` converts that receipt manifest into an ordered 33-item collection-day
checklist: nine DZT files, 24 metadata JSON files, five copy/rerun actions,
and zero evidence-ready items. Use run `455` as the practical copy checklist;
after files are copied, rerun receipt, parser, provenance, and archive gates
before field FWI or field 3D/HPC work. Run `456` converts that checklist into
33 non-executed receipt-check commands: nine DZT nonempty/checksum checks and
24 JSON nonempty/parse/checksum checks. Use run `456` after measured files are
copied, then rerun receipt, parser, provenance, and archive gates. Run `457`
creates 24 fillable metadata JSON templates from the guarded schema contract:
15 global metadata templates, nine per-file metadata templates, and 129
top-level fields. The templates parse as JSON but contain blank or null real
values, are stored only in the run output folder, and are not live field files
or accepted evidence. Run `458` validates that template pack with five passing
checks: source readiness, exact 24-file/129-field shape, blank required real
values, blocked downstream states, figure output, and frozen script snapshots.
Run `459` joins the run `455` checklist with the validated metadata templates
into one collection-day bundle manifest: 33 required live-file entries, nine
DZT entries, 24 metadata JSON entries, 24 linked metadata templates, and zero
live files or evidence-ready entries.
Run `460` validates that bundle manifest from a consumer perspective. Five of
five checks pass: source readiness, exact 33-entry/9-DZT/24-JSON shape, 24
metadata template links, zero live files, zero receipt-ready rows, zero
evidence-ready rows, blocked downstream states, figure output, and frozen
script snapshots. Use runs `459-460` as the guarded collection-day bundle block
before copying measured DZT files and completed metadata JSON files into live
staging.
Run `461` sensitivity-hardens that validator: the exact run `459` bundle
passes, while ten damaged variants fail as expected for source readiness drift,
missing bundle rows, DZT/JSON count drift, removed metadata-template links,
missing template paths, premature live-file promotion, premature
evidence-ready promotion, downstream field-evidence promotion, figure damage,
and script-snapshot damage. Use runs `459-461` as the guarded collection-day
bundle block.
Run `462` audits the live boundary after that bundle block. The field stream
has 57 prepared artifacts across metadata templates and receipt commands, but
0 of the 33 required live files are present. The missing live files are nine
DZT files and 24 completed metadata JSON files. Receipt commands remain
unexecuted, evidence-ready rows remain zero, and parser, provenance, archive,
field FWI, GPU work, and field 3D/HPC remain blocked. Run `463`
sensitivity-hardens that live-boundary audit: the exact run `462` source state
passes, while seven damaged states fail as expected for metadata-template
readiness damage, bundle-validator readiness damage, live-file promotion,
missing-count drift, receipt-command execution promotion, receipt-readiness
promotion, and downstream controlled-evidence promotion. Run `464` adds a
reusable live receipt verifier and runs it against the current locked 33-row
manifest. The verifier writes a current-state receipt report, but all 33 files
remain missing, zero receipt rows pass, and parser, provenance, archive, field
FWI, GPU work, and field 3D/HPC remain blocked. Run `465` validates that
current-state receipt report with six passing checks: source readiness, exact
33-row/9-DZT/24-JSON shape, all live files missing, zero receipt readiness,
blocked downstream states, and figure/script presence. Run `466`
sensitivity-hardens the validator: the exact current-state report passes,
while eight damaged states fail as expected for source readiness damage,
receipt report shape damage, live-file promotion, missing-count drift,
receipt-readiness promotion, downstream field-FWI promotion, figure damage, and
missing script snapshots. Run `467` defines the live receipt acceptance gate:
five receipt families, 33 required files, 183 required receipt checks, zero
present live files, zero receipt-ready rows, and zero accepted families. Parser,
provenance, archive, controlled field evidence, field FWI, GPU work, and field
3D/HPC remain blocked until all 33 receipt rows pass.
Run `468` validates that gate with six passing checks: source readiness,
five-family/33-file shape, six acceptance checks, zero current live receipts,
blocked actions/downstream states, and figure/script artifacts.
Run `469` sensitivity-hardens that validator: the exact run `467` gate passes,
while ten damaged states fail as expected for source readiness removal,
receipt-family removal, family-acceptance promotion, acceptance-check removal,
live-receipt promotion, parser-readiness promotion, field-FWI promotion,
action-readiness promotion, figure damage, and missing script snapshots.
Run `470` audits the current live staging tree against that latest receipt
gate. All five staging directories are present and no unexpected files are
found, but all 33 required receipt files are still missing: nine measured DZT
files and 24 completed metadata JSON files. Parser reruns, provenance
acceptance, archive acceptance, controlled field evidence, field FWI, and field
3D/HPC remain blocked.
Run `471` validates that staging-gap audit with six passing checks: source-chain
readiness, staging-directory shape, 33 missing required files, family gap shape,
blocked actions/downstream states, and figure/script artifacts.
Run `472` sensitivity-hardens that validator: the exact run `470` audit passes,
while fourteen damaged states fail as expected for source readiness removal,
directory drift/absence, unexpected-file promotion, file-count drift,
file/receipt/family readiness promotion, action-readiness promotion, field-FWI
promotion, figure damage, and missing script snapshots.
Run `473` reduces the same live staging gap into six closure groups: three
controlled profile DZT files, three time-zero reference DZT files, three
amplitude-reference DZT files, fifteen global metadata JSON files, nine
per-file metadata JSON files, and one receipt/parser/provenance/archive rerun
group. No files are present or accepted, and field FWI, GPU work, and field
3D/HPC remain blocked.
Run `474` validates the closure plan with five passing checks: source
readiness, six closure groups, exact 33-row missing-file table, blocked
closure/downstream state, and figure/script artifacts.
Run `475` sensitivity-hardens the validator: the exact run `473` closure plan
passes, while twelve damaged states fail as expected for closure-group damage,
missing-file count drift, family identity damage, file/receipt readiness
promotion, field-FWI promotion, figure damage, and missing script snapshots.
Run `476` audits the live field staging paths after that closure-plan block and
confirms that the planning step created no live files: all 33 required receipt
files remain absent, zero receipt rows are ready, and receipt, parser,
provenance, archive, controlled field evidence, field FWI, GPU work, and field
3D/HPC remain blocked. Run `477` validates that guard with five passing checks:
source-chain readiness, exact 33-row/9-DZT/24-metadata live guard shape, zero
live-file or receipt promotion, blocked downstream states, and figure/script
artifacts. Run `478` sensitivity-hardens the validator: the exact run `476`
guard passes, while thirteen damaged states fail as expected for source-chain
damage, live-file promotion, receipt-readiness promotion,
closure-plan-created-file promotion, field-FWI promotion, figure damage, and
missing script snapshots. Run `479` converts the validated live-boundary block
into a collection-day route specification: three controlled profile repeat DZT
files, three time-zero reference DZT files, three amplitude-reference DZT
files, fifteen global metadata JSON files, nine per-file metadata JSON files,
and a receipt/parser/provenance/archive rerun phase. The route has 33 files and
183 receipt checks; zero files are present or receipt-ready, so parser,
provenance, archive, field FWI, GPU work, and field 3D/HPC remain blocked.
Run `480` validates that route spec with five passing checks: exact
33-route/9-DZT/24-metadata shape, six phase shape, 183 receipt checks, zero
present or receipt-ready files, blocked downstream states, and figure/script
artifacts. Run `481` sensitivity-hardens the validator: the exact run `479`
route spec passes, while fourteen damaged states fail as expected for route
count damage, phase damage, receipt-check-count damage, file/receipt readiness
promotion, field-FWI or field-3D/HPC promotion, figure damage, and missing
script snapshots. Run `482` exercises that route in an output-local sandbox:
33 synthetic placeholder files pass the shallow live-receipt verifier with 183
receipt checks, while the locked live external return paths still contain zero
measured files and controlled field evidence, parser, provenance, archive,
field FWI, GPU work, and field 3D/HPC remain blocked. Run `483` validates that
sandbox smoke with five passing checks: exact 33-file/9-DZT/24-metadata
synthetic shape, 33 sandbox receipt-ready rows, 183 receipt checks, zero live
measured files, zero measured evidence files, blocked downstream states, and
figure/script artifacts. Run `484` sensitivity-hardens the validator: the exact
run `482` sandbox smoke passes, while twenty-one damaged states fail as
expected for synthetic-boundary loss, measured-evidence promotion,
receipt-readiness damage, live-file promotion, parser/provenance/archive
promotion, field-FWI/3D promotion, figure damage, and missing script
snapshots. Run `485` audits the locked live paths after the sandbox smoke and
confirms that all 33 synthetic files remained output-local: zero live files
exist, zero sandbox files overlap the live paths, zero sandbox files are under
the live root, and live receipt, parser, provenance, archive, controlled field
evidence, field FWI, GPU work, and field 3D/HPC remain blocked. Run `486`
validates that guard with five passing checks: exact 33-row shape, 33 sandbox
files, zero live files, zero sandbox/live path overlap, zero measured evidence
files, blocked downstream states, and figure/script artifacts. Run `487`
sensitivity-hardens the validator: the exact run `485` guard passes, while
eighteen damaged states fail as expected for live-file promotion,
sandbox/live-path overlap, sandbox-under-live-root promotion,
synthetic-boundary loss, measured-evidence promotion, downstream promotion,
figure damage, and missing script snapshots. Run `488` turns the validated
post-sandbox route into an incremental acceptance frontier over the five file
families: controlled profile repeats, time-zero references, amplitude
references, global metadata, and per-file metadata. It enumerates all 32
family-completion scenarios and finds that zero partial scenarios satisfy the
conservative receipt gate. All five families, totaling 33 files and 183 receipt
checks, are required before parser/provenance/archive promotion can proceed.
Run `489` validates that frontier from artifacts with five passing checks:
family table shape, 32-scenario frontier shape, all-family-only completion,
blocked live/downstream state, and figure/script artifacts. Run `490`
sensitivity-hardens that validator: the exact run `488` frontier passes, while
sixteen damaged states fail as expected for family-total damage, frontier-row
damage, partial-completion promotion, live-file/receipt promotion, downstream
promotion, figure damage, and missing script snapshots. Run `491` converts the
frontier into a work-split policy: the 15 global metadata files can be prepared
before collection, while the nine measured DZT files and nine per-file metadata
records remain measurement-dependent. The all-files-required promotion gate is
unchanged. Run `492` validates that policy with five passing checks: source
readiness, exact four-stage route shape, 15 pre-collection files, 18
measurement-dependent files, blocked partial-delivery promotion, and
figure/script artifacts. Run `493` sensitivity-hardens that validator: the
exact run `491` policy passes, while fifteen damaged states fail as expected
for source readiness damage, stage or count damage, timing/dependency damage,
partial-promotion damage, field-FWI or field-3D/HPC promotion, figure damage,
and missing script snapshots. Run `494` creates an output-local pre-collection
template pack for the fifteen global metadata JSON files. The templates have
nine keys each, contain thirty value/unit placeholders in total, and have zero
path overlap with the live external return paths. They help prepare collection
metadata but do not count as live receipt files; live receipt, parser,
provenance, archive, field FWI, and field 3D/HPC remain blocked. Run `495`
validates the template pack with five passing checks: source readiness, exact
15-template global metadata route shape, placeholder schema, output-local
non-receipt placement, and figure/script artifacts. Run `496`
sensitivity-hardens that validator: the exact run `494` template pack passes,
while sixteen damaged states fail as expected for template identity damage,
required-check damage, template-written damage, placeholder-count damage,
live-file or receipt promotion, path-overlap promotion, field-FWI or
field-3D/HPC promotion, figure damage, and missing script snapshots.
Run `497` creates an output-local post-measurement template pack for the nine
per-file metadata JSON files. Each template is paired with one expected DZT
filename, has twelve keys, contains four measured-value placeholders, and is
explicitly marked as requiring measured DZT. The templates have zero path
overlap with live external return paths and do not count as live receipt files;
live receipt, parser, provenance, archive, field FWI, and field 3D/HPC remain
blocked. Run `498` validates that template pack with five passing checks:
source readiness, exact nine-template per-file route shape, measured-DZT
dependency, output-local non-receipt placement, and figure/script artifacts.
Run `499` sensitivity-hardens that validator: the exact run `497` template
pack passes, while eighteen damaged states fail as expected for template
identity, paired-DZT identity, required-check damage, placeholder damage,
measured-DZT dependency removal, live-file or receipt promotion, field-FWI or
field-3D/HPC promotion, figure damage, and missing script snapshots. Run `500`
combines the validated metadata preparation streams into one collection-day
bundle manifest: 15 global pre-collection templates and nine per-file
post-measurement templates, totaling 24 output-local templates, 129 receipt
checks, and 66 placeholders. The manifest does not promote live receipt,
parser/provenance/archive readiness, field FWI, or field 3D/HPC. Run `501`
validates that manifest with five passing checks: source readiness,
15/9 global/per-file shape, pre-collection/post-measurement timing shape,
template accounting and hashes, blocked live receipt/downstream states, and
figure/script artifacts. Run `502` sensitivity-hardens that validator: the
exact run `500` bundle manifest passes, while eighteen damaged states fail as
expected for family/timing shape damage, paired-DZT damage, accounting drift,
template hash damage, live-receipt promotion, field-FWI or field-3D/HPC
promotion, figure damage, and missing script snapshots. Run `503` audits the
locked live external-return paths after that bundle block and confirms that the
24 metadata templates remain output-local preparation files: 24 template files
exist, zero live files exist, zero templates overlap live paths, zero templates
sit under the live staging root, and live receipt, parser/provenance/archive,
controlled field evidence, field FWI, and field 3D/HPC remain blocked.
Run `504` validates that post-live-path guard with five passing checks: source
readiness, 24-row guard shape, empty and separated live paths, blocked receipt
and downstream states, and figure/script artifacts. Run `505`
sensitivity-hardens that validator: the exact run `503` guard passes, while
eighteen damaged states fail as expected for source readiness, row shape,
template output-local state, live-file or live-receipt promotion, path overlap,
template-under-live-root promotion, live-root damage, field-FWI or field-3D/HPC
promotion, figure damage, and missing script snapshots.
Run `506` joins the validated live-route specification and metadata-template
bundle into one collection-day return-packet intake contract. The contract has
33 files: three controlled profile repeat DZT files, three time-zero reference
DZT files, three amplitude-reference DZT files, fifteen completed global
metadata JSON files, and nine completed per-file metadata JSON files. All
twenty-four metadata templates are linked to their expected live paths but
remain output-local preparation files and do not count as live receipt. Zero
live files are present, zero files are receipt-ready, and parser/provenance,
archive promotion, field FWI, GPU work, and field 3D/HPC remain blocked until
all 33 live files pass receipt.
Run `507` validates that return-packet contract with five passing checks:
source readiness, exact 33-file/5-family/183-check shape, twenty-four linked
metadata templates that still do not count as live receipt, zero live files or
receipt-ready files, blocked parser/provenance/archive and field-FWI/3D/HPC
states, figure output, and script snapshots.
Run `508` sensitivity-hardens that validator: the exact run `506` contract
passes, while twenty-two damaged states fail as expected for source readiness,
contract row/family/count damage, metadata-template unlinking or live-receipt
promotion, live-file/receipt/parser-input promotion, parser/provenance/archive
promotion, field-FWI/3D/HPC promotion, figure damage, and missing script
snapshots. Run `509` exercises the positive receipt path for the same
33-file contract in an output-local sandbox: all nine DZT placeholders and
twenty-four metadata JSON placeholders pass all 183 receipt checks, all five
file families are complete in the sandbox, and the original live paths still
have zero files. This proves the intake mechanics can pass when the packet is
complete, but it creates no measured field evidence and does not promote live
receipt, parser/provenance/archive readiness, field FWI, or field 3D/HPC.
Run `510` validates that smoke with five passing checks: source readiness,
33-file/183-check sandbox shape, receipt-report consistency, non-evidence and
empty-live-path boundary, figure output, and script snapshots. Run `511`
sensitivity-hardens that validator: the exact run `509` smoke passes, while
twenty-two damaged states fail as expected for source readiness, packet shape,
receipt report, template/live/evidence/downstream boundary, figure damage, and
missing script snapshots. Run `512` then audits the locked live external-return
paths after the sandbox completion and confirms that all thirty-three expected
live paths remain empty, all thirty-three sandbox files remain output-local,
zero sandbox files overlap or sit under the live return root, and zero files
count as measured field evidence. Run `513` validates that guard with five
passing checks: source readiness, exact 33-row/5-family guard shape, empty live
return paths, blocked evidence and downstream states, figure output, and script
snapshots. Run `514` sensitivity-hardens the guard validator: the exact run
`512` guard passes, while twenty-four damaged states fail as expected for live
file promotion, original-live-file promotion, path overlap,
sandbox-under-live-root promotion, synthetic-boundary loss,
measured-evidence promotion, template-live promotion, live-receipt promotion,
parser/provenance/archive
promotion, field-FWI or field-3D/HPC promotion, downstream promotion, figure
damage, and missing script snapshots.
Run `515` turns the locked 33-file return-packet contract into a live delta
monitor: nine expected DZT files and twenty-four expected metadata JSON files
are checked at the live return paths across five file families. The current
state remains empty: zero of 33 live files are present, all 33 are missing, no
family is complete, and parser/provenance/archive, controlled field evidence,
field FWI, and field 3D/HPC remain blocked. Run `516` validates that monitor
with five passing checks covering exact 33-file/5-family shape, all live files
missing, blocked receipt/downstream states, figure output, and script
snapshots. Run `517` sensitivity-hardens that validator: the exact run `515`
monitor passes, while twenty-one damaged states fail as expected for source
readiness damage, row or family count damage, DZT or metadata count damage,
live-file promotion, missing-count reduction, family-complete or parser-ready
promotion, parser/provenance/archive promotion, controlled-evidence promotion,
field-FWI or field-3D/HPC promotion, downstream promotion, figure damage, and
missing script snapshots.
Run `518` converts that empty live-delta state into a collection closure
sequence: fifteen global metadata files can be prepared before collection, and
eighteen files remain measurement-dependent across three DZT-plus-metadata
groups: controlled profile repeats, time-zero references, and amplitude
references. The fifth action is the final receipt/parser/provenance/archive
gate after all thirty-three live files exist. Run `519` validates the sequence
with six passing checks covering source readiness, exact 33-file/5-action
shape, 15/18 pre-collection versus measurement-dependent accounting, blocked
receipt/downstream state, figure output, and script snapshots. Run `520`
sensitivity-hardens that validator: the exact sequence passes, while seventeen
damaged or prematurely promoted states fail as expected.
Run `521` turns the 15 global metadata placeholders into a fillability audit:
seven entries can be prepared from existing instrument, survey, material, or
target-truth records, while eight entries require setup verification or
collection-day logging. No metadata value is currently ready, no live file is
present, and live receipt, parser/provenance/archive readiness, field FWI, and
field 3D/HPC remain blocked. Run `522` validates that audit with six passing
checks covering source readiness, metadata/stage shape, fill-stage accounting,
placeholder/live state, downstream boundary, figure output, and frozen script
snapshots. Run `523` sensitivity-hardens the validator: the exact run `521`
audit passes, while fifteen damaged or prematurely promoted states fail as
expected.
Run `524` expands the nine post-measurement per-file metadata templates into a
fillability audit: three controlled-profile, three time-zero, and three
amplitude-reference metadata files require 36 total metadata fields, and all
nine remain dependent on paired measured DZT files. Zero paired DZT files, zero
metadata files, and zero field values are currently live or ready. Run `525`
validates that audit with six passing checks covering source readiness,
metadata/field/family shape, family accounting, measured-DZT dependency,
downstream boundary, figure output, and frozen script snapshots. Run `526`
sensitivity-hardens the validator: the exact run `524` audit passes, while
fourteen damaged or prematurely promoted states fail as expected.
Run `527` combines the global and per-file fillability audits into one metadata
completion route: 24 metadata files and 51 metadata values are required, with
seven record-based global metadata files, eight collection-day global metadata
files, nine measured-DZT dependencies, and 36 post-measurement per-file fields.
No metadata values, metadata live files, or paired DZT live files are currently
ready. Run `528` validates that route with six passing checks covering source
readiness, route shape, count accounting, empty current state, downstream
boundary, figure output, and frozen script snapshots. Run `529`
sensitivity-hardens the validator: the exact run `527` route passes, while
fourteen damaged or prematurely promoted states fail as expected.
Run `530` rescans the current live external return paths behind that route:
all thirty-three expected parent directories exist, but zero live files are
present or accepted. The required live files are fifteen global metadata JSON
files, nine measured DZT files, and nine per-file metadata JSON files. The
global metadata and measured-DZT actions can start on a collection workflow,
while per-file metadata remains downstream of measured DZT receipt. Live
receipt, parser/provenance/archive readiness, controlled field evidence, field
FWI, and field 3D/HPC remain blocked. Run `531` validates that rescan with six
passing checks covering source readiness, 33-item/4-action shape, empty live
paths, metadata/DZT split, downstream blocking, figure output, and frozen
script snapshots. Run `532` sensitivity-hardens the validator: the exact run
`530` state passes, while twenty damaged or prematurely promoted states fail
as expected.
Run `533` creates a non-live global metadata handoff template pack for the
fifteen global metadata JSON files. Seven templates are record-based, four are
setup-before-measurement, and four are during/after collection-session logs.
The packet leaves sixty user value fields blank, keeps all target live metadata
files absent, and does not promote live receipt, parser/provenance/archive,
field FWI, or field 3D/HPC readiness. Run `534` validates that packet with
seven passing checks covering source readiness, template/stage/action shape,
placeholder payloads, blank real fields, absent live files, downstream
blocking, figure output, and frozen script snapshots. Run `535`
sensitivity-hardens the validator: the exact non-live global metadata template
packet passes, while fourteen damaged or prematurely promoted states fail as
expected.
Run `536` creates a non-live measured-DZT collection manifest for the nine DZT
files required by the controlled field packet: three controlled profile
repeats, three time-zero references, and three amplitude references. All nine
parent directories exist, but zero live DZT files are present, zero
placeholders are created, and live receipt, parser/provenance/archive, field
FWI, and field 3D/HPC remain blocked. Run `537` validates that manifest with
six passing checks covering source readiness, nine-file/three-family/four-action
shape, three files per family, absent live DZT files, downstream blocking,
figure output, and frozen script snapshots. Run `538` sensitivity-hardens the
validator: the exact no-live-DZT manifest state passes, while fourteen damaged
or prematurely promoted states fail as expected.
Run `539` binds those nine measured-DZT live paths to the current GSSI DZT
receipt signature guard: `.DZT` extension, a `65536` byte minimum size, `ff07`
header prefix, and SHA-256 checksum recording after binary acceptance. The
current live state still has zero DZT files present, zero signature passes, and
zero observed checksums, so live receipt, parser/provenance/archive,
controlled field evidence, field FWI, and field 3D/HPC remain blocked. Run
`540` validates that boundary with seven passing checks covering source
readiness, nine-slot/three-family/four-action shape, exact DZT guard constants,
empty live-file state, blocked families/actions, downstream blocking, figure
output, and frozen script snapshots. Run `541` sensitivity-hardens the
validator: the exact run `539` state passes, while seventeen damaged or
prematurely promoted states fail as expected.
Run `542` binds the twenty-four metadata JSON live paths to a fail-closed
schema gate: fifteen global metadata files and nine per-file metadata files
must carry ninety-six real non-placeholder value fields before live receipt can
proceed. The current live state has zero metadata JSON files present, zero JSON
parseable, zero schema passes, ninety-six blank required value fields, and zero
paired DZT signature passes, so receipt, parser/provenance/archive,
controlled field evidence, field FWI, and field 3D/HPC remain blocked. Run
`543` validates that boundary with eight passing checks covering source
readiness, 24-slot/2-group/4-action shape, JSON guard contract, absent live
metadata files, blank-value and DZT-dependency blocking, downstream blocking,
figure output, and frozen script snapshots. Run `544` sensitivity-hardens the
validator: the exact run `542` state passes, while twenty damaged or
prematurely promoted states fail as expected.
Run `545` joins the measured-DZT signature gate and metadata JSON schema gate
into one integrated live-receipt frontier. The packet requires thirty-three
live items: nine measured DZT files, fifteen global metadata JSON files, and
nine per-file metadata JSON files. All thirty-three parent directories exist,
but zero live files are present, zero items are accepted, zero DZT signatures
pass, zero metadata schemas pass, and ninety-six metadata value fields remain
blank. Run `546` validates that frontier with eight passing checks. Run `547`
sensitivity-hardens the validator: the exact frontier passes, while sixteen
damaged or falsely promoted states fail with zero unexpected outcomes. Parser,
provenance, archive, controlled field evidence, field FWI, and field 3D/HPC
remain blocked until all thirty-three live receipt items pass.
Run `548` adds an output-local synthetic positive control for that integrated
frontier. It creates nine synthetic DZT files and twenty-four synthetic
metadata JSON files inside the run output folder; all thirty-three synthetic
items pass the receipt mechanics, but zero live receipt items are accepted and
no downstream field state is promoted. Run `549` validates that smoke with six
passing checks, and run `550` sensitivity-hardens the validator: the exact
synthetic smoke passes, while fifteen damaged or falsely promoted states fail
with zero unexpected outcomes. Use runs `548-550` only as mechanics coverage,
not as field evidence.
Run `551` converts the integrated live-receipt frontier and its synthetic
mechanics coverage into a six-stage collection-day packet. The thirty-three
required live items are ordered as seven pre-collection record files, four
setup-control metadata files, three controlled-profile DZT files plus three
paired metadata files, three time-zero DZT files plus three paired metadata
files, three amplitude-reference DZT files plus three paired metadata files,
and four session-closeout metadata files. The packet writes stage-only and
cumulative CSVs under the field experiment output folder and keeps zero live
items accepted. Live receipt, parser/provenance/archive promotion, controlled
field evidence, field FWI, and field 3D/HPC remain blocked until all
thirty-three live receipt items pass.
Run `552` exercises stage 1 of that packet with an output-local synthetic
metadata fill. Seven pre-collection metadata JSON files and twenty-eight
required values pass local schema checks with zero blanks, but the run accepts
zero live receipt items and does not include measured DZT files, setup
metadata, per-file metadata, or session-closeout metadata. Use it only as
stage-1 mechanics coverage; live receipt and downstream field work remain
blocked until real live files pass.
Run `553` defines the live replacement contract for that first stage. The
contract expects seven pre-collection metadata JSON files:
antenna model/serial/frequency, antenna serial, material, software version,
survey method, system, and truth source. All seven parent directories exist,
but zero stage-1 live metadata files are present. Live receipt,
parser/provenance/archive promotion, controlled field evidence, field FWI, and
field 3D/HPC remain blocked until real live files pass.
Run `554` defines the live replacement contract for stage 2, the setup
measurement controls. The contract expects four metadata JSON files for antenna
footprint and phase-center geometry, antenna ground coupling and lift
condition, antenna positioning and polarization control, and gain setting.
Together, stages `1` and `2` now require eleven metadata files and forty-four
metadata value fields before any measured trace collection stage is accepted.
All four stage-2 parent directories exist, but zero stage-2 live metadata files
are present. Live receipt, parser/provenance/archive promotion, controlled
field evidence, field FWI, and field 3D/HPC remain blocked until real live
files pass.
Run `555` defines the live replacement contract for stage 3, the controlled
profile repeats. The contract expects three measured DZT files and three
paired per-file metadata JSON files for the controlled profile repeats. This is
the first staged receipt contract that requires measured radar files rather
than only global metadata. Through stage `3`, the controlled collection now
has seventeen exact receipt items and fifty-six metadata value fields
specified. All six stage-3 parent directories exist, but zero stage-3 live
files are present. Live receipt, parser/provenance/archive promotion,
controlled field evidence, field FWI, and field 3D/HPC remain blocked until
real live files pass.
Run `556` defines the live replacement contract for stage 4, the time-zero
references. The contract expects three measured DZT files and three paired
per-file metadata JSON files for the time-zero references. Through stage `4`,
the controlled collection now has twenty-three exact receipt items and
sixty-eight metadata value fields specified. All six stage-4 parent
directories exist, but zero stage-4 live files are present. Live receipt,
parser/provenance/archive promotion, controlled field evidence, field FWI, and
field 3D/HPC remain blocked until real live files pass.
Run `557` defines the live replacement contract for stage 5, the amplitude
references. The contract expects three measured DZT files and three paired
per-file metadata JSON files for the amplitude references. Through stage `5`,
the controlled collection now has twenty-nine exact receipt items and eighty
metadata value fields specified. All six stage-5 parent directories exist, but
zero stage-5 live files are present. Live receipt, parser/provenance/archive
promotion, controlled field evidence, field FWI, and field 3D/HPC remain
blocked until real live files pass.
Run `558` defines the live replacement contract for stage 6, the session
closeout records. The contract expects four metadata JSON files for date,
notes, operator, and weather. With stage `6`, the controlled collection now has
all thirty-three receipt items and all ninety-six metadata value fields
specified across the six-stage contract. All four stage-6 parent directories
exist, but zero stage-6 live files are present. Live receipt,
parser/provenance/archive promotion, controlled field evidence, field FWI, and
field 3D/HPC remain blocked until all real live files pass.
Run `559` combines the six live receipt stages into one controlled-collection
ledger. The ledger contains thirty-three expected live files: nine measured DZT
files and twenty-four metadata JSON files carrying ninety-six required metadata
value fields. All thirty-three parent directories exist and zero live files are
present. The field receipt contract is complete as a checklist, but live
receipt, parser/provenance/archive promotion, controlled field evidence, field
FWI, and field 3D/HPC remain blocked until all thirty-three live files pass.
Run `560` adds a reusable intake gate for those thirty-three controlled
collection files. The gate can classify missing files, empty files,
extension mismatches, JSON parse failures, incomplete metadata, DZT signature
failures, and accepted files. The current state remains pre-return: all
thirty-three parent directories exist, zero live files are present, and all
ninety-six metadata value fields are still missing. Live receipt,
parser/provenance/archive promotion, controlled field evidence, field FWI, and
field 3D/HPC remain blocked until all thirty-three files pass intake.
Run `561` validates the saved run `560` intake gate from artifacts. Seven of
seven checks pass, confirming source readiness, thirty-three expected live
files, nine DZT files, twenty-four metadata JSON files, zero live files
present, preserved six-stage shape, blocked receipt acceptance, blocked
downstream states, and figure/script snapshot presence. Sensitivity hardening
remains the next step before relying on the gate for damaged future field
returns.
Run `562` sensitivity-hardens that validator. The exact run `560` intake state
passes, while eight damaged states fail as expected: source readiness damage,
missing-file count drift, file-status damage, stage-shape damage, false
receipt acceptance, downstream promotion, figure damage, and script-snapshot
damage. Use runs `560-562` as the guarded controlled-collection live receipt
intake block.
Run `563` adds the output-local positive control for the first field collection
stage. Seven pre-collection metadata JSON files pass intake with twenty-eight
observed metadata values and zero missing values. This proves the gate's
positive mechanics for stage `1` without accepting live field evidence. Live
receipt, controlled field evidence, parser/provenance/archive promotion, field
FWI, and field 3D/HPC remain blocked until real controlled-collection files
pass the guarded intake path.
Run `564` guards the next parser handoff for that stage-1 metadata positive
control. Five of five handoff checks pass: the seven metadata files are
accepted as a mechanics control, the full receipt remains incomplete at
seven of thirty-three files, all nine measured DZT files are still required,
metadata coverage remains partial at twenty-eight of ninety-six values, and
the parser remains blocked. Use run `564` to prevent the stage-1 metadata
positive control from being promoted as controlled field evidence.
Run `565` defines the controlled field trace-pairing table schema. The table
has three profile-repeat rows and eighteen columns linking each controlled
profile repeat to its matching time-zero reference, amplitude reference,
per-file metadata, and shared global metadata. The schema links nine measured
DZT files, nine per-file metadata records, and fifteen shared global metadata
records, but zero pairing rows are ready because the live measured files are
absent. Parser, provenance/archive promotion, controlled field evidence, field
FWI, and field 3D/HPC remain blocked.
Run `566` validates that trace-pairing table schema from saved outputs. Seven
of seven checks pass: source schema readiness, table shape, required links,
absent live files, preserved field receipt boundary, blocked parser/field
evidence state, and figure/script snapshot presence.
Run `567` sensitivity-hardens that validator. The exact saved state passes,
while ten damaged states fail: source flag damage, column-count damage,
pair-row damage, required-link damage, live-file promotion, ready-row
promotion, field-table filled promotion, parser promotion, figure damage, and
script-snapshot damage. Use runs `565-567` as the guarded controlled field
trace-pairing schema block.
Run `568` adds the live-return intake gate for that trace-pairing table. Each
profile repeat requires six linked row-level files: profile DZT, profile
metadata, time-zero DZT, time-zero metadata, amplitude-reference DZT, and
amplitude-reference metadata, plus the fifteen shared global metadata records.
The current state remains pre-return: zero linked files and zero shared global
metadata files are present, so zero trace-pairing rows are ready and parser,
provenance/archive promotion, controlled field evidence, field FWI, and field
3D/HPC remain blocked.
Run `569` validates that trace-pairing intake gate from saved outputs. Seven
of seven checks pass: source intake readiness, three represented rows, linked
file/global metadata count preservation, absent live state, zero ready rows,
blocked field analysis states, and figure/script snapshot presence.
Run `570` sensitivity-hardens that validator. The exact saved state passes,
while ten damaged states fail: source flag damage, row-count damage,
linked-file count damage, global-metadata count damage, live-file promotion,
ready-row promotion, field-table acceptance promotion, field FWI promotion,
figure damage, and script-snapshot damage. Use runs `568-570` as the guarded
field trace-pairing intake block.
Run `571` writes an output-local collection-day return package template for the
controlled field trace-pairing block. It lists all thirty-three required files,
writes twenty-four blank metadata JSON templates, and writes three
trace-pairing capture rows while creating no fake DZT files and accepting no
live evidence. The templates contain zero nonblank metadata values, so parser,
provenance/archive promotion, controlled field evidence, field FWI, and field
3D/HPC remain blocked until real measured files and filled metadata pass
intake.
Run `572` validates the saved run `571` template pack. Seven of seven checks
pass: source template-pack readiness, thirty-three represented package items,
twenty-four metadata templates and zero DZT placeholders, preserved six-stage
shape, blank unaccepted templates, three blocked capture rows, and
figure/script snapshot presence.
Run `573` sensitivity-hardens that validator. The exact saved run `571` state
passes, while eleven damaged states fail: source flag damage, item-count
damage, metadata-template damage, DZT-placeholder damage, stage-shape damage,
nonblank-template damage, false live acceptance, false capture readiness, field
FWI promotion, figure damage, and script-snapshot damage. Use runs `571-573` as
the guarded field collection-day template-pack block.
Run `574` reconciles that collection-day template pack against the live intake
paths. The table covers all thirty-three expected return items: twenty-four
metadata templates are present and blank, nine measured DZT files are still
absent, zero live files are present, zero items are ready for guarded live
intake, and zero items are accepted as live field evidence. Use run `574` as
the current pre-return checklist before real measured files arrive.
Run `575` validates the saved run `574` reconciliation table. Seven of seven
checks pass: source reconciliation readiness, thirty-three items and six
stages, blank metadata templates, absent live files, the current status split
of twenty-four metadata items and nine measured DZT files still awaiting
return, blocked field analysis states, and figure/script snapshot presence.
Run `576` sensitivity-hardens that validator. The exact run `574` pre-return
state passes, while thirteen damaged states fail as expected: source flag
damage, item-count damage, stage-count damage, metadata-template damage,
nonblank-template damage, live-file promotion, ready-for-intake promotion,
false acceptance, status-split damage, parser promotion, field FWI promotion,
figure damage, and script-snapshot damage. Use runs `574-576` as the guarded
field collection-day live-intake reconciliation block.
Run `577` creates the non-executed staging plan for the thirty-three controlled
collection return items. It names twenty-four filled metadata JSON files, nine
measured DZT files, thirty-three exact live-path copy commands, and five guarded
action groups: fill metadata, collect measured DZT files, preflight measured
files and metadata together, stage only real collection files, then rerun
trace-pairing and field intake gates. Blank metadata templates are not
stageable, zero commands are executed, and parser, provenance, controlled field
evidence, field FWI, and field 3D/HPC remain blocked.
Run `578` validates the saved run `577` staging plan. Seven of seven checks
pass: source staging-plan readiness, thirty-three items and six stages,
twenty-four metadata JSON and nine measured DZT requirements, non-stageable
blank templates, thirty-three non-executed commands, blocked action groups and
field-analysis states, and figure/script snapshot presence.
Run `579` sensitivity-hardens that validator. The exact run `577` non-executed
state passes, while eighteen damaged states fail as expected: source flag
damage, item-count damage, stage-count damage, metadata-count damage, DZT-count
damage, template-copy permission damage, filled-metadata promotion,
measured-DZT promotion, live-file promotion, ready-to-stage promotion,
executed-command promotion, copy-command damage, action-count damage,
ready-action promotion, field-table promotion, field FWI promotion, figure
damage, and script-snapshot damage. Use runs `577-579` as the guarded field
collection-day return staging-plan block.
Run `580` defines the preflight gate for those thirty-three controlled
collection return items. It separately checks filled metadata JSON files and
measured DZT files before staging. The current state remains pre-return: zero
candidate field files are present, zero metadata JSON files are valid, zero DZT
files are readable, zero items pass preflight, zero items are ready to stage,
and parser, provenance, controlled field evidence, field FWI, and field 3D/HPC
remain blocked.
Run `581` validates that saved preflight gate. Seven of seven checks pass:
source readiness, thirty-three items and six stages, the twenty-four metadata
JSON plus nine measured-DZT split, absent and unreadable producer field files,
zero preflight-passed or stageable items, blocked field-analysis states, and
figure/script snapshot presence.
Run `582` sensitivity-hardens that validator. The exact saved run `580` state
passes, while twenty damaged states fail as expected: source readiness damage,
item-count damage, stage-count damage, metadata-count damage, DZT-count damage,
candidate-file promotion, JSON-valid promotion, metadata-nonblank promotion,
DZT-size promotion, DZT-header promotion, preflight-passed promotion,
ready-to-stage promotion, executed-command promotion, trace-pairing promotion,
field-table promotion, controlled-evidence promotion, field FWI promotion,
field 3D/HPC promotion, figure damage, and script-snapshot damage. Use runs
`580-582` as the guarded collection-day return preflight block.
Run `583` records the claim boundary after that preflight block. Two claims
are guarded: controlled collection return requirements and the fail-closed
preflight gate. Three claims remain blocked: controlled field evidence,
parser/provenance promotion, and field FWI or field 3D/HPC. Zero candidate
files are present, zero items pass preflight, and no downstream claim is
promoted.
Run `584` validates that saved claim boundary. Seven of seven checks pass,
confirming claim counts, source preflight metrics, guarded rows, blocked rows,
downstream blocks, figure validation, and script snapshots.
Run `585` sensitivity-hardens the validator. The exact run `583` boundary
passes, while thirteen damaged states fail as expected: policy-label damage,
claim-count damage, guarded-count damage, blocked-count damage, guarded-ready
damage, blocked-ready promotion, candidate-file promotion, preflight-pass
promotion, field-evidence promotion, downstream promotion, sensitivity damage,
figure damage, and script-snapshot damage. Use runs `583-585` as the guarded
post-preflight claim-boundary block.
Run `586` splits the thirty-three controlled collection return items into
practical collection dependencies: fifteen global/setup/closeout metadata JSON
records that can be prepared separately where values are known, nine measured
DZT files that require controlled collection, and nine per-file metadata
records that must travel with those measured DZT files. The collection-coupled
stages are controlled profile repeats, time-zero references, and amplitude
references. Zero items pass preflight, zero stages are ready, and controlled
field evidence, parser/provenance promotion, field FWI, and field 3D/HPC remain
blocked until the coupled measured files and metadata pass preflight together.
Run `587` validates the saved run `586` dependency audit. Seven of seven checks
pass, confirming the six-stage shape, thirty-three return items, twenty-four
metadata JSON requirements, nine measured DZT requirements, fifteen metadata
records preparable without DZT files, nine metadata records paired with DZT
files, zero preflight-passed items, zero ready stages, zero ready action groups,
blocked field-analysis states, figure validation, and script snapshots.
Run `588` sensitivity-hardens that validator. The exact run `586` dependency
map passes, while seventeen damaged states fail as expected: policy-label
damage, stage-count damage, item-count damage, metadata-count damage, DZT-count
damage, metadata-split damage, collection-coupled-stage damage, preflight-pass
promotion, ready-stage promotion, action-readiness promotion, trace-pairing
promotion, field-evidence promotion, field FWI promotion, field 3D/HPC
promotion, figure damage, and script-snapshot damage. Use runs `586-588` as the
guarded collection-day dependency-map block.
Run `589` converts that dependency map into a per-file controlled collection
manifest. The table has thirty-three file slots across six stages: fifteen
metadata JSON records that can be prepared before collection, nine metadata JSON
records that must be completed with measured radar files, and nine measured DZT
files. Zero slots currently pass preflight, so controlled field evidence, field
FWI, and field 3D/HPC remain blocked until the paired measured files and
metadata pass together.
Run `590` validates the saved run `589` manifest. Eight of eight checks pass,
confirming the thirty-three-slot shape, six stages, twenty-four metadata JSON
slots, nine measured DZT slots, fifteen preparable metadata records, nine
metadata records paired with DZT files, nine measured DZT dependencies, eighteen
collection-coupled slots, zero preflight passes, zero ready slots, figure
validation, script snapshots, and blocked field-analysis states.
Run `591` sensitivity-hardens that validator. The exact run `589` manifest
passes, while fourteen damaged states fail as expected: policy-label damage,
slot-count damage, stage-count damage, metadata/measured-file count damage,
dependency-class count damage, collection-coupled count damage, candidate-file
promotion, preflight-pass promotion, ready-slot promotion, controlled-field
evidence promotion, field FWI promotion, field 3D/HPC promotion, figure damage,
and script-snapshot damage. Use runs `589-591` as the guarded per-file
collection-return manifest block.
Run `592` records the claim boundary after that file-slot manifest block. Two
claims are guarded: the thirty-three-slot collection manifest and the dependency
split between fifteen preparable metadata records and eighteen
collection-coupled slots. Three claims remain blocked: measured radar scan
files, paired collection metadata, and controlled field evidence or downstream
escalation. Zero slots pass preflight.
Run `593` validates the saved run `592` boundary. Seven of seven checks pass,
confirming the five-claim shape, two guarded claims, three blocked claims,
thirty-three file slots, twenty-four metadata JSON slots, nine measured DZT
slots, fifteen preparable metadata slots, eighteen collection-coupled slots,
zero preflight-passed slots, blocked field-analysis states, figure validation,
and script snapshots.
Run `594` sensitivity-hardens that validator. The exact run `592` boundary
passes, while nineteen damaged states fail as expected: policy-label damage,
claim-count damage, guarded/blocked-count damage, missing guarded claims,
file-slot-count damage, stage-shape damage, metadata/measured-file count
damage, dependency-count damage, preflight/ready-slot promotion, sensitivity
damage, blocked-support damage, field-evidence promotion, field FWI promotion,
field 3D/HPC promotion, figure damage, and script-snapshot damage. Use runs
`592-594` as the guarded file-slot manifest claim-boundary block.
Run `595` creates output-local JSON templates for the fifteen metadata records
that can be prepared before collection. The templates are distributed across
stages `1`, `2`, and `6` with shape `7;4;4`; all 75 required fill fields remain
blank, no template is written under the external field-return root, and zero
templates are accepted as live metadata. Controlled field evidence, field FWI,
and field 3D/HPC remain blocked until live metadata and measured DZT files pass
preflight.
Run `596` validates the saved run `595` template pack. Eight of eight checks
pass, confirming the fifteen-template shape, stage shape `7;4;4`, 75 blank
required fill fields, output-local placement, zero live-metadata acceptance,
blocked downstream states, figure validation, and script snapshots.
Run `597` sensitivity-hardens that validator. The exact run `595` pack passes,
while nineteen damaged states fail as expected: policy-label damage,
source-readiness damage, template row-count damage, stage-count damage,
stage-shape damage, template-file-count damage, blank-field-count damage,
payload-field damage, external-root damage, live-metadata promotion, evidence
promotion, field-FWI promotion, field-3D promotion, figure damage, and
script-snapshot damage. Use runs `595-597` as the guarded preparable metadata
template-pack block.
Run `598` creates output-local JSON templates for the nine metadata records
that must be completed together with measured DZT files. The templates cover
three controlled profile-repeat metadata records, three time-zero-reference
metadata records, and three amplitude-reference metadata records, with stage
shape `3;3;3`. All 54 required fill fields remain blank, zero paired DZT files
are present, zero paired metadata records are accepted as live evidence, and
field FWI/3D remain blocked until measured files and paired metadata pass
together.
Run `599` validates the saved run `598` paired metadata template pack. Eight of
eight checks pass, confirming the nine-template shape, stage shape `3;3;3`, 54
blank required fill fields, measured-DZT pairing identity, output-local
placement, zero paired DZT files present, zero live paired metadata acceptance,
blocked downstream states, figure validation, and script snapshots.
Run `600` sensitivity-hardens that validator. The exact run `598` pack passes,
while twenty-one damaged states fail as expected: policy-label damage,
source-readiness damage, template row-count damage, stage-count damage,
stage-shape damage, template-file-count damage, paired-DZT presence promotion,
blank-field damage, payload-field damage, payload-pairing damage,
payload-status promotion, external-root damage, live-metadata promotion,
evidence promotion, field-FWI promotion, field-3D promotion, figure damage, and
script-snapshot damage. Use runs `598-600` as the guarded paired metadata
template-pack block.
Run `601` assembles the controlled collection-day execution packet from the
guarded manifest and both metadata-template blocks. The packet contains 24
metadata templates, nine measured DZT requirements, and six action groups:
prepare global/setup/closeout metadata, collect controlled profile repeats,
collect time-zero references, collect amplitude references, place real returns
under the external field root, and run live preflight after collection. Zero
live measured DZT files and zero live paired metadata files are present, so the
packet is collection-day ready as a checklist but not field evidence.
Run `602` validates the saved run `601` collection-day execution packet. Seven
of seven checks pass, confirming the 33-slot count, 24 metadata templates, nine
measured DZT requirements, 18 required live collection-coupled returns, six
action groups, zero live measured files, zero live paired metadata files, zero
accepted action groups, blocked downstream states, figure validation, and script
snapshots.
Run `603` sensitivity-hardens that validator. The exact run `601` checklist
passes, while nineteen damaged states fail as expected: policy-label damage,
packet-readiness damage, source-readiness damage, slot-count damage,
template-count damage, measured-DZT count damage, live-return-count damage,
action-shape damage, action-count damage, live-DZT promotion, live-metadata
promotion, row-level live-file promotion, accepted-action promotion, evidence
promotion, field-FWI promotion, field-3D promotion, figure damage, and
script-snapshot damage. Use runs `601-603` as the guarded collection-day
execution packet block.
Run `604` records the claim boundary after that execution-packet block. Two
claims are guarded: the collection-day execution packet and the metadata
template split. Three claims remain blocked: measured collection returns,
controlled field evidence, and field FWI/3D escalation. The field packet still
requires nine measured DZT files and nine paired measured metadata files; zero
live measured files and zero live paired metadata files are present.
Run `605` validates the saved run `604` claim boundary. Eight of eight checks
pass, confirming the five-claim shape, two guarded claims, three blocked
claims, stable collection counts, zero live measured returns, zero accepted
action groups, blocked field evidence/downstream states, figure validation, and
script snapshots.
Run `606` sensitivity-hardens that validator. The exact run `604` boundary
passes, while eighteen damaged states fail as expected: policy-label damage,
boundary/source readiness damage, claim-shape/count damage, guarded/blocked
support damage, slot-count and live-file requirement damage, live-DZT and
live-metadata promotion, accepted-action promotion, field-evidence promotion,
field-FWI/3D promotion, figure damage, and script-snapshot damage. Use runs
`604-606` as the guarded post-execution-packet field claim-boundary block.
Run `607` refreshes the live field-return state after that claim boundary. The
33 expected return slots still contain 15 preparable metadata slots, nine
measured DZT requirements, and nine paired measured metadata requirements.
Zero of the 18 collection-coupled live files are present, zero live-state
groups are accepted, and controlled field evidence, field FWI, and field 3D/HPC
remain blocked.
Run `608` validates the saved run `607` refresh. Six of six checks pass,
confirming source readiness, six live-state rows, stable required counts,
zero live collection-coupled files, 18 missing collection-coupled files, zero
accepted groups, blocked downstream states, figure validation, and script
snapshots.
Run `609` sensitivity-hardens that validator. The exact live-file-absent state
passes, while twelve damaged states fail as expected: source-readiness damage,
row-count damage, slot-count damage, required-count damage, false live-file
presence, missing-count damage, false acceptance, field-evidence promotion,
field-FWI/3D promotion, figure damage, and script-snapshot damage. Use runs
`607-609` as the guarded field post-boundary live-state refresh block.
Run `610` creates the external field-return parent directories for the pending
controlled collection without creating any measured DZT files or metadata
files. Five directories are present after the scaffold, the 33 expected return
slots and 18 collection-coupled live file requirements are unchanged, zero live
files are present, and field evidence/FWI/3D remain blocked.
Run `611` validates the saved run `610` directory scaffold. Six of six checks
pass, confirming source readiness, five-directory shape, 33 slot preservation,
18 collection-coupled live file requirement preservation, zero files created,
zero live expected files, blocked field evidence/downstream states, figure
validation, and script snapshots.
Run `612` sensitivity-hardens that validator. The exact directory-only no-file
state passes, while fifteen damaged states fail as expected: source-readiness
damage, row-count damage, directory-count/presence damage, slot-count damage,
collection-coupled requirement damage, file/live-file promotion, accepted-group
promotion, field-evidence promotion, field-FWI/3D promotion, figure damage, and
script-snapshot damage. Use runs `610-612` as the guarded external
field-return directory scaffold block.
Run `613` refreshes the live field-return state after the external directory
scaffold. Five external return parent directories are now present, but zero of
the 18 collection-coupled live files are present, all 18 remain missing, zero
live-state groups are accepted, and controlled field evidence, field FWI, and
field 3D/HPC remain blocked.
Run `614` validates the saved run `613` refresh. Seven of seven checks pass,
confirming source readiness, directory presence, live-state row shape, stable
slot counts, zero live collection-coupled files, 18 missing collection-coupled
files, zero accepted groups, blocked downstream states, figure validation, and
script snapshots.
Run `615` sensitivity-hardens that validator. The exact directory-present,
live-file-absent state passes, while fourteen damaged states fail as expected:
source-readiness damage, directory-count/presence damage, row-count damage,
slot-count damage, collection-coupled requirement damage, live-file promotion,
missing-count damage, acceptance promotion, field-evidence promotion,
field-FWI/3D promotion, figure damage, and script-snapshot damage. Use runs
`613-615` as the guarded post-directory-scaffold field live-state refresh block.
Run `616` rolls that guarded live-state refresh into an operator-facing
collection-day action checklist. Six action groups are present, with directory
verification and downstream-hold accepted now; the 15 preparable metadata
records, nine measured DZT files, nine paired metadata files, and live preflight
remain open collection actions. Five directory parents exist, but zero of the
18 collection-coupled live files are present, so controlled field evidence,
field FWI, and field 3D/HPC remain blocked.
Run `617` validates the saved run `616` action rollup with seven of seven
checks passing: summary readiness, action-row shape, directory and slot counts,
absence of live collection-coupled files, blocked downstream states, figure
metadata, and frozen script snapshots. The validated artifact remains a
logistics checklist only, not field evidence.
Run `618` sensitivity-hardens that validator. The exact saved action rollup
passes, while eighteen damaged or prematurely promoted states fail as expected:
rollup readiness damage, action-count drift, accepted-action drift, row-count
and label damage, directory count/presence damage, slot and metadata count
damage, false live-file promotion, missing-file count damage, field-evidence,
FWI, and 3D/HPC promotion, figure damage, and script-snapshot damage. Use runs
`616-618` as the guarded collection-day action rollup block.
Run `619` audits the external return tree hygiene after the directory scaffold
and action rollup. The dataset-local pending root exists, all five leaf drop
directories are present and clean, the expected and actual directory counts
both equal eight, there are zero unexpected directories, zero files, and zero
symlinks, and the 33-slot/18 collection-coupled-slot counts are preserved. This
is a clean no-data drop-area result, not measured field evidence.
Run `620` validates the saved run `619` hygiene audit with seven of seven
checks passing: readiness, expected leaf directories, clean directory tree,
absence of live files and symlinks, slot-count preservation, downstream
blockers, figure output, and script snapshots.
Run `621` sensitivity-hardens that validator. The exact clean tree passes,
while fifteen damaged or prematurely promoted states fail as expected:
readiness damage, missing leaf directories, unexpected directories, false file
or symlink presence, slot-count damage, writable-count damage, field-evidence
promotion, field FWI promotion, field 3D promotion, GPU-priority promotion,
figure damage, and script-snapshot damage. Use runs `619-621` as the guarded
no-data external-return hygiene block.
Run `622` converts the clean external return tree and 33-slot manifest into a
nine-pair first-return watchlist. The required measured pairs are three
controlled profile repeats, three time-zero references, and three amplitude
references, each with one measured DZT file and one paired metadata JSON file.
Zero pairs are complete, zero are partial, zero DZT files are present, and zero
paired metadata files are present. The result is an intake checklist only;
controlled field evidence, field FWI, and field 3D/HPC remain blocked.
Run `623` validates that watchlist from saved artifacts with six of six checks
passing: source readiness, nine-pair shape, three controlled-profile pairs,
three time-zero pairs, three amplitude-reference pairs, zero live complete or
partial pairs, blocked downstream states, figure output, and script snapshots.
Run `624` sensitivity-hardens that validator. The exact no-data watchlist
passes, while fourteen damaged or prematurely promoted states fail as expected:
watchlist readiness, pair count, category identity, complete-pair promotion,
partial-pair promotion, false DZT or metadata presence, dirty-tree promotion,
field-evidence promotion, field FWI promotion, field 3D/HPC promotion,
GPU-priority promotion, figure damage, and script-snapshot damage. Use runs
`622-624` as the guarded first-return pair watchlist block.
Run `625` converts that nine-pair watchlist into an explicit first-return
acceptance gate. The gate is structurally ready, but zero measured pairs are
accepted: all nine DZT files and all nine paired metadata JSON files are
missing. The gate contains 108 required acceptance checks across three
controlled-profile repeats, three time-zero references, and three
amplitude-reference pairs; zero checks pass while the live files are absent.
Run `626` validates the saved acceptance gate with six of six checks passing:
source readiness, pair/category shape, missing-file blockers, acceptance-check
counts, blocked field evidence/FWI/3D states, figure output, and script
snapshots.
Run `627` sensitivity-hardens that validator. The exact nine-pair missing-file
gate passes, while fourteen damaged or prematurely promoted states fail as
expected: gate readiness damage, row removal, false pair acceptance, false DZT
or metadata presence, acceptance-check count damage, false passed-check
promotion, parent-directory damage, field-evidence promotion, field FWI
promotion, field 3D/HPC promotion, GPU-priority promotion, figure damage, and
script-snapshot damage. Use runs `625-627` as the guarded first-return pair
acceptance-gate block.
Run `628` converts the guarded first-return acceptance gate into a path-level
operator action matrix. All nine measured pairs remain open, with nine missing
DZT files and nine missing paired metadata JSON files. Parent directories are
ready for all nine pairs, but zero pairs are ready for acceptance recheck and
controlled field evidence, field FWI, and field 3D/HPC remain blocked.
Run `629` validates the saved action matrix with six of six checks passing:
source readiness, action-row shape, open artifact counts, parent/category
stability, blocked downstream claim flags, figure output, and script snapshots.
Run `630` sensitivity-hardens that validator. The exact action matrix passes,
while thirteen damaged or prematurely promoted states fail as expected: source
readiness damage, row removal, pair-order damage, false ready-for-recheck
promotion, missing-count damage, parent-directory damage, category damage,
field-evidence promotion, field FWI promotion, field 3D/HPC promotion,
GPU-priority promotion, figure damage, and script-snapshot damage. Use runs
`628-630` as the guarded first-return unblock action matrix block.
Run `631` converts that action matrix into an operator-facing file placement
packet with one row per required live file. It lists 18 missing file
instructions across nine pairs: nine DZT files and nine paired metadata JSON
files. Parent directories are ready for all 18 rows, but zero rows are ready
for acceptance recheck and controlled field evidence, field FWI, and field
3D/HPC remain blocked.
Run `632` validates the saved operator packet with five of five checks
passing: source readiness, file-instruction shape, missing-file and
parent-directory state, blocked downstream claim flags, figure output, and
script snapshots.
Run `633` sensitivity-hardens that validator. The exact operator packet
passes, while fifteen damaged or prematurely promoted states fail as expected:
packet readiness damage, row removal, pair-count damage, file-kind damage,
missing-count damage, false file presence, parent-directory damage, false
recheck readiness, command damage, field-evidence promotion, field FWI
promotion, field 3D/HPC promotion, GPU-priority promotion, figure damage, and
script-snapshot damage. Use runs `631-633` as the guarded first-return
operator-packet block.
Run `634` converts that operator packet into a fillable first-return receipt
checklist. The checklist has 18 pending rows across nine measured DZT files
and nine paired metadata JSON files. All operator initials, received
timestamps, observed SHA-256 values, observed file sizes, DZT signature checks,
and metadata-schema checks remain blank by design. Parent directories are ready
for all 18 rows, but zero rows are ready for acceptance recheck. Use run `634`
as the receipt checklist to fill after collection-day file placement; field
evidence, field FWI, and field 3D/HPC remain blocked until real files and
metadata pass the guarded acceptance gate.
Run `635` validates that receipt checklist with six of six checks passing:
receipt checklist readiness, row shape, blank pending receipt fields,
DZT/metadata check requirements, blocked downstream state, figure output, and
script snapshots. Use runs `634-635` as the guarded first-return receipt
checklist block.
Run `636` sensitivity-hardens that validator. The exact blank pending receipt
checklist passes, while eighteen damaged or prematurely promoted states fail
as expected: readiness damage, row and pair-count damage, premature receipt
field fills, false recheck readiness, DZT/metadata check-requirement damage,
parent-directory damage, acceptance-command damage, field-evidence promotion,
field-FWI promotion, field-3D/HPC promotion, GPU-priority promotion, figure
damage, and script-snapshot damage. Use runs `634-636` as the guarded
first-return receipt checklist block.
Run `637` refreshes the live file state against that receipt checklist. The
18 expected first-return files are still absent: zero live files, zero observed
SHA-256 values, zero observed file sizes, zero metadata JSON parse checks, and
zero DZT signature candidates. The receipt structure remains ready, but the
acceptance gate does not need to be rerun until real files appear and
preliminary receipt checks are populated. Controlled field evidence, field FWI,
and field 3D/HPC remain blocked.
Run `638` validates that live-state refresh with six of six checks passing:
source readiness, 18-row and nine-pair shape, current no-file state, blank
receipt observation fields, blocked downstream states, figure output, and
script snapshots.
Run `639` sensitivity-hardens that validator. The exact no-file live refresh
passes, while eighteen damaged or prematurely promoted states fail as expected:
refresh readiness damage, row removal, stage-count damage, file-kind count
damage, false live-file presence, filled observed hash or size fields,
metadata-parse promotion, DZT signature-candidate promotion, acceptance-rerun
promotion, accepted field-evidence row promotion, field-evidence promotion,
field-FWI promotion, field-3D/HPC promotion, GPU-priority promotion, figure
damage, and script-snapshot damage. Use runs `637-639` as the guarded
live-state refresh block before any first-return acceptance-gate rerun.
Run `640` converts that live-state refresh block into an explicit
first-return acceptance-rerun decision gate. The source refresh/validator/
sensitivity chain is ready, but the 18 expected first-return files remain
absent, receipt observations remain blank, and the two active blockers are
complete live-file presence plus completed preliminary receipt observations.
Acceptance-gate rerun needed and acceptance-gate rerun authorized are both
false; controlled field evidence, field FWI, and field 3D/HPC remain blocked.
Run `641` validates the saved decision gate with six of six checks passing:
source decision readiness, decision row shape and blocker counts, no-file
rerun deferral, closed action state, downstream claim blockers, figure output,
and script snapshots.
Run `642` sensitivity-hardens that validator. The exact no-file/no-rerun
decision passes, while twenty-three damaged or prematurely promoted states fail
as expected: decision/source readiness damage, row/count/blocker damage, false
live-file/hash/size/metadata/DZT/ready-row promotion, rerun-needed or
rerun-authorized promotion, command/next-action promotion, accepted-row
promotion, field-evidence/FWI/3D/GPU promotion, figure damage, and script
snapshot damage. Use runs `640-642` as the guarded no-rerun block before any
first-return acceptance-gate launch.
Run `643` converts the guarded BEM acquisition-geometry sensitivity result
into field-side collection controls. Six metadata controls are required:
Tx/Rx offset lock, antenna z/standoff lock, phase-center/track geometry,
controlled-repeat geometry consistency, reference-scan geometry matching, and
radar/metadata receipt binding. The BEM geometry block shows a `2.6214537950832346`
dB peak span across Tx/Rx offset at antenna z `0`, `0.7099232724148534` max
relative L2 across Tx/Rx offset, `0.4171376953084501` max relative L2 across
antenna z, and `0.9115427115447009` max relative L2 across the tested
geometry grid. All six controls remain pending because the nine paired
metadata JSON files and nine DZT files are still absent. Use run `643` as the
collection-day acquisition-geometry control checklist; field evidence, field
FWI, GPU escalation, and field 3D/HPC remain blocked.
Run `644` validates that acquisition-geometry control audit with six of six
checks passing: source identity, six-control shape, required metadata state,
no-file field state, BEM geometry metric basis, blocked downstream claims,
figure output, and script snapshots. Use runs `643-644` as the guarded
acquisition-geometry control checklist.
Run `645` sensitivity-hardens that validator. The exact acquisition-geometry
control state passes, while twenty-five damaged or prematurely promoted states
fail as expected: readiness damage, source-readiness damage, row removal,
control-id damage, metadata-required damage, false control satisfaction,
blocking-control demotion, metadata/DZT/pair-count damage, live-file
promotion, acceptance-rerun promotion, BEM metric damage, geometry-metadata
promotion, geometry-interpretation promotion, field-evidence/FWI/3D/GPU
promotion, figure damage, and script-snapshot damage. Use runs `643-645` as
the guarded field acquisition-geometry control checklist.
Run `646` adds a tolerance-scale collection addendum from the guarded 32-panel
BEM fine-offset result. The BEM result shows that a `5` mm Tx/Rx spacing
change remains visible after selected 32-panel checking: peak offset span
`0.6390885783938787` dB and max relative L2 `0.16690711298912922`. The field
addendum adds four blocking tolerance rows: Tx/Rx spacing measurement, Tx/Rx
spacing repeat tolerance, panel-resolution basis, and metadata binding. The
current field state remains unchanged: nine DZT files and nine paired metadata
files are still absent, so controlled field evidence, field FWI, GPU
escalation, and field 3D/HPC remain closed.
Run `647` validates that geometry-tolerance addendum with six of six checks
passing: addendum identity, tolerance-row shape, field no-file state, BEM
tolerance basis, blocked downstream scope, figure output, and script
snapshots. Use runs `646-647` as the guarded field geometry-tolerance addendum.
Run `648` sensitivity-hardens that validator. The exact addendum state passes,
while fifteen damaged or prematurely promoted states fail as expected:
addendum-readiness damage, row/item/blocking-count damage, field file-count
damage, BEM tolerance-basis damage, field-evidence/FWI/3D/GPU promotion,
figure damage, and script-snapshot damage. Use runs `646-648` as the guarded
field geometry-tolerance addendum block.

Runs `098-100` remain the previous timing-anchor conflict publication/policy
chain and source-note audit, now superseded by `102-104`.

## Policy

Field trackers are dataset-local and should not consume IDs from
`docs/experiments/`, which remains the synthetic simulation and infrastructure
tracker stream.
