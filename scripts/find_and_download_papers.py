"""
Find and download similar papers published from 2020 to 2026 on arXiv.
Queries multiple thematic domains matching TRTL:
1. Relativistic & Lorentzian Geometry in Machine Learning
2. Wave Interference & Helmholtz Machine Learning
3. Thermodynamic Phase Transitions & Ginzburg-Landau Theory in ML
4. Continuous Counterfactual Recourse along Dynamical Gradient Flows
5. Certified Adversarial Robustness in Physical / Energy Models
"""

import os
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

queries = [
    # 1. Relativistic & Lorentzian ML
    'all:"Lorentzian" AND (cat:cs.LG OR cat:stat.ML OR cat:math.ST)',
    'all:"pseudo-Riemannian" AND (cat:cs.LG OR cat:stat.ML)',
    'ti:"relativistic" AND (cat:cs.LG OR cat:stat.ML)',
    'all:"hyperbolic metric learning" AND (cat:cs.LG OR cat:stat.ML)',

    # 2. Wave & Physical Interference in ML
    'all:"wave interference" AND (cat:cs.LG OR cat:stat.ML OR cat:physics.comp-ph)',
    'all:"Helmholtz" AND (cat:cs.LG OR cat:stat.ML)',
    'ti:"phase field" AND (cat:cs.LG OR cat:stat.ML)',

    # 3. Thermodynamic & Ginzburg-Landau ML
    'all:"thermodynamic" AND ti:"neural" AND (cat:cs.LG OR cat:stat.ML)',
    'all:"Ginzburg-Landau" AND (cat:cs.LG OR cat:stat.ML OR cat:cond-mat.stat-mech)',
    'all:"phase transition" AND ti:"classification" AND (cat:cs.LG OR cat:stat.ML)',

    # 4. Continuous Counterfactual Recourse & Vector Fields
    'all:"counterfactual recourse" AND (all:"gradient flow" OR all:"geodesic" OR all:"manifold")',
    'all:"counterfactual explanations" AND all:"optimal transport" AND (cat:cs.LG OR cat:stat.ML)',

    # 5. Energy-Based Certified Robustness & Out-of-Distribution
    'all:"certified robustness" AND all:"energy-based" AND (cat:cs.LG OR cat:stat.ML)',
]

def search_arxiv_queries(queries, max_per_query=10):
    papers = {}
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    for q_idx, q in enumerate(queries):
        print(f"[*] Query {q_idx+1}/{len(queries)}: {q[:60]}...")
        encoded = urllib.parse.quote(q)
        url = f"http://export.arxiv.org/api/query?search_query={encoded}&start=0&max_results={max_per_query}&sortBy=submittedDate&sortOrder=descending"

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'TRTL-Research-Literature-Explorer/1.0 (mailto:research@trtl-learning.org)'})
            with urllib.request.urlopen(req, timeout=20) as resp:
                xml_data = resp.read()

            root = ET.fromstring(xml_data)
            for entry in root.findall('atom:entry', ns):
                id_url = entry.find('atom:id', ns).text
                arxiv_id = id_url.split('/abs/')[-1]
                title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                published = entry.find('atom:published', ns).text[:10]
                updated = entry.find('atom:updated', ns).text[:10]

                authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]

                # Filter: year between 2020 and 2026
                year = int(published[:4])
                if 2020 <= year <= 2026:
                    pdf_link = None
                    for link in entry.findall('atom:link', ns):
                        if link.attrib.get('title') == 'pdf':
                            pdf_link = link.attrib.get('href')

                    if not pdf_link:
                        clean_id = arxiv_id.split('v')[0]
                        pdf_link = f"https://arxiv.org/pdf/{clean_id}.pdf"

                    if arxiv_id not in papers:
                        papers[arxiv_id] = {
                            'id': arxiv_id,
                            'title': title,
                            'authors': authors,
                            'published': published,
                            'year': year,
                            'summary': summary,
                            'pdf_url': pdf_link,
                            'query': q
                        }
        except Exception as e:
            print(f"    [WARN] Query failed: {e}")

        time.sleep(3.2) # Strict compliance with arXiv 3-second rate limit

    print(f"\n[OK] Found {len(papers)} unique matching papers published between 2020 and 2026.")
    return papers

if __name__ == "__main__":
    papers = search_arxiv_queries(queries, max_per_query=8)
    import json
    with open("scripts/arxiv_search_results.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, indent=2)
    print(f"Saved metadata to scripts/arxiv_search_results.json")
