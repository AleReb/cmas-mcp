import os
import json
import yt_dlp
from datetime import datetime

def ingest_youtube_full(channel_url, output_dir):
    print(f"Iniciando ingesta completa de: {channel_url}")
    
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "videos.jsonl")
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['es', 'en'],
        'outtmpl': os.path.join(output_dir, 'captions', '%(id)s.%(ext)s'),
    }
    
    videos_data = []
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)
            if 'entries' in info:
                for entry in info['entries']:
                    if not entry: continue
                    video_meta = {
                        "id": entry.get("id"),
                        "title": entry.get("title"),
                        "url": entry.get("url") or f"https://www.youtube.com/watch?v={entry.get('id')}",
                        "date": entry.get("upload_date") or datetime.now().strftime("%Y%m%d"),
                        "description": entry.get("description", ""),
                        "duration": entry.get("duration"),
                        "view_count": entry.get("view_count"),
                        "ingested_at": datetime.now().isoformat()
                    }
                    videos_data.append(video_meta)
        except Exception as e:
            print(f"Error extrayendo info del canal: {e}")
            # Fallback a mock si falla la red o API en este entorno
            return

    with open(output_file, 'w', encoding='utf-8') as f:
        for v in videos_data:
            f.write(json.dumps(v, ensure_ascii=False) + '\n')
            
    print(f"Ingesta finalizada: {len(videos_data)} videos guardados en {output_file}")

if __name__ == "__main__":
    CHANNEL = "https://www.youtube.com/@direcciondeinnovacion-inge4104"
    RAW_DIR = os.path.join("D:\\cmas-mcp", "data", "raw", "youtube")
    ingest_youtube_full(CHANNEL, RAW_DIR)
