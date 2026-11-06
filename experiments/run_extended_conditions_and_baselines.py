import os
import json
import numpy as np
from sklearn.datasets import load_breast_cancer, load_digits
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# Ensure output directory
out_dir = "data_and_results"
os.makedirs(out_dir, exist_ok=True)

class TRTLExtendedClassifier:
    """Python implementation of TRTL for multi-condition benchmarking."""
    def __init__(self, beta=0.92, k=2.5, mu=0.8, kappa=1.5, T0=0.85, Tc=1.042, b=1.0, xi=0.5):
        self.beta = beta
        self.k = k
        self.mu = mu
        self.kappa = kappa
        self.T0 = T0
        self.Tc = Tc
        self.b = b
        self.xi = xi

    def fit(self, X, y):
        self.X_ = np.asarray(X, dtype=np.float64)
        self.y_ = np.asarray(y, dtype=np.int64)
        self.classes_ = np.unique(self.y_)
        self.n_classes_ = len(self.classes_)
        self.n_samples_, self.n_features_ = self.X_.shape

        # Compute Shannon entropy per sample over 5-NN
        from sklearn.neighbors import NearestNeighbors
        nn = NearestNeighbors(n_neighbors=min(6, self.n_samples_)).fit(self.X_)
        _, indices = nn.kneighbors(self.X_)

        self.H_ = np.zeros(self.n_samples_)
        H_max = np.log(self.n_classes_) if self.n_classes_ > 1 else 1.0

        for i, nbrs in enumerate(indices):
            nbr_labels = self.y_[nbrs[1:]]
            counts = np.bincount(nbr_labels, minlength=self.n_classes_)
            probs = counts / np.sum(counts)
            p_pos = probs[probs > 0]
            self.H_[i] = -np.sum(p_pos * np.log(p_pos))

        # Lorentz dilatation factor
        ratio = np.clip(self.H_ / (H_max + 1e-12), 0.0, 0.999)
        self.gamma_ = 1.0 / np.sqrt(np.maximum(1e-6, 1.0 - self.beta * (ratio ** 2)))

        # Learn diagonal feature metric tensor w_j based on variance / Fisher criterion
        var_between = np.zeros(self.n_features_)
        var_within = np.zeros(self.n_features_) + 1e-8
        overall_mean = np.mean(self.X_, axis=0)

        for c in self.classes_:
            Xc = self.X_[self.y_ == c]
            if len(Xc) > 0:
                var_between += len(Xc) * (np.mean(Xc, axis=0) - overall_mean)**2
                var_within += np.sum((Xc - np.mean(Xc, axis=0))**2, axis=0)

        fisher = var_between / var_within
        w = fisher / (np.sum(fisher) + 1e-12) * self.n_features_
        self.w_ = np.clip(w, 0.1, 5.0)

        return self

    def predict_proba(self, X):
        X = np.asarray(X, dtype=np.float64)
        N_test = len(X)
        probs = np.zeros((N_test, self.n_classes_))

        for idx, x in enumerate(X):
            # RAMD dilated distances
            diff = self.X_ - x
            d_W = np.sqrt(np.sum(self.w_ * (diff ** 2), axis=1))
            d_rel = self.gamma_ * d_W

            # TWIL coherent wavefields
            wave_real = np.zeros(self.n_classes_)
            wave_imag = np.zeros(self.n_classes_)

            for i in range(self.n_samples_):
                c = self.y_[i]
                d = d_rel[i]
                # Gaussian envelope with spatial cutoff
                if d <= 3.5:
                    env = np.exp(-0.5 * self.mu * (d ** 2))
                    wave_real[c] += env * np.cos(self.k * d)
                    wave_imag[c] += env * np.sin(self.k * d)

            # Class wave energies
            psi_sq = wave_real**2 + wave_imag**2
            energies = np.zeros(self.n_classes_)
            for c in range(self.n_classes_):
                cross = np.sum([psi_sq[c_p] for c_p in range(self.n_classes_) if c_p != c])
                cross_term = (self.kappa / max(1, self.n_classes_ - 1)) * cross
                energies[c] = max(0.0, psi_sq[c] - cross_term)

            E_tot = np.sum(energies)
            # TPTC Ginzburg-Landau relaxation
            T = self.T0 + 0.5 / (1.0 + E_tot / 0.5)

            if T >= self.Tc or E_tot < 1e-12:
                # Disordered symmetric state / metric void
                probs[idx] = np.ones(self.n_classes_) / self.n_classes_
            else:
                # Symmetry breaking: relaxation to order parameter
                S = np.zeros(self.n_classes_)
                dt = 0.05
                for _ in range(15):
                    for c in range(self.n_classes_):
                        cross_S = np.sum([S[cp]**2 for cp in range(self.n_classes_) if cp != c])
                        dS = -(T - self.Tc)*S[c] - self.b*(S[c]**3) + energies[c] - self.xi*S[c]*cross_S
                        S[c] += dt * dS
                        S[c] = max(0.0, S[c])

                if np.sum(S) > 1e-12:
                    # Softmax with temperature
                    exp_S = np.exp(np.clip(S / 0.2, -20, 20))
                    probs[idx] = exp_S / np.sum(exp_S)
                else:
                    probs[idx] = np.ones(self.n_classes_) / self.n_classes_

        return probs

    def predict(self, X):
        proba = self.predict_proba(X)
        return self.classes_[np.argmax(proba, axis=1)]


def evaluate_benchmarks():
    print("[1/4] Running Asymmetric Label Noise Stress Benchmarks...")
    data = load_breast_cancer()
    X, y = data.data, data.target
    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)

    asym_levels = [0.0, 0.10, 0.20, 0.30, 0.40]
    results_asym = {
        "TRTL": [],
        "Deep_MLP": [],
        "RBF_SVM": [],
        "Random_Forest": [],
        "Complex_Wave": [],
        "Energy_GL": []
    }

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for asym in asym_levels:
        fold_accs = {k: [] for k in results_asym}
        for tr, te in skf.split(X, y):
            X_tr, X_te = X[tr], X[te]
            y_tr, y_te = y[tr].copy(), y[te]

            # Asymmetric class-conditional noise: Class 0 -> 1 with p=asym, Class 1 -> 0 with p=asym/2
            if asym > 0:
                mask0 = (y_tr == 0)
                mask1 = (y_tr == 1)
                flip0 = np.random.rand(np.sum(mask0)) < asym
                flip1 = np.random.rand(np.sum(mask1)) < (asym / 2.0)
                idx0 = np.where(mask0)[0][flip0]
                idx1 = np.where(mask1)[0][flip1]
                y_tr[idx0] = 1
                y_tr[idx1] = 0

            # 1. TRTL
            m_trtl = TRTLExtendedClassifier().fit(X_tr, y_tr)
            fold_accs["TRTL"].append(accuracy_score(y_te, m_trtl.predict(X_te)))

            # 2. Deep MLP
            m_mlp = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=300, random_state=42).fit(X_tr, y_tr)
            fold_accs["Deep_MLP"].append(accuracy_score(y_te, m_mlp.predict(X_te)))

            # 3. RBF SVM
            m_svm = SVC(kernel='rbf', probability=True, random_state=42).fit(X_tr, y_tr)
            fold_accs["RBF_SVM"].append(accuracy_score(y_te, m_svm.predict(X_te)))

            # 4. Random Forest
            m_rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_tr, y_tr)
            fold_accs["Random_Forest"].append(accuracy_score(y_te, m_rf.predict(X_te)))

            # 5. Complex Wave (simplified)
            m_cw = TRTLExtendedClassifier(beta=0.0, T0=1.2).fit(X_tr, y_tr) # no dilatation, no symmetry breaking
            fold_accs["Complex_Wave"].append(accuracy_score(y_te, m_cw.predict(X_te)))

            # 6. Energy G-L (no waves, Euclidean metric)
            m_egl = TRTLExtendedClassifier(beta=0.0, k=0.0).fit(X_tr, y_tr)
            fold_accs["Energy_GL"].append(accuracy_score(y_te, m_egl.predict(X_te)))

        for k in results_asym:
            mean_acc = float(np.mean(fold_accs[k]))
            results_asym[k].append(round(mean_acc * 100, 2))
            print(f"  Asym {asym*100:2.0f}% | {k:15s}: {mean_acc*100:.2f}%")

    # ---------------------------------------------------------
    # 2. Covariate Jitter Noise (Manifold Distortion)
    # ---------------------------------------------------------
    print("\n[2/4] Running Covariate Jitter Noise Benchmarks...")
    jitter_levels = [0.0, 0.1, 0.2, 0.3, 0.5]
    results_jitter = {
        "TRTL": [],
        "Deep_MLP": [],
        "RBF_SVM": [],
        "Random_Forest": []
    }

    for jit in jitter_levels:
        fold_accs = {k: [] for k in results_jitter}
        for tr, te in skf.split(X, y):
            X_tr, X_te = X[tr].copy(), X[te].copy()
            y_tr, y_te = y[tr], y[te]

            if jit > 0:
                X_te += np.random.normal(0, jit, X_te.shape)

            m_trtl = TRTLExtendedClassifier().fit(X_tr, y_tr)
            fold_accs["TRTL"].append(accuracy_score(y_te, m_trtl.predict(X_te)))

            m_mlp = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=300, random_state=42).fit(X_tr, y_tr)
            fold_accs["Deep_MLP"].append(accuracy_score(y_te, m_mlp.predict(X_te)))

            m_svm = SVC(kernel='rbf', random_state=42).fit(X_tr, y_tr)
            fold_accs["RBF_SVM"].append(accuracy_score(y_te, m_svm.predict(X_te)))

            m_rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_tr, y_tr)
            fold_accs["Random_Forest"].append(accuracy_score(y_te, m_rf.predict(X_te)))

        for k in results_jitter:
            mean_acc = float(np.mean(fold_accs[k]))
            results_jitter[k].append(round(mean_acc * 100, 2))
            print(f"  Jitter {jit:.1f} | {k:15s}: {mean_acc*100:.2f}%")

    # ---------------------------------------------------------
    # 3. Sample Starvation / Low-Data Regime
    # ---------------------------------------------------------
    print("\n[3/4] Running Low-Data Starvation Benchmarks...")
    fractions = [0.10, 0.25, 0.50, 0.75, 1.00]
    results_starvation = {
        "TRTL": [],
        "Deep_MLP": [],
        "RBF_SVM": [],
        "Random_Forest": []
    }

    for frac in fractions:
        fold_accs = {k: [] for k in results_starvation}
        for tr, te in skf.split(X, y):
            n_sub = max(10, int(len(tr) * frac))
            sub_tr = np.random.choice(tr, size=n_sub, replace=False)

            X_tr, y_tr = X[sub_tr], y[sub_tr]
            X_te, y_te = X[te], y[te]

            m_trtl = TRTLExtendedClassifier().fit(X_tr, y_tr)
            fold_accs["TRTL"].append(accuracy_score(y_te, m_trtl.predict(X_te)))

            m_mlp = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=300, random_state=42).fit(X_tr, y_tr)
            fold_accs["Deep_MLP"].append(accuracy_score(y_te, m_mlp.predict(X_te)))

            m_svm = SVC(kernel='rbf', random_state=42).fit(X_tr, y_tr)
            fold_accs["RBF_SVM"].append(accuracy_score(y_te, m_svm.predict(X_te)))

            m_rf = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_tr, y_tr)
            fold_accs["Random_Forest"].append(accuracy_score(y_te, m_rf.predict(X_te)))

        for k in results_starvation:
            mean_acc = float(np.mean(fold_accs[k]))
            results_starvation[k].append(round(mean_acc * 100, 2))
            print(f"  Fraction {frac*100:3.0f}% | {k:15s}: {mean_acc*100:.2f}%")

    # Save all results to data_and_results/
    out_payload = {
        "asymmetric_noise": {
            "levels": asym_levels,
            "results": results_asym
        },
        "covariate_jitter": {
            "levels": jitter_levels,
            "results": results_jitter
        },
        "sample_starvation": {
            "fractions": fractions,
            "results": results_starvation
        }
    }

    out_file = os.path.join(out_dir, "extended_multi_condition_benchmark_results.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(out_payload, f, indent=2)
    print(f"\n[SUCCESS] Saved benchmark results to {out_file}")

if __name__ == "__main__":
    np.random.seed(42)
    evaluate_benchmarks()
