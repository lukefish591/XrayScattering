"""Shared helpers for the intro course.

TEACHING TOYS ONLY — not the project's production models and not experimental data.
Optical constants below are the Pyrex illustration from Sinha et al., Phys. Rev. B 38,
2297 (1988), Sec. V, used so plots sit near a real θ_c. Do not treat them as this
project's sample.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

PLOTS = Path(__file__).resolve().parent / "plots"

# PRB Sec. V Pyrex illustration (λ = 1.46 Å, θ_c = 0.20°)
LAMBDA_A = 1.46
DELTA = 6.3e-6
BETA = 8.5e-8
N_PYREX = 1.0 - DELTA + 1j * BETA
THETA_C_DEG = 0.20
K = 2.0 * np.pi / LAMBDA_A  # Å^-1


def ensure_plots() -> Path:
    PLOTS.mkdir(parents=True, exist_ok=True)
    return PLOTS


def q_of(alpha, beta, k: float = K):
    """Wave-vector transfer for grazing angles from the surface (Physica Fig. 1, PRB Fig. 1)."""
    alpha = np.asarray(alpha, dtype=float)
    beta = np.asarray(beta, dtype=float)
    qx = k * (np.cos(beta) - np.cos(alpha))
    qz = k * (np.sin(alpha) + np.sin(beta))
    return qx, qz


def kz_vac(alpha, k: float = K):
    return k * np.sin(alpha)


def kz_med(alpha, n=N_PYREX, k: float = K):
    """Transmitted k_z; branch chosen so Im(kz) >= 0 (decay into the sample)."""
    val = np.sqrt(n**2 - np.cos(alpha) ** 2 + 0j) * k
    return np.where(np.imag(val) < 0, -val, val)


def fresnel_rt(alpha, n=N_PYREX, k: float = K):
    """PRB Eqs. (4.8): R = (k_z0 - k_z1)/(k_z0 + k_z1), T = 2 k_z0 / (k_z0 + k_z1)."""
    kz0 = kz_vac(alpha, k)
    kz1 = kz_med(alpha, n, k)
    denom = kz0 + kz1
    return (kz0 - kz1) / denom, 2.0 * kz0 / denom
