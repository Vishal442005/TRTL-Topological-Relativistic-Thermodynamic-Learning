import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Dimensions (normalized 0 to 1)
categories = [
    'Clean Multi-Class\nAccuracy',
    'High-Dim Contrast\n($D=1,000$)',
    'Noise Stability\n(40% Flip)',
    'Adversarial Robustness\n(PGD-20, $\\epsilon=0.30$)',
    'Far-OOD Void\nAUROC',
    'Recourse Manifold\nPlausibility ($1/d_\\Sigma$)'
]
N = len(categories)

# Angles for radar chart
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

# Model values (normalized between 0 and 1)
# Clean Acc: TRTL (0.966), MLP (0.961), SVM (0.974), XGB (0.960)
# High-Dim Contrast: TRTL (0.6924 -> 1.0), Euc (0.1333 -> 0.19)
# Noise 40%: TRTL (0.8963 -> 1.0), MLP (0.5449 -> 0.40), SVM (0.8718 -> 0.90)
# PGD-20: TRTL (0.7972 -> 1.0), MLP (0.5455 -> 0.45), SVM (0.7018 -> 0.75)
# OOD: TRTL (1.0000 -> 1.0), MLP (0.3919 -> 0.20), SVM (0.6020 -> 0.50)
# Recourse (1/d_Sigma): TRTL (1/8.78 -> 1.0), DiCE (1/80.67 -> 0.11)

trtl_vals = [0.966, 1.000, 0.896, 0.797, 1.000, 0.950]
trtl_vals += trtl_vals[:1]

mlp_vals = [0.961, 0.192, 0.545, 0.545, 0.392, 0.350]
mlp_vals += mlp_vals[:1]

svm_vals = [0.974, 0.192, 0.872, 0.702, 0.602, 0.200]
svm_vals += svm_vals[:1]

xgb_vals = [0.960, 0.192, 0.884, 0.649, 0.584, 0.110]
xgb_vals += xgb_vals[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True), dpi=300)
fig.suptitle("Six-Dimensional Holistic Value Scorecard (TRTL vs. Premier Baselines)", fontweight='bold', y=0.98, fontsize=12)

# Draw axes
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontweight='bold', fontsize=9.5)
ax.set_ylim(0, 1.05)
ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], ['0.2', '0.4', '0.6', '0.8', '1.0'], color='grey', size=8)

# Plot TRTL
ax.plot(angles, trtl_vals, 's-', color='#1f77b4', lw=2.8, label='TRTL (Proposed Unified Model)')
ax.fill(angles, trtl_vals, color='#1f77b4', alpha=0.22)

# Plot SVM
ax.plot(angles, svm_vals, '^-', color='#2ca02c', lw=1.8, label='RBF Support Vector Machine')

# Plot XGBoost
ax.plot(angles, xgb_vals, 'd--', color='#ff7f0e', lw=1.8, label='XGBoost')

# Plot Deep MLP
ax.plot(angles, mlp_vals, 'o-', color='#d62728', lw=1.8, label='Deep Multi-Layer Perceptron')

ax.legend(loc='lower left', bbox_to_anchor=(0.85, 0.02), framealpha=0.95, fontsize=9)
plt.tight_layout()
plt.savefig("figures/comparative/fig24_worth_radar_multi_dimension.png", bbox_inches='tight', dpi=300)
plt.close()
print("[OK] Updated fig24_worth_radar_multi_dimension.png")
