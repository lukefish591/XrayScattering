#!/usr/bin/env python3
"""Ch.8 — Fresnel R,T from k_z matching; |R|→1 below θ_c; |T| peaks near θ_c."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

delta, beta = 6.3e-6, 8.5e-8  # PRB Sec. V Pyrex illustration
n = 1.0 - delta + 1j * beta
theta_c = np.sqrt(2 * delta)
k0 = 1.0  # overall scale cancels in R,T


def kz1(alpha):
    val = k0 * np.sqrt(n**2 - np.cos(alpha) ** 2 + 0j)
    return np.where(np.imag(val) < 0, -val, val)


alpha = np.deg2rad(np.linspace(0.02, 1.0, 400))
kz0 = k0 * np.sin(alpha)
kz_m = kz1(alpha)
R = (kz0 - kz_m) / (kz0 + kz_m)
T = 2 * kz0 / (kz0 + kz_m)

# Snell form PRB (4.8)
st = np.sqrt(1 - (np.cos(alpha) / n) ** 2)
R2 = (np.sin(alpha) - n * st) / (np.sin(alpha) + n * st)
assert np.allclose(R, R2)

print("theta_c deg", float(np.rad2deg(theta_c)))
print("|R|^2 below tc", float(np.abs(R[alpha < 0.5 * theta_c])[0] ** 2))
print("|T|^2 max at deg", float(np.rad2deg(alpha[np.argmax(np.abs(T) ** 2)])))

fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.5))
axes[0].semilogy(np.rad2deg(alpha), np.abs(R) ** 2, "k")
axes[0].axvline(np.rad2deg(theta_c), color="C3", ls="--")
axes[0].set_xlabel(r"$\alpha$ (deg)")
axes[0].set_ylabel(r"$|R|^2$")
axes[1].plot(np.rad2deg(alpha), np.abs(T) ** 2, "k")
axes[1].axvline(np.rad2deg(theta_c), color="C3", ls="--")
axes[1].set_xlabel(r"$\alpha$ (deg)")
axes[1].set_ylabel(r"$|T|^2$")
fig.suptitle("Toy Pyrex n from PRB Sec. V — not your sample", fontsize=9)
fig.tight_layout()
fig.savefig(OUT / "10_fresnel.png", dpi=130)
print("saved", OUT / "10_fresnel.png")
assert np.abs(R[alpha < 0.4 * theta_c][0]) ** 2 > 0.9
