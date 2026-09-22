# Arquitectura SEO — recomendaciones

**Fecha:** 22/09/2026 · **Alcance:** este documento. No se ha tocado `layouts/`, `hugo.toml` ni `content/`.
Todo cambio que afecte a esos directorios está descrito aquí como instrucción para aplicar a mano.

**Sobre las cifras:** no hay ningún volumen de búsqueda ni CPC en este documento. Donde hace falta un
número para decidir, se indica el criterio y la fuente donde validarlo (Keyword Planner / SERP real).
Los umbrales de métricas del apartado 7 son objetivos operativos, no predicciones.

---

## 0. Dos bloqueantes antes de publicar la primera pieza

### 0.1. El dominio tiene que estar decidido y conectado ANTES del primer contenido indexable

`INSTRUCCIONES-CLAUDE-CODE.md` (Fase 4) dice "devolver URL `.pages.dev`, no conectar dominio propio
todavía". Eso está bien para probar el build. **No está bien para publicar contenido.**

Secuencia problemática: publicas 8 fichas en `proyecto.pages.dev`, Google las indexa, luego conectas
`normativacoche.es` y tienes que migrar con 301. En un dominio de 3 meses sin autoridad, una migración
cuesta entre 4 y 12 semanas de reevaluación y puede tirar por tierra todo lo ganado. El coste de
evitarlo es cero.

Regla: mientras `baseURL` apunte a `*.pages.dev`, **ningún contenido real se publica en estado
indexable**. Dos formas de garantizarlo (elegir una):

- **Preferida:** elegir dominio y conectarlo antes de la pieza nº 1. Es una decisión de 20 € que
  desbloquea todo lo demás.
- **Alternativa:** mantener el despliegue como preview. Cloudflare Pages añade `X-Robots-Tag: noindex`
  automáticamente a *todos* los preview deployments (`rama.proyecto.pages.dev`), pero **no** al
  despliegue de producción (`proyecto.pages.dev`). Verificarlo con
  `curl -I https://<url>.pages.dev | findstr /i x-robots-tag` antes de fiarse.

Cuando se conecte el dominio: `baseURL` debe apuntar al dominio propio **el mismo día**. PaperMod
genera el canonical desde `.Permalink`, que deriva de `baseURL` (`_partials/head.html`, línea 25), así
que con `baseURL` correcto el `proyecto.pages.dev` residual emitirá canonicals hacia el dominio bueno y
el duplicado se resuelve solo. Verificar la propiedad en Search Console como **propiedad de dominio**
(TXT en DNS), no como prefijo de URL — así cubre `www`, no-`www` y http/https de golpe.

### 0.2. `params.env = "production"` está fijado en `hugo.toml` y anula la protección del tema

`themes/PaperMod/layouts/_partials/head.html`, línea 4:

```go-html-template
{{- if hugo.IsProduction | or (eq site.Params.env "production") | and (ne .Params.robotsNoIndex true) }}
<meta name="robots" content="index, follow">
```

Con `env = "production"` escrito a fuego en `[params]`, **cualquier** build —local, rama, preview—
emite `index, follow`. Lo mismo pasa con `themes/PaperMod/layouts/robots.txt`, que decide
`Disallow: /` vs `Disallow:` con la misma condición.

**Cambio en `hugo.toml`:** eliminar la línea `env = "production"` de `[params]`. `hugo.IsProduction`
ya es `true` cuando se ejecuta `hugo` sin `-e`, así que la producción sigue funcionando. Luego, en
Cloudflare Pages → Settings → Environment variables → **Preview**, añadir `HUGO_ENVIRONMENT = preview`.
A partir de ahí los previews emiten `noindex, nofollow` y `Disallow: /` por sí solos.

---

## 1. Arquitectura de URLs

### 1.1. Veredicto: la propuesta plana es correcta. No anidar por provincia.

Mantener `/zbe/<municipio>/` y **no** pasar a `/zbe/<provincia>/<municipio>/`. Tres razones de
posicionamiento, por orden de peso:

**(a) La anidación diseña una canibalización que luego hay que arreglar.** En España, 23 de las 50
provincias se llaman igual que su capital: Madrid, Barcelona, Valencia, Sevilla, Zaragoza, Málaga,
Murcia, Alicante, Córdoba, Valladolid, Granada, Badajoz, Toledo, Burgos, Salamanca, León, Cáceres,
Castellón, Huesca, Teruel, Cuenca, Segovia, Soria... La anidación produce el par:

```
/zbe/madrid/          ← hub de provincia
/zbe/madrid/madrid/   ← ficha de la ciudad
```

Ambas URLs compiten por la misma consulta (`zbe madrid`), y el hub de provincia gana por estar un nivel
más arriba y recibir más enlaces internos — es decir, gana la página que **no** tiene la respuesta. Ese
es exactamente el fallo que el apartado 3 se dedica a prevenir; no tiene sentido introducirlo en la
estructura de URLs.

**(b) El nivel de provincia no tiene demanda que capturar.** El patrón de búsqueda es
`zbe + [ciudad]`, no `zbe + provincia de [X]`. Las ZBE son competencia municipal: no existe una "ZBE
de la provincia de Córdoba". Un nivel de URL que no corresponde a ninguna consulta real solo añade
saltos entre el pilar y la ficha. Validar en Keyword Planner antes de descartarlo del todo, pero la
hipótesis por defecto es demanda nula.

**(c) Al lanzar habría ~12 hubs de provincia con una ficha cada uno.** Eso son 12 URLs cuyo contenido
es un enlace. Thin content indexable en la sección que más necesita señales de calidad. Ver apartado 4.

**Profundidad resultante:** home → `/zbe/` → ficha = 2 saltos. Con un solo nivel intermedio, todas las
fichas están a la misma distancia del pilar y del home. Cualquier enlace que gane el sitio (que vendrá
a `/datos/` o al home) llega a las fichas en 2 saltos.

**Riesgo de colisión de nombres:** entre los ~151 municipios de más de 50.000 habitantes no hay
homónimos. Los duplicados clásicos del nomenclátor (Villanueva de..., Puebla de...) son municipios
pequeños que nunca tendrán ZBE. El espacio de nombres plano es seguro para este universo. Si algún día
aparece una colisión, se resuelve con sufijo en el slug (`/zbe/miranda-de-ebro/`), **nunca** añadiendo
un nivel de directorio: añadir el nivel cambiaría la URL de las 151 fichas existentes.

### 1.2. Reglas de slug (fijarlas ahora, no se pueden cambiar después)

1. **Slug = nombre oficial del municipio, sin acentos, en minúsculas, con guiones.** `malaga`,
   `a-coruna`, `caceres`, `alcala-de-henares`. Añadir `removePathAccents = true` a `hugo.toml` como
   red de seguridad para que un fichero llamado `málaga.md` no genere `/zbe/m%C3%A1laga/`.
2. **Topónimos con doble forma: el slug lleva la forma oficial, el contenido lleva las dos.**
   `/zbe/a-coruna/` con `<title>` "ZBE A Coruña (La Coruña): ...", y la variante castellana en la
   descripción y en una pregunta del FAQ. `/zbe/girona/`, `/zbe/donostia-san-sebastian/`,
   `/zbe/vitoria-gasteiz/`, `/zbe/eivissa/`. **Nunca dos URLs para el mismo municipio.** Es la forma
   más fácil de crear un duplicado perfecto en un sitio de 20 páginas.
3. **Sin año en la URL.** El `<title>` puede llevar "2026"; la URL no. Si `/zbe/madrid-2026/` existe,
   cada enero hay que redirigir, y una cadena de 301 anuales en un dominio joven es gratuita de evitar.
4. **Sin prefijo redundante.** `/zbe/madrid/`, no `/zbe/zbe-madrid/`.

### 1.3. Municipios con varias zonas, y zonas que cubren varios municipios

Son dos casos reales y hay que decidirlos antes de la ficha nº 2.

**Un municipio, varias zonas** (Madrid: ZBEDEP Distrito Centro, ZBEDEP Plaza Elíptica, ZBE municipal):
**una sola ficha** `/zbe/madrid/` con un `<h2>` por zona. No crear `/zbe/madrid/distrito-centro/` —
eso reintroduce la anidación y su canibalización. Única excepción: si una zona tiene un nombre propio
con demanda de búsqueda independiente y verificable (el caso histórico de "Madrid Central"), se crea
al **mismo nivel** (`/zbe/madrid-central/`), con keyword primaria distinta, y `/zbe/madrid/` la enlaza
sin competir con ella.

**Una zona, varios municipios** (ZBE Rondes: Barcelona, L'Hospitalet, Esplugues, Cornellà, Sant Adrià):
**una ficha por municipio**, porque así se busca ("zbe hospitalet"). Pero con una condición dura:
cada ficha debe tener al menos un 40 % de contenido propio y verificado — qué ayuntamiento tramita
las excepciones, qué registro de residentes aplica, qué administración emite la sanción, qué calles
del término municipal quedan dentro. Si para un municipio no se puede llegar a ese 40 %, **no se
publica la ficha**: se cubre dentro de la del municipio principal con un `<h2>`. Cinco fichas que
repiten el mismo horario y las mismas etiquetas son cinco duplicados, y Google elige una y descarta
las otras cuatro.

### 1.4. `/etiquetas/<tipo>/`

Cambiar `/etiquetas/b/` por `/etiquetas/etiqueta-b/`. Es feo (`etiquetas/etiqueta-`), y el valor de
la palabra clave en la URL es un factor muy débil, así que el motivo no es ese: es que `/etiquetas/b/`
es un token ambiguo que rompe el breadcrumb ("Inicio > Etiquetas DGT > b"), rompe el anchor text
automático y rompe el enlace que otro sitio te pegue en crudo. Slugs definitivos:

```
/etiquetas/etiqueta-0/
/etiquetas/etiqueta-eco/
/etiquetas/etiqueta-c/
/etiquetas/etiqueta-b/
/etiquetas/sin-etiqueta/
/etiquetas/como-pedir-la-etiqueta-ambiental/
```

Prioridad: baja. Hacerlo antes de publicar; no merece una redirección después.

### 1.5. Dónde va el contenido transversal

No usar `/guias/` para el contenido transversal de ZBE. La masa temática de una sección se construye
con URLs bajo el mismo directorio; sacar "multa por entrar en una ZBE" a `/guias/` reparte la señal
entre dos carpetas sin ganar nada.

```
/zbe/multa-por-entrar-en-zbe/     ← pieza nº 26 del plan
/zbe/excepciones/                 ← pieza nº 28 del plan
/zbe/                             ← pieza nº 27 del plan (ver 3.5: NO es una página aparte)
```

Reservar `/guias/` para lo que no pertenece a ninguna vertical (por ejemplo, "cómo leer una ficha
técnica"). Al lanzar, `/guias/` puede no existir.

---

## 2. Enlazado interno hub-and-spoke

Reglas escritas para que el agente de `layouts/` las implemente sin decidir nada. Los conteos son
objetivos, no máximos rígidos: la banda importa, el número exacto no.

### 2.1. Mapa de flujo

```
                         /  (herramienta)
                         │  12-18 enlaces
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
     /zbe/          /etiquetas/        /datos/zbe/
     (pilar)          (pilar)          (imán de enlaces)
        │  todas         │  5 fichas         ▲
        │                │                   │ 1 enlace desde cada ficha
        ▼                ▼                   │ + 1 desde cada pilar
  /zbe/<municipio/ ◄──► /etiquetas/etiqueta-X/
        │  ▲
        │  └─ 3-5 municipios relacionados (misma provincia → misma CCAA)
        │
        ├──► /zbe/multa-por-entrar-en-zbe/
        ├──► /zbe/excepciones/
        └──► bloque cruzado: /impuestos/ivtm/<municipio>/ · /itv/<ccaa>/   (auto-activable)
```

### 2.2. Home (`layouts/index.html`)

| Destino | Nº | Anchor |
|---|---|---|
| `/zbe/` | 1 | `todas las ciudades con ZBE en España` |
| `/etiquetas/` | 1 | `qué etiqueta ambiental tiene tu coche` |
| `/datos/zbe/` | 1 | `descargar el dataset de ZBE (CSV y JSON)` |
| Fichas destacadas | 8-12 | `ZBE {{ municipio }}` |

La lista de fichas destacadas va en `data/destacados.yaml` (lista curada de slugs), **no** generada
automáticamente con `first 150`. El home es la página con más autoridad del sitio; repartirla entre
151 enlaces equivale a no repartirla. 8-12 enlaces nombrados concentran señal en las fichas que se
quiere empujar ese trimestre, y la lista se edita a mano cada 2-3 meses.

**Regla crítica:** el enlace que la herramienta JS inyecta en el resultado ("Ver la ficha completa de
la ZBE de Zaragoza") **no cuenta como enlace para descubrimiento**. Es para el usuario. La ruta
rastreable a todas las fichas es siempre `/zbe/` renderizado en HTML. No depender nunca de un enlace
que solo existe tras ejecutar JS.

### 2.3. Pilar `/zbe/` (`layouts/zbe/list.html`)

- **Lista completa de fichas publicadas, sin paginar.** `hugo.toml` tiene `pagerSize = 20`: si la
  plantilla usa `.Paginator`, los municipios 21 en adelante acaban en `/zbe/page/2/`, que recibe una
  fracción del PageRank y hunde las fichas de las ciudades pequeñas — justo las que sí se pueden
  ganar. **Usar `.Pages` directamente, nunca `.Paginator`, en `zbe/list.html`.**
- Agrupar por CCAA con un `<h2>` por comunidad, y **ordenar dentro de cada grupo por población
  descendente**, no alfabéticamente. La posición en el HTML es una señal de importancia relativa.
- Cada fila: enlace + estado (`activa` / `prevista`) + `fecha_vigor` + `fecha_verificacion`. Con eso,
  el pilar deja de ser un índice y pasa a ser la respuesta a "lista de ciudades con ZBE en España".
- Anchor: `ZBE {{ .Params.municipio }}`. Nunca el `<title>` completo (lleva el año).
- Enlaces salientes adicionales: `/etiquetas/` (1), `/datos/zbe/` (1), `/zbe/multa-por-entrar-en-zbe/`
  (1), `/zbe/excepciones/` (1).

### 2.4. Ficha de municipio (`layouts/zbe/single.html`) — 10-14 enlaces internos

Orden en la página, de arriba abajo:

**1. Breadcrumb** — `Inicio > ZBE > ZBE {{ municipio }}`. PaperMod ya emite `BreadcrumbList` en
`_partials/templates/schema_json.html`; mantenerlo.

**2. Enlace al pilar**, en el primer párrafo. Para no repetir 151 veces el mismo anchor, alternar de
forma determinista entre dos variantes:

```go-html-template
{{ $anchors := slice "todas las ZBE de España" "el listado de ciudades con ZBE" }}
{{ $i := mod (len .File.ContentBaseName) 2 }}
<a href="/zbe/">{{ index $anchors $i }}</a>
```

**3. Enlaces a etiquetas**, dentro de la tabla de restricciones, generados desde el front matter. Es
el puente ZBE → etiquetas y es 100 % automatizable:

```go-html-template
{{ range .Params.etiquetas_permitidas }}
  {{ $slug := cond (eq . "sin") "sin-etiqueta" (printf "etiqueta-%s" (lower .)) }}
  {{ with site.GetPage (printf "/etiquetas/%s" $slug) }}
    <a href="{{ .RelPermalink }}">etiqueta {{ $.Scratch.Get "x" | default "" }}{{ $slug }}</a>
  {{ end }}
{{ end }}
```

Anchor: `etiqueta {{ X }}`. Son 1-4 enlaces. El `with site.GetPage` evita enlazar a páginas que aún no
existen: al lanzar solo existen 3 de las 5 fichas de etiqueta y el bloque se adapta solo.

**4. Bloque "Qué pasa si entras sin permiso"** — 2 enlaces:
`/zbe/multa-por-entrar-en-zbe/` (anchor: `cómo recurrir una multa de ZBE`) y `/zbe/excepciones/`
(anchor: `excepciones para residentes, PMR y vehículos históricos`).

**5. Municipios relacionados — 3-5 enlaces.** Regla automatizable, sin depender de taxonomías:

```go-html-template
{{ $self := . }}
{{ $prov := where (where site.RegularPages "Section" "zbe") "Params.provincia" .Params.provincia }}
{{ $ccaa := where (where site.RegularPages "Section" "zbe") "Params.ccaa" .Params.ccaa }}
{{ $rel := (union $prov $ccaa) | symdiff (slice $self) }}
{{ $rel = first 4 (sort $rel "Params.poblacion" "desc") }}
```

Prelación: misma provincia primero, luego misma CCAA, y si aún faltan, completar con las fichas de
mayor población del país. Requiere un campo `poblacion` (entero) en el front matter de la ficha o en
`data/zbe.json`; **recomendación: en `data/zbe.json`**, para que el front matter no crezca y el dato
lo mantenga el pipeline. Anchor: `ZBE {{ municipio }}`.

Este bloque es el que evita que las fichas de ciudades pequeñas queden colgando de un solo enlace.
Objetivo duro: **toda ficha publicada recibe ≥2 enlaces internos contextuales** (el pilar + al menos
un "relacionado" o una tabla de etiqueta). Ver el chequeo automático en 2.8.

**6. Bloque cruzado entre verticales — 0-2 enlaces, autoactivable.** Es el que sube páginas vistas por
sesión y, con ello, el RPM. Se escribe ahora y no hace nada hasta que existan las verticales:

```go-html-template
{{ $slug := .File.ContentBaseName }}
{{ $ccaa := urlize .Params.ccaa }}
{{ $ivtm := site.GetPage (printf "/impuestos/ivtm/%s" $slug) }}
{{ $itv  := site.GetPage (printf "/itv/%s" $ccaa) }}
{{ if or $ivtm $itv }}
<aside class="cruzado">
  <h2>Más obligaciones de tu coche en {{ .Params.municipio }}</h2>
  <ul>
    {{ with $ivtm }}<li><a href="{{ .RelPermalink }}">Impuesto de circulación en {{ $.Params.municipio }}</a></li>{{ end }}
    {{ with $itv }}<li><a href="{{ .RelPermalink }}">Precio y plazos de la ITV en {{ $.Params.ccaa }}</a></li>{{ end }}
  </ul>
</aside>
{{ end }}
```

Tres detalles que deciden si esto funciona:
- **Colocación: justo después del bloque de datos verificados y antes del FAQ.** No en el footer. Un
  enlace repetido en el footer de 151 páginas se trata como boilerplate y se descuenta; ahí en medio,
  con anchor que incluye el municipio, es un enlace contextual.
- **Anchor con el topónimo dentro**, siempre. "Impuesto de circulación en Gijón", no "ver IVTM".
- **`site.GetPage` devuelve `nil` si la página no existe o es draft**, así que el bloque no genera
  nunca un 404 ni una sección vacía. Es la razón por la que se puede escribir hoy.

**7. Bloque de fuente** — enlace externo a la ordenanza / BOP / sede del ayuntamiento.
**Sin `rel="nofollow"`.** Citar la fuente oficial con un enlace normal es la señal E-E-A-T más barata
que tiene el sitio y es literalmente el argumento del plan de negocio (apartado 9.3). Poner `nofollow`
a un enlace a `.gob.es` no protege de nada y desperdicia la señal. Añadir en ese mismo bloque un
enlace a `/datos/zbe/` con anchor `metodología y descarga del dataset de ZBE`.

**8. Sin prev/next.** `hugo.toml` tiene `ShowPostNavLinks = true`. En una sección de fichas de ciudad,
prev/next ordena por fecha y produce enlaces semánticamente vacíos ("ZBE Gijón" → "ZBE Vitoria" porque
se publicaron seguidas). Desactivarlo en las fichas (`ShowPostNavLinks: false` en el arquetipo o
condicionarlo por sección en la plantilla) y dejar que el bloque 5 haga ese trabajo.

### 2.5. Páginas de etiqueta (`layouts/etiquetas/single.html`) — 8-12 + tabla

La aportación clave: **una segunda ruta de enlaces hacia las fichas, ortogonal al pilar.** Desde
`data/zbe.json`, cada página de etiqueta lista los municipios donde esa etiqueta tiene restricción:

```go-html-template
<h2>Ciudades donde la etiqueta {{ .Params.etiqueta }} tiene restricciones</h2>
<table>
{{ range first 20 (sort (where site.Data.zbe.municipios "restringe_<X>" true) "poblacion" "desc") }}
  <tr><td><a href="/zbe/{{ .slug }}/">ZBE {{ .municipio }}</a></td><td>{{ .horario }}</td></tr>
{{ end }}
</table>
<p><a href="/zbe/">Consultar el resto de ciudades con ZBE</a></p>
```

Límite: 20 filas + 1 enlace al pilar. Con esto, cada ficha recibe enlaces desde el pilar **y** desde
1-4 páginas de etiqueta, sin enlaces artificiales: la tabla es contenido real y es el tipo de tabla
que se lleva fragmentos destacados.

Resto de enlaces de la página de etiqueta: `/etiquetas/` (1), `/` herramienta (1), las otras 4 páginas
de etiqueta (4, en un bloque de comparación), `/etiquetas/como-pedir-la-etiqueta-ambiental/` (1).

### 2.6. `/datos/zbe/`

- Recibe: 1 enlace desde el home, 1 desde el pilar `/zbe/`, 1 desde cada ficha. Es donde se quiere
  concentrar autoridad porque es la página que se pretende que enlacen desde fuera.
- Emite: enlace a `/zbe/` y a la metodología. Poco más: una página que quieres que se enlace no debe
  repartir su equity.
- **Schema `Dataset` completo** — es el único schema de este sitio con retorno real. Google Dataset
  Search lo indexa y es un canal de descubrimiento gratuito para el público exacto que buscas
  (periodistas de datos, gestorías). Campos mínimos: `name`, `description`, `license`
  (`https://creativecommons.org/licenses/by/4.0/`), `creator`, `dateModified`, `temporalCoverage`,
  `spatialCoverage` (España), y `distribution` con un `DataDownload` por cada fichero
  (`encodingFormat: text/csv` / `application/json`, `contentUrl` absoluta).

### 2.7. Reglas de anchor text (aplicables sin criterio humano)

1. **Nunca el `<title>` completo como anchor** si contiene el año. Usar siempre la forma perenne.
2. **Nunca** `aquí`, `ver más`, `leer más`, `este enlace` como único anchor.
3. Ficha → ficha: `ZBE {{ municipio }}`.
4. Cruzado entre verticales: siempre con el topónimo dentro del anchor.
5. Hacia el pilar: rotación determinista entre 2 variantes (2.4, punto 2).
6. Hacia `/datos/`: siempre incluir el formato (`CSV y JSON`). Ayuda a que quien lo cite escriba un
   anchor útil.

### 2.8. Chequeo automatizable (añadir a `pipeline/auditoria.py`)

Sobre el HTML de `public/` después del build:

- **Huérfanas:** toda URL de `/zbe/` y `/etiquetas/` debe aparecer como `href` en ≥2 páginas distintas
  fuera de la navegación y el footer. Falla el build si no.
- **Saturación:** ninguna página de contenido supera los 60 enlaces internos (el pilar `/zbe/` está
  exento por definición).
- **Anchors prohibidos:** `grep` de `>aquí<`, `>ver más<`, `>leer más<` en `<a>`.
- **Enlaces rotos internos:** todo `href` interno resuelve a un fichero existente en `public/`.

---

## 3. Canibalización

Todavía no hay datos de Search Console, así que este apartado usa el método de mapa de intención +
deconflicto de `<title>`/`H1` (el método pre-GSC). A partir del mes 3 se valida con datos reales
según el apartado 7.4.

### 3.1. El riesgo real y por qué es el riesgo nº 1 del sitio

La amenaza no es que dos artículos se solapen. Es esta, y es estructural:

> El home es la herramienta "¿Puedo circular?". El home concentra toda la autoridad del dominio. Si el
> home contiene texto sobre ciudades concretas, Google lo posicionará por `zbe [ciudad]` **por encima
> de la ficha**, porque tiene más autoridad. El usuario aterriza en un formulario vacío en vez de en
> la respuesta, rebota, y la ficha —que es donde están el contenido verificado, los enlaces internos
> y el hueco de anuncio— nunca acumula señales.

Es el patrón "página ancla + subpágina" de manual, y en este sitio está montado por diseño porque la
herramienta ocupa el home. Se previene, no se arregla después.

### 3.2. Mapa de propiedad de consultas

Cada página tiene **una** keyword primaria. Esta tabla es el contrato: ninguna página puede invadir
la columna de otra.

| URL | Intención | Consultas que DEBE ganar | Consultas que NO debe tocar | Prohibido en la página |
|---|---|---|---|---|
| `/` | Herramienta, sin ciudad | `puedo circular zbe`, `comprobar si puedo entrar en una zbe`, `consultar zbe de mi coche` | cualquier `zbe + [ciudad]` | **ningún topónimo en `<title>`, `H1` o `H2`**; ningún párrafo estático por ciudad |
| `/zbe/` | Informacional nacional + directorio | `ciudades con zbe en españa`, `lista de zbe 2026`, `cuántas zbe hay en españa`, `mapa zbe españa` | `zbe + [ciudad]` | `H2` con el nombre de una sola ciudad; reglas de una ciudad en prosa |
| `/zbe/<municipio>/` | Navegacional-local + decisión | `zbe [ciudad]`, `zbe [ciudad] horario`, `puedo entrar en [ciudad] con etiqueta B`, `multa zbe [ciudad]`, `zbe [ciudad] residentes` | consultas nacionales genéricas | explicar qué es una ZBE en más de 2 frases; explicar qué es la etiqueta B |
| `/etiquetas/` | Informacional + herramienta | `etiqueta ambiental de mi coche`, `qué distintivo me corresponde`, `distintivo ambiental dgt` | `zbe + [ciudad]` | listados de reglas municipales |
| `/etiquetas/etiqueta-b/` | Informacional nacional | `etiqueta b`, `coches con etiqueta b`, `dónde puede circular la etiqueta b` | `etiqueta b [ciudad]` (es de la ficha) | secciones en prosa por ciudad — **solo tabla de enlaces** |
| `/zbe/multa-por-entrar-en-zbe/` | Transaccional | `multa zbe`, `cuánto es la multa por entrar en una zbe`, `recurrir multa zbe` | `multa zbe [ciudad]` | importes o plazos por ciudad en `H2` o en prosa |
| `/zbe/excepciones/` | Informacional | `excepciones zbe`, `zbe residentes`, `zbe vehículos históricos`, `zbe discapacidad` | `zbe [ciudad] residentes` | procedimientos municipales concretos |
| `/datos/zbe/` | Datos / captación de enlaces | `dataset zbe`, `csv zonas de bajas emisiones españa`, `datos abiertos zbe` | todo lo anterior | contenido divulgativo — solo metodología, licencia y descarga |

### 3.3. Las tres reglas que hacen cumplir la tabla

**Regla A — el home no nombra ciudades.** Ni en `<title>`, ni en `H1`, ni en `H2`, ni en texto
estático. `hugo.toml` ya está bien en esto:
`homeInfoParams.Title = "¿Puedes circular por la ZBE de tu ciudad?"` — genérico, correcto, mantener.
Los municipios aparecen en el home solo como: (a) opciones del `<select>` de la herramienta, y (b) los
8-12 enlaces destacados, donde el topónimo está dentro de un `<a>` y no en texto de la página. Esa
distinción es la que mantiene la separación.

**Regla B — el genérico enlaza al local; el local no explica lo genérico.** Cuando dos páginas
cubren el mismo eje a distinta escala, la nacional lista a la local en forma de **tabla con enlaces**,
nunca en prosa. En cuanto `/zbe/multa-por-entrar-en-zbe/` tenga un `<h2>Multa de la ZBE en Madrid</h2>`
con tres párrafos, se lleva la consulta local que pertenece a `/zbe/madrid/`. Y al revés: la ficha de
Madrid no explica el régimen sancionador general, lo resume en dos frases y enlaza.

**Regla C — cada `<h2>` pertenece a una sola página del sitio.** Antes de publicar, comprobar que el
`<h2>` que vas a escribir no existe ya, con el mismo significado, en otra página. Es el chequeo
manual de 30 segundos que evita el 80 % de los problemas.

### 3.4. Las dos herramientas: cómo se separan

`/` y `/etiquetas/` contienen las dos un widget que deduce la etiqueta DGT. Hay que separarlas o son
duplicados funcionales:

- **`/etiquetas/`** = **paso 1 aislado**. Input: tipo, combustible, año. Output: tu etiqueta + qué
  significa. Intención: *"¿qué etiqueta tengo?"*. Sin selector de municipio.
- **`/`** = **flujo completo**. Perfil de vehículo (recuperado de `localStorage` si ya lo introdujo en
  `/etiquetas/`) + selector de municipio → puedo circular / no, con horario, excepciones y fuente.
  Intención: *"¿puedo entrar?"*.

Son intenciones distintas y el sitio gana las dos. Lo que **no** puede pasar es que `/etiquetas/`
incorpore el selector de municipio: en ese momento son la misma página en dos URLs.

### 3.5. Colisiones ya presentes en el plan, a corregir antes de escribir

1. **Pieza nº 27 del plan ("Lista completa de ciudades con ZBE en España") = el pilar `/zbe/`.**
   Son la misma intención al 100 %. No crear una página aparte: el brief de la pieza 27 es el
   contenido del pilar. Ahorra una página y elimina un duplicado garantizado.
2. **Taxonomía `etiquetas-dgt` vs sección `/etiquetas/`.** `/etiquetas-dgt/c/` y
   `/etiquetas/etiqueta-c/` apuntan a la misma consulta, y la taxonómica es una lista pelada. Ver
   apartado 4: eliminar.
3. **Taxonomías `provincias` y `ccaa` vs fichas.** `/provincias/madrid/` vs `/zbe/madrid/`, misma
   consulta. Ver apartado 4: eliminar.
4. **Pieza nº 30 ("Etiqueta B: qué coches la tienen y dónde pueden circular") vs las fichas.** El
   "dónde pueden circular" es el eje que canibaliza. Resolver con la Regla B: tabla de enlaces, no
   prosa por ciudad.
5. **Fichas `estado_zbe: prevista` sin reglas verificadas.** Nivel C: no hay reglas que publicar, así
   que la ficha queda en 150 palabras. Quince fichas así arrastran la valoración de calidad de toda la
   sección. **Umbral duro: una ficha se publica si (nivel A o B) o (nivel C con ≥300 palabras de
   contenido propio verificado: delimitación oficial, calendario publicado, estado de tramitación de
   la ordenanza con enlace al expediente).** Si no llega, se queda en `draft` y aparece en el pilar
   como fila sin enlace, con estado "prevista, pendiente de ordenanza". El pilar sí puede listarla
   —eso es dato verificado del mapa MITECO— sin que exista una URL propia.

### 3.6. Verificación automatizable, sin Search Console

Añadir a `pipeline/auditoria.py`, sobre el HTML de `public/`:

1. Extraer `<title>` y `<h1>` de todas las páginas construidas.
2. Cargar la lista de municipios de `data/zbe.json`.
3. **Fallar si un topónimo aparece en el `<title>` o el `<h1>` de más de una página.**
4. **Fallar si un topónimo aparece en el `<title>` o el `<h1>` del home.**
5. Avisar si dos páginas comparten un `<h2>` con normalización (minúsculas, sin acentos, sin año).

Son 40 líneas de Python y cubren la canibalización estructural desde el día 1, mucho antes de que
haya datos en Search Console.

---

## 4. Taxonomías

### 4.1. Diagnóstico

`hugo.toml` define tres taxonomías:

```toml
[taxonomies]
  provincia = "provincias"
  ccaa = "ccaa"
  etiqueta = "etiquetas-dgt"
```

| Taxonomía | URLs que genera | Contenido al lanzar | Veredicto |
|---|---|---|---|
| `provincias` | `/provincias/` + ~12 términos | 1 enlace por término | **Thin content + canibalización** con la ficha homónima (`/provincias/madrid/` vs `/zbe/madrid/`) |
| `ccaa` | `/ccaa/` + ~8 términos | 1-2 enlaces por término | **Thin content**. Valor futuro real cuando exista `/itv/<ccaa>/`, pero hoy no |
| `etiquetas-dgt` | `/etiquetas-dgt/` + 0 términos | **vacío** | El arquetipo usa `etiquetas_permitidas` (array), no la clave `etiqueta`. La taxonomía nunca se rellena, pero Hugo **igualmente genera `/etiquetas-dgt/`**: una URL indexable con cero contenido, viva desde el primer build |

Las tres aportan al sitio exactamente una cosa: la posibilidad de listar fichas por provincia o
comunidad. Eso se puede hacer sin ellas con un `where` sobre `site.RegularPages` (ver 2.4, punto 5),
que es lo que la plantilla ya necesita de todos modos. Es decir, **el coste (URLs finas e indexables)
es real y el beneficio es cero**.

### 4.2. Recomendación: eliminarlas, no ponerlas en `noindex`

**Cambios en `hugo.toml`:**

```toml
[taxonomies]
  provincia = "provincias"
  ccaa = "ccaa"
  # etiqueta = "etiquetas-dgt"   ← eliminar: nunca se rellena y choca con /etiquetas/

disableKinds = ["taxonomy", "term"]
```

Por qué `disableKinds` y no `noindex`:

1. **`noindex` deja la URL viva.** Sigue gastando rastreo, sigue pudiendo recibir enlaces, y hay que
   mantener la directiva. `disableKinds` hace que la URL no exista. Un problema que no existe no
   necesita una directiva que lo gestione.
2. **El `noindex` de PaperMod es el incorrecto para este caso.** `_partials/head.html` línea 7 emite
   `noindex, **nofollow**` cuando `robotsNoIndex: true`. Para una página de directorio lo que se quiere
   es `noindex, follow`, para que el equity siga fluyendo hacia las fichas. Usar el parámetro del tema
   tal cual cortaría ese flujo, y corregirlo obliga a copiar las 195 líneas de `head.html` al proyecto.
3. **No se pierde nada.** `disableKinds` impide renderizar las páginas de taxonomía, pero
   `site.Taxonomies` sigue disponible en plantillas. Y la lógica de "municipios relacionados" del
   apartado 2.4 no usa taxonomías en absoluto: filtra por `.Params.provincia` con `where`. Es más
   robusta y no depende de que el término se renderice.
4. **Evita el efecto colateral de borrar el bloque.** Si se elimina `[taxonomies]` entero, Hugo
   restaura las taxonomías por defecto (`tags` y `categories`) y aparecen `/tags/` y `/categories/`
   vacías. Por eso se deja el bloque y se añade `disableKinds`.

### 4.3. Cuándo reconsiderarlo (`ccaa`, mes 9+)

`ccaa` es la única con valor futuro, cuando exista la vertical ITV (el precio y el régimen de la ITV
sí son autonómicos). En ese momento, la página autonómica **no debe ser una página de taxonomía**: debe
ser una página de sección real, `/itv/aragon/`, escrita a mano, con datos propios. Los criterios para
crearla:

- ≥5 fichas relacionadas en esa comunidad, **y**
- ≥300 palabras de introducción escrita, no generada por plantilla, **y**
- al menos un dato propio (precio medio de ITV en esa CCAA, extraído del dataset).

Nunca indexar una página de agregación solo porque haya superado un umbral de elementos. El umbral de
elementos hace que la página exista; el texto propio hace que merezca estar en el índice.

---

## 5. robots.txt y sitemap

### 5.1. `static/robots.txt`: **no procede**. Motivo:

`hugo.toml` tiene `enableRobotsTXT = true` y el tema trae `themes/PaperMod/layouts/robots.txt`, que
ya genera un robots.txt correcto. Meter además un `static/robots.txt` crea dos ficheros compitiendo
por la misma ruta de salida (`public/robots.txt`) con resultado dependiente del orden de montaje — es
el tipo de fallo que se descubre tres meses después mirando por qué no se rastrea nada. Además, un
fichero estático obliga a escribir a mano la URL absoluta del sitemap, y el dominio aún no está
decidido (ver 0.1); la plantilla la deriva de `baseURL` y se actualiza sola.

**Por eso no se ha creado el fichero.** La vía correcta es un override de proyecto en
`layouts/robots.txt` (el proyecto gana sobre el tema). **Ojo con la ruta:** esta versión de PaperMod
exige Hugo ≥ 0.146 y usa el layout lookup nuevo (`layouts/baseof.html`, `layouts/_partials/`), así
que el override va en **`layouts/robots.txt`**, no en `layouts/_default/`.

Contenido para el agente de `layouts/`:

```go-html-template
{{- if hugo.IsProduction }}
User-agent: *
Allow: /
Disallow: /404.html
Disallow: /search/
Disallow: /index.json

# Rastreadores de IA: permitidos deliberadamente.
# Ser la fuente citada en una respuesta generada es el canal de autoridad
# más barato disponible para un dominio sin presupuesto de enlaces.
User-agent: GPTBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: CCBot
Allow: /

Sitemap: {{ "sitemap.xml" | absURL }}
{{- else }}
User-agent: *
Disallow: /
{{- end }}
```

### 5.2. Qué excluir y, sobre todo, qué NO excluir

**Excluir:**

| Ruta | Motivo |
|---|---|
| `/404.html` | Hugo la emite y Cloudflare Pages la sirve; no debe estar en el índice |
| `/search/` | Página de búsqueda de PaperMod: cero contenido propio. Añadirle además `robotsNoIndex: true` y `sitemap: {disable: true}` en su front matter |
| `/index.json` | Índice de búsqueda de PaperMod (`[outputs] home = [..., "JSON"]`): contiene el texto completo de todas las páginas en una sola URL. Es el duplicado más grande del sitio |

**No excluir, y esto importa más:**

- **Nada de las taxonomías.** Con `disableKinds` no existen. Y aunque existieran: `Disallow` en
  robots.txt **no desindexa** — impide leer la página, con lo que Google no puede ver el `noindex` y
  puede indexar la URL a pelo. Nunca usar robots.txt para controlar indexación.
- **Nada de `/datos/`.** Los CSV y JSON se quieren rastreables e indexables: son el activo de
  captación de enlaces y la entrada a Google Dataset Search.
- **Nada por presupuesto de rastreo.** Un sitio estático de 20-150 URLs sin parámetros de query no
  tiene problema de crawl budget. Cualquier `Disallow` justificado "por eficiencia de rastreo" en este
  sitio es un error.

### 5.3. Sitemap

**Los drafts ya están cubiertos.** `buildDrafts = false` y la convención `estado_dato: pendiente ⇔
draft: true` hacen que una ficha sin verificar no se compile, y lo que no se compila no puede entrar
en el sitemap. No hay que hacer nada más. Lo único que hay que mantener es el guardián de
`pipeline/auditoria.py` que comprueba que ambos campos no se desincronicen.

**Cambio 1 — `lastmod` debe ser la fecha de verificación, no la del fichero.** Es el cambio con mejor
relación valor/esfuerzo de este apartado. La propuesta de valor del sitio es "esto está verificado y
fechado"; si el `<lastmod>` del sitemap dice la fecha en que se tocó el Markdown por cualquier motivo,
se está desperdiciando la única señal de frescura que se tiene. En `hugo.toml`:

```toml
[frontmatter]
  lastmod = ["fecha_verificacion", "lastmod", ":fileModTime"]
```

Efecto secundario deseable: `dateModified` del schema (`schema_json.html` línea 94 usa `.Lastmod`)
pasa a reflejar también la verificación.

**Cambio 2 — quitar `changefreq` y `priority`.** Google ignora los dos desde hace años. Hoy se emiten
en todas las URLs con el mismo valor (`monthly` / `0.5`), lo que no transmite ninguna información y
solo engorda el fichero. Eliminar el bloque `[sitemap]` de `hugo.toml` salvo `filename`.

**Cambio 3 — filtrar el sitemap por `Kind`.** Si en algún momento se revierte `disableKinds`, o si
aparecen páginas paginadas, el sitemap las incluirá. Un override en `layouts/sitemap.xml` lo cierra
de forma permanente:

```go-html-template
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  {{- range . }}
  {{- if and (in (slice "home" "page" "section") .Kind) (not .Params.sitemap_disable) }}
  <url>
    <loc>{{ .Permalink }}</loc>
    {{- if not .Lastmod.IsZero }}
    <lastmod>{{ .Lastmod.Format "2006-01-02" }}</lastmod>
    {{- end }}
  </url>
  {{- end }}
  {{- end }}
</urlset>
```

Para casos sueltos (la página de búsqueda), Hugo ≥ 0.125 admite `sitemap: {disable: true}` en el front
matter. Verificar la versión antes de usarlo; el filtro por `Kind` de arriba funciona en cualquier caso.

**Cambio 4 — `disableXML = true` en `[minify]`: correcto, mantener.** Minificar el sitemap y los RSS
no aporta nada y ha dado problemas de parseo. Está bien como está.

### 5.4. Tres problemas adicionales detectados en el tema (no son robots, pero son técnicos y caros)

**(a) `schema_json.html` vuelca el contenido entero de la página dentro del JSON-LD.** Línea 77:

```go-html-template
"articleBody": {{ .Content | safeJS | htmlUnescape | plainify }},
```

Eso duplica el peso de HTML de cada página. En una ficha con tablas, mapa y FAQ, es un sobrecoste
directo sobre LCP y sobre la transferencia, a cambio de nada: Google lee el cuerpo visible. **Quitar
`articleBody` y `wordCount` en un override de `layouts/_partials/templates/schema_json.html`.**

**(b) El tipo de schema es `BlogPosting` para todas las páginas.** Una ficha de ZBE no es una entrada
de blog. En el mismo override, condicionar por sección: `Article` (o mejor, `WebPage` con
`about`) para las fichas y las páginas de etiqueta, `Dataset` para `/datos/`. `BlogPosting` no rompe
nada, pero describe mal la entidad justo en un sitio cuya tesis es "somos la fuente de referencia".

**(c) Sobre `FAQPage`:** `INSTRUCCIONES-CLAUDE-CODE.md` lo pide para las guías. Merece un aviso:
desde agosto de 2023 Google restringe los resultados enriquecidos de FAQ a sitios gubernamentales y
sanitarios; **no habrá acordeón en la SERP**. Implementarlo igualmente —ayuda a la comprensión de
entidades y a la citación en respuestas generadas— pero con prioridad baja y sin esperar espacio extra
en resultados. El valor del bloque FAQ está en el contenido en sí (captura de long tail y de "Otras
preguntas"), no en el marcado.

**(d) El `<title>` va a desbordar.** `_partials/head.html` línea 11 compone
`{{ .Title }} | {{ site.Title }}`, y `site.Title` son 34 caracteres
("Normativa del vehículo en España"). Con el título del plan para la pieza 1:

> `ZBE Madrid 2026: qué coches pueden entrar y en qué horario | Normativa del vehículo en España` → 93 caracteres.

Google lo reescribirá, y cuando reescribe suele quedarse con el `H1` o con texto del ayuntamiento.
Dos arreglos, hacer los dos:
1. Al elegir dominio, poner en `hugo.toml` un `title` de marca corto (≤ 15 caracteres).
2. En el override de `head.html`, soportar un `seo_title` de front matter y omitir el sufijo de marca
   cuando `len(.Title) > 45`.

Regla de redacción para los títulos de ficha: **≤ 60 caracteres contando el sufijo de marca**, con el
topónimo lo más a la izquierda posible. `ZBE Madrid 2026: horarios y etiquetas | Marca` cabe; la
versión del plan no.

---

## 6. Los primeros 20 contenidos

### 6.1. Criterio de ordenación (y una corrección al plan)

Se ordena por **dependencia estructural primero, dificultad-ajustada-a-oportunidad después**:

1. **Los hubs van antes que los spokes.** Publicar 6 fichas antes de que exista el pilar significa 6
   páginas sin enlaces entrantes durante semanas, en el momento en que más importa que Google las
   descubra y las relacione entre sí.
2. **El imán de enlaces va lo antes posible.** Un enlace editorial tarda meses en traducirse en
   posiciones. `/datos/zbe/` es lo único que puede generarlos sin presupuesto, y su coste marginal es
   casi nulo una vez hecho el listado del pilar: es el mismo dato en otro formato. Publicarlo en el
   mes 1, no en el mes 6.
3. **El contenido transversal va antes que la masa de fichas.** Si `/zbe/excepciones/` no existe
   cuando escribes la sexta ficha, cada ficha acaba con tres párrafos genéricos sobre residentes y
   vehículos históricos, y a la décima ficha tienes diez copias del mismo texto compitiendo. Publicar
   el transversal pronto es una medida de control de canibalización, no de contenido.

**Corrección al plan de negocio:** el apartado 4 ordena las fichas "por población". Para un dominio de
un mes, ese orden está invertido. Para `zbe madrid` compiten `madrid.es`, la Wikipedia, la EMT,
El País, Motor.es y los cinco grandes portales de automoción. No se gana, ni en el mes 1 ni en el 12.
Donde sí se puede entrar es en ciudades de tamaño medio con activación reciente y una página municipal
que no responde la pregunta en HTML legible.

**Criterio de selección de ciudad — ejecutar este test antes de comprometerse con cada ficha** (5
minutos, en incógnito, sin personalización):

1. Buscar `zbe [ciudad] horario` y `puedo entrar en la zbe de [ciudad]`.
2. Contar cuántos de los 5 primeros resultados **responden literalmente con horario, etiquetas y
   excepciones en el texto visible**. Si son ≤ 1, es un objetivo bueno.
3. Mirar si la página del ayuntamiento está en el top 3. Si está y **responde bien**, la ficha no le
   quitará el puesto 1 — pero sí puede ganar los long tail (`...con etiqueta B`, `...los sábados`,
   `...siendo de fuera`). Eso sigue valiendo la pena; hay que saberlo de antemano.
4. Comprobar si hay AI Overview. Si lo hay y responde bien, esa consulta concreta dará menos clics del
   que sugiere su volumen — descontarlo al priorizar.

Candidatos a pasar por el test (población media, activación 2026, cobertura editorial débil *(est.,
por verificar con el test)*): Gijón, Valladolid, Vitoria-Gasteiz, Pamplona, Santander, Cartagena,
Elche, Badalona, Getafe, Alcalá de Henares, Logroño, Burgos, Salamanca.

### 6.2. Calendario, 5 piezas/mes, meses 1-4

**Mes 1 — cimientos. Ninguna ficha nueva salvo la de calibración.**

| # | URL | Rol | Dificultad *(est.)* | Por qué aquí |
|---|---|---|---|---|
| 1 | `/zbe/` | Pilar + contenido (pieza 27 del plan) | Media | Es el hub del que cuelga todo. Y es publicable con datos nivel C: la *lista* de municipios con ZBE está verificada por el mapa MITECO aunque no lo estén las reglas de cada uno. Ninguna otra página del sitio se puede publicar antes sin quedar huérfana |
| 2 | `/datos/zbe/` | Imán de enlaces | Baja (dato ya hecho) | Mismo dato que la pieza 1, otro formato. Los enlaces tienen el ciclo de maduración más largo del plan: arrancarlo el mes 1 en vez del 6 son 5 meses de ventaja sobre el único riesgo calificado como "alta gravedad" |
| 3 | `/etiquetas/` | Pilar + herramienta paso 1 | Media | Segundo hub. Tema nacional, perenne, independiente de la política de ZBE. Alimenta la herramienta del home y es el destino de los enlaces desde las tablas de restricciones de las fichas |
| 4 | `/` | Producto | — | La herramienta completa. No se puede publicar útil antes de tener ≥1 ficha verificada, por eso va la cuarta. Su keyword primaria es genérica, sin topónimo (ver 3.2) |
| 5 | `/zbe/zaragoza/` | Ficha de calibración | Baja | Carlos es de Zaragoza: acceso más rápido al BOP, conocimiento local para detectar un error y verificación más barata. Es la ficha con la que se fija la plantilla, así que conviene que sea la más fácil de comprobar. ZBE con activación 2026 = pico de búsqueda local en curso |

**Mes 2 — el clúster de etiquetas, que es el destino de los enlaces de todas las fichas futuras.**

| # | URL | Rol | Dificultad *(est.)* | Por qué aquí |
|---|---|---|---|---|
| 6 | `/etiquetas/etiqueta-c/` | Spoke | Media | La C es la etiqueta frontera: en unas ZBE entra y en otras no, y ese es el conjunto de conductores que de verdad no sabe qué hacer. Consulta con ansiedad máxima y respuesta que depende del dataset, o sea resistente a AI Overviews |
| 7 | `/etiquetas/etiqueta-b/` | Spoke | Media | La B es la excluida. Máxima ansiedad y máxima adyacencia comercial (renting, eléctricos, financiación) — es la página que mejor monetiza del lote de lanzamiento |
| 8 | `/etiquetas/sin-etiqueta/` | Spoke | **Baja** | La respuesta ("¿dónde puedo circular todavía?") es literalmente una consulta sobre tu dataset. Nadie más la puede contestar sin haber consolidado las ordenanzas. Es la página más defendible del sitio y la de menor competencia del clúster |
| 9 | `/zbe/<ciudad-A>/` | Ficha | Baja-media | Primera ficha elegida por el test de 6.1, no por población |
| 10 | `/zbe/<ciudad-B>/` | Ficha | Baja-media | **De otra CCAA que la A.** Con dos fichas en la misma comunidad, el bloque de "municipios relacionados" se cierra sobre sí mismo y la vertical ITV nace con un solo territorio cubierto |

**Mes 3 — cerrar el clúster de etiquetas y abrir el transversal de alto CPC.**

| # | URL | Rol | Dificultad *(est.)* | Por qué aquí |
|---|---|---|---|---|
| 11 | `/etiquetas/etiqueta-eco/` | Spoke | Baja | Completa el clúster. Poca ansiedad (estos conductores no tienen problema), pero intención comercial alta hacia híbridos y eléctricos |
| 12 | `/etiquetas/etiqueta-0/` | Spoke | Baja | Ídem. Con 11 y 12, las cinco tablas de restricciones de las fichas ya resuelven todos sus enlaces (`site.GetPage` deja de devolver `nil`) |
| 13 | `/zbe/multa-por-entrar-en-zbe/` | Transversal | Media-alta | El CPC más alto del alcance de lanzamiento *(est., validar)*: abogados de tráfico y aseguradoras. Intención transaccional. Se publica ahora y no antes porque necesita ≥4 fichas que le enlacen para no nacer huérfano |
| 14 | `/zbe/<ciudad-C>/` | Ficha | Baja-media | Test de 6.1 |
| 15 | `/zbe/<ciudad-D>/` | Ficha | Baja-media | Test de 6.1 |

**Mes 4 — control de canibalización, primer trámite y primera pieza de difusión.**

| # | URL | Rol | Dificultad *(est.)* | Por qué aquí |
|---|---|---|---|---|
| 16 | `/zbe/excepciones/` | Transversal | Media | "Residentes" es el modificador long tail más frecuente sobre *todas* las fichas. Esta página absorbe la consulta nacional y deja la local a cada ficha. Publicarla antes de que las fichas se multipliquen evita que cada una engorde con el mismo texto genérico — es control de duplicación, no contenido |
| 17 | `/etiquetas/como-pedir-la-etiqueta-ambiental/` | Trámite | **Baja** | Transaccional puro, volumen estable todo el año, verificación trivial (sede DGT + Correos). Es la salida natural de las cinco páginas de etiqueta. Y es la primera pieza del sitio que **no depende de la política de ZBE**: cubre el riesgo "cambio político" del plan |
| 18 | `/zbe/<ciudad-grande>/` | Ficha | **Alta** | Ahora sí: Madrid o Barcelona. Con 7 fichas y 2 pilares detrás, el sitio tiene masa temática para intentarlo. Se publica asumiendo que no ganará el término principal en mucho tiempo; el objetivo son los long tail (`...con etiqueta B`, `...los fines de semana`, `...siendo de fuera de Madrid`) y la completitud del dataset, que es lo que hace citable la pieza 20 |
| 19 | `/zbe/<ciudad-E>/` | Ficha | Baja-media | Test de 6.1 |
| 20 | `/datos/zbe/` v2 + nota de datos | Difusión | Media | Actualización del dataset + primera pieza de análisis propio: **"Qué etiquetas prohíbe cada una de las N ZBE de España"**. Sale del trabajo ya hecho, no hay que investigar nada nuevo, y es material que un medio local reproduce. Es el activo con el que se hace el primer contacto de difusión (datos.gob.es, periodistas locales, referencias en Wikipedia). Mes 4 es el momento: hay suficientes datos para que sea creíble y quedan margen suficiente para que los enlaces maduren antes del mes 12 |

### 6.3. Recuento

7 fichas de ciudad · 6 páginas de etiquetas + 1 trámite · 2 pilares · 2 transversales · 1 herramienta ·
2 hitos de `/datos/`. **20 piezas, 4 meses, 5 al mes.**

Al terminar el mes 4 el sitio tiene 20 páginas, que es justo el umbral que el plan de negocio marca
para solicitar AdSense (apartado 6.1) — con las legales rellenas y la CMP puesta, la solicitud entra
a principios del mes 5.

### 6.4. Qué NO hacer en estos cuatro meses

- **No publicar fichas de las 151 ciudades aunque el pipeline las genere.** El pilar puede listar las
  151 (eso es dato del mapa MITECO, verificado); solo se crea URL para las que superen el umbral de
  3.5, punto 5.
- **No abrir `/impuestos/`, `/itv/`, `/multas/` ni `/tramites/`.** Las secciones existen en la
  estructura, sin `_index.md` publicado. El bloque cruzado de 2.4 las detecta solo cuando existan.
- **No crear `/guias/` todavía.** No hay nada que meter que no encaje mejor bajo `/zbe/` o
  `/etiquetas/`.
- **No escribir la pieza 27 del plan como página aparte** (ver 3.5, punto 1).

---

## 7. Métricas de control, meses 1-6

No mirar tráfico los primeros 3 meses: no lo habrá, y mirarlo es exactamente lo que provoca el
abandono en el mes cuatro que el plan identifica como riesgo principal. Cada fase tiene una métrica
distinta, y ninguna de las tres primeras son clics.

**Montaje (día 1):** propiedad de **dominio** en Search Console (TXT en DNS), sitemap enviado, y alta
en **Bing Webmaster Tools** — son 2 minutos, es gratis, y el índice de Bing alimenta la búsqueda de
ChatGPT, que para este nicho no es marginal.

### 7.1. Meses 1-2 — indexación. Única métrica.

| Dónde | Qué mirar | Objetivo |
|---|---|---|
| Indexación > Páginas | URLs en "Indexadas" ÷ URLs del sitemap | ≥ 90 % a los 21 días de cada publicación |
| Indexación > Páginas | **"Descubierta: actualmente sin indexar"** | 0 fichas publicadas ahí pasados 21 días |
| Indexación > Páginas | **"Página alternativa con la etiqueta canónica adecuada"** | 0. Cualquier ficha aquí = Google la considera duplicado de otra |
| Seguridad y acciones manuales | Acciones manuales | Vacío. Mirar 10 segundos cada mes |

Usar Inspección de URL + "Solicitar indexación" con cada pieza nueva. A 5 piezas/mes es viable a mano
y tiene sentido mientras el dominio no tenga rastreo propio.

**La señal más temprana de que algo va mal está aquí, y no necesita nada de tráfico:**
"Descubierta: actualmente sin indexar" significa que Google conoce la URL y ha decidido no gastar en
ella. En un sitio de 10 páginas es casi siempre contenido fino o percibido como duplicado. Y
"Página alternativa con etiqueta canónica adecuada" sobre una ficha **es la alarma de canibalización
antes de tener un solo clic**: Google está diciendo que esa ficha es la misma página que otra.

### 7.2. Meses 2-4 — impresiones, nunca posición media.

Rendimiento > Resultados de búsqueda, filtro **Consulta → no contiene → [marca]**, para separar lo
que es orgánico real de lo que es alguien buscando el nombre del sitio.

| Qué mirar | Cómo | Objetivo mes 4 *(est.)* |
|---|---|---|
| Impresiones no-marca | Total, semana a semana | Crecimiento sostenido. No importa el número absoluto |
| **Distribución de posiciones** | Exportar la tabla de Consultas y contar cuántas caen en 1-10 / 11-20 / 21+ | Crecimiento de la banda **11-20** |
| Consulta principal por página | Pestaña Páginas → clic en una ficha → Consultas | La consulta nº 1 de cada ficha **contiene su topónimo** |
| CTR en posiciones 5-10 | Filtrar esas consultas | > 2 % |

Dos matices que cambian cómo se lee esto:

- **La posición media es un promedio de cosas distintas y no significa nada.** Si entras en posición 4
  para una consulta nueva de cola larga, tu "posición media" empeora. Mirar la *distribución*, no la
  media.
- **La banda 11-20 es el indicador adelantado.** Es lo que 3-6 meses después se convierte en clics. En
  el mes 3 es la única señal positiva disponible, y es una señal real.
- **Si la consulta principal de una ficha es nacional y genérica** (`zbe`, `etiqueta ambiental`) en vez
  de local, Google está tratando la ficha como una página genérica más: el `<title>`, el `H1` y el FAQ
  no son suficientemente locales. Es corregible en una tarde y hay que corregirlo en cuanto se vea.

### 7.3. Meses 4-6 — clics y enlaces.

| Qué mirar | Dónde | Objetivo mes 6 *(est.)* |
|---|---|---|
| Clics no-marca | Rendimiento, filtro no-marca | 20-80 / mes |
| Impresiones no-marca | Ídem | 300-800 / mes |
| **Dominios de referencia** | Enlaces > Sitios con más enlaces | ≥ 3 que no sean directorios ni scrapers |
| Páginas vistas por sesión | Cloudflare Web Analytics o GA4 | ≥ 1,8 |
| Core Web Vitals | Experiencia > Core Web Vitals | Todo en "Buena". Con Hugo + Cloudflare no hay excusa |

Las cifras de clics e impresiones son objetivos operativos para saber si el orden de magnitud es el
correcto, no predicciones. El número que de verdad decide el proyecto es el de **dominios de
referencia**: es el riesgo calificado como "alta gravedad" en el plan y es el único que no se arregla
escribiendo más.

**Páginas vistas por sesión** es la métrica que mide si el apartado 2 ha funcionado. Por debajo de 1,3
el enlazado interno no está moviendo a nadie, y como el RPM efectivo depende de las impresiones por
visita, es una pérdida directa de ingresos independiente del tráfico.

### 7.4. Mes 3 en adelante — auditoría mensual de canibalización (20 minutos)

Ahora ya hay datos para validar el mapa de 3.2:

1. **Por ciudad publicada:** Rendimiento → filtro Consulta **contiene** `[ciudad]` → pestaña Páginas.
   Si aparece más de una URL con impresiones y ambas están en el top 30, hay conflicto. Se resuelve
   según la tabla de 3.2: la ficha se queda la consulta, la otra página pierde el `H2` y gana un
   enlace hacia la ficha.
2. **El chequeo del home, que es el importante:** filtro Página **=** `/` → pestaña Consultas. **Si
   aparece cualquier consulta con un topónimo, el home está robando consultas locales.** Actuar
   inmediatamente: eliminar del home todo texto con nombres de ciudad (ver Regla A en 3.3). Es el
   fallo más caro del sitio y es detectable desde el mes 3.
3. **Por etiqueta:** filtro Consulta contiene `etiqueta b` → Páginas. Debe ganar
   `/etiquetas/etiqueta-b/` en las consultas nacionales, y la ficha correspondiente en `etiqueta b
   [ciudad]`.

### 7.5. Señales tempranas de que NO funciona, con umbral y acción

| Cuándo | Señal | Interpretación | Acción |
|---|---|---|---|
| Mes 2 | > 30 % de las URLs publicadas siguen sin indexar a los 21 días | Contenido percibido como fino o duplicado | **Parar de publicar.** Consolidar y engordar lo que hay antes de añadir nada |
| Mes 3 | Impresiones no-marca < ~200/mes con 12+ páginas vivas | O las keywords no tienen volumen, o las páginas no responden a la intención | Validar volúmenes en Keyword Planner **antes de escribir nada más**, y pasar el test SERP de 6.1 a las fichas ya publicadas |
| Mes 4 | Impresiones suben, pero ninguna consulta lleva topónimo | La estrategia local no está aterrizando: las fichas no se diferencian del hub | Auditar `<title>` y `H1` de cada ficha; ampliar el bloque FAQ con el fraseo local exacto de "Otras preguntas" |
| Mes 4 | El home aparece por `zbe [ciudad]` por encima de la ficha | Canibalización estructural en marcha | Quitar del home todo topónimo en texto. Ver 3.3, Regla A |
| Mes 5 | CTR < 1 % en consultas donde estás en posición 3-8 | El `<title>` no coincide con la intención, o Google lo ha reescrito (ver 5.4.d) | Reescribir `<title>` y `description`. Es la corrección más barata que existe |
| Mes 6 | 0 dominios de referencia descontando directorios | La estrategia de datasets ha fallado en su versión pasiva | Pasar a difusión activa: alta del dataset en datos.gob.es, contacto con 10 periodistas locales de las ciudades cubiertas, referencias en los artículos de Wikipedia sobre ZBE |
| Cualquiera | Acción manual en Search Console | Fatal | "Contenido generado automáticamente" sería el fin del proyecto. Es la razón del ritmo de 4-6 piezas/mes con verificación humana |

**Qué es normal y no es una señal de alarma:** cero clics en los meses 1-2; una ficha nueva sin
impresiones durante 3-4 semanas; posición media que empeora mientras las impresiones suben (es lo que
pasa cuando entras por consultas nuevas, y es buena señal); 0-3 dominios de referencia en el mes 6.

---

## Anexo — Cambios fuera de mi alcance, para aplicar a mano

### `hugo.toml`

| # | Cambio | Apartado |
|---|---|---|
| 1 | Eliminar `env = "production"` de `[params]` y poner `HUGO_ENVIRONMENT = preview` en el entorno Preview de Cloudflare Pages | 0.2 |
| 2 | Añadir `removePathAccents = true` | 1.2 |
| 3 | Eliminar `etiqueta = "etiquetas-dgt"` del bloque `[taxonomies]` | 4.2 |
| 4 | Añadir `disableKinds = ["taxonomy", "term"]` | 4.2 |
| 5 | Añadir `[frontmatter]` con `lastmod = ["fecha_verificacion", "lastmod", ":fileModTime"]` | 5.3 |
| 6 | Eliminar `changefreq` y `priority` del bloque `[sitemap]` | 5.3 |
| 7 | Al elegir dominio: `baseURL` al dominio propio y `title` de marca corto (≤ 15 car.) | 0.1 / 5.4.d |
| 8 | Considerar `ShowPostNavLinks = false` (o condicionarlo por sección en la plantilla) | 2.4, punto 8 |

### `layouts/` (para el agente que está trabajando ahí)

Ruta de overrides: esta versión de PaperMod exige Hugo ≥ 0.146 y usa el lookup nuevo —
**`layouts/baseof.html`, `layouts/_partials/…`**, no `layouts/_default/`.

| # | Fichero | Cambio | Apartado |
|---|---|---|---|
| 1 | `layouts/robots.txt` | Override con el contenido de 5.1 | 5.1 |
| 2 | `layouts/sitemap.xml` | Override filtrando por `.Kind` | 5.3 |
| 3 | `layouts/_partials/templates/schema_json.html` | Quitar `articleBody` y `wordCount`; `Article` en vez de `BlogPosting`; `Dataset` en `/datos/` | 5.4.a, 5.4.b, 2.6 |
| 4 | `layouts/_partials/head.html` | Soportar `seo_title`; omitir el sufijo de marca si el título es largo | 5.4.d |
| 5 | `layouts/index.html` | 12-18 enlaces; destacados desde `data/destacados.yaml`; **ningún topónimo en texto** | 2.2, 3.3 |
| 6 | `layouts/zbe/list.html` | `.Pages`, **nunca `.Paginator`**; agrupar por CCAA; ordenar por población desc.; columna de estado y fecha de verificación | 2.3 |
| 7 | `layouts/zbe/single.html` | Los 8 bloques de 2.4, en ese orden. Incluido el bloque cruzado autoactivable |  2.4 |
| 8 | `layouts/etiquetas/single.html` | Tabla de 20 ciudades desde `data/zbe.json` + enlace al pilar | 2.5 |

### `content/` y arquetipos

| # | Cambio | Apartado |
|---|---|---|
| 1 | Slugs de etiquetas: `etiqueta-0`, `etiqueta-eco`, `etiqueta-c`, `etiqueta-b`, `sin-etiqueta` | 1.4 |
| 2 | Arquetipo de ficha: `<title>` ≤ 60 car. con el sufijo de marca, topónimo a la izquierda, **sin año en el slug** | 1.2, 5.4.d |
| 3 | `content/search.md` (si se crea): `robotsNoIndex: true` + `sitemap: {disable: true}` | 5.2 |
| 4 | La pieza 27 del plan es el contenido de `content/zbe/_index.md`, no una página nueva | 3.5 |

### `pipeline/auditoria.py`

| # | Chequeo | Apartado |
|---|---|---|
| 1 | Topónimo en `<title>`/`<h1>` de más de una página → fallo | 3.6 |
| 2 | Topónimo en `<title>`/`<h1>` del home → fallo | 3.6 |
| 3 | Toda URL de `/zbe/` y `/etiquetas/` con ≥2 enlaces entrantes contextuales → si no, fallo | 2.8 |
| 4 | Ninguna página de contenido con > 60 enlaces internos (pilar exento) | 2.8 |
| 5 | Anchors prohibidos (`aquí`, `ver más`, `leer más`) → fallo | 2.7 |
| 6 | Enlaces internos rotos → fallo | 2.8 |
| 7 | `estado_dato` y `draft` desincronizados → fallo (ya previsto en `hugo.toml`) | 5.3 |
| 8 | `fecha_verificacion` > 6 meses → aviso (ya previsto en INSTRUCCIONES) | — |

### Datos que hacen falta y aún no existen

| Dato | Dónde | Para qué |
|---|---|---|
| `poblacion` (entero) por municipio | `data/zbe.json` | Ordenar el pilar y elegir municipios relacionados (2.3, 2.4) |
| `restringe_<etiqueta>` (booleano) por municipio | `data/zbe.json` | Tablas de las páginas de etiqueta (2.5) |
| `slug` por municipio | `data/zbe.json` | Construir enlaces sin depender del nombre del fichero |
| `data/destacados.yaml` | nuevo | Lista curada de 8-12 slugs para el home (2.2) |
