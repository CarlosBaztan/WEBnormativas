# Brief de montaje — portal normativa/fiscalidad del vehículo

Contexto de negocio: ver `PLAN.md` (mismo directorio). Este archivo manda sobre lo técnico.

## Stack
Hugo (extended) + tema ligero tipo PaperMod (submódulo git) · GitHub (repo privado) · Cloudflare Pages (build `hugo --gc --minify`, output `public`, var `HUGO_VERSION`) · sin backend · Windows.

## Reglas duras
1. Nunca publicar un dato sin verificar por el usuario. Default `estado_dato: pendiente` → excluido del build.
2. Ritmo: 4-6 piezas/mes. Nunca generar lotes masivos (scaled content abuse).
3. Al lanzar solo se publican `zbe/` y `etiquetas/`. El resto existe en estructura, sin contenido.
4. Cero anuncios encima del formulario de la herramienta. Hueco de anuncio solo DEBAJO del resultado.
5. Cada ficha cita fuente oficial + fecha de verificación, visible en página.
6. Prioridad técnica: Core Web Vitals y accesibilidad.

## Fase 1 — Estructura (hacer y parar a revisar)
- Instalar Hugo. Crear sitio. Tema como submódulo.
- Secciones: `zbe/ etiquetas/ impuestos/ itv/ multas/ tramites/ datos/ guias/ legal/`
- Front matter obligatorio en fichas: `title, description, municipio, provincia, ccaa, estado_zbe(activa|prevista|sin_zbe), fecha_vigor, etiquetas_permitidas, horario_restriccion, excepciones, fuente_nombre, fuente_url, fecha_verificacion, estado_dato(verificado|pendiente)`
- Partial que renderiza "Fuente: X · enlace · Verificado el DD/MM/AAAA"; si `pendiente`, aviso visible.
- Build excluye `estado_dato: pendiente`.
- `legal/`: privacidad, aviso-legal, cookies, contacto (vacías).
- sitemap + robots + schema.org (FAQPage en guías, Dataset en `/datos/`).
- README: arrancar local, publicar, añadir ficha.
- Entregar solo 1 ficha de ejemplo (ZBE Zaragoza) en estado pendiente.

## Fase 2 — Herramienta "¿Puedo circular?"
Página Hugo + JS cliente. Input: tipo vehículo, combustible, año → deduce etiqueta DGT (0/ECO/C/B/sin), con las reglas documentadas en comentarios. Selector de municipio. Output: puede circular o no + horarios + excepciones + bloque fuente/fecha.
- Datos desde `data/*.json` de Hugo, nunca hardcodeados.
- Municipio no verificado → decirlo, no inventar.
- Accesible (teclado + ARIA). `div` reservado para anuncio bajo el resultado.
- Perfil de vehículo en localStorage (avisando) para reutilizar en IVTM/ITV.

## Fase 3 — Pipeline de datos (`/pipeline/`, fuera del sitio)
Python, idempotente, con log de cambios entre ejecuciones.
Fuentes: NAP-DGT ZBE (DATEX2V3, CC-BY) · listado ZBE MITECO · consulta impositiva municipal de Hacienda (IVTM, export masivo) · DGT en cifras (ancho fijo).
Salidas: `data/zbe.json`, `data/ivtm.json` (consumo Hugo) + `static/datos/*.csv|json` (descarga pública).
Cada registro: `fuente_url`, `fecha_descarga`, `confianza(oficial|derivado|pendiente_verificacion)`.
Script extra de auditoría: listar fichas con `fecha_verificacion` > 6 meses.
Páginas en `/datos/`: contenido, metodología, licencia CC-BY, fecha, descargas, schema Dataset.

## Fase 4 — Publicación
Instalar `gh` y `wrangler`; avisar antes de `gh auth login` / `wrangler login` (el usuario autoriza en navegador). Repo privado + push. Proyecto en Cloudflare Pages conectado al repo. Devolver URL `.pages.dev`. No conectar dominio propio todavía.

## Fase 5 — Pre-AdSense (cuando haya 20-30 páginas)
Rellenar páginas legales. Integrar CMP certificada por Google (la gratuita de AdSense, "Privacidad y mensajes") — obligatoria para servir anuncios en el EEE. Activar los huecos de anuncio.

## Agentes a usar
`engineering-frontend-developer` (tema + herramienta) · `engineering-devops-automator` (deploy) · `engineering-data-visualization-engineer` (mapas/gráficos) · `marketing-seo-specialist` (hub-and-spoke, long tail local) · `marketing-content-creator` (borradores) · `marketing-ai-citation-strategist` (citabilidad) · `testing-performance-benchmarker` · `testing-accessibility-auditor`
