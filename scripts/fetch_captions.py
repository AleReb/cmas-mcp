import os
import yt_dlp
import json

def fetch_captions(video_ids, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['es', 'en'],
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegSubtitlesConvertor',
            'format': 'srt',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for vid in video_ids:
            url = f"https://www.youtube.com/watch?v={vid}"
            try:
                ydl.download([url])
            except Exception as e:
                print(f"Error downloading caption for {vid}: {e}")

if __name__ == "__main__":
    # Leer los primeros 10 videos del jsonl
    raw_path = os.path.join("D:\\cmas-mcp", "data", "raw", "youtube", "videos.jsonl")
    vids_to_fetch = []
    if os.path.exists(raw_path):
        with open(raw_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i >= 10: break
                v = json.loads(line)
                vids_to_fetch.append(v['id'])
    
    CAP_DIR = os.path.join("D:\\cmas-mcp", "data", "raw", "youtube", "captions")
    fetch_captions(vids_to_fetch, CAP_DIR)
