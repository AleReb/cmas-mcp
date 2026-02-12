import json
import os

proc_path = "D:\\cmas-mcp\\data\\processed\\youtube\\processed_videos_v1.jsonl"
missing_indices = []
if os.path.exists(proc_path):
    with open(proc_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            item = json.loads(line)
            if not item.get('enriched'):
                missing_indices.append(i)

print(json.dumps(missing_indices[:50]))
