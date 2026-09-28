---
title: "Política de privacidad"
description: "Qué datos trata esta web, cuáles no, y qué derechos tienes. Escrita en claro y ajustada a lo que el sitio hace realmente."
date: 2026-09-23
draft: false
---

*Última actualización: 23 de septiembre de 2026*

Esta política describe lo que **esta web hace realmente hoy**, no un texto genérico copiado de otro sitio. Si cambia, cambiará también esta página y su fecha.

## Lo importante, primero

- **No te pedimos ningún dato personal.** No hay registro, ni formularios de contacto con campos obligatorios, ni suscripción.
- **Los datos de tu vehículo no salen de tu navegador.** Ni se envían, ni se almacenan en ningún servidor.
- **No hacemos perfiles** ni seguimiento entre sitios.

## Los datos de tu vehículo

Cuando usas la herramienta para consultar si puedes circular, introduces el tipo de vehículo, el combustible y el año de matriculación.

Esos datos **se procesan en tu propio navegador**, con código que se ejecuta en tu dispositivo. No viajan a ningún servidor: no llegan a nosotros en ningún momento.

Para no tener que repetirlos, se guardan en el **almacenamiento local** de tu navegador (`localStorage`). Eso significa:

- Se quedan **en tu dispositivo**, no en nuestros sistemas.
- **No son accesibles** para nosotros ni para terceros.
- Puedes **borrarlos cuando quieras**, con el botón «Borrar mis datos» de la propia herramienta, o limpiando los datos del sitio desde tu navegador.

Al no salir de tu equipo, no hay tratamiento de datos personales por nuestra parte en esta función.

## Quién trata los datos

<!-- PENDIENTE: completar con la identificación del responsable antes de lanzar. -->
El responsable del sitio, cuya identificación figura en el **[aviso legal](/legal/aviso-legal/)**.

## Datos que se tratan por el hecho de visitar la web

Como en cualquier sitio, el servidor que la sirve registra datos técnicos para funcionar y protegerse de ataques: dirección IP, tipo de navegador, páginas solicitadas y momento de la visita.

El alojamiento lo presta **Cloudflare**, que actúa como encargado del tratamiento. Puedes consultar su [política de privacidad](https://www.cloudflare.com/privacypolicy/).

La base jurídica es el **interés legítimo** en mantener el servicio disponible y seguro.

## Publicidad y medición

<!-- Actualizar cuando se activen anuncios o analítica. Ver DESPLIEGUE.md, fase 5. -->
**Ahora mismo esta web no muestra publicidad ni utiliza herramientas de analítica.**

Cuando se activen, esta página se actualizará **antes**, explicando qué proveedor se usa y qué datos trata, y se pedirá tu consentimiento mediante un aviso de cookies. No activaremos nada de eso sin ese paso previo.

## Enlaces a otros sitios

Enlazamos a boletines oficiales, sedes electrónicas y webs de ayuntamientos. Cuando sales de aquí, se aplica la política de privacidad del sitio al que llegas, no esta.

## Tus derechos

Aunque hoy no conservamos datos personales que te identifiquen, tienes en todo caso derecho a **acceder, rectificar, suprimir, limitar el tratamiento, oponerte y solicitar la portabilidad** de tus datos, conforme al Reglamento (UE) 2016/679 y a la Ley Orgánica 3/2018.

Para ejercerlos, escríbenos a la dirección del aviso legal. También puedes reclamar ante la [Agencia Española de Protección de Datos](https://www.aepd.es/).

## Menores

Esta web no se dirige a menores de edad ni recoge deliberadamente datos de menores.

## Cambios

Si esta política cambia, se actualizará la fecha del encabezado. Los cambios relevantes, como activar publicidad o analítica, se anunciarán en la propia web antes de aplicarse.

---

- **[Aviso legal](/legal/aviso-legal/)**
- **[Política de cookies](/legal/cookies/)**
## Búsqueda de direcciones

La herramienta [«¿está mi calle dentro de una ZBE?»](/zbe/mi-calle/) necesita convertir
la dirección que escribes en unas coordenadas. Eso lo hace **tu propio navegador**
consultando a [Nominatim](https://nominatim.openstreetmap.org/), el servicio de
direcciones de OpenStreetMap.

Qué implica, en concreto:

- **La dirección no pasa por ningún servidor nuestro.** Este sitio es estático y no
  tiene backend: no hay dónde recibirla.
- **No la guardamos** ni en el servidor ni en tu navegador.
- **Sí llega a OpenStreetMap**, junto con la dirección IP de tu conexión, porque la
  petición la hace tu navegador directamente. Se rige por
  [su política de privacidad](https://wiki.osmfoundation.org/wiki/Privacy_Policy).
- El cálculo de si esa dirección cae dentro de una zona se hace **en tu dispositivo**,
  con los perímetros que ya se han descargado.

Si prefieres no usar ese servicio, tienes el mismo dato en
[el mapa](/mapa/), que no envía nada a ninguna parte.

