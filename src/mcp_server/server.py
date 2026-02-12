import os
import json
from mcp.server.fastmcp import FastMCP

# Inicializar FastMCP
mcp = FastMCP("CMAS Knowledge Server")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "raw")

def load_jsonl(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

@mcp.tool()
def list_videos():
    """Lista todos los videos disponibles de la Facultad de Ingeniería UDD (CMAS)."""
    videos_path = os.path.join(DATA_DIR, "youtube", "videos.jsonl")
    videos = load_jsonl(videos_path)
    return [{"id": v["id"], "title": v["title"], "published": v["published"]} for v in videos]

@mcp.tool()
def search_videos(query: str):
    """Busca videos por título o descripción."""
    videos_path = os.path.join(DATA_DIR, "youtube", "videos.jsonl")
    videos = load_jsonl(videos_path)
    results = [v for v in videos if query.lower() in v["title"].lower()]
    return results

@mcp.tool()
def get_video_summary(video_id: str):
    """Obtiene un resumen del contenido de un video para evitar el desbordamiento de contexto."""
    # Por ahora simulamos el resumen. En Fase 3 se integrará con el motor de transcripción.
    return f"Resumen del video {video_id}: Este video trata sobre innovación y tecnología en la Facultad de Ingeniería."

@mcp.tool()
def search_cmas_pages(query: str):
    """Busca información en las páginas web rastreadas de CMAS."""
    pages_path = os.path.join(DATA_DIR, "cmas_web", "pages.jsonl")
    pages = load_jsonl(pages_path)
    results = []
    for p in pages:
        if query.lower() in p["title"].lower() or query.lower() in p["content"].lower():
            results.append({
                "url": p["url"],
                "title": p["title"],
                "snippet": p["content"][:300] + "..."
            })
    return results

if __name__ == "__main__":
    mcp.run()
