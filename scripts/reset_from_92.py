import json

path = r'D:\cmas-mcp\data\processed\youtube\processed_videos_v1.jsonl'
lines = []
with open(path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        obj = json.loads(line)
        if i >= 92:
            # Reset enrichment
            obj['enriched'] = False
            if 'summary' in obj: del obj['summary']
            if 'keywords' in obj: del obj['keywords']
            if 'entities' in obj: del obj['entities']
        lines.append(json.dumps(obj, ensure_ascii=False) + '\n')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Reset enrichment from index 92 onwards.")
