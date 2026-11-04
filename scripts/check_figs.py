import os
import re

with open('scripts/build_comprehensive_elsevier_manuscript.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'add_figure\(\s*doc,\s*"([^"]+)",\s*(\d+),\s*"([^"]+)",\s*"([^"]+)"'
matches = re.findall(pattern, text)
print(f'Total matches: {len(matches)}')
for path, num, title, desc in matches:
    print(f'Fig {num}: {path} (Exists: {os.path.exists(path)})')
