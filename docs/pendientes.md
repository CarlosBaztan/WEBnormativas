# Pendientes: lo que te toca a ti y lo que no he podido verificar

Actualizado el **07/10/2026**. La lista crece: lo que se resuelve se tacha y se
deja a la vista, para no volver a abrirlo. Lo nuevo de hoy va marcado así:
**(nuevo 07/10)**.

---

## 0. Un aviso que va primero, porque va contra una regla tuya

**El ritmo de publicación se ha disparado.** `CLAUDE.md` dice:

> **4-6 piezas/mes**, cada una verificada. Publicar 80 páginas de golpe generadas con IA = penalización por *scaled content abuse*. El ritmo lento es una decisión de diseño, no una limitación.

En tres días se han publicado **siete fichas de municipio** (Sevilla, Palma,
Alicante, La Coruña, Vitoria-Gasteiz, Oviedo y Pamplona), la tabla comparativa
y la pieza de la etiqueta ambiental. Eso es el doble de lo que la regla fija
para un mes entero, en tres días, en un dominio de una semana de vida.

**A favor:** las siete salen del boletín oficial leído entero, con artículo
citado, enlace y fecha. No son contenido generado a escala, que es lo que
persigue esa política de Google. El dataset tampoco se infla: crece con lo que
una persona ha verificado.

**En contra:** Google no lee tu intención, lee el patrón. Un dominio nuevo que
pasa de 37 a 46 URL en seis días, con siete páginas casi gemelas en estructura,
es exactamente la silueta que esa política describe. Y el coste de equivocarse
aquí no es perder una posición: es perder la confianza del dominio entero.

**Mi recomendación sigue siendo parar las fichas unas semanas.** No porque
estén mal hechas, sino porque el riesgo es asimétrico. **(nuevo 07/10)** Los
dos últimos días no he publicado ninguna ficha nueva: el trabajo ha ido a
arreglar lo ya publicado, que no suma URL y sí suma calidad.

Tú decides, y si me dices que siga, sigo.

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

Me pediste que lo revise de aquí en adelante. **Sigo sin poder**: vive en tu
cuenta de Google y mi navegador está aislado del tuyo, sin tu sesión.

Dos caminos, y el segundo es más barato:

- **Conectar la extensión Claude en Chrome.** Actúa en tu Chrome real con tus
  sesiones abiertas, así que podría entrar y leer los informes.
- **Que exportes tú los datos.** Search Console → Rendimiento → Exportar → CSV.
  Dejas el fichero en la carpeta del proyecto y yo lo analizo y lo comparo con
  el de la vez anterior. Cero configuración.

**Aviso de expectativas:** la propiedad se creó el 02/10 y el sitio se abrió a
los buscadores el 01/10. Datos de rendimiento con los que hacer algo habrá
dentro de dos o tres semanas, y conclusiones sólidas hacia el mes y medio.

### Decisiones tuyas, sin prisa

| | Qué | El precio de cada opción |
|:---|:---|:---|
| 8 | **El logotipo del `Organization`** es el `favicon.ico`, de 48 px, y Google pide 112 px mínimo | O adoptamos 128 líneas del tema y las mantenemos nosotros, o se vive sin logotipo en el panel de conocimiento |
| 9 | **`/itv/` está en borrador** y sus dos páginas cuelgan de una sección sin entrada | O se cierra la sección, o se le escribe un hub de verdad |
| 10 | **Tres claves del front matter que nadie lee**: `fecha_vigor_ordenanza`, `sancion_importe`, `verificado_por` | O se publican de forma legible por máquina, o se borran |
| 11 | **Renombrar la carpeta a `webCocheApto`** | Tuyo desde hace días. El Worker de Cloudflare y el repositorio NO se renombran |
| 12 | **(nuevo 07/10) Los títulos son demasiado largos para la caja de Google** | Ver abajo. Es la decisión con más efecto en tráfico de toda esta lista |

#### 12. Los títulos, con los números delante

Google pinta el título del resultado en una caja de unos **600 px**. Medidos
los 46 con la tipografía que usa:

| | |
|:---|---:|
| Títulos que se pasan de 600 px | **30 de 46** |
| El peor, antes de tocarlo (Valencia) | 964 px |
| Lo que ocupa el sufijo «\| Coche Apto» | ~115 px |
| Lo que ocupa «Zona de Bajas Emisiones (ZBE) de » | ~302 px |

O sea que en una ficha de municipio **la mitad de la caja se va antes de
nombrar la ciudad**, y lo que se corta es justo el final, que es donde está lo
que diferencia una ficha de otra («qué distintivos pueden entrar»).

Las dos causas son decisiones tomadas, y por eso no las toco yo:

- La **convención de títulos** de `CLAUDE.md`: las dos formas, «Zona de Bajas
  Emisiones (ZBE) de Valencia». Se tomó para no perder ninguna de las dos
  búsquedas, y el motivo sigue en pie.
- El **sufijo de marca**, que puse el 01/10 al cambiar `site.Title`.

Tres salidas, de menos a más invasiva:

1. **Quitar el sufijo «| Coche Apto»** de las páginas que no son la portada.
   Recupera 115 px de golpe en las 46. Google ya muestra el nombre del sitio
   por su cuenta encima del título, así que se duplica. Es un cambio de una
   línea en `layouts/partials/head.html`.
2. **Acortar la fórmula** a «ZBE de Valencia: Zona de Bajas Emisiones y qué
   distintivos entran». Mantiene las dos formas pero pone la sigla delante,
   que es lo contrario de lo que decidiste.
3. **Dejarlo como está** y asumir que Google recorta. No es una penalización:
   es que el visitante ve menos razones para pulsar.

Yo haría la 1. Pero es tu marca y la pusiste hace seis días.

---

## 2. Lo que no he podido verificar

Todo esto está dicho en las propias fichas, para que ningún lector se lleve una idea que no podemos sostener.

| Municipio | Qué falta | Por qué |
|:---|:---|:---|
| **La Coruña** | Quién puede ser «vehículo autorizado» | La ordenanza remite a dos decretos de alcaldía (27/03/2017 y 01/06/2018). **Buscados el 06/10/2026 y no están publicados en abierto** ni en coruna.gal ni en el BOP. Son la única puerta de entrada a esa ZBE, así que o se piden al Concello o esto se queda sin publicar |
| **Vitoria-Gasteiz** | Si el APR ya está en vigor | La ordenanza eximía a las categorías del APR de la etiqueta y de las sanciones **hasta el 15/09/2026**, fecha ya pasada, pero las directrices se aprueban por decreto de alcaldía y **no lo he localizado publicado**. Si lo está, en el casco medieval no basta con tener etiqueta. La ficha lo advierte |
| **Pamplona** | Los horarios del Casco Antiguo | **(nuevo 07/10)** La ordenanza de la ZBE no fija franja horaria: quien la fija son las Normas de Acceso al Casco Antiguo, de 2017. La página municipal que las recoge no está disponible, así que la ficha dice que existen y dónde se tramitan, y no las reproduce |
| **Granada** | Que su enlace oficial siga vivo | `granada.org` va tras Akamai y devuelve 403 a cualquier comprobación automática, incluso en su portada. **Ábrelo una vez en el navegador y me dices** |
| ~~**Alicante**~~ | ~~Cuándo acaba la moratoria~~ | **RESUELTO el 06/10/2026**, y de paso corregido un error nuestro: no hay restricción por etiqueta, así que la moratoria es irrelevante |
| ~~**Oviedo**~~ | ~~El número y la fecha del BOPA~~ | **RESUELTO el 06/10/2026**: BOPA núm. 243, de 18 de diciembre de 2025 |
| ~~**Zaragoza**~~ | ~~El horario de la ZBE~~ | **RESUELTO el 06/10/2026**: de lunes a viernes de 8:00 a 20:00 |
| ~~**Madrid**~~ | ~~La zona «Madrid ciudad»~~ | **RESUELTO el 06/10/2026**: art. 21 y disposición transitoria séptima de la Ordenanza 2/2026 |

---

## 2 bis. La revisión que me puse a mí mismo, cerrada

El error de Alicante abrió una pregunta incómoda: **¿estaba el mismo fallo en
otras fichas?** Releídos los textos oficiales uno a uno el 06/10/2026:
**Sevilla, Palma, Oviedo, Barcelona, Bilbao, Valladolid, Málaga y Granada
quedan confirmadas.** El error era único de Alicante y está corregido, con la
explicación escrita en la propia página.

---

## 3. Lo que sigue en mi lado

1. **Fichas**, si decides seguir: Salamanca, Cartagena y Alcalá de Henares
   están en la cola. Pamplona ya está publicada.
2. ~~**La pieza 17 del plan**: `/etiquetas/como-pedir-la-etiqueta-ambiental/`~~
   **HECHA el 06/10/2026.** Con ella, las 20 piezas del plan de arquitectura
   están completas.
3. **Tarifas de ITV por comunidad autónoma**, que tu plan apuntaba para
   octubre: mismo patrón que las ZBE, dato público disperso en diecisiete
   sitios que nadie consolida. **No suma una ficha más de municipio**, así que
   no agrava el aviso del punto 0.
4. **(nuevo 07/10) Limpiar `herramienta.css`.** `.pc-campo`, `.pc-campo label`
   y `.pc-boton` están declarados **dos veces** en el mismo fichero, a 600
   líneas de distancia: una vez con valores a pelo y otra con los tokens del
   sistema. Gana el segundo por orden de aparición, así que hoy funciona, pero
   es exactamente la forma de las trampas de `CLAUDE.md`. No urge y no lo he
   tocado hoy para no mezclarlo con el repaso de diseño.
5. **(nuevo 07/10) El resto del repaso de redacción.** Queda releer las
   entradillas de las fichas más antiguas: nueve de quince abren con un
   superlativo o con una promesa, y eso se nota al leerlas seguidas.

---

## 4. (nuevo 07/10) Lo que he arreglado estos dos días, para que no lo busques

No hace falta que hagas nada con esto. Está aquí para que sepas qué cambió por
si algo se ve distinto.

### Lo más serio: tres fichas se desmentían a sí mismas

**Alicante, La Coruña y Pamplona** publicaban, encima de su propio artículo,
el aviso «Las reglas de acceso de esta ZBE no están verificadas… todavía no
hemos contrastado artículo por artículo qué distintivos ambientales pueden
circular». Las tres tienen la ordenanza leída por artículos y por boletín. Y
su tabla de datos lo repetía: «Sin verificar».

El motivo es el modelo de las ZBE donde la etiqueta no abre la puerta: ahí la
lista de distintivos está vacía **a propósito**, y la plantilla lo leía como
un hueco. `auditoria.py` ya lo entendía bien desde el 05/10; la plantilla no.

Lo vigila ahora `pipeline/test_paginas_publicadas.py`, que es de un tipo nuevo:
**compila el sitio y lee el HTML que sale**. Es la única forma de responder a
«¿esta página dice de sí misma algo que no es verdad?», que ya ha fallado
cuatro veces y las cuatro con el build en verde.

### La tabla que es el argumento del sitio desbordaba la pantalla

`/zbe/distintivos-por-ciudad/` no llevaba envoltorio: a 375 px la tabla medía
420 y **empujaba la página entera a 434**. No se desplazaba la tabla, se
desplazaba todo: el titular, los párrafos y el pie se iban hacia la derecha.
La del listado de `/zbe/` sí se desplazaba, pero no se podía enfocar con el
teclado. Las tres tablas del sitio usan ya el mismo envoltorio.

### Zonas táctiles

76 enlaces y controles por debajo de 40 px de alto repartidos por las 46
páginas, incluidas las 35 filas del panel de secciones, que en móvil es la
única navegación que hay. Ahora **cero**, y cero desbordes horizontales en las
46 páginas.

### La cabecera

- Un `line-height: 60px` del tema se heredaba a todo: la lupa medía 74 px de
  alto dentro de una cabecera de 61 y sobresalía por los dos lados.
- `.header-nav a { display: block }` del tema ganaba a nuestro `inline-flex`,
  así que el centrado de los iconos **nunca se aplicó**: la lupa se pintaba a
  once píxeles y medio del centro de su círculo.
- El menú de secciones pasa a la izquierda, pegado a la marca, y la cabecera
  comparte ya la retícula de la página.
- **Botón nuevo: «¿Puedo circular?».** La cabecera tenía tres enlaces de
  sección, una lupa y el botón de tema, y ninguno era lo que el sitio hace.

### Longitud de línea

A 1920 px el texto corrido salía a 164 caracteres por línea, el doble de lo
recomendable. Nuevo tope de 86ch que **deja 1366 exactamente como estaba** y
baja 1920 a 96. Si algún día quieres apretar hasta el rango de manual, se
cambia `--medida` en `sistema.css` a `75ch` y afecta a todo el sitio.

### Contraste

Repasadas las 46 páginas en los dos temas: **cero incidencias**.
