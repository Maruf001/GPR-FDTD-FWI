# Experiment 78: Report Figure Caption Package

## Purpose

Assemble the report-ready figure set and draft captions from the combined
report draft, decision-figure map, and figure-readiness audit.

## 545: Report Figure Caption Package

Output:

```text
outputs/experiments/545_report_figure_caption_package
```

Command:

```text
Manual CPU-only reporting package. Figure files are symlinks to existing
validated PNG artifacts; captions are written in figure_caption_package.md.
```

Artifacts:

```text
figure_caption_package.md
figures/FIGURE_NOTES.md
figures/figure01_txrx50_coordinate_confidence.png
figures/figure02_txrx50_ambiguity_widths.png
figures/figure03_objective_summary.png
figures/figure04_source_shape_guardrail.png
figures/figure05_shallow_r4_material_uncertainty.png
figures/figure06_close50_metadata_confidence.png
figures/figure07_close50_ambiguity_widths.png
figures/supplement_s1_fitted_ringdown_objective_detail.png
run_manifest.json
```

Primary figure decisions:

```text
Figure 1: run 498 coordinate confidence, Tx/Rx=50 mm interval evidence.
Figure 2: run 498 ambiguity widths, x/z collapse and 0.25 mm radius interval.
Figure 3: run 543 compact objective summary, replacing ultra-wide objective
  plots in the report layout.
Figure 4: run 507 source-shape transfer guardrail.
Figure 5: run 201 shallow r=4 material/source uncertainty.
Figure 6: run 534 close50 metadata-repair confidence summary.
Figure 7: run 534 close50 metadata-repair ambiguity summary.
Supplement S1: run 531 fitted-ringdown objective detail audit.
```

## Interpretation

The report can now be assembled from stable package paths without copying
large PNG artifacts. The captions keep the current evidence boundaries visible:
radius results are interval-supported where margins are weak, veryhigh is only
a Tx/Rx=50 variable-depth/radius reporting diagnostic, and close50 legacy
default-offset rows remain labelled as filled metadata.

## Next Decision

Proceed to a report consistency audit: verify that the draft text, evidence
table, figure captions, and handoff matrix make the same claims with the same
run numbers and non-claims.
