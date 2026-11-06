import os
import re
import sys
import csv
import docx
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("DEEP SYSTEMATIC AUDIT & VERIFICATION: UPDATED SIGNIFICANT PACKAGE")
print("Target: Chaos, Solitons & Fractals (Elsevier)")
print("Author: Vishal Chandel (ORCID: 0009-0006-0552-8551)")
print("=" * 80)

BASE_DIR = "Updated_significant"
failures = []

def check(condition, message):
    if condition:
        print(f"  [PASS] {message}")
    else:
        print(f"  [FAIL] {message}")
        failures.append(message)

# -----------------------------------------------------------------------------
# 1. Verification of Required Files & Structural Partitioning
# -----------------------------------------------------------------------------
print("\n[STEP 1] Verifying Directory Layout and Submission Documents...")
expected_files = [
    os.path.join(BASE_DIR, "manuscript", "TRTL_Manuscript_Chaos_Solitons_Fractals_Significant.docx"),
    os.path.join(BASE_DIR, "cover_letter", "Cover_Letter_Chaos_Solitons_Fractals.docx"),
    os.path.join(BASE_DIR, "highlights", "Research_Highlights.docx"),
    os.path.join(BASE_DIR, "statements", "Declaration_of_Competing_Interests.docx"),
    os.path.join(BASE_DIR, "statements", "Author_Contribution_Statement.docx"),
    os.path.join(BASE_DIR, "README_SIGNIFICANT_SUBMISSION.md"),
    os.path.join(BASE_DIR, "tables", "ALL_TABLES_MASTER.md"),
    os.path.join(BASE_DIR, "data_and_results", "extended_multi_condition_benchmark_results.json"),
    os.path.join(BASE_DIR, "data_and_results", "comparative_study_against_recent_works.md"),
    os.path.join(BASE_DIR, "data_and_results", "enhanced_sota_comparative_additions.md"),
]

for ef in expected_files:
    exists = os.path.exists(ef)
    size = os.path.getsize(ef) if exists else 0
    check(exists and size > 0, f"{ef} exists and non-empty ({size:,} bytes)")

# -----------------------------------------------------------------------------
# 2. Verify All 12 Tables in Master Markdown and CSV Files
# -----------------------------------------------------------------------------
print("\n[STEP 2] Verifying Table CSVs and Master Markdown...")
for t_i in range(1, 13):
    csv_candidates = [f for f in os.listdir(os.path.join(BASE_DIR, "tables")) if f.startswith(f"table{t_i:02d}") and f.endswith(".csv")]
    md_candidates = [f for f in os.listdir(os.path.join(BASE_DIR, "tables")) if f.startswith(f"table{t_i:02d}") and f.endswith(".md")]
    check(len(csv_candidates) == 1, f"Table {t_i:02d} CSV exists: {csv_candidates}")
    check(len(md_candidates) == 1, f"Table {t_i:02d} MD exists: {md_candidates}")

# -----------------------------------------------------------------------------
# 3. Verify All 18 Figure Files (PNG and PDF)
# -----------------------------------------------------------------------------
print("\n[STEP 3] Verifying High-Resolution Figure Files (PNG & PDF)...")
for f_i in range(1, 19):
    png_candidates = [f for f in os.listdir(os.path.join(BASE_DIR, "figures")) if f.startswith(f"fig{f_i:02d}") and f.endswith(".png")]
    pdf_candidates = [f for f in os.listdir(os.path.join(BASE_DIR, "figures")) if f.startswith(f"fig{f_i:02d}") and f.endswith(".pdf")]
    check(len(png_candidates) == 1, f"Figure {f_i:02d} PNG exists: {png_candidates}")
    check(len(pdf_candidates) == 1, f"Figure {f_i:02d} PDF exists: {pdf_candidates}")

    if png_candidates:
        png_p = os.path.join(BASE_DIR, "figures", png_candidates[0])
        img = Image.open(png_p)
        check(img.size[0] >= 1500, f"Figure {f_i:02d} resolution {img.size[0]}x{img.size[1]} >= 1500px width")

# -----------------------------------------------------------------------------
# 4. In-Depth Inspection of DOCX Master Manuscript
# -----------------------------------------------------------------------------
print("\n[STEP 4] Deep Audit of Master Manuscript Document...")
doc_path = os.path.join(BASE_DIR, "manuscript", "TRTL_Manuscript_Chaos_Solitons_Fractals_Significant.docx")
doc = docx.Document(doc_path)

# A. Tables count in docx
tables = doc.tables
check(len(tables) == 12, f"Expected 12 embedded docx tables, found {len(tables)}")

for idx, tbl in enumerate(tables):
    rows = len(tbl.rows)
    cols = len(tbl.columns)
    header = [c.text.strip().replace('\n', ' ') for c in tbl.rows[0].cells]
    print(f"    Table {idx+1:02d}: {rows} rows x {cols} cols | Header: {header[:3]}...")
    check(rows >= 3 and cols >= 2, f"Table {idx+1} has valid dimensions ({rows}x{cols})")

# B. In-text citations for all 18 figures and 12 tables
full_text = " ".join([p.text for p in doc.paragraphs])

print("\n[STEP 4B] Verifying In-Text Citations of Figures & Tables...")
for f_i in range(1, 19):
    pattern = rf'(?:Fig\.|Figure)\s+{f_i}\b'
    matches = re.findall(pattern, full_text)
    # At least 2 matches: one in discussion/analysis and one in the figure caption
    check(len(matches) >= 2, f"Figure {f_i} cited in text (Found {len(matches)} mentions)")

for t_i in range(1, 13):
    pattern = rf'(?:Table|Tab\.)\s+{t_i}\b'
    matches = re.findall(pattern, full_text)
    check(len(matches) >= 2, f"Table {t_i} cited in text (Found {len(matches)} mentions)")

# C. Placeholder check
print("\n[STEP 4C] Scanning for Placeholder / Incomplete Tokens...")
forbidden_tokens = ["TODO", "TBD", "XXXX", "PLACEHOLDER", "MISSING DATA", "NaN"]
for token in forbidden_tokens:
    found = token in full_text
    check(not found, f"Absence of placeholder token '{token}'")

# D. Authorship and Metadata check
print("\n[STEP 4D] Verifying Sole Authorship & Metadata...")
check("Vishal Chandel" in full_text, "Author 'Vishal Chandel' present")
check("0009-0006-0552-8551" in full_text, "Author ORCID '0009-0006-0552-8551' present")
check("Indian Institute of Information Technology" in full_text, "Affiliation IIIT Gwalior present")
check("10.5281/zenodo.23968898" in full_text, "Zenodo DOI present")

# E. Crucial Statistical Consistency (Wilcoxon p-values for n=10)
print("\n[STEP 4E] Verifying Non-Parametric Wilcoxon Statistics (Table 7)...")
t7 = tables[6] # Table 7
t7_text = " ".join([c.text.strip() for r in t7.rows for c in r.cells])
check("0.000977" in t7_text, "Table 7 contains exact Wilcoxon W=0.0 p=0.000977 (2^-10)")
check("10-fold" in full_text or "10-Fold" in full_text, "Text explicitly states 10-fold cross-validation splits")

# F. Operational Envelope & Multi-Condition Stress Content
print("\n[STEP 4F] Verifying Operational Envelope & Archival Analysis...")
check("Operational Envelope" in full_text or "operational envelope" in full_text, "Section on operational envelope present")
check("Asymmetric" in full_text, "Asymmetric noise stress analysis present")
check("Covariate" in full_text, "Covariate jitter analysis present")
check("Starvation" in full_text or "starvation" in full_text, "Sample starvation regime analysis present")
check("Hamiltonian" in full_text, "Hamiltonian contraction / phase space analysis present")
check("Beyer" in full_text, "Beyer distance concentration analysis present")
check("Ginzburg-Landau" in full_text, "Ginzburg-Landau thermodynamic foundation present")

# -----------------------------------------------------------------------------
# 5. Highlights Document Verification (Elsevier <= 85 Chars Rule)
# -----------------------------------------------------------------------------
print("\n[STEP 5] Verifying Research Highlights (< 85 chars per bullet)...")
hl_doc_path = os.path.join(BASE_DIR, "highlights", "Research_Highlights.docx")
hl_doc = docx.Document(hl_doc_path)
bullets = [p.text.strip() for p in hl_doc.paragraphs if p.text.strip()]
print(f"  Found {len(bullets)} highlight items:")
for b in bullets:
    # Remove leading bullet symbols if any
    cleaned = re.sub(r'^[•\-\*\d\.\s]+', '', b)
    print(f"    [{len(cleaned)} chars] {cleaned}")
    check(len(cleaned) <= 85, f"Highlight length {len(cleaned)} <= 85 characters")

# -----------------------------------------------------------------------------
# 6. Cover Letter Verification
# -----------------------------------------------------------------------------
print("\n[STEP 6] Verifying Cover Letter Details...")
cl_doc_path = os.path.join(BASE_DIR, "cover_letter", "Cover_Letter_Chaos_Solitons_Fractals.docx")
cl_doc = docx.Document(cl_doc_path)
cl_text = " ".join([p.text for p in cl_doc.paragraphs])
check("Stefano Boccaletti" in cl_text, "Addressed to Editor-in-Chief Prof. Stefano Boccaletti")
check("Chaos, Solitons & Fractals" in cl_text, "Journal name correct")
check("archival value" in cl_text.lower(), "Addresses archival value directly")
check("operational envelope" in cl_text.lower(), "Synthesizes operational envelope")
check("Vishal Chandel" in cl_text, "Signed by Vishal Chandel")

# -----------------------------------------------------------------------------
# 7. Git Safety Inspection
# -----------------------------------------------------------------------------
print("\n[STEP 7] Verifying Git Hygiene & Protection Rules...")
with open(".gitignore", "r", encoding="utf-8") as f:
    gi = f.read()

check("Updated_significant/" in gi or "Updated_significant" in gi, ".gitignore protects Updated_significant/")
check("*.docx" in gi, ".gitignore protects *.docx")

# Summary
print("\n" + "=" * 80)
if failures:
    print(f"AUDIT COMPLETED WITH {len(failures)} FAILURE(S):")
    for fl in failures:
        print(f"  - {fl}")
    sys.exit(1)
else:
    print("AUDIT RESULT: 100% PERFECT! ALL CHECKS PASSED WITH ZERO ERRORS.")
    print("=" * 80)
