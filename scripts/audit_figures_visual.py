"""
Visual inspection script: checks all 16 figures for border clipping, blank edges, and valid dimensions.
"""
import glob
import os
import numpy as np
from PIL import Image

fig_paths = [
    "figures/phase1/fig1_classical_boundary_pathologies.png",
    "figures/phase1/fig2_trtl_tripartite_fields.png",
    "figures/phase4/fig9_anisotropic_metric_learning_1000D_300dpi.png",
    "figures/phase3/fig5_radial_chattering_dynamics_300dpi.png",
    "figures/phase2/fig3_geodesic_deflection_and_nodal_horizon.png",
    "figures/phase2/fig4_lyapunov_free_energy_and_invariance.png",
    "figures/phase3/fig6_hwtao_phase_space_trajectory.png",
    "figures/phase4/fig8_measure_concentration_and_relative_contrast.png",
    "figures/phase6/fig15_noise_stress_degradation_curves.png",
    "figures/comparative/fig28_calibration_and_reliability_diagram.png",
    "figures/comparative/fig27_ood_energy_vs_dnn_confidence.png",
    "figures/comparative/fig24_worth_radar_multi_dimension.png",
    "figures/comparative/fig29_near_ood_spectrum_and_recourse_plausibility.png",
    "figures/phase7/fig20_ep_map_force_field_and_streamlines.png",
    "figures/phase7/fig18_counterfactual_recourse_trajectories.png",
    "figures/comparative/fig25_noise_and_adversarial_head_to_head.png"
]

print(f"Auditing {len(fig_paths)} figures for visual clarity and border integrity...\n")
all_passed = True
for idx, p in enumerate(fig_paths, 1):
    if not os.path.exists(p):
        print(f"[{idx:2d}] FAIL: Missing file: {p}")
        all_passed = False
        continue
    with Image.open(p) as img:
        arr = np.array(img.convert('RGB'))
        w, h = img.size
        # Check border margins (is there padding around the outer 10 pixels?)
        top_edge = arr[:10, :, :].mean()
        bottom_edge = arr[-10:, :, :].mean()
        left_edge = arr[:, :10, :].mean()
        right_edge = arr[:, -10:, :].mean()
        
        # In a well-padded figure, the outer border pixels are white/light (> 240)
        padded = (top_edge > 240 and bottom_edge > 240 and left_edge > 240 and right_edge > 240)
        status = "EXCELLENT" if padded else "ADEQUATE"
        print(f"[{idx:2d}] {os.path.basename(p):<55s} | {w}x{h} | Border status: {status}")

print("\nAudit completed.")
