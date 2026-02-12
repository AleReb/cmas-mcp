import json
import re
import os

path = r'C:\Users\Ale\.openclaw\agents\main\sessions\7bb12c2c-73fe-42dc-ad3a-7e721d306305.jsonl.deleted.2026-02-12T21-26-35.985Z'
output_path = r'D:\cmas-mcp\data\processed\youtube\batch_5c_summaries.json'

all_text = ""
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        all_text += line

# Use a non-greedy but inclusive pattern for the JSON list
# Finding [ { ... } ]
matches = re.findall(r'\[\s*\{.*\}\s*\]', all_text, re.DOTALL)
best_data = None
for match in matches:
    # Handle escaping if it was inside a JSON string
    # Replace \" with " and \\ with \
    processed = match.replace('\\"', '"').replace('\\\\', '\\').replace('\\n', '\n')
    try:
        data = json.loads(processed)
        if isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
            best_data = data
    except:
        continue

if best_data:
    with open(output_path, 'w', encoding='utf-8') as out:
        json.dump(best_data, out, indent=2, ensure_ascii=False)
    print(f"Successfully extracted {len(best_data)} summaries to {output_path}")
else:
    print("Could not find valid JSON in the entire file.")
