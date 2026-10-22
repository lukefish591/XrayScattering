#!/usr/bin/env python3
"""Module 4 — DWBA |T(α)|²|T(β)|² and Yoneda wings. TEACHING TOY, PRB Sec. IV / Fig. 6."""

import matplotlib.pyplot as plt
import numpy as np

from toy import PLOTS, THETA_C_DEG, ensure_plots, fresnel_rt

ensure_plots()

# Rocking at fixed 2θ = 1° as in PRB Fig. 6 (their calculation, not our data)
two_theta = np.deg2rad(1.0)
off = np.deg2rad(np.linspace(-0.45, 0.45, 500))
alpha = two_theta / 2 + off
beta = two_theta / 2 - off
valid = (alpha > np.deg2rad(0.03)) & (beta > np.deg2rad(0.03))
alpha, beta, off = alpha[valid], beta[valid], off[valid]

_, Ta = fresnel_rt(alpha)
_, Tb = fresnel_rt(beta)
yoneda = np.abs(Ta) ** 2 * np.abs(Tb) ** 2

# Naive Born envelope: no T factors (flat, arbitrary scale)
bornish = np.ones_like(yoneda)

fig, ax = plt.subplots(figsize=(6.2, 4.2))
ax.plot(np.rad2deg(off), yoneda / yoneda.max(), "k", label=r"DWBA factor $|T(\alpha)|^2|T(\beta)|^2$")
ax.plot(np.rad2deg(off), 0.15 * bornish, "0.6", ls="--", label="Born (no T factors), scaled")
ax.axvline(np.rad2deg(two_theta / 2) - THETA_C_DEG, color="C3", ls=":", label=r"α or β = $θ_c$")
ax.axvline(-(np.rad2deg(two_theta / 2) - THETA_C_DEG), color="C3", ls=":")
ax.set_xlabel(r"rocking offset $(\alpha-\beta)/2$ (deg)")
ax.set_ylabel("scaled factor")
ax.set_title("Toy Yoneda wings at 2θ = 1° (PRB Fig. 6 geometry)")
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(PLOTS / "04_yoneda.png", dpi=140)
print("saved", PLOTS / "04_yoneda.png")
print("theta_c deg", THETA_C_DEG)
print("max |T|^2|T|^2 at offset deg", float(np.rad2deg(off[np.argmax(yoneda)])))
