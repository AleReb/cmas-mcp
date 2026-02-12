import json
import os
import sys

proc_path = os.path.join("D:\\cmas-mcp", "data/processed/youtube/processed_videos_v1.jsonl")

# If arguments are provided, use them as summary files. Otherwise, use all batches in the folder.
summary_paths = []
if len(sys.argv) > 1:
    summary_paths = sys.argv[1:]
else:
    # Default behavior: look for all batch_X_summaries.json files
    folder = os.path.join("D:\\cmas-mcp", "data/processed/youtube")
    summary_paths = [os.path.join(folder, f) for f in os.listdir(folder) if f.startswith("batch_") and f.endswith("_summaries.json")]

summary_map = {}
for path in summary_paths:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            try:
                summaries = json.load(f)
                for s in summaries:
                    summary_map[s['id']] = s
            except Exception as e:
                print(f"Error reading {path}: {e}")

updated_count = 0
updated_lines = []
if os.path.exists(proc_path):
    with open(proc_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            if item['id'] in summary_map:
                s = summary_map[item['id']]
                item['summary'] = s['summary']
                item['keywords'] = s['keywords']
                item['entities'] = s['entities']
                item['enriched'] = True
                updated_count += 1
            updated_lines.append(item)

with open(proc_path, 'w', encoding='utf-8') as f:
    for item in updated_lines:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"Merge complete. Total enriched videos in master: {updated_count}")
