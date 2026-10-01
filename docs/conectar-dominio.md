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

## Fase 0 · Comprar **[Carlos]** · HECHO el 01/10/2026

- [x] Comprado `cocheapto.com` en Cloudflare Registrar, con renovación
      automática activada (10,46 $/año, que es el precio de coste).
- [ ] **Verificar el correo del titular.** Llega un correo a la dirección del
      registrante y hay que pulsarlo. Por exigencia de ICANN, **si no se
      verifica en 15 días se pone el dominio en hold y le cambian los
      servidores de nombres por un servidor de aparcamiento**, o sea que la
      web se cae. Es el fallo más tonto y más caro de todo este documento.

**Sobre el correo del titular, para cuando se quiera cambiar:** no es el
correo corporativo del sitio, es el contacto de titularidad ante ICANN, y no
sale público porque la ocultación del WHOIS viene incluida. Cambiarlo después
no es editar un campo: dispara un *Change of Registrant* que tienen que
aprobar la dirección vieja y la nueva, se cancela solo si nadie aprueba en
siete días, y al aceptarlo **el dominio queda bloqueado para transferencias
60 días**.

Por eso ahí va un Gmail y no `contacto@cocheapto.com`: sería circular. Si
algún día el dominio se queda en hold, ese correo dejaría de funcionar justo
cuando ICANN necesita escribir para arreglarlo.

Al terminar, el dominio ya está en tu cuenta, con su zona creada y apuntando a
Cloudflare. **No hay fase 1, 2 ni 3.**

---

## Fase 1 · Conectar el dominio al Worker **[Carlos]**

Un minuto.

- [ ] En Cloudflare: **Workers & Pages** → el proyecto **webnormativas**.
- [ ] **Settings** → **Domains & Routes** → **Add** → **Custom Domain**.
- [ ] Escribir `cocheapto.com` y confirmar.
- [ ] Repetir con `www.cocheapto.com`, para que las dos formas funcionen.

Cloudflare crea los registros DNS y emite el certificado él solo. No hay que
configurar nada de HTTPS.

---

## Fase 2 · El correo del aviso legal **[Carlos]**

Hace falta una dirección de contacto en el dominio: el **artículo 10 de la
LSSI** obliga a publicarla, y AdSense no aprueba un sitio sin aviso legal.

Cloudflare **no da buzones**, solo reenvío. Su Email Routing *«route[s]
incoming emails sent to your domain to existing mailboxes»*, o sea que
`contacto@cocheapto.com` acabaría en tu Gmail de siempre. Para cumplir
la LSSI vale: lo que exige es una dirección de contacto que funcione.

- [ ] En Cloudflare: **Email** → **Email Routing** → activarlo.
- [ ] Crear la dirección `contacto@cocheapto.com` y apuntarla a tu Gmail.
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

## Pendiente · Que `www` redirija al dominio principal **[Carlos]**

**No corre prisa y no bloquea nada.** Apuntado el 01/10/2026 para hacerlo con
calma.

**El problema.** Con `cocheapto.com` y `www.cocheapto.com` conectados los dos
como dominio personalizado del Worker, el sitio **responde igual en las dos
direcciones**: no son la misma página servida desde un sitio, son dos copias
idénticas en dos direcciones distintas. Lo correcto es que una sea la buena y
la otra lleve a ella.

**Por qué no urge.** Las etiquetas canónicas de todas las páginas apuntan ya a
`https://cocheapto.com/` sin `www`, porque es lo que dice `baseURL`, así que
un buscador sabría cuál es la buena. Y además el `noindex` sigue puesto, o sea
que ahora mismo no hay ningún buscador mirando. **Lo que sí conviene es
hacerlo antes de quitar el `noindex`**, para que Google no llegue a ver nunca
las dos.

**Cómo se hace** (gratis, incluido en el plan, unos dos minutos):

- [ ] En el panel de Cloudflare, entrar en el dominio `cocheapto.com` (no en
      el proyecto de Workers: en el dominio).
- [ ] **Rules** → **Redirect Rules** → **Create rule**.
- [ ] Ponerle un nombre reconocible, por ejemplo `www al dominio principal`.
- [ ] Condición: que el **Hostname** sea igual a `www.cocheapto.com`.
- [ ] Acción: redirección **dinámica**, para conservar la ruta. La expresión
      es `concat("https://cocheapto.com", http.request.uri.path)`.
- [ ] Código de estado: **301** (permanente). **Preserve query string**
      activado, para no perder los parámetros de la URL.

**Comprobarlo después, que es la parte que se olvida:** pedir
`https://www.cocheapto.com/zbe/madrid/` y ver que contesta un 301 hacia
`https://cocheapto.com/zbe/madrid/`, con la ruta intacta. Si redirige a la
portada y se come el `/zbe/madrid/`, la redirección está puesta como estática
en vez de dinámica.

---

## Pendiente · Dos ajustes del panel de Cloudflare **[Carlos]**

Apuntados el 01/10/2026 al leer el correo de registro, que los ofrece los dos
en la misma pantalla. **Uno hay que activarlo y el otro NO**, y el que no es
el que suena mejor.

### Early Hints: SÍ, cuando abramos a Google

Es gratis y en el plan Free. Permite que el navegador empiece a descargar la
hoja de estilos antes de que llegue el HTML entero, lo que adelanta el pintado.
Encaja con lo que ya se hizo en la T14 (caché de un año para lo que lleva
huella, `preconnect` a cdnjs).

No corre prisa mientras el `noindex` esté puesto, porque la velocidad importa
cuando hay visitantes. Está en **Speed** → **Optimization** dentro del dominio.

### Bot Fight Mode: NO

Cloudflare lo ofrece como protección gratuita y describe que gestiona el
tráfico de bots **«incluidos los bots de IA»**. Ahí está el problema: parte de
la estrategia del proyecto es que ChatGPT, Perplexity, Claude y compañía
puedan leer el sitio para citarlo como fuente. Activar eso sería bloquear
justo a los visitantes que más interesan, y además en silencio: no hay aviso,
simplemente dejan de aparecer las citas.

**Si alguna vez hay que frenar bots**, el criterio es a la inversa del
habitual: bloquear raspadores de contenido comercial, nunca los rastreadores
de los buscadores ni los de las IA generativas.

Tampoco hacen falta los planes Pro (20 $/mes) ni Business (200 $/mes) que
ofrece ese mismo correo. El sitio es estático, pesa menos de 10 KB por página
comprimida y lo sirve la red de Cloudflare. No hay nada que optimizar ahí.

---

## Lo que NO se hace todavía

**El `noindex` se queda puesto.** Tener el dominio no es motivo para abrirlo a
Google: eso toca cuando haya municipios verificados suficientes, el mapa y las
herramientas terminadas. Abrirlo ahora haría que Google conociera el sitio a
medias, y la primera impresión de un dominio nuevo conviene cuidarla.

Está en `hugo.toml`, `noindex = true`, con el porqué escrito al lado.
