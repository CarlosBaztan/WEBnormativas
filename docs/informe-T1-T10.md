# Informe de ejecución, tareas T1 a T10

29 de septiembre de 2026. Todo lo que sigue está desplegado en producción.

---

## Resumen

| | Antes | Ahora |
|---|---|---|
| Municipios con respuesta verificada | 1 | **7** |
| Fichas de ZBE publicadas | 5 | **15** |
| Herramientas | 1 | **3** |
| Páginas publicadas | 30 | **42** |
| Tests automáticos | 0 | **33** |

Siete municipios responden en la herramienta y **responden distinto**, que es justo el valor del proyecto: un coche con etiqueta B entra en Granada, Málaga, Valladolid, Zaragoza y Barcelona, no entra en Bilbao, y en Madrid depende de la zona.

---

## Lo que se ha construido

**T1. La geometría de las 45 ZBE.** Los ficheros DATEX2 que el pipeline ya descargaba llevaban 37.708 coordenadas de perímetro y el parser las tiraba. Ahora se publican en dos versiones: 3,2 MB como dato abierto y 175 KB para el navegador. Es el activo diferencial del proyecto: ningún competidor publica los polígonos.

**T2. Auditoría automática.** Dos comprobaciones nuevas y una acción de GitHub que se ejecuta sola los lunes y abre una incidencia si algo falla. Es la red de seguridad para el mayor riesgo del proyecto, que según tu propio plan de negocio no es técnico: es que pasen meses sin tocarlo.

**T3. Flujo de verificación.** Un guion fijo para que las fichas salgan todas iguales, y el contrato entre la plantilla y la validación del build comprobado en los dos sentidos.

**T4 y T5. Nueve municipios verificados.** Madrid ya estaba. Se suman Barcelona, Bilbao, Granada, Málaga, Valencia, Valladolid, Zaragoza y Benidorm.

**T7 y T8. El mapa.** Las 45 zonas sobre un mapa, coloreadas según el nivel de verificación, y el perímetro de cada municipio dentro de su propia ficha.

**T9. La ITV.** Herramienta de periodicidad con la tabla del artículo 6.1 del RD 920/2017, y la página sobre la pegatina obligatoria, que era la mejor oportunidad individual del estudio de palabras clave.

**T10. «¿Está mi calle dentro de una ZBE?».** Escribes una dirección y se cruza con los 45 perímetros. Sustituye a la calculadora del IVTM, que el estudio de palabras clave tumbó.

---

## Los hallazgos, que es lo que importa

### La ZBE de Valencia no está en vigor

Leí las 23 páginas de la ordenanza y después comprobé su estado en **dos páginas oficiales del ayuntamiento**. Las dos dicen lo mismo: aprobada solo inicialmente el 25 de febrero de 2025, en exposición pública, «estando pendiente el acuerdo plenario de aprobación definitiva».

Sin aprobación definitiva no hay ordenanza en vigor, y sin ordenanza en vigor no hay multa posible. Media prensa lleva meses dando por hecho que arrancó en diciembre de 2025.

De paso saqué dos cosas que casi nadie cuenta: el texto solo afectaría a vehículos **sin distintivo**, y solo a **turismos, ciclomotores y motocicletas**, porque el artículo 3.4 exige tres requisitos a la vez y una furgoneta no encaja en el primero.

### A los vehículos con etiqueta B en Málaga les quedan dos meses

La ZBE de Málaga se escalona año a año. El 30 de noviembre de 2026 empieza el tercer año y el distintivo B queda restringido, salvo que el vehículo esté domiciliado en Málaga antes de esa fecha.

Es el dato más accionable de todo el fin de semana.

### Granada usa un criterio que no usa nadie más

No es el empadronamiento del conductor ni la residencia en la zona: es **dónde tributa el vehículo**. Un coche sin distintivo que pague el impuesto en Granada entra igual. En la práctica, la ZBE de Granada afecta sobre todo a quien viene de fuera.

### Alicante publica sus coordenadas en dos sistemas a la vez

26 de sus 47 puntos vienen en UTM, en metros, y el resto en grados, dentro del mismo elemento del mismo fichero, sin que el XML declare cuál es cuál.

No los he convertido. Adivinar la proyección dibujaría la zona en otro sitio de Alicante, y eso es peor que no dibujarla. El anillo afectado se descarta y queda registrado dentro del propio fichero que publicamos.

### El distintivo B de Bilbao tuvo un año de moratoria

Cuando la ZBE arrancó en junio de 2024 los B podían entrar. Desde el 15 de junio de 2025 no. Si alguien con un B lleva tiempo sin conducir por Bilbao, ese es el cambio que le afecta y no se lo ha contado nadie.

---

## Los fallos

### Míos, corregidos

**Me inventé los hashes de integridad de Leaflet.** Los puse de memoria, eran falsos, el navegador bloqueó el script y el mapa no cargaba. Ahora están calculados sobre los ficheros reales del CDN, con el comando anotado en la plantilla para cuando se cambie de versión.

**Introduje una regresión en la página más importante del sitio.** Al separar «no verificado» de «no está en vigor» usé la condición `estado_zbe != activa`. Madrid no declaraba ese campo, así que sus tres zonas activas pasaron a mostrar «No consta una zona de bajas emisiones en vigor». La cacé al verificar, no al escribir. Un campo ausente es un dato que falta, no una afirmación.

**Escribí «Cada dos anos» sin tilde** en el JSON de la ITV, que en español significa algo muy distinto.

**El identificador del BOE del decreto de la ITV que tenía era el equivocado.** Me devolvió un real decreto sobre la Junta Electoral Central. Lo verifiqué antes de usarlo.

### Trampas del entorno

**Una ficha creada de madrugada no se publica.** Granada y Barcelona se escribieron a las 00:04 y Hugo no las generó: interpreta un `date` sin hora como medianoche UTC, que en España son las 02:00, así que la fecha quedaba en el futuro y `buildFuture = false` las descartaba **en silencio**, con el build en verde. Resuelto con `timeZone = "Europe/Madrid"`.

Lo peligroso de ese fallo no es el fallo: es que no avisa.

**La herramienta no habría respondido por ninguna ficha nueva.** Solo leía municipios con el campo `zonas`, que usa Madrid por tener tres zonas distintas. Bilbao y las demás usan los campos planos, que es lo que genera la propia plantilla del proyecto. Una ficha perfectamente verificada habría hecho que la herramienta dijera «no consta ninguna zona verificada».

### Defectos del plan que escribí el jueves

Tres tareas estaban mal especificadas: el aviso de caducidad de la T2 ya estaba implementado, el archetype de la T3 ya existía, y a ese archetype le faltaba `codigo_ine`, que es un campo que el propio build exige. Una ficha creada de la plantilla y publicada rompía el build por un campo que la plantilla no ofrecía.

---

## Una decisión de diseño que no estaba prevista

El proyecto no tenía forma de publicar un nivel C.

`CLAUDE.md` dice desde el principio que un nivel C se publica: ficha con las reglas sin verificar más el enlace oficial, sin responder «¿puedo entrar?». Pero `estado_dato: pendiente` obliga a `draft: true`, así que la ficha no salía y el trabajo de comprobar que una ZBE existe se perdía entero.

Me lo encontré de frente con Benidorm: su ZBE opera desde enero de 2025, eso consta, pero ni la página municipal ni el portal de gestión publican de forma legible qué distintivos quedan restringidos. Hay resúmenes de terceros que lo dicen; no los doy por buenos.

He añadido un tercer estado, `parcial`, que publica la ficha, dice lo que consta y lo que no, y **no** entra en el selector de la herramienta. Es el mecanismo que permite crecer honestamente a los 37 municipios que faltan, en vez de perderlos.

---

## Lo que falta

**Pendiente tuyo, y bloquea poco:**

- El dominio. Nada de lo hecho depende de él.
- Tus datos de identidad para las páginas legales. Bloquea AdSense, no el contenido.

**Pendiente mío:** de la T11 en adelante, con el Reality Checker de la T6 todavía en marcha sobre las nueve fichas.

**Y una cosa que conviene mirar:** la ficha de Málaga tiene fecha de caducidad real. El 30 de noviembre de 2026 cambia lo que dice, y falta poco.
