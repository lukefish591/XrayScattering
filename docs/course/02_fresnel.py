#!/usr/bin/env python3
"""Module 2 — n, θ_c, Fresnel R and T. TEACHING TOY (Pyrex numbers from PRB Sec. V)."""

import matplotlib.pyplot as plt
import numpy as np

from toy import DELTA, N_PYREX, PLOTS, THETA_C_DEG, ensure_plots, fresnel_rt

ensure_plots()

theta_c = np.sqrt(2 * DELTA)  # radians; PRB (4.10) θ_c ≃ √(2(1-n)) for real n
print(f"delta = {DELTA}, theta_c from sqrt(2 delta) = {np.rad2deg(theta_c):.3f} deg")
print(f"paper Sec. V quoted theta_c = {THETA_C_DEG} deg")

alpha = np.deg2rad(np.linspace(0.02, 1.2, 400))
R, T = fresnel_rt(alpha, N_PYREX)

fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6))
axes[0].semilogy(np.rad2deg(alpha), np.abs(R) ** 2, "k")
axes[0].axvline(THETA_C_DEG, color="C3", ls="--", label=r"$\theta_c$ (paper)")
axes[0].set_xlabel(r"grazing $\alpha$ (deg)")
axes[0].set_ylabel(r"$|R|^2$")
axes[0].set_title("Fresnel reflectivity (toy Pyrex n)")
axes[0].legend(fontsize=8)
axes[1].plot(np.rad2deg(alpha), np.abs(T) ** 2, "k")
axes[1].axvline(THETA_C_DEG, color="C3", ls="--")
axes[1].set_xlabel(r"grazing $\alpha$ (deg)")
axes[1].set_ylabel(r"$|T|^2$")
axes[1].set_title("Fresnel $|T|^2$ (peaks near θ_c)")
fig.tight_layout()
fig.savefig(PLOTS / "02_fresnel.png", dpi=140)
print("saved", PLOTS / "02_fresnel.png")
print("|R|^2 at 0.05 deg =", float(np.abs(fresnel_rt(np.deg2rad(0.05))[0]) ** 2))
print("|R|^2 at 0.8 deg  =", float(np.abs(fresnel_rt(np.deg2rad(0.8))[0]) ** 2))
