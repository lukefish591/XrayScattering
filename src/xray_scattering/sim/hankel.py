from __future__ import annotations

import numpy as np
from scipy.special import j0


def cosine_taper(R, Rmax: float, frac: float = 0.15):
    R = np.asarray(R, dtype=float)
    edge = (1.0 - frac) * Rmax
    w = np.ones_like(R, dtype=float)
    tail = R > edge
    span = max(Rmax - edge, 1e-15)
    w[tail] = np.cos(0.5 * np.pi * np.clip((R[tail] - edge) / span, 0.0, 1.0)) ** 2
    return w


def hankel0(q, R, f_R):
    """H(q)=∫ R dR J0(q R) f(R). Vectorised over q."""
    q = np.atleast_1d(np.asarray(q, dtype=float))
    R = np.asarray(R, dtype=float)
    f_R = np.asarray(f_R, dtype=float)
    integrand = (R * f_R)[None, :] * j0(q[:, None] * R[None, :])
    return np.trapezoid(integrand, R, axis=1)


def inverse_hankel0(R, q, H_q):
    """f(R)=∫ q dq J0(q R) H(q)  (order-0 Hankel inverse of hankel0)."""
    R = np.atleast_1d(np.asarray(R, dtype=float))
    q = np.asarray(q, dtype=float)
    H_q = np.asarray(H_q, dtype=float)
    integrand = (q * H_q)[None, :] * j0(R[:, None] * q[None, :])
    return np.trapezoid(integrand, q, axis=1)
