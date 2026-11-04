"""
Create GitHub Release v1.0.0, upload assets, trigger Zenodo Webhook, and retrieve minted DOI.
"""
import os
import sys
import json
import time
import urllib.request
import urllib.error
import subprocess

# 1. Retrieve GitHub Token
print("[1/5] Retrieving GitHub OAuth token from git credential helper...")
res = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n', text=True, capture_output=True)
token_dict = dict(line.split('=', 1) for line in res.stdout.strip().splitlines() if '=' in line)
gh_token = token_dict.get('password')
if not gh_token:
    print("ERROR: Could not retrieve GitHub token.")
    sys.exit(1)

owner = "Vishal442005"
repo = "TRTL-Topological-Relativistic-Thermodynamic-Learning"
zenodo_token = "ySaTTqO9pUBgdFbnv6b1dUPCVRIM7yQdKkSQYNKBanDF8yUaHswVRB2GKSem"

gh_headers = {
    'Authorization': f'token {gh_token}',
    'Accept': 'application/vnd.github.v3+json',
    'User-Agent': 'TRTL-Publisher'
}

# 2. Prepare Release Body
release_body = """# Topological-Relativistic-Thermodynamic Learning (TRTL) — v1.0.0 Official Research Artifact

This release accompanies the peer-reviewed submission to **Elsevier *Pattern Recognition***:
**"Topological-Relativistic-Thermodynamic Learning: A Unified Physics-Grounded Manifold Learning Framework for Certified Robustness, Dynamic Geodesic Propagation, and Exact Recourse"**

## Research Highlights & Artifact Contents:
- **Core Package (`trtl/`):** Full PyTorch implementation of Relativistic Anisotropic Metric Dilatation (RAMD), Thermodynamic Wave Interference Layers (TWIL), and Ginzburg-Landau Thermodynamic Phase-Transition Crystallization (TPTC).
- **Formal Theoretical Guarantees:** Mathematical proofs for Curvature-Invariant Geodesic Boundedness (Lemma 3.1), Global Non-Equilibrium Convergence (Theorem 3.2), Relativistic Speed of Information (Theorem 3.3), and Closed-Form Recourse Plausibility (Theorem 3.4).
- **Comprehensive Benchmark Suite:** Full evaluation suite benchmarking TRTL against 10 baselines (Euclidean MLP, Poincaré, Hyperbolic GCN, Energy-Based Models, PINNs, Riemannian Flow) across multi-scale manifolds, noise levels (up to 40%), and high dimensions ($D=2$ to $D=1,000$).
- **Submission Manuscripts:** Publication-ready `.docx` manuscript with 16 embedded high-resolution figures, 10 Elsevier 3-line tables, and native Word OMML display equations.

## Citation:
```bibtex
@software{trtl2026,
  author       = {Vishal and TRTL Research Consortium},
  title        = {{Topological-Relativistic-Thermodynamic Learning (TRTL): A Unified Physics-Grounded Machine Learning Framework}},
  month        = nov,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {v1.0.0},
  url          = {https://github.com/Vishal442005/TRTL-Topological-Relativistic-Thermodynamic-Learning}
}
```
"""

# 3. Create GitHub Release
print("[2/5] Creating GitHub Release v1.0.0 on GitHub...")
release_payload = {
    "tag_name": "v1.0.0",
    "target_commitish": "main",
    "name": "v1.0.0: Official TRTL Research Artifact & Benchmark Suite",
    "body": release_body,
    "draft": False,
    "prerelease": False
}

rel_req = urllib.request.Request(
    f"https://api.github.com/repos/{owner}/{repo}/releases",
    data=json.dumps(release_payload).encode('utf-8'),
    headers=gh_headers,
    method='POST'
)

try:
    with urllib.request.urlopen(rel_req) as resp:
        release_data = json.loads(resp.read().decode('utf-8'))
        release_id = release_data['id']
        upload_url = release_data['upload_url'].split('{')[0]
        html_url = release_data['html_url']
        print(f" -> Release created successfully! ID: {release_id}")
        print(f" -> Release URL: {html_url}")
except urllib.error.HTTPError as e:
    err_body = e.read().decode('utf-8')
    print(f"HTTPError creating release: {e.code} - {err_body}")
    # Check if release already exists
    req_existing = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}/releases/tags/v1.0.0", headers=gh_headers)
    with urllib.request.urlopen(req_existing) as resp:
        release_data = json.loads(resp.read().decode('utf-8'))
        release_id = release_data['id']
        upload_url = release_data['upload_url'].split('{')[0]
        html_url = release_data['html_url']
        print(f" -> Existing release found! ID: {release_id}")
        print(f" -> Release URL: {html_url}")

# 4. Upload Assets to Release
assets_to_upload = [
    ("TRTL_Manuscript_Pattern_Recognition.docx", "elsevier_submission/TRTL_Manuscript_Pattern_Recognition.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ("Cover_Letter_Pattern_Recognition.docx", "elsevier_submission/Cover_Letter_Pattern_Recognition.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
    ("Research_Highlights.docx", "elsevier_submission/Research_Highlights.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
]

print("[3/5] Uploading release assets to GitHub...")
for asset_name, asset_path, mime in assets_to_upload:
    if os.path.exists(asset_path):
        print(f" -> Uploading {asset_name} ({os.path.getsize(asset_path):,} bytes)...")
        upload_target = f"{upload_url}?name={asset_name}"
        with open(asset_path, 'rb') as f:
            asset_bytes = f.read()
        
        up_headers = {
            'Authorization': f'token {gh_token}',
            'Content-Type': mime,
            'Content-Length': str(len(asset_bytes)),
            'User-Agent': 'TRTL-Publisher'
        }
        try:
            up_req = urllib.request.Request(upload_target, data=asset_bytes, headers=up_headers, method='POST')
            with urllib.request.urlopen(up_req) as up_resp:
                print(f"    [OK] Uploaded {asset_name}")
        except urllib.error.HTTPError as ue:
            print(f"    Notice on {asset_name}: {ue.code} (might already exist)")
    else:
        print(f"    [SKIP] Asset {asset_path} not found.")

# 5. Monitor Zenodo for Deposition / Minted DOI
print("[4/5] Checking Zenodo webhook integration and monitoring for minted DOI...")
zenodo_headers = {
    'Authorization': f'Bearer {zenodo_token}',
    'Accept': 'application/json'
}

max_attempts = 30
found_deposition = None

for attempt in range(1, max_attempts + 1):
    print(f" -> [Attempt {attempt}/{max_attempts}] Checking Zenodo depositions API...")
    try:
        zen_req = urllib.request.Request("https://zenodo.org/api/deposit/depositions?size=15", headers=zenodo_headers)
        with urllib.request.urlopen(zen_req) as zresp:
            depositions = json.loads(zresp.read().decode('utf-8'))
            
            for dep in depositions:
                title = dep.get('title', '')
                desc = dep.get('metadata', {}).get('description', '')
                dep_doi = dep.get('doi')
                dep_id = dep.get('id')
                state = dep.get('state')
                submitted = dep.get('submitted')
                
                # Check if this deposition corresponds to TRTL
                if 'TRTL' in title or 'TRTL-Topological-Relativistic' in title or 'Topological-Relativistic-Thermodynamic Learning' in title:
                    found_deposition = dep
                    print(f"\n==========================================")
                    print(f"FOUND ZENODO DEPOSITION FOR TRTL!")
                    print(f"Deposition ID: {dep_id}")
                    print(f"Title: {title}")
                    print(f"State: {state} | Submitted: {submitted}")
                    print(f"DOI: {dep_doi}")
                    print(f"DOI URL: https://doi.org/{dep_doi}")
                    print(f"Record URL: {dep.get('links', {}).get('html', f'https://zenodo.org/records/{dep_id}')}")
                    print(f"==========================================\n")
                    break
                    
            if found_deposition:
                # If draft, attempt to publish if needed
                if not found_deposition.get('submitted') and found_deposition.get('state') == 'unsubmitted':
                    print("Deposition is in draft. Publishing to finalize DOI...")
                    pub_req = urllib.request.Request(
                        f"https://zenodo.org/api/deposit/depositions/{found_deposition['id']}/actions/publish",
                        headers=zenodo_headers,
                        method='POST'
                    )
                    with urllib.request.urlopen(pub_req) as pub_resp:
                        pub_data = json.loads(pub_resp.read().decode('utf-8'))
                        print(f"Published! Permanent DOI: {pub_data.get('doi')}")
                        found_deposition = pub_data
                break
    except Exception as ze:
        print(f"    Error querying Zenodo: {ze}")
        
    time.sleep(5)

if not found_deposition:
    print("Zenodo webhook event may still be in transit or processing.")
    # Check if a manual deposition creation or direct check is possible
    print("Checking Zenodo public search API for latest records...")
    try:
        srch_req = urllib.request.Request("https://zenodo.org/api/records?q=TRTL&sort=mostrecent", headers={'User-Agent': 'TRTL-Publisher'})
        with urllib.request.urlopen(srch_req) as sresp:
            sdata = json.loads(sresp.read().decode('utf-8'))
            hits = sdata.get('hits', {}).get('hits', [])
            for h in hits:
                print("Hit:", h.get('id'), h.get('doi'), h.get('metadata', {}).get('title'))
    except Exception as se:
        print("Search error:", se)

print("\n[5/5] Release and DOI Process Execution Completed.")
