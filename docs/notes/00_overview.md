# Notes Overview: Single-Rebar FWI Research (Experiments 024–058)

These notes are my own synthesis of the second research arc, written so the
next presentation can be built from a single coherent narrative rather than a
chronological list of runs.

The first presentation (`outputs/GPR_FDTD_FWI_SingleRebar_Pipeline.pptx`)
covers experiments 001–023 — the baseline single-rebar pipeline, the
depth–radius coupling, and the grid polish that fixes the exact synthetic
case. **The new deck starts where that one ended.** It tells the story of
what happens when we take that exact-synthetic success and stress-test it
against the kinds of issues that the five FWI papers warn about.

## Files in this folder

```text
docs/notes/
  00_overview.md            — this file
  01_five_papers.md         — one-section-per-paper summary tuned to our project
  02_narrative_arc.md       — the coherent research story across experiments 024–058
  03_experiment_groups.md   — experiments grouped by theme, with the figures and numbers per slide
  04_slide_plan.md          — proposed slide order for the next deck
```

## One-paragraph summary

The exact synthetic single-rebar pipeline recovers location and radius without
error and remains correct under modest noise. That made it a good platform for
asking a sharper question: **what assumption, if broken, would actually move
radius?** Five published FWI papers were used as a menu of candidate ideas.
Each candidate was tried on the same local radius problem before any optimizer
integration. The result is a hierarchy of usefulness for this specific
problem:

```text
strongly useful:
  source-wavelet profiling (amplitude, time-zero, center-frequency scale)
  frequency-weighted LS that emphasizes the higher source band
  spectrum-driven bandwidth schedule (as a seed builder)

useful as diagnostic only:
  trace-shift / NRCCC reports
  W2 trace landscape (proves the shift-convexity claim)

rejected for this problem:
  W2 / Sinkhorn as the final radius objective
  unweighted multi-frequency averaging
  free rebar conductivity / concrete εr in the radius optimizer
  full WRI and full IFWI for this stage
```

## Why this matters for the next deck

The next presentation is not a chronological run log. It is the story of
**which assumptions actually move the radius answer**, with the five papers
acting as the menu of hypotheses we tested. Each major experiment in this
arc became a yes/no decision, and the surviving pieces compose into a
production-style source-profiled radius polish (exp. 057–058) that is the
recommended pipeline going forward into multi-rebar and field-style data.
