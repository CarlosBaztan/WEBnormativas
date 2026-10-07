---
title: "Dataset: municipios con Zona de Bajas Emisiones en España"
description: "Listado consolidado de los municipios con ZBE registrada en el Punto de Acceso Nacional de la DGT, con su fuente oficial y fecha. Descarga libre en CSV y JSON."
date: 2026-09-22
lastmod: 2026-09-22
draft: false

# Las dos claves que lee layouts/partials/schema.html para el JSON-LD del
# Dataset. Antes esto se llamaba dataset_licencia y dataset_formatos, que no
# las lee nadie: el Dataset se publicaba sin `distribution`, o sea sin decirle
# a Google que el dato se puede descargar.
licencia: "https://creativecommons.org/licenses/by/4.0/"
descargas:
  - nombre: "Municipios con ZBE (CSV)"
    formato: "text/csv"
    url: "/datos/zbe.csv"
  - nombre: "Municipios con ZBE (JSON, con la evidencia en bruto)"
    formato: "application/json"
    url: "/datos/zbe.json"
fecha_verificacion: "2026-09-22"
estado_dato: "verificado"
fuente_nombre: "Punto de Acceso Nacional de la DGT, Zonas de Bajas Emisiones (DATEX2 v3)"
fuente_url: "https://nap.dgt.es/dataset/zonas-de-bajas-emisiones"
---

Listado consolidado de los **45 municipios españoles con Zona de Bajas Emisiones registrada** en el Punto de Acceso Nacional de la DGT, con el enlace al fichero oficial de cada uno y la fecha en que su ayuntamiento lo publicó.

## Descargas

- [zbe.csv](/datos/zbe.csv): una fila por municipio
- [zbe.json](/datos/zbe.json): incluye la evidencia en bruto sin interpretar

Licencia **CC-BY 4.0**. Puedes reutilizarlo libremente citando como fuente a la Dirección General de Tráfico y, si te viene bien, a esta página.

## Qué contiene, y qué no

Lo primero que hay que mirar de cada fila es la columna **`confianza`**, porque es la que dice cuánto vale.

**Para los 45 municipios**, sea cual sea su confianza:

- Que existe una ZBE registrada oficialmente.
- El enlace directo al fichero DATEX2 de la DGT.
- La fecha en que el ayuntamiento publicó ese fichero.
- Los horarios de restricción declarados en ese fichero.
- La evidencia en bruto de las condiciones por distintivo, **sin interpretar**.

**Para los que tienen `confianza: oficial`**, que son aquellos cuya ordenanza hemos leído entera:

- **Qué distintivos pueden entrar** (`etiquetas_permitidas`).
- El horario que fija la ordenanza, que no siempre coincide con el del fichero de la DGT (`horario_verificado`).
- El artículo concreto en que lo pone (`articulo`).
- El nombre de la ordenanza, el boletín en que se publicó y su enlace (`ordenanza_nombre`, `ordenanza_boletin`, `ordenanza_url`).
- La fecha en que lo comprobamos (`fecha_verificacion`) y el enlace a la ficha (`ficha_url`).
- Si el municipio tiene varias zonas con reglas distintas, cada una con las suyas (`zonas_verificadas`).

**De los que tienen `confianza: pendiente_verificacion` no se puede deducir qué distintivos entran.** Ahí la columna va vacía a propósito, y el porqué es lo siguiente.

Un aviso para quien procese el fichero: **`etiquetas_permitidas` vacía en una fila `oficial` no es un olvido.** O el municipio tiene varias zonas con reglas distintas, y entonces están en `zonas_verificadas`, o su ZBE todavía no restringe ningún distintivo, como pasa hoy en Valencia.

## Por qué no publicamos los distintivos permitidos de los demás

Los ficheros de la DGT sí traen condiciones de acceso por distintivo. El problema es que **cada ayuntamiento las codifica de forma distinta**, usando la misma estructura XML para decir cosas opuestas.

Tres ejemplos reales, comprobados el 22 de septiembre de 2026 sobre los 45 ficheros:

| Municipio | `negate` | Distintivos declarados |
|:---|:---|:---|
| A Coruña | `true` | 0, ECO, C, B |
| Madrid | `true` | Sin distintivo |
| Bilbao | `true` | 0, ECO, C, B, Sin distintivo |

Si ese bloque negado fueran los **permitidos**, en Madrid solo podrían circular los vehículos sin distintivo, que es falso. Si fueran los **prohibidos**, en A Coruña estarían prohibidos todos los distintivos, que también es falso. Y Bilbao resulta absurdo en las dos lecturas: o no restringe a nadie, o lo prohíbe todo.

No hay una regla automática que acierte en los tres. Cualquier interpretación algorítmica acertaría en unos municipios y diría **justo lo contrario de la verdad** en otros.

Como equivocarse aquí le cuesta al lector una multa de 200 €, preferimos no publicarlo. Estamos leyendo las ordenanzas municipales una a una; cada vez que verificamos una, su ficha pasa a mostrar las reglas con el artículo citado y la fecha de comprobación, **y esa lectura entra también en este fichero**, con su artículo, su boletín y su fecha.

Es decir: lo que falta aquí no es lo que no se puede saber, es lo que todavía no hemos leído.

## Metodología

1. Se descarga el catálogo de ZBE del NAP de la DGT y se recorren sus 45 recursos.
2. De cada fichero DATEX2 v3 se extraen municipio, horarios, fecha de publicación y las condiciones por distintivo **en bruto**.
3. Si la estructura no se puede interpretar sin ambigüedad, el municipio se marca como `pendiente_verificacion` y no se publica ninguna afirmación sobre sus reglas.
4. El proceso es idempotente y deja registro de los cambios entre ejecuciones.

El código del pipeline está en el repositorio del proyecto, en `pipeline/zbe_nap.py`.

## Limitaciones

- La lista refleja los municipios **registrados en el NAP**, no todos los que tienen ZBE. Desde el 1 de enero de 2026 están obligados todos los de más de 50.000 habitantes, así que faltan bastantes.
- Las fechas de publicación de los ayuntamientos van de 2024 a 2025: algunos ficheros llevan tiempo sin actualizarse en origen.
- Un municipio ausente **no significa que no tenga ZBE**.

Si detectas un error, [escríbenos](/legal/contacto/) y lo corregimos citando la fuente.
