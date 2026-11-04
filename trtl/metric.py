"""
TRTL Metric Engine: Relativistic Anisotropic Metric Dilatation (RAMD)
Computes local Shannon conflict entropy and Lorentz dilatation factors.
"""

import numpy as np
from scipy.spatial.distance import cdist


class RelativisticMetric:
    """
    Computes local Shannon conflict entropy and Lorentz dilatation factor gamma_i.
    Expands metric distance around high-entropy boundary anchors:
        d_rel(x, x_i) = ||x - x_i||_W * gamma_i
    where gamma_i = 1 / sqrt(1 - beta * (H_i / H_max)^2).
    """
    def __init__(self, beta=0.75, k_neighbors=7, use_anisotropic=True):
        self.beta = beta
        self.k_neighbors = k_neighbors
        self.use_anisotropic = use_anisotropic
        self.gamma_ = None
        self.feat_weights_ = None
        self.d_scale_ = 1.0

    def fit(self, X, y):
        X = np.asarray(X, dtype=np.float64)
        N, D = X.shape
        classes = np.unique(y)
        n_classes = len(classes)
        y_idx = np.searchsorted(classes, y)

        # 1. Feature anisotropy weighting
        if self.use_anisotropic and n_classes > 1:
            mean_total = np.mean(X, axis=0)
            ss_between = np.zeros(D)
            ss_within = np.zeros(D)
            for c in range(n_classes):
                X_c = X[y_idx == c]
                n_c = len(X_c)
                if n_c > 1:
                    mean_c = np.mean(X_c, axis=0)
                    ss_between += n_c * (mean_c - mean_total) ** 2
                    ss_within += np.sum((X_c - mean_c) ** 2, axis=0)
            f_ratio = ss_between / (ss_within + 1e-6)
            f_mean = np.mean(f_ratio) + 1e-6
            self.feat_weights_ = np.sqrt(np.clip(f_ratio / f_mean, 0.25, 4.0))
        else:
            self.feat_weights_ = np.ones(D)

        X_w = X * self.feat_weights_

        # 2. Characteristic distance scale
        sub = X_w[:min(N, 200)]
        d_sub = cdist(sub, sub)
        pos = d_sub[d_sub > 0]
        self.d_scale_ = float(np.median(pos)) if len(pos) > 0 else 1.0

        # 3. Shannon Conflict Entropy
        d_tr = cdist(X_w, X_w)
        np.fill_diagonal(d_tr, np.inf)
        k_eff = min(self.k_neighbors, N - 1)
        nn_idx = np.argsort(d_tr, axis=1)[:, :k_eff]

        entropies = np.zeros(N)
        for i in range(N):
            c_counts = np.bincount(y_idx[nn_idx[i]], minlength=n_classes)
            probs = np.clip(c_counts / np.sum(c_counts), 1e-12, 1.0)
            entropies[i] = -np.sum(probs * np.log(probs))

        H_max = np.log(n_classes) if n_classes > 1 else 1.0
        ratio_sq = np.clip((entropies / (H_max + 1e-5)) ** 2, 0.0, 0.99)
        self.gamma_ = 1.0 / np.sqrt(1.0 - self.beta * ratio_sq)

        return self

    def transform_distance(self, X_query, X_train):
        """Calculates dilated distances u_d = (||X_query - X_train||_W * gamma) / d_scale."""
        X_q_w = np.asarray(X_query, dtype=np.float64) * self.feat_weights_
        X_tr_w = np.asarray(X_train, dtype=np.float64) * self.feat_weights_
        raw_dists = cdist(X_q_w, X_tr_w)
        d_rel = raw_dists * self.gamma_[np.newaxis, :]
        return d_rel / self.d_scale_
