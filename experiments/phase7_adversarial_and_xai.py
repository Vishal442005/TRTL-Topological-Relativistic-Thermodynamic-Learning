"""
Phase 7: Adversarial Security & Explainable AI (XAI) Testing Suite
Topological-Relativistic-Thermodynamic Learning (TRTL)

This script executes:
1. Adversarial Robustness Stress-Testing:
   - Fast Gradient Sign Method (FGSM) across perturbation budgets epsilon in [0.0, 0.30]
   - Projected Gradient Descent (PGD-L_inf, 20 iterations, step alpha = epsilon / 4)
   - Benchmarking TRTL vs. Deep MLP and RBF-SVM.
2. Continuous Thermodynamic Counterfactual Recourse (TCR):
   - Gradient flow along nabla_x S_{c*}(x)
   - Head-to-head benchmarking against Wachter's optimization and DiCE proxy
   - Evaluation of path length, curvature, sparsity, and run-time latency.
3. Electro-Potential Manifold Projection (EP-MAP):
   - Conservative force vector field, equipotential contours, and streamline flow.
4. Generates publication-grade Figures 17, 18, 19, 20 (300 DPI PNG & vector PDF).
"""

import os
import sys
import time
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

import torch
import torch.nn as nn
import torch.optim as optim

from sklearn.datasets import load_breast_cancer, make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


# ==============================================================================
# Model Implementations
# ==============================================================================

class PyTorchMLP(nn.Module):
    """Deep Multi-Layer Perceptron with 2 hidden layers and ReLU activations."""
    def __init__(self, in_features, hidden_dim=48):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Linear(hidden_dim // 2, 2)
        )

    def forward(self, x):
        return self.net(x)


class TRTLTorchDifferentiable(nn.Module):
    """
    Fully differentiable PyTorch implementation of TRTL for adversarial
    stress testing and analytical order-parameter gradient computation.
    """
    def __init__(self, X_train, y_train, beta=0.75, k_wave=0.15, mu=1.5,
                 cooling_steps=8, dt=0.04):
        super().__init__()
        self.N, self.D = X_train.shape
        self.classes = np.unique(y_train)
        self.n_classes = len(self.classes)
        self.y_idx = np.searchsorted(self.classes, y_train)

        self.beta = beta
        self.k_wave = k_wave
        self.mu = mu
        self.cooling_steps = cooling_steps
        self.dt = dt

        # Characteristic distance scale
        sub = X_train[:min(self.N, 200)]
        d_sub = cdist(sub, sub)
        pos = d_sub[d_sub > 0]
        self.d_scale = float(np.median(pos)) if len(pos) > 0 else 1.0

        # Precompute Lorentz factors
        d_tr = cdist(X_train, X_train)
        np.fill_diagonal(d_tr, np.inf)
        k_eff = min(7, self.N - 1)
        nn_idx = np.argsort(d_tr, axis=1)[:, :k_eff]
        entropies = np.zeros(self.N)
        for i in range(self.N):
            c = np.bincount(self.y_idx[nn_idx[i]], minlength=self.n_classes)
            p = np.clip(c / np.sum(c), 1e-12, 1.0)
            entropies[i] = -np.sum(p * np.log(p))
        H_max = np.log(self.n_classes) if self.n_classes > 1 else 1.0
        ratio_sq = np.clip((entropies / (H_max + 1e-5)) ** 2, 0.0, 0.99)
        gamma = 1.0 / np.sqrt(1.0 - self.beta * ratio_sq)

        counts = np.bincount(self.y_idx, minlength=self.n_classes)
        weights = 1.0 / np.maximum(counts, 1)

        # Register tensors as buffers
        self.register_buffer("X_train", torch.tensor(X_train, dtype=torch.float32))
        self.register_buffer("y_idx_t", torch.tensor(self.y_idx, dtype=torch.long))
        self.register_buffer("gamma", torch.tensor(gamma, dtype=torch.float32))
        self.register_buffer("class_weights", torch.tensor(weights, dtype=torch.float32))

    def forward(self, X):
        # Pairwise Euclidean distances
        diff = X.unsqueeze(1) - self.X_train.unsqueeze(0) # (M, N, D)
        raw_dists = torch.norm(diff, p=2, dim=2)          # (M, N)
        d_rel = raw_dists * self.gamma.unsqueeze(0)       # (M, N)
        u_d = d_rel / self.d_scale

        w_emit = self.class_weights[self.y_idx_t].unsqueeze(0) # (1, N)
        envelope = torch.exp(-self.mu * (u_d ** 2)) * w_emit

        energies = []
        for c in range(self.n_classes):
            mask_c = (self.y_idx_t == c).unsqueeze(0) # (1, N)
            u_c = torch.where(mask_c, u_d, torch.zeros_like(u_d))
            env_c = torch.where(mask_c, envelope, torch.zeros_like(envelope))

            re_psi = torch.sum(env_c * torch.cos(self.k_wave * u_c), dim=1)
            im_psi = torch.sum(env_c * torch.sin(self.k_wave * u_c), dim=1)
            psi_sq = (re_psi ** 2) + (im_psi ** 2)
            energies.append(psi_sq)

        E = torch.stack(energies, dim=1) # (M, C)

        # Cross-class competitive wave inhibition
        if self.n_classes > 1:
            E_total = torch.sum(E, dim=1, keepdim=True)
            cross_inhibition = (E_total - E) / (self.n_classes - 1)
            E = torch.clamp(E - 0.20 * cross_inhibition, min=0.0)

        # Initial order parameter
        S = E / (torch.sum(E, dim=1, keepdim=True) + 1e-12)

        # Thermodynamic relaxation
        h_field = S.clone()
        for _ in range(self.cooling_steps):
            S_sq_sum = torch.sum(S ** 2, dim=1, keepdim=True)
            repulsion = 2.0 * S * (S_sq_sum - S ** 2)
            dF = -1.5 * S + (S ** 3) - h_field + repulsion
            S = torch.clamp(S - self.dt * dF, min=0.0, max=1.0)
            S = S / (torch.sum(S, dim=1, keepdim=True) + 1e-12)

        return S


# ==============================================================================
# 1. Adversarial Robustness Benchmark: FGSM and PGD-L_inf
# ==============================================================================

def train_mlp_model(X_train, y_train, epochs=250):
    model = PyTorchMLP(in_features=X_train.shape[1])
    optimizer = optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()

    X_t = torch.tensor(X_train, dtype=torch.float32)
    y_t = torch.tensor(y_train, dtype=torch.long)

    model.train()
    for _ in range(epochs):
        optimizer.zero_grad()
        out = model(X_t)
        loss = criterion(out, y_t)
        loss.backward()
        optimizer.step()

    return model


def attack_fgsm(model, X, y, epsilon, is_trtl=False):
    """Fast Gradient Sign Method (FGSM) attack."""
    if epsilon == 0.0:
        return X.clone()

    X_adv = X.clone().detach().requires_grad_(True)
    if is_trtl:
        probs = model(X_adv)
        # Maximize loss: negative log likelihood of true class
        loss = -torch.mean(torch.log(torch.clamp(probs[torch.arange(len(y)), y], min=1e-8)))
    else:
        logits = model(X_adv)
        loss = nn.CrossEntropyLoss()(logits, y)

    loss.backward()
    grad_sign = X_adv.grad.data.sign()
    X_adv = X_adv + epsilon * grad_sign
    return X_adv.detach()


def attack_pgd_linf(model, X, y, epsilon, steps=20, is_trtl=False):
    """Projected Gradient Descent (PGD-L_inf) attack."""
    if epsilon == 0.0:
        return X.clone()

    alpha = epsilon / 4.0
    X_adv = X.clone().detach()

    for _ in range(steps):
        X_adv.requires_grad_(True)
        if is_trtl:
            probs = model(X_adv)
            loss = -torch.mean(torch.log(torch.clamp(probs[torch.arange(len(y)), y], min=1e-8)))
        else:
            logits = model(X_adv)
            loss = nn.CrossEntropyLoss()(logits, y)

        loss.backward()
        grad_sign = X_adv.grad.data.sign()
        X_adv = X_adv.detach() + alpha * grad_sign

        # Project back into L_inf ball
        eta = torch.clamp(X_adv - X, min=-epsilon, max=epsilon)
        X_adv = X + eta

    return X_adv.detach()


def run_adversarial_suite(X_tr, X_te, y_tr, y_te):
    print("=" * 70)
    print("EXPERIMENT 1: WHITE-BOX ADVERSARIAL STRESS-TESTING (FGSM & PGD-L_inf)")
    print("=" * 70)

    # 1. Train models
    print("[*] Training PyTorch Deep MLP...")
    mlp = train_mlp_model(X_tr, y_tr)
    mlp.eval()

    print("[*] Constructing Differentiable TRTL Engine...")
    trtl = TRTLTorchDifferentiable(X_tr, y_tr)
    trtl.eval()

    print("[*] Fitting Baseline RBF SVM...")
    svm = SVC(kernel='rbf', probability=True, random_state=42)
    svm.fit(X_tr, y_tr)

    eps_range = [0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    X_te_t = torch.tensor(X_te, dtype=torch.float32)
    y_te_t = torch.tensor(y_te, dtype=torch.long)

    fgsm_mlp_acc, fgsm_trtl_acc, fgsm_svm_acc = [], [], []
    pgd_mlp_acc, pgd_trtl_acc = [], []

    for eps in eps_range:
        # FGSM Attacks
        adv_mlp = attack_fgsm(mlp, X_te_t, y_te_t, eps, is_trtl=False)
        adv_trtl = attack_fgsm(trtl, X_te_t, y_te_t, eps, is_trtl=True)

        # MLP Accuracy under FGSM
        with torch.no_grad():
            acc_mlp = (mlp(adv_mlp).argmax(dim=1) == y_te_t).float().mean().item()
            acc_trtl = (trtl(adv_trtl).argmax(dim=1) == y_te_t).float().mean().item()
            acc_svm = accuracy_score(y_te, svm.predict(adv_mlp.numpy()))

        fgsm_mlp_acc.append(acc_mlp)
        fgsm_trtl_acc.append(acc_trtl)
        fgsm_svm_acc.append(acc_svm)

        # PGD-L_inf Attacks
        pgd_adv_mlp = attack_pgd_linf(mlp, X_te_t, y_te_t, eps, steps=20, is_trtl=False)
        pgd_adv_trtl = attack_pgd_linf(trtl, X_te_t, y_te_t, eps, steps=20, is_trtl=True)

        with torch.no_grad():
            p_acc_mlp = (mlp(pgd_adv_mlp).argmax(dim=1) == y_te_t).float().mean().item()
            p_acc_trtl = (trtl(pgd_adv_trtl).argmax(dim=1) == y_te_t).float().mean().item()

        pgd_mlp_acc.append(p_acc_mlp)
        pgd_trtl_acc.append(p_acc_trtl)

        print(f"    eps={eps:.2f} | FGSM: MLP={acc_mlp:.4f}, SVM={acc_svm:.4f}, TRTL={acc_trtl:.4f} "
              f"| PGD-20: MLP={p_acc_mlp:.4f}, TRTL={p_acc_trtl:.4f}")

    return eps_range, fgsm_mlp_acc, fgsm_svm_acc, fgsm_trtl_acc, pgd_mlp_acc, pgd_trtl_acc, trtl, mlp


# ==============================================================================
# 2. Continuous Thermodynamic Counterfactual Recourse (TCR) Suite
# ==============================================================================

def compute_tcr_path(trtl_model, x_0, target_class=1, max_steps=100, eta=0.08, lambda_reg=0.01):
    """Computes the continuous thermodynamic gradient flow counterfactual path."""
    x = x_0.clone().detach().unsqueeze(0).requires_grad_(True)
    path = [x.detach().squeeze(0).numpy().copy()]
    t_start = time.perf_counter()

    for _ in range(max_steps):
        probs = trtl_model(x)
        p_target = probs[0, target_class]

        if p_target.item() >= 0.50:
            break

        # Maximize target class order parameter while minimizing deviation
        objective = p_target - 0.5 * lambda_reg * torch.sum((x - x_0.unsqueeze(0)) ** 2)
        objective.backward()

        with torch.no_grad():
            grad = x.grad.data
            grad_norm = torch.norm(grad)
            if grad_norm > 1e-6:
                x.data += eta * (grad / grad_norm)
            x.grad.zero_()

        path.append(x.detach().squeeze(0).numpy().copy())

    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    return np.array(path), elapsed_ms


def compute_wachter_path(mlp_model, x_0, target_class=1, max_steps=100, lr=0.05, lambda_l1=0.02):
    """Classical Wachter et al. (2017) L1-penalized gradient counterfactual."""
    x = x_0.clone().detach().unsqueeze(0).requires_grad_(True)
    path = [x.detach().squeeze(0).numpy().copy()]
    t_start = time.perf_counter()

    for _ in range(max_steps):
        logits = mlp_model(x)
        probs = torch.softmax(logits, dim=1)
        p_target = probs[0, target_class]

        if p_target.item() >= 0.50:
            break

        # Loss = BCE(p_target, 1.0) + lambda * L1(x - x_0)
        loss = -torch.log(torch.clamp(p_target, min=1e-8)) + lambda_l1 * torch.sum(torch.abs(x - x_0.unsqueeze(0)))
        loss.backward()

        with torch.no_grad():
            x.data -= lr * x.grad.data
            x.grad.zero_()

        path.append(x.detach().squeeze(0).numpy().copy())

    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    return np.array(path), elapsed_ms


def compute_dice_proxy_path(mlp_model, x_0, target_class=1, max_steps=100, step_size=0.08):
    """DiCE proxy: Coordinate greedy search along high-gradient features."""
    x = x_0.clone().detach().numpy().copy()
    path = [x.copy()]
    t_start = time.perf_counter()

    for _ in range(max_steps):
        x_t = torch.tensor(x, dtype=torch.float32).unsqueeze(0).requires_grad_(True)
        logits = mlp_model(x_t)
        probs = torch.softmax(logits, dim=1)
        if probs[0, target_class].item() >= 0.50:
            break

        probs[0, target_class].backward()
        grad = x_t.grad.data.squeeze(0).numpy()

        # Step along the single most sensitive coordinate (sparse orthogonal move)
        best_coord = np.argmax(np.abs(grad))
        x[best_coord] += step_size * np.sign(grad[best_coord])
        path.append(x.copy())

    elapsed_ms = (time.perf_counter() - t_start) * 1000.0
    return np.array(path), elapsed_ms


def evaluate_trajectory_metrics(path):
    """Calculates path length, total curvature, and sparsity."""
    diffs = np.diff(path, axis=0)
    step_lens = np.linalg.norm(diffs, axis=1)
    total_length = np.sum(step_lens)

    # Curvature (sum of angular changes between consecutive tangent vectors)
    if len(diffs) > 1:
        unit_v = diffs / (step_lens[:, np.newaxis] + 1e-12)
        curvature = np.sum(np.linalg.norm(np.diff(unit_v, axis=0), axis=1))
    else:
        curvature = 0.0

    # Sparsity (number of coordinates changed from origin)
    total_disp = np.abs(path[-1] - path[0])
    sparsity = np.sum(total_disp > 0.05)

    return total_length, curvature, sparsity


def run_counterfactual_suite(trtl, mlp, X_te, y_te, n_queries=30):
    print("\n" + "=" * 70)
    print("EXPERIMENT 2: COUNTERFACTUAL RECOURSE HEAD-TO-HEAD BENCHMARK")
    print("=" * 70)

    # Select queries from class 0
    c0_indices = np.where(y_te == 0)[0][:n_queries]

    tcr_lens, tcr_curvs, tcr_latencies = [], [], []
    wachter_lens, wachter_curvs, wachter_latencies = [], [], []
    dice_lens, dice_curvs, dice_latencies = [], [], []

    sample_paths = {}

    for idx in c0_indices:
        x_0_t = torch.tensor(X_te[idx], dtype=torch.float32)

        # 1. TCR
        p_tcr, t_tcr = compute_tcr_path(trtl, x_0_t, target_class=1)
        l_tcr, c_tcr, _ = evaluate_trajectory_metrics(p_tcr)
        tcr_lens.append(l_tcr)
        tcr_curvs.append(c_tcr)
        tcr_latencies.append(t_tcr)

        # 2. Wachter
        p_wach, t_wach = compute_wachter_path(mlp, x_0_t, target_class=1)
        l_wach, c_wach, _ = evaluate_trajectory_metrics(p_wach)
        wachter_lens.append(l_wach)
        wachter_curvs.append(c_wach)
        wachter_latencies.append(t_wach)

        # 3. DiCE Proxy
        p_dice, t_dice = compute_dice_proxy_path(mlp, x_0_t, target_class=1)
        l_dice, c_dice, _ = evaluate_trajectory_metrics(p_dice)
        dice_lens.append(l_dice)
        dice_curvs.append(c_dice)
        dice_latencies.append(t_dice)

        if len(sample_paths) == 0:
            sample_paths["TCR"] = p_tcr
            sample_paths["Wachter"] = p_wach
            sample_paths["DiCE"] = p_dice

    print("\n[*] Recourse Performance Summary (Mean across 30 Queries):")
    print(f"    TCR (Proposed)     | Length: {np.mean(tcr_lens):.3f} | Curvature: {np.mean(tcr_curvs):.3f} | Latency: {np.mean(tcr_latencies):.2f} ms")
    print(f"    Wachter's Method   | Length: {np.mean(wachter_lens):.3f} | Curvature: {np.mean(wachter_curvs):.3f} | Latency: {np.mean(wachter_latencies):.2f} ms")
    print(f"    DiCE Greedy Search | Length: {np.mean(dice_lens):.3f} | Curvature: {np.mean(dice_curvs):.3f} | Latency: {np.mean(dice_latencies):.2f} ms")

    return sample_paths, (tcr_lens, wachter_lens, dice_lens), (tcr_curvs, wachter_curvs, dice_curvs), (tcr_latencies, wachter_latencies, dice_latencies)


# ==============================================================================
# 3. Visualization Pipeline: Figures 17, 18, 19, 20
# ==============================================================================

def generate_phase7_figures(eps_range, fgsm_mlp, fgsm_svm, fgsm_trtl, pgd_mlp, pgd_trtl,
                            sample_paths, lens_data, curvs_data, lat_data, X_tr, y_tr):
    fig_dir = os.path.join("figures", "phase7")
    ensure_dir(fig_dir)
    plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 13})

    # --------------------------------------------------------------------------
    # Figure 17: Adversarial Vulnerability Curves (FGSM and PGD-L_inf)
    # --------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), constrained_layout=True)

    # Subplot 1: FGSM
    ax1.plot(eps_range, fgsm_mlp, 'r-o', linewidth=2.2, label='Deep MLP')
    ax1.plot(eps_range, fgsm_svm, 'g--s', linewidth=2.2, label='RBF SVM')
    ax1.plot(eps_range, fgsm_trtl, 'b-^', linewidth=2.5, label='TRTL (Proposed)')
    ax1.set_xlabel(r"Perturbation Budget $\epsilon$ ($L_\infty$)")
    ax1.set_ylabel("Clean Test Accuracy")
    ax1.set_title("Fast Gradient Sign Method (FGSM) Resilience")
    ax1.legend(frameon=True)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-0.02, 1.02)

    # Subplot 2: PGD-L_inf
    ax2.plot(eps_range, pgd_mlp, 'r-o', linewidth=2.2, label='Deep MLP (PGD-20)')
    ax2.plot(eps_range, pgd_trtl, 'b-^', linewidth=2.5, label='TRTL (PGD-20)')
    ax2.set_xlabel(r"Perturbation Budget $\epsilon$ ($L_\infty$)")
    ax2.set_ylabel("Clean Test Accuracy")
    ax2.set_title(r"Projected Gradient Descent (PGD-$L_\infty$, 20 Steps)")
    ax2.legend(frameon=True)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-0.02, 1.02)

    fig17_png = os.path.join(fig_dir, "fig17_adversarial_robustness_curves.png")
    fig17_pdf = os.path.join(fig_dir, "fig17_adversarial_robustness_curves.pdf")
    plt.savefig(fig17_png, dpi=300)
    plt.savefig(fig17_pdf)
    plt.close()
    print(f"[OK] Saved Figure 17 to {fig17_png} and {fig17_pdf}")

    # --------------------------------------------------------------------------
    # Figure 18: Continuous Recourse Trajectories on 2D Manifold
    # --------------------------------------------------------------------------
    # Train 2D TRTL for clear spatial visualization
    np.random.seed(42)
    X_m, y_m = make_moons(n_samples=400, noise=0.15, random_state=42)
    s2d = StandardScaler()
    X_m_s = s2d.fit_transform(X_m)
    trtl_2d = TRTLTorchDifferentiable(X_m_s, y_m, beta=0.75, k_wave=0.20, mu=1.2)
    mlp_2d = train_mlp_model(X_m_s, y_m, epochs=250)

    # Source point in class 0
    x_source = torch.tensor([-0.8, -0.6], dtype=torch.float32)
    p_tcr_2d, _ = compute_tcr_path(trtl_2d, x_source, target_class=1, max_steps=120, eta=0.06)
    p_wach_2d, _ = compute_wachter_path(mlp_2d, x_source, target_class=1, max_steps=120, lr=0.05)
    p_dice_2d, _ = compute_dice_proxy_path(mlp_2d, x_source, target_class=1, max_steps=120, step_size=0.06)

    fig, ax = plt.subplots(figsize=(8.5, 6.5), constrained_layout=True)
    # Background order parameter
    gx = np.linspace(-2.5, 2.5, 120)
    gy = np.linspace(-2.5, 2.5, 120)
    GX, GY = np.meshgrid(gx, gy)
    grid_pts = torch.tensor(np.c_[GX.ravel(), GY.ravel()], dtype=torch.float32)
    with torch.no_grad():
        S_grid = trtl_2d(grid_pts)[:, 1].numpy().reshape(GX.shape)

    cf = ax.contourf(GX, GY, S_grid, levels=25, cmap='RdBu', alpha=0.65)
    cbar = plt.colorbar(cf, ax=ax)
    cbar.set_label("Target Class Order Parameter $S_{c=1}$")
    ax.contour(GX, GY, S_grid, levels=[0.5], colors='black', linewidths=2.0, linestyles='--')

    # Data anchors
    ax.scatter(X_m_s[y_m == 0, 0], X_m_s[y_m == 0, 1], c='red', s=18, alpha=0.4, label='Class 0 (Source)')
    ax.scatter(X_m_s[y_m == 1, 0], X_m_s[y_m == 1, 1], c='blue', s=18, alpha=0.4, label='Class 1 (Target)')

    # Trajectories
    ax.plot(p_tcr_2d[:, 0], p_tcr_2d[:, 1], 'b-o', markersize=4, linewidth=2.5, label='TCR (Proposed Path)')
    ax.plot(p_wach_2d[:, 0], p_wach_2d[:, 1], 'g--s', markersize=4, linewidth=2.0, label="Wachter's Path")
    ax.plot(p_dice_2d[:, 0], p_dice_2d[:, 1], 'm:^', markersize=4, linewidth=2.0, label='DiCE Greedy Path')

    ax.scatter(x_source[0], x_source[1], c='gold', edgecolors='black', s=140, zorder=5, marker='*', label='Origin Factual $x_0$')
    ax.set_title("Continuous Thermodynamic Counterfactual Recourse vs. Classical XAI")
    ax.set_xlabel("Latent Coordinate $z_1$")
    ax.set_ylabel("Latent Coordinate $z_2$")
    ax.legend(loc='lower left', frameon=True)

    fig18_png = os.path.join(fig_dir, "fig18_counterfactual_recourse_trajectories.png")
    fig18_pdf = os.path.join(fig_dir, "fig18_counterfactual_recourse_trajectories.pdf")
    plt.savefig(fig18_png, dpi=300)
    plt.savefig(fig18_pdf)
    plt.close()
    print(f"[OK] Saved Figure 18 to {fig18_png} and {fig18_pdf}")

    # --------------------------------------------------------------------------
    # Figure 19: Recourse Benchmark Multi-Metric Bar Chart
    # --------------------------------------------------------------------------
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5), constrained_layout=True)

    methods = ["TCR", "Wachter", "DiCE"]
    colors = ['#1f77b4', '#2ca02c', '#d62728']

    # Path length
    mean_lens = [np.mean(d) for d in lens_data]
    std_lens = [np.std(d) for d in lens_data]
    ax1.bar(methods, mean_lens, yerr=std_lens, capsize=5, color=colors, alpha=0.85, edgecolor='black')
    ax1.set_ylabel("Path Length $L_2$")
    ax1.set_title("Recourse Proximity (Lower is Better)")
    ax1.grid(axis='y', alpha=0.3)

    # Curvature
    mean_curvs = [np.mean(d) for d in curvs_data]
    std_curvs = [np.std(d) for d in curvs_data]
    ax2.bar(methods, mean_curvs, yerr=std_curvs, capsize=5, color=colors, alpha=0.85, edgecolor='black')
    ax2.set_ylabel(r"Total Curvature $\kappa$")
    ax2.set_title("Path Smoothness (Lower is Better)")
    ax2.grid(axis='y', alpha=0.3)

    # Latency
    mean_lat = [np.mean(d) for d in lat_data]
    std_lat = [np.std(d) for d in lat_data]
    ax3.bar(methods, mean_lat, yerr=std_lat, capsize=5, color=colors, alpha=0.85, edgecolor='black')
    ax3.set_ylabel("Computation Latency (ms)")
    ax3.set_title("Execution Speed (Lower is Better)")
    ax3.grid(axis='y', alpha=0.3)

    fig19_png = os.path.join(fig_dir, "fig19_xai_recourse_benchmark_metrics.png")
    fig19_pdf = os.path.join(fig_dir, "fig19_xai_recourse_benchmark_metrics.pdf")
    plt.savefig(fig19_png, dpi=300)
    plt.savefig(fig19_pdf)
    plt.close()
    print(f"[OK] Saved Figure 19 to {fig19_png} and {fig19_pdf}")

    # --------------------------------------------------------------------------
    # Figure 20: EP-MAP Phase Portrait (Force Field & Streamlines)
    # --------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8.5, 6.5), constrained_layout=True)

    # Compute numerical force field F(x) = -nabla S_0(x) = +nabla S_1(x)
    dx = gx[1] - gx[0]
    dy = gy[1] - gy[0]
    dF_dy, dF_dx = np.gradient(S_grid, dy, dx)

    st = ax.streamplot(GX, GY, dF_dx, dF_dy, color=np.sqrt(dF_dx**2 + dF_dy**2),
                      cmap='autumn', density=1.2, linewidth=1.2, arrowsize=1.2)
    cbar = plt.colorbar(st.lines, ax=ax)
    cbar.set_label(r"Force Magnitude $\|\mathbf{F}(\mathbf{x})\|$")

    ax.contour(GX, GY, S_grid, levels=15, colors='gray', alpha=0.4, linewidths=0.8)
    ax.contour(GX, GY, S_grid, levels=[0.5], colors='black', linewidths=2.2, linestyles='--')

    ax.scatter(X_m_s[y_m == 0, 0], X_m_s[y_m == 0, 1], c='red', s=22, alpha=0.5, label='Class 0 Well')
    ax.scatter(X_m_s[y_m == 1, 0], X_m_s[y_m == 1, 1], c='blue', s=22, alpha=0.5, label='Class 1 Well')

    ax.set_title("EP-MAP: Conservative Force Field and Recourse Streamlines")
    ax.set_xlabel("Phase Coordinate $z_1$")
    ax.set_ylabel("Phase Coordinate $z_2$")
    ax.legend(loc='lower left', frameon=True)

    fig20_png = os.path.join(fig_dir, "fig20_ep_map_force_field_and_streamlines.png")
    fig20_pdf = os.path.join(fig_dir, "fig20_ep_map_force_field_and_streamlines.pdf")
    plt.savefig(fig20_png, dpi=300)
    plt.savefig(fig20_pdf)
    plt.close()
    print(f"[OK] Saved Figure 20 to {fig20_png} and {fig20_pdf}")


# ==============================================================================
# Main Runner
# ==============================================================================

if __name__ == "__main__":
    bc = load_breast_cancer()
    scaler = StandardScaler()
    X = scaler.fit_transform(bc.data)
    y = bc.target

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    eps_range, fgsm_mlp, fgsm_svm, fgsm_trtl, pgd_mlp, pgd_trtl, trtl, mlp = run_adversarial_suite(
        X_tr, X_te, y_tr, y_te)

    sample_paths, lens_data, curvs_data, lat_data = run_counterfactual_suite(
        trtl, mlp, X_te, y_te, n_queries=30)

    generate_phase7_figures(eps_range, fgsm_mlp, fgsm_svm, fgsm_trtl, pgd_mlp, pgd_trtl,
                            sample_paths, lens_data, curvs_data, lat_data, X_tr, y_tr)
