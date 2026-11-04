# Phase 7: Adversarial Security & Explainable AI (XAI) Testing
## Topological-Relativistic-Thermodynamic Learning (TRTL)

---

## 1. Executive Summary & Problem Formulation

In high-stakes deployment regimes (e.g., automated oncology triage, aerospace radar classification, financial fraud forensics), predictive accuracy alone is insufficient. Machine learning architectures face two critical existential requirements:
1. **Adversarial Security:** Mathematical and empirical immunity against worst-case adversarial perturbations designed to trigger catastrophic misclassification with imperceptible input shifts ($\ell_\infty, \ell_2$).
2. **Actionable, Interpretable Recourse (XAI):** Generating deterministic, low-cost counterfactual explanations that instruct human stakeholders on the exact minimal feature modifications required to transition an unfavorable prediction to a favorable class.

Classical machine learning models exhibit severe pathologies in both dimensions:
- **Deep Neural Networks (MLPs, ResNets):** Suffer from linear extrapolation vulnerabilities outside the training support. Adversarial attacks like FGSM, PGD, and Carlini-Wagner exploit gradient alignment to push predictions across razor-thin hyperplanes with zero physical resistance. Existing gradient-based counterfactual methods (Wachter et al., 2017) optimize non-convex loss surfaces, becoming trapped in off-manifold voids and generating unrealistic, high-curvature recourse paths.
- **Tree Ensembles (Random Forest, XGBoost):** Exhibit non-differentiable step boundaries. Calculating counterfactual recourse requires combinatorial integer programming (e.g., DiCE, Mothilal et al., 2020), which is computationally intractable for real-time systems and produces orthogonal, jagged step trajectories.

**TRTL's Solution:** By grounding classification in relativistic metric dilatation, coherent wave interference, and thermodynamic phase transitions, TRTL establishes:
1. **Certified and Empirical Adversarial Immunity:** High-entropy adversarial perturbations compress distance metrics ($\gamma \gg 1$), dissipating adversarial energy across destructive wave interference horizons.
2. **Continuous Thermodynamic Counterfactual Recourse (TCR):** Leveraging the conservative force vector field $\mathbf{F}(\mathbf{x}) = -\nabla \mathcal{F}(\mathbf{x})$ to transport query points along minimal-action geodesic gradient flows directly toward target class certainty cores.

---

## 2. Adversarial Security Framework & Threat Model

### 2.1 Threat Model Definition
We evaluate white-box and black-box adversaries constrained by norm balls $\mathcal{B}_p(\mathbf{x}, \epsilon) = \{ \mathbf{x}' \in \mathbb{R}^D : \|\mathbf{x}' - \mathbf{x}\|_p \le \epsilon \}$.

1. **Projected Gradient Descent ($\text{PGD-}\ell_\infty$):**
   The standard multi-step adversarial benchmark:
   $$\mathbf{x}^{(t+1)} = \Pi_{\mathcal{B}_\infty(\mathbf{x}_0, \epsilon)} \left( \mathbf{x}^{(t)} + \alpha \cdot \text{sign}\left( \nabla_{\mathbf{x}} \mathcal{L}(\mathbf{x}^{(t)}, y) \right) \right)$$
   where $\alpha = \epsilon / 4$ is the step size, and $\Pi$ projects the perturbation onto the $\ell_\infty$ $\epsilon$-cube.

2. **Projected Gradient Descent ($\text{PGD-}\ell_2$):**
   $$\mathbf{x}^{(t+1)} = \Pi_{\mathcal{B}_2(\mathbf{x}_0, \epsilon)} \left( \mathbf{x}^{(t)} + \alpha \cdot \frac{\nabla_{\mathbf{x}} \mathcal{L}(\mathbf{x}^{(t)}, y)}{\|\nabla_{\mathbf{x}} \mathcal{L}(\mathbf{x}^{(t)}, y)\|_2} \right)$$

3. **Fast Gradient Sign Method (FGSM):**
   Single-step linear perturbation:
   $$\mathbf{x}_{\text{adv}} = \mathbf{x}_0 + \epsilon \cdot \text{sign}\left( \nabla_{\mathbf{x}} \mathcal{L}(\mathbf{x}_0, y) \right)$$

4. **Carlini-Wagner ($\text{CW-}\ell_2$) Optimization Attack:**
   Formulated as the box-constrained optimization:
   $$\min_{\boldsymbol{\delta}} \|\boldsymbol{\delta}\|_2^2 + c \cdot \max\left( \max_{c' \ne y} Z(\mathbf{x} + \boldsymbol{\delta})_{c'} - Z(\mathbf{x} + \boldsymbol{\delta})_y, -\kappa \right)$$
   subject to $\mathbf{x} + \boldsymbol{\delta} \in [0, 1]^D$.

---

### 2.2 Absence of Gradient Masking (Athalye Audit)
A common failure mode in purported "adversarially robust" models is **gradient masking** or **gradient obfuscation** (Athalye et al., ICML 2018), where vanishing gradients prevent gradient-based attackers from finding adversarial examples that nonetheless exist.

We prove TRTL does not rely on gradient masking:
1. **$C^\infty$ Field Differentiability:** From Lemma 2.0, the order parameter field $S_c(\mathbf{x})$ is smooth and everywhere differentiable:
   $$\|\nabla_{\mathbf{x}} S_c(\mathbf{x})\| > 0 \quad \forall \mathbf{x} \in \mathbb{R}^D \setminus \{\text{nodal stationary points}\}$$
2. **Single-Step vs. Multi-Step Resilience:** Unlike gradient-masked models where PGD-100 breaks defenses that resist FGSM-1, TRTL exhibits monotonic, proportional decay under both single-step and 100-step PGD attacks.
3. **Black-Box Decision-Based Verification:** Black-box boundary attacks (HopSkipJump, Boundary Attack) that query zero gradient information fail to find adversarial samples within TRTL's certified radius $r_{\text{cert}}$.

---

## 3. Mathematical Foundations of Thermodynamic Counterfactual Recourse (TCR)

### 3.1 Closed-Form Gradient of the Thermodynamic Order Parameter
To generate counterfactual recourse, a query point $\mathbf{x}$ classified as source class $c_0$ must be transported toward target class $c^*$. The ideal trajectory follows the ascending gradient of the target class order parameter $S_{c^*}(\mathbf{x})$.

#### Theorem 7.1 (Analytical Chain Rule for Order-Parameter Gradients)
Let $\mathbf{x} \in \mathbb{R}^D$ be a continuous feature vector. The gradient of the target class order parameter $S_{c^*}(\mathbf{x})$ with respect to input coordinates $\mathbf{x}$ is given analytically by:
$$\nabla_{\mathbf{x}} S_{c^*}(\mathbf{x}) = \sum_{c=1}^C \frac{\partial S_{c^*}}{\partial E_c} \nabla_{\mathbf{x}} E_c(\mathbf{x})$$

where:
1. **Thermodynamic Stage Sensitivity:**
   $$\frac{\partial S_{c^*}}{\partial E_c} = \frac{\delta_{c c^*} \sum_{k} E_k - E_{c^*}}{\left( \sum_{k} E_k \right)^2}$$
2. **Coherent Wave Energy Spatial Gradient:**
   $$\nabla_{\mathbf{x}} E_c(\mathbf{x}) = 2 \, \text{Re}\left(\Psi_c(\mathbf{x})\right) \nabla_{\mathbf{x}} \text{Re}\left(\Psi_c(\mathbf{x})\right)$$
3. **Anchor-Summed Spatial Derivative:**
   $$\nabla_{\mathbf{x}} \text{Re}\left(\Psi_c(\mathbf{x})\right) = -\sum_{i \in \mathcal{C}_c} A_i e^{-\frac{1}{2} \mu d_{i, \text{rel}}^2} \left[ \mu \, \cos(k d_{i, \text{rel}}) + \frac{k}{d_{i, \text{rel}}} \sin(k d_{i, \text{rel}}) \right] \gamma_i^2 W (\mathbf{x} - \mathbf{x}_i)$$

*Proof:*
Applying the multivariate chain rule across Stage I (metric), Stage II (wave interference), and Stage III (thermodynamic relaxation):
$$\frac{\partial d_{i, \text{rel}}}{\partial \mathbf{x}} = \gamma_i \frac{W (\mathbf{x} - \mathbf{x}_i)}{\|\mathbf{x} - \mathbf{x}_i\|_W} = \frac{\gamma_i^2 W (\mathbf{x} - \mathbf{x}_i)}{d_{i, \text{rel}}}$$
Differentiating the real wave packet component $\psi_i(\mathbf{x}) = A_i e^{-\frac{1}{2} \mu d^2} \cos(k d)$:
$$\nabla_{\mathbf{x}} \psi_i = A_i e^{-\frac{1}{2} \mu d^2} \left( -\mu d \cos(k d) - k \sin(k d) \right) \nabla_{\mathbf{x}} d$$
Substituting $\nabla_{\mathbf{x}} d = \frac{\gamma_i^2 W (\mathbf{x} - \mathbf{x}_i)}{d}$ yields the exact closed-form expression. $\blacksquare$

---

### 3.2 Thermodynamic Recourse Trajectory Equation
The continuous counterfactual path $\mathbf{x}(t)$ is governed by the conservative gradient dynamical system:
$$\dot{\mathbf{x}}(t) = \nabla_{\mathbf{x}} S_{c^*}(\mathbf{x}(t)) - \lambda_{\text{reg}} (\mathbf{x}(t) - \mathbf{x}_0)$$
discretized via Euler-Maruyama or adaptive Runge-Kutta 4th order (RK4):
$$\mathbf{x}^{(k+1)} = \mathbf{x}^{(k)} + \eta \nabla_{\mathbf{x}} S_{c^*}\left(\mathbf{x}^{(k)}\right) - \eta \lambda_{\text{reg}} \left(\mathbf{x}^{(k)} - \mathbf{x}_0\right)$$
where $\eta > 0$ is the recourse learning rate, and $\lambda_{\text{reg}}$ enforces proximity to the original factual point.

---

### 3.3 Theoretical Properties of TCR

#### Theorem 7.2 (Monotonic Order-Parameter Growth)
Under pure gradient ascent ($\lambda_{\text{reg}} = 0$), the target class confidence $S_{c^*}(\mathbf{x}(t))$ along the counterfactual trajectory $\mathbf{x}(t)$ is strictly monotonically non-decreasing:
$$\frac{d}{dt} S_{c^*}(\mathbf{x}(t)) = \left\| \nabla_{\mathbf{x}} S_{c^*}(\mathbf{x}(t)) \right\|^2 \ge 0$$
Equality holds if and only if $\mathbf{x}(t)$ attains a stationary point of the potential manifold.

*Proof:*
By directional derivation:
$$\frac{d}{dt} S_{c^*}(\mathbf{x}(t)) = \left\langle \nabla_{\mathbf{x}} S_{c^*}(\mathbf{x}(t)), \dot{\mathbf{x}}(t) \right\rangle = \left\langle \nabla_{\mathbf{x}} S_{c^*}(\mathbf{x}(t)), \nabla_{\mathbf{x}} S_{c^*}(\mathbf{x}(t)) \right\rangle = \left\| \nabla_{\mathbf{x}} S_{c^*}(\mathbf{x}(t)) \right\|^2 \ge 0 \quad \blacksquare$$

#### Theorem 7.3 (Manifold-Adherence Guarantee)
Let $\mathcal{M}$ be the data manifold embedded in $\mathbb{R}^D$. If the training anchors sample $\mathcal{M}$ with density $\rho(\mathbf{x}) \ge \rho_0 > 0$, any off-manifold deviation $\mathbf{x}_\perp \perp T_{\mathbf{x}} \mathcal{M}$ experiences an exponential restoring force:
$$\left\| \mathbf{F}_{\text{restoring}}(\mathbf{x}_\perp) \right\| \ge \mathcal{O}\left( e^{-\frac{1}{2} \mu \|\mathbf{x}_\perp\|^2} \right)$$
preventing counterfactual trajectories from straying into unphysical, low-density regions.

---

## 4. Recourse Quality Evaluation Metrics

To benchmark TCR against classical counterfactual algorithms (Wachter's Optimization, DiCE), we implement four standard quantitative metrics:

1. **Recourse Proximity (Total Path Length $\mathcal{L}_2$):**
   $$\mathcal{L}_2(\gamma) = \sum_{k=0}^{K-1} \left\| \mathbf{x}^{(k+1)} - \mathbf{x}^{(k)} \right\|_2$$
   Measures the total physical effort required by the agent to implement the recourse.

2. **Path Smoothness / Total Curvature ($\kappa$):**
   $$\kappa(\gamma) = \sum_{k=1}^{K-1} \left\| \mathbf{v}^{(k)} - \mathbf{v}^{(k-1)} \right\|_2, \quad \mathbf{v}^{(k)} = \frac{\mathbf{x}^{(k+1)} - \mathbf{x}^{(k)}}{\|\mathbf{x}^{(k+1)} - \mathbf{x}^{(k)}\|_2}$$
   Quantifies the angular tortuosity of the trajectory. Low curvature corresponds to direct, intuitive recourse.

3. **Feature Sparsity ($\ell_0$ Metric):**
   $$S_0 = \sum_{j=1}^D \mathbb{I}\left( \left| x_j^{(K)} - x_j^{(0)} \right| > \epsilon_{\text{tol}} \right)$$
   Measures how many distinct features must be altered to reverse the prediction.

4. **Computational Latency ($T_{\text{recourse}}$ in ms):**
   Wall-clock execution time required to reach the target decision horizon $S_{c^*} \ge 0.50$.

---

## 5. Architectural Comparison: TCR vs. Classical XAI

```
┌───────────────────────────────┬───────────────────────────────┬───────────────────────────────┐
│ Feature / Attribute           │ Classical Recourse (Wachter)  │ TRTL Thermodynamic Recourse   │
├───────────────────────────────┼───────────────────────────────┼───────────────────────────────┤
│ Optimization Landscape        │ Highly non-convex, saddle traps│ Conservative potential gradient│
│ Trajectory Nature             │ Unconstrained line search     │ Physical gradient flow        │
│ Manifold Adherence            │ Poor (often lands in OOD void)│ Strong (anchored by envelope) │
│ Boundary Crossing Guarantee   │ No guarantee (may diverge)    │ Guaranteed monotonic growth   │
│ Computational Complexity      │ O(N_iter * Backprop)          │ O(N_iter * N_active * D)      │
│ Vector Field Compatibility    │ None (isolated point search)  │ Native conservative force field│
└───────────────────────────────┴───────────────────────────────┴───────────────────────────────┘
```
