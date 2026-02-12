import json
import re
import os

files = [
    (r'C:\Users\Ale\.openclaw\agents\main\sessions\7bb12c2c-73fe-42dc-ad3a-7e721d306305.jsonl.deleted.2026-02-12T21-26-35.985Z', 'batch_5c_summaries.json'),
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
                data_line = json.loads(line)
                if data_line.get('type') == 'message':
                    msg = data_line.get('message', {})
                    if msg.get('role') == 'assistant':
                        content = msg.get('content', '')
                        if isinstance(content, list):
                            for part in content:
                                if part.get('type') == 'text':
                                    text = part.get('text', '')
                                    # Try finding [ { ... } ] anywhere
                                    match = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
                                    if match:
                                        try:
                                            json_data = json.loads(match.group(0))
                                            if isinstance(json_data, list) and len(json_data) > 0 and 'id' in json_data[0]:
                                                summaries = json_data
                                        except: pass
                        elif isinstance(content, str):
                            match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
                            if match:
                                try:
                                    json_data = json.loads(match.group(0))
                                    if isinstance(json_data, list) and len(json_data) > 0 and 'id' in json_data[0]:
                                        summaries = json_data
                                except: pass
            except: continue
            
    if summaries:
        with open(output_path, 'w', encoding='utf-8') as out:
            json.dump(summaries, out, indent=2, ensure_ascii=False)
        print(f"Extracted {len(summaries)} summaries to {output_path}")
    else:
        print(f"No summaries found in {path}")
