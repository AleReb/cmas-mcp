import json
import os

proc_path = os.path.join("D:\\cmas-mcp", "data/processed/youtube/processed_videos_v1.jsonl")
summary_paths = [
    os.path.join("D:\\cmas-mcp", "data/processed/youtube/batch_1_summaries.json"),
    os.path.join("D:\\cmas-mcp", "data/processed/youtube/batch_2_summaries.json"),
    os.path.join("D:\\cmas-mcp", "data/processed/youtube/batch_3_summaries.json")
]

summary_map = {}
for path in summary_paths:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            summaries = json.load(f)
            for s in summaries:
                summary_map[s['id']] = s

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
            updated_lines.append(item)

with open(proc_path, 'w', encoding='utf-8') as f:
    for item in updated_lines:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"Updated {len(summaries)} videos with real summaries.")
