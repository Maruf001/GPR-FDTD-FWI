# Experiment Category Index

## Purpose

Keep the numbered experiment archive stable while making the research branches
easier to scan.

Canonical output paths remain:

```text
outputs/experiments/NNN_run_name
```

The category view is additional:

```text
outputs/experiments/_by_category_symlinks/single_rebar/
outputs/experiments/_by_category_symlinks/multi_rebar/
outputs/experiments/_by_category_symlinks/infrastructure_smoke/
```

Those category folders contain symlinks to the canonical numbered folders.
They are for browsing and inspection only, not for writing new outputs.

## Current Categories

| Category | Canonical range | Count | Category view |
| --- | --- | ---: | --- |
| Single rebar | `001`-`062`, `107`-`109`, `111`-`113`, `116`-`121`, `123`-`124`, `126`, `128`, `131`-`132`, `135`-`140`, `142`-`143`, `145`-`148`, `150`-`151`, `153`, `155`-`157`, `159`, `162`, `164`, `166`-`167`, `169`, `172`-`173`, `175`-`176`, `178`, `181`-`182`, `184`, `186`-`187`, `190`-`192`, `194`-`196`, `198`, `200`, `421`-`424` | 126 | `outputs/experiments/_by_category_symlinks/single_rebar/` |
| Multi rebar | `063`-`106`, `110`, `114`-`115`, `203`, `206`, `208`, `210`, `216`, `219`, `221`-`223`, `225`-`227`, `230`, `233`-`235`, `239`, `242`-`244`, `247`, `250`, `252`, `254`-`255`, `258`-`259`, `261`, `265`, `267`, `269`-`270`, `274`, `276`, `278`-`279`, `281`-`283`, `285`-`288`, `290`-`292`, `294`-`296`, `298`-`300`, `302`-`304`, `306`-`309`, `311`-`313`, `315`-`318`, `320`-`322`, `324`-`326`, `328`-`330`, `332`-`334`, `336`-`340`, `342`-`348`, `350`-`355`, `357`-`359`, `361`-`363`, `365`-`367`, `369`-`371`, `373`-`375`, `377`-`380`, `382`-`384`, `386`-`389`, `391`-`393`, `395`-`398`, `400`-`402`, `404`-`407`, `409`-`411`, `413`-`417`, `425`-`433` | 200 | `outputs/experiments/_by_category_symlinks/multi_rebar/` |
| Infrastructure/reporting smoke | `122`, `125`, `127`, `129`-`130`, `133`-`134`, `141`, `144`, `149`, `152`, `154`, `158`, `160`-`161`, `163`, `165`, `168`, `170`-`171`, `174`, `177`, `179`-`180`, `183`, `185`, `188`-`189`, `193`, `197`, `199`, `201`-`202`, `204`-`205`, `207`, `209`, `211`-`215`, `217`-`218`, `220`, `224`, `228`-`229`, `231`-`232`, `236`-`238`, `240`-`241`, `245`-`246`, `248`-`249`, `251`, `253`, `256`-`257`, `260`, `262`-`264`, `266`, `268`, `271`-`273`, `275`, `277`, `280`, `284`, `289`, `293`, `297`, `301`, `305`, `310`, `314`, `319`, `323`, `327`, `331`, `335`, `341`, `349`, `356`, `360`, `364`, `368`, `372`, `376`, `381`, `385`, `390`, `394`, `399`, `403`, `408`, `412`, `418`-`420` | 107 | `outputs/experiments/_by_category_symlinks/infrastructure_smoke/` |

## Canonical Category Definitions

Single rebar:

```text
one circular steel rebar target; includes single-rebar radius/depth/location,
source-wavelet mismatch, bandwidth, W2/OT diagnostics, material tradeoff, and
single-target source-profiled polish experiments.
```

Multi rebar:

```text
multiple circular steel rebars in one model; includes common/per-target radius
profiles, per-target x/z/r coupling, confidence reports, coordinate optimizer
runs, guarded revisit runs, and objective-diagnostic matrices.
```

Infrastructure/reporting smoke:

```text
plotting, aggregation, CLI, and reporting runs that summarize physical
experiments but are not themselves a new physical inversion scene.
```

## Future Categories

Reserve new category names when the physics changes enough that direct
comparison to the current two groups would be confusing:

| Future category | Use when |
| --- | --- |
| `multi_rebar_variable_depth` | two or more rebars at different depths |
| `multi_rebar_variable_radius` | multiple rebars with intentionally different sizes |
| `shape_material_variants` | non-circular bars, corrosion, coatings, or material-property sweeps beyond the current single-rebar material diagnostic |
| `field_data_or_lab_data` | measured data or lab-calibrated synthetic data |

## Symlink Policy

The symlink view is safe as long as these rules are followed:

- Keep `outputs/experiments/NNN_run_name` as the canonical path in manifests,
  docs, scripts, and generated summaries.
- Do not move existing numbered folders into category folders.
- Do not write new experiments through `_by_category_symlinks` paths.
- Avoid recursive symlink-following commands such as `find -L`, `cp -L`, or
  `rsync -L` unless duplicate traversal is intended.

If a future tool needs category awareness, it should read an explicit category
field or this index, not infer category from a symlink path.

## Next Layout Step

For future runs, keep the flat numbered archive until `allocate_output_dir()`
and downstream docs are deliberately updated and tested for category-aware
roots. The current symlink view is enough for navigation without risking
broken references.
