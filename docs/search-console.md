# Google Search Console

Qué hay que hacer para dar de alta `cocheapto.com` en Search Console, qué
parte está ya resuelta y qué tiene que hacer Carlos con su cuenta de Google.

Search Console **no pone ninguna cookie en la web**: se verifica con un
registro DNS o con una etiqueta en el `<head>`. Por eso no hace falta banner
de consentimiento ni tocar las páginas legales. Es lo contrario que Google
Analytics, que sí instala cookies y arrastra todo eso detrás.

## Lo que ya está listo (comprobado el 02/10/2026)

| Requisito | Estado |
|---|---|
| `robots.txt` permite el rastreo | `User-agent: * / Allow: /` |
| Sitemap declarado en `robots.txt` | `https://cocheapto.com/sitemap.xml` |
| Sitemap accesible | HTTP 200, 37 URL, todas en `cocheapto.com` |
| Las 37 URL responden | las 37 en HTTP 200 y sin `noindex` |
| Canónicos | todos al ápex, también los que sirve `www` |
| `noindex` global | desactivado (`noindex = false` en `hugo.toml`) |

O sea que no hay nada que arreglar en la web antes de darla de alta.

## Qué tipo de propiedad elegir: **Dominio**

Search Console ofrece dos tipos y la diferencia importa aquí:

- **Propiedad de dominio** (`cocheapto.com`): cubre el ápex, `www`, `http` y
  `https`, todo en una. Se verifica con un registro TXT en el DNS.
- **Prefijo de URL** (`https://cocheapto.com/`): cubre solo esa combinación
  exacta. Haría falta una propiedad aparte para `www`.

**Aquí toca la de dominio**, por una razón concreta: `www.cocheapto.com` y
`cocheapto.com` sirven los dos el mismo contenido con HTTP 200, porque la
regla de redirección sigue pendiente. Los canónicos apuntan todos al ápex, así
que Google consolida y no hay penalización, pero con una propiedad de dominio
se ven los dos hosts sin tener que crear dos propiedades ni esperar a la
redirección.

Además el DNS está en Cloudflare, que es donde se compró el dominio, así que
añadir el TXT son dos minutos.

## Pasos (los hace Carlos, son en su cuenta de Google)

1. Entrar en <https://search.google.com/search-console> con su cuenta.
2. **Añadir propiedad** y elegir la columna de la izquierda, **Dominio**.
3. Escribir `cocheapto.com`, sin `https://` y sin `www`.
4. Google da un registro TXT del estilo
   `google-site-verification=XXXXXXXXXXXXXXXXXXXXXXXX`. **Copiarlo entero.**
5. En Cloudflare: el dominio `cocheapto.com` → pestaña **DNS** → **Add
   record**:
   - **Type:** `TXT`
   - **Name:** `@` (significa el dominio raíz)
   - **Content:** el valor que dio Google, pegado tal cual
   - **TTL:** Auto
6. Guardar, volver a Search Console y pulsar **Verificar**. Cloudflare propaga
   en segundos, así que normalmente verifica a la primera. Si falla, esperar
   unos minutos y reintentar: el registro tarda en verse desde fuera.
7. Ya dentro, en el menú lateral: **Sitemaps** → escribir la **URL
   completa**, `https://cocheapto.com/sitemap.xml` → **Enviar**.

   **Ojo aquí, que es el paso donde falla todo el mundo.** En una propiedad de
   Dominio el campo NO lleva el dominio escrito delante, porque la propiedad
   cubre el ápex, el `www`, `http` y `https` a la vez y Google no puede
   adivinar a cuál te refieres. Si escribes solo `sitemap.xml` responde
   «Dirección de sitemap no válida». En las propiedades de prefijo de URL sí
   sale el dominio delante del campo y ahí basta la ruta; de ahí viene la
   confusión, y de ahí venía la instrucción equivocada que tenía este
   documento el 02/10/2026.

**No borrar el registro TXT después.** Google lo vuelve a comprobar cada
cierto tiempo y, si no lo encuentra, retira la verificación.

## Alternativa si el DNS da problemas: la etiqueta en el HTML

Verifica solo `https://cocheapto.com/`, no `www`, pero sirve de apaño.

En el paso 4, elegir el método **Etiqueta HTML**. Google da algo así:

```html
<meta name="google-site-verification" content="XXXXXXXXXXXX" />
```

Hace falta **solo el valor de `content`**. Va en `hugo.toml`, dentro de
`[params]` y ANTES de cualquier cabecera `[params.loquesea]` (ver la trampa de
TOML anotada en CLAUDE.md):

```toml
[params.analytics.google]
  SiteVerificationTag = "XXXXXXXXXXXX"
```

`layouts/partials/head.html` ya la emite si existe, y no emite nada si no
existe. Comprobado el 02/10/2026 compilando con un valor de prueba.

Después, desplegar y pulsar **Verificar** en Search Console.

## Qué mirar cuando empiecen a llegar datos

Tarda de días a un par de semanas en tener algo. Cuando lo tenga:

- **Rendimiento**: qué consultas traen gente, cuántas impresiones y clics, y
  en qué posición media sale cada página. **Esto es lo que no da ninguna otra
  herramienta**, y es lo que de verdad hace falta aquí: saber por qué palabras
  nos encuentran y cuáles están en la página 2, que son las que con un retoque
  suben a la 1.
- **Indexación de páginas**: cuántas de las 37 ha indexado y por qué ha
  descartado el resto, si descarta alguna.
- **Experiencia en la página**: Core Web Vitals con datos de visitantes
  reales, no de laboratorio.
