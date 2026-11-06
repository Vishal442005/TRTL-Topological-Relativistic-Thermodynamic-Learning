import os
import shutil

fig_mapping = [
    ("figures/phase1/fig1_classical_boundary_pathologies.png", "fig01_classical_boundary_pathologies.png"),
    ("figures/phase1/fig2_trtl_tripartite_fields.png", "fig02_trtl_tripartite_fields.png"),
    ("figures/phase4/fig9_anisotropic_metric_learning_1000D_300dpi.png", "fig03_anisotropic_metric_learning_1000D.png"),
    ("figures/phase3/fig5_radial_chattering_dynamics_300dpi.png", "fig04_radial_chattering_dynamics.png"),
    ("figures/phase2/fig3_geodesic_deflection_and_nodal_horizon.png", "fig05_geodesic_deflection_nodal_horizon.png"),
    ("figures/phase2/fig4_lyapunov_free_energy_and_invariance.png", "fig06_lyapunov_free_energy_invariance.png"),
    ("figures/phase3/fig6_hwtao_phase_space_trajectory.png", "fig07_phase_space_lyapunov_relaxation.png"),
    ("figures/phase4/fig8_measure_concentration_and_relative_contrast.png", "fig08_measure_concentration_relative_contrast.png"),
    ("figures/phase6/fig15_noise_stress_degradation_curves.png", "fig09_label_noise_stress_curves.png"),
    ("figures/comparative/fig28_calibration_and_reliability_diagram.png", "fig10_calibration_reliability_diagram.png"),
    ("figures/comparative/fig27_ood_energy_vs_dnn_confidence.png", "fig11_ood_energy_vs_dnn_confidence.png"),
    ("figures/comparative/fig24_worth_radar_multi_dimension.png", "fig12_multi_dimension_radar_profile.png"),
    ("figures/comparative/fig29_near_ood_spectrum_and_recourse_plausibility.png", "fig13_near_ood_roc_and_recourse_plausibility.png"),
    ("figures/phase7/fig20_ep_map_force_field_and_streamlines.png", "fig14_ep_map_force_field_streamlines.png"),
    ("figures/phase7/fig18_counterfactual_recourse_trajectories.png", "fig15_counterfactual_recourse_curvature.png"),
    ("figures/comparative/fig25_noise_and_adversarial_head_to_head.png", "fig16_pgd20_adversarial_robustness.png"),
    ("figures/phase8/fig17_operational_envelope_phase_diagram.png", "fig17_operational_envelope_phase_diagram.png"),
    ("figures/phase8/fig18_multi_condition_stress_profiles.png", "fig18_multi_condition_stress_profiles.png")
]

dest_fig_dir = "Updated_significant/figures"
os.makedirs(dest_fig_dir, exist_ok=True)

for src, dst_name in fig_mapping:
    if os.path.exists(src):
        dst = os.path.join(dest_fig_dir, dst_name)
        shutil.copy2(src, dst)
        print(f"[OK] Copied {src} -> {dst}")
        # also copy PDF if available
        src_pdf = os.path.splitext(src)[0] + ".pdf"
        if os.path.exists(src_pdf):
            dst_pdf = os.path.join(dest_fig_dir, os.path.splitext(dst_name)[0] + ".pdf")
            shutil.copy2(src_pdf, dst_pdf)
            print(f"  [PDF] Copied {src_pdf} -> {dst_pdf}")
    else:
        print(f"[WARNING] Missing source figure: {src}")

# Copy data and results
dest_data_dir = "Updated_significant/data_and_results"
os.makedirs(dest_data_dir, exist_ok=True)

src_data_files = [
    "data_and_results/extended_multi_condition_benchmark_results.json",
    "docs/comparative_study_against_recent_works.md",
    "docs/enhanced_sota_comparative_additions.md"
]

for src in src_data_files:
    if os.path.exists(src):
        dst = os.path.join(dest_data_dir, os.path.basename(src))
        shutil.copy2(src, dst)
        print(f"[OK] Copied data file {src} -> {dst}")
