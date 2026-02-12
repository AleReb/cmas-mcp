import json
import re

path = r'C:\Users\Ale\.openclaw\agents\main\sessions\7bb12c2c-73fe-42dc-ad3a-7e721d306305.jsonl'
output_path = r'D:\cmas-mcp\data\processed\youtube\batch_5c_summaries.json'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    msg_data = json.loads(lines[6])
    content_list = msg_data['message']['content']
    
    for item in content_list:
        if item.get('type') == 'text':
            content = item.get('text', '')
            # Look for [ { ... } ]
            matches = re.findall(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
            if matches:
                for match in reversed(matches):
                    try:
                        data = json.loads(match)
                        if isinstance(data, list) and len(data) > 0 and 'id' in data[0]:
                            with open(output_path, 'w', encoding='utf-8') as out:
                                json.dump(data, out, indent=2, ensure_ascii=False)
                            print(f"Successfully extracted {len(data)} summaries to {output_path}")
                            exit(0)
                    except:
                        continue
    print("Could not find valid JSON in text parts of line 7.")
