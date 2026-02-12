# Resultado de Smoke Test - Fase 1 & 2

Este documento registra los resultados de la prueba inicial de ingesta y estructura del servidor MCP.

## 1. Ingesta de YouTube
- **Script:** `scripts/ingest_youtube.py`
- **Resultado:** Exitoso (Mocked).
- **Registros generados:** 2 videos.
- **Ubicación:** `data/raw/youtube/videos.jsonl`

## 2. Raspado de CMAS Web
- **Script:** `scripts/scrape_cmas.py`
- **Método:** `httpx` + `lxml`.
- **Resultado:** Exitoso.
- **Páginas capturadas:** 2 (Home + 1 subpágina).
- **Observación:** Se respetó la estructura pero se detectó que `robots.txt` es permisivo aunque `urllib.robotparser` dio un aviso menor.

## 3. Servidor MCP (Esqueleto)
- **Script:** `src/mcp_server/server.py`
- **Estado:** Implementado con herramientas: `list_videos`, `search_videos`, `get_video_summary`, `search_cmas_pages`.
- **Dependencias necesarias:** `mcp` (FastMCP).

## 4. Configuración
- Archivos creados: `config/sources.yaml`, `config/pipeline.yaml`.
