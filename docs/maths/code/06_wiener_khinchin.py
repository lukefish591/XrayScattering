#!/usr/bin/env python3
"""Ch.4 — Wiener–Khinchin on a 1D Gaussian process: PSD vs FT of C."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(1)
N = 8192
dx = 0.5
x = np.arange(N) * dx
sigma, xi = 3.0, 12.0
# Target C(Δ) = σ² exp(−|Δ|/ξ)
lag = np.fft.fftfreq(N, d=1.0 / N) * dx  # -L/2.. for ifftshift use rfft later
# Build circular C on the grid
n = np.arange(N)
dcirc = np.minimum(n, N - n) * dx
C = sigma**2 * np.exp(-dcirc / xi)
P = np.fft.fft(C).real * dx  # discrete FT ~ PSD; clip noise
P = np.maximum(P, 0.0)
# Spectral synthesis (numpy: ifft(sqrt(P/dx)*white)*N scaling)
white = rng.normal(size=N) + 1j * rng.normal(size=N)
white = (white + np.conj(np.roll(white[::-1], 1))) / 2  # not strictly needed if we take .real
z = np.fft.ifft(np.sqrt(P / dx) * rng.normal(size=N)).real
z *= sigma / (z.std() + 1e-15)

# Empirical C from one realisation (ergodic)
nmax = 400
C_emp = np.array([np.mean(z[: N - n] * z[n:]) for n in range(nmax)])
lags = np.arange(nmax) * dx
C_thy = sigma**2 * np.exp(-lags / xi)

# Periodogram vs P
q = 2 * np.pi * np.fft.fftfreq(N, d=dx)
z_q = np.fft.fft(z) * dx
P_emp = (np.abs(z_q) ** 2) / (N * dx)
# smooth periodogram
kern = np.ones(21) / 21
P_smooth = np.convolve(np.fft.fftshift(P_emp), kern, mode="same")
q_shift = np.fft.fftshift(q)
P_shift = np.fft.fftshift(P)

fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.5))
axes[0].plot(lags, C_emp, "k", label="from z(x)")
axes[0].plot(lags, C_thy, "C1--", label=r"$\sigma^2 e^{-R/\xi}$")
axes[0].set_xlabel("lag")
axes[0].set_ylabel("C")
axes[0].legend(fontsize=8)
axes[0].set_title("Correlation (Wiener–Khinchin, real space)")
axes[1].semilogy(q_shift, P_smooth, "k", label="smoothed periodogram")
axes[1].semilogy(q_shift, np.maximum(P_shift, 1e-18), "C1--", label="FT[C]")
axes[1].set_xlim(-0.8, 0.8)
axes[1].set_xlabel(r"$q$")
axes[1].set_ylabel("PSD")
axes[1].legend(fontsize=8)
axes[1].set_title("Power spectrum")
fig.tight_layout()
fig.savefig(OUT / "06_wiener_khinchin.png", dpi=130)
rel = np.max(np.abs(C_emp[:80] - C_thy[:80])) / C_thy[0]
print("C relative mismatch (small lag)", float(rel))
print("saved", OUT / "06_wiener_khinchin.png")
assert rel < 0.25, rel
