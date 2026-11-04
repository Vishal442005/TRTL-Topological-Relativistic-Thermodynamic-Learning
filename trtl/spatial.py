"""
TRTL Spatial Engine: Metric Ball-Tree Indexing & Truncation Horizon Pruning
Enforces exact zero-support vacuum horizon R_cut to achieve O(D log N) query scaling.
"""

import numpy as np
from sklearn.neighbors import BallTree


class SpatialBallTreeIndexer:
    """
    Hierarchical metric Ball-Tree spatial acceleration index.
    Prunes distant training clusters in O(1) time when dist > R_cut.
    """
    def __init__(self, mu=1.5, eps_tol=1e-12, leaf_size=40):
        self.mu = mu
        self.eps_tol = eps_tol
        self.leaf_size = leaf_size
        self.ball_tree_ = None
        self.R_cut_ = None

    def fit(self, X_train_w, d_scale):
        """
        Builds the metric Ball-Tree on anisotropic features and computes R_cut.
        """
        # Analytical truncation horizon: exp(-mu * (R_cut / d_scale)^2) = eps_tol
        # => (R_cut / d_scale)^2 = ln(1 / eps_tol) / mu
        u_cut = np.sqrt(np.log(1.0 / self.eps_tol) / self.mu)
        self.R_cut_ = u_cut * d_scale
        self.ball_tree_ = BallTree(X_train_w, leaf_size=self.leaf_size, metric='euclidean')
        return self

    def query_radius(self, X_query_w):
        """
        Returns list of active anchor indices for each query sample within R_cut.
        """
        return self.ball_tree_.query_radius(X_query_w, r=self.R_cut_)
