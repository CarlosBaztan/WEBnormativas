# Plan de negocio: portal de normativa y fiscalidad del vehículo en España

**Fecha:** 22 de septiembre de 2026
**Autor:** Carlos (Zaragoza) — analista de datos, ADE + máster en BI
**Stack:** Hugo + Cloudflare Pages + GitHub · Presupuesto: dominio (~10-20 €/año)

> **Nota sobre las cifras.** Todo dato marcado *(est.)* es una estimación cualitativa, no un dato medido. Los volúmenes de búsqueda y los CPC deben validarse en Google Keyword Planner antes de tomar decisiones. Los datos de competidores sí son reales: se obtuvieron el 21-22/09/2026 mediante consulta RDAP, análisis de sitemaps, inspección de código fuente y Semrush.

---

## 1. Selección del nicho

### 1.1. El nicho elegido

**Normativa, fiscalidad y trámites del vehículo en España**, con las **Zonas de Bajas Emisiones (ZBE)** como punto de entrada.

No es "automoción" ni "coches". Es deliberadamente más estrecho: el conjunto de **obligaciones legales, fiscales y administrativas** que afectan a un conductor español, y que están dispersas entre 8.100 ordenanzas municipales, 17 normativas autonómicas y varios organismos estatales.

La tesis central es esta: **el producto no es la calculadora, es el dataset.** Cualquiera programa una fórmula en una tarde; nadie consolida 151 ordenanzas municipales de ZBE. La ventaja competitiva está en el trabajo de datos, que es precisamente el perfil profesional del propietario.

### 1.2. Nivel de competencia: **MEDIO**

Esta evaluación no es una impresión, sale de un análisis real de los competidores directos:

| Competidor | Antigüedad | Páginas | AdSense | Dom. referencia | Visitas/mes | Estado |
|---|---|---|---|---|---|---|
| sacacuentas.es | ~12 meses | 91 | Sí | 119 | **28** | Parado desde mar-2026 |
| simuloo.com | ~12 meses (reg. 02/09/2025) | 150 | Sí | 100+ | **~4.000** | Parado desde may-2026 |
| costerealcoche.com | ~8 meses (reg. 28/01/2026) | 12 | Sí | — | — | Activo |
| ibeonix.es | Muy reciente | **3** | Sí | — | — | Activo (lastmod 21/09/2026) |

**Lecturas clave:**

1. **Nadie está consolidado.** Ninguno supera los 12 meses de vida ni las 150 páginas. No hay autoridad acumulada de años que resulte inalcanzable.
2. **La barrera real son los enlaces.** Los dos con datos tienen 100+ dominios de referencia. sacacuentas duplicó los suyos (+109%) en poco tiempo, patrón típico de enlaces comprados — y con 28 visitas/mes, no le sirvieron de nada.
3. **El patrón de abandono es la señal más importante.** Dos de cuatro llevan meses sin tocarse. La interpretación optimista es que dejan hueco; la realista es que **montaron el sitio, no ganaron lo suficiente y lo dejaron.**
4. **Ninguno tiene datos propios.** Todos son calculadoras de fórmula genérica. Ninguno ha tocado ZBE, IVTM municipal ni normativa.

**Conclusión:** competencia fácil de superar en calidad, difícil de superar en enlaces. Por eso la estrategia debe ganar enlaces por mérito y no por compra.

### 1.3. Potencial de tráfico

*(est. — validar en Keyword Planner)*

El dato duro que sí está verificado es el tamaño del mercado, y es excepcional:

- Desde el **1 de enero de 2026**, todos los municipios de más de 50.000 habitantes están **legalmente obligados** a tener ZBE activa (RD 1052/2022 y Ley 7/2021).
- A febrero de 2026: **56 ciudades con ZBE plenamente operativa**.
- Previsión para el resto del año: **151 municipios**, que afectan a **33 millones de personas** (del 45,5% al 66% de la población española).
- Sanción estándar por acceso indebido: **200 €**.

Traducido: 33 millones de personas con un coche, una norma que no entienden y una multa de 200 € si se equivocan. Ese es el tamaño de la audiencia potencial.

Estimación de tráfico alcanzable en 18 meses con ejecución correcta: **15.000-40.000 visitas/mes** *(est.)*. Es una horquilla amplia porque depende casi por completo de la capacidad de conseguir enlaces.

### 1.4. Intención de búsqueda del usuario

El usuario tipo no busca información: busca **una decisión y tranquilidad**. Es un perfil con tres rasgos muy favorables:

- **Ansioso.** Teme una multa concreta y cuantificada. Eso eleva muchísimo la tasa de clic y el tiempo en página.
- **Con datos propios.** Su pregunta depende de *su* coche y *su* ciudad. Google AI Overviews no puede responderla sin la herramienta.
- **Con intención comercial adyacente.** Quien revisa la etiqueta de su coche está a un paso de plantearse cambiarlo, asegurarlo o pasar la ITV.

Tipos de consulta dominantes:
- **Navegacional-local:** "ZBE Zaragoza horarios", "puedo entrar en Madrid Central con etiqueta B"
- **Transaccional-fiscal:** "cuánto pago de impuesto de circulación en [municipio]"
- **Trámite:** "cómo pedir la etiqueta ambiental", "cuándo me toca la ITV"

---

## 2. Justificación del nicho

### 2.1. Por qué funciona con AdSense

AdSense es una de las capas de ingreso, y su rendimiento depende mucho de la sección:

| Sección | CPC de anunciantes *(est.)* | Por qué |
|---|---|---|
| ZBE / etiquetas | Medio | Concesionarios, renting, movilidad eléctrica |
| IVTM / fiscalidad | Medio-alto | Gestorías, comparadores de seguros |
| ITV / multas | **Alto** | Seguros, abogados de tráfico, talleres |
| Compra de vehículo | **Muy alto** | Seguros, financiación, concesionarios |

El sector asegurador del automóvil es de los que más pujan en España *(est.)*, y este contenido es adyacente a él: quien mira normativa del coche es exactamente el público que un comparador de seguros quiere.

**RPM estimado:** 2-8 € por cada 1.000 páginas vistas *(est.)*, con las secciones de multas e ITV en la parte alta de la horquilla.

**Ventaja específica de este nicho:** el usuario ansioso consume varias páginas por sesión (mira su ciudad, luego su etiqueta, luego el impuesto). Más páginas vistas por visita significa más impresiones, y eso mejora el RPM efectivo respecto a una calculadora de una sola página.

### 2.2. Estacionalidad

- **ZBE:** picos fuertes en cada entrada en vigor municipal. Durante 2026-2027 habrá decenas de activaciones escalonadas, cada una generando un pico local. **Es estacionalidad a favor**, repartida en el tiempo.
- **IVTM:** muy marcada. El periodo voluntario de pago se concentra según municipio, típicamente entre marzo y junio.
- **ITV:** plana todo el año.
- **Multas y trámites:** plana, con repunte en operaciones salida (verano, festivos).

La combinación de las cuatro **aplana la curva anual**, que es exactamente lo que se busca para un ingreso publicitario estable.

### 2.3. Tendencia: creciente y con calendario legal

Este es el argumento más sólido del plan. No se apuesta a que el interés crezca: **está legislado que crezca.**

- 2026: de 56 a ~151 municipios obligados.
- Población afectada: del 45,5% al 66%.
- Normativa en revisión (hay un proyecto de modificación del RD 1052/2022 en información pública), lo que generará una nueva oleada de búsquedas.

**Riesgo asociado:** lo que la ley da, la ley lo quita. Un cambio de gobierno podría relajar las ZBE. Se mitiga porque el sitio cubre además IVTM, ITV y trámites, que no dependen de esa política concreta.

---

## 3. Subnichos y arquitectura de categorías

```
/                     Herramienta principal: "¿Puedo circular?"
/zbe/                 Zonas de Bajas Emisiones (núcleo)
  /zbe/<municipio>/    Ficha por ciudad
/etiquetas/           Distintivos ambientales DGT
/impuestos/           IVTM y fiscalidad municipal
/itv/                 Inspección técnica
/multas/              Sanciones y recursos
/tramites/            Gestiones con la DGT
/datos/               Datasets abiertos descargables
/guias/               Contenido de apoyo
```

**Justificación de cada categoría:**

| Categoría | Por qué está | Papel |
|---|---|---|
| **ZBE** | Único hueco verificadamente libre; crecimiento legislado | Captación y diferenciación |
| **Etiquetas** | Puerta de entrada natural: para saber si puedes circular, primero necesitas tu etiqueta | Conversión hacia la herramienta |
| **Impuestos** | Dataset de Hacienda disponible; nadie lo ha explotado a fondo | Segundo foso de datos |
| **ITV** | Volumen constante y CPC alto; variación por CCAA | Ingresos estables |
| **Multas** | El CPC más alto del conjunto *(est.)* | Rentabilidad |
| **Trámites** | Volumen alto, competencia baja, enlaza con todo lo anterior | Tráfico de soporte |
| **Datos** | Los datasets abiertos son el imán de enlaces | Autoridad y SEO |

**Principio rector:** la estructura existe desde el día uno, pero **solo se publica ZBE + Etiquetas** hasta tener tracción. Abrir siete categorías a la vez diluye la autoridad temática — y sacacuentas.es, con seis categorías y 28 visitas/mes, es la demostración empírica de ese error.

---

## 4. Plan de contenido

**Advertencia metodológica importante:** este listado es una hoja de ruta de **18 meses**, no un lote a generar de golpe. Publicar 80 páginas generadas con IA en pocas semanas es exactamente el patrón que Google penaliza como *scaled content abuse*. El ritmo recomendado es de 4-6 piezas al mes, cada una verificada contra fuente oficial.

### Fase 1 — ZBE (meses 1-6) · 28 piezas

**Fichas de ciudad** (prioridad por población; cada una con reglas, horarios, mapa, excepciones, fuente y fecha de verificación):

| # | Título | Intención |
|---|---|---|
| 1 | ZBE Madrid 2026: qué coches pueden entrar y en qué horario | Navegacional-local |
| 2 | ZBE Barcelona: zonas, restricciones y multas actualizadas | Navegacional-local |
| 3 | ZBE Valencia: calendario de entrada en vigor y vehículos afectados | Navegacional-local |
| 4 | ZBE Sevilla: mapa de la zona y etiquetas permitidas | Navegacional-local |
| 5 | ZBE Zaragoza: qué cambia y a quién afecta | Navegacional-local |
| 6 | ZBE Málaga: restricciones de acceso por distintivo | Navegacional-local |
| 7 | ZBE Bilbao: horarios y excepciones para residentes | Navegacional-local |
| 8 | ZBE Palma: normativa municipal y sanciones | Navegacional-local |
| 9 | ZBE Murcia: fechas clave y vehículos excluidos | Navegacional-local |
| 10 | ZBE A Coruña: delimitación y régimen de acceso | Navegacional-local |
| 11 | ZBE Pamplona: qué vehículos quedan fuera | Navegacional-local |
| 12-25 | *(resto de capitales por población)* | Navegacional-local |

**Contenido transversal de ZBE:**

| # | Título | Intención |
|---|---|---|
| 26 | Multa por entrar en una ZBE: cuánto es y cómo recurrirla | Transaccional |
| 27 | Lista completa de ciudades con ZBE en España (actualizada) | Informacional |
| 28 | Excepciones a las ZBE: residentes, discapacidad, vehículos históricos | Informacional |

### Fase 2 — Etiquetas DGT (meses 3-8) · 10 piezas

| # | Título | Intención |
|---|---|---|
| 29 | Qué etiqueta ambiental le corresponde a mi coche según año y combustible | **Herramienta** |
| 30 | Etiqueta B: qué coches la tienen y dónde pueden circular | Informacional |
| 31 | Etiqueta C: restricciones reales por ciudad | Informacional |
| 32 | Etiqueta ECO: ventajas fiscales y de acceso | Informacional |
| 33 | Etiqueta 0 emisiones: qué vehículos la obtienen | Informacional |
| 34 | Coches sin etiqueta: dónde puedes circular todavía | Informacional |
| 35 | Cómo pedir la etiqueta ambiental: pasos y precio | Trámite |
| 36 | Mi coche no tiene etiqueta asignada: qué hacer | Resolución |
| 37 | Etiquetas ambientales para motos y ciclomotores | Informacional |
| 38 | Diferencias entre etiqueta ambiental y clasificación europea Euro | Informacional |

### Fase 3 — IVTM (meses 6-12) · 16 piezas

| # | Título | Intención |
|---|---|---|
| 39 | Calculadora del impuesto de circulación por municipio | **Herramienta** |
| 40 | Impuesto de circulación 2026: qué es y cómo se calcula | Informacional |
| 41 | Municipios más caros y más baratos en impuesto de circulación | **Datos propios** |
| 42 | Bonificación del IVTM para coches eléctricos por municipio | **Datos propios** |
| 43 | Caballos fiscales: qué son y cómo saber los de tu coche | Informacional |
| 44 | Exención del IVTM por discapacidad: requisitos | Trámite |
| 45 | IVTM para vehículos históricos: bonificaciones | Informacional |
| 46 | Cuándo se paga el impuesto de circulación en cada municipio | **Datos propios** |
| 47 | Qué pasa si no pagas el impuesto de circulación | Informacional |
| 48-54 | *(fichas de IVTM por capital de provincia)* | Navegacional-local |

### Fase 4 — ITV, multas y trámites (meses 9-18) · 26 piezas

| # | Título | Intención |
|---|---|---|
| 55 | Cuándo me toca la ITV según matrícula y año | **Herramienta** |
| 56 | Precio de la ITV por comunidad autónoma | **Datos propios** |
| 57 | Qué revisan en la ITV: lista completa | Informacional |
| 58 | ITV desfavorable: plazos para volver a pasarla | Resolución |
| 59 | Multa por ITV caducada: importe y consecuencias | Transaccional |
| 60 | Cómo recurrir una multa de tráfico paso a paso | Trámite |
| 61 | Plazos para pagar una multa con descuento del 50% | Informacional |
| 62 | Puntos del carné: cuántos tengo y cómo consultarlos | Trámite |
| 63 | Cambio de titularidad de un vehículo: coste y pasos | Trámite |
| 64 | Dar de baja un coche: temporal y definitiva | Trámite |
| 65 | Impuesto de matriculación: cuándo se paga y cuánto | Informacional |
| 66 | Homologar una reforma en el coche: qué necesitas | Trámite |
| 67-80 | *(ampliación por subtema y variantes autonómicas)* | Mixta |

---

## 5. Estrategia SEO

### 5.1. Tipo de keywords

**Long tail con modificador local.** Es el núcleo de la estrategia y encaja con las tres restricciones del proyecto: baja competencia, resistencia a AI Overviews e imposibilidad de comprar enlaces.

Patrón objetivo: `[trámite/norma] + [ciudad/CCAA] + [año o condición]`

Se evita deliberadamente la cabecera genérica ("mejor coche", "seguro de coche barato"): son términos donde compiten portales con presupuestos de millones.

### 5.2. Arquitectura de enlazado: hub and spoke

- Cada categoría tiene una **página pilar** (ej. `/zbe/`) que enlaza a todas sus fichas.
- Cada **ficha de ciudad** enlaza de vuelta al pilar, a la herramienta y a las ciudades limítrofes.
- La **herramienta principal** enlaza a la ficha del resultado que devuelve.
- **Enlace cruzado entre verticales**: la ficha de ZBE Zaragoza enlaza al IVTM de Zaragoza y a la ITV en Aragón. Esto multiplica las páginas vistas por sesión, que es justo lo que mejora el RPM de AdSense.

### 5.3. Estrategia de enlaces entrantes (la parte crítica)

Es el punto donde fallan los competidores y donde se decide el proyecto. No se pueden comprar (presupuesto 0, y además es arriesgado). Hay que ganarlos:

1. **Publicar los datasets en `/datos/`** en CSV y JSON con licencia abierta. Un periodista que escribe sobre ZBE necesita la lista consolidada; si es la única que existe, cita la fuente.
2. **Notas de datos periodísticas**: "Los 10 municipios con el impuesto de circulación más caro de España". Material que los medios locales reproducen.
3. **Contribuir a datos.gob.es** con el dataset consolidado.
4. **Wikipedia**: los artículos sobre ZBE necesitan fuentes actualizadas.
5. **Foros y comunidades de conductores**: presencia útil, no promocional.

**Ritmo de publicación:** 4-6 piezas/mes. Sostenible con pocas horas semanales y muy por debajo del umbral que dispara las alarmas de contenido masivo.

---

## 6. Monetización

La estrategia es **apilar capas**, no elegir una. Cada euro suma y cada capa tiene un momento óptimo de activación.

### 6.1. Capa 1 — AdSense

**Cuándo:** solicitar en el mes 2-3, con 20-30 páginas reales publicadas y páginas legales completas (privacidad, aviso legal, cookies, contacto). El motivo habitual de rechazo es "contenido de poco valor", que afecta a sitios de menos de 15-20 páginas.

**Posiciones recomendadas:**

| Posición | Prioridad | Nota |
|---|---|---|
| Justo **debajo del resultado** de la herramienta | **Máxima** | El usuario acaba de obtener su respuesta: máxima atención y máxima predisposición comercial |
| Dentro del contenido, tras el primer bloque | Alta | Formato in-article |
| Barra lateral fija en escritorio | Media | |
| Final de artículo | Media | Multiplex funciona bien aquí |
| Anclado inferior en móvil | Media | Rinde bien, pero vigilar Core Web Vitals |

**Lo que no hacer:** anuncios encima del formulario de la herramienta. Rompen la experiencia, hunden la conversión y comprometen el CLS. El usuario debe obtener su respuesta primero.

**Rendimiento esperado:** RPM de 2-8 € *(est.)*, con ITV y multas en la franja alta.

### 6.2. Capa 2 — Afiliación y leads

Es la capa de mayor valor por visita, pero requiere un sitio ya presentable: las redes valoran diseño, audiencia y frescura del contenido antes de aceptarte.

| Fase | Programas accesibles |
|---|---|
| Meses 0-3 | Amazon Afiliados (fácil, paga poco: ~3% en accesorios) |
| Meses 3-6 | Alta en Awin/Tradedoubler; recambios, neumáticos, talleres |
| Meses 6-12 | Seguros y comparadores — los que de verdad pagan |

**Encajes naturales:** tras calcular el IVTM → comparador de seguros. Tras consultar la ITV → taller o recambios. Tras descubrir que el coche no puede entrar en la ZBE → renting, eléctricos, financiación.

*(Nota verificada: se localizó el programa de afiliación de Rastreator para México, no se pudo confirmar el de España. Hay que preguntárselo directamente.)*

### 6.3. Capa 3 — Ingresos futuros

Activables solo con tracción demostrada:
- **Contenido patrocinado** de concesionarios o aseguradoras locales.
- **API de pago** del dataset de ZBE/IVTM para gestorías, aseguradoras o apps de movilidad. Con el dataset ya construido, el coste marginal es casi nulo. Es la vía con mejor margen a largo plazo.
- **Venta del dominio**: un sitio consolidado en este nicho es un activo vendible.

### 6.4. Estimación de ingresos por tráfico

*(est. — combinando las tres capas)*

| Visitas/mes | AdSense | Afiliación/leads | **Total mensual** |
|---|---|---|---|
| 1.000 | 3-10 € | 0-15 € | **5-25 €** |
| 5.000 | 15-50 € | 20-80 € | **35-130 €** |
| 15.000 | 45-150 € | 75-300 € | **120-450 €** |
| 40.000 | 120-400 € | 200-800 € | **320-1.200 €** |

La afiliación supera a AdSense a partir de cierto volumen porque el tráfico es muy cualificado — pero AdSense empieza a generar antes y no depende de que ningún anunciante te acepte. Por eso van las dos.

---

## 7. Coste de contenido

### 7.1. Coste de mercado (referencia)

| Concepto | Rango en España *(est.)* |
|---|---|
| Precio por palabra, redactor generalista | 0,03-0,06 €/palabra |
| Precio por palabra, redactor especializado en legal/fiscal | 0,08-0,15 €/palabra |
| Artículo de 1.500 palabras, especializado | 120-225 € |
| **Lanzamiento de 50 artículos** | **6.000-11.000 €** |

### 7.2. El modelo real de este proyecto

**Coste en efectivo: ~0 €.** Claude genera borradores y herramientas; el propietario verifica contra fuente oficial y publica.

**Coste real: tiempo de verificación.** Y no es opcional ni delegable, por dos razones:

1. **Es el producto.** El valor diferencial es que los datos están verificados y fechados. Sin verificación, el sitio es uno más de los cuatro competidores.
2. **Es la defensa contra la penalización.** Contenido generado a escala y sin valor añadido es exactamente lo que Google castiga. La verificación humana y las fuentes citadas son lo que lo convierte en otra cosa.

**Estimación de esfuerzo:** 1-2 horas de verificación por ficha de ciudad. A 4-6 piezas/mes, entre 6 y 12 horas mensuales. Compatible con jornada completa.

**Gasto total del proyecto:** dominio, 10-20 €/año. Hosting, repositorio y herramientas, 0 €.

---

## 8. Proyección de ingresos

Escenarios anclados en datos reales de competidores: simuloo.com alcanzó ~4.000 visitas/mes en 12 meses con 150 páginas y más de 100 dominios de referencia.

### Escenario conservador (probabilidad estimada: 45%)

| Mes | Situación | Ingresos/mes |
|---|---|---|
| 1-3 | 20-30 páginas, sin tráfico | 0 € |
| 4-6 | AdSense aprobado, ~500 visitas | 2-8 € |
| 7-12 | ~2.000 visitas | 15-60 € |
| 13-18 | ~4.000 visitas | 40-130 € |

Equivale a igualar al mejor competidor actual. **Primer cobro de AdSense (umbral de 70 €) hacia el mes 12-16.**

### Escenario medio (probabilidad estimada: 35%)

| Mes | Situación | Ingresos/mes |
|---|---|---|
| 4-6 | ~1.000 visitas | 5-25 € |
| 7-12 | ~6.000 visitas, dataset citado un par de veces | 50-180 € |
| 13-18 | ~15.000 visitas | 120-450 € |

Requiere que la estrategia de datasets funcione y genere enlaces editoriales.

### Escenario optimista (probabilidad estimada: 20%)

| Mes | Situación | Ingresos/mes |
|---|---|---|
| 7-12 | ~15.000 visitas, dataset de referencia en el sector | 120-450 € |
| 13-18 | ~40.000 visitas | 320-1.200 € |
| 18+ | Vía API/B2B abierta | +variable |

Requiere que uno de los datasets se convierta en la fuente citada por medios cuando hay una oleada de ZBE.

### Escalabilidad

El proyecto escala bien por tres motivos:
1. **Coste marginal casi nulo**: sitio estático, hosting gratuito.
2. **Los datasets se reutilizan**: el trabajo hecho para ZBE alimenta ITV, IVTM y seguros.
3. **El perfil de vehículo del usuario sirve para todas las herramientas futuras.**

Y tiene un techo claro: es un mercado nacional, en español, de un sector concreto. No es un proyecto de crecimiento ilimitado.

---

## 9. Ejemplo práctico

### 9.1. Dominio

Criterio acordado: **neutro y ampliable**, que no ate el proyecto a ZBE (una normativa que puede cambiar) ni a un solo vertical.

**Candidatos** (disponibilidad por comprobar):
- `normativacoche.es`
- `reglasdelcoche.es`
- `vehiculolegal.es`
- `conducirlegal.es`
- `datoscoche.es`

A evitar: `zbe-algo.es` (se queda obsoleto si cambia la normativa) y nombres con marcas registradas.

### 9.2. Estructura inicial de lanzamiento

```
Home
 └── Herramienta "¿Puedo circular?"  ← el producto central
      · Perfil de vehículo (tipo, combustible, año) → etiqueta DGT
      · Selector de municipio
      · Resultado documentado con fuente y fecha

/zbe/              12-15 fichas de ciudad
/etiquetas/        6-8 piezas
/datos/            Dataset ZBE en CSV/JSON, licencia abierta
/guias/            4-5 piezas de apoyo
/legal/            Privacidad, aviso legal, cookies, contacto
```

### 9.3. Cómo se ve una ficha bien hecha

> **ZBE Zaragoza**
> Estado: **Activa** desde 01/03/2026
> Vehículos permitidos: etiquetas 0, ECO y C
> Horario de restricción: L-V, 7:00-20:00
> Excepciones: residentes, PMR, vehículos históricos
>
> *Fuente: Ordenanza municipal art. 7, BOP Zaragoza 12/03/2026 · [Ver ordenanza]*
> *Verificado el 21/09/2026*

Ese bloque de fuente y fecha es simultáneamente el control de riesgo, la señal de calidad para Google y el motivo por el que un periodista te cita. Ningún competidor lo tiene.

---

## 10. Conclusión

### 10.1. ¿Merece la pena?

**Sí, con la expectativa correcta.**

Lo que este proyecto **no** es: una vía para ganar dinero serio con AdSense. La investigación de competidores lo desmiente con claridad — el mejor del nicho genera del orden de 15-50 €/mes *(est.)* tras un año de trabajo y más de 100 enlaces.

Lo que este proyecto **sí** es:
- Un activo digital construido sobre un foso real (datos consolidados que nadie tiene).
- Con un mercado en crecimiento **legislado**, no especulativo.
- Con coste en efectivo prácticamente nulo.
- Con múltiples vías de monetización apilables.
- Que aprovecha exactamente la ventaja profesional del propietario.

Objetivo razonable a 18 meses: **120-450 €/mes**. Más, si el dataset se convierte en referencia.

### 10.2. Riesgos principales

| Riesgo | Gravedad | Mitigación |
|---|---|---|
| **No conseguir enlaces** | **Alta** | Es el riesgo que mata el proyecto. Los datasets abiertos son la única vía viable sin presupuesto |
| **Cambio político en ZBE** | Media | Diversificar hacia IVTM, ITV y trámites, que no dependen de esa norma |
| **Publicar un dato erróneo** | Media | Modelo de niveles de confianza: no publicar lo no verificado |
| **Abandono por desánimo** | **Alta** | Es lo que le pasó a dos de cuatro competidores. Los primeros 6 meses no darán casi nada |
| **Penalización por contenido masivo** | Baja | Ritmo de 4-6 piezas/mes con verificación humana |
| **Que un competidor copie el dataset** | Media | Es público, así que se copiará. La defensa es la frescura: quien actualiza primero, manda |

### 10.3. Recomendación final

Adelante, con tres condiciones:

1. **Empezar estrecho.** Solo ZBE y etiquetas hasta los 6 meses. La tentación de abrir siete categorías es el error que hundió a sacacuentas.es.
2. **Tratar los datasets como el producto, no como un accesorio.** Son la única fuente de enlaces gratuitos disponible y, por tanto, lo único que separa este proyecto del montón de calculadoras abandonadas.
3. **Asumir el calendario real.** Seis meses sin apenas ingresos. Quien no lo acepte de partida, abandona en el mes cuatro — como dos de los cuatro competidores analizados.

El mayor riesgo de este proyecto no es la competencia, ni Google, ni la normativa.

Es abandonarlo en el mes cuatro.

---

## Anexo — Fuentes de datos verificadas

| Fuente | Contenido | Licencia | Verificado |
|---|---|---|---|
| [NAP-DGT](https://nap.dgt.es/dataset?license_id=cc-by&res_format=DATEX2V3&tags=ZBE) | Geometría y restricciones de ZBE (DATEX2V3); cobertura parcial | **CC-BY** | 22/09/2026 |
| [Mapa ZBE MITECO](https://www.miteco.gob.es/en/calidad-y-evaluacion-ambiental/temas/movilidad/zonas_de_bajas_emisiones_en_espana.html) | Listado oficial de municipios y estado de implantación | Pública | 22/09/2026 |
| [Consulta impositiva municipal (Hacienda)](https://serviciostelematicosext.hacienda.gob.es/SGFAL/ConsultaTipos/aspx/listado_municipiosm.aspx) | IVTM, IBI, IAE, IVTNU, ICIO por municipio. **Exportable a Excel en masa**, serie 2000-2025 | Pública | 21/09/2026 |
| [API de carburantes (MITECO)](https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestres/) | Precios de todas las gasolineras, actualización horaria | Pública | 22/09/2026 |
| [DGT en cifras](https://www.dgt.es/menusecundario/dgt-en-cifras/) | Parque de vehículos y matriculaciones (ficheros de ancho fijo) | Pública | 22/09/2026 |
| [RD 1052/2022](https://www.boe.es/buscar/doc.php?id=BOE-A-2022-22689) | Marco legal de las ZBE | Pública | 22/09/2026 |

**Nota legal:** el [art. 13 de la LPI](https://www.iberley.es/legislacion/articulo-13-ley-propiedad-intelectual) excluye de la propiedad intelectual las disposiciones legales y reglamentarias y los actos y acuerdos de organismos públicos. Las ordenanzas municipales son libremente reproducibles. *(No es asesoramiento jurídico.)*
