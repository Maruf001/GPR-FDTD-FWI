"""
Build the reinforced concrete model geometry.

Constructs MaterialModel instances for:
  - Ground-truth model (air + concrete + rebars)
  - Initial model for inversion (air + homogeneous concrete, no rebars)
"""
import numpy as np
from core.materials import MaterialModel
import config as cfg


def build_rebar_model():
    """
    Construct the ground-truth model with air, concrete, and embedded rebars.

    Layout (z increasing downward, including PML padding):
        PML top
        Air layer: z = 0 to AIR_THICKNESS
        Concrete: z = AIR_THICKNESS to DOMAIN_Z
        Rebars: circular cross-sections at specified positions
        PML bottom

    Returns
    -------
    model : MaterialModel
        Complete ground-truth model with all material properties set.
    """
    model = MaterialModel(cfg.NZ, cfg.NX,
                          eps_r_bg=cfg.AIR_EPSR,
                          sigma_bg=cfg.AIR_SIGMA,
                          mu_r_bg=cfg.MU_R)

    # Concrete region: from concrete surface to bottom of domain
    iz_concrete_top = int(np.round(cfg.CONCRETE_TOP / cfg.DZ)) + cfg.NPML
    iz_bottom = cfg.NZ  # fills to bottom including bottom PML

    model.set_region(
        slice(iz_concrete_top, iz_bottom),
        slice(0, cfg.NX),
        eps_r=cfg.CONCRETE_EPSR,
        sigma=cfg.CONCRETE_SIGMA,
    )

    # Embed rebars as circular inclusions
    for z_center, x_center in cfg.REBAR_POSITIONS:
        model.add_circle(
            z_center_m=z_center,
            x_center_m=x_center,
            radius_m=cfg.REBAR_RADIUS,
            eps_r=cfg.REBAR_EPSR,
            sigma=cfg.REBAR_SIGMA,
            dz=cfg.DZ,
            dx=cfg.DX,
            npml=cfg.NPML,
        )

    return model


def build_initial_model():
    """
    Construct the initial model for inversion (no rebars).

    Same as ground-truth but with uniform concrete below the air layer.
    This is the starting point for the inversion -- the optimizer must
    recover the rebar locations from the data.

    Returns
    -------
    model : MaterialModel
    """
    model = MaterialModel(cfg.NZ, cfg.NX,
                          eps_r_bg=cfg.AIR_EPSR,
                          sigma_bg=cfg.AIR_SIGMA,
                          mu_r_bg=cfg.MU_R)

    iz_concrete_top = int(np.round(cfg.CONCRETE_TOP / cfg.DZ)) + cfg.NPML
    iz_bottom = cfg.NZ

    model.set_region(
        slice(iz_concrete_top, iz_bottom),
        slice(0, cfg.NX),
        eps_r=cfg.CONCRETE_EPSR,
        sigma=cfg.CONCRETE_SIGMA,
    )

    return model


def model_from_epsilon_r(eps_r_array):
    """
    Build a MaterialModel from a 2D epsilon_r array.

    Used during inversion: the optimizer proposes new eps_r values,
    and we need to construct a full model from them. Conductivity is
    derived from eps_r using a threshold: if eps_r < 2 (air-like),
    sigma = 0; otherwise sigma = CONCRETE_SIGMA. Rebar regions
    (eps_r close to 1 but deep in concrete) get high sigma.

    For simplicity in this implementation, we keep sigma fixed at the
    initial model values and only update eps_r.

    Parameters
    ----------
    eps_r_array : ndarray, shape (Nz, Nx)

    Returns
    -------
    model : MaterialModel
    """
    model = build_initial_model()
    model.epsilon_r = eps_r_array.copy()
    return model
