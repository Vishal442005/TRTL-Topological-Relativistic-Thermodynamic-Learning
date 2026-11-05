# Topological-Relativistic-Thermodynamic Learning (TRTL)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23968898.svg)](https://doi.org/10.5281/zenodo.23968898)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--0552--8551-green.svg)](https://orcid.org/0009-0006-0552-8551)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status: Certified](https://img.shields.io/badge/Status-Fully%20Verified-brightgreen.svg)]()

> **Official Open-Science Implementation & Reproducibility Suite**  
> *Author:* Vishal Chandel ([ORCID: 0009-0006-0552-8551](https://orcid.org/0009-0006-0552-8551)) & TRTL Research Consortium  
> *Target Venue:* Elsevier Pattern Recognition / IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI).

---

## 1. Overview & Theoretical Architecture

**Topological-Relativistic-Thermodynamic Learning (TRTL)** replaces arbitrary geometric decision boundaries (hyperplanes, orthogonal axis cuts, deep ReLU polyhedra) with a unified, three-stage physical field pipeline:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              TRTL THREE-STAGE PHYSICAL PIPELINE                        │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ Stage I: RAMD            │ Stage II: TWIL           │ Stage III: TPTC                  │
│ Relativistic Metric      │ Wavefield Superposition  │ Thermodynamic Crystallization    │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ - Local Shannon Entropy  │ - Multi-Class Wavepacket │ - Ginzburg-Landau Relax          │
│ - Lorentz Dilatation     │ - Coherent Projection    │ - Simplex Projection             │
│ - Anisotropic Metric W   │ - Cross-Class Inhibition │ - Certified Invariance r_cert    │
│ - Ball-Tree Horizon Cut  │ - Interference Horizon   │ - Continuous Recourse dot{x}     │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

1. **Stage I: Relativistic Anisotropic Metric Dilatation (RAMD):**
   $$d_{i, \text{rel}}(\mathbf{x}) = \|\mathbf{x} - \mathbf{x}_i\|_W \cdot \gamma_i, \quad \gamma_i = \frac{1}{\sqrt{1 - \beta (H_i / H_{\max})^2}}$$
2. **Stage II: Thermodynamic Wave Interference Layer (TWIL):**
   $$\Psi_c(\mathbf{x}) = \sum_{i \in \mathcal{C}_c} A_i e^{-\frac{1}{2} \mu d_{i, \text{rel}}^2} e^{i k d_{i, \text{rel}}}, \quad E_c(\mathbf{x}) = \max\left( 0, |\Psi_c|^2 - \frac{\kappa}{C-1} \sum_{c' \ne c} |\Psi_{c'}|^2 \right)$$
3. **Stage III: Thermodynamic Phase-Transition Crystallization (TPTC):**
   $$S^{(k+1)} = \Pi_\Delta \left( S^{(k)} - \Delta t \left[ (T - T_c) S + b S^3 - \mathbf{h} + \xi S \sum_{c' \ne c} S_{c'}^2 \right] \right)$$

---

## 2. Repository Structure

```
.
├── CITATION.cff                      # CFF citation metadata
├── LICENSE                           # Open source MIT license
├── pyproject.toml                    # Modern PEP 517 build configuration
├── requirements.txt                  # Python dependencies
├── reproduce_all.py                  # One-click master reproduction script
│
├── trtl/                             # Core Python Package
│   ├── __init__.py                   # Package initialization and exports
│   ├── metric.py                     # Stage I: RAMD Lorentz dilatation & W metric
│   ├── wave.py                       # Stage II: TWIL wavepacket interference
│   ├── thermo.py                     # Stage III: TPTC Ginzburg-Landau relaxation
│   ├── spatial.py                    # Spatial Ball-Tree acceleration & R_cut
│   ├── classifier.py                 # Scikit-Learn API classifier (TRTLClassifier)
│   └── recourse.py                   # Thermodynamic Counterfactual Recourse engine
│
├── docs/                             # Full Theoretical Derivations & Documentation
│   ├── phase1_conceptualization_and_formulation.md
│   ├── phase2_mathematical_derivations_and_proofs.md
│   ├── phase3_optimization_and_algorithmic_engineering.md
│   ├── phase4_high_dimensional_scaling_and_metric_learning.md
│   ├── phase5_computational_efficiency_and_spatial_indexing.md
│   ├── phase6_multi_domain_empirical_benchmarking.md
│   ├── phase7_adversarial_security_and_xai.md
│   ├── phase8_publication_graphics_and_visualization_pipeline.md
│   └── phase9_open_science_and_doi_archival.md
│
├── experiments/                      # Phase-Wise Verification Scripts
│   ├── phase1_pathology_audit.py
│   ├── phase2_theoretical_verification.py
│   ├── phase3_optimization_verification.py
│   ├── phase4_scaling_verification.py
│   ├── phase5_spatial_indexing_verification.py
│   ├── phase6_benchmark_suite.py
│   └── phase7_adversarial_and_xai.py
│
├── figures/                          # 23 Publication-Grade Figures (PNG & PDF)
│   ├── phase1/ (Figs 1-2)
│   ├── phase2/ (Figs 3-4)
│   ├── phase3/ (Figs 5-7)
│   ├── phase4/ (Figs 8-10)
│   ├── phase5/ (Figs 11-12)
│   ├── phase6/ (Figs 13-16)
│   ├── phase7/ (Figs 17-20)
│   └── phase8/ (Figs 21-23)
│
└── manuscript/                       # Dual-Format Publication Source
    ├── manuscript_tpami.tex          # Full 35+ page IEEE TPAMI LaTeX manuscript
    └── manuscript_tpami.docx         # Native OMML Microsoft Word production document
```

---

## 3. Installation & Quickstart

```bash
# Clone the repository
git clone https://github.com/trtl-consortium/trtl.git
cd trtl

# Install dependencies
pip install -r requirements.txt

# Install TRTL package in editable mode
pip install -e .
```

### Python Quickstart
```python
from trtl import TRTLClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

clf = TRTLClassifier()
clf.fit(X_tr, y_tr)
print("Test Accuracy:", clf.score(X_te, y_te))

# Compute Certified L2 Invariance Radius for query sample
r_cert = clf.compute_certified_radius(X_te[0])
print("Certified L2 Robustness Radius:", r_cert)
```

---

## 4. Complete Reproduction Workflow

To replicate all mathematical proofs, empirical benchmarks, adversarial stress tests, and 23 vector figures with a single command:

```bash
python reproduce_all.py
```

The master script automatically validates environment prerequisites, runs verification scripts across Phases 1 to 8, verifies checksums, and compiles summary metrics.

---

## 5. Citation

```bibtex
@article{chandel2026trtl,
  title={Topological-Relativistic-Thermodynamic Learning: Continuous Manifold Invariance, Coherent Wave Superposition, and Certified Adversarial Immunity},
  author={Chandel, Vishal and TRTL Research Consortium},
  journal={Pattern Recognition},
  year={2026},
  doi={10.5281/zenodo.23968898},
  url={https://doi.org/10.5281/zenodo.23968898}
}
```
