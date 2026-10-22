# 3. Random variables and random fields

A polished glass, a liquid, or a pitted copper film is not one known function z(x,y). It is a **random surface**. Scattering measures **statistics** of that surface, not a photograph of one realisation (unless the beam is coherent over the whole sample).

## 3.1 One random variable

A **random variable** <i>X</i> is a number we do not know in advance, equipped with a probability density p(x) dx=Prob(X∈[x,x+dx]). Then ∫ p(x) dx=1.

The **mean** (expectation) is ⟨X⟩=∫ x p(x) dx. The **variance** is Var(X)=⟨(X-⟨X⟩)<sup>2</sup>⟩=⟨X<sup>2</sup>⟩-⟨X⟩<sup>2</sup>. The **root-mean-square (rms)** of a zero-mean variable is σ=√(⟨X<sup>2</sup>⟩). For a surface, <i>σ</i> is the **rms roughness** of PRB.

## 3.2 The Gaussian (normal) law

$$
p(x)=\frac{1}{\sqrt{2\pi}\sigma}\,e^{-(x-m)^2/(2\sigma^2)}
$$

has mean <i>m</i> and rms <i>σ</i>. Why it appears: the **central limit theorem** — a sum of many independent small contributions is approximately Gaussian. Height <i>z</i> at a point is often the sum of many polishing / capillary / growth events.

**Characteristic function (the calculation PRB uses).** Let <i>X</i> be Gaussian, mean 0, variance σ<sup>2</sup>. Then

$$
\langle e^{-iq X}\rangle=\int dx\,p(x)e^{-iqx}=e^{-q^2\sigma^2/2}.
$$

Proof: the integral is the FT of a Gaussian (chapter 2) with s=σ. All higher moments of a zero-mean Gaussian are determined by <i>σ</i>; in particular ⟨X<sup>4</sup>⟩=3σ<sup>4</sup>.

If <i>X</i> is Gaussian, so is aX, and ⟨e<sup>-iq<sub>z</sub> X</sup>⟩= exp(-q<sub>z</sub><sup>2</sup>⟨X<sup>2</sup>⟩/2). PRB’s central assumption (after (2.4)): the **height difference** X=z(<b>R</b>')-z(<b>R</b>) is Gaussian. Then the phase factor in (2.4) averages to exp(-q<sub>z</sub><sup>2</sup> g/2) with g=⟨X<sup>2</sup>⟩. Numeric check: `code/04_gaussian_characteristic.py`.

**Uncertain:** “height differences are Gaussian” is an *assumption* (PRB: “we now make the central assumption”), not a theorem. PRB Sec. V notes that Pyrex specular falloff is *not* exactly Gaussian in w(z) at large q<sub>z</sub>. If your surface is two-level (islands), the difference is **not** Gaussian — that is why Physica uses a different average (chapter 7).

## 3.3 Random fields

A **random field** z(x,y) assigns a random variable to every point of the plane. A **realisation** is one particular surface (one AFM image). The beam, if it covers many independent patches, measures an **ensemble average** ⟨⋯⟩.

**Ergodicity (working hypothesis):** ensemble average = average over a large area of one realisation,

$$
\langle z(\mathbf{0})z(\mathbf{R})\rangle \;\approx\; \frac{1}{A}\int_A d^2R'\,z(\mathbf{R}')z(\mathbf{R}'+\mathbf{R}).
$$

You will use the right-hand side on simulated and measured maps.

## 3.4 Stationarity and isotropy

**Stationary** (statistically translation-invariant): ⟨z(<b>r</b>)z(<b>r</b>+<b>R</b>)⟩ depends only on the lag <b>R</b>, not on <b>r</b>. Then a roughness σ<sup>2</sup>=⟨z<sup>2</sup>⟩ is the same everywhere.

**Isotropic:** that lag function depends only on R=|<b>R</b>|. Then polar coordinates and J<sub>0</sub> apply (chapter 4). Anisotropic roughness (e.g. polishing scratches) needs a 2D FT without angular averaging.

PRB (2.5)–(2.6) assumes both.

## 3.5 Mean height

Shift z→ z-⟨z⟩ so that ⟨z⟩=0. A constant offset in height is a phase e<sup>-iq<sub>z</sub>⟨z⟩</sup> that cancels in ∣A∣<sup>2</sup>. Only fluctuations scatter diffusely. Specular still “sees” the mean density step (Fresnel).
