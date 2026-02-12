# Baseline Técnico: Arquitectura MCP (v2)

Este documento detalla la arquitectura del servidor MCP basada en el análisis de `github-mcp-server` y los requerimientos del proyecto CMAS.

## 1. Protocolo y Transporte
Siguiendo el estándar MCP, se implementarán los siguientes transportes:
- **stdio (Estándar):** Para integración directa con clientes locales (e.g., Claude Desktop).
- **HTTP/SSE (Opcional):** Para integraciones distribuidas si se requiere en fases posteriores.

## 2. Primitivas MCP
- **Tools (Herramientas):** Acciones ejecutables para búsqueda y recuperación de información específica.
  - `list_videos`: Lista general con paginación.
  - `search_videos`: Búsqueda léxica/semántica.
- **Resources (Recursos):** Datos estáticos o dinámicos accesibles vía URIs.
  - `youtube://video/{id}/summary`: Acceso al resumen procesado.
  - `cmas://page/{slug}`: Contenido de páginas web.
- **Prompts (Plantillas):** Guías para que el LLM interactúe con el conocimiento de CMAS.

## 3. Esquema de Respuesta y Paginación
- **Schema:** Las respuestas seguirán el formato JSON-RPC 2.0 de MCP.
- **Paginación:** Las herramientas de listado aceptarán parámetros `cursor` o `offset` para manejar grandes volúmenes de datos.
- **Caching:** Se implementará una capa de caché en `data/cache/` para metadatos frecuentes de la API de YouTube.

## 4. Estructura de Datos (Anti-Overflow)
Para evitar saturar el contexto del modelo:
- Las herramientas de búsqueda devolverán **snippets** (fragmentos) y **metadatos**.
- El contenido completo solo se entregará bajo demanda mediante recursos específicos de "lectura profunda".

## 5. Template Base
El archivo `src/mcp_server/server.py` actúa como el template base, utilizando `FastMCP` para facilitar la extensión de herramientas y recursos.
