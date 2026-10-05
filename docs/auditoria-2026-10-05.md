# Auditoría interna y análisis SEO

**Fecha:** 05/10/2026. **Alcance:** las 45 páginas que genera el build de producción, el dataset publicado, la configuración y las fuentes oficiales citadas.

Todo lo que sigue está medido sobre el build de producción o sobre `cocheapto.com` en vivo. Donde no he podido medir algo, lo digo.

---

## 1. Fallos encontrados y ya corregidos

### 1.1. El autor de las 42 páginas era el nombre viejo del sitio

`hugo.toml` seguía con `author = "Normativa del vehículo"`, que es como se llamaba el sitio **antes del 01/10**. Al cambiar la marca se cambió `site.Title` y este se quedó atrás.

Salía en dos sitios visibles para Google: el `<meta name=author>` de cada página y el `author.name` del JSON-LD de tipo `BlogPosting`. En un sitio que habla de multas y de normativa, la firma no es decorativa.

Corregido a `Coche Apto`.

### 1.2. La comprobación de fuentes daba dos falsas alarmas

La auditoría diaria daba por rotas dos fuentes oficiales que estaban perfectamente en pie:

| Fuente | Qué pasaba | Realidad |
|:---|:---|:---|
| `benidorm.org` | 405 a `HEAD` | 200 a `GET`, con 64 KB de página |
| `granada.org` | 403 | Va tras Akamai y responde según la huella de la petición: 403 con un `User-Agent` de navegador, 200 sin ninguno. Hasta su portada |

Dos arreglos: `_codigo_http` reintenta con `GET` cuando `HEAD` falla, y captura `HTTPError` para poder **leer** el código (sin eso, `urlopen` lanza excepción con cualquier cosa desde 400 y un 403 llegaba arriba como «no responde», indistinguible de un servidor caído).

Y `enlaces_rotos` devuelve ahora dos listas: las rotas de verdad, que cuentan como incidencia, y las que no se pueden comprobar solas (401, 403, 405, 429), que se listan para mirarlas a mano y **no** cuentan.

Importa más de lo que parece: un aviso que grita sin motivo se deja de mirar, y entonces el día que avise de algo real tampoco se mirará.

**Resultado: de 2 incidencias falsas a 0.**

### 1.3. El buscador llevaba cuatro días invitando a Google a indexarlo

`/search/` se sacó del sitemap el 01/10 con este comentario escrito en su front matter:

> «Esta página ya emite `noindex` por su propio layout.»

**Era falso.** El layout de búsqueda del tema no menciona `robots` por ningún lado, y la página llevaba desde entonces sirviendo `index, follow` en producción. Se sacó del sitemap dando por hecho algo que no se cumplía, y el comentario tapaba el agujero en vez de enseñarlo.

Corregido con `robotsNoIndex: true`, que es la clave que lee la plantilla del tema. Comprobado en el HTML generado, no en el código: **una página con `noindex` en todo el sitio, y es esa.**

La lección es la del comentario, no la de la etiqueta: un comentario que afirma un comportamiento sin que nadie lo haya comprobado es peor que no tener comentario, porque el siguiente que pase se lo cree.

---

## 2. Lo que la auditoría NO encontró

Esto también es información, y conviene tenerla por escrito para no volver a buscarla:

| Comprobación | Resultado |
|:---|:---|
| Enlaces internos rotos | **0** |
| Saltos en la jerarquía de encabezados (h2 → h4) | **0** |
| Páginas con más de un `h1`, o sin `h1` | **0** (salvo los redirectores de Hugo) |
| Imágenes sin `alt` | **0** |
| Enlaces externos sin `rel="noopener"` | **0** |
| Canónicos incoherentes o fuera de dominio | **0** |
| Títulos duplicados · descripciones duplicadas | **0** · **0** |
| Títulos o descripciones vacíos | **0** |
| Fechas en el futuro (`buildFuture` descarta en silencio) | **0** |
| JSON-LD que no parsea | **0** |
| Propiedades de objeto con tipo no esperado por Google | **0** |
| Recursos servidos por `http://` | **0** |
| Cookies en producción | **0** |
| Scripts de terceros fuera de las páginas con mapa | **0** |

**Un aviso sobre una de estas cifras.** La primera vez que medí las imágenes me salieron 172 sin `alt`. Era falso: el minificador convierte `alt=""` en el atributo suelto `alt`, que en HTML5 vale lo mismo, y mi regla de medida no lo contemplaba. La web estaba bien; la medición, no.

---

## 3. Política de Google y Search Console

### 3.1. Lo que está en regla

- **Indexación.** `robots.txt` en `Allow: /`, sin `noindex` en ninguna página real, 41 URL en el sitemap y todas con el dominio bueno. Canónicos coherentes en las 42.
- **Rastreadores de IA.** GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot, Google-Extended y Bingbot reciben **200**. Es una decisión deliberada del plan: ser la fuente citada en una respuesta generada es el canal de autoridad más barato para un dominio sin presupuesto de enlaces.
- **Autoría y método (E-E-A-T).** `/sobre/` nombra a una persona real con su formación y `/metodología/` publica la jerarquía de fuentes y la regla de no publicar por encima del nivel de confianza que se tiene. Para contenido con consecuencias económicas, esto es justo lo que Google pide y está por encima de la media del nicho.
- **Contenido a escala.** El ritmo de 4-6 piezas al mes, cada una con ordenanza leída, artículo citado y fecha, es la defensa frente a la política de *scaled content abuse*. Conviene no acelerarlo aunque se pueda.
- **Legales.** Cero cookies en producción, y la página de cookies lo promete por escrito y acierta. La política de privacidad declara a Cloudflare, Google y OpenStreetMap, con bases jurídicas y transferencias internacionales.
- **Sin JavaScript**, la portada sirve 395 palabras y 12 enlaces a fichas en el HTML. No depende del navegador para ser rastreable.
- **Camino crítico ligero**: una hoja de estilos, un script, **cero fuentes web externas**.

### 3.2. Riesgos reales, por orden

**1. `www` y `http` responden 200 sin redirigir.** Ya estaba en la lista de pendientes, pero ahora hay una medición que lo justifica: **Bing tiene indexada una sola URL nuestra, la portada, y además la variante `http://`**. Perplexity y la búsqueda de ChatGPT se apoyan en Bing. Esto deja de ser higiene y pasa a ser un canal perdido.

**2. El bloqueo de rastreadores de IA de Cloudflare no se puede comprobar desde fuera.** Mis pruebas usan la cadena de identificación, y Cloudflare bloquea por firma verificada. Cloudflare lo activa por defecto en zonas nuevas. **Hay que mirarlo en el panel.**

**3. Dos páginas delgadas y una tercera discutible.**

| Página | Palabras | Qué es |
|:---|---:|:---|
| `/datos/` | 101 | Índice de sección, con un solo dataset dentro |
| `/multas/` | 147 | Índice de sección, con un solo artículo dentro |
| `/search/` | 14 | El buscador. **Ya resuelto**, ver 1.3 |

Ninguna es contenido basura: son páginas de navegación, y las dos de sección crecerán solas conforme se publique en ellas. **No hay que tocarlas.**

**4. El `Organization` de la portada sigue con `logo: /favicon.ico` y `sameAs: []`.** Decidido ayer dejarlo: no es configurable sin mover la URL del icono. El array vacío de `sameAs` es peor que no emitir la propiedad, y se arregla desde `hugo.toml` con cuidado de la trampa de TOML.

**5. El JSON-LD declara `author` como `Person` con el nombre de la marca.** Lo emite la plantilla del tema, la misma de las 128 líneas. Es incoherente, no es grave, y entra en la misma decisión.

---

## 4. Análisis SEO

### 4.1. El plan ya existía, y está casi entero ejecutado

`docs/seo-arquitectura.md` fija 20 piezas para los cuatro primeros meses. Medido contra el sitio en vivo:

**19 de 20 publicadas.** Los dos bloqueantes del punto 0 (dominio conectado antes del primer contenido indexable, y `params.env` sin fijar) están los dos resueltos.

Falta una, y no es una cualquiera:

| # | URL | Por qué importa, según el propio plan |
|---:|:---|:---|
| 17 | `/etiquetas/como-pedir-la-etiqueta-ambiental/` | Transaccional puro, volumen estable todo el año, verificación trivial (sede de la DGT y Correos), dificultad **baja**. Es la salida natural de las cinco páginas de etiqueta y **la primera pieza que no depende de la política de ZBE**, o sea la que cubre el riesgo de «cambio político» del plan de negocio |

Nota: la pieza 20 del plan era literalmente *«Qué etiquetas prohíbe cada una de las N ZBE de España»*. Es la tabla que se publicó ayer en `/zbe/distintivos-por-ciudad/`, escrita sin haber leído ese plan. Convergencia, no coincidencia: era el siguiente paso evidente.

### 4.2. Dónde se ha desviado el sitio del plan, y si importa

El plan decía: *«No abrir `/impuestos/`, `/itv/`, `/multas/` ni `/trámites/`»* durante los cuatro primeros meses.

Hoy `/multas/` está abierto con un artículo, y `/itv/` tiene **dos páginas publicadas con la sección en borrador**. Eso deja la miga de pan de sus dos páginas muriendo en un «ITV» sin enlace, y deja sin página de entrada a la sección con más demanda de todo el estudio de palabras.

No es grave, pero es una incoherencia: o se cierra la sección, o se le da entrada.

### 4.3. El cuello de botella, dicho con números

| Dato | Valor |
|:---|:---|
| Municipios con ZBE registrada en el NAP | 45 |
| Con ordenanza leída y publicada | **12** |
| Que responden «¿puedo entrar?» | 10 |
| En el dataset abierto, como `confianza: oficial` | 10 |

El estudio de palabras del proyecto da a las ZBE 221.010 búsquedas al mes. Con 12 municipios de 45, se está sirviendo una fracción pequeña de esa demanda, y **ninguna otra palanca compensa eso**: ni el marcado, ni los enlaces internos, ni la velocidad. Todo lo demás del sitio ya está en su sitio.

### 4.4. Orden recomendado para las próximas semanas

1. **Redirección de `www` y `http`.** Minutos, y desbloquea Bing, que es de donde beben dos de los tres motores generativos.
2. **Alta en Bing Webmaster Tools e IndexNow.** Se importa desde Search Console con un clic; IndexNow es un interruptor gratuito en Cloudflare.
3. **Comprobar el bloqueo de rastreadores de IA en Cloudflare.**
4. **Más fichas.** A Coruña, Vitoria-Gasteiz y Oviedo están en cola. Es lo único que mueve la aguja.
5. **La pieza 17**, cuando apetezca un descanso de ordenanzas municipales: es trámite, no normativa local, y se verifica en una tarde.
6. **Decidir qué hacer con `/itv/`**: o se cierra la sección, o se le da página de entrada.

---

## 5. Qué NO hay que hacer

- **No acelerar el ritmo de publicación.** Es la defensa frente a *scaled content abuse*, y es una decisión de diseño.
- **No pasar a respuestas binarias** («Sí, puedes entrar») aunque sea lo que premian los motores generativos. Es lo que hizo que Google AI Mode contradijera la ordenanza de Sevilla el 04/10. Esa regla cuesta citas en las preguntas fáciles y es lo único que deja ganar la difícil.
- **No tocar el marcado esperando citas.** Ya es más rico que el de cualquier competidor medido: `citation` de tipo `Legislation` con nombre y URL del boletín, `lastReviewed`, `about` con `Place`. La palanca es el contenido, no su etiquetado.
- **No añadir `llms.txt` ni marcado de FAQ.** Ningún motor documenta leer el primero, y Google retiró los resultados enriquecidos de FAQ para la mayoría de sitios en 2023.
