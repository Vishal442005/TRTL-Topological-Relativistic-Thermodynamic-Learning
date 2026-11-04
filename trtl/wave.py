"""
TRTL Wave Engine: Thermodynamic Wave Interference Layer (TWIL)
Implements complex wave packet superposition, phase rotation, and cross-class inhibition.
"""

import numpy as np


class WaveInterferenceLayer:
    """
    Computes coherent wavefield amplitudes per class channel:
        psi_c(x) = sum_{i: y_i=c} A_i * exp(-mu * u_d^2) * exp(i * k * u_d)
    and cross-class competitive wave inhibition:
        E_c = |psi_c|^2 - (kappa / (C-1)) * sum_{c' != c} |psi_{c'}|^2.
    """
    def __init__(self, k_wave=0.15, mu=1.5, cross_inhibition_kappa=0.20):
        self.k_wave = k_wave
        self.mu = mu
        self.cross_inhibition_kappa = cross_inhibition_kappa

    def compute_energies(self, u_d, y_train_idx, n_classes, class_weights):
        """
        Args:
            u_d: (M, N) normalized dilated distances.
            y_train_idx: (N,) integer class indices of anchors.
            n_classes: int, total number of unique classes.
            class_weights: (n_classes,) asymptotic balance weights (1 / N_c).
        Returns:
            energies: (M, n_classes) rectified coherent energies.
        """
        M, N = u_d.shape
        w_emit = class_weights[y_train_idx]
        envelope = np.exp(-self.mu * (u_d ** 2)) * w_emit[np.newaxis, :]

        energies = np.zeros((M, n_classes))
        for c in range(n_classes):
            mask_c = (y_train_idx == c)
            if not np.any(mask_c):
                continue
            u_c = u_d[:, mask_c]
            env_c = envelope[:, mask_c]

            re_psi = np.sum(env_c * np.cos(self.k_wave * u_c), axis=1)
            im_psi = np.sum(env_c * np.sin(self.k_wave * u_c), axis=1)
            energies[:, c] = (re_psi ** 2) + (im_psi ** 2)

        # Cross-class competitive wave inhibition
        if n_classes > 1 and self.cross_inhibition_kappa > 0.0:
            E_total = np.sum(energies, axis=1, keepdims=True)
            cross_inh = (E_total - energies) / (n_classes - 1)
            energies = np.maximum(0.0, energies - self.cross_inhibition_kappa * cross_inh)

        return energies
