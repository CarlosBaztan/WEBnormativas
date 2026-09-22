# WEBnormativas — contexto del proyecto

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
| [Hacienda — consulta impositiva municipal](https://serviciostelematicosext.hacienda.gob.es/SGFAL/ConsultaTipos/aspx/listado_municipiosm.aspx) | IVTM/IBI/IAE/IVTNU/ICIO por municipio, **export Excel masivo**, 2000-2025 | Pública |
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
| costerealcoche.com | ~8m | 12 | — | — |
| ibeonix.es | nuevo | 3 | — | — |

Dos de los cuatro llevan meses abandonados.

## Expectativa realista

120-450 €/mes a 18 meses (escenario medio). **Los primeros 6 meses no darán casi nada.**
El mayor riesgo del proyecto es abandonarlo en el mes cuatro.

## Estado actual

- [x] Investigación de nicho y competencia
- [x] Plan de negocio
- [x] Repo inicializado
- [x] **Fase 1 — estructura Hugo** (pendiente de revisión del usuario)
- [ ] Dominio: se arranca en `.pages.dev` y se migra en ~2 semanas (decisión del
      22/09/2026). Coste cero mientras no haya enlaces ni indexación.
      **Migrar ANTES de empezar a buscar enlaces.**
- [ ] Fase 2 — herramienta "¿Puedo circular?"
- [ ] Fase 3 — pipeline de datos
- [ ] Fase 4 — GitHub + Cloudflare Pages
- [ ] Fase 5 — pre-AdSense (legales + CMP)

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
