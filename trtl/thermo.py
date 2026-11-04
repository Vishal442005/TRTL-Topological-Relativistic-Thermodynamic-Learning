"""
TRTL Thermodynamic Engine: Thermodynamic Phase-Transition Crystallization (TPTC)
Implements Ginzburg-Landau symmetry breaking, order-parameter relaxation, and HWTAO optimizer.
"""

import numpy as np


class ThermodynamicCrystallizer:
    """
    Relaxes initial order parameter S^{(0)} along Ginzburg-Landau potential:
        dF/dS_c = (T - T_c) * S_c + b * S_c^3 - h_c + xi * S_c * sum_{c' != c} S_{c'}^2
    projecting onto the probability simplex Pi_Delta.
    """
    def __init__(self, cooling_steps=12, dt=0.04, temp_diff=-1.5, repulsion_xi=2.0):
        self.cooling_steps = cooling_steps
        self.dt = dt
        self.temp_diff = temp_diff
        self.repulsion_xi = repulsion_xi

    def crystallize(self, energies):
        """
        Relaxes energies into crystallized order-parameter probabilities.
        Args:
            energies: (M, C) non-negative wave energy matrix.
        Returns:
            S: (M, C) crystallized probability distributions on simplex.
        """
        row_sums = np.sum(energies, axis=1, keepdims=True) + 1e-12
        S = energies / row_sums
        h_field = S.copy()

        for _ in range(self.cooling_steps):
            S_sq_sum = np.sum(S ** 2, axis=1, keepdims=True)
            repulsion = self.repulsion_xi * S * (S_sq_sum - S ** 2)
            dF = self.temp_diff * S + (S ** 3) - h_field + repulsion
            S = np.clip(S - self.dt * dF, 0.0, 1.0)
            S /= (np.sum(S, axis=1, keepdims=True) + 1e-12)

        return S
