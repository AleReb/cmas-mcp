import json
import re

path = r'C:\Users\Ale\.openclaw\agents\main\sessions\b5e81590-28f9-4698-ba94-75266b3a1300.jsonl'
output_path = r'D:\cmas-mcp\data\processed\youtube\batch_5_sub_107_114_summaries.json'

with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    msg_data = json.loads(lines[-1])
    content_list = msg_data['message']['content']
    
    for item in content_list:
        if item.get('type') == 'text':
            content = item.get('text', '')
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
    print("Could not find valid JSON.")
