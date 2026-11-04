"""
TRTL Classifier: Scikit-Learn Compatible Classifier API
Integrates RAMD, TWIL, TPTC, and Spatial Ball-Tree Indexing.
"""

import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.preprocessing import StandardScaler

from .metric import RelativisticMetric
from .wave import WaveInterferenceLayer
from .thermo import ThermodynamicCrystallizer
from .spatial import SpatialBallTreeIndexer


class TRTLClassifier(BaseEstimator, ClassifierMixin):
    """
    Topological-Relativistic-Thermodynamic Learning (TRTL) Classifier.
    Fully compatible with scikit-learn cross-validation and pipeline pipelines.
    """
    def __init__(self, beta=0.75, k_wave=0.15, mu=1.5, cooling_steps=12, dt=0.04,
                 cross_inhibition_kappa=0.20, use_spatial_index=False):
        self.beta = beta
        self.k_wave = k_wave
        self.mu = mu
        self.cooling_steps = cooling_steps
        self.dt = dt
        self.cross_inhibition_kappa = cross_inhibition_kappa
        self.use_spatial_index = use_spatial_index

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        self.n_classes_ = len(self.classes_)
        self.y_idx_ = np.searchsorted(self.classes_, y)

        self.scaler_ = StandardScaler()
        self.X_train_ = self.scaler_.fit_transform(np.asarray(X, dtype=np.float64))

        # 1. Metric Stage
        self.metric_ = RelativisticMetric(beta=self.beta)
        self.metric_.fit(self.X_train_, self.y_idx_)

        # 2. Wave Stage
        self.wave_ = WaveInterferenceLayer(
            k_wave=self.k_wave, mu=self.mu, cross_inhibition_kappa=self.cross_inhibition_kappa)

        # 3. Thermodynamic Stage
        self.thermo_ = ThermodynamicCrystallizer(
            cooling_steps=self.cooling_steps, dt=self.dt)

        # Class counts for asymptotic balance
        counts = np.bincount(self.y_idx_, minlength=self.n_classes_)
        self.class_weights_ = 1.0 / np.maximum(counts, 1)

        # 4. Optional Spatial Index
        if self.use_spatial_index:
            self.spatial_ = SpatialBallTreeIndexer(mu=self.mu)
            self.spatial_.fit(self.X_train_ * self.metric_.feat_weights_, self.metric_.d_scale_)
        else:
            self.spatial_ = None

        return self

    def predict_proba(self, X):
        X_scaled = self.scaler_.transform(np.asarray(X, dtype=np.float64))
        u_d = self.metric_.transform_distance(X_scaled, self.X_train_)
        energies = self.wave_.compute_energies(u_d, self.y_idx_, self.n_classes_, self.class_weights_)
        probs = self.thermo_.crystallize(energies)
        return probs

    def predict(self, X):
        probs = self.predict_proba(X)
        return self.classes_[np.argmax(probs, axis=1)]

    def compute_certified_radius(self, x):
        """
        Computes the certified L2 invariance radius r_cert around point x (Theorem 2.6).
        """
        probs = self.predict_proba([x])[0]
        top_idx = np.argsort(-probs)
        margin = probs[top_idx[0]] - probs[top_idx[1]]
        # Global Lipschitz constant estimate
        L_max = 2.0 * self.mu / (self.metric_.d_scale_ + 1e-6)
        r_cert = margin / (2.0 * L_max)
        return float(r_cert)
