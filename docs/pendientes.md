# Pendientes: lo que te toca a ti y lo que no he podido verificar

Al 05/10/2026. Esta lista recoge también cosas que quedaron en el aire de días anteriores, no solo de hoy.

---

## 0. Un aviso que va primero, porque va contra una regla tuya

**El ritmo de publicación se ha disparado.** `CLAUDE.md` dice:

> **4-6 piezas/mes**, cada una verificada. Publicar 80 páginas de golpe generadas con IA = penalización por *scaled content abuse*. El ritmo lento es una decisión de diseño, no una limitación.

En dos días se han publicado **seis fichas de municipio** (Sevilla, Palma, Alicante, La Coruña, Vitoria-Gasteiz y Oviedo) más la tabla comparativa. Eso es más de lo que la regla fija para un mes entero, en dos días, en un dominio de cinco días de vida.

**A favor:** las seis salen del boletín oficial leído entero, con artículo citado, enlace y fecha. No son contenido generado a escala, que es lo que persigue esa política de Google. El dataset tampoco se infla: crece con lo que una persona ha verificado.

**En contra:** Google no lee tu intención, lee el patrón. Un dominio nuevo que pasa de 37 a 47 URL en cinco días, con seis páginas casi gemelas en estructura, es exactamente la silueta que esa política describe. Y el coste de equivocarse aquí no es perder una posición: es perder la confianza del dominio entero.

**Mi recomendación: parar las fichas unas semanas.** No porque estén mal hechas, sino porque el riesgo es asimétrico. Si quieres seguir publicando, que sea contenido de otra forma: la pieza 17 que falta del plan, el hub de `/itv/`, las tarifas de ITV por comunidad.

Tú decides, y si me dices que siga, sigo. Pero no quería que esto pasara sin que lo supieras.

---

## 1. Lo que solo puedes hacer tú

### En Cloudflare

| | Qué | Por qué importa |
|:---|:---|:---|
| 1 | **Redirección de `www` y de `http` al dominio principal** | Medido: **Bing solo tiene indexada la portada, y por `http://`**. Perplexity y la búsqueda de ChatGPT se apoyan en Bing. Deja de ser higiene y pasa a ser un canal perdido |
| 2 | **Mirar si está activado el bloqueo de rastreadores de IA** | No lo puedo comprobar desde fuera: mis pruebas usan la cadena de identificación y Cloudflare bloquea por firma verificada. Lo activa por defecto en zonas nuevas |
| 3 | **Early Hints** | Gratis, un interruptor. Pasos en `docs/conectar-dominio.md` |
| 4 | **IndexNow** | Interruptor gratuito. Avisa a Bing de cada cambio sin esperar al rastreo |

### En Google y Bing

| | Qué |
|:---|:---|
| 5 | **Search Console: pulsar «Validar corrección»** en el aviso de datos estructurados de Conjuntos de datos. Está arreglado desde el 04/10, pero sin eso Google lo recomprueba cuando le toca |
| 6 | **Alta en Bing Webmaster Tools.** Se importa desde Search Console con un clic |
| 7 | **Solicitar AdSense**, cuando quieras. Ojo al orden: trae cookies de terceros y obliga a poner banner de consentimiento y a reescribir `/legal/cookies/`, que hoy promete por escrito que el sitio no usa ninguna |

### Para que yo pueda ver Search Console

Me pediste que lo revise de aquí en adelante. **Hoy no puedo**: vive en tu cuenta de Google y mi navegador está aislado del tuyo, sin tu sesión. Comprobado: no hay ningún Chrome conectado a esta cuenta.

Dos caminos, y el segundo es más barato:

- **Conectar la extensión Claude en Chrome.** Actúa en tu Chrome real con tus sesiones abiertas, así que podría entrar y leer los informes.
- **Que exportes tú los datos.** Search Console → Rendimiento → Exportar → CSV. Dejas el fichero en la carpeta del proyecto y yo lo analizo y lo comparo con el de la vez anterior. Cero configuración.

**Aviso de expectativas:** la propiedad se creó el 02/10 y el sitio se abrió a los buscadores el 01/10. Ahora mismo hay **9 URL indexadas de 47**, lo cual es normal a los cinco días. Datos de rendimiento con los que hacer algo habrá dentro de dos o tres semanas, y conclusiones sólidas hacia el mes y medio.

### Decisiones tuyas, sin prisa

| | Qué | El precio de cada opción |
|:---|:---|:---|
| 8 | **El logotipo del `Organization`** es el `favicon.ico`, de 48 px, y Google pide 112 px mínimo | O adoptamos 128 líneas del tema y las mantenemos nosotros, o se vive sin logotipo en el panel de conocimiento |
| 9 | **`/itv/` está en borrador** y sus dos páginas cuelgan de una sección sin entrada | O se cierra la sección, o se le escribe un hub de verdad |
| 10 | **Tres claves del front matter que nadie lee**: `fecha_vigor_ordenanza`, `sancion_importe`, `verificado_por` | O se publican de forma legible por máquina, o se borran |
| 11 | **Renombrar la carpeta a `webCocheApto`** | Tuyo desde hace días. El Worker de Cloudflare y el repositorio NO se renombran |

---

## 2. Lo que no he podido verificar

Todo esto está dicho en las propias fichas, para que ningún lector se lleve una idea que no podemos sostener.

| Municipio | Qué falta | Por qué |
|:---|:---|:---|
| **Alicante** | Cuándo acaba la moratoria sin sanciones | La ordenanza la establece (art. 4.3) y **no dice cuánto dura**. No he encontrado publicación oficial que la cierre. La ficha dice la regla y dice que no sabemos si ya multan |
| **La Coruña** | Quién puede ser «vehículo autorizado» | La ordenanza remite a dos decretos de alcaldía (27/03/2017 y 01/06/2018) que **no he leído**. Son la única puerta de entrada a esa ZBE |
| **Vitoria-Gasteiz** | Los límites concretos del APR | Las directrices de funcionamiento se aprueban por decreto de alcaldía y la ordenanza no las contiene |
| **Oviedo** | El número y la fecha del BOPA | Tengo el acuerdo del Pleno (02/12/2025) y el PDF oficial del ayuntamiento, pero no he localizado la referencia del boletín |
| **Granada** | Que su enlace oficial siga vivo | `granada.org` va tras Akamai y devuelve 403 a cualquier comprobación automática, incluso en su portada. **Ábrelo una vez en el navegador y me dices** |
| **Zaragoza** | El horario de la ZBE | Ya constaba: no se pudo confirmar en fuente oficial, y la ficha lo dice |
| **Madrid** | La zona «Madrid ciudad» | Sigue pendiente de verificar: hay que leer el texto consolidado de la Ordenanza de Movilidad Sostenible (art. 21 y disposición transitoria primera). Es la zona con más volumen de búsqueda de las tres |

---

## 3. Lo que sigue en mi lado

1. **Fichas**, si decides seguir: Pamplona, Salamanca y Cartagena están en la cola.
2. **La pieza 17 del plan**: `/etiquetas/como-pedir-la-etiqueta-ambiental/`. Es lo único que falta de las 20 del plan de arquitectura, es transaccional, y no depende de la política de ZBE.
3. **Tarifas de ITV por comunidad autónoma**, que tu plan apuntaba para octubre: mismo patrón que las ZBE, dato público disperso en diecisiete sitios que nadie consolida.
