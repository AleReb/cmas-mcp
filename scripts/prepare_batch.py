import os
import json
import re

def clean_vtt(vtt_content):
    lines = vtt_content.split('\n')
    text_lines = []
    for line in lines:
        if not line.strip() or line.strip() == "WEBVTT" or "-->" in line or line.strip().isdigit():
            continue
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        if clean_line:
            text_lines.append(clean_line)
    final_lines = []
    for line in text_lines:
        if not final_lines or line != final_lines[-1]:
            final_lines.append(line)
    return " ".join(final_lines)

raw_path = os.path.join("D:\\cmas-mcp", "data/raw/youtube", "videos.jsonl")
cap_dir = os.path.join("D:\\cmas-mcp", "data/raw/youtube", "captions")

def prepare_batch(offset, limit=20):
    batch_data = []
    if os.path.exists(raw_path):
        with open(raw_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # Handle list slicing safely
            target_lines = lines[offset : offset + limit]
            for line in target_lines:
                video = json.loads(line)
                vid_id = video['id']
                
                transcript = ""
                for lang in ['es', 'en']:
                    cap_path = os.path.join(cap_dir, f"{vid_id}.{lang}.vtt")
                    if os.path.exists(cap_path):
                        with open(cap_path, 'r', encoding='utf-8') as f_cap:
                            transcript = clean_vtt(f_cap.read())
                        break
                
                batch_data.append({
                    "id": vid_id,
                    "title": video.get("title"),
                    "description": video.get("description"),
                    "transcript": transcript
                })
    return batch_data

if __name__ == "__main__":
    import sys
    # offset starts at 0 for the first line
    off = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    print(json.dumps(prepare_batch(off, limit), ensure_ascii=False))
