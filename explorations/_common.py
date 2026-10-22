"""Plot helpers for exploration scripts. Physics lives in xray_scattering.sim."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from xray_scattering.sim.correlations import C_capillary, C_gaussian, C_self_affine
from xray_scattering.sim.forward import born_s_diff, born_s_diff_qz, fresnel_rt, specular_dw
from xray_scattering.sim.hankel import hankel0
from xray_scattering.sim.surface import generate_field

from scipy.special import j1

PLOTS = Path(__file__).resolve().parent / "plots"


def ensure_plots() -> Path:
    PLOTS.mkdir(parents=True, exist_ok=True)
    return PLOTS


def style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.grid": True,
            "grid.alpha": 0.25,
            "font.size": 9,
            "axes.labelsize": 10,
            "axes.titlesize": 10,
            "legend.fontsize": 8,
        }
    )


def radial_psd_theory(q, C_of_R, Rmax: float, nR: int = 1600):
    from xray_scattering.sim.hankel import cosine_taper

    R = np.linspace(0.0, Rmax, nR)
    C = np.asarray(C_of_R(R), dtype=float) * cosine_taper(R, Rmax)
    return np.maximum(2.0 * np.pi * hankel0(q, R, C), 1e-30)


def disk_form_factor(q, radius: float):
    x = np.asarray(q, dtype=float) * radius
    out = np.empty_like(x, dtype=float)
    small = np.abs(x) < 1e-8
    out[small] = 1.0
    xs = x[~small]
    out[~small] = 2.0 * j1(xs) / xs
    return out


def s_hard_disk_hole(q, d: float, rho: float):
    q = np.asarray(q, dtype=float)
    out = np.empty_like(q, dtype=float)
    for i, qq in enumerate(q):
        if abs(qq) < 1e-10:
            out[i] = 1.0 - np.pi * rho * d**2
        else:
            out[i] = 1.0 - 2.0 * np.pi * rho * d * j1(qq * d) / qq
    return out


def save(fig, name: str) -> Path:
    ensure_plots()
    path = PLOTS / name
    fig.savefig(path, dpi=140, bbox_inches="tight")
    plt.close(fig)
    print("saved", path)
    return path


__all__ = [
    "C_capillary",
    "C_gaussian",
    "C_self_affine",
    "PLOTS",
    "born_s_diff",
    "born_s_diff_qz",
    "disk_form_factor",
    "ensure_plots",
    "fresnel_rt",
    "generate_field",
    "radial_psd_theory",
    "s_hard_disk_hole",
    "save",
    "specular_dw",
    "style",
]
