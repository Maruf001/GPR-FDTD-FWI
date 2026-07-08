"""
Central configuration for all FDTD simulation and inversion parameters.

Every parameter choice is documented with its physical justification.
See docs/parameter_justifications.md for detailed derivations.
"""
import numpy as np

# ============================================================================
# Physical Constants
# ============================================================================
C0 = 299792458.0            # Speed of light in vacuum [m/s]
EPS0 = 8.854187817e-12      # Vacuum permittivity [F/m]
MU0 = 4.0 * np.pi * 1e-7   # Vacuum permeability [H/m]
ETA0 = np.sqrt(MU0 / EPS0)  # Free-space impedance [~377 Ohm]

# ============================================================================
# Material Parameters
# ============================================================================
# Concrete: typical dry concrete at ~1.5 GHz
#   eps_r = 6.0 (literature range 5-10; 6 is standard for dry concrete)
#   sigma = 0.01 S/m (low-loss dielectric)
CONCRETE_EPSR = 6.0
CONCRETE_SIGMA = 0.01       # [S/m]

# Rebar (steel): modeled as near-perfect electric conductor (PEC)
#   eps_r = 1.0 (irrelevant at this conductivity)
#   sigma = 1e7 S/m (steel conductivity; effectively PEC for FDTD)
REBAR_EPSR = 1.0
REBAR_SIGMA = 1.0e7         # [S/m]

# Air
AIR_EPSR = 1.0
AIR_SIGMA = 0.0             # [S/m]

# Relative permeability fixed at 1.0 for all materials
# Justification: at GPR frequencies, magnetic effects in concrete and
# carbon steel are negligible compared to dielectric contrast
MU_R = 1.0

# ============================================================================
# Source Parameters
# ============================================================================
# Center frequency: 1.5 GHz
# Justification: 1-2 GHz is standard for concrete inspection GPR.
# At 1.5 GHz, wavelength in concrete (eps_r=6) is ~82 mm, providing
# adequate resolution for 12 mm diameter rebars.
F_CENTER = 1.5e9            # [Hz]

# ============================================================================
# Geometry Parameters
# ============================================================================
# Domain: 500 mm wide x 300 mm deep (typical concrete slab cross-section)
DOMAIN_X = 0.50             # [m] lateral extent
DOMAIN_Z = 0.30             # [m] depth extent

# Air layer above concrete surface (antenna standoff + coupling)
AIR_THICKNESS = 0.04        # 40 mm [m]
CONCRETE_TOP = AIR_THICKNESS  # concrete surface z-coordinate

# Rebar configuration: single layer of 3 parallel rebars
# #4 rebar: nominal diameter 12.7 mm -> radius ~6 mm
REBAR_RADIUS = 0.006        # [m]
REBAR_COVER = 0.050         # 50 mm cover depth from concrete surface [m]
REBAR_SPACING = 0.100       # 100 mm center-to-center [m]
NUM_REBARS = 3

# Rebar center positions (computed)
# Centered horizontally: first rebar at x = 0.15, then +0.10 each
REBAR_POSITIONS = [
    (CONCRETE_TOP + REBAR_COVER, 0.150),  # (z, x) in meters
    (CONCRETE_TOP + REBAR_COVER, 0.250),
    (CONCRETE_TOP + REBAR_COVER, 0.350),
]

# ============================================================================
# Grid Parameters
# ============================================================================
# Wavelength calculation:
#   At f_center = 1.5 GHz, in concrete (eps_r=6):
#     lambda = c0 / (f * sqrt(eps_r)) = 3e8 / (1.5e9 * 2.449) = 81.6 mm
#   Maximum frequency content of Ricker wavelet: f_max ~ 2.5 * f_center = 3.75 GHz
#     lambda_min = c0 / (f_max * sqrt(eps_r)) = 3e8 / (3.75e9 * 2.449) = 32.7 mm
#   Rule of thumb: dx <= lambda_min / 20 = 1.63 mm
#   We use dx = 2 mm (>16 points per shortest wavelength) for a balance
#   of accuracy and computational cost. This also gives 3 cells across
#   the rebar radius (6 mm), adequate for resolving the circular geometry.
DX = 0.002                  # [m]
DZ = 0.002                  # [m] (square grid cells)

# ============================================================================
# Time Parameters
# ============================================================================
# CFL stability condition for 2D FDTD:
#   dt <= 1 / (c0 * sqrt(1/dx^2 + 1/dz^2))
#   For dx = dz: dt_max = dx / (c0 * sqrt(2)) = 4.714 ps
# Use Courant factor = 0.9 for safety margin
COURANT = 0.9
DT = COURANT * DX / (C0 * np.sqrt(2.0))  # ~4.243 ps

# Total simulation time: wave must traverse domain and return
#   Two-way travel in concrete: 2 * 0.30 / (c0/sqrt(6)) = 4.90 ns
#   Add buffer for late arrivals and PML interaction
T_MAX = 8.0e-9              # 8 ns [s]
NT = int(np.ceil(T_MAX / DT))  # ~1887 time steps

# ============================================================================
# CPML (Convolutional Perfectly Matched Layer) Parameters
# ============================================================================
# PML thickness: 15 layers * 2 mm = 30 mm
# Provides ~60 dB attenuation for normally-incident waves
NPML = 15
PML_ORDER = 3               # Polynomial grading order (cubic)
PML_KAPPA_MAX = 5.0         # Maximum coordinate stretching factor
PML_ALPHA_MAX = 0.05        # CFS-PML alpha (prevents late-time growth)
PML_SIGMA_OPT_FACTOR = 0.8  # Fraction of theoretical optimal sigma_max

# ============================================================================
# Scanning Parameters
# ============================================================================
# Scan aperture: avoid PML regions (offset by ~50 mm from edges)
SCAN_START_X = 0.050        # [m]
SCAN_END_X = 0.450          # [m]
SCAN_STEP = 0.004           # 4 mm step (2 grid cells) [m]
TX_RX_OFFSET = 0.020        # 20 mm transmitter-receiver separation [m]

# Antenna height: 2 mm above concrete surface (in air)
TX_Z = AIR_THICKNESS - 0.002  # [m]
RX_Z = AIR_THICKNESS - 0.002  # [m]

# ============================================================================
# Inversion Parameters
# ============================================================================
N_ITERATIONS = 30           # Maximum FWI iterations
TV_WEIGHT = 0.01            # Total Variation regularization weight
TV_BETA = 1e-6              # TV smoothing parameter (differentiability)
EPSR_BOUNDS = (1.0, 15.0)   # Physical bounds on relative permittivity

# For inversion, use fewer scan positions to reduce cost
INVERSION_SCAN_STEP = 0.008  # 8 mm step -> ~50 sources instead of ~100

# ============================================================================
# Computed Grid Dimensions
# ============================================================================
NX_INNER = int(np.round(DOMAIN_X / DX))   # 250
NZ_INNER = int(np.round(DOMAIN_Z / DZ))   # 150
NX = NX_INNER + 2 * NPML                   # 280
NZ = NZ_INNER + 2 * NPML                   # 180
