#!/usr/bin/env python3
"""Module 7 — Kiessig fringes and conformal roughness. TEACHING TOY, Physica Eqs. (12) + text."""

import matplotlib.pyplot as plt
import numpy as np

from toy import PLOTS, ensure_plots

ensure_plots()

# Toy slab on a substrate. USER: your t, densities, σ are unknown.
t = 400.0  # Å film thickness
rho_film, rho_sub = 0.4, 1.0  # relative electron density (arbitrary units)
sigma1, sigma2 = 4.0, 6.0  # Å, film/air and film/substrate rms
delta_island = 0.0  # no islands in this module

qz = np.linspace(0.04, 0.35, 500)
# Physica (12) structure (Born-like, φ=0): substrate + film terms
rough1 = np.exp(-0.5 * qz**2 * sigma1**2)
rough2 = np.exp(-0.5 * qz**2 * sigma2**2)
# |ρ_f e^{-q²σ1²/2} + (ρ_s-ρ_f) e^{i q t} e^{-q²σ2²/2}|² / qz^4
amp = rho_film * rough1 + (rho_sub - rho_film) * np.exp(1j * qz * t) * rough2
r_spec = np.abs(amp) ** 2 / qz**4

# Diffuse along qz, near ql=0:
# conformal: both interfaces share the same lateral roughness → same phase factor e^{i qz t}
# independent: no cross term → no Kiessig in diffuse
conf = (rho_film**2 * rough1**2 + (rho_sub - rho_film) ** 2 * rough2**2
        + 2 * rho_film * (rho_sub - rho_film) * rough1 * rough2 * np.cos(qz * t)) / qz**2
indep = (rho_film**2 * rough1**2 + (rho_sub - rho_film) ** 2 * rough2**2) / qz**2

fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.7))
axes[0].semilogy(qz, r_spec / r_spec.max(), "k")
axes[0].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[0].set_ylabel("toy specular (scaled)")
axes[0].set_title(fr"Kiessig period $2\pi/t$ with t={t:.0f} Å")
axes[1].plot(qz, conf / np.max(conf), "k", label="conformal: fringes IN PHASE with specular")
axes[1].plot(qz, indep / np.max(indep), "C0--", label="independent: no Kiessig in diffuse")
axes[1].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[1].set_ylabel("toy diffuse (scaled)")
axes[1].set_title("Diffuse along qz")
axes[1].legend(fontsize=7)
fig.suptitle("Toy two-interface film — not your stack", fontsize=9)
fig.tight_layout()
fig.savefig(PLOTS / "07_kiessig.png", dpi=140)
print("saved", PLOTS / "07_kiessig.png")
print("Kiessig Delta qz = 2π/t =", 2 * np.pi / t, "Å^-1")
print("delta_island unused here:", delta_island)
