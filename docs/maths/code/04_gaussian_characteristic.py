#!/usr/bin/env python3
"""Ch.3 — <exp(−i q X)> = exp(−q² σ² / 2) for Gaussian X."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(0)
sigma = 2.5
X = rng.normal(0.0, sigma, size=200_000)
q = np.linspace(-2.0, 2.0, 80)
emp = np.array([np.mean(np.exp(-1j * qq * X)) for qq in q])
thy = np.exp(-(q**2) * sigma**2 / 2)
err = np.max(np.abs(emp.real - thy))
assert err < 0.02, err
assert np.max(np.abs(emp.imag)) < 0.02

fig, ax = plt.subplots(figsize=(5.8, 3.5))
ax.plot(q, emp.real, "k", label="sample average")
ax.plot(q, thy, "C1--", label=r"$e^{-q^2\sigma^2/2}$")
ax.set_xlabel(r"$q$")
ax.set_ylabel(r"$\langle e^{-iqX}\rangle$")
ax.legend(fontsize=8)
ax.set_title("Gaussian characteristic function (PRB moment step)")
fig.tight_layout()
fig.savefig(OUT / "04_gaussian_char.png", dpi=130)
print("max |emp-thy|", float(err))
print("saved", OUT / "04_gaussian_char.png")
