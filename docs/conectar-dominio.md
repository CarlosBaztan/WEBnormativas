# Conectar el dominio de OVH con Cloudflare

Guía paso a paso. Los pasos marcados **[Carlos]** necesitan tus contraseñas,
así que los tienes que hacer tú. Los marcados **[Claude]** los hago yo.

Tiempo real de trabajo: unos quince minutos repartidos. Lo que más tarda es
esperar a que se propaguen los servidores de nombres, y eso es esperar, no
trabajar.

**Antes de empezar, lo único que puede salir mal:** cambiar los servidores de
nombres con el DNSSEC activado. La documentación de Cloudflare lo dice sin
rodeos: *«If your domain has DNSSEC active, you must turn it off at your
registrar before replacing nameservers»*. Si se hace al revés, el dominio
puede quedarse inaccesible. Va resuelto en la fase 2, paso 1.

---

## Fase 0 · Terminar la compra en OVH **[Carlos]**

- [ ] Confirmar que el precio de renovación que aparece es el que esperas.
      En la pantalla que me pasaste: 7,99 € el primer año y 13,49 €/año desde
      septiembre de 2027. Está bien para un `.com`.
- [ ] Dejar **DNSSEC** y la **cuenta de correo**, que vienen incluidas. La del
      correo hace falta para el aviso legal: el art. 10 de la LSSI obliga a
      publicar un contacto, y así no expones tu correo personal.
- [ ] Decir que no a cualquier otro añadido: hosting, certificado SSL,
      constructor de webs, copias de seguridad. Todo eso ya lo cubre Cloudflare
      y es gratis.
- [ ] **Activar la renovación automática.** Perder el dominio por un descuido
      dentro de dos años, con el sitio ya posicionado, es el peor final
      posible.

---

## Fase 1 · Añadir el dominio en Cloudflare **[Carlos]**

- [ ] Entrar en [dash.cloudflare.com](https://dash.cloudflare.com) con la
      cuenta que ya usas para el sitio.
- [ ] Buscar la opción de añadir un dominio (**Add a domain** u **Onboard a
      domain**, según cómo lo tengan traducido ese día).
- [ ] Escribir el dominio **sin `www` y sin `https://`**. Solo
      `cocheenregla.com`.
- [ ] Elegir el plan **Free**. No hace falta nada más para este sitio.
- [ ] Cloudflare escanea los registros DNS que ya existen en OVH y te los
      muestra. **Revisa que estén los registros `MX`**, que son los del correo.
      Si no aparecen, avísame antes de seguir: sin ellos la cuenta de correo
      deja de recibir en cuanto se haga el cambio.
- [ ] Al final te da **dos servidores de nombres**, con pinta de
      `algo.ns.cloudflare.com`. Cópialos, que son los de la fase siguiente.

---

## Fase 2 · Cambiar los servidores de nombres en OVH **[Carlos]**

**El orden importa.** Primero se desactiva el DNSSEC, y solo después se tocan
los servidores de nombres.

- [ ] En el panel de OVH, ir a tu dominio.
- [ ] Buscar **DNSSEC** y **desactivarlo**. Esperar a que la operación termine
      y el panel confirme que está desactivado. No seguir hasta entonces.
- [ ] Ir a la sección de **servidores DNS** y elegir modificarlos.
- [ ] Sustituir los de OVH por los dos de Cloudflare de la fase anterior.
- [ ] Guardar.

---

## Fase 3 · Esperar **[nadie]**

Cloudflare avisa por correo cuando la zona pasa a **Active**. Suele tardar de
minutos a un par de horas, aunque su documentación dice que puede llegar a 24.

No hay nada que hacer mientras tanto. La web sigue funcionando en
`webnormativas.bi-ia-carlosbaz.workers.dev` todo el rato.

Cuando llegue ese correo, **dímelo**.

---

## Fase 4 · Conectar el dominio al Worker **[Carlos]**

Un minuto, y solo se puede hacer cuando la zona esté activa. Cloudflare exige
que la zona sea tuya y esté en su panel: no vale con apuntar un registro desde
fuera.

- [ ] En Cloudflare: **Workers & Pages** → el proyecto **webnormativas**.
- [ ] **Settings** → **Domains & Routes** → **Add** → **Custom Domain**.
- [ ] Escribir `cocheenregla.com` y confirmar.
- [ ] Repetir con `www.cocheenregla.com`, para que las dos formas funcionen.

Cloudflare crea los registros DNS y emite el certificado él solo. No hay que
configurar nada de HTTPS.

---

## Fase 5 · Lo que hago yo **[Claude]**

- [ ] Actualizar `baseURL` en `hugo.toml` al dominio nuevo.
- [ ] Reconstruir y desplegar.
- [ ] Comprobar de verdad, no fiarme del panel: que los servidores de nombres
      son los de Cloudflare, que el certificado es válido, que el sitio
      responde en el dominio nuevo y que las URL internas apuntan donde deben.
- [ ] Revisar que los registros `MX` del correo siguen en pie.
- [ ] Volver a activar el DNSSEC, ahora desde Cloudflare.

---

## Lo que NO se hace todavía

**El `noindex` se queda puesto.** Tener el dominio no es motivo para abrirlo a
Google: eso toca el domingo, cuando haya ocho municipios verificados, el mapa
y las herramientas. Abrirlo ahora haría que Google conociera el sitio con una
sola ciudad, y la primera impresión de un dominio nuevo conviene cuidarla.

Está en `hugo.toml`, `noindex = true`, con el porqué escrito al lado.
