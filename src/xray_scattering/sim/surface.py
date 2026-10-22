from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from xray_scattering.sim.correlations import correlation_function
from xray_scattering.sim.params import SurfaceParams


@dataclass
class Surface:
    z: np.ndarray
    x: np.ndarray
    dx: float
    params: SurfaceParams

    @property
    def L(self) -> float:
        return float(self.params.L)

    @property
    def N(self) -> int:
        return int(self.z.shape[0])

    def C_of_R(self, R):
        p = self.params
        return correlation_function(
            p.family, R, p.sigma, p.xi, p.h, p.B, p.xi_ir, p.a_uv
        )


def generate_field(C_of_R, N: int, dx: float, rng: np.random.Generator):
    """FFT-filtered Gaussian field with target isotropic C(R)."""
    x = (np.arange(N) - N // 2) * dx
    X, Y = np.meshgrid(x, x, indexing="ij")
    R = np.hypot(X, Y)
    C = np.asarray(C_of_R(R), dtype=float)
    P = np.fft.fft2(np.fft.ifftshift(C)).real
    P = np.maximum(P, 0.0)
    noise = rng.normal(size=(N, N))
    z = np.fft.ifft2(np.fft.fft2(np.fft.ifftshift(noise)) * np.sqrt(P)).real
    c0 = float(C[N // 2, N // 2])
    z *= np.sqrt(max(c0, 1e-30)) / (z.std() + 1e-15)
    return z, x


def _place_disks(L: float, radius: float, d_min: float, rng, n_try: int = 2500):
    pts: list[np.ndarray] = []
    for _ in range(n_try):
        p = rng.uniform(0.0, L, size=2)
        if all(np.hypot(*(p - q)) >= d_min for q in pts):
            pts.append(p)
    return np.asarray(pts) if pts else np.zeros((0, 2))


def add_islands(z: np.ndarray, dx: float, p: SurfaceParams, rng: np.random.Generator):
    """Add a two-level island/pit layer. Toy structure factor, not Wu (13)."""
    N = z.shape[0]
    L = N * dx
    pts = _place_disks(L, p.island_R, p.island_d, rng)
    yy, xx = np.meshgrid(np.arange(N) * dx, np.arange(N) * dx, indexing="ij")
    mask = np.zeros((N, N), dtype=bool)
    r2 = p.island_R**2
    for px, py in pts:
        mask |= (xx - px) ** 2 + (yy - py) ** 2 <= r2
    # Target coverage φ by keeping a random subset of mask pixels if overfull.
    frac = float(mask.mean())
    if frac > 1e-12 and abs(frac - p.phi) > 0.02:
        # scale: if too much coverage, drop islands at random
        if frac > p.phi and len(pts) > 1:
            keep = max(1, int(round(len(pts) * p.phi / frac)))
            pts = pts[:keep]
            mask = np.zeros((N, N), dtype=bool)
            for px, py in pts:
                mask |= (xx - px) ** 2 + (yy - py) ** 2 <= r2
    z_out = z.copy()
    z_out[mask] += p.delta
    z_out -= z_out.mean()
    return z_out


def generate_surface(p: SurfaceParams) -> Surface:
    N = int(p.N)
    if N < 16 or N > 512:
        raise ValueError("N must be between 16 and 512")
    dx = float(p.L) / N
    rng = np.random.default_rng(int(p.seed))

    def C_of_R(R):
        return correlation_function(
            p.family, R, p.sigma, p.xi, p.h, p.B, p.xi_ir, p.a_uv
        )

    z, x = generate_field(C_of_R, N, dx, rng)
    if p.islands:
        z = add_islands(z, dx, p, rng)
    return Surface(z=z, x=x, dx=dx, params=p)
