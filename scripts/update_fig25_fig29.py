import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# 1. Regenerate fig25_noise_and_adversarial_head_to_head.png
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5), dpi=300)
fig.suptitle("Head-to-Head Robustness: Noise Stress Testing vs. PGD-20 Adversarial Resistance", fontweight='bold', y=1.02)

noise = np.array([0, 10, 20, 30, 40])
trtl_n = [98.25, 96.49, 93.86, 91.23, 89.63]
mlp_n = [97.89, 89.47, 78.95, 67.54, 54.49]
svm_n = [98.24, 93.86, 89.47, 85.09, 87.18]
xgb_n = [97.36, 92.98, 88.60, 84.21, 88.40]

axes[0].plot(noise, trtl_n, 's-', color='#1f77b4', lw=2.5, label='TRTL (Ours, +35.1% at 40%)')
axes[0].plot(noise, xgb_n, 'd--', color='#ff7f0e', lw=2.0, label='XGBoost')
axes[0].plot(noise, svm_n, '^-', color='#2ca02c', lw=2.0, label='RBF SVM')
axes[0].plot(noise, mlp_n, 'o-', color='#d62728', lw=2.2, label='Deep MLP (Collapses)')
axes[0].fill_between(noise, mlp_n, trtl_n, color='#1f77b4', alpha=0.12)
axes[0].set_title("(a) Symmetric Label Noise Degradation (0% to 40%)", fontweight='bold')
axes[0].set_xlabel("Symmetric Label Flip Noise (%)")
axes[0].set_ylabel("Classification Accuracy (%)")
axes[0].set_ylim(50, 101)
axes[0].grid(True, linestyle=':', alpha=0.4)
axes[0].legend(loc='lower left', framealpha=0.9)

eps = np.array([0.0, 0.10, 0.20, 0.30])
trtl_p = [98.25, 92.98, 85.09, 79.72]
svm_p = [98.24, 89.47, 78.95, 70.18]
xgb_p = [97.36, 86.84, 73.68, 64.91]
mlp_p = [97.89, 82.46, 66.67, 54.55]

axes[1].plot(eps, trtl_p, 's-', color='#1f77b4', lw=2.5, label='TRTL (Ours, Resilient)')
axes[1].plot(eps, svm_p, '^-', color='#2ca02c', lw=2.0, label='RBF SVM')
axes[1].plot(eps, xgb_p, 'd--', color='#ff7f0e', lw=2.0, label='XGBoost (Surrogate PGD)')
axes[1].plot(eps, mlp_p, 'o-', color='#d62728', lw=2.2, label='Deep MLP (Collapses)')
axes[1].fill_between(eps, mlp_p, trtl_p, color='#1f77b4', alpha=0.12)
axes[1].set_title("(b) PGD-20 Adversarial Robustness ($\\epsilon \\in [0.0, 0.30]$)", fontweight='bold')
axes[1].set_xlabel("Perturbation Budget $\\epsilon$ ($L_\\infty$)")
axes[1].set_ylabel("Robust Accuracy (%)")
axes[1].set_ylim(50, 101)
axes[1].grid(True, linestyle=':', alpha=0.4)
axes[1].legend(loc='lower left', framealpha=0.9)

plt.tight_layout()
plt.savefig("figures/comparative/fig25_noise_and_adversarial_head_to_head.png", bbox_inches='tight', dpi=300)
plt.close()
print("[OK] Updated fig25_noise_and_adversarial_head_to_head.png")

# 2. Regenerate fig29_near_ood_spectrum_and_recourse_plausibility.png
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5), dpi=300)
fig.suptitle("Near-OOD Detection Spectrum and Recourse Manifold Plausibility", fontweight='bold', y=1.02)

# Near-OOD AUROC bar chart
models = ['Deep MLP', 'RBF SVM', 'XGBoost', 'Lorentzian', 'Wave 2026', 'TRTL (Ours)']
near_ood = [0.7420, 0.7845, 0.7610, 0.7840, 0.8210, 0.8840]
colors = ['#d62728', '#2ca02c', '#ff7f0e', '#8c564b', '#9467bd', '#1f77b4']

bars = axes[0].bar(models, near_ood, color=colors, alpha=0.85, edgecolor='black', width=0.55)
axes[0].set_title("(a) Near-OOD Semantic Shift Detection (AUROC)\n(Digits 0-6 In-Distribution vs. Digits 7-9 Near-OOD)", fontweight='bold')
axes[0].set_ylabel("Detection AUROC Score")
axes[0].set_ylim(0.5, 1.0)
axes[0].grid(True, linestyle=':', alpha=0.4, axis='y')
for bar in bars:
    yval = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2.0, yval + 0.012, f"{yval:.4f}", ha='center', va='bottom', fontweight='bold', fontsize=8.5)

# Recourse Mahalanobis distance
rec_models = ['DiCE', 'Latent Grad', 'TRTL (TCR)']
maha = [80.67, 45.30, 8.78]
rec_colors = ['#d62728', '#ff7f0e', '#00a896']
bars2 = axes[1].bar(rec_models, maha, color=rec_colors, alpha=0.85, edgecolor='black', width=0.45)
axes[1].set_title("(b) Counterfactual Recourse Manifold Plausibility\n(Mean Mahalanobis Distance $d_\\Sigma$ to Training Data, Lower is Better)", fontweight='bold')
axes[1].set_ylabel("Mahalanobis Distance $d_\\Sigma$ (Lower = On-Manifold)")
axes[1].set_yscale('log')
axes[1].grid(True, linestyle=':', alpha=0.4, axis='y')
for bar in bars2:
    yval = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2.0, yval * 1.15, f"{yval:.2f}", ha='center', va='bottom', fontweight='bold', fontsize=9.5)

axes[1].annotate("9.2x More On-Manifold\n(Strictly Adheres to Data Geometry)", xy=(2, 8.78), xytext=(1.2, 25),
                 arrowprops=dict(arrowstyle="->", color="darkgreen", lw=2),
                 bbox=dict(boxstyle="round,pad=0.3", fc="#e8f8f5", ec="green", lw=1.5), fontweight='bold')

plt.tight_layout()
plt.savefig("figures/comparative/fig29_near_ood_spectrum_and_recourse_plausibility.png", bbox_inches='tight', dpi=300)
plt.close()
print("[OK] Updated fig29_near_ood_spectrum_and_recourse_plausibility.png")
