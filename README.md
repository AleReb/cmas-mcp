# CMAS MCP (Pre-Step1 Scaffold)

Estado: preparado **hasta antes del Paso/Fase 1** (sin análisis del repo guía ni implementación MCP todavía).

## Objetivo
Construir un pipeline de conocimiento para un MCP que combine:
1. Canal YouTube: https://www.youtube.com/@direcciondeinnovacion-inge4104
2. Sitio CMAS: https://cmas.udd.cl/

## Alcance actual (Fases 1-3)
- **Fase 1 (Baseline):** Arquitectura MCP documentada en `docs/02_mcp_baseline.md`. Soporte para stdio, herramientas y recursos.
- **Fase 2 (Ingesta YT):** Ingesta completa de metadatos de YouTube implementada en `scripts/ingest_youtube.py`. Datos en `data/raw/youtube/`.
- **Fase 3 (Pipeline):** Procesamiento por lotes (limpieza, chunking, resúmenes base) implementado en `scripts/process_pipeline.py`. Resultados en `data/processed/youtube/`.

## Setup
```bash
pip install httpx lxml pyyaml mcp yt-dlp
```

## Ejecución
1. **Ingesta YouTube (Phase 2):**
   ```bash
   python scripts/ingest_youtube.py
   ```
2. **Pipeline de Conocimiento (Phase 3 - Lotes de 10):**
   ```bash
   python scripts/process_pipeline.py
   ```
3. **Servidor MCP:**
   ```bash
   python src/mcp_server/server.py
   ```

## Siguiente paso
- Fase 3: Procesamiento de videos (transcripción) y refinamiento del motor de búsqueda.
