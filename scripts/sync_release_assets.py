import json
import os
import subprocess
import urllib.request

res = subprocess.run(['git', 'credential', 'fill'], input='protocol=https\nhost=github.com\n', text=True, capture_output=True)
token = dict(line.split('=', 1) for line in res.stdout.strip().splitlines() if '=' in line).get('password')

headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json', 'User-Agent': 'TRTL-Publisher'}
owner = 'Vishal442005'
repo = 'TRTL-Topological-Relativistic-Thermodynamic-Learning'

# Get release v1.0.0
req = urllib.request.Request(f'https://api.github.com/repos/{owner}/{repo}/releases/tags/v1.0.0', headers=headers)
with urllib.request.urlopen(req) as resp:
    rel = json.loads(resp.read().decode())
    rel_id = rel['id']
    upload_url = rel['upload_url'].split('{')[0]
    assets = rel.get('assets', [])

print(f"Current release assets count: {len(assets)}")
# Delete old TRTL_Manuscript_Pattern_Recognition.docx asset if present
for a in assets:
    if a['name'] == 'TRTL_Manuscript_Pattern_Recognition.docx':
        print(f"Deleting older asset ID {a['id']}...")
        del_req = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}/releases/assets/{a['id']}", headers=headers, method='DELETE')
        with urllib.request.urlopen(del_req) as del_resp:
            print("Deleted successfully!")

# Upload new 9.02 MB manuscript
asset_path = "elsevier_submission/TRTL_Manuscript_Pattern_Recognition.docx"
asset_name = "TRTL_Manuscript_Pattern_Recognition.docx"
print(f"Uploading new {asset_name} ({os.path.getsize(asset_path):,} bytes)...")

with open(asset_path, 'rb') as f:
    asset_bytes = f.read()

up_headers = {
    'Authorization': f'token {token}',
    'Content-Type': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'Content-Length': str(len(asset_bytes)),
    'User-Agent': 'TRTL-Publisher'
}
up_req = urllib.request.Request(f"{upload_url}?name={asset_name}", data=asset_bytes, headers=up_headers, method='POST')
with urllib.request.urlopen(up_req) as up_resp:
    print(f"[OK] Successfully uploaded updated {asset_name} to GitHub Release v1.0.0!")
