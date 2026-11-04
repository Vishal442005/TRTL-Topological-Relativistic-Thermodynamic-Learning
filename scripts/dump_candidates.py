import json

with open("scripts/arxiv_search_results.json", "r", encoding="utf-8") as f:
    papers = json.load(f)

with open("scripts/all_candidates_summary.txt", "w", encoding="utf-8") as out:
    for i, (pid, p) in enumerate(papers.items(), 1):
        clean_authors = ", ".join(p['authors'][:3])
        if len(p['authors']) > 3:
            clean_authors += " et al."
        out.write(f"[{i:2d}] Year: {p['year']} | ID: {pid}\n")
        out.write(f"     Title: {p['title']}\n")
        out.write(f"     Authors: {clean_authors}\n")
        out.write(f"     Summary: {p['summary'][:160]}...\n")
        out.write("-" * 80 + "\n")

print("Wrote all candidates summary to scripts/all_candidates_summary.txt")
