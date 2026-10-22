from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.ndimage import gaussian_filter1d

from xray_scattering.sim.correlations import correlation_function
from xray_scattering.sim.hankel import cosine_taper, hankel0
from xray_scattering.sim.params import MeasureParams, SurfaceParams
from xray_scattering.sim.surface import Surface


def specular_dw(qz, sigma: float):
    qz = np.asarray(qz, dtype=float)
    return np.exp(-(qz**2) * sigma**2)


def fresnel_rt(alpha, n: complex, k0: float = 1.0):
    alpha = np.asarray(alpha, dtype=float)
    kz0 = k0 * np.sin(alpha)
    val = k0 * np.sqrt(n**2 - np.cos(alpha) ** 2 + 0j)
    kz1 = np.where(np.imag(val) < 0, -val, val)
    R = (kz0 - kz1) / (kz0 + kz1 + 1e-30)
    T = 2.0 * kz0 / (kz0 + kz1 + 1e-30)
    return R, T, kz1


def _C_line(p: SurfaceParams, R, xi_coh: float | None):
    C = correlation_function(
        p.family, R, p.sigma, p.xi, p.h, p.B, p.xi_ir, p.a_uv
    )
    if xi_coh is not None and np.isfinite(xi_coh) and xi_coh > 0:
        C = C * np.exp(-np.asarray(R, dtype=float) / xi_coh)
    return C


def born_s_diff(qpar, qz: float, C_of_R, Rmax: float, nR: int = 800):
    """PRB (2.28b) kernel (constants dropped)."""
    R = np.linspace(0.0, Rmax, nR)
    C = np.asarray(C_of_R(R), dtype=float) * cosine_taper(R, Rmax)
    sigma2 = float(np.asarray(C_of_R(np.array([0.0]))).reshape(-1)[0])
    kernel = np.exp(qz**2 * C) - 1.0
    s = hankel0(qpar, R, kernel)
    pref = np.exp(-(qz**2) * sigma2) / (qz**2 + 1e-30)
    return pref * s, sigma2


def born_s_diff_qz(qz, C_of_R, Rmax: float, nR: int = 800, qpar: float = 0.0):
    R = np.linspace(0.0, Rmax, nR)
    C = np.asarray(C_of_R(R), dtype=float) * cosine_taper(R, Rmax)
    sigma2 = float(np.asarray(C_of_R(np.array([0.0]))).reshape(-1)[0])
    qz = np.atleast_1d(np.asarray(qz, dtype=float))
    out = np.empty_like(qz, dtype=float)
    qp = np.array([qpar], dtype=float)
    for i, qzi in enumerate(qz):
        kernel = np.exp(qzi**2 * C) - 1.0
        out[i] = hankel0(qp, R, kernel)[0] * np.exp(-(qzi**2) * sigma2) / (
            qzi**2 + 1e-30
        )
    return out, sigma2


def _convolve_resolution(x, y, dx_width: float):
    if dx_width <= 0 or len(x) < 4:
        return y
    step = float(np.mean(np.diff(x)))
    if step <= 0:
        return y
    sigma_bins = dx_width / (step * 2.355)  # FWHM → σ
    if sigma_bins < 0.15:
        return y
    return gaussian_filter1d(y, sigma=sigma_bins, mode="nearest")


def _rebin(x, y, pixel: float):
    if pixel <= 0 or len(x) < 4:
        return x, y
    lo, hi = float(x[0]), float(x[-1])
    n = max(8, int(round((hi - lo) / pixel)))
    edges = np.linspace(lo, hi, n + 1)
    centers = 0.5 * (edges[1:] + edges[:-1])
    idx = np.clip(np.digitize(x, edges) - 1, 0, n - 1)
    acc = np.zeros(n)
    w = np.zeros(n)
    np.add.at(acc, idx, y)
    np.add.at(w, idx, 1.0)
    w = np.maximum(w, 1.0)
    return centers, acc / w


@dataclass
class DetectorData:
    scan: str
    x: np.ndarray
    y: np.ndarray | None
    intensity: np.ndarray
    qpar: np.ndarray
    qz: np.ndarray
    xlabel: str
    ylabel: str
    title: str
    qz_ref: float


def simulate_measurement(surface: Surface, m: MeasureParams) -> DetectorData:
    """Illustrative detector. Not a measured dataset."""
    p = surface.params
    k = 2.0 * np.pi / max(m.wavelength, 1e-6)
    Rmax = max(6.0 * p.xi, 0.45 * p.L)
    nR = 640
    R = np.linspace(0.0, Rmax, nR)
    C = _C_line(p, R, m.xi_coh) * cosine_taper(R, Rmax)
    sigma = float(p.sigma)
    n = 1.0 - m.delta_n + 1j * m.beta_n
    rng = np.random.default_rng(int(m.seed) + 17)

    def s_at(qpar, qz):
        qpar = np.atleast_1d(np.asarray(qpar, dtype=float))
        qz = float(qz)
        kernel = np.exp(qz**2 * C) - 1.0
        s = hankel0(qpar, R, kernel)
        pref = np.exp(-(qz**2) * sigma**2) / (qz**2 + 1e-30)
        return np.maximum(pref * s, 0.0)

    if m.scan == "specular":
        qz = np.linspace(m.qz_min, m.qz_max, int(m.n_pts))
        alpha = np.arcsin(np.clip(qz / (2.0 * k), 1e-6, 0.999))
        rf = 1.0 / (qz**4 + 1e-30)
        spec = specular_dw(qz, sigma) * rf
        spec = spec / (spec[0] + 1e-30)
        if m.footprint:
            spec = spec / np.maximum(np.sin(alpha), 1e-3)
        spec = _convolve_resolution(qz, spec, m.dq)
        qz_b, spec = _rebin(qz, spec, m.pixel_dq)
        I = _add_noise(spec, m, rng)
        return DetectorData(
            scan="specular",
            x=qz_b,
            y=None,
            intensity=I,
            qpar=np.zeros_like(qz_b),
            qz=qz_b,
            xlabel=r"$q_z$ (Å$^{-1}$)",
            ylabel="counts (arb.)",
            title="Toy specular scan (illustrative)",
            qz_ref=float(np.median(qz_b)),
        )

    if m.scan == "qmap":
        nq = max(16, min(40, int(np.sqrt(m.n_pts))))
        qpar = np.linspace(0.0, 0.22, nq)
        qz = np.linspace(m.qz_min, m.qz_max, nq)
        img = np.empty((nq, nq), dtype=float)
        for i, qzi in enumerate(qz):
            row = s_at(qpar, qzi)
            if m.use_dwba:
                alpha = np.arcsin(np.clip(qzi / (2.0 * k), 1e-6, 0.999))
                _, T, _ = fresnel_rt(np.full_like(qpar, alpha), n)
                row = row * (np.abs(T) ** 4)
            img[i] = row
        # light q-resolution blur
        if m.dq > 0:
            step = float(qpar[1] - qpar[0])
            sig = max(m.dq / (step * 2.355), 0.0)
            if sig > 0.15:
                img = gaussian_filter1d(img, sigma=sig, axis=1, mode="nearest")
        I = _add_noise(img / (img.max() + 1e-30), m, rng)
        QPAR, QZ = np.meshgrid(qpar, qz)
        return DetectorData(
            scan="qmap",
            x=qpar,
            y=qz,
            intensity=I,
            qpar=QPAR,
            qz=QZ,
            xlabel=r"$q_\parallel$ (Å$^{-1}$)",
            ylabel=r"$q_z$ (Å$^{-1}$)",
            title="Toy 2D q-map (illustrative)",
            qz_ref=float(np.median(qz)),
        )

    # rocking / transverse at fixed 2θ ≈ 2α
    two_theta = 2.0 * np.deg2rad(m.alpha_deg)
    off = np.deg2rad(np.linspace(-m.rock_range_deg, m.rock_range_deg, int(m.n_pts)))
    alpha = two_theta / 2.0 + off
    beta = two_theta / 2.0 - off
    ok = (alpha > np.deg2rad(0.03)) & (beta > np.deg2rad(0.03))
    alpha, beta = alpha[ok], beta[ok]
    qx = k * (np.cos(beta) - np.cos(alpha))
    qz = k * (np.sin(alpha) + np.sin(beta))
    qpar = np.abs(qx)
    s = np.empty_like(qpar)
    for i, (qp, qzi) in enumerate(zip(qpar, qz)):
        s[i] = s_at([qp], qzi)[0]
    if m.use_dwba:
        _, Ta, _ = fresnel_rt(alpha, n)
        _, Tb, _ = fresnel_rt(beta, n)
        s = s * (np.abs(Ta) ** 2) * (np.abs(Tb) ** 2)
    if m.footprint:
        s = s / np.maximum(np.sin(alpha), 1e-3)
    s = _convolve_resolution(qx, s, m.dq)
    qx_b, s = _rebin(qx, s, m.pixel_dq)
    # interpolate qz onto rebinned axis
    qz_b = np.interp(qx_b, qx, qz)
    I = _add_noise(s / (s.max() + 1e-30), m, rng)
    return DetectorData(
        scan="rocking",
        x=qx_b,
        y=None,
        intensity=I,
        qpar=np.abs(qx_b),
        qz=qz_b,
        xlabel=r"$q_x$ (Å$^{-1}$)",
        ylabel="counts (arb.)",
        title="Toy rocking scan (illustrative)",
        qz_ref=float(np.median(qz_b)),
    )


def _add_noise(I, m: MeasureParams, rng: np.random.Generator):
    I = np.asarray(I, dtype=float)
    I = np.maximum(I, 0.0)
    if m.noise <= 0 and m.background <= 0:
        return I
    scale = max(m.counts_scale, 1.0)
    lam = np.maximum(I * scale + m.background, 1e-6)
    if m.noise <= 0:
        return lam / scale
    noisy = rng.poisson(lam * m.noise + 1e-6).astype(float)
    # if noise is a relative knob 0–1, mix poisson with noiseless
    return ((1.0 - min(m.noise, 1.0)) * (lam / scale) + min(m.noise, 1.0) * (noisy / scale))
