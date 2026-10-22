# 7. Islands and pits (Physica A 1996)

A two-level surface (islands of height <i>Δ</i>, or pits of depth <i>Δ</i>) is **not** a Gaussian random field. The PRB average ⟨e<sup>-iq<sub>z</sub> X</sup>⟩=e<sup>-q<sub>z</sub><sup>2</sup> g/2</sup> is the wrong tool. Physica computes the phase average from coverage and in-plane statistics, and *cites the PRB only for DWBA / continuous roughness*.

## 7.1 Height distribution h(q<sub>z</sub>)

Let h<sub>pdf</sub>(ζ) dζ be the probability that a covering island (or pit) has height (depth) <i>ζ</i>. Physica (2) writes its FT

$$
h(q_z)=\int_{-\infty}^{\infty}d\zeta\,h_{\mathrm{pdf}}(\zeta)\,e^{-iq_z\zeta}.
$$

If every island has the **same** thickness <i>Δ</i>, h<sub>pdf</sub>(ζ)=δ(ζ-Δ) and h(q<sub>z</sub>)=e<sup>-iq<sub>z</sub>Δ</sup> (Physica (9)). Pits: Δ<0 or h<sub>pdf</sub> supported on negative <i>ζ</i>.

## 7.2 Coverage and the specular average

Let <i>φ</i> be the **area fraction** covered by islands (so 1-φ is the bare film). Ignore for one moment in-plane correlations, and treat the height at a random surface point as

$$
z=\begin{cases}\Delta & \text{with probability }\phi,\\ 0 & \text{with probability }1-\phi.\end{cases}
$$

The mean phase factor is

$$
\bigl\langle e^{-iq_z z}\bigr\rangle=(1-\phi)+\phi\,h(q_z).
$$

Specular intensity follows the **mean** (coherent) field, Physica (5):

$$
S_{\mathrm{spec}}\propto\frac{(\Delta\rho)^2}{q_z^2}A\,(2\pi)^2\delta(q_x)\delta(q_y)\,\bigl\lvert(1-\phi)+\phi\,h(q_z)\bigr\rvert^2.
$$

For h=e<sup>-iq<sub>z</sub>Δ</sup>,

$$
\begin{aligned}
\bigl\lvert(1-\phi)+\phi e^{-iq_z\Delta}\bigr\rvert^2
&=(1-\phi)^2+\phi^2+2\phi(1-\phi)\cos(q_z\Delta)\\
&=1-2\phi(1-\phi)\bigl(1-\cos(q_z\Delta)\bigr)\\
&=1-4\phi(1-\phi)\sin^2(q_z\Delta/2),
\end{aligned}
$$

using 1- cosθ=2 sin<sup>2</sup>(θ/2). Dividing by the Fresnel/Born smooth reflectivity R<sub>F</sub>∝(Δρ)<sup>2</sup>/q<sub>z</sub><sup>4</sup> produces Physica (11):

$$
R(q_z)=R_F(q_z)\bigl[1-4\phi(1-\phi)\sin^2(q_z\Delta/2)\bigr].
$$

Oscillation period in q<sub>z</sub>: Δ q<sub>z</sub>=2π/Δ.

## 7.3 Diffuse: form factor, structure factor, sin<sup>2</sup>

Intensity also has a **variance** piece: two points <b>R</b>,<b>R</b>' may lie in the same island, in two different islands, or on the bare film. After subtracting the mean (which already went to specular), Physica (6) groups the remainder as

$$
S_{\mathrm{diff}}\propto\frac{(\Delta\rho)^2}{q_z^2}\,\phi A A_0\,\lvert f(q_\parallel)\rvert^2
\Bigl\{S(q_\parallel)\lvert 1-h(q_z)\rvert^2+\bigl(1-\lvert h(q_z)\rvert^2\bigr)\Bigr\}.
$$

**Form factor** (Physica (3)): for one island occupying area A<sub>0</sub>,

$$
f(\mathbf{q}_\parallel)=\frac{1}{A_0}\int_{\text{island}}d^2r\,e^{-i\mathbf{q}_\parallel\cdot\mathbf{r}}.
$$

Shift theorem: an island at <b>r</b><sub>n</sub> multiplies <i>f</i> by e<sup>-i<b>q</b><sub>∥</sub>·<b>r</b><sub>n</sub></sup>. A disk of radius <i>R</i> has f∝ 2J<sub>1</sub>(q<sub>∥</sub> R)/(q<sub>∥</sub> R); Physica’s fits instead used a Gaussian average ∣f∣<sup>2</sup>∼ e<sup>-4π<sup>2</sup> R<sup>2</sup> q<sub>∥</sub><sup>2</sup></sup>.

**Structure factor** of centres (Physica (7)):

$$
S(\mathbf{q}_\parallel)=\frac{1}{N}\Bigl\langle\sum_{n,m}e^{-i\mathbf{q}_\parallel\cdot(\mathbf{r}_n-\mathbf{r}_m)}\Bigr\rangle
-\text{(mean-density }\delta(\mathbf{q}_\parallel)\text{ piece)}.
$$

The subtracted <i>δ</i> is the average island density, already in S<sub>spec</sub>.

**Pair correlation.** In a 2D liquid of areal density ρ<sub>N</sub>=N/A, the **pair correlation** g<sub>pair</sub>(r) is defined so that ρ<sub>N</sub> g<sub>pair</sub>(r) d<sup>2</sup>r is the expected number of other islands in d<sup>2</sup>r at distance <i>r</i>. Then (standard liquid theory; Physica points to Chen / Wu)

$$
S(\mathbf{q}_\parallel)=1+\rho_N\int d^2r\,\bigl(g_{\mathrm{pair}}(r)-1\bigr)e^{-i\mathbf{q}_\parallel\cdot\mathbf{r}}.
$$

**Uncertain:** Physica (13) quotes Wu’s 2D hard-sphere formula, but the PDF OCR of that equation is unreadable. Use the S=1+ρ FT[g<sub>pair</sub>-1] definition, or a toy peak at q<sub>∥</sub>=2π/d, until you have Wu’s paper in a clean copy. Do not code (13) from the garbled text.

**Fixed <i>Δ</i>, near-specular ∣f∣∼ 1:** ∣1-e<sup>-iq<sub>z</sub>Δ</sup>∣<sup>2</sup>=4 sin<sup>2</sup>(q<sub>z</sub>Δ/2). Physica (10) absorbs the 4 into the prefactor 4(Δρ)<sup>2</sup>/q<sub>z</sub><sup>2</sup>:

$$
S_{\mathrm{diff}}\propto q_z^{-2}\,\phi A_0\lvert f\rvert^2 S(q_\parallel)\sin^2(q_z\Delta/2).
$$

Specular ∝ 1-4φ(1-φ) sin<sup>2</sup>(q<sub>z</sub>Δ/2) **dips** when sin<sup>2</sup>=1; diffuse **peaks** there. They are **out of phase** along q<sub>z</sub>. Numeric: `code/09_islands_sin2.py`.

## 7.4 Coherence

The ⟨∑<sub>n,m</sub>e<sup>-iq·(r<sub>n</sub>-r<sub>m</sub>)</sup>⟩ only includes pairs inside **one coherent patch**. Physica: synchrotron surface coherence typically 10–20 µm. If island spacing ≫ξ<sub>coh</sub>, S(q<sub>∥</sub>) has no side peaks (their MW 100k PS/PMMA, ~25 µm islands). Fitted φ<sub>0</sub> is a **local** density, not the global <i>φ</i>.
