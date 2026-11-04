import json
import subprocess
import urllib.request

res = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n', text=True, capture_output=True)
token = dict(line.split('=', 1) for line in res.stdout.strip().splitlines() if '=' in line).get('password')

headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'TRTL-Publisher'}
owner = 'Vishal442005'
repo = 'TRTL-Topological-Relativistic-Thermodynamic-Learning'

req = urllib.request.Request(f'https://api.github.com/repos/{owner}/{repo}/releases/tags/v1.0.0', headers=headers)
with urllib.request.urlopen(req) as resp:
    rel = json.loads(resp.read().decode())
    rel_id = rel['id']

body = """# Topological-Relativistic-Thermodynamic Learning (TRTL) — v1.0.0 Official Research Artifact

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23951913.svg)](https://doi.org/10.5281/zenodo.23951913)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Permanent Open-Science DOI:** [https://doi.org/10.5281/zenodo.23951913](https://doi.org/10.5281/zenodo.23951913)
**Zenodo Record:** [https://zenodo.org/records/23951913](https://zenodo.org/records/23951913)

This release accompanies the peer-reviewed submission to **Elsevier *Pattern Recognition***:
**"Topological-Relativistic-Thermodynamic Learning: A Unified Physics-Grounded Manifold Learning Framework for Certified Robustness, Dynamic Geodesic Propagation, and Exact Recourse"**

## Research Highlights & Artifact Contents:
- **Core Package (`trtl/`):** Full PyTorch implementation of Relativistic Anisotropic Metric Dilatation (RAMD), Thermodynamic Wave Interference Layers (TWIL), and Ginzburg-Landau Thermodynamic Phase-Transition Crystallization (TPTC).
- **Formal Theoretical Guarantees:** Mathematical proofs for Curvature-Invariant Geodesic Boundedness (Lemma 3.1), Global Non-Equilibrium Convergence (Theorem 3.2), Relativistic Speed of Information (Theorem 3.3), and Closed-Form Recourse Plausibility (Theorem 3.4).
- **Comprehensive Benchmark Suite:** Full evaluation suite benchmarking TRTL against 10 baselines (Euclidean MLP, Poincaré, Hyperbolic GCN, Energy-Based Models, PINNs, Riemannian Flow) across multi-scale manifolds, noise levels (up to 40%), and high dimensions ($D=2$ to $D=1,000$).
- **Submission Manuscripts:** Publication-ready `.docx` manuscript with 16 embedded high-resolution figures, 10 Elsevier 3-line tables, and native Word OMML display equations.

## How to Cite:
```bibtex
@software{trtl2026,
  author       = {Vishal and TRTL Research Consortium},
  title        = {{Topological-Relativistic-Thermodynamic Learning (TRTL): A Unified Physics-Grounded Machine Learning Framework}},
  month        = nov,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.23951913},
  url          = {https://doi.org/10.5281/zenodo.23951913}
}
```
"""

patch_payload = {
    'name': 'v1.0.0: Official TRTL Research Artifact & Benchmark Suite (DOI: 10.5281/zenodo.23951913)',
    'body': body
}
req_patch = urllib.request.Request(f'https://api.github.com/repos/{owner}/{repo}/releases/{rel_id}', data=json.dumps(patch_payload).encode('utf-8'), headers=headers, method='PATCH')
with urllib.request.urlopen(req_patch) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print("Successfully updated release on GitHub!")
    print("Release URL:", data.get('html_url'))
