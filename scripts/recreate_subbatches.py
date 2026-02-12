import os
import json
import sys

# Add script dir to path to import prepare_specific_batch
sys.path.append(r'D:\cmas-mcp\scripts')
from prepare_specific_batch import prepare_specific_batch

batches = [
    (range(92, 100), 'subbatch_92_99.json'),
    (range(100, 108), 'subbatch_100_107.json'),
    (range(108, 116), 'subbatch_108_115.json'),
    (range(116, 122), 'subbatch_116_121.json')
]

for indices, name in batches:
    data = prepare_specific_batch(list(indices))
    path = os.path.join(r'D:\cmas-mcp\data\processed\youtube', name)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Created {path} with {len(data)} videos.")
