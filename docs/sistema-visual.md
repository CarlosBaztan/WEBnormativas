# Sistema visual

Las decisiones de diseño del sitio, tomadas una vez y escritas aquí para no
volver a decidirlas. Si algo de esto se contradice con lo que hay en el CSS,
el CSS manda y este documento está viejo: avísame.

Todos los tokens viven en **[`assets/css/extended/sistema.css`](../assets/css/extended/sistema.css)**.
Los demás ficheros de `extended/` los consumen y no deciden nada por su cuenta.

## Por qué existe

Antes de septiembre de 2026 había **26 tamaños de letra distintos**, diez de
ellos entre 12,5 y 15,2 píxeles, **31 valores de espaciado** y **10 de
interlineado**. Nadie distingue 14,08 de 14,4 píxeles, pero el conjunto se
percibe como desorden, y el desorden en un sitio cuyo argumento es la
fiabilidad cuesta credibilidad.

## Orden de carga

PaperMod concatena `assets/css/extended/*.css` **por nombre de fichero**,
después de su propio CSS. Orden actual:

```
distintivos → herramienta → mapa → menu-lateral → normativa → pagina-zbe → sistema
```

`sistema.css` entra el último a propósito: sus declaraciones de `:root` ganan
a cualquier otra de la misma especificidad, que es lo que se quiere de un
fichero de tokens. **Lo que no se puede hacer ahí es escribir reglas normales**
(`.clase { ... }`) esperando que las pise otro fichero, porque desde ahí ya no
pisa nadie.

Dos trampas ya pisadas que conviene recordar:

- **Las variables CSS solo se heredan hacia abajo.** `--ml-ancho` estuvo en
  `.menu-lateral` y `.main` no es descendiente suyo: la declaración quedaba
  inválida en silencio. Por eso todo token va en `:root`.
- **El orden dentro de un fichero importa.** Añadir
  `.mapa-zbe { position: relative }` *después* de `.mapa--ampliado` dejó la
  pantalla completa con `height: 0`. Una propiedad nueva se añade a la regla
  que ya existe, no al final del fichero.

## Escala tipográfica

**Aviso que se cobró varias horas:** `1rem` son 16 px (el `<html>`), pero el
cuerpo de PaperMod es de 18 px. Por eso `0.9rem` no era el 90 % del texto, era
el 80 %. Los valores están elegidos por su resultado en píxeles.

| Token | Valor | Píxeles | Para qué |
|:---|:---|---:|:---|
| `--txt-xs` | 0.8125rem | 13 | Fuente, fecha de verificación, atribución |
| `--txt-sm` | 0.9375rem | 15 | Notas, ayudas de formulario, tablas |
| `--txt-md` | 1.0625rem | 17 | Cuerpo |
| `--txt-lg` | 1.1875rem | 19 | Rótulo de bloque, `h4` |
| `--txt-xl` | 1.375rem | 22 | `h3` y titular de la respuesta |
| `--txt-2xl` | 1.625rem | 26 | `h2` de artículo |
| `--txt-3xl` | 2.125rem | 34 | `h1` |

Interlineado: `--lh-titular` 1.2, `--lh-corto` 1.45 (fichas, tablas, notas,
celdas), `--lh-lectura` 1.65 (párrafos largos).

**Adopción a 1 de octubre de 2026:** 82 usos de `var(--txt-*)` frente a 4
literales, y los cuatro son `1em` o `0.8em`, que son relativos a propósito.

## Espaciado

Múltiplos de 4 px: `--sp-1` (4 px), `--sp-2` (8), `--sp-3` (12), `--sp-4` (16),
`--sp-5` (20), `--sp-6` (24), `--sp-8` (32), `--sp-12` (48).

**Adopción parcial y a propósito.** Hay 71 usos de `var(--sp-*)` y todavía
unos 60 literales. No se han convertido todos, y la razón no es pereza: buena
parte son ajustes ópticos de valores que la escala de 4 px no puede expresar
(`0.35rem`, `0.45rem`, `0.15rem`), afinados a ojo sobre el resultado. Forzarlos
a la escala cambiaría maquetados que hoy están bien a cambio de nada que el
visitante note. Si se tocan, que sea al reescribir ese bloque por otro motivo.

## Cajas

| Token | Valor | Nota |
|:---|:---|:---|
| `--caja-radio` | 8px | |
| `--caja-borde` | `var(--tertiary)` (#d6d6d6) | En oscuro, `#4a4c52` |
| `--caja-acento` | `var(--content)` | 15:1 en claro, 12:1 en oscuro |

**El origen del problema.** `--border` del tema es `#eee`, y las páginas de
tipo *list* (la portada y `/zbe/`) llevan de fondo `--code-bg`, que es
`#f5f5f5`. Un borde `#eee` sobre `#f5f5f5` da **1,06:1**: no se ve. Quedaban
los rellenos y los márgenes de cinco cajas, o sea el ruido, sin agrupar nada,
o sea sin jerarquía. En oscuro pasaba lo mismo con `#333` sobre `#1d1e20`.

## Colores de estado

Cuatro parejas fondo/texto/línea, con variante para tema oscuro:

| Estado | Token | Significado |
|:---|:---|:---|
| Verde | `--nv-ok-*` | Verificado: la ordenanza está leída |
| Ámbar | `--nv-warn-*` | Aviso, pendiente de revisión |
| Rojo apagado | `--nv-stop-*` | Sin verificar |
| Neutro | `--nv-neutral-*` | Informativo |

## Paleta del mapa

Estos tres colores **no son decorativos**: son el único sitio donde el mapa
dice si puedes fiarte de una zona.

| Token | Color | Significado |
|:---|:---|:---|
| `--mapa-verificado` | `#d6006e` magenta | La ordenanza está leída |
| `--mapa-parcial` | `#d35400` naranja | Consta la zona, no sus reglas |
| `--mapa-pendiente` | `#7209b7` morado | Solo consta que existe |
| `--mapa-suelo` | `#f2efe9` | El color del suelo en las teselas de OSM |
| `--mapa-relleno` | 35% | Opacidad del relleno del polígono |

**Por qué estos tonos y no otros.** Los anteriores eran verde, ámbar y gris,
que es justo la paleta del mapa base de OpenStreetMap: los parques son verdes,
las carreteras ámbar y el suelo urbano gris. Las zonas se confundían con el
fondo. Estos tres no aparecen en el mapa base.

**Una sola fuente.** Estaban escritos en cuatro sitios: las tres muestras de la
leyenda y los dos ficheros de JavaScript del mapa, con un comentario que decía
«si cambian allí, cambian aquí». Ahora el JavaScript los lee con
`getComputedStyle` de estas variables. Cada fichero de mapa conserva un valor
de reserva por si la hoja de estilos no ha llegado cuando arranca el script:
sin él, la variable viene vacía y Leaflet pinta las zonas de negro sin avisar.
**`pipeline/test_estilos.py` vigila que ese respaldo no se quede atrás.**

**La muestra de la leyenda se pinta sobre `--mapa-suelo`, no sobre el fondo de
la página**, y por eso es idéntica en tema claro y oscuro. Es lo correcto por
dos motivos: enseña exactamente lo que se ve en el mapa, cuyas teselas no
cambian con el tema del sitio, y evita que el morado quede en 1,94:1 sobre el
panel oscuro.

## Contraste medido

Medido el 1 de octubre de 2026 con `getComputedStyle` sobre los elementos
reales, en los dos temas. Mínimo exigible: **4,5:1** para texto normal
(WCAG 1.4.3) y **3:1** para elementos gráficos (WCAG 1.4.11).

| Elemento | Claro | Oscuro |
|:---|---:|---:|
| Texto del cuerpo | 16,48 | 9,57 |
| Verde, verificado | 8,14 | 10,36 |
| Ámbar, aviso | 8,33 | 10,39 |
| Rojo, sin verificar | 8,96 | 8,76 |
| Neutro | 10,33 | 9,33 |

Paleta del mapa, como elemento gráfico sobre los fondos donde aparece:

| Color | Blanco | Suelo OSM | Parque OSM |
|:---|---:|---:|---:|
| Magenta | 5,14 | 4,48 | 4,41 |
| Naranja | 4,17 | 3,63 | 3,57 |
| Morado | 8,61 | 7,50 | 7,38 |

**El naranja se cambió por esto.** Era `#ff6d00` y daba **2,82:1** sobre
blanco, por debajo del mínimo. `#d35400` sube a 4,17 y sigue siendo naranja a
la vista.

Queda un caso por debajo de 3:1 y se deja a propósito: el naranja **sobre el
azul del agua** de OpenStreetMap da 2,60. Las ZBE se dibujan sobre suelo
urbano, no sobre el mar, y oscurecer más el naranja lo acercaría al marrón de
las carreteras, que es el problema que esta paleta vino a resolver.

**Y el color nunca va solo.** Cada entrada de la leyenda lleva su texto al
lado («Reglas verificadas», «Zona confirmada, reglas sin verificar», «Solo
consta que la zona existe»), así que nada depende de distinguir tonos.

## Logotipo y cabecera

La marca es el título del sitio (`.marca__texto`) más una señal de tráfico
dibujada en SVG en línea (`partials/logo-senal.html`). Sin fuentes externas y
sin imágenes: cero peticiones de red añadidas.

`--cabecera-alto` (3,25rem) y `--ml-ancho` (16rem) viven en `menu-lateral.css`
porque son medidas de maquetación, no de identidad, pero están en `:root` por
la misma regla de herencia de siempre.

Dos trampas de la cabecera:

- **`height` y no `min-height`.** `--cabecera-alto` también posiciona el menú
  lateral; si la cabecera creciera por su cuenta se solaparían.
- **`min-width: 0` hace falta en todos los eslabones de la cadena flex.** Lo
  tenían `.logo` y `.marca__texto` pero no `.marca`, que está en medio: el
  título no se recortaba y la señal se montaba encima de la lupa en móvil.

## Qué no hay, y no por olvido

- **Sin fuentes externas.** Se usa la pila del sistema. Una fuente web son dos
  peticiones bloqueantes y un salto de maquetación.
- **Sin animaciones ni transiciones** más allá de lo que trae el tema.
- **Sin framework de CSS.** 2.400 líneas propias frente a los 60 KB mínimos de
  cualquier framework, en un sitio que se monetiza con publicidad y donde cada
  kilobyte compite con el anuncio.
