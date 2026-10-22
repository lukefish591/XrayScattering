#!/usr/bin/env python3
"""Ch.4 — angular integral that defines J0."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.special import j0

OUT = Path(__file__).resolve().parent / "plots"
OUT.mkdir(parents=True, exist_ok=True)

theta = np.linspace(0, 2 * np.pi, 2000, endpoint=False)
dtheta = theta[1] - theta[0]
xs = np.linspace(0, 15, 80)
num = np.array([np.sum(np.exp(1j * x * np.cos(theta))) * dtheta / (2 * np.pi) for x in xs])
thy = j0(xs)
err = np.max(np.abs(num.real - thy))
assert err < 0.01, err
assert np.max(np.abs(num.imag)) < 0.01

fig, ax = plt.subplots(figsize=(5.8, 3.5))
ax.plot(xs, num.real, "k", label=r"$\frac{1}{2\pi}\int e^{ix\cos\theta}d\theta$")
ax.plot(xs, thy, "C1--", label=r"$J_0(x)$")
ax.set_xlabel(r"$x=q_\parallel R$")
ax.legend(fontsize=8)
ax.set_title("Hankel angular identity")
fig.tight_layout()
fig.savefig(OUT / "05_hankel_j0.png", dpi=130)
print("max |J0 error|", float(err))
print("saved", OUT / "05_hankel_j0.png")
