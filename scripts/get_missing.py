import json
import os

proc_path = "D:\\cmas-mcp\\data\\processed\\youtube\\processed_videos_v1.jsonl"
missing = []
if os.path.exists(proc_path):
    with open(proc_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            item = json.loads(line)
            if not item.get('enriched'):
                missing.append((i, item['id']))

print(json.dumps(missing[:20]))
