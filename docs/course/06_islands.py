#!/usr/bin/env python3
"""Module 6 — islands/pits. TEACHING TOY, Physica A Eqs. (9)–(13) / (10)–(11)."""

import matplotlib.pyplot as plt
import numpy as np

from toy import PLOTS, ensure_plots

ensure_plots()

# Toy island height and coverage. USER: your Δ, φ, R, d are unknown.
delta = 176.0  # Å, Physica PS/PMMA illustration (MW 30k), not your film
phi = 0.35
radius = 2.5e4  # Å = 2.5 µm (paper ~5 µm FWHM-ish size; toy Gaussian)
d_nn = 8.0e4  # Å = 8 µm, order of Physica pit spacing illustration
q_coh = 2 * np.pi / 1.5e5  # coherence ~15 µm → q-resolution of in-plane peaks

qz = np.linspace(0.01, 0.12, 400)
# Physica (11): R/RF = 1 - 4φ(1-φ) sin²(qz Δ/2)
mod = np.sin(qz * delta / 2.0) ** 2
r_over_rf = 1.0 - 4.0 * phi * (1.0 - phi) * mod
s_diff_qz = mod  # (10) near ql~0: diffuse ~ sin²(qz Δ/2)  — OUT OF PHASE with specular dip

qpar = np.linspace(0, 0.0012, 400)
# |f|² ~ exp(-4 π² R² q∥²)  Physica text under Eq. (6)
ff2 = np.exp(-4 * np.pi**2 * radius**2 * qpar**2)
# TOY in-plane peak at 2π/d (stand-in for Wu S(q∥) side lobes — not the Wu formula)
q0 = 2 * np.pi / d_nn
sq = 1.0 + 2.2 * np.exp(-0.5 * ((qpar - q0) / (0.35 * q0)) ** 2)
# smear as if coherence length is finite (Physica: peaks vanish if d > coherence)
sq_smeared = 1.0 + 2.2 * np.exp(-0.5 * ((qpar - q0) / np.hypot(0.35 * q0, q_coh)) ** 2)

fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.7))
axes[0].plot(qz, r_over_rf, "k", label=r"specular $R/R_F$")
axes[0].plot(qz, 0.4 + 0.6 * s_diff_qz, "C0", label=r"diffuse $\propto\sin^2(q_z\Delta/2)$ (offset)")
axes[0].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[0].set_ylabel("toy signal")
axes[0].set_title(rf"Islands Δ={delta:.0f} Å: out of phase")
axes[0].legend(fontsize=7)
axes[1].plot(qpar * 1e4, ff2 * sq, "k", label="form × S (infinite coherence)")
axes[1].plot(qpar * 1e4, ff2 * sq_smeared, "C1--", label="smeared by ~15 µm coherence")
axes[1].set_xlabel(r"$q_\parallel$ ($10^{-4}$ Å$^{-1}$)")
axes[1].set_ylabel("toy |f|² S")
axes[1].set_title("In-plane: side peak at ~2π/d")
axes[1].legend(fontsize=7)
fig.suptitle("Toy islands — Physica numbers for scale only, not your sample", fontsize=9)
fig.tight_layout()
fig.savefig(PLOTS / "06_islands.png", dpi=140)
print("saved", PLOTS / "06_islands.png")
print("period 2π/Δ =", 2 * np.pi / delta, "Å^-1")
print("q_side 2π/d =", q0, "Å^-1")
print("If island size > coherence, in-plane peak washes out (Physica MW 100k case).")
