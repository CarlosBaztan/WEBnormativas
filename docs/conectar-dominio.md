# Conectar el dominio con Cloudflare

Guía paso a paso. Los pasos marcados **[Carlos]** necesitan tus contraseñas,
así que los tienes que hacer tú. Los marcados **[Claude]** los hago yo.

**Comprando el dominio en el propio Cloudflare, esta guía se queda en nada:**
diez minutos y sin ningún paso que pueda salir mal.

## Por qué comprarlo en Cloudflare cambia tanto

La versión anterior de este documento daba por hecho que el dominio se
compraba en OVH, y tenía un aviso en rojo al principio: cambiar los
servidores de nombres con el DNSSEC activado puede dejar el dominio
inaccesible. Ese riesgo **desaparece**, junto con la mitad del procedimiento.

Comprobado en la documentación de Cloudflare el 30/09/2026:

- *«All domains acquired via Cloudflare Registrar use Cloudflare nameservers»*.
  Nacen ya apuntando a Cloudflare, así que **no hay cambio de servidores de
  nombres, no hay que tocar el DNSSEC y no hay que esperar a que se propague
  nada**. Las tres fases que daban miedo se caen.
- *«Cloudflare Registrar does not mark up domain prices at all. Cloudflare
  ensures customers only pay the price charged by registries and ICANN for
  domain registration and renewal»*. **Vende a precio de coste, y también al
  renovar.** En OVH la renovación subía a 13,49 €/año desde el segundo año;
  aquí se queda en lo que cobre el registro del `.com`, que es de donde salen
  esos 9,50 €.
- Incluye sin coste la **ocultación de los datos del titular** en el WHOIS, el
  **DNSSEC en un clic** y el certificado SSL.

**La contrapartida, que es pequeña pero hay que saberla:** mientras el dominio
esté en Cloudflare Registrar no se pueden poner los servidores de nombres de
otro proveedor. Para este proyecto da igual, porque el sitio vive en
Cloudflare de todas formas. Si algún día quisieras moverlo, se transfiere el
dominio a otro registrador y punto, salvo durante los primeros 60 días, que es
un bloqueo de ICANN y lo tienen todos los registradores.

---

## Fase 0 · Comprar **[Carlos]**

- [ ] En el panel de Cloudflare: **Domain Registration** → **Register Domains**.
- [ ] Buscar `papelesdelcoche.com` y comprobar el precio antes de pagar.
- [ ] **Activar la renovación automática.** Perder el dominio por un descuido
      dentro de dos años, con el sitio ya posicionado, es el peor final
      posible y el más tonto.
- [ ] Los datos del titular son reales (ICANN lo exige), pero la ocultación en
      el WHOIS viene puesta, así que no quedan públicos.

Al terminar, el dominio ya está en tu cuenta, con su zona creada y apuntando a
Cloudflare. **No hay fase 1, 2 ni 3.**

---

## Fase 1 · Conectar el dominio al Worker **[Carlos]**

Un minuto.

- [ ] En Cloudflare: **Workers & Pages** → el proyecto **webnormativas**.
- [ ] **Settings** → **Domains & Routes** → **Add** → **Custom Domain**.
- [ ] Escribir `papelesdelcoche.com` y confirmar.
- [ ] Repetir con `www.papelesdelcoche.com`, para que las dos formas funcionen.

Cloudflare crea los registros DNS y emite el certificado él solo. No hay que
configurar nada de HTTPS.

---

## Fase 2 · El correo del aviso legal **[Carlos]**

Hace falta una dirección de contacto en el dominio: el **artículo 10 de la
LSSI** obliga a publicarla, y AdSense no aprueba un sitio sin aviso legal.

Cloudflare **no da buzones**, solo reenvío. Su Email Routing *«route[s]
incoming emails sent to your domain to existing mailboxes»*, o sea que
`contacto@papelesdelcoche.com` acabaría en tu Gmail de siempre. Para cumplir
la LSSI vale: lo que exige es una dirección de contacto que funcione.

- [ ] En Cloudflare: **Email** → **Email Routing** → activarlo.
- [ ] Crear la dirección `contacto@papelesdelcoche.com` y apuntarla a tu Gmail.
- [ ] Confirmar el correo de verificación que llega a esa cuenta.

Cloudflare añade solo los registros MX, SPF y DKIM.

**Si alguna vez necesitas responder desde esa dirección**, y no solo recibir,
eso ya no lo cubre el reenvío: hace falta configurar «Enviar como» en Gmail
con un relé SMTP. No es urgente y no bloquea nada.

---

## Fase 3 · Lo que hago yo **[Claude]**

- [ ] Actualizar `baseURL` en `hugo.toml` al dominio nuevo.
- [ ] Reconstruir y desplegar.
- [ ] Comprobar de verdad, no fiarme del panel: que el certificado es válido,
      que el sitio responde en el dominio nuevo y en el `www`, y que las URL
      internas apuntan donde deben.
- [ ] Activar el DNSSEC desde Cloudflare, que ahora es un clic y sin riesgo,
      porque el registrador y el DNS son el mismo.

---

## Lo que NO se hace todavía

**El `noindex` se queda puesto.** Tener el dominio no es motivo para abrirlo a
Google: eso toca cuando haya municipios verificados suficientes, el mapa y las
herramientas terminadas. Abrirlo ahora haría que Google conociera el sitio a
medias, y la primera impresión de un dominio nuevo conviene cuidarla.

Está en `hugo.toml`, `noindex = true`, con el porqué escrito al lado.
