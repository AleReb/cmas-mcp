# Baseline Técnico: Arquitectura MCP

Este documento resume las decisiones de arquitectura basadas en el análisis de `github-mcp-server` y las mejores prácticas del Model Context Protocol (MCP).

## 1. Patrón de Implementación
Se adopta el patrón de **Servidor MCP basado en Herramientas (Tools)** utilizando la librería `fastmcp` para Python. Este enfoque permite una definición declarativa y tipada de las capacidades del servidor.

### Similitudes con GitHub MCP Server:
- **Herramientas de Búsqueda y Lectura:** Al igual que el servidor de GitHub expone herramientas para buscar repositorios y leer archivos, CMAS MCP expondrá herramientas para buscar videos y leer transcripciones/páginas web.
- **Manejo de Contexto:** Se implementará una estrategia "anti-overflow" para evitar saturar el contexto del LLM con datos crudos excesivos.
- **Configuración vía Entorno/YAML:** Las fuentes y parámetros se gestionarán externamente.

## 2. Estructura de Datos
- **Raw Data:** JSONL para almacenamiento eficiente de registros (videos, páginas).
- **Metadata:** Esquema mínimo (id, título, url, fecha, contenido/resumen).

## 3. Estrategia Anti-Overflow
- **Resúmenes:** En lugar de devolver transcripciones completas de 1 hora, se devolverán resúmenes o fragmentos relevantes.
- **Paginación/Límites:** Las herramientas de búsqueda limitarán el número de resultados devueltos por defecto.

## 4. Herramientas Definidas
1. `list_videos`: Lista videos disponibles con metadatos básicos.
2. `search_videos`: Búsqueda semántica o por palabras clave en los títulos/descripciones.
3. `get_video_summary`: Obtiene el resumen de un video específico (evitando el "overflow" del contenido completo).
4. `search_cmas_pages`: Busca información en las páginas rastreadas del sitio CMAS.
