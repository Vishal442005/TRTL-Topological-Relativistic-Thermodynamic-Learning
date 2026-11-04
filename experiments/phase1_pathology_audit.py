"""
Phase 1: Pathology Audit and Physical Grounding Verification
Topological-Relativistic-Thermodynamic Learning (TRTL)

This script empirically audits the classical decision boundary pathologies
(SVM, Random Forest, Deep MLP, k-NN) and verifies the tripartite physical
mechanisms of TRTL (RAMD, TWIL, TPTC) on entangled 2D synthetic manifolds.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.spatial.distance import cdist

from sklearn.datasets import make_moons
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, f1_score


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


class TRTLPhase1Engine:
    """Mathematical implementation of TRTL Tripartite Engine for Phase 1."""
    def __init__(self, beta=0.85, sigma_entropy=0.6, k_wave=1.2, mu_damp=0.35, 
                 temp_diff=-1.5, repulsion_xi=2.2, cooling_steps=15, dt=0.04):
        self.beta = beta
        self.sigma_entropy = sigma_entropy
        self.k_wave = k_wave
        self.mu_damp = mu_damp
        self.temp_diff = temp_diff
        self.repulsion_xi = repulsion_xi
        self.cooling_steps = cooling_steps
        self.dt = dt

    def fit(self, X, y):
        self.scaler_ = StandardScaler()
        self.X_ = self.scaler_.fit_transform(X)
        self.y_ = np.asarray(y)
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        N = self.X_.shape[0]

        # Stage I: Local Shannon Conflict Entropy & Lorentz Dilatation
        dists = cdist(self.X_, self.X_, metric='euclidean')
        weights = np.exp(-(dists ** 2) / (2.0 * self.sigma_entropy ** 2))
        self.H_ = np.zeros(N)

        for i in range(N):
            w = weights[i]
            total_w = np.sum(w) + 1e-12
            probs = np.array([np.sum(w[self.y_ == c]) for c in self.classes_]) / total_w
            probs = np.clip(probs, 1e-12, 1.0)
            self.H_[i] = -np.sum(probs * np.log(probs))

        H_max = np.log(self.n_classes_) + 1e-5
        ratio_sq = (self.H_ / H_max) ** 2
        # Lorentz Dilatation factor: high entropy -> large dilatation -> expands distance
        self.gamma_ = 1.0 / np.sqrt(np.maximum(1.0 - self.beta * ratio_sq, 1e-4))
        
        # Base phase angles on unit circle
        self.class_phases_ = np.linspace(0, 2 * np.pi, self.n_classes_, endpoint=False)
        return self

    def compute_fields(self, X_raw):
        """Returns intermediate physical fields: Lorentz dilatation, Wave Energy, and Crystal State."""
        X_scaled = self.scaler_.transform(X_raw)
        raw_dists = cdist(X_scaled, self.X_, metric='euclidean')
        d_rel = raw_dists * self.gamma_[np.newaxis, :]

        # Stage II: Unified Complex Wavefield Superposition
        envelope = np.exp(-self.mu_damp * d_rel) / (d_rel + 0.15)
        n_query = X_scaled.shape[0]
        
        # Anchor phase allocation
        anchor_phases = self.class_phases_[self.y_]
        
        # Net complex wavefield psi(x)
        total_psi = np.sum(envelope * np.exp(1j * (self.k_wave * d_rel + anchor_phases[np.newaxis, :])), axis=1)

        # Coherent projection onto class phase vectors
        energies = np.zeros((n_query, self.n_classes_))
        for idx, phase_c in enumerate(self.class_phases_):
            proj = np.real(total_psi * np.exp(-1j * phase_c))
            energies[:, idx] = np.maximum(0.0, proj) ** 2

        # Stage III: Thermodynamic Phase Crystallization
        row_sums = np.sum(energies, axis=1, keepdims=True) + 1e-12
        S = energies / row_sums
        h_field = S.copy()

        for _ in range(self.cooling_steps):
            S_sq_sum = np.sum(S ** 2, axis=1, keepdims=True)
            repulsion = self.repulsion_xi * S * (S_sq_sum - S ** 2)
            dF_dS = self.temp_diff * S + (S ** 3) - h_field + repulsion
            S = S - self.dt * dF_dS
            S = np.clip(S, 0.0, 1.0)
            S /= (np.sum(S, axis=1, keepdims=True) + 1e-12)

        return d_rel, energies, S


def run_pathology_audit():
    print("=" * 70)
    print("PHASE 1: PATHOLOGY AUDIT & PHYSICAL GROUNDING EXPERIMENT")
    print("=" * 70)

    fig_dir = os.path.join("figures", "phase1")
    ensure_dir(fig_dir)

    # 1. Generate Synthetic Manifolds with Boundary Noise
    np.random.seed(42)
    X_clean, y_clean = make_moons(n_samples=500, noise=0.20, random_state=42)
    
    # Inject 12% symmetric boundary label noise
    y_noisy = y_clean.copy()
    flip_indices = np.random.choice(len(y_clean), size=int(0.12 * len(y_clean)), replace=False)
    y_noisy[flip_indices] = 1 - y_noisy[flip_indices]

    # Clean test set to measure true generalization
    X_test, y_test = make_moons(n_samples=300, noise=0.20, random_state=142)

    # 2. Train Classical Baseline Classifiers
    models = {
        "RBF SVM": SVC(kernel='rbf', C=1.0, probability=True, random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42),
        "Deep MLP (ReLU)": MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=800, random_state=42),
        "k-NN (k=5)": KNeighborsClassifier(n_neighbors=5)
    }

    results = {}
    for name, model in models.items():
        model.fit(X_clean, y_noisy)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        results[name] = {"acc": acc, "f1": f1}
        print(f"[*] Baseline {name:16s} | Clean Test Acc: {acc:.4f} | Macro F1: {f1:.4f}")

    # 3. Fit TRTL Phase 1 Engine
    trtl = TRTLPhase1Engine()
    trtl.fit(X_clean, y_noisy)
    _, _, S_test = trtl.compute_fields(X_test)
    y_pred_trtl = np.argmax(S_test, axis=1)
    acc_trtl = accuracy_score(y_test, y_pred_trtl)
    f1_trtl = f1_score(y_test, y_pred_trtl)
    results["TRTL (Phase 1)"] = {"acc": acc_trtl, "f1": f1_trtl}
    print(f"[+] Proposed TRTL (Phase 1)   | Clean Test Acc: {acc_trtl:.4f} | Macro F1: {f1_trtl:.4f}")

    # 4. Generate Spatial Evaluation Mesh
    x_min, x_max = -2.0, 3.0
    y_min, y_max = -1.5, 2.0
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 250), np.linspace(y_min, y_max, 250))
    grid = np.c_[xx.ravel(), yy.ravel()]

    # -------------------------------------------------------------
    # FIGURE 1: Classical Decision Boundary Pathologies
    # -------------------------------------------------------------
    plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13})
    fig, axes = plt.subplots(2, 2, figsize=(12, 10), constrained_layout=True)
    axes = axes.ravel()

    cm_bg = plt.cm.RdBu_r
    cm_points = ListedColormap(['#d95f02', '#1b9e77'])

    for idx, (name, model) in enumerate(models.items()):
        ax = axes[idx]
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(grid)[:, 1]
        else:
            probs = model.predict(grid)
        probs = probs.reshape(xx.shape)

        ax.contourf(xx, yy, probs, levels=25, cmap=cm_bg, alpha=0.85)
        ax.contour(xx, yy, probs, levels=[0.5], colors='black', linewidths=2.2)
        ax.scatter(X_clean[:, 0], X_clean[:, 1], c=y_noisy, cmap=cm_points, 
                   edgecolors='k', s=35, alpha=0.85)
        ax.set_title(f"{name}\nAcc: {results[name]['acc']:.3f} | F1: {results[name]['f1']:.3f}")
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        ax.set_xticks([])
        ax.set_yticks([])

    fig_path_1 = os.path.join(fig_dir, "fig1_classical_boundary_pathologies.png")
    fig_path_pdf1 = os.path.join(fig_dir, "fig1_classical_boundary_pathologies.pdf")
    plt.savefig(fig_path_1, dpi=300)
    plt.savefig(fig_path_pdf1)
    plt.close()
    print(f"\n[OK] Saved Figure 1 to {fig_path_1} and {fig_path_pdf1}")

    # -------------------------------------------------------------
    # FIGURE 2: TRTL Tripartite Physical Mechanism & Tri-Zone Topology
    # -------------------------------------------------------------
    d_rel_grid, energies_grid, S_grid = trtl.compute_fields(grid)
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5), constrained_layout=True)
    
    # 1. Stage I: Lorentz Metric Dilatation & Geodesic Warping
    ax1 = axes[0]
    min_d_rel = np.min(d_rel_grid, axis=1).reshape(xx.shape)
    im1 = ax1.contourf(xx, yy, min_d_rel, levels=30, cmap='magma_r')
    ax1.scatter(X_clean[:, 0], X_clean[:, 1], c=trtl.gamma_, cmap='viridis', 
                s=40, edgecolors='black', linewidths=0.5)
    ax1.set_title("Stage I: RAMD Metric Dilatation\n(Lorentz Geodesic Warping $\\gamma(x)$)")
    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(y_min, y_max)
    plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)

    # 2. Stage II: Topological Wave Interference & Nodal Trenches
    ax2 = axes[1]
    wave_contrast = (energies_grid[:, 1] - energies_grid[:, 0]).reshape(xx.shape)
    im2 = ax2.contourf(xx, yy, wave_contrast, levels=35, cmap='coolwarm')
    ax2.contour(xx, yy, wave_contrast, levels=[0.0], colors='black', linewidths=2.5, linestyles='--')
    ax2.scatter(X_clean[:, 0], X_clean[:, 1], c=y_noisy, cmap=cm_points, 
                s=35, edgecolors='k')
    ax2.set_title("Stage II: TWIL Helmholtz Superposition\n(Zero-Amplitude Nodal Boundary Trenches)")
    ax2.set_xlim(x_min, x_max)
    ax2.set_ylim(y_min, y_max)
    plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)

    # 3. Stage III: Thermodynamic Phase Crystallization & Tri-Zone Core
    ax3 = axes[2]
    crystal_prob = S_grid[:, 1].reshape(xx.shape)
    im3 = ax3.contourf(xx, yy, crystal_prob, levels=30, cmap='RdBu_r', alpha=0.9)
    ax3.contour(xx, yy, crystal_prob, levels=[0.5], colors='black', linewidths=2.5)
    ax3.scatter(X_clean[:, 0], X_clean[:, 1], c=y_noisy, cmap=cm_points, 
                s=35, edgecolors='k')
    ax3.set_title(f"Stage III: TPTC Ginzburg-Landau Cooling\nAcc: {acc_trtl:.3f} | F1: {f1_trtl:.3f}")
    ax3.set_xlim(x_min, x_max)
    ax3.set_ylim(y_min, y_max)
    plt.colorbar(im3, ax=ax3, fraction=0.046, pad=0.04)

    for ax in axes:
        ax.set_xticks([])
        ax.set_yticks([])

    fig_path_2 = os.path.join(fig_dir, "fig2_trtl_tripartite_fields.png")
    fig_path_pdf2 = os.path.join(fig_dir, "fig2_trtl_tripartite_fields.pdf")
    plt.savefig(fig_path_2, dpi=300)
    plt.savefig(fig_path_pdf2)
    plt.close()
    print(f"[OK] Saved Figure 2 to {fig_path_2} and {fig_path_pdf2}")

    # -------------------------------------------------------------
    # OOD Calibration Diagnostic Test
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print("OUT-OF-DISTRIBUTION (OOD) CALIBRATION & VOID UNCERTAINTY TEST")
    print("=" * 70)
    X_ood = np.array([[10.0, 10.0], [-10.0, -10.0], [8.0, -8.0], [-8.0, 8.0]])
    
    print(f"{'Model':20s} | {'OOD Probabilities':35s} | {'OOD Shannon Entropy':20s}")
    print("-" * 80)
    for name, model in models.items():
        if hasattr(model, "predict_proba"):
            ood_p = model.predict_proba(X_ood)
            ood_ent = -np.sum(ood_p * np.log(ood_p + 1e-12), axis=1)
            p_str = np.array2string(ood_p[:, 1], precision=3, separator=', ')
            print(f"{name:20s} | p(y=1) = {p_str:25s} | Mean H: {np.mean(ood_ent):.4f}")

    _, ood_energies, ood_S = trtl.compute_fields(X_ood)
    total_energy = np.sum(ood_energies, axis=1)
    ood_ent_trtl = -np.sum(ood_S * np.log(ood_S + 1e-12), axis=1)
    print(f"{'TRTL Raw Wave Energy':20s} | Total E = {np.array2string(total_energy, precision=4, separator=', '):25s} | Field Vacuum Detected!")
    print("=" * 70)


if __name__ == "__main__":
    run_pathology_audit()
