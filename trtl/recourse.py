"""
TRTL Recourse Engine: Continuous Thermodynamic Counterfactual Recourse (TCR)
Transports query points along conservative potential gradient flows to target class cores.
"""

import numpy as np


class ThermodynamicRecourse:
    """
    Computes smooth, manifold-adherent counterfactual recourse paths:
        dot{x}(t) = nabla_x S_{c*}(x(t)) - lambda_reg * (x(t) - x_0)
    """
    def __init__(self, trtl_model, max_steps=100, eta=0.08, lambda_reg=0.01):
        self.model = trtl_model
        self.max_steps = max_steps
        self.eta = eta
        self.lambda_reg = lambda_reg

    def generate_recourse(self, x_0, target_class):
        """
        Generates recourse trajectory from x_0 to target_class.
        Returns:
            trajectory: (K, D) array of consecutive coordinates along the path.
            success: bool, whether target probability >= 0.50 was reached.
        """
        x = np.array(x_0, dtype=np.float64).copy()
        trajectory = [x.copy()]
        dim = len(x)
        h = 1e-4

        for _ in range(self.max_steps):
            probs = self.model.predict_proba([x])[0]
            if probs[target_class] >= 0.50:
                return np.array(trajectory), True

            # Finite-difference gradient of order parameter
            grad = np.zeros(dim)
            for j in range(dim):
                x_plus = x.copy()
                x_minus = x.copy()
                x_plus[j] += h
                x_minus[j] -= h
                p_plus = self.model.predict_proba([x_plus])[0, target_class]
                p_minus = self.model.predict_proba([x_minus])[0, target_class]
                grad[j] = (p_plus - p_minus) / (2.0 * h)

            # Regularized gradient step
            grad_norm = np.linalg.norm(grad)
            if grad_norm > 1e-6:
                step_dir = grad / grad_norm
            else:
                step_dir = np.zeros(dim)

            x += self.eta * step_dir - self.eta * self.lambda_reg * (x - x_0)
            trajectory.append(x.copy())

        final_probs = self.model.predict_proba([x])[0]
        return np.array(trajectory), (final_probs[target_class] >= 0.50)
