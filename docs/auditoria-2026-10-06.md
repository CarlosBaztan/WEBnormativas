# Auditoría de errores y riesgos

**Fecha:** 06/10/2026. **Alcance:** las 47 páginas del build de producción, el pipeline, la herramienta en el navegador y las promesas legales.

Continúa la [auditoría del 05/10](auditoria-2026-10-05.md), que cubría indexación, datos estructurados y SEO. Esta mira otra cosa: **qué puede romperse, y qué se rompe sin avisar**.

---

## 1. El hallazgo que más importa: una contradicción con fecha de caducidad

Varias ordenanzas escalonan las restricciones. Hoy hay siete fechas futuras escritas en las fichas, y dos están cerca:

| Municipio | Qué caduca | Cuándo | Faltan |
|:---|:---|:---|---:|
| **Málaga** | distintivo B | 30/11/2026 | **55 días** |
| **Palma** | distintivo B | 01/01/2027 | **87 días** |
| Oviedo | sin distintivo, anillo exterior | 31/12/2027 | 451 |
| Valladolid | distintivo B | 31/12/2027 | 451 |
| Palma y Valladolid | distintivo C | 01/01/2030 | 1.183 |
| Vitoria-Gasteiz | distintivo B | 01/01/2030 | 1.183 |

Esas fechas las leen **tres cosas distintas, y cada una en un momento distinto**:

| Quién | Cuándo lo evalúa | ¿Se entera solo? |
|:---|:---|:---|
| La herramienta de la portada | En el navegador, con la fecha del día | Sí |
| La tabla comparativa | Al compilar el sitio | **No lo hacía** |
| El texto de la ficha | Nunca: lo escribió una persona | No, y no puede |

**Lo simulé antes de tocar nada.** Poniendo la fecha de Málaga en el pasado, la tabla seguía diciendo «entra hoy: 0, ECO, C y B» y, peor, «el B **deja de entrar** el 30/11/2025»: futuro sobre una fecha pasada. Mientras tanto la portada habría dicho «Ya no». Dos páginas del mismo sitio contradiciéndose, sin que nadie recibiera un aviso.

**Arreglado**: la tabla compara con la fecha del día, saca de «qué entra hoy» los distintivos caducados y cambia el tiempo verbal a «ya no entra desde el». Verificado en los dos sentidos.

**Lo que una plantilla no puede arreglar es la prosa.** La ficha de Málaga dice «Hoy entran 0, ECO, C y B», y eso lo tiene que reescribir una persona. Para que nadie se olvide, `pipeline/test_caducidades.py` falla el día siguiente a cada caducidad y nombra la ficha. Comprobado poniendo una fecha en el pasado.

---

## 2. Una regla del proyecto que se estaba incumpliendo

Un barrido de las 47 páginas encontró **una raya larga publicada**, en la tabla de `/zbe/vitoria-gasteiz/`, usada como celda vacía.

Va contra una regla explícita: ninguna raya en texto de cara al usuario, porque delatan texto generado. Había sobrevivido a tres revisiones porque es un carácter que no se ve leyendo deprisa.

Quitada. Y ahora lo vigila `auditoria.py`, que distingue la raya del guion corto para no quejarse de «Vitoria-Gasteiz» ni de «2001-2006»: una comprobación que da falsos positivos se desactiva el primer día.

---

## 3. Lo que se comprobó y está bien

Esto vale tanto como lo anterior, porque dice dónde no hay que volver a mirar.

| Comprobación | Resultado |
|:---|:---|
| Enlaces internos rotos | **0** en 47 páginas |
| Saltos en la jerarquía de encabezados | **0** |
| Páginas con un `h1` que no sea exactamente uno | **0** |
| Imágenes sin `alt` | **0** |
| Plantillas sin procesar en el texto visible | **0** |
| Errores de JavaScript en consola | **0** en portada, ficha y mapa |
| Rayas largas (tras el arreglo) | **0** |

### La herramienta no adivina

Probado el caso límite: un diésel de 2015 sin mes cae justo entre el distintivo B y el C. La herramienta responde:

> «No podemos afirmar qué distintivo te corresponde. Tu año de matriculación cae justo en el límite entre el distintivo B y el C. Sin el mes no se puede determinar cuál es.»

Y aun así enseña lo que dice la ordenanza del municipio. Es el comportamiento correcto: prefiere no responder antes que acertar por suerte.

### El mapa carga lo que debe

Las páginas con mapa piden `zbe-simplificado.geojson`, **184 KB**, no el fichero completo de 3,2 MB. Leaflet 1.9.4 carga bien, pinta las teselas y dibuja 101 polígonos de zona.

### La promesa legal se sostiene

La página de cookies declara exactamente tres claves de almacenamiento local: `pref-theme`, `menu-scroll-position` y `perfil_vehiculo_v1`. El código usa **esas tres y ninguna más**. Producción no envía ni una cabecera `Set-Cookie`.

---

## 4. Riesgos que quedan, sin arreglar

**Dependencia de cdnjs.** Leaflet se carga desde `cdnjs.cloudflare.com`. Si ese servicio falla, los mapas dejan de funcionar. Es una decisión consciente y con `preconnect`, y el coste de alojarlo nosotros es bajo. No urge, pero conviene saberlo.

**Dos ordenanzas que no se pueden leer.** Los decretos de alcaldía de La Coruña y las directrices del APR de Vitoria no están publicados en abierto. Las dos fichas lo advierten, así que no hay riesgo para el lector, pero hay un hueco de información real.

**Fuentes que cambian bajo nuestros pies.** Pasó con Granada: la URL que citábamos seguía viva pero había dejado de contener lo que citábamos. La auditoría comprueba que las fuentes respondan, no que sigan diciendo lo mismo. **Eso no se puede automatizar**, y es el riesgo de fondo de un sitio cuyo valor es la trazabilidad.

**El ritmo de publicación.** Sigue en pie el aviso del 05/10: la regla del proyecto son 4-6 piezas al mes y se ha ido muy por encima. Está dicho en [pendientes.md](pendientes.md).
