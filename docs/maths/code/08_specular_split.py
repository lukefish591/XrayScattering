#!/usr/bin/env python3
"""Ch.5–6 — why a cutoff makes a δ-like specular (integral of 1 grows with area)."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import j0

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

sigma, xi, h = 3.0, 20.0, 0.5
qz = 0.1
A_nc = 4.0  # g(R)=A R^{2h} (no cutoff); large A so the R-integral converges by R~200

def C_cut(R):
    return sigma**2 * np.exp(-((R / xi) ** (2 * h)))

Rmaxs = np.linspace(80, 500, 9)
# q∥=0: ∫ R dR <e^{-iqz Δz}>
i_cut = []
i_ncut = []
i_cut_F = []  # only F = e^{qz² C}-1
for Rm in Rmaxs:
    R = np.linspace(0, Rm, 2500)
    phase_cut = np.exp(-(qz**2) * sigma**2) * np.exp(qz**2 * C_cut(R))
    phase_ncut = np.exp(-(qz**2) * A_nc * R ** (2 * h) / 2)
    i_cut.append(np.trapezoid(R * phase_cut, R))
    i_ncut.append(np.trapezoid(R * phase_ncut, R))
    F = np.exp(qz**2 * C_cut(R)) - 1
    i_cut_F.append(np.exp(-(qz**2) * sigma**2) * np.trapezoid(R * F, R))

qpar = np.linspace(0, 0.2, 50)
R = np.linspace(0, 8 * xi, 2000)
F = np.exp(qz**2 * C_cut(R)) - 1
s_diff = np.exp(-(qz**2) * sigma**2) * np.array(
    [np.trapezoid(R * j0(q * R) * F, R) for q in qpar]
)

fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.5))
axes[0].plot(Rmaxs, i_cut, "k", label="with cutoff: grows ~ area (specular)")
axes[0].plot(Rmaxs, i_cut_F, "C1", label=r"cutoff, only $e^{q_z^2 C}-1$ (saturates)")
axes[0].plot(Rmaxs, i_ncut, "C2--", label=r"no cutoff $g=A R^{2h}$ (saturates)")
axes[0].set_xlabel("R_max (area cutoff)")
axes[0].set_ylabel(r"$\int R\,dR\,\langle e^{-iq_z\Delta z}\rangle$ at $q_\parallel=0$")
axes[0].legend(fontsize=7)
axes[1].semilogy(qpar, np.maximum(s_diff, 1e-18), "k")
axes[1].set_xlabel(r"$q_\parallel$")
axes[1].set_ylabel("diffuse kernel")
axes[1].set_title("finite ξ ⇒ smooth S_diff")
fig.tight_layout()
fig.savefig(OUT / "08_specular_split.png", dpi=130)
print("I_cut last/first", float(i_cut[-1] / i_cut[0]))
print("I_F last/first", float(i_cut_F[-1] / i_cut_F[0]))
print("I_ncut last/first", float(i_ncut[-1] / i_ncut[0]))
print("saved", OUT / "08_specular_split.png")
assert i_cut[-1] / i_cut[0] > 5
assert i_cut_F[-1] / i_cut_F[0] < 2.5  # F decays on scale ξ; first Rmax already ≳ ξ
assert i_ncut[-1] / i_ncut[0] < 2.5
