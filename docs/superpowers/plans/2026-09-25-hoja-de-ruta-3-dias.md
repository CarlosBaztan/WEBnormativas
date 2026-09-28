# Hoja de ruta 25–27 de septiembre de 2026

> **Para quien ejecute esto:** las tareas están en orden de dependencia. Cada
> una termina en un estado desplegable y con su propio commit. Los pasos usan
> casillas (`- [ ]`) para ir marcándolos.

**Objetivo:** pasar de un sitio con una sola ciudad verificada y una
herramienta a un portal con mapa propio de las ZBE de España, tres
herramientas, entre ocho y doce municipios verificados y el expediente de
AdSense listo para enviar.

**Enfoque:** el fin de semana se dedica a lo que crea foso competitivo —el
dato verificado y la geometría que nadie más ha publicado— y no a producir
páginas. La parte de código existe para explotar ese dato.

**Stack:** Hugo 0.166 extendido · PaperMod · JavaScript sin framework ·
Python 3.12 para el pipeline · Cloudflare Workers · Leaflet 1.9 (solo en las
páginas con mapa).

**Documentos de referencia:** [CLAUDE.md](../../../CLAUDE.md) ·
[PLAN-NEGOCIO.md](../../../PLAN-NEGOCIO.md) ·
[docs/seo-arquitectura.md](../../seo-arquitectura.md)

---

## Antes de empezar: una tensión que hay que resolver

`CLAUDE.md` fija un ritmo de **4-6 piezas al mes** y explica por qué: publicar
muchas páginas de golpe es el patrón que Google penaliza como *scaled content
abuse*. Este plan propone entre 8 y 12 fichas en tres días. Es una
contradicción y conviene mirarla de frente.

Por qué creo que aquí no aplica la penalización:

1. **El sitio está en `noindex` y con `robots.txt` bloqueando todo.** Nada de
   lo que se publique este fin de semana llega a Google. Se está montando el
   corpus en privado, no publicando.
2. **Lo que se penaliza es el contenido generado sin valor propio.** Una ficha
   con el artículo de la ordenanza citado, su boletín y su fecha de
   verificación es justo lo contrario, y se distingue por tener datos que no
   están en ningún otro sitio.
3. **El ritmo lento importa cuando el sitio ya es visible.** Esa regla vuelve a
   estar en vigor el día que se conecte el dominio y se quite el `noindex`.

**Decisión que propongo, y que conviene que confirmes:** se construye todo
ahora con el sitio invisible; el `noindex` no se toca hasta que el dominio
propio esté conectado. Si prefieres mantener el ritmo lento incluso en
privado, dímelo y recorto a 4 municipios y dedico el tiempo sobrante a
herramientas.

---

## Lo que necesito de ti

| Qué | Para qué | Bloquea |
|---|---|---|
| **Nombre, NIF, domicilio y email de contacto** | El art. 10 LSSI obliga a identificar al titular del sitio. AdSense no aprueba un sitio sin aviso legal real. | T13 y todo el expediente de AdSense |
| **Decisión de dominio** | Migrar antes de que nadie enlace nada. | Quitar el `noindex`, no este fin de semana |
| **PDF de alguna ordenanza concreta** | Algunos ayuntamientos publican solo en el boletín provincial, y a veces detrás de un visor que no puedo leer. | Se sabrá sobre la marcha (ver T4/T5) |

No inventaré datos de identidad ni publicaré tu correo por iniciativa propia.
Mientras no lleguen, las páginas legales se quedan como están, con los huecos
marcados en comentarios HTML.

**Sobre las ordenanzas:** he comprobado que sí puedo leerlas. La de Zaragoza
está entera en la web del ayuntamiento (normativa, vehículos autorizados,
mapa de fases y preguntas frecuentes). Trabajaré así con todas y **te pediré
solo las que se me atraganten**, con el enlace exacto que he intentado y qué
me ha fallado. No te voy a pedir documentos por adelantado «por si acaso».

---

## Restricciones que se aplican a todas las tareas

Salen de `CLAUDE.md` y no se negocian dentro de este plan:

- **Nunca una respuesta binaria por cuenta propia.** No «✅ puedes entrar»,
  sino «la ordenanza X, art. Y, permite… [enlace]. Verificado el DD/MM/AAAA».
- **Niveles de confianza A/B/C/D. Nunca se publica por encima del nivel que se
  tiene.** Nivel C (solo consta que hay ZBE) es ficha sin reglas y con enlace
  oficial; nivel D es no publicar página.
- **Cada dato lleva fuente, enlace y fecha de verificación visibles.**
- **Las reglas de acceso no se derivan del NAP-DGT.** El hallazgo del 22/09
  sigue en pie: cada ayuntamiento codifica el `negate` al revés del vecino.
  Del NAP se usa la existencia de la zona, la fuente oficial, el horario y
  —a partir de este plan— la geometría. Nunca los distintivos.
- **Solo fuentes oficiales y abiertas.** Se respeta `robots.txt`. No se
  scrapea a competidores.
- **La DGT se cita.** El NAP es CC-BY: la atribución es obligatoria en cada
  página que use sus datos, mapa incluido.
- **`noindex = true` no se toca en todo el fin de semana.**
- **Cero anuncios encima de un formulario.** Solo debajo del resultado o al
  final de un artículo (regla dura 4, ya la hace cumplir
  `partials/anuncio.html`).
- **Ningún agente redacta contenido normativo.** El dato sale del BOE, del
  boletín correspondiente o de la web del organismo. Un agente puede
  estructurar, revisar o contrastar; no puede ser el origen del dato.

---

## Dónde suele romperse esto

Cinco cosas que ninguna tarea prueba por sí sola y que son las que más
probablemente le estallen a un usuario real. Cada una tiene su comprobación
asignada dentro de la tarea que la causa.

1. **Coordenadas invertidas.** DATEX2 da `latitude`/`longitude` por separado;
   GeoJSON los quiere como `[lon, lat]`. Si se copian en el orden que vienen,
   las ZBE españolas aparecen en Somalia. → Comprobación en T1.
2. **Una ordenanza que cambia y una ficha que no.** Una ficha verificada hoy
   miente dentro de seis meses y nadie se entera. → Comprobación en T2.
3. **El mapa en un móvil con datos.** 50 polígonos con decenas de miles de
   puntos son megas de GeoJSON y un bloqueo del hilo principal. → T7.
4. **`localStorage` bloqueado o lleno.** En navegación privada lanza
   excepción. Si no está envuelto, la herramienta entera deja de responder al
   pulsar «Consultar». → T9.
5. **Una dirección ambigua.** «Calle Mayor» existe en cientos de municipios:
   si el geocodificador la resuelve en el que no es, la herramienta afirmará
   que estás dentro de una ZBE que no es la tuya. Tiene que mostrar siempre
   qué dirección ha entendido y pedir que se confirme antes de responder.
   → T10.

---

# DÍA 1 — Viernes 25: el dato

El producto es el dataset. Todo lo del sábado depende de lo que salga hoy.

---

### T1 · Extraer la geometría del NAP y publicarla como GeoJSON

**Agente:** Data Engineer (dispatch en segundo plano mientras yo sigo con T3).

**Contexto:** los 50 XML ya descargados en `pipeline/estado/cache/` contienen
76.676 coordenadas dentro de `<loc:openlrPolygonCorners>`. El parser actual
las descarta. Es el activo más valioso que tenemos sin explotar: ningún
competidor publica los polígonos.

**Ficheros:**
- Crear: `pipeline/zbe_geometria.py`
- Crear: `static/datos/zbe.geojson` (completo, para descarga)
- Crear: `static/datos/zbe-simplificado.geojson` (para el mapa)
- Modificar: `pipeline/auditoria.py` (comprobación nueva, ver pasos)

**Interfaz que produce:** un `FeatureCollection` donde cada `Feature` tiene
`properties.slug`, `properties.municipio`, `properties.provincia`,
`properties.url_ficha`, `properties.fuente_url`, `properties.fecha_descarga`
y `properties.estado_dato`. El mapa de T7 y las fichas de T8 consumen esto.

- [ ] **Paso 1.** Leer `pipeline/zbe_nap.py` entero antes de tocar nada. El
      nuevo script reutiliza su mapa `CORRECCIONES_NOMBRE` y su forma de
      derivar el slug: si los slugs no coinciden, el mapa no enlaza con las
      fichas.
- [ ] **Paso 2.** Escribir `pipeline/zbe_geometria.py` con el namespace
      correcto. El XML usa prefijos: hay que registrar el namespace de
      `loc:` en lugar de buscar `<latitude>` a pelo, que no aparece.
- [ ] **Paso 3.** Escribir la comprobación de cordura ANTES de generar nada.
      España cabe entera en un rectángulo; cualquier punto fuera es un bug de
      orden de coordenadas:

```python
# España peninsular + islas + Ceuta y Melilla, con margen.
LIMITES = {"lat": (27.0, 44.0), "lon": (-19.0, 5.0)}

def verificar_punto(lat, lon, contexto):
    """Un punto fuera de España casi siempre significa lat/lon invertidos."""
    if not (LIMITES["lat"][0] <= lat <= LIMITES["lat"][1]):
        raise ValueError(f"{contexto}: latitud {lat} fuera de España. "
                         f"¿Has intercambiado latitud y longitud?")
    if not (LIMITES["lon"][0] <= lon <= LIMITES["lon"][1]):
        raise ValueError(f"{contexto}: longitud {lon} fuera de España.")
```

- [ ] **Paso 4.** Ejecutarlo a propósito con las coordenadas cambiadas de
      orden y confirmar que revienta con ese mensaje. Una comprobación que no
      se ha visto fallar no es una comprobación.
- [ ] **Paso 5.** Generar el GeoJSON de verdad. En GeoJSON el orden es
      `[longitud, latitud]`, al revés de como se lee en voz alta.
- [ ] **Paso 6.** Generar la versión simplificada con el algoritmo de
      Ramer–Douglas–Peucker, implementado a mano (no añadimos dependencias
      por esto). Objetivo: **el fichero simplificado por debajo de 250 KB**.
- [ ] **Paso 7.** Comprobar el resultado:

```bash
python pipeline/zbe_geometria.py
python -c "import json;d=json.load(open('static/datos/zbe.geojson',encoding='utf-8'));print(len(d['features']),'zonas')"
ls -l static/datos/zbe-simplificado.geojson
```

Esperado: 45 o más zonas, y el simplificado por debajo de 250 KB.

- [ ] **Paso 8.** Abrir el GeoJSON en geojson.io y mirarlo con los ojos. Que
      valide no significa que la forma sea la correcta: Madrid tiene que
      parecerse a la M-30.
- [ ] **Paso 9.** Añadir a `pipeline/auditoria.py` una comprobación que falle
      si un municipio con ficha publicada no tiene geometría, o al revés.
- [ ] **Paso 10.** Commit.

```bash
git add pipeline/zbe_geometria.py pipeline/auditoria.py static/datos/
git commit -m "Extrae la geometria del NAP y la publica como GeoJSON"
```

---

### T2 · Que el sitio avise solo cuando un dato caduca

**Agente:** ninguno. Es una hora de trabajo mío.

**Contexto:** `CLAUDE.md` dice que los datos sin revisar «se marcan solos como
pendientes de verificación». Ahora mismo `auditoria.py` lo detecta pero hay
que acordarse de ejecutarlo, y el aviso no llega al lector.

**Ficheros:**
- Modificar: `pipeline/auditoria.py`
- Modificar: `layouts/partials/fuente-verificacion.html`
- Crear: `.github/workflows/auditoria.yml`

- [ ] **Paso 1.** En `fuente-verificacion.html`, calcular la antigüedad de
      `fecha_verificacion` con `time.Now.Sub`. Por encima de 180 días, pintar
      un aviso visible: «Este dato se verificó hace más de seis meses.
      Compruébalo en la fuente antes de fiarte».
- [ ] **Paso 2.** Comprobarlo poniendo a mano una fecha de 2024 en una ficha,
      viendo el aviso, y devolviéndola a su valor.
- [ ] **Paso 3.** Añadir a `auditoria.py` dos comprobaciones nuevas: que todo
      `fuente_url` de una ficha publicada responde 200, y que ninguna ficha
      publicada tiene `etiquetas_permitidas` vacío.
- [ ] **Paso 4.** Crear la acción de GitHub que ejecuta `auditoria.py` todos
      los lunes y abre una incidencia si falla. Es la red de seguridad para
      cuando pasen semanas sin tocar el proyecto —que según el plan de
      negocio es el riesgo número uno.
- [ ] **Paso 5.** `python pipeline/auditoria.py` y `hugo --gc --minify`, los
      dos en verde.
- [ ] **Paso 6.** Commit.

---

### T3 · Flujo de verificación de una ordenanza

**Agente:** ninguno para el flujo. Content Creator redactará después sobre
esta plantilla.

**Contexto:** verificar ocho municipios a mano sin un guion fijo garantiza que
cada ficha salga distinta y que alguna se publique con un hueco. Esto es lo
que convierte T4 y T5 en trabajo mecánico.

**Ficheros:**
- Crear: `archetypes/zbe.md`
- Crear: `docs/verificacion-ordenanzas.md`

- [ ] **Paso 1.** Escribir el archetype con todos los campos obligatorios ya
      presentes y vacíos, de modo que la validación de `layouts/index.html`
      salte si se publica incompleto.
- [ ] **Paso 2.** Escribir el guion de verificación, con los seis datos que
      hay que sacar de cada ordenanza: distintivos que pueden acceder,
      horario, perímetro, excepciones, artículo exacto y boletín con fecha.
- [ ] **Paso 3.** Incluir en el guion la regla de parada: **si un dato no
      aparece literalmente en el texto oficial, no se publica.** Ante la duda,
      la ficha se queda en nivel C con su enlace.
- [ ] **Paso 4.** Pasar la ficha de Madrid por el guion como prueba: debe
      salir idéntica a lo que ya está publicado.
- [ ] **Paso 5.** Commit.

---

### T4 · Cuatro municipios verificados: Valencia, Bilbao, Granada, Barcelona

**Agentes:** yo leo las fuentes y extraigo los datos. Content Creator redacta
el cuerpo a partir de los datos ya extraídos. Reality Checker revisa al final
(T6). **Ningún agente toca la fuente.**

**Contexto:** el orden sale de los datos de Semrush del 28/09/2026, no de
una intuición. Valencia tiene la mejor relación de todo el conjunto (3.600
búsquedas con dificultad 16), seguida de Bilbao (4.400 con 21) y Granada
(4.400 con 25). Barcelona es más difícil (6.600 con 39) pero entra en el
primer grupo por una razón distinta: su CPC es de 4,12 $ frente a 0,00 $ de
Bilbao. Es el único municipio donde el tráfico de ZBE tiene valor
publicitario real.

Zaragoza y Sevilla salen de este bloque: no aparecen entre las diez primeras
por volumen. Zaragoza se mantiene como candidata porque ya hay una ficha de
ejemplo en `content/zbe/zaragoza.md` y porque es donde vive Carlos, así que
puede contrastar el resultado con lo que ve en la calle.

**Ficheros:**
- Modificar: `content/zbe/zaragoza.md` (pasa de ejemplo a ficha real)
- Crear: `content/zbe/barcelona.md`, `content/zbe/valencia.md`,
  `content/zbe/sevilla.md`
- Modificar: `data/cobertura.json`, `data/zbe_destacados.json`

- [ ] **Paso 1.** Zaragoza. Fuentes localizadas y comprobadas:
      la [ordenanza municipal de ZBE](https://www.zaragoza.es/sede/servicio/normativa/13277),
      los [vehículos autorizados](https://www.zaragoza.es/sede/portal/movilidad/bajas-emisiones/vehiculos)
      y el [mapa y fases de implantación](https://www.zaragoza.es/sede/portal/movilidad/bajas-emisiones/mapa-fases).
      Extraer los seis datos del guion de T3.
- [ ] **Paso 2.** Rellenar el front matter de `zaragoza.md`, quitar
      `draft: true` y el comentario de «ficha de ejemplo».
- [ ] **Paso 3.** `hugo --gc --minify`. La validación de `layouts/index.html`
      rompe el build si falta `codigo_ine`, `fuente_url` o
      `fecha_verificacion`. Que compile es la prueba de que la ficha está
      completa.
- [ ] **Paso 4.** Abrir la herramienta en el navegador, elegir Zaragoza con un
      vehículo de cada distintivo y comprobar que los cinco veredictos
      coinciden con lo que dice la ordenanza. **Esto no se delega.**
- [ ] **Paso 5.** Repetir pasos 1-4 con Barcelona. Ojo: en el NAP figura como
      «Rondas de Barcelona» y la ZBE Rondas incluye municipios del área
      metropolitana, no solo Barcelona ciudad. Si la ordenanza es del AMB y no
      del ayuntamiento, la ficha lo tiene que decir.
- [ ] **Paso 6.** Repetir con Valencia.
- [ ] **Paso 7.** Repetir con Sevilla. En el NAP consta solo «Sevilla
      (Cartuja)»: si la ordenanza cubre más zonas, la ficha usa el esquema por
      zonas de Madrid; si no, se publica solo Cartuja y se dice.
- [ ] **Paso 8.** Actualizar `cobertura.json` («Por ahora solo Madrid está
      verificada» deja de ser cierto) y `zbe_destacados.json`.
- [ ] **Paso 9.** Si alguna fuente no se deja leer, **parar con esa y seguir
      con la siguiente**. Anotarla en `docs/verificacion-ordenanzas.md` con la
      URL intentada y el error, para pedírtela junta al final del día.
- [ ] **Paso 10.** `python pipeline/auditoria.py` en verde. Commit, uno por
      municipio.

---

### T5 · Cuatro municipios más: Málaga, Valladolid, Benidorm, Zaragoza

**Agentes:** los mismos que T4.

**Contexto:** segundo escalón de volumen. Vitoria-Gasteiz entra porque es el
caso raro del NAP (declara los cinco distintivos a la vez, lo que no puede ser
cierto) y resolverlo a mano vale como prueba de que el flujo aguanta.

**Ficheros:** `content/zbe/{malaga,bilbao,valladolid,vitoria-gasteiz}.md`

- [ ] **Paso 1 a 4.** Repetir el ciclo de T4 con cada uno: localizar la
      ordenanza, extraer los seis datos, compilar, comprobar en navegador.
- [ ] **Paso 5.** Si sobra tiempo, seguir por Palma, Granada, A Coruña y
      Alicante, en ese orden. Si no, quedan para la semana que viene: **ocho
      municipios bien es mejor resultado que doce a medias.**
- [ ] **Paso 6.** Actualizar `cobertura.json` con el recuento real.
- [ ] **Paso 7.** Commit por municipio.

---

### T6 · Reality Checker sobre todo lo verificado

**Agente:** Reality Checker. Viene configurado para partir de «NEEDS WORK» y
exigir pruebas antes de aprobar. Es exactamente lo que hace falta aquí.

- [ ] **Paso 1.** Dispatch con el encargo concreto: para cada ficha nueva,
      abrir su `fuente_url`, localizar el artículo citado y confirmar que dice
      lo que la ficha afirma. Devolver una lista de discrepancias.
- [ ] **Paso 2.** Toda discrepancia se resuelve **a la baja**: si no se puede
      confirmar, la ficha baja a nivel C y pierde la tabla de distintivos.
- [ ] **Paso 3.** Arreglar lo que salga. Commit.
- [ ] **Paso 4.** Desplegar y comprobar en producción que la herramienta
      responde por los municipios nuevos.

---

# DÍA 2 — Sábado 26: funcionalidad

---

### T7 · Mapa interactivo de las ZBE de España

**Agentes:** Frontend Developer implementa; UI Designer revisa el resultado
visual.

**Contexto:** es la funcionalidad diferencial del proyecto. Sale del GeoJSON
de T1 y ningún competidor lo tiene.

**Ficheros:**
- Crear: `content/mapa.md`, `layouts/mapa/single.html` (o `_default` según
  cómo resuelva el lookup), `assets/js/mapa-zbe.js`,
  `assets/css/extended/mapa.css`

**Consume:** `static/datos/zbe-simplificado.geojson` de T1, con las
propiedades `slug`, `municipio`, `url_ficha`, `estado_dato`.

- [ ] **Paso 1.** Cargar Leaflet 1.9 desde cdnjs **solo en esta página**, no
      en el bundle global. Teselas de OpenStreetMap con su atribución, y la
      atribución CC-BY a la DGT junto a ella: las dos son obligatorias.
- [ ] **Paso 2.** Cargar el GeoJSON de forma diferida, después del primer
      pintado, para no hundir el LCP.
- [ ] **Paso 3.** Colorear cada zona por `estado_dato`: verificada en un
      color, pendiente en otro, con leyenda. Que se vea de un vistazo lo que
      está contrastado y lo que no es coherente con el resto del sitio.
- [ ] **Paso 4.** Al pulsar una zona, un globo con el municipio y el enlace a
      su ficha. El enlace sale de `properties.url_ficha`, no se construye en
      JavaScript.
- [ ] **Paso 5.** Comprobar el peso real en el navegador: el panel de red
      tiene que dar **menos de 400 KB en total** para la página del mapa,
      Leaflet incluido. Si se pasa, simplificar más la geometría en T1.
- [ ] **Paso 6.** Comprobarlo a 375 px: que el mapa no secuestre el gesto de
      scroll de la página. Leaflet lo hace por defecto y en móvil es
      insoportable; se arregla con `dragging` desactivado hasta que se toca el
      mapa.
- [ ] **Paso 7.** Alternativa sin JavaScript: si no carga, la página tiene que
      mostrar igualmente la tabla de municipios enlazada. El mapa es un extra,
      no el único camino al dato.
- [ ] **Paso 8.** Añadir «Mapa de ZBE» al menú lateral en
      `data/menu_lateral.json`.
- [ ] **Paso 9.** Commit y despliegue.

---

### T8 · Mapa de la zona dentro de cada ficha

**Agente:** Frontend Developer.

**Ficheros:** modificar `layouts/zbe/single.html`; crear
`layouts/partials/mapa-municipio.html`.

- [ ] **Paso 1.** Partial que pinta solo el polígono del municipio, centrado y
      sin controles de navegación. Se activa únicamente si existe geometría
      para ese slug.
- [ ] **Paso 2.** Va **debajo** del bloque de fuente y verificación: primero
      de dónde sale el dato, luego el dibujo.
- [ ] **Paso 3.** Comprobar en una ficha sin geometría que no queda un hueco
      vacío ni un error en consola.
- [ ] **Paso 4.** Commit.

---

### T9 · Herramienta «¿Cuándo me toca la ITV?»

**Agente:** Frontend Developer.

**Contexto:** la más barata de las tres calculadoras —son reglas por tipo y
antigüedad, sin datos municipales— y abre la vertical de ITV que el plan de
negocio tenía prevista. Fuente: RD 920/2017, verificado en el BOE.

**Ficheros:** crear `content/itv/cuando-me-toca.md`, `data/itv_periodicidad.json`,
`assets/js/itv.js`; modificar `data/menu_lateral.json`.

- [ ] **Paso 1.** Extraer del RD 920/2017 los plazos por tipo de vehículo y
      llevarlos a `data/itv_periodicidad.json`, con su fuente y su fecha,
      igual que `etiquetas_dgt.json`. **Las reglas no se escriben en el JS.**
- [ ] **Paso 2.** Reutilizar el perfil de vehículo de `localStorage` que ya
      usa la herramienta de ZBE: quien ya metió su coche no lo vuelve a meter.
- [ ] **Paso 3.** Envolver **toda** lectura y escritura de `localStorage` en
      `try/catch`. En navegación privada lanza excepción y sin esto la
      herramienta deja de responder al pulsar «Consultar»:

```javascript
function leerPerfil() {
  try {
    return JSON.parse(localStorage.getItem(CLAVE_PERFIL)) || null;
  } catch (e) {
    return null;  // Navegación privada o almacenamiento lleno.
  }
}
```

- [ ] **Paso 4.** Probarlo de verdad en una ventana privada con el
      almacenamiento bloqueado: la herramienta tiene que funcionar entera, solo
      que sin recordar el vehículo.
- [ ] **Paso 5.** La salida dice la fecha y **cita el artículo**, igual que
      las fichas de ZBE. Misma regla: no es una autorización.
- [ ] **Paso 6.** Hueco de anuncio debajo del resultado, con
      `partials/anuncio.html`. Nunca encima.
- [ ] **Paso 7.** Crear también `content/itv/pegatina.md`, respondiendo a «¿es
      obligatorio llevar la pegatina de la ITV?». Son 2.190 búsquedas al mes
      con KD 15 y 16, la mejor oportunidad individual de todo el estudio de
      palabras clave. Mismo formato que las páginas de distintivos: norma
      citada con su artículo, enlace al BOE y fecha de verificación. **El dato
      sale del texto oficial, no de lo que yo crea recordar.**
- [ ] **Paso 8.** Commit y despliegue.

---

### T10 · ¿Está mi calle dentro de una ZBE?

**Agente:** Frontend Developer.

**Contexto y por qué sustituye a la calculadora del IVTM.** Los datos de
Semrush del 28/09/2026 tumbaron el plan anterior. El racimo del impuesto de
circulación son 25.900 búsquedas al mes frente a las 221.010 de ZBE, con un
CPC prácticamente igual (0,44 $ frente a 0,49 $), y sobre todo con la
intención equivocada: las cinco primeras variaciones son «cómo pagar»,
«pagar por internet» y «pagar sin recibo», y los diez primeros resultados son
portales tributarios de ayuntamientos. Quien busca el IVTM quiere pagarlo, no
calcularlo, y eso solo lo resuelve su ayuntamiento.

Lo que sí tiene demanda es el mapa: «mapa» es el segundo subgrupo más grande
del racimo de ZBE, con 849 palabras, y entre las preguntas aparece «cómo saber
si una calle es zbe madrid». Esta herramienta responde a eso con la geometría
que ya está en disco desde T1.

**Ficheros:** crear `content/zbe/mi-calle.md`, `assets/js/mi-calle.js`;
modificar `data/menu_lateral.json`.

**Consume:** `static/datos/zbe.geojson` de T1, con `properties.slug`,
`properties.municipio` y `properties.url_ficha`.

- [ ] **Paso 1.** Geocodificar la dirección con Nominatim de OpenStreetMap,
      limitado a España. Respetar su política de uso: una petición por segundo
      y cabecera de identificación. Si no responde, la herramienta lo dice y
      ofrece el mapa para buscar a mano.
- [ ] **Paso 2.** Implementar punto en polígono con el algoritmo de proyección
      de rayos, a mano. Son 50 polígonos, no hace falta ninguna librería.
- [ ] **Paso 3.** Probarlo con tres direcciones conocidas: una dentro de
      Distrito Centro, una en Madrid pero fuera de él, y una en un municipio
      sin ZBE. Las tres respuestas tienen que ser distintas y correctas.
- [ ] **Paso 4.** **La respuesta nunca es binaria.** No «sí, estás dentro»,
      sino «esta dirección cae dentro del perímetro que la DGT publica para la
      ZBE de X. El perímetro oficial lo fija la ordenanza: compruébalo en
      [enlace] y en la señalización de la calle». La geometría del NAP es un
      dato de la DGT, no la ordenanza.
- [ ] **Paso 5.** Enlazar desde el resultado a la ficha del municipio y a la
      herramienta de «¿puedo circular?», que es el siguiente paso natural.
- [ ] **Paso 6.** La dirección que escribe el usuario **no se guarda ni se
      envía a ningún sitio nuestro**: va a Nominatim y se descarta. Decirlo en
      la propia página y en la política de privacidad.
- [ ] **Paso 7.** Hueco de anuncio debajo del resultado. Nunca encima.
- [ ] **Paso 8.** Commit y despliegue.

---

### T11 · Página sobre las cámaras de las ZBE

**Agente:** Content Creator redacta; yo extraigo los datos de la fuente.

**Contexto:** «camara» es un subgrupo de 181 palabras dentro del racimo de
ZBE, y no estaba en el plan. La gente quiere saber dónde están las cámaras
que multan y cómo funcionan. Es contenido barato de producir y encaja con la
página de multas que ya existe.

**Ficheros:** crear `content/zbe/camaras.md`; modificar
`content/multas/zbe.md` y `data/menu_lateral.json`.

- [ ] **Paso 1.** Reunir de las ordenanzas ya verificadas qué dicen sobre el
      control por cámara y la lectura de matrículas.
- [ ] **Paso 2.** Explicar el circuito completo: cámara, cotejo con el
      Registro de Vehículos, notificación. Sin especular sobre lo que no
      conste por escrito en una fuente oficial.
- [ ] **Paso 3.** Enlazar con `/multas/zbe/` en los dos sentidos.
- [ ] **Paso 4.** Commit y despliegue.

---

### T12 · Sistema visual de las herramientas

**Agentes:** UI Designer y Brand Guardian (este último, una sola vez en la
vida del proyecto).

**Contexto:** ya hay tres herramientas y cada una se ha ido pintando por su
cuenta. Es el momento de unificar, antes de que sean seis.

**Ficheros:** crear `assets/css/extended/sistema.css`,
`docs/sistema-visual.md`; modificar los CSS existentes.

- [ ] **Paso 1.** UI Designer audita las tres herramientas y el mapa y
      devuelve las inconsistencias concretas.
- [ ] **Paso 2.** Extraer a variables CSS en `:root` lo que se repite.
      Recordatorio de `CLAUDE.md`: **las variables solo se heredan hacia
      abajo**, por eso van en `:root` y no en el componente.
- [ ] **Paso 3.** Brand Guardian fija paleta, escala tipográfica y uso del
      logotipo, y lo deja escrito en `docs/sistema-visual.md` para no volver a
      decidirlo.
- [ ] **Paso 4.** Comprobar los colores en tema claro y oscuro con un medidor
      de contraste. Mínimo 4.5:1 para texto normal.
- [ ] **Paso 5.** Commit y despliegue.

---

# DÍA 3 — Domingo 27: calidad, SEO y monetización

---

### T13 · Accesibilidad

**Agente:** Accessibility Auditor.

- [ ] **Paso 1.** Auditoría de las páginas que representan cada plantilla:
      portada, una ficha de ZBE, el mapa, una calculadora, `/etiquetas/` y una
      página legal.
- [ ] **Paso 2.** Arreglar todo lo que sea bloqueante o grave. Sospecho ya de
      tres: el mapa sin alternativa por teclado, el contraste de los estados
      de veredicto, y el foco dentro del panel del menú en móvil.
- [ ] **Paso 3.** Recorrer el sitio entero solo con teclado, sin ratón.
- [ ] **Paso 4.** Commit.

---

### T14 · Rendimiento

**Agente:** Performance Benchmarker.

- [ ] **Paso 1.** Medir Core Web Vitals en las mismas seis páginas, en móvil.
- [ ] **Paso 2.** Vigilar en particular la página del mapa, que es la única
      con JavaScript de terceros.
- [ ] **Paso 3.** Objetivo: LCP por debajo de 2,5 s y CLS por debajo de 0,1 en
      móvil simulado. Documentar lo que no se cumpla y por qué.
- [ ] **Paso 4.** Comprobar que todas las imágenes llevan `width` y `height`.
      Es la causa habitual de CLS y ya mordió con las pegatinas de la DGT.
- [ ] **Paso 5.** Commit.

---

### T15 · SEO técnico y enlazado interno

**Agente:** SEO Specialist.

- [ ] **Paso 1.** Revisar el enlazado interno con las páginas nuevas: cada
      ficha de municipio debe enlazar a las etiquetas que nombra, al mapa y a
      las calculadoras; y al revés.
- [ ] **Paso 2.** Revisar `partials/schema.html` para las plantillas nuevas.
      `Dataset` para `/datos/`, `HowTo` o `FAQPage` donde encaje de verdad, no
      forzado.
- [ ] **Paso 3.** Comprobar que ninguna página nueva se queda huérfana.
- [ ] **Paso 4.** Actualizar `docs/seo-arquitectura.md`.
- [ ] **Paso 5.** Verificar que `noindex` **sigue activo**. Es el paso que más
      fácil se cuela.
- [ ] **Paso 6.** Commit.

---

### T16 · Redacción y citabilidad

**Agentes:** Content Creator para los textos, AI Citation Strategist para
`/metodologia/`.

**Contexto:** que ChatGPT o Perplexity citen el sitio como fuente sobre ZBE es
un canal que no depende de Google y que encaja con tener datos propios.

- [ ] **Paso 1.** Content Creator revisa todos los textos de cara al usuario
      buscando jerga, frases largas y párrafos sin respiro. **No inventa
      datos**: solo mejora la redacción de lo ya verificado.
- [ ] **Paso 2.** AI Citation Strategist revisa `/metodologia/`, `/datos/` y
      `/sobre/`: son las páginas que decide un modelo cuando valora si el
      sitio es citable.
- [ ] **Paso 3.** Asegurar que cada ficha empieza respondiendo a la pregunta y
      no con un preámbulo. Es lo que se extrae como respuesta.
- [ ] **Paso 4.** Commit.

---

### T17 · Legales y consentimiento

**Agente:** Legal Compliance Checker.

**Bloqueada en parte:** sin tus datos de identidad, los pasos 2 y 3 no se
pueden completar.

- [ ] **Paso 1.** Revisión de las cuatro páginas legales contra lo que exigen
      el RGPD, la LSSI y las políticas de AdSense. Lista de lo que falta.
- [ ] **Paso 2.** *(Bloqueado)* Rellenar la identidad del titular.
- [ ] **Paso 3.** Integrar un CMP certificado por Google. Sin él no se puede
      servir publicidad a usuarios del EEE.
- [ ] **Paso 4.** Comprobar que **ningún script de terceros se carga antes del
      consentimiento**. Hoy no hay ninguno, y conviene que siga así por
      defecto.
- [ ] **Paso 5.** Commit.

---

### T18 · Preparar la monetización

**Agente:** ninguno. Investigación mía, y decisiones tuyas.

- [ ] **Paso 1.** Inventario de huecos de anuncio ya existentes y dónde
      faltaría alguno, respetando la regla dura 4.
- [ ] **Paso 2.** Investigar programas de afiliación de **seguros de coche**,
      que es donde está el dinero: 6,13 $ de CPC frente a 0,49 $ de ZBE, con un
      racimo de 446.000 búsquedas al mes. Anotar **condiciones reales, no
      estimadas**, con enlace a cada programa. Después, ITV y talleres.
- [ ] **Paso 2b.** Diseñar la vertical de **seguro obligatorio**, que es el
      puente entre el tráfico y el dinero. No se compite por «seguro de coche»:
      su SERP son diez aseguradoras con KD de 42 a 47. Se compite por las
      preguntas de normativa que ellas no responden, que tienen KD de 6 a 11:
      «¿es obligatorio el seguro si el coche no circula?», «¿qué pasa si
      conduzco sin seguro?», «¿qué multa hay por no tenerlo?». Mismo formato
      que las fichas de ZBE: norma citada, artículo y fecha de verificación.
      Salen del BOE, nunca de lo que sepa un modelo.
- [ ] **Paso 3.** Escribir `docs/monetizacion.md` con lo encontrado y lo que
      queda por decidir. Sin cifras inventadas: lo que sea estimación irá
      marcado como tal.
- [ ] **Paso 4.** Lista de comprobación previa a solicitar AdSense, con lo que
      ya se cumple y lo que no.
- [ ] **Paso 5.** Commit.

---

### T19 · Puerta final y despliegue

**Agente:** Reality Checker.

- [ ] **Paso 1.** Dispatch sobre todo el fin de semana: que certifique, con
      pruebas, que cada ficha publicada se corresponde con su fuente y que
      ninguna herramienta afirma nada que no pueda respaldar.
- [ ] **Paso 2.** `python pipeline/auditoria.py` y `hugo --gc --minify`, los
      dos limpios.
- [ ] **Paso 3.** Recorrido manual en producción a 375 px y a 1400 px, en tema
      claro y oscuro.
- [ ] **Paso 4.** Actualizar `CLAUDE.md`: estado, municipios verificados y
      cualquier trampa nueva en «Trampas ya pisadas».
- [ ] **Paso 5.** Escribir el resumen del fin de semana: qué se hizo, qué
      quedó fuera y qué te toca a ti.

---

## Qué NO se va a hacer este fin de semana

Por si alguna de estas te parece más urgente que lo planificado:

- **Quitar el `noindex`.** Va atado al dominio, no a este plan.
- **Solicitar AdSense.** Sin datos de identidad no se puede, y pedirlo dos
  veces perjudica.
- **Los 37 municipios restantes.** Verificar bien ocho ya son tres días.
- **Motos y ciclomotores.** Sus criterios de distintivo siguen sin
  contrastar contra fuente oficial. Se quedan fuera hasta que lo estén.
- **Rediseñar la portada.** Funciona; hay cosas con más retorno.
