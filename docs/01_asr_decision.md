# Decisión ASR del proyecto CMAS MCP

Fecha: 2026-02-12

## Decisión
Para este proyecto se usará **Whisper local estándar (`openai-whisper`)** como motor de transcripción por defecto.

## Motivo
En pruebas locales del entorno actual, Whisper estándar mostró mejor rendimiento práctico que faster-whisper para el caso evaluado (audio corto real).

## Alcance
- Proyecto: `D:\cmas-mcp`
- Uso: transcripción de audios para pipeline de conocimiento (YouTube/CMAS)

## Nota
faster-whisper queda instalado como alternativa, pero no será el motor principal por ahora.
