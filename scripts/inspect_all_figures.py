import os
import re
from PIL import Image

with open('scripts/build_comprehensive_elsevier_manuscript.py', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = r'add_figure\(\s*doc,\s*"([^"]+)",\s*(\d+),\s*"([^"]+)"'
matches = re.findall(pattern, text)

print(f"Total Figures checked: {len(matches)}\n")
for path, num, title in matches:
    if os.path.exists(path):
        with Image.open(path) as img:
            w, h = img.size
            dpi = img.info.get('dpi', (72, 72))
            aspect = w / h
            print(f"Fig {num:>2s}: {path:<65s} | Size: {w:>5d}x{h:<5d} | DPI: {dpi} | Aspect: {aspect:.2f}")
    else:
        print(f"Fig {num:>2s}: MISSING -> {path}")
