import json

with open("scripts/arxiv_search_results.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

print(f"Total candidate papers: {len(papers)}")
items = list(papers.items())
for i, (pid, p) in enumerate(items[25:60], 26):
    authors_str = ", ".join(p['authors'][:3])
    if len(p['authors']) > 3:
        authors_str += " et al."
    print(f"{i:2d}. [{p['year']}] {pid}: {p['title']}")
    print(f"    Authors: {authors_str}")
