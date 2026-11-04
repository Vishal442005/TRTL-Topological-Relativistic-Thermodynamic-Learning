import re
from docx import Document

doc = Document('elsevier_submission/TRTL_Manuscript_Pattern_Recognition.docx')

print(f"Total Paragraphs: {len(doc.paragraphs)}")
print(f"Total Tables: {len(doc.tables)}")

# 1. Check colors
blue_runs = []
for i, p in enumerate(doc.paragraphs):
    for r in p.runs:
        if r.font.color and r.font.color.rgb:
            rgb = str(r.font.color.rgb)
            if rgb != '000000':
                blue_runs.append((i, p.text[:40], rgb))

print(f"Non-black text runs count: {len(blue_runs)}")
if blue_runs:
    for b in blue_runs[:5]:
        print("  Found non-black run:", b)

# 2. Check for LaTeX backslashes
backslash_paras = []
for i, p in enumerate(doc.paragraphs):
    if '\\' in p.text:
        backslash_paras.append((i, p.text[:60]))

print(f"Paragraphs containing backslash '\\': {len(backslash_paras)}")
if backslash_paras:
    for bp in backslash_paras:
        print("  Backslash in para:", bp)

# 3. Check for 1st-person pronouns
first_person = []
fp_pattern = re.compile(r'\b(we|our|us|my|I)\b', re.IGNORECASE)
for i, p in enumerate(doc.paragraphs):
    # Ignore inside reference citations or bibliography titles if any
    if i > len(doc.paragraphs) - 25:
        continue
    matches = fp_pattern.findall(p.text)
    if matches:
        first_person.append((i, p.text[:60], matches))

print(f"First person pronouns in body text: {len(first_person)}")
if first_person:
    for fp in first_person:
        print("  1st person:", fp)

# 4. Check OMML equations
omml_count = 0
for p in doc.paragraphs:
    if 'oMath' in p._p.xml:
        omml_count += 1
print(f"Native OMML Equation Paragraphs: {omml_count}")
