---
title: "Buscar en la web"
description: "Busca cualquier municipio, distintivo o trámite dentro de esta web."
layout: "search"
summary: "Buscador"
placeholder: "Busca un municipio, un distintivo o un trámite…"
draft: false

# Fuera del sitemap desde el 01/10/2026, al abrir el sitio a Google.
# Un buscador interno no es contenido: no hay nada que indexar en el, y Google
# desaconseja expresamente indexar paginas de resultados de busqueda interna.
sitemap:
  disable: true

# CORREGIDO EL 05/10/2026, y la correccion vale mas que el cambio.
#
# Aqui ponia que "esta pagina ya emite noindex por su propio layout". Era
# FALSO: el layout de busqueda del tema no menciona robots por ningun lado, y
# /search/ llevaba cuatro dias en produccion sirviendo `index, follow`. O sea
# que se saco del sitemap dando por hecho algo que no se cumplia, y el
# comentario tapaba el agujero en vez de enseñarlo.
#
# La clave buena es esta, y la lee themes/PaperMod/layouts/_partials/head.html
# en su linea 4. Comprobado en el HTML generado, no en el codigo.
robotsNoIndex: true
---
