"""
Download selected most similar papers from arXiv search results.
Filters and ranks papers published between 2020 and 2026 across TRTL's core physical pillars.
Downloads at least 15-18 full PDFs into 'papers/' directory.
"""

import os
import sys
import re
import json
import time
import urllib.request

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

KEYWORDS = [
    # Relativistic & Manifold
    "lorentzian", "relativistic", "pseudo-riemannian", "riemannian manifold", "metric learning", "hyperbolic",
    # Wave & Field
    "wave interference", "helmholtz", "wave packet", "phase field", "wave propagation", "coherent",
    # Thermodynamic
    "thermodynamic", "ginzburg-landau", "phase transition", "free energy", "non-equilibrium", "order parameter",
    # Recourse & Robustness
    "counterfactual recourse", "gradient flow", "geodesic", "certified robustness", "energy-based", "out-of-distribution"
]

def score_paper(p):
    text = (p['title'] + " " + p['summary']).lower()
    score = 0
    # Title matches are weighted 3x
    for kw in KEYWORDS:
        if kw in p['title'].lower():
            score += 4
        if kw in p['summary'].lower():
            score += 1
    # Bonus for newer papers
    score += (p['year'] - 2020) * 0.2
    return score

def select_and_download(input_json, papers_dir, target_count=16):
    ensure_dir(papers_dir)

    with open(input_json, "r", encoding="utf-8") as f:
        papers = json.load(f)

    print(f"[*] Loaded {len(papers)} candidate papers from {input_json}.")

    # Score and rank papers
    scored = []
    for pid, p in papers.items():
        s = score_paper(p)
        scored.append((s, p))

    scored.sort(key=lambda x: x[0], reverse=True)

    # Pick top diverse papers
    selected = []
    seen_titles = set()
    for s, p in scored:
        norm_title = re.sub(r'[^a-zA-Z0-9]', '', p['title'].lower()[:30])
        if norm_title not in seen_titles:
            seen_titles.add(norm_title)
            selected.append(p)
        if len(selected) >= target_count:
            break

    print(f"\n[*] Selected top {len(selected)} most relevant papers (2020-2026):")
    for i, p in enumerate(selected, 1):
        print(f"    {i:2d}. [{p['year']}] {p['id']}: {p['title'][:65]}...")

    # Download PDFs
    downloaded = []
    for i, p in enumerate(selected, 1):
        clean_id = p['id'].split('v')[0]
        # Clean title for filename
        slug = re.sub(r'[^a-zA-Z0-9_-]', '_', p['title'][:40]).strip('_')
        out_filename = f"{p['year']}_{clean_id}_{slug}.pdf"
        out_path = os.path.join(papers_dir, out_filename)

        print(f"\n[{i}/{len(selected)}] Downloading: {clean_id} -> {out_filename}...")
        if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
            print(f"    [SKIP] Already exists ({os.path.getsize(out_path)} bytes).")
            p['local_pdf'] = out_path
            downloaded.append(p)
            continue

        pdf_url = f"https://arxiv.org/pdf/{clean_id}.pdf"
        try:
            req = urllib.request.Request(pdf_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
                'Accept': 'application/pdf'
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read()

            if content.startswith(b'%PDF'):
                with open(out_path, 'wb') as f_out:
                    f_out.write(content)
                size_kb = len(content) / 1024.0
                print(f"    [OK] Downloaded {size_kb:.1f} KB.")
                p['local_pdf'] = out_path
                downloaded.append(p)
            else:
                print(f"    [WARN] Response not valid PDF (starts with {content[:15]}).")
        except Exception as e:
            print(f"    [FAIL] Failed to download {pdf_url}: {e}")

        time.sleep(3.2) # Strict arXiv rate-limit compliance

    print(f"\n[OK] Successfully downloaded {len(downloaded)} papers to '{papers_dir}'.")
    with open(os.path.join(papers_dir, "downloaded_papers_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(downloaded, f, indent=2)

    return downloaded

if __name__ == "__main__":
    papers_dir = "papers"
    input_json = "scripts/arxiv_search_results.json"
    if os.path.exists(input_json):
        select_and_download(input_json, papers_dir, target_count=16)
    else:
        print(f"Waiting for {input_json} to be created by task-385...")
