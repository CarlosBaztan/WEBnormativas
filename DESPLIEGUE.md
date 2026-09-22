# Despliegue

## Cloudflare Pages

El sitio se despliega solo: Cloudflare compila y publica en cada push a `master`.

### Configuración del proyecto

En el panel de Cloudflare → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**,
elige el repositorio y aplica estos ajustes:

| Ajuste | Valor |
|---|---|
| Framework preset | Hugo |
| Build command | `hugo --gc --minify` |
| Build output directory | `public` |
| Root directory | *(vacío)* |

**Variable de entorno** (pestaña *Settings → Environment variables*), imprescindible:

| Nombre | Valor |
|---|---|
| `HUGO_VERSION` | `0.166.0` |

Sin esa variable, Cloudflare usa una versión antigua de Hugo y el build falla.

### Submódulo del tema

El tema PaperMod es un submódulo de Git. Cloudflare los clona automáticamente,
pero si el build falla con un `public/` vacío o sin estilos, es que no lo hizo:
comprueba que `.gitmodules` está en el repositorio.

### baseURL

`hugo.toml` tiene `baseURL = "https://example.pages.dev/"` como marcador.
**Hay que cambiarlo por la URL real** en cuanto Cloudflare asigne el subdominio,
porque de él dependen el sitemap, las URL canónicas y los enlaces absolutos.

## Dominio propio

Decisión del 22/09/2026: se arranca en `.pages.dev` y se migra en unas dos semanas.
Mientras no haya enlaces entrantes ni indexación, la migración no cuesta nada.

**Migrar antes de empezar a buscar enlaces.** Después obligaría a un 301 sobre un
dominio joven, y ahí sí se pierde parte de lo acumulado.

Al conectar el dominio: actualizar `baseURL` en `hugo.toml` en el mismo push.

## Antes de solicitar AdSense (Fase 5)

1. Tener 20-30 páginas reales publicadas. El rechazo habitual es «contenido de poco valor».
2. Redactar las páginas de `content/legal/`, que ahora están vacías.
3. Integrar una CMP certificada por Google. La gratuita («Privacidad y mensajes»,
   dentro de AdSense) sirve, y **es obligatoria** para servir anuncios en el EEE.
4. Activar los huecos de anuncio: `adsEnabled = true` en `hugo.toml`.
5. Cargar el script de AdSense en `layouts/partials/extend_head.html`.

El orden importa: activar los anuncios antes de tener la CMP incumple el RGPD.

## Comprobaciones antes de cada push

```powershell
hugo --gc --minify              # el build no puede fallar
python pipeline/auditoria.py    # ningún dato sin verificar se publica
```
