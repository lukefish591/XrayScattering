# 6. Capillary waves and logarithmic correlations

PRB Sec. II.D: a liquid surface is not self-affine in the solid sense. The restoring force is **surface tension** (and gravity at long wavelength).

## 6.1 Equipartition ⇒ 1/q<sup>2</sup> spectrum

Let z(x,y) be the instantaneous height of a liquid. For small slopes the excess energy is

$$
H=\frac{\gamma}{2}\int d^2R\,\lvert\nabla z\rvert^2+\frac{\Delta\rho_m g_{\mathrm{grav}}}{2}\int d^2R\,z^2,
$$

where <i>γ</i> is the surface tension, Δρ<sub>m</sub> a mass-density contrast, and g<sub>grav</sub> gravity. In Fourier space (Parseval),

$$
H=\frac{1}{2}\sum_{\mathbf{q}_\parallel}\bigl(\gamma q_\parallel^2+\Delta\rho_m g_{\mathrm{grav}}\bigr)\lvert z_{\mathbf{q}}\rvert^2.
$$

Each quadratic mode has mean energy (1/2) k<sub>B</sub> T (**equipartition**), so

$$
P(\mathbf{q}_\parallel)=\langle\lvert z_{\mathbf{q}}\rvert^2\rangle\propto\frac{k_B T}{\gamma q_\parallel^2+\Delta\rho_m g_{\mathrm{grav}}}.
$$

Without gravity, P∼ 1/q<sub>∥</sub><sup>2</sup>. The 2D FT of 1/q<sup>2</sup> is **logarithmic** in <i>R</i> (the 2D Green function of the Laplacian). That is PRB (2.31):

$$
g(R)=A+B\ln(R/\text{Å}),
$$

with <i>B</i> set by k<sub>B</sub> T/γ (and a conventional Å in the log to keep the argument dimensionless). Then C(R)=σ<sub>eff</sub><sup>2</sup>-g(R)/2 **does not tend to a finite σ<sup>2</sup>**: the variance ∫ d<sup>2</sup>q P(q) diverges both as q→ 0 (infinite surface) and as q→∞ (continuum).

## 6.2 Why a cutoff restores specular

PRB lists two experimental cutoffs:

1. **Physics:** gravity (or finite depth) replaces q<sup>2</sup> by q<sup>2</sup>+κ<sup>2</sup>, κ<sup>-1</sup>= capillary length. Then g(R)=σ<sup>2</sup>(1-K<sub>0</sub>(κ R)) (PRB (2.35)), K<sub>0</sub> a decaying Bessel, and g(∞)=σ<sup>2</sup><∞. Specular δ(<b>q</b><sub>∥</sub>) returns, (2.28a).
2. **Instrument:** the integral over <i>R</i> only runs out to the **coherence length** ξ<sub>coh</sub> of the beam on the surface (PRB: typically microns projected; they use a Kummer-function form (2.33) following Dutta & Sinha). That also caps <i>g</i>.

**Moral for modelling:** a log correlation is a well-defined *local* statistic, but the split “specular vs diffuse” is **ill-posed until you state the IR cutoff**. Never import a liquid <i>B</i> without ξ<sub>coh</sub> or <i>κ</i>.

**Uncertain:** the exact prefactors A,B in (2.31) depend on UV (molecular) cutoff conventions; PRB treats them as fit parameters for a given experiment. We do not need those numbers for your project unless you have a liquid surface.

Numeric log vs cutoff: `code/08_specular_split.py` includes a log-like <i>g</i> truncated at <i>ξ</i>.
