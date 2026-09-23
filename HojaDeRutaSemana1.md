# Brief: calculadora solo Madrid + 18 páginas

Reglas vigentes: nada sin verificar se publica · máx. 900 palabras/página ·
fuente + fecha visibles · cero anuncios encima del formulario.
Estructura de toda página: respuesta directa → tabla/lista → bloque fuente.
Lo largo (perímetros, excepciones) dentro de `<details>`.

## 1. Calculadora: solo Madrid

- El selector ofrece solo municipios con `estado_dato: verificado` (hoy: Madrid).
- El resto se sigue descargando a `data/zbe.json` como `pendiente_verificacion`, sin salir a público.
- Línea bajo el selector, desde el fichero de datos (no hardcodeada): "Por ahora solo Madrid está verificada. Siguientes: Barcelona, Valencia, Sevilla."
- Madrid tiene 3 zonas: el resultado responde por zona, no una respuesta única.
- Cambiar `estado_dato` a `verificado` debe bastar para publicar un municipio. Sin tocar código.
- Test que rompa el build si un municipio publicado no tiene `codigo_ine`, `fuente_url` y `fecha_verificacion`.

## 2. Páginas

**A. Distintivos DGT (6)** — fuente: criterios de clasificación DGT. Si no estás seguro de un año o criterio, deja `{{VERIFICAR}}`. Todas enlazan a `/zbe/madrid/`.

| Ruta | Qué responde |
|---|---|
| `/etiquetas/` | Tabla comparativa de los 5 casos + cómo consultar el tuyo por matrícula |
| `/etiquetas/0-emisiones/` | Qué vehículos la llevan y qué permite |
| `/etiquetas/eco/` | Qué híbridos y GLP/GNC entran y cuáles no |
| `/etiquetas/c/` | Años y combustibles |
| `/etiquetas/b/` | Años y combustibles, y dónde ya no entra |
| `/etiquetas/sin-distintivo/` | Qué vehículos quedan fuera y qué zonas los prohíben |

**B. Madrid (3)** — fuente: Ordenanza 2/2026, de 24 de marzo (BOCM núm. 80, de 6/4/2026). Cita el artículo en cada una; enlazadas entre sí.

| Ruta | Contenido |
|---|---|
| `/zbe/madrid/` | Usa `ficha-madrid-zbe.md` tal cual. No la amplíes |
| `/zbe/madrid/distrito-centro/` | Perímetro, quién entra, horarios: industriales 0 = 24 h, ECO 7-21, C 7-15; motos B/C 7-22. Art. 23 y anexo III |
| `/zbe/madrid/plaza-eliptica/` | Sin distintivo no circula (incluido tramo A-42 interior). Excepciones: TEPMR, históricos, transporte de personas con discapacidad. Art. 24 y anexo IV |

**C. ZBE general (4)**

| Ruta | Qué responde | Fuente |
|---|---|---|
| `/zbe/` | Tabla de todos los municipios con ZBE: nombre, provincia, estado, enlace oficial y columna "¿Verificado por nosotros?". Generada desde `data/zbe.json` | MITECO |
| `/zbe/que-es/` | Qué es, umbral de 50.000 hab., desde cuándo | Ley 7/2021, RD 1052/2022 |
| `/multas/zbe/` | Importe, plazo con descuento, cómo alegar | Ley de Tráfico, arts. 76.z3), 80.1, 81 |
| `/zbe/excepciones/` | Residentes, TEPMR, históricos, reparto, emergencias | Ordenanza Madrid + régimen general |

**D. Institucionales (5)**: `/sobre/` (quién hay detrás, criterio, contacto) · `/metodologia/` (jerarquía de fuentes: boletín oficial > web oficial > prensa nunca citable; qué significa "verificado"; cada cuánto se revisa; cómo avisar de errores — esta no la despaches en cuatro líneas) · `/legal/aviso-legal/` · `/legal/privacidad/` · `/legal/cookies/`, con texto real, sin placeholders.

## 3. Orden

1 (calculadora) → A → B → C → D. Para después de cada bloque. En el bloque A, enséñame la primera página antes de hacer las otras cinco.

## 4. No hacer

No rellenar `{{VERIFICAR}}` ni campos `pendiente` · no publicar ningún municipio salvo Madrid · no citar prensa ni blogs como fuente normativa · no ampliar la ficha de Madrid.
