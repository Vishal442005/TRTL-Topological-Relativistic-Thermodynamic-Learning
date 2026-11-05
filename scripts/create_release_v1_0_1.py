"""
Create GitHub Release v1.0.1 and publish Zenodo deposition with Vishal Chandel & ORCID.
"""
import json
import os
import subprocess
import urllib.request
import urllib.error

# 1. Retrieve GitHub Token
print("[1/5] Retrieving GitHub token...")
res = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n', text=True, capture_output=True)
token_dict = dict(line.split('=', 1) for line in res.stdout.strip().splitlines() if '=' in line)
gh_token = token_dict.get('password')
if not gh_token:
    raise RuntimeError("Could not retrieve GitHub token.")

owner = "Vishal442005"
repo = "TRTL-Topological-Relativistic-Thermodynamic-Learning"
zenodo_token = "ySaTTqO9pUBgdFbnv6b1dUPCVRIM7yQdKkSQYNKBanDF8yUaHswVRB2GKSem"

gh_headers = {
    'Authorization': f'token {gh_token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'TRTL-Publisher'
}

# 2. Release Body
release_body = """# Topological-Relativistic-Thermodynamic Learning (TRTL) — Release v1.0.1

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23951913.svg)](https://doi.org/10.5281/zenodo.23951913)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0006--0552--8551-green.svg)](https://orcid.org/0009-0006-0552-8551)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Official Open-Science Implementation & Reproducibility Suite**  
- **Lead Author:** Vishal Chandel ([ORCID: 0009-0006-0552-8551](https://orcid.org/0009-0006-0552-8551))
- **Consortium:** TRTL Research Consortium
- **Master Concept DOI:** [https://doi.org/10.5281/zenodo.23951912](https://doi.org/10.5281/zenodo.23951912)
- **Release Version DOI:** [https://doi.org/10.5281/zenodo.23968898](https://doi.org/10.5281/zenodo.23968898)
- **Target Venue:** Elsevier *Pattern Recognition* / IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)

---

### Highlights of Release v1.0.1:
1. **Author Identification & ORCID Registry:** Formally binds authorship to **Vishal Chandel** (ORCID: `0009-0006-0552-8551`) across Zenodo deposition metadata, `CITATION.cff`, and `pyproject.toml`.
2. **Three-Stage Physics Pipeline:**
   - **Stage I (RAMD):** Relativistic Anisotropic Metric Dilatation with Lorentz gamma factors and adaptive metric tensors.
   - **Stage II (TWIL):** Multi-class wavepacket interference layer enforcing coherent manifold boundaries.
   - **Stage III (TPTC):** Ginzburg-Landau non-equilibrium thermodynamic crystallization for certified robustness.
3. **Rigorous Empirical Verification:** Fully reproducible benchmarks comparing TRTL against 10 SOTA architectures across synthetic manifolds, noise stress tests, and high-dimensional regimes ($D=1,000$).
4. **Open-Science Codebase:** Pure source code, unit tests, and empirical verification scripts (manuscripts excluded per pre-review privacy standards).

---

### Citation:
```bibtex
@software{chandel2026trtl_v101,
  author       = {Chandel, Vishal and TRTL Research Consortium},
  title        = {{Topological-Relativistic-Thermodynamic Learning (TRTL): A Unified Physics-Grounded Machine Learning Framework}},
  version      = {v1.0.1},
  year         = 2026,
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.23968898},
  url          = {https://doi.org/10.5281/zenodo.23968898}
}
```
"""

# 3. Create GitHub Release
print("[2/5] Creating GitHub Release v1.0.1 on GitHub...")
payload = {
    "tag_name": "v1.0.1",
    "target_commitish": "main",
    "name": "v1.0.1: Official TRTL Research Artifact & Benchmark Suite",
    "body": release_body,
    "draft": False,
    "prerelease": False
}

req = urllib.request.Request(
    f"https://api.github.com/repos/{owner}/{repo}/releases",
    data=json.dumps(payload).encode('utf-8'),
    headers=gh_headers,
    method='POST'
)

try:
    with urllib.request.urlopen(req) as resp:
        gh_rel = json.loads(resp.read().decode())
        print(f" -> GitHub Release created! ID: {gh_rel['id']}, URL: {gh_rel['html_url']}")
except urllib.error.HTTPError as e:
    err_body = e.read().decode()
    print(f"Notice on GitHub release creation: {e.code} - {err_body}")
    # Fetch existing
    req_ex = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}/releases/tags/v1.0.1", headers=gh_headers)
    with urllib.request.urlopen(req_ex) as resp:
        gh_rel = json.loads(resp.read().decode())
        print(f" -> Found existing GitHub Release! ID: {gh_rel['id']}, URL: {gh_rel['html_url']}")

# 4. Update and Publish Zenodo Draft 23968898
print("[3/5] Updating Zenodo deposition 23968898...")
zenodo_headers = {
    'Authorization': f'Bearer {zenodo_token}',
    'Content-Type': 'application/json'
}

dep_id = 23968898
zenodo_meta = {
    "metadata": {
        "title": "Topological-Relativistic-Thermodynamic Learning (TRTL): A Unified Physics-Grounded Machine Learning Framework",
        "upload_type": "software",
        "publication_date": "2026-11-05",
        "version": "1.0.1",
        "description": "Official reproduction suite and research artifact for Topological-Relativistic-Thermodynamic Learning (TRTL). Includes full mathematical proofs, non-Euclidean manifold embeddings, relativistic phase propagation engines, non-equilibrium thermodynamic phase transition monitors, 16 publication figures, 10 comparative benchmark tables, and verified empirical benchmarks.",
        "access_right": "open",
        "creators": [
            {
                "name": "Chandel, Vishal",
                "affiliation": "Department of Advanced Agentic AI and Computational Physics",
                "orcid": "0009-0006-0552-8551"
            },
            {
                "name": "TRTL Research Consortium",
                "affiliation": "Department of Advanced Agentic AI and Computational Physics"
            }
        ],
        "keywords": [
            "Machine Learning",
            "Pattern Recognition",
            "Topological Data Analysis",
            "Relativistic Metric Dilatation",
            "Lorentzian Manifolds",
            "Non-Equilibrium Thermodynamics",
            "Ginzburg-Landau Theory",
            "Adversarial Robustness",
            "Counterfactual Recourse"
        ],
        "related_identifiers": [
            {
                "identifier": f"https://github.com/{owner}/{repo}/tree/v1.0.1",
                "relation": "isSupplementTo",
                "resource_type": "software",
                "scheme": "url"
            }
        ],
        "custom": {
            "code:codeRepository": f"https://github.com/{owner}/{repo}"
        },
        "license": "mit-license",
        "imprint_publisher": "Zenodo"
    }
}

zen_put = urllib.request.Request(
    f"https://zenodo.org/api/deposit/depositions/{dep_id}",
    data=json.dumps(zenodo_meta).encode('utf-8'),
    headers=zenodo_headers,
    method='PUT'
)

with urllib.request.urlopen(zen_put) as zresp:
    zdata = json.loads(zresp.read().decode())
    print(" -> Zenodo metadata updated successfully!")
    print(f" -> Creators: {json.dumps(zdata['metadata']['creators'], indent=2)}")

# 5. Publish Zenodo Deposition to finalize the DOI
print("[4/5] Publishing Zenodo deposition 23968898...")
pub_req = urllib.request.Request(
    f"https://zenodo.org/api/deposit/depositions/{dep_id}/actions/publish",
    headers={'Authorization': f'Bearer {zenodo_token}', 'Accept': 'application/json'},
    method='POST'
)

with urllib.request.urlopen(pub_req) as pub_resp:
    published_data = json.loads(pub_resp.read().decode())
    minted_doi = published_data.get('doi')
    print(f" -> Deposition published! Minted DOI: {minted_doi}")
    print(f" -> Record URL: https://zenodo.org/records/{dep_id}")
    print(f" -> DOI URL: https://doi.org/{minted_doi}")

print("[5/5] All operations completed successfully!")
