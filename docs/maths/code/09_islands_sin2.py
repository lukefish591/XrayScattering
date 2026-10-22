#!/usr/bin/env python3
"""Ch.7 — |⟨e^{-iqz z}⟩|² = 1 − 4φ(1−φ) sin²(qz Δ/2); out of phase with |1−h|²."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

phi, delta = 0.35, 176.0
qz = np.linspace(0.0, 0.12, 400)
h = np.exp(-1j * qz * delta)
mean = (1 - phi) + phi * h
spec = np.abs(mean) ** 2
spec_th = 1 - 4 * phi * (1 - phi) * np.sin(qz * delta / 2) ** 2
assert np.allclose(spec, spec_th)
one_m_h = np.abs(1 - h) ** 2
four_sin = 4 * np.sin(qz * delta / 2) ** 2
assert np.allclose(one_m_h, four_sin)

fig, ax = plt.subplots(figsize=(6.0, 3.6))
ax.plot(qz, spec, "k", label=r"specular $|\langle e^{-iq_z z}\rangle|^2$")
ax.plot(qz, one_m_h / 4, "C0", label=r"diffuse $\sin^2(q_z\Delta/2)$")
ax.set_xlabel(r"$q_z$ (Å$^{-1}$)")
ax.legend(fontsize=8)
ax.set_title("Out of phase along q_z (Physica (10)–(11))")
fig.tight_layout()
fig.savefig(OUT / "09_islands_sin2.png", dpi=130)
print("specular identity: OK")
print("period 2π/Δ", 2 * np.pi / delta)
print("saved", OUT / "09_islands_sin2.png")
