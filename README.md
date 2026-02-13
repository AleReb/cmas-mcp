# CMAS MCP - Knowledge Pipeline

Este repositorio contiene la infraestructura para construir y alimentar un servidor de **Model Context Protocol (MCP)** especializado en el ecosistema de innovación y tecnología de la Facultad de Ingeniería UDD (Centro C+ y CMAS).

## Objetivo del Proyecto
El propósito central es transformar cientos de horas de contenido audiovisual y documentos técnicos en una base de conocimiento estructurada y accesible para Modelos de Lenguaje (LLMs). Esto permite que asistentes de IA puedan responder preguntas técnicas sobre proyectos como la extracción de litio, sensores ambientales, y gobernanza territorial con datos precisos y contextualizados.

## Estructura de Carpetas

### `data/` - El Corazón de los Datos
Esta carpeta gestiona el ciclo de vida de la información, desde su captura bruta hasta su refinamiento final.
- **`data/raw/`**: Almacena los datos originales sin procesar.
    - `youtube/`: Metadatos completos y archivos de subtítulos (`.vtt`) extraídos del canal de la Dirección de Innovación.
    - `cmas_web/`: Contenido crudo obtenido mediante crawling del sitio oficial CMAS UDD.
- **`data/processed/`**: Es la **Base de Conocimiento** optimizada para Inteligencia Artificial.
    - **Propósito:** Los LLMs no pueden "ver" videos ni procesar miles de transcripciones desordenadas eficientemente. En esta carpeta, los textos son limpiados, divididos en fragmentos (chunking) y enriquecidos con resúmenes ejecutivos, palabras clave y entidades identificadas.
    - **Archivo Maestro:** `processed_videos_v1.jsonl`. Es el archivo que lee el servidor MCP para entregar respuestas rápidas y precisas.

### `scripts/` - Herramientas de Automatización
Scripts en Python para las diferentes fases del pipeline:
- `ingest_youtube.py`: Descarga la lista completa de videos y metadatos.
- `fetch_captions.py`: Obtiene los subtítulos en múltiples idiomas.
- `process_pipeline.py`: Realiza la limpieza de texto y estructuración base.
- `process_next_batch.py`: Gestiona el procesamiento incremental por lotes de 10 videos.

### `src/mcp_server/` - El Servidor
Contiene la implementación del servidor MCP (basado en `FastMCP`) que expone las herramientas y recursos para que clientes como Claude Desktop puedan consultar este conocimiento.

---

## Alcance Actual (Completado)
- [x] **Fase 1 (Baseline):** Definición de arquitectura, transporte (stdio/http) y esquemas de respuesta.
- [x] **Fase 2 (Ingesta):** Captura del 100% de metadatos y subtítulos del canal de YouTube (193 videos).
- [x] **Fase 3 (Pipeline):** Estructuración de datos procesados, generación de índice léxico y limpieza de texto.
- [x] **Fase 4 (Enriquecimiento):** Generación del 100% de resúmenes ejecutivos, keywords técnicas e identificación de entidades para los 193 videos mediante IA. (Finalizado: 12 de febrero, 2026).
