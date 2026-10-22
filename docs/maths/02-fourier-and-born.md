# 2. Fourier transforms and the Born approximation

## 2.1 What a Fourier transform is

A function f(x) of a real variable can be rebuilt as a sum of complex waves e<sup>iqx</sup> of different spatial frequencies <i>q</i>. The **Fourier transform** (FT) is the recipe for the weights:

$$
\tilde f(q)=\int_{-\infty}^{\infty} dx\, f(x)\,e^{-iqx},\qquad
f(x)=\frac{1}{2\pi}\int_{-\infty}^{\infty} dq\, \tilde f(q)\,e^{iqx}.
$$

Read the first formula as: at each <i>q</i>, multiply <i>f</i> by a wave of wavelength 2π/q and integrate. Where <i>f</i> oscillates in step with that wave, the integral is large; where it is out of step, the integral cancels.

**Worked example (Gaussian).** Let f(x)=e<sup>-x<sup>2</sup>/(2s<sup>2</sup>)</sup> with s>0. Completing the square in the exponent -x<sup>2</sup>/(2s<sup>2</sup>)-iqx=-(x+iqs<sup>2</sup>)<sup>2</sup>/(2s<sup>2</sup>)-q<sup>2</sup> s<sup>2</sup>/2 and using ∫ e<sup>-u<sup>2</sup>/(2s<sup>2</sup>)</sup>du=s√(2π) gives

$$
\tilde f(q)=s\sqrt{2\pi}\,e^{-q^2 s^2/2}.
$$

A wide bump in <i>x</i> (large <i>s</i>) is a *narrow* bump in <i>q</i>. That is the uncertainty relation you will meet as “large islands ⇒ sharp peaks in q<sub>∥</sub>”. Numeric check: `code/02_ft_gaussian.py`.

## 2.2 Properties used in scattering

Let ℱ[f]=f̃.

| Property | Statement | Use here |
| --- | --- | --- |
| Linearity | ℱ[af+bg]=af̃+bg̃ | Superposition of scatterers |
| Shift | ℱ[f(x-x<sub>0</sub>)]=e<sup>-iq x<sub>0</sub></sup>f̃(q) | An island centred at <b>r</b><sub>n</sub> |
| Scaling | ℱ[f(x/a)]=∣a∣ f̃(aq) | Size ↔ peak width |
| Parseval | ∫ ∣f∣<sup>2</sup> dx=(2π)<sup>-1</sup>∫∣f̃∣<sup>2</sup> dq | Intensity accounting |
| Convolution | (f∗g)(x)=∫ dx' f(x')g(x-x'), ℱ[f∗g]=f̃ g̃ | Resolution smearing (ch. 8) |
| Dual convolution | ℱ[fg]=(2π)<sup>-1</sup>f̃ ∗ g̃ | Product of density and window |

**Convolution theorem, one line:** blurring a function in real space *multiplies* FTs; multiplying in real space *blurs* FTs. Instrument resolution is a blur in <i>q</i>, hence a product of the sample’s S(<b>q</b>) with a resolution function.

Proof sketch of ℱ[f∗g]=f̃g̃: write the double integral, change variable u=x-x', and the x' and <i>u</i> integrals factor.

In <i>d</i> dimensions replace dx by d<sup>d</sup> r and 2π by (2π)<sup>d</sup>.

## 2.3 Why a scattering amplitude is an FT of density

**Single scattering (Born, first principles).** An incident plane wave e<sup>i<b>k</b><sub>0</sub>·<b>r</b></sup> hits a small element of volume dV at <b>r</b> that contains scattering-length density ρ(<b>r</b>). (For X-rays ρ=r<sub>e</sub> n<sub>e</sub>, with r<sub>e</sub>=e<sup>2</sup>/mc<sup>2</sup> the Thomson length and n<sub>e</sub> the electron number density. For neutrons ρ=b n<sub>nuclei</sub>. PRB calls the scattering length <i>b</i> and the number density <i>N</i>.)

That element radiates a spherical wavelet. Far away, in a direction with wave vector <b>k</b><sub>1</sub>, the **extra phase** of that wavelet relative to a wavelet from the origin is

$$
(\mathbf{k}_0-\mathbf{k}_1)\cdot\mathbf{r}=-\mathbf{q}\cdot\mathbf{r},\qquad\mathbf{q}=\mathbf{k}_1-\mathbf{k}_0.
$$

Geometry: the incident wave has already accumulated <b>k</b><sub>0</sub>·<b>r</b> to reach <b>r</b>; the outgoing wave then accumulates <b>k</b><sub>1</sub>·(<b>R</b><sub>det</sub>-<b>r</b>). The <b>r</b>-dependent part is -<b>k</b><sub>1</sub>·<b>r</b>+<b>k</b><sub>0</sub>·<b>r</b>=-<b>q</b>·<b>r</b>.

If each element scatters **once** (weak interaction; no shadowing), the total amplitude is the integral of phasors

$$
A(\mathbf{q})=\int d^3r\,\rho(\mathbf{r})\,e^{-i\mathbf{q}\cdot\mathbf{r}}=\tilde\rho(\mathbf{q}).
$$

The **differential cross section** (scattered intensity per solid angle, per incident flux) is

$$
\frac{d\sigma}{d\Omega}=\lvert A(\mathbf{q})\rvert^2
$$

in units where the single-particle scattering length is absorbed into <i>ρ</i>. This is PRB (2.1). **Born approximation = first-order perturbation = Fourier transform of <i>ρ</i>.**

It fails when the wave inside the sample is strongly distorted — near total external reflection — which is why chapter 8 introduces the distorted-wave Born approximation (DWBA).

## 2.4 From a 3D density to a surface

PRB assumes the material is **homogeneous except for a surface**: ρ(<b>r</b>)=ρ<sub>0</sub> for z<z(x,y) and 0 above, with z(x,y) a single-valued height (PRB Sec. II, after (2.3)). Atomic structure is ignored when qa≪ 1 (<i>a</i> is an atomic size).

Do the <i>z</i> integral first, at fixed (x,y). Put a tiny absorption so the integral from -∞ converges:

$$
\int_{-\infty}^{z(x,y)} dz\,e^{-iq_z z}=\frac{e^{-iq_z z(x,y)}}{-iq_z}
$$

(up to a factor from the lower limit that gives only a q<sub>z</sub>=0 piece). Then

$$
A(\mathbf{q})\propto\frac{\rho_0}{q_z}\int dx\,dy\,e^{-iq_z z(x,y)}e^{-i(q_x x+q_y y)}.
$$

The observed intensity contains ∣A∣<sup>2</sup>, hence a factor 1/q<sub>z</sub><sup>2</sup> and a **four-fold** integral over two surface points (x,y) and (x',y'). That is PRB (2.4):

$$
\frac{d\sigma}{d\Omega}\propto\frac{\rho_0^2}{q_z^2}\int d^2R\int d^2R'\,
\exp\bigl(-iq_z[z(\mathbf{R}')-z(\mathbf{R})]\bigr)
\exp\bigl(-i\mathbf{q}_\parallel\cdot(\mathbf{R}'-\mathbf{R})\bigr).
$$

Physica (1) writes the same with electron-density contrast Δρ in place of ρ<sub>0</sub>.

**Uncertain (prefactor only):** PRB (2.3) quotes a surface-integral identity with an arbitrary unit vector <b>A</b>. The <i>Θ</i>-function derivation above reproduces (2.4) including the 1/q<sub>z</sub><sup>2</sup>. Absolute constants (N b<sup>2</sup>, illuminated area) are not needed to understand correlation-function modelling.

## 2.5 Intensity is never ρ̃; it is ∣ρ̃∣<sup>2</sup>

$$
\lvert A(\mathbf{q})\rvert^2=\tilde\rho(\mathbf{q})\,\tilde\rho(-\mathbf{q})=\int d^3r\int d^3r'\,\rho(\mathbf{r})\rho(\mathbf{r}')e^{-i\mathbf{q}\cdot(\mathbf{r}-\mathbf{r}')}.
$$

The integrand depends on the **product** of densities at two points. After averaging (chapter 3–4) that product becomes a **correlation function**, and the remaining integral is the FT of that correlation. That is why modelling scattering *is* modelling correlations.

Numeric phase picture: `code/03_born_two_slits.py` (two point scatterers: intensity ∝ cos<sup>2</sup>(<b>q</b>·<b>d</b>/2)).
