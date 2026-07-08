# BEM Experiment 011: Colleague scarep 2D Code Audit

Date: 2026-06-23

## Purpose

Audit the colleague-provided 2D GPR-BEM/MFS code drop:

```text
/home/lam002/Downloads/scarep_gpr_forward_pkg.tar.gz
```

The goal is to decide whether the package is scientifically useful, whether it
can run in the current environment, how it compares with the current 2D
FDTD/BEM track, and whether it can be used for the 3D GPR-BEM plan.

## Output

```text
outputs/bem_experiments/011_colleague_scarep_2d_code_audit
```

Key artifacts:

```text
data/scarep_code_audit_summary.json
data/scarep_file_inventory.csv
data/scarep_static_findings.csv
data/scarep_import_checks.csv
data/scarep_bem_convergence.csv
data/scarep_smoke_checks.csv
docs/COLLEAGUE_SCAREP_2D_CODE_AUDIT.md
run_manifest.json
```

The extracted external code copy is local and ignored:

```text
outputs/bem_experiments/_external_code/scarep_gpr_forward_pkg
```

## Result

```text
tarball sha256:                 352b92c2d6026f6d0ef060b4682314e4ee14040eaafd79a570fe0cf02ebbf6d7
tar members:                    73
unsafe tar paths:               0
python files:                   55
import ready:                   true
compile ready:                  true
CuPy basic array ready:         true
CuPy linalg ready:              false
geometry smoke ready:           true
CPU BEM convergence ready:      true
best CPU BEM relative error:    0.00405772229133273
PEC BEM smoke ready:            true
GPU MFS smoke ready:            false
GPU MFS blocker:                ImportError: libcublas.so.12
direct 3D backend ready:        false
ready to replace current FDTD:  false
2D validation reference ready:  true
```

CPU Galerkin BEM convergence against the analytic dielectric-cylinder
reference:

| Panels | Relative error |
| ---: | ---: |
| 8 | 0.05542860015391826 |
| 16 | 0.015394717409198885 |
| 32 | 0.00405772229133273 |

## Interpretation

The code is not junk. It contains a real 2D TMz forward-model stack:

- Galerkin-style 2D TMz BEM classes.
- PEC cylinder and layered half-space variants.
- Meshless MFS/Trefftz scene solver.
- Analytic dielectric-cylinder reference.
- Bundled GPU Yee-FDTD baseline.

The useful part right now is the CPU/numpy Galerkin BEM path. It imports,
compiles, and shows improving agreement against an analytic cylinder reference.

The headline demo path is not ready in this environment because the GPU MFS
solver reaches `cupy.linalg.solve`, which cannot load `libcublas.so.12`.

## Decision

Keep this package as a 2D validation and algorithm reference.

Do not treat it as a direct 3D production backend. It is 2D scalar TMz, while
the project's new BEM track needs 3D Maxwell finite-rebar modeling. It should
inform the 2D side of the BEM plan and help define shared BEM/FDTD comparison
cases, while `bempp-cl` remains the practical 3D prototype backend.

## Validation

Commands run:

```text
conda run -n gpr-fdtd-fwi python -m py_compile run_colleague_scarep_2d_code_audit.py
python -m py_compile run_colleague_scarep_2d_code_audit.py
conda run -n gpr-fdtd-fwi python run_colleague_scarep_2d_code_audit.py --outdir outputs/bem_experiments/011_colleague_scarep_2d_code_audit
```

## Next Action

Use the package to reproduce a controlled 2D BEM/FDTD comparison case. The
first target should be the analytic dielectric-cylinder case because it has an
exact reference and does not require the currently broken GPU MFS path.
