#!/usr/bin/env python3
"""Module 3 — specular ridge vs diffuse. TEACHING TOY, PRB Sec. II split S = S_spec + S_diff."""

import matplotlib.pyplot as plt
import numpy as np

from toy import PLOTS, ensure_plots, q_of

ensure_plots()

# Toy rms roughness (Å). USER: your σ is unknown until you specify it.
sigma = 7.6  # PRB Sec. V Pyrex fit, illustration only
qz = np.linspace(0.03, 0.45, 250)
rf = 1.0 / qz**4  # Born smooth-surface envelope, PRB (2.15)
r_spec = rf * np.exp(-(qz**2) * sigma**2)  # PRB (2.28a)

# Transverse cut at fixed qz: delta-like specular + broader diffuse (schematic)
qx = np.linspace(-0.004, 0.004, 400)
qz0 = 0.15
# resolution-broadened "specular" Gaussian vs slower diffuse (not a fit)
spec_peak = np.exp(-(qx / 1.5e-4) ** 2)
diff_peak = 0.08 * np.exp(-np.abs(qx) / 8e-4) / (1 + (qx / 5e-4) ** 2)

fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))
axes[0].semilogy(qz, rf / rf[0], "0.6", label=r"smooth Born $\sim q_z^{-4}$")
axes[0].semilogy(qz, r_spec / rf[0], "k", label=fr"times $e^{{-q_z^2\sigma^2}}$, σ={sigma} Å")
axes[0].set_xlabel(r"$q_z$ (Å$^{-1}$)")
axes[0].set_ylabel("toy specular (scaled)")
axes[0].set_title("Specular loses intensity as σ grows")
axes[0].legend(fontsize=8)
axes[1].plot(qx, spec_peak, "k", label="specular (resolution)")
axes[1].plot(qx, spec_peak + diff_peak, "C0", label="plus diffuse")
axes[1].set_xlabel(r"$q_x$ (Å$^{-1}$) at fixed $q_z$")
axes[1].set_ylabel("toy intensity")
axes[1].set_title("Rocking cut: ridge + wings")
axes[1].legend(fontsize=8)
fig.suptitle("Toy — not your measurement", fontsize=9)
fig.tight_layout()
fig.savefig(PLOTS / "03_spec_diff.png", dpi=140)
print("saved", PLOTS / "03_spec_diff.png")
print("qx,qz at α=β=0.4°", q_of(np.deg2rad(0.4), np.deg2rad(0.4)))
print("At qz=0.2, DW factor exp(-qz^2 σ^2) =", np.exp(-(0.2**2) * sigma**2))
