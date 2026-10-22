# Key equations (from the two context papers)

Searchable extract only. Originals: `docs/papers/PhysRevB.38.2297.pdf`, `docs/papers/1-s2.0-0378437196000854-main.pdf`. Narrative: [`paper-takeaways.md`](paper-takeaways.md).

## Kinematics (both)

<b>q</b>=<b>k</b><sub>1</sub>-<b>k</b><sub>0</sub>. Grazing incidence <i>α</i> (or θ<sub>1</sub>), exit <i>β</i> (or θ<sub>2</sub>). Specular: α=β so q<sub>x</sub>=q<sub>y</sub>=0.

X-ray scattering length b=e<sup>2</sup>/mc<sup>2</sup>; refractive index n=1-b Nλ<sup>2</sup>/2π. Critical angle θ<sub>c</sub>≃√(2(1-n)).

## PRB 1988 — Born, self-affine surface

Height–height (cutoff form used in fits):

$$
C(R)=\sigma^2\exp\big[-(R/\xi)^{2h}\big],\quad g(R)=2\sigma^2-2C(R),\quad 0<h<1.
$$

Specular (Born, with cutoff; multiplies smooth-surface Fresnel/Porod q<sub>z</sub><sup>-4</sup>):

$$
S_\mathrm{spec}(\mathbf{q})\propto q_z^{-4}\,e^{-q_z^2\sigma^2}\,\delta(q_x)\delta(q_y).
$$

Diffuse (Born):

$$
S_\mathrm{diff}(\mathbf{q})\propto q_z^{-2}e^{-q_z^2\sigma^2}\int_0^\infty R\,dR\,J_0(q_\parallel R)\big(e^{q_z^2 C(R)}-1\big).
$$

No cutoff ⇒ no <i>δ</i>-function specular. Liquid capillary: g(R)=A+B ln R; finite coherence ξ<sub>coh</sub> restores a sharp peak.

DWBA diffuse (near θ<sub>c</sub>):

$$
\left(\frac{d\sigma}{d\Omega}\right)_\mathrm{diff}\propto \lvert T(k_1)\rvert^2\lvert T(k_2)\rvert^2\,S(\mathbf{q}')
$$

with in-medium q<sub>z</sub>'. Yoneda peaks when <i>α</i> or β=θ<sub>c</sub>.

Nevot–Croce-like specular interpolation (q<sub>z</sub>σ≲ 1):

$$
\lvert R\rvert^2\simeq\lvert R_F\rvert^2\exp(-q_z q_z'\sigma^2).
$$

Use Born, not this DWBA specular formula, when q<sub>z</sub>σ≫ 1.

Porod (smooth, randomly oriented): S(q)∼ q<sup>-4</sup>. Self-affine average: S(q)∼ A<sub>1</sub> q<sup>-4</sup>+A<sub>2</sub> q<sup>-(3+h)</sup>. D<sub>s</sub>=3-h.

## Physica A 1996 — islands / pits

S=S<sub>spec</sub>+S<sub>diff</sub>. Coverage <i>φ</i>, island form factor f(q<sub>∥</sub>), in-plane structure factor S(q<sub>∥</sub>), height-distribution FT h(q<sub>z</sub>).

Fixed island thickness <i>Δ</i>: h(q<sub>z</sub>)=e<sup>-i q<sub>z</sub>Δ</sup>.

Diffuse (island term, near-specular f∼ 1):

$$
S_\mathrm{diff}\propto q_z^{-2}\,\phi\,A_0\,\lvert f(q_\parallel)\rvert^2 S(q_\parallel)\,\sin^2(q_z\Delta/2).
$$

Specular vs Fresnel (Born, no substrate):

$$
R(q_z)=R_F(q_z)\big[1-4\phi(1-\phi)\sin^2(q_z\Delta/2)\big].
$$

Island-induced q<sub>z</sub> oscillations of specular and diffuse are **out of phase** (period 2π/Δ).

Film on substrate: extra Kiessig period 2π/t. Those fringes appear in **diffuse iff conformal roughness**, and are then **in phase** with specular.

DWBA: I(<b>q</b>)=∣T(α)∣<sup>2</sup>∣T(β)∣<sup>2</sup> S(<b>q</b>).

Pit in-plane S(q<sub>∥</sub>) used in the Cu example (Wu hard-sphere 2D liquid); ∣f∣<sup>2</sup>∼ exp(-4π<sup>2</sup> R<sup>2</sup> q<sub>∥</sub><sup>2</sup>) as a Gaussian average size. Fit parameters R,d,φ<sub>0</sub> apply **inside one coherence patch**, not necessarily the whole sample.

Side peaks in q<sub>∥</sub> require neighbour spacing ≲ surface coherence (paper: typically 10–20 µm).
