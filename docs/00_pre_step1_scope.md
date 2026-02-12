# Pre-Step1 Scope (anti-overflow)

## Fuentes a integrar en el pipeline

### A) YouTube
- Canal: `@direcciondeinnovacion-inge4104`
- Datos objetivo (más adelante):
  - listado de videos (id, título, fecha, url)
  - metadata
  - captions/transcripciones cuando existan

### B) Sitio web CMAS
- URL base: `https://cmas.udd.cl/`
- Datos objetivo (más adelante):
  - páginas institucionales relevantes
  - noticias/publicaciones
  - contenido técnico útil para base de conocimiento

## Estructura creada en D:\cmas-mcp
- `docs/`
- `config/`
- `scripts/`
- `src/`
- `data/raw/youtube/`
- `data/raw/cmas_web/`
- `data/processed/`

## Criterio anti-overflow aplicado
- Trabajo por lotes
- Resúmenes compactos
- Sin volcado de logs extensos al chat
- Entregables pequeños y trazables por etapa

## Límite actual
Detenido intencionalmente antes del Paso/Fase 1.
