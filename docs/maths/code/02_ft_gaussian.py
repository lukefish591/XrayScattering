#!/usr/bin/env python3
"""Ch.2 — numerical FT of a Gaussian vs analytic s√(2π) exp(−q²s²/2)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

s = 1.7
N = 4096
L = 40.0
x = np.linspace(-L / 2, L / 2, N, endpoint=False)
dx = x[1] - x[0]
f = np.exp(-(x**2) / (2 * s**2))
# numpy fft: q = 2π n / L, forward sum f e^{-iqx} ≈ (1/dx) but we multiply by dx
tilde = np.fft.fftshift(np.fft.fft(np.fft.ifftshift(f))) * dx
q = 2 * np.pi * np.fft.fftshift(np.fft.fftfreq(N, d=dx))
analytic = s * np.sqrt(2 * np.pi) * np.exp(-(q**2) * s**2 / 2)

rel = np.max(np.abs(tilde.real - analytic)) / np.max(analytic)
assert rel < 0.02, rel

fig, ax = plt.subplots(figsize=(5.8, 3.6))
ax.plot(q, tilde.real, "k", label="numeric FT")
ax.plot(q, analytic, "C1--", label="analytic")
ax.set_xlim(-6, 6)
ax.set_xlabel(r"$q$")
ax.set_ylabel(r"$\tilde f(q)$")
ax.set_title(rf"FT of $e^{{-x^2/(2s^2)}}$, $s={s}$")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT / "02_ft_gaussian.png", dpi=130)
print("max relative error", float(rel))
print("saved", OUT / "02_ft_gaussian.png")
