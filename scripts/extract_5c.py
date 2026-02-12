import json
import re
import os

path = r'C:\Users\Ale\.openclaw\agents\main\sessions\7bb12c2c-73fe-42dc-ad3a-7e721d306305.jsonl'
output_path = r'D:\cmas-mcp\data\processed\youtube\batch_5c_summaries.json'

summaries = []
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            msg = json.loads(line)
            if msg.get('role') == 'assistant':
                content = msg.get('content', '')
                if not content: continue
                
                # The subagent output is in a "Findings" block or similar
                # Let's try to find [ { ... } ]
                # Sometimes it's inside markdown code blocks
                matches = re.findall(r'\[\s*\{.*?\}\s*\]', content, re.DOTALL)
                for match in matches:
                    try:
                        data = json.loads(match)
                        if isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
                            summaries = data
                    except:
                        continue
        except:
            continue

if summaries:
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(summaries)} summaries to {output_path}")
else:
    print("No summaries found in transcript.")
