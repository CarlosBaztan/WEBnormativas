# Coche Apto: contexto del proyecto

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

**Cómo se expresa cada nivel en el front matter** (`estado_dato`):

| Nivel | `estado_dato` | `draft` | Efecto |
|---|---|---|---|
| A o B | `verificado` | `false` | Se publica, responde «¿puedo entrar?» y entra en el selector de la herramienta |
| C | `parcial` | `false` | **Se publica**, dice lo que consta y lo que no, y **no** entra en el selector |
| D | `pendiente` | `true` | No se publica |

El nivel `parcial` existe desde el 29/09/2026. Antes no había forma de publicar
un nivel C: `pendiente` obliga a `draft: true` y la ficha no salía, así que el
trabajo de comprobar que una ZBE existe se perdía. Primer caso: Benidorm, cuya
ZBE opera desde enero de 2025 pero cuyo ayuntamiento no publica de forma
legible qué distintivos quedan restringidos.

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

**Topónimos bilingües: castellano primero, lengua propia después.** Decisión
de Carlos del 30/09/2026, por el mismo motivo que la convención de títulos: no
perder ninguna de las dos búsquedas. Se publica «Gerona / Girona», «Lérida /
Lleida» y «San Sebastián / Donostia», en ese orden, porque la mayoría escribe
la forma castellana pero la oficial es la que aparece en la ordenanza, en el
NAP y en la prensa local.

**En los desplegables va solo la forma castellana, corta.** En el selector del
mapa la forma doble alarga la lista sin aportar nada: quien lo abre ya sabe qué
ciudad quiere. Además, con el nombre oficial Gerona quedaba ordenada por la i y
Lérida por la elle, donde nadie las busca.

Son dos tablas, una por sitio, y las dos están comentadas:

| Dónde | Tabla | Qué sale |
|---|---|---|
| Dataset, listado de `/zbe/`, descargas | `NOMBRES_BILINGUES` en `pipeline/zbe_nap.py` | `Gerona / Girona` |
| Mapa y selector | `NOMBRES` en `pipeline/zbe_geometria.py` | `Gerona` |

Aplica a los casos del mismo tipo que vayan saliendo. **`A Coruña` es el
siguiente**, y debería pasar a «La Coruña / A Coruña» cuando se toque. No
confundirlo con `Vitoria-Gasteiz`, que es un nombre oficial compuesto, ni con
`Palma`, donde «Palma de Mallorca» no es otra lengua sino una precisión
geográfica.

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

Al 01/10/2026. **El sitio está en producción, en `cocheapto.com`, abierto a
los buscadores y con las páginas legales publicadas.**

- [x] Investigación de nicho y competencia
- [x] Plan de negocio
- [x] Fase 1: estructura Hugo
- [x] Fase 2: herramienta «¿Puedo circular?»
- [x] Fase 3: pipeline de datos (`pipeline/zbe_nap.py`, 45 municipios)
- [x] Fase 4: GitHub y Cloudflare Workers. En producción en
      **`cocheapto.com`** (y en `www`), con certificado y caché de un año
      para lo que lleva huella. El Worker sigue llamándose `webnormativas`
      a propósito: renombrarlo crearía uno nuevo y rompería el despliegue.
- [x] Estudio de palabras clave (ver la sección de datos de búsqueda)
- [x] Mapa: gestos, pantalla completa y chinchetas por municipio. Los
      recuentos de `/mapa/` salen de `data/zbe_resumen.json`, que escribe el
      pipeline, para que no vuelvan a quedarse viejos.
- [x] Ficha de Barcelona reescrita con la ordenanza de 2023 leída en el BOPB
      (21/02/2023, CVE 202310032045), artículo por artículo. Publicada en
      `/zbe/barcelona/`.
- [x] Hoja de ruta de tres días:
      `docs/superpowers/plans/2026-09-25-hoja-de-ruta-3-dias.md`
- [x] T11: página de cámaras (`/zbe/camaras/`), con el circuito completo
      leído en la Ley de Tráfico: art. 89.2.c) (por qué la multa tarda),
      arts. 90-92 (DEV, domicilio, BOE, TESTRA) y art. 84.4 (sanciona el
      Alcalde, no la DGT). Importe y reducción cerrados: 200 € (art. 80.1),
      50 % si se paga en 20 días naturales (art. 94), sin pérdida de puntos
      (no está en el anexo II).
- [x] T12: sistema visual. Tokens en `assets/css/extended/sistema.css` y
      documentado en [docs/sistema-visual.md](docs/sistema-visual.md).
- [x] T13: accesibilidad. Ocho plantillas sin incidencias de axe-core, enlace
      para saltar al contenido y foco que entra de verdad en el panel móvil.
- [x] T14: rendimiento. `static/_headers` con caché de un año para lo que
      lleva huella, y `preconnect` a cdnjs en las páginas con mapa.
- [x] **Dominio `cocheapto.com`**, comprado y conectado el 01/10. Ver abajo.
- [x] **Fase 5: páginas legales.** Aviso legal, privacidad, cookies y
      contacto, con los datos reales del titular, enlazadas desde el pie de
      todas las páginas. Leído el art. 10 LSSI en el BOE para publicar lo que
      pide y nada más.
      **No hay banner de consentimiento, y es correcto**: el sitio no pone ni
      una cookie. Solo tres claves de almacenamiento local, las tres exentas
      por el art. 22.2 LSSI al ser servicio solicitado por el usuario. Cuando
      entre la publicidad habrá que ponerlo.
- [x] **Abierto a los buscadores** el 01/10: `noindex = false`, robots.txt en
      `Allow` y 37 URL en el sitemap. Antes se comprobó que no hubiera títulos
      ni descripciones duplicadas, que no hubiera enlaces rotos y que no
      quedaran páginas delgadas (`/guias/` estaba vacía y pasó a borrador).
- [x] **Marca: Coche Apto.** Logotipo en la cabecera, en dos versiones para
      tema claro y oscuro, y `site.Title` cambiado en todo el sitio.
- [ ] **Redirect Rule para que `www` lleve al dominio principal.** Los dos
      hosts sirven lo mismo. Los canónicos apuntan todos al dominio sin `www`,
      así que Google consolida y no penaliza, pero lo limpio es la
      redirección. Pasos en [docs/conectar-dominio.md](docs/conectar-dominio.md).
- [ ] **Early Hints** en Cloudflare, gratis. Mismo documento.
- [ ] **Solicitar AdSense.** Ya se puede: el sitio es accesible y tiene las
      legales. Lo tiene que hacer Carlos.
- [ ] **Más fichas de municipio verificadas.** 13 de 45 con ZBE registrada en
      el NAP. **Es el cuello de botella real del proyecto**: sin contenido no
      hay tráfico, y sin tráfico no hay ingresos.

### Dominio: `cocheapto.com` (comprado el 01/10/2026)

**Comprado en Cloudflare Registrar**, con renovación automática, a 10,46 $/año
de coste. `baseURL` en `hugo.toml` ya apunta ahí.

Por qué este y no otro, para no volver a debatirlo: «apto» es el veredicto de
la ITV, lo entiende cualquier conductor al instante, son nueve letras que se
dictan sin deletrear y no ata el sitio a las ZBE, que es la decisión 5. Se
descartó `tucocheapto.com` porque «tu coche apto» no es español natural (se
dice «tu coche *es* apto») y porque tres letras más se pagan cada vez que se
dice el nombre en voz alta.

Comprobado antes de comprar: cero marcas en TMview para «coche apto» y
«cocheapto», en España y en la UE. Las que hay de «APTO» a secas son de otros
sectores (una bicicleta de 3T Cycling en la clase 12, software de TLS Corp.,
centros de datos de Apto DC).

**Contrapartida conocida:** «coche apto» es descriptivo, así que sería una
marca difícil de registrar en exclusiva. Se acepta a cambio de que se entienda
sin explicar nada.

**El correo del titular es un Gmail a propósito**, no `contacto@cocheapto.com`.
Sería circular: si el dominio se queda en hold, ese correo deja de funcionar
justo cuando ICANN necesita escribir. Cambiarlo después dispara un *Change of
Registrant* con doble aprobación y 60 días de bloqueo de transferencias.

**Lo que Cloudflare NO da es buzón de correo**, solo reenvío (Email Routing).
`contacto@cocheapto.com` reenviará al Gmail. Para el art. 10 de la LSSI vale,
porque lo que exige es una dirección de contacto que funcione.

**Lección del proceso, y vale para cualquier nombre futuro: que el dominio
esté libre no significa que el nombre lo esté.** `tuguantera.com` estaba libre
y era el favorito hasta que miramos qué había al lado: `laguantera.com` es una
gestoría online de trámites de vehículos en marcha (ITV, informes de la DGT,
transferencias, distintivo ambiental, multas), con 75.000 clientes declarados
y la solicitud de marca M4297581 en la OEPM. Mismo sector, cuatro de las seis
verticales. **Antes de comprar: TMview, búsqueda del nombre en la web, y solo
después el RDAP.**

El procedimiento de conexión está en [docs/conectar-dominio.md](docs/conectar-dominio.md).

Sobre ampliar a otros países: ni «coche» ni el `.es` valen fuera de España,
pero el activo del proyecto es el dataset español y no se transfiere. Si
alguna vez se quiere esa puerta, la decisión es `.com` (ya tomada) más
carpetas por país, no cambiar el nombre.

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
- **Fijar un solo margen sobre algo que tiene `margin: auto` lo descentra.**
  El tema trae `.main { margin: auto }`. Al poner `margin-left: var(--ml-ancho)`
  para dejar sitio al menú lateral, el margen derecho se quedaba en `auto` y se
  comía todo el sobrante: en 1366 px el texto arrancaba pegado al menú y
  quedaban 327 px muertos a la derecha, en todas las páginas. **Para reservar
  el ancho de un elemento fijo se usa `padding`, no `margin`**, y los dos
  márgenes se dejan en `auto`; así el contenido queda centrado en el espacio
  libre. Depende de `box-sizing: border-box`, que el reset del tema ya aplica.
  Y al mover una columna hay que mirar quién más debería seguirla: el pie se
  centraba por su cuenta y no coincidía con el cuerpo.
- **No editar contenido con `Get-Content`/`Set-Content` de PowerShell 5.1.**
  Lee como ANSI y reescribe como UTF-8: corrompe todos los acentos. Usar las
  herramientas de edición o Python.

- **Sin `timeZone` en `hugo.toml`, una ficha creada de madrugada no se
  publica.** Un `date: 2026-09-29` sin hora se interpreta como medianoche
  UTC, que en España son las 02:00. A las 00:04 hora local esa fecha está
  en el futuro, y `buildFuture = false` descarta la página **en silencio**:
  no aparece, no hay aviso, y el build termina en verde. Pasó con Granada y
  Barcelona. Resuelto con `timeZone = "Europe/Madrid"`.
- **Renombrar una ficha rompe tres cruces, y los tres en silencio.** El slug
  de `data/zbe.json` sale del nombre del fichero XML del NAP, que la DGT pone
  a su gusto: la ZBE de Barcelona viene como `rondas-de-barcelona` y la ficha
  se publica en `/zbe/barcelona/`. Tres sitios cruzan ficha y dato y ninguno
  avisa cuando dejan de encajar: `_ficha_de()` en `zbe_geometria.py` (el mapa
  enlaza a un 404), `$verificadas` en `layouts/zbe/list.html` (la fila pierde
  el enlace y la marca de verificada) y el `data-slug` de
  `partials/mapa-municipio.html` (la ficha se queda sin mapa). Resuelto con
  `slug_nap` en el front matter y la tabla `FICHAS` del pipeline. El build
  termina en verde en los tres casos.
  Por lo mismo, **el nombre que se muestra no puede alimentar al slug**: la
  tabla de topónimos bilingües se aplica en `analizar()`, despues de calcular
  el slug, y no en `url_xml_de_recurso()` como `CORRECCIONES_NOMBRE`. Si se
  aplicara antes, `girona` pasaría a `gerona-girona` y cambiarían de golpe la
  clave de `data/zbe.json`, el nombre del fichero de caché y el slug del
  GeoJSON. Lo vigila `test_ningun_nombre_bilingue_cambia_el_slug`.
- **El GeoJSON se sirve en una URL fija, sin huella.** Al regenerarlo, el
  navegador sigue dando el anterior hasta que caduca su copia. Si una prueba
  en local no refleja un cambio del pipeline, recargar sin cache antes de
  buscar el fallo en el codigo.

- **`{{VERIFICAR}}` no es una plantilla de Hugo.** Parece una, pero Goldmark
  imprime las llaves tal cual y la nota interna acaba publicada. Estuvo cuatro
  veces a la vista en `/multas/zbe/`. Lo vigila ahora `auditoria.py`, que
  además del front matter mira el cuerpo de cada página publicada.
- **Hugo elige plantilla por sección, no por lo que la página sea.** En
  `content/zbe/` conviven fichas de municipio con artículos y con una página
  de herramienta, y las tres caían en `layouts/zbe/single.html`: los artículos
  salían coronados con «Las reglas de acceso de esta ZBE no están verificadas»
  y una tabla llena de «No consta». Resuelto con `$esFicha`, que mira `tipo`
  con `"municipio"` por defecto.
- **La hoja de Leaflet se carga DESPUÉS que la nuestra.** Trae
  `.leaflet-container a { color: #0078A8 }`, que empata en especificidad con
  `.leaflet-control-attribution a`, y a igualdad gana la última. Hace falta
  doblar la clase: `.leaflet-container .leaflet-control-attribution a`.
- **El enlace para saltar al contenido no mueve el foco por sí solo.** El
  patrón habitual (href a un id con `tabindex="-1"`) cambia la URL y desplaza
  la página, pero el siguiente tabulador vuelve al principio. Comprobado
  pulsando Intro de verdad. Necesita cinco líneas de JavaScript, y están en
  `layouts/_default/baseof.html`.
- **Un elemento en `visibility: hidden` no admite foco, y la transición de
  `visibility` retrasa cuándo deja de estarlo.** El panel del menú en móvil
  abría sin llevarse el foco dentro, y ni un `requestAnimationFrame` llegaba a
  tiempo. Se arregla por los dos lados: la transición es instantánea al abrir
  y solo espera al cerrar, y el JavaScript reintenta en `transitionend`.
- **Los fallos de teclado no salen con `click()` de prueba.** Los tres de
  arriba pasaban las comprobaciones automáticas y solo aparecieron pulsando
  teclas reales. axe-core tampoco detecta el primero: su regla `bypass` se da
  por satisfecha con que haya landmarks y encabezados.
- **No escribir `
` dentro de un heredoc de Python.** Se convierte en un
  salto de línea real y rompe el fichero generado. Usar la herramienta de
  escritura, o construirlo con `chr(10)` y `chr(92)`.
- **En TOML, una cabecera `[tabla]` se traga todo lo que venga detrás.** Abre un
  ámbito que dura hasta la siguiente cabecera, así que cualquier `clave = valor`
  escrito después pertenece a esa tabla, aunque esté al mismo nivel visual que
  el resto y aunque el fichero se lea perfectamente bien. **Esta trampa se ha
  pisado dos veces**, y la segunda fue cara:
  - `disableKinds` colocado tras una cabecera y dejó de aplicarse. Por eso va
    en la raíz de `hugo.toml`, antes de cualquier `[tabla]`.
  - El 01/10/2026 el bloque `[params.fuseOpts]` del buscador se insertó justo
    detrás de `[params]`, y los **diecisiete ajustes siguientes** quedaron
    dentro del tercer `[[params.fuseOpts.keys]]`. `[params]` pasó de 18 claves
    a 2. Las 37 páginas se desplegaron sin migas de navegación, sin enlaces de
    anterior/siguiente, con `<meta name=author>` vacío, con la descripción
    vacía en el JSON-LD y con el título del logotipo partido en
    «Coche Apto:  (Alt + H)». El build terminó en verde.

  **Regla: los ajustes sueltos de `[params]` van arriba; las tablas, al final.**
  Y como el daño no se ve leyendo el fichero (hay que parsearlo), lo vigila
  `pipeline/test_configuracion.py`.
- **Los iconos del sitio no se editan a mano.** Salen de `LogoCocheApto.png`
  por `pipeline/marca_favicon.py`, que reconstruye las tres piezas por máscaras
  de color. Reducir el PNG tal cual no vale: es un render con ruido, y a 16 px
  ese ruido se promedia y deja el coche gris. El fotograma de 16 del `.ico` es
  **distinto** de los de 32 y 48 (coche macizo, sin bujes ni ventanilla), y eso
  es deliberado. Las cuatro URL no se renombran: Google pide que la dirección
  del icono sea estable y tarda de días a semanas en releer una nueva.
  Lo vigila `pipeline/test_marca_favicon.py`.
- **`params.env = "production"` fijo** fuerza `index, follow` en todos los builds,
  incluidas las previsualizaciones. No fijarlo: PaperMod ya usa `hugo.Environment`.
- **`public/` no se limpia sola** entre builds. Para verificar que algo dejó de
  generarse hay que borrarla antes (`Remove-Item public -Recurse -Force`).
- **JSON-LD con `jsonify` dentro de `<script>`** sale escapado como cadena e
  invisible para Google. Necesita `| safeJS`.
- **`cast.ToInt` sobre `"09"`** devuelve 0 (lo interpreta en base 0). No usar para
  aritmética de fechas.
