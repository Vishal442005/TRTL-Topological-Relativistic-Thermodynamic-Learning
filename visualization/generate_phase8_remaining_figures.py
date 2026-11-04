"""
Phase 8: Additional Publication Graphics Engine (Figures 21, 22, 23)
Topological-Relativistic-Thermodynamic Learning (TRTL)

Completes the 23-figure publication-grade portfolio:
- Figure 21: Tri-Zone Topological Anatomy & Certified Invariance Spheres
- Figure 22: Relativistic Geodesic Deflection on 3D Potential Surface
- Figure 23: Complete TRTL End-to-End Architectural Flowchart & Inference Pipeline
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle
import matplotlib.patheffects as pe


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def generate_figure21(fig_dir):
    """Figure 21: Tri-Zone Topological Anatomy & Certified Invariance Spheres."""
    fig, ax = plt.subplots(figsize=(8.0, 7.5), constrained_layout=True)

    # Center anchor
    x0, y0 = 0.0, 0.0

    # Zone 3: Vacuum Horizon boundary
    c_vac = Circle((x0, y0), 3.2, color='#f0f4f8', ec='#94a3b8', linestyle='--', linewidth=2.0, label='Zero-Support Vacuum Horizon ($R_{cut}$)')
    ax.add_patch(c_vac)

    # Zone 2: Exponential Decay Shell
    c_decay = Circle((x0, y0), 2.0, color='#dbeafe', ec='#3b82f6', linestyle='-', linewidth=2.2, label='Relativistic Decay Shell ($R_{decay}$)')
    ax.add_patch(c_decay)

    # Zone 1: Deterministic Certainty Core
    c_core = Circle((x0, y0), 0.9, color='#93c5fd', ec='#1d4ed8', linestyle='-', linewidth=2.5, label='Deterministic Certainty Core ($R_{core}$)')
    ax.add_patch(c_core)

    # Certified Invariance Sphere
    c_cert = Circle((x0, y0), 0.55, color='#fbbf24', ec='#d97706', linewidth=2.5, linestyle=':', label=r'Certified $L_2$ Invariance Sphere ($r_{cert}$)')
    ax.add_patch(c_cert)

    # Anchor point
    ax.scatter(x0, y0, c='red', s=120, zorder=6, edgecolors='black', label=r'Support Anchor $\mathbf{x}_i$')

    # Radial dimension lines and annotations
    ax.annotate(r'$r_{cert}$', xy=(0.35, 0.35), xytext=(0.8, 0.9),
                arrowprops=dict(arrowstyle="->", color='#b45309', lw=1.5),
                fontsize=11, fontweight='bold', color='#b45309')

    ax.annotate(r'$R_{core}$', xy=(0.65, -0.65), xytext=(1.2, -1.1),
                arrowprops=dict(arrowstyle="->", color='#1d4ed8', lw=1.5),
                fontsize=11, fontweight='bold', color='#1d4ed8')

    ax.annotate(r'$R_{decay}$', xy=(-1.4, 1.4), xytext=(-2.3, 2.1),
                arrowprops=dict(arrowstyle="->", color='#2563eb', lw=1.5),
                fontsize=11, fontweight='bold', color='#2563eb')

    ax.annotate(r'$R_{cut}$', xy=(-2.2, -2.2), xytext=(-3.1, -2.9),
                arrowprops=dict(arrowstyle="->", color='#64748b', lw=1.5),
                fontsize=11, fontweight='bold', color='#64748b')

    # Adversarial perturbation vector inside cert ball
    ax.annotate("", xy=(0.25, -0.35), xytext=(0.0, 0.0),
                arrowprops=dict(arrowstyle="->", color='darkred', lw=2.5))
    ax.text(0.15, -0.22, r'$\boldsymbol{\delta} \in \mathcal{B}_2(r_{cert})$', fontsize=10, fontweight='bold', color='darkred')

    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(-3.6, 3.6)
    ax.set_aspect('equal')
    ax.set_title("Tri-Zone Topological Anchor Anatomy & Certified Invariance Geometry", fontsize=12, pad=12)
    ax.legend(loc='upper right', frameon=True, fontsize=9.5)
    ax.grid(True, alpha=0.25)

    png_path = os.path.join(fig_dir, "fig21_trizone_topological_anatomy.png")
    pdf_path = os.path.join(fig_dir, "fig21_trizone_topological_anatomy.pdf")
    plt.savefig(png_path, dpi=300)
    plt.savefig(pdf_path)
    plt.close()
    print(f"[OK] Saved Figure 21 to {png_path} and {pdf_path}")


def generate_figure22(fig_dir):
    """Figure 22: Relativistic Geodesic Deflection on 3D Potential Surface."""
    fig = plt.figure(figsize=(10, 7.5))
    ax = fig.add_subplot(111, projection='3d')

    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x, y)

    # 3D Double-well free energy surface with central entropic barrier
    Z = 0.5 * (X**4 - 3*X**2 + Y**2) + 1.2 * np.exp(-((X**2 + Y**2) / 0.8))

    surf = ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.75, edgecolor='none', antialiased=True)
    cbar = fig.colorbar(surf, ax=ax, shrink=0.55, aspect=10)
    cbar.set_label("Thermodynamic Free Energy $\\mathcal{F}(\\mathbf{x})$")

    # Geodesic particle trajectory deflecting away from central ridge
    t = np.linspace(0, 1, 100)
    x_geo = -2.2 + 2.0 * t - 0.6 * np.sin(np.pi * t)
    y_geo = 1.8 - 2.8 * t + 0.8 * np.sin(np.pi * t)
    z_geo = 0.5 * (x_geo**4 - 3*x_geo**2 + y_geo**2) + 1.2 * np.exp(-((x_geo**2 + y_geo**2) / 0.8)) + 0.15

    ax.plot(x_geo, y_geo, z_geo, color='black', linewidth=3.0, label='Relativistic Geodesic $\\gamma(t)$')
    ax.scatter([x_geo[0]], [y_geo[0]], [z_geo[0]], color='green', s=100, label='Query Origin $\\mathbf{x}_0$')
    ax.scatter([x_geo[-1]], [y_geo[-1]], [z_geo[-1]], color='blue', s=100, label='Ground State Equilibrium')

    ax.set_title("Relativistic Geodesic Deflection across Entropic Horizon Ridge", fontsize=12, pad=15)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_zlabel("$\\mathcal{F}(\\mathbf{x})$")
    ax.view_init(elev=32, azim=-55)
    ax.legend(loc='upper right', frameon=True, fontsize=10)

    png_path = os.path.join(fig_dir, "fig22_geodesic_deflection_3d_surface.png")
    pdf_path = os.path.join(fig_dir, "fig22_geodesic_deflection_3d_surface.pdf")
    plt.savefig(png_path, dpi=300)
    plt.savefig(pdf_path)
    plt.close()
    print(f"[OK] Saved Figure 22 to {png_path} and {pdf_path}")


def generate_figure23(fig_dir):
    """Figure 23: Complete TRTL End-to-End Architectural Flowchart & Inference Pipeline."""
    fig, ax = plt.subplots(figsize=(12, 6.5), constrained_layout=True)

    # Stage boxes
    boxes = [
        ("Query Input\nx in R^D", 0.05, 0.40, 0.12, 0.20, '#f1f5f9', '#475569'),
        ("Stage I: RAMD\nMetric Dilatation\ngamma_i = (1 - beta H^2)^{-1/2}\nBall-Tree Pruning (R_cut)", 0.22, 0.32, 0.22, 0.36, '#dbeafe', '#1d4ed8'),
        ("Stage II: TWIL\nCoherent Wavefield\nPsi_c(x) = sum psi_i(x)\nCross-Class Inhibition", 0.49, 0.32, 0.22, 0.36, '#e0e7ff', '#4338ca'),
        ("Stage III: TPTC\nGinzburg-Landau Relax\nS^{(k+1)} = Pi(S^{(k)} - dt dF)\nOrder Crystallization", 0.76, 0.32, 0.20, 0.36, '#dcfce7', '#15803d'),
    ]

    for label, x, y, w, h, bg, ec in boxes:
        rect = Rectangle((x, y), w, h, facecolor=bg, edgecolor=ec, linewidth=2.0, transform=ax.transAxes, zorder=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2, label, ha='center', va='center', transform=ax.transAxes,
                fontsize=10.5, fontweight='bold', color=ec, zorder=3)

    # Output branch 1: Class Prediction & Order Parameter
    out_rect = Rectangle((0.80, 0.76), 0.18, 0.16, facecolor='#fef3c7', edgecolor='#b45309', linewidth=2.0, transform=ax.transAxes)
    ax.add_patch(out_rect)
    ax.text(0.89, 0.84, "Deterministic Output\ny* = argmax S_c\nCertainty C = max S_c", ha='center', va='center',
            transform=ax.transAxes, fontsize=10, fontweight='bold', color='#b45309')

    # Output branch 2: Certified Robustness & Recourse
    xai_rect = Rectangle((0.80, 0.08), 0.18, 0.16, facecolor='#fce7f3', edgecolor='#be185d', linewidth=2.0, transform=ax.transAxes)
    ax.add_patch(xai_rect)
    ax.text(0.89, 0.16, "Certified XAI & Security\nRadius r_{cert} Invariance\nRecourse dot{x} = nabla S*", ha='center', va='center',
            transform=ax.transAxes, fontsize=10, fontweight='bold', color='#be185d')

    # Arrows connecting stages
    arrows = [
        ((0.17, 0.50), (0.22, 0.50)),
        ((0.44, 0.50), (0.49, 0.50)),
        ((0.71, 0.50), (0.76, 0.50)),
        ((0.86, 0.68), (0.86, 0.76)),
        ((0.86, 0.32), (0.86, 0.24)),
    ]

    for start, end in arrows:
        ax.annotate("", xy=end, xytext=start, xycoords='axes fraction', textcoords='axes fraction',
                    arrowprops=dict(arrowstyle="-|>", color='#1e293b', lw=2.2, mutation_scale=15), zorder=4)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title("TRTL End-to-End Inference Pipeline: From Metric Warping to Thermodynamic Crystallization", fontsize=13, pad=15)

    png_path = os.path.join(fig_dir, "fig23_trtl_end_to_end_flowchart_pipeline.png")
    pdf_path = os.path.join(fig_dir, "fig23_trtl_end_to_end_flowchart_pipeline.pdf")
    plt.savefig(png_path, dpi=300)
    plt.savefig(pdf_path)
    plt.close()
    print(f"[OK] Saved Figure 23 to {png_path} and {pdf_path}")


if __name__ == "__main__":
    fig_dir = os.path.join("figures", "phase8")
    ensure_dir(fig_dir)
    generate_figure21(fig_dir)
    generate_figure22(fig_dir)
    generate_figure23(fig_dir)
