import os
import json
import yt_dlp
import re
from datetime import datetime

# Configuración de rutas
BASE_DIR = "D:\\cmas-mcp"
RAW_PATH = os.path.join(BASE_DIR, "data/raw/youtube/videos.jsonl")
CAP_DIR = os.path.join(BASE_DIR, "data/raw/youtube/captions")
PROC_PATH = os.path.join(BASE_DIR, "data/processed/youtube/processed_videos_v1.jsonl")

def clean_vtt(vtt_content):
    lines = vtt_content.split('\n')
    text_lines = []
    for line in lines:
        if not line.strip() or line.strip() == "WEBVTT" or "-->" in line or line.strip().isdigit():
            continue
        clean_line = re.sub(r'<[^>]+>', '', line).strip()
        if clean_line: text_lines.append(clean_line)
    final_lines = []
    for line in text_lines:
        if not final_lines or line != final_lines[-1]:
            final_lines.append(line)
    return " ".join(final_lines)

def process_video(video):
    vid_id = video['id']
    title = video.get("title") or ""
    desc = video.get("description") or ""
    
    # 1. Fetch Caption
    ydl_opts = {
        'skip_download': True, 'writesubtitles': True, 'writeautomaticsub': True,
        'subtitleslangs': ['es', 'en'], 'quiet': True,
        'outtmpl': os.path.join(CAP_DIR, '%(id)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try: ydl.download([f"https://www.youtube.com/watch?v={vid_id}"])
        except: pass

    # 2. Read Transcript
    transcript = ""
    for lang in ['es', 'en']:
        cap_path = os.path.join(CAP_DIR, f"{vid_id}.{lang}.vtt")
        if os.path.exists(cap_path):
            with open(cap_path, 'r', encoding='utf-8') as f:
                transcript = clean_vtt(f.read())
            break
    
    # Placeholder para resumen
    summary = f"Contenido extraído de la descripción y transcripción ({len(transcript)} chars)." if transcript else "Sin transcripción disponible."
    
    return {
        "id": vid_id, "title": title, "summary": summary,
        "keywords": [], "entities": [], "has_transcript": bool(transcript),
        "transcript_raw": transcript,
        "version": "1.2", "processed_at": datetime.now().isoformat()
    }

def run_batch(offset, limit=10):
    if not os.path.exists(RAW_PATH): return
    with open(RAW_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    batch = lines[offset:offset+limit]
    results = []
    for line in batch:
        video = json.loads(line)
        print(f"Procesando: {video['title']}...")
        results.append(process_video(video))
    
    existing = {}
    if os.path.exists(PROC_PATH):
        with open(PROC_PATH, 'r', encoding='utf-8') as f:
            for l in f:
                item = json.loads(l)
                existing[item['id']] = item
    
    for r in results:
        existing[r['id']] = r
        
    with open(PROC_PATH, 'w', encoding='utf-8') as f:
        for item in existing.values():
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            
    print(f"Batch {offset}-{offset+limit} completado.")

if __name__ == "__main__":
    import sys
    off = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    run_batch(off)
