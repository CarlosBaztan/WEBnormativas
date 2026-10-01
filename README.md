# Coche Apto

Portal de normativa y fiscalidad del vehículo en España. Sitio estático con Hugo.

Contexto de negocio: [PLAN-NEGOCIO.md](PLAN-NEGOCIO.md) · Reglas del proyecto: [CLAUDE.md](CLAUDE.md)

## Requisitos

- **Hugo extended** ≥ 0.166.0 — `winget install Hugo.Hugo.Extended`
- **Git** ≥ 2.40 — `winget install Git.Git`

## Arrancar en local

```powershell
git clone --recurse-submodules <url-del-repo>
cd webCocheApto
hugo server
```

Abre http://localhost:1313.

Si clonaste sin `--recurse-submodules`, el tema falta:

```powershell
git submodule update --init --recursive
```

Para ver también las fichas sin verificar (drafts):

```powershell
hugo server --buildDrafts
```

## Publicar

El despliegue es automático: Cloudflare Pages compila cada push a `master`.

| Ajuste | Valor |
|---|---|
| Comando de build | `hugo --gc --minify` |
| Directorio de salida | `public` |
| Variable de entorno | `HUGO_VERSION` = `0.166.0` |

Para comprobar el build en local antes de subir:

```powershell
hugo --gc --minify
```

## Añadir una ficha de ZBE

```powershell
hugo new content zbe/nombre-municipio.md --kind zbe
```

Se crea con `estado_dato: pendiente` y `draft: true`. **Así no se publica, y es lo correcto**: el sitio no debe afirmar nada que no se haya comprobado.

Para publicarla:

1. Busca la ordenanza municipal oficial (normalmente en el BOP de la provincia).
2. Rellena `estado_zbe`, `fecha_vigor`, `etiquetas_permitidas`, `horario_restriccion` y `excepciones` con lo que diga literalmente la ordenanza.
3. Rellena la trazabilidad:
   - `fuente_nombre` — ej. `"Ordenanza municipal art. 7, BOP Zaragoza"`
   - `fuente_url` — enlace directo al documento oficial
   - `fecha_verificacion` — el día que lo comprobaste, en formato `YYYY-MM-DD`
4. Cambia `estado_dato` a `"verificado"` y `draft` a `false`.

### Si solo sabes que existe la ZBE, pero no las reglas

Deja `etiquetas_permitidas` vacío y `estado_dato` en `"pendiente"`. La ficha no se publicará.

**Nunca rellenes un campo a ojo.** Una regla inventada puede costarle 200 € a un lector, y el proyecto entero depende de que los datos sean fiables.

## Reglas duras

1. Ningún dato se publica sin verificar. `estado_dato: pendiente` ⇔ `draft: true`.
2. Ritmo de 4-6 piezas al mes. Nada de lotes masivos generados con IA.
3. Al lanzar solo se publican `zbe/` y `etiquetas/`. El resto existe como estructura vacía.
4. Cero anuncios encima del formulario de una herramienta. Solo debajo del resultado.
5. Cada ficha cita fuente oficial y fecha de verificación, visibles en la página.
6. Prioridad técnica: Core Web Vitals y accesibilidad.

## Estructura

```
content/
  zbe/          Fichas por municipio          [se publica]
  etiquetas/    Distintivos ambientales DGT   [se publica]
  datos/        Datasets abiertos (CC-BY)     [se publica]
  guias/        Contenido de apoyo            [se publica]
  impuestos/    IVTM                          [estructura, sin contenido]
  itv/          Inspección técnica            [estructura, sin contenido]
  multas/       Sanciones                     [estructura, sin contenido]
  tramites/     Gestiones DGT                 [estructura, sin contenido]
  legal/        Privacidad, cookies, contacto [se publica]
data/           JSON que alimenta las herramientas
layouts/        Overrides del tema PaperMod
static/datos/   CSV y JSON de descarga pública
themes/PaperMod Submódulo git — no editar
```

## Nota sobre OneDrive

El repositorio vive en una carpeta sincronizada con OneDrive. Si aparecen conflictos
extraños en `.git/` o en `public/`, excluye ambas carpetas de la sincronización.
