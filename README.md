# CMAS MCP (Pre-Step1 Scaffold)

Estado: preparado **hasta antes del Paso/Fase 1** (sin análisis del repo guía ni implementación MCP todavía).

## Objetivo
Construir un pipeline de conocimiento para un MCP que combine:
1. Canal YouTube: https://www.youtube.com/@direcciondeinnovacion-inge4104
2. Sitio CMAS: https://cmas.udd.cl/

## Alcance actual (hecho)
- Estructura de carpetas creada.
- Análisis de arquitectura MCP documentado en `docs/02_mcp_baseline.md`.
- Scripts de ingesta para YouTube (mock) y CMAS Web (lxml) funcionales.
- Configuración base en `config/`.
- Esqueleto del servidor MCP en `src/mcp_server/server.py`.
- Smoke test realizado y documentado en `docs/03_smoke_test.md`.

## Setup
Para instalar las dependencias necesarias:
```bash
pip install httpx lxml pyyaml mcp
```

## Ejecución
1. **Ingesta de datos:**
   ```bash
   python scripts/ingest_youtube.py
   python scripts/scrape_cmas.py
   ```
2. **Iniciar servidor MCP:**
   ```bash
   python src/mcp_server/server.py
   ```

## Siguiente paso
- Fase 3: Procesamiento de videos (transcripción) y refinamiento del motor de búsqueda.
