# WEBnormativas: contexto del proyecto

Portal de **normativa y fiscalidad del vehículo en España**. Sitio de nicho monetizado.
Ver [PLAN-NEGOCIO.md](PLAN-NEGOCIO.md) para el análisis completo.

## Quién

Carlos, Zaragoza. Analista de negocio/datos (SQL, Power BI), ADE + máster en BI.
Jornada completa: pocas horas/semana para esto. Presupuesto: solo dominio (~10-20 €/año).

## Stack

- **Hugo** (sitio estático) + **Cloudflare Pages** (hosting gratis) + **GitHub**
- Herramientas interactivas en **JavaScript client-side**, sin backend
- Claude genera contenido y herramientas; Carlos verifica y publica

## Decisiones tomadas (no volver a debatir)

1. **Nicho:** normativa/fiscalidad del vehículo. ZBE como punto de entrada.
2. **Verticales:** ZBE → etiquetas DGT → IVTM → ITV → multas → trámites.
3. **Empezar estrecho:** solo ZBE + etiquetas hasta ~mes 6. Abrir todas las categorías a la vez diluye la autoridad temática.
4. **El producto es el dataset**, no la calculadora. Una fórmula la copia cualquiera; 151 ordenanzas consolidadas no.
5. **Dominio neutro y ampliable** (no atarlo a "ZBE"). Sin decidir aún.
6. **Monetización apilada:** AdSense (arranca antes) + afiliación/leads (más valor por visita). Ambas.
7. **Perfil de vehículo único** en `localStorage`, reutilizable por todas las herramientas.

## Reglas de publicación de datos (críticas)

Niveles de confianza. **Nunca publicar por encima del nivel que se tiene:**

| Nivel | Origen | Qué se publica |
|---|---|---|
| A | NAP-DGT, DATEX2 legible por máquina | Respuesta completa |
| B | Ordenanza leída a mano, artículo citado | Respuesta completa + fecha |
| C | Solo se sabe que hay ZBE (mapa MITECO) | Ficha "reglas sin verificar" + enlace oficial. **No responder** "¿puedo entrar?" |
| D | Sin datos | **No publicar página** |

- **Nunca respuesta binaria.** No "✅ puedes entrar", sino "la ordenanza X (art. Y, fecha) permite… [enlace]. Verificado el DD/MM/AAAA".
- Cada dato lleva **fuente + enlace + fecha de verificación** visibles.
- Datos sin revisar durante meses se marcan solos como "pendiente de verificación".
- Solo fuentes oficiales y abiertas. Respetar robots.txt. No scrapear competidores.

## Ritmo

**4-6 piezas/mes**, cada una verificada. Publicar 80 páginas de golpe generadas con IA = penalización por *scaled content abuse*. El ritmo lento es una decisión de diseño, no una limitación.

## Fuentes de datos verificadas

| Fuente | Contenido | Licencia |
|---|---|---|
| [NAP-DGT](https://nap.dgt.es/dataset?license_id=cc-by&res_format=DATEX2V3&tags=ZBE) | Geometría + restricciones ZBE (DATEX2V3), cobertura parcial | **CC-BY** (citar) |
| [Mapa MITECO](https://www.miteco.gob.es/en/calidad-y-evaluacion-ambiental/temas/movilidad/zonas_de_bajas_emisiones_en_espana.html) | Listado oficial de municipios con ZBE y su estado | Pública |
| [Consulta impositiva municipal de Hacienda](https://serviciostelematicosext.hacienda.gob.es/SGFAL/ConsultaTipos/aspx/listado_municipiosm.aspx) | IVTM/IBI/IAE/IVTNU/ICIO por municipio, **export Excel masivo**, 2000-2025 | Pública |
| [API carburantes MITECO](https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/) | Precios de todas las gasolineras, horario | Pública |
| [DGT en cifras](https://www.dgt.es/menusecundario/dgt-en-cifras/) | Parque de vehículos y matriculaciones (ancho fijo) | Pública |
| [RD 1052/2022](https://www.boe.es/buscar/doc.php?id=BOE-A-2022-22689) | Marco legal ZBE | Pública |

**Legal:** el [art. 13 LPI](https://www.iberley.es/legislacion/articulo-13-ley-propiedad-intelectual) excluye las disposiciones legales y los actos de organismos públicos de la propiedad intelectual → las ordenanzas municipales son libremente reproducibles.

## Contexto de mercado (verificado 21-22/09/2026)

- Desde **01/01/2026** todos los municipios >50.000 hab. están obligados a tener ZBE.
- Feb-2026: 56 ciudades operativas → previsión de **151 municipios / 33M personas** durante el año.
- Multa por acceso indebido: **200 €**.

**Competidores analizados** (ninguno consolidado, ninguno con datos propios):

| Sitio | Edad | Páginas | Dom. ref. | Visitas/mes |
|---|---|---|---|---|
| sacacuentas.es | ~12m | 91 | 119 | **28** |
| simuloo.com | ~12m | 150 | 100+ | ~4.000 |
| costerealcoche.com | ~8m | 12 | Sin dato | Sin dato |
| ibeonix.es | nuevo | 3 | Sin dato | Sin dato |

Dos de los cuatro llevan meses abandonados.

## Datos de búsqueda verificados (Semrush, 28/09/2026)

España, escritorio. Cifras reales, no estimaciones.

| Racimo | Búsquedas/mes | CPC | Densidad | Intención |
|---|---|---|---|---|
| ZBE | 221.010 | 0,49 $ | 0,01 | Informativa |
| Impuesto de circulación | 25.900 | 0,44 $ | 0,02 | Informativa |
| Seguro de coche | 446.000 | **6,13 $** | 0,83 | **Comercial** |
| ITV | 5.272.580 | 0,50 $ | 0,08 | Comercial |

**El hallazgo que define la monetización:** el tráfico de ZBE es abundante y
fácil de ganar (KD medio del 19 % sobre 5.755 palabras) pero vale muy poco por
clic. El del seguro vale doce veces más, pero su SERP lo ocupan diez
aseguradoras con KD de 42 a 47. **No se compite por «seguro de coche».**

**Matiz importante, comprobado después:** al abrir los grupos del racimo del
seguro **no aparece ninguno de «obligatorio», «multa», «ley» ni «sin
seguro»** entre los diez mayores. Las dos palabras de normativa con KD 6 y 11
que parecían abrir una veta son casos sueltos, no un filón: las 537 preguntas
del racimo suman solo 2.600 búsquedas al mes entre todas.

Los diez grupos mayores son: baja 1.383, baratos 1.340, mas 913, dar 895,
precio 833, alquiler 815, mejor 803, compañía 706, puede 695, cuanto 690.
Cuatro de ellos (baratos, precio, mejor, compañía) son puro comercial y no se
pueden disputar.

**Modelo resultante: ZBE trae el tráfico, y el seguro se monetiza por
afiliación, no por contenido.** No hay una vertical de normativa del seguro
que construir; hay un mercado caro al que enviar tráfico propio.

**Pendiente de resolver (octubre):** qué es el grupo «baja», el mayor del
racimo con 1.383 palabras. Si es «dar de baja el seguro» es retención de
clientes y no nos toca; si es «baja temporal del vehículo» es un trámite de la
DGT y encaja de lleno en la vertical de trámites. Son cosas opuestas y no se
puede deducir del recuento.

Subgrupos dentro del racimo de ZBE, por número de palabras: barcelona 884,
**mapa 849**, madrid 779, zona 542, etiqueta 254, multa 210, camara 181.
Que «mapa» sea el segundo mayor es lo que justifica el mapa y la herramienta
de «¿está mi calle dentro de una ZBE?».

Municipios por volumen y dificultad: Madrid 9.900/36, Barcelona 6.600/39
(CPC 4,12 $, el único con valor publicitario), Bilbao 4.400/21, Granada
4.400/25, Valencia 3.600/**16**, Málaga 3.600/26, Valladolid 3.600/31,
Benidorm 2.900/17.

**La ITV es enorme y casi toda inservible.** De sus 253.247 palabras, más de
71.000 son para pedir cita (grupos: cita 37.116, previa 15.566, telefono
10.874, pedir 7.433), y las cinco primeras suman más de 600.000 búsquedas al
mes solo para reservar hora. Eso lo resuelven Applus, Itevelesa y Sitval, que
ocupan el top 10, **con el local pack de Google Maps apareciendo dos veces**:
Google trata la consulta como local, y una web nacional no gana consultas
locales. El término principal tiene KD 73.

Lo que sí se puede servir de la ITV:
- **La pegatina de la ITV: cuatro variantes de la misma pregunta que suman
  2.930 búsquedas al mes, ninguna por encima de KD 18** (1.600/16, 590/15,
  480/18, 260/17). Todas se responden con una sola página. Es la mejor
  oportunidad individual de todo el estudio: más tráfico potencial que
  `zbe benidorm` con una cuarta parte de la dificultad.
- **El formato «¿Es obligatorio…?», con 292 preguntas** dentro del racimo. No
  es una página, es una serie. Son preguntas de normativa con respuesta breve
  y una norma detrás, que es justo para lo que está montado este sitio. Su CPC
  es 0,00 $ porque no venden nada, pero traen visitas sin competencia que
  después pasan por las páginas que sí monetizan.
- **Tarifas de ITV por comunidad autónoma** (710 búsquedas entre «cuánto cuesta
  pasar la itv» y «cuánto cuesta la itv»). Mismo patrón que las ZBE: dato
  público, disperso en diecisiete sitios, que nadie consolida. Para octubre.
- El grupo «paso», 21.231 palabras, el segundo mayor. Casi con seguridad
  «cuándo pasar la ITV» y «cada cuánto se pasa». Intención deducida del nombre
  del grupo, no comprobada palabra por palabra.

Aviso sobre la cifra: parte del volumen es ruido británico, ya cuantificado.
Entre las 6.809 preguntas, los grupos `hub` (709), `watch` (531) y `tonight`
(308) son la cadena de televisión ITV del Reino Unido. Unas 1.500 preguntas
de cada 6.809 no tienen nada que ver con la inspección de vehículos.

**Convención de títulos: se usan las dos formas.** «Zona de Bajas Emisiones
(ZBE) de Valencia», no solo la sigla. La gente busca de las dos maneras y el
visitante típico llega después de una multa de 200 euros sin conocer el
acrónimo. No hay medición del racimo completo de la expresión larga (la
consulta del 28/09 salió filtrada a preguntas), así que se toma la decisión
conservadora de cubrir ambas.

**Cuánto respaldo tiene el mapa, dicho con precisión.** Conviene no inflarlo:

- El grupo «mapa» son **849 variantes de escritura de 5.755**, una de cada
  siete. Sale de la vista sin filtrar, que es lo que le da valor. Pero es un
  **recuento de palabras, no de búsquedas**: la barra lateral estaba en modo
  «By number» y no se midió el volumen. No tratar 849 como demanda.
- Que en las preguntas de «zona de bajas emisiones» domine «¿cuál es la de
  Madrid?» **no es una confirmación independiente**: esa vista estaba filtrada a
  preguntas, y las 63 juntas suman 1.060 búsquedas. Es la misma señal con datos
  más débiles.

Lo que de verdad sostiene el mapa no es el volumen, son las otras dos patas:
**ningún competidor publica los polígonos** (los diez primeros resultados son
ayuntamientos, cada uno con el suyo) y **la geometría ya está descargada**, así
que el coste es un script. Aunque la demanda sea la mitad de lo estimado, sale
a cuenta.

**Lo que NO funciona, comprobado:** la calculadora del IVTM. Las variaciones
principales son «cómo pagar», «pagar por internet» y «pagar sin recibo», y los
diez primeros resultados son portales tributarios municipales. Quien busca el
IVTM quiere pagarlo, y eso solo lo resuelve su ayuntamiento.

## Expectativa realista

120-450 €/mes a 18 meses (escenario medio). **Los primeros 6 meses no darán casi nada.**
El mayor riesgo del proyecto es abandonarlo en el mes cuatro.

## Estado actual

Al 28/09/2026.

- [x] Investigación de nicho y competencia
- [x] Plan de negocio
- [x] Fase 1: estructura Hugo
- [x] Fase 2: herramienta «¿Puedo circular?»
- [x] Fase 3: pipeline de datos (`pipeline/zbe_nap.py`, 45 municipios)
- [x] Fase 4: GitHub y Cloudflare Workers. En producción en
      `webnormativas.bi-ia-carlosbaz.workers.dev`, con `noindex` puesto.
- [x] Estudio de palabras clave (ver la sección de datos de búsqueda)
- [x] Hoja de ruta de tres días:
      `docs/superpowers/plans/2026-09-25-hoja-de-ruta-3-dias.md`
- [ ] **Dominio: elegido, sin comprar.** Ver abajo. Es lo único que bloquea
      arrancar la hoja de ruta.
- [ ] Fase 5: pre-AdSense (legales y CMP). Bloqueada hasta tener los datos de
      identidad de Carlos, que exige el art. 10 LSSI.

### Dominio (28/09/2026)

**Elegido: `cocheenregla`.** Carlos estuvo a punto de comprar
`cocheenregla.com` en OVH por 7,99 € el primer año y 13,49 €/año de
renovación, y lo dejó para otro momento. **No comprado todavía.**

Por qué ese: «tener el coche en regla» describe el servicio entero (ITV,
impuesto, etiqueta, ZBE, multas, trámites) sin atarse a ninguna vertical, y
suena serio. Segundo candidato: `papelesdelcoche`, más memorable pero con la
sombra de «sin papeles».

Disponibilidad comprobada el 28/09 (`.com` por RDAP, autoritativo; `.es` por
ausencia de NS, que es indicio fuerte pero hay que confirmarlo al pagar).
Libres en las dos extensiones: cocheenregla, papelesdelcoche,
normativadelcoche, vehiculoenregla, normativauto, reglasdelcoche,
micochelegal, tucochealdia, cocheenregla, conductorenregla, datosdelcoche.
Cogidos: cochelegal, autolegal, autonorma, enregla, autoenregla, vialibre,
luzverde, sinmultas, todoenregla, etiquetacoche, mivehiculo.

Descartado a propósito `codigocirculacion` pese a ser el de más gancho: hace
parecer que el sitio es oficial, y todo el argumento del proyecto es el
contrario.

Sobre ampliar a otros países: ni «coche» ni el `.es` valen fuera de España, pero
el activo del proyecto es el dataset español y no se transfiere. Si alguna vez
se quiere esa puerta, la decisión es `.com` (ya tomada) más carpetas por país,
no cambiar el nombre.

El procedimiento de conexión con Cloudflare está escrito paso a paso en
[docs/conectar-dominio.md](docs/conectar-dominio.md). **Lo crítico:** desactivar
el DNSSEC en OVH ANTES de cambiar los servidores de nombres, o el dominio
puede quedarse inaccesible.

### Hallazgo crítico sobre el NAP-DGT (22/09/2026)

**Los ficheros DATEX2 de la DGT NO sirven para deducir qué distintivos pueden
circular.** Cada ayuntamiento codifica el mismo XML con significados opuestos:

| Municipio | `negate` | Distintivos declarados |
|---|---|---|
| A Coruña | true | 0, ECO, C, B |
| Madrid | true | Sin distintivo |
| Bilbao | true | 0, ECO, C, B, Sin distintivo |

Si el bloque negado son los permitidos, Madrid queda al revés. Si son los
prohibidos, A Coruña queda al revés. Bilbao es absurdo en ambas lecturas.

**Decisión: no se publica ninguna regla de acceso derivada de esta fuente.**
`pipeline/zbe_nap.py` guarda la evidencia en bruto (`evidencia_sin_interpretar`)
para agilizar la verificación manual, pero las reglas solo se publican tras
leer la ordenanza. No reabrir esto salvo que la DGT normalice el formato.

Lo que sí aporta el NAP: los 45 municipios con ZBE registrada, su fuente
oficial, fecha y horarios. Es información de nivel C, publicable.

### Trampas ya pisadas (no repetir)

- **`extend_footer.html` no sirve para contenido que dependa de la página.**
  `baseof.html` del tema llama al pie con
  `partialCached "footer.html" . .Layout .Kind ...`: la clave **no incluye la
  página**, así que todas las que comparten layout reutilizan un único render.
  El menú lateral estuvo ahí y marcaba la misma entrada como actual en todo el
  sitio. La cabecera sí se cachea por página (`partialCached "header.html" . .Page`),
  así que el menú se renderiza desde `header.html`.
- **Las variables CSS solo se heredan hacia abajo.** `--ml-ancho` estaba en
  `.menu-lateral` y `.main` no es descendiente suyo: la declaración quedaba
  inválida en silencio. Las variables compartidas van en `:root`.
- **`min-width: 0` hace falta en TODOS los eslabones de una cadena flex.**
  Un elemento flex con `min-width: auto` no baja de su tamaño mínimo de
  contenido, aunque sus hijos sí puedan encogerse. En la cabecera lo tenían
  `.logo` y `.marca__texto` pero no `.marca`, que está en medio: el título no
  se recortaba y la señal del logotipo se montaba encima de la lupa en móvil.
- **PaperMod gana por especificidad en cosas que parecen nuestras.** `.main`
  y `.logo a` del tema pisan a `.main` y `.marca`. Usar `body .main` y
  `.logo a.marca`.
- **No editar contenido con `Get-Content`/`Set-Content` de PowerShell 5.1.**
  Lee como ANSI y reescribe como UTF-8: corrompe todos los acentos. Usar las
  herramientas de edición o Python.

- **Sin `timeZone` en `hugo.toml`, una ficha creada de madrugada no se
  publica.** Un `date: 2026-09-29` sin hora se interpreta como medianoche
  UTC, que en España son las 02:00. A las 00:04 hora local esa fecha está
  en el futuro, y `buildFuture = false` descarta la página **en silencio**:
  no aparece, no hay aviso, y el build termina en verde. Pasó con Granada y
  Barcelona. Resuelto con `timeZone = "Europe/Madrid"`.
- **`disableKinds` debe ir en la raíz de `hugo.toml`**, antes de cualquier cabecera
  `[tabla]`. Si va después, TOML la anida dentro de esa tabla y deja de aplicarse
  en silencio.
- **`params.env = "production"` fijo** fuerza `index, follow` en todos los builds,
  incluidas las previsualizaciones. No fijarlo: PaperMod ya usa `hugo.Environment`.
- **`public/` no se limpia sola** entre builds. Para verificar que algo dejó de
  generarse hay que borrarla antes (`Remove-Item public -Recurse -Force`).
- **JSON-LD con `jsonify` dentro de `<script>`** sale escapado como cadena e
  invisible para Google. Necesita `| safeJS`.
- **`cast.ToInt` sobre `"09"`** devuelve 0 (lo interpreta en base 0). No usar para
  aritmética de fechas.
