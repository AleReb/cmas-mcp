import json
import os
from datetime import datetime

# En un entorno real usaríamos yt-dlp o la API de YouTube.
# Para este scaffold/smoke test, simularemos la obtención de datos si no hay API Key.
# Opcionalmente, el usuario puede instalar: pip install yt-dlp

def ingest_youtube(channel_url, output_path):
    print(f"Ingestando videos de: {channel_url}")
    
    # Datos de ejemplo para el smoke test
    mock_videos = [
        {
            "id": "vid1",
            "title": "Introducción a CMAS",
            "url": "https://www.youtube.com/watch?v=vid1",
            "published": "2024-01-01T10:00:00Z"
        },
        {
            "id": "vid2",
            "title": "Innovación en Ingeniería",
            "url": "https://www.youtube.com/watch?v=vid2",
            "published": "2024-01-15T12:00:00Z"
        }
    ]
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for video in mock_videos:
            f.write(json.dumps(video, ensure_ascii=False) + '\n')
            
    print(f"Guardados {len(mock_videos)} videos en {output_path}")

if __name__ == "__main__":
    CHANNEL_URL = "https://www.youtube.com/@direcciondeinnovacion-inge4104"
    OUTPUT = os.path.join("D:\\cmas-mcp", "data", "raw", "youtube", "videos.jsonl")
    ingest_youtube(CHANNEL_URL, OUTPUT)
