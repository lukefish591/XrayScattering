from __future__ import annotations

import numpy as np


def C_self_affine(R, sigma: float, xi: float, h: float):
    R = np.asarray(R, dtype=float)
    xi = max(float(xi), 1e-12)
    return sigma**2 * np.exp(-((R / xi) ** (2.0 * h)))


def C_gaussian(R, sigma: float, xi: float):
    return C_self_affine(R, sigma, xi, h=1.0)


def C_capillary(R, B: float, xi_ir: float, a_uv: float = 1.0):
    """Log g(R) with IR cutoff. Returns (C, sigma2). Prefactors are conventional."""
    R = np.asarray(R, dtype=float)
    a_uv = max(float(a_uv), 1e-12)
    g_sat = B * np.log((xi_ir + a_uv) / a_uv)
    g = np.minimum(B * np.log((R + a_uv) / a_uv), g_sat)
    sigma2 = 0.5 * g_sat
    return sigma2 - 0.5 * g, sigma2


def correlation_function(
    family: str,
    R,
    sigma: float,
    xi: float,
    h: float,
    B: float = 8.0,
    xi_ir: float = 80.0,
    a_uv: float = 1.0,
):
    """C(R) scaled so C(0)=σ² for every family (UI always owns σ)."""
    fam = family.lower()
    R = np.asarray(R, dtype=float)
    if fam in ("self-affine", "self_affine", "selfaffine"):
        C = C_self_affine(R, 1.0, xi, h)
    elif fam in ("gaussian", "gauss"):
        C = C_gaussian(R, 1.0, xi)
    elif fam in ("capillary", "log", "capillary/log"):
        C, _ = C_capillary(R, B, xi_ir, a_uv)
        c0 = float(np.asarray(C).reshape(-1)[0]) if C.size else 1.0
        C = C / max(c0, 1e-30)
    else:
        raise ValueError(f"unknown correlation family: {family}")
    return sigma**2 * C


def g_of_C(C, sigma: float | None = None):
    C = np.asarray(C, dtype=float)
    sig2 = float(sigma**2) if sigma is not None else float(C.reshape(-1)[0])
    return 2.0 * sig2 - 2.0 * C
