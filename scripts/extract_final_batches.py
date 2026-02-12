import json
import re
import os

files = [
    (r'C:\Users\Ale\.openclaw\agents\main\sessions\7bb12c2c-73fe-42dc-ad3a-7e721d306305.jsonl.deleted.2026-02-12T21-26-35.985Z', 'batch_5c_summaries.json'),
    (r'C:\Users\Ale\.openclaw\agents\main\sessions\8c69529b-82a4-4d5d-ab74-89014add005e.jsonl.deleted.2026-02-12T21-27-36.015Z', 'batch_5d_summaries.json')
]

for path, out_name in files:
    output_path = os.path.join(r'D:\cmas-mcp\data\processed\youtube', out_name)
    summaries = []
    if not os.path.exists(path):
        print(f"File not found: {path}")
        continue
        
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                msg = json.loads(line)
                if msg.get('type') == 'message' and msg.get('message', {}).get('role') == 'assistant':
                    content_parts = msg['message'].get('content', [])
                    if isinstance(content_parts, list):
                        for part in content_parts:
                            if part.get('type') == 'text':
                                text = part.get('text', '')
                                matches = re.findall(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL)
                                for match in matches:
                                    try:
                                        data = json.loads(match)
                                        if isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
                                            summaries = data
                                    except: continue
                    elif isinstance(content_parts, str):
                        matches = re.findall(r'\[\s*\{.*?\}\s*\]', content_parts, re.DOTALL)
                        for match in matches:
                             try:
                                 data = json.loads(match)
                                 if isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
                                     summaries = data
                             except: continue
            except: continue
            
    if summaries:
        with open(output_path, 'w', encoding='utf-8') as out:
            json.dump(summaries, out, indent=2, ensure_ascii=False)
        print(f"Extracted {len(summaries)} summaries to {output_path}")
    else:
        print(f"No summaries found in {path}")
