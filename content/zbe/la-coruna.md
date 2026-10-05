---
title: "Zona de Bajas Emisiones (ZBE) de La Coruña / A Coruña: quién puede entrar"
description: "La ZBE de La Coruña no va por etiqueta ambiental: ningún distintivo da acceso. Solo entran transporte público, taxis en calles concretas, vehículos autorizados y la carga y descarga."
date: 2026-10-05

tipo: "municipio"
municipio: "La Coruña"
codigo_ine: "15030"
provincia: "A Coruña"
ccaa: "Galicia"
# El NAP publica esta ZBE como ACoruña.xml. La página se llama la-coruna
# porque es como la busca la mayoría, así que la equivalencia va aquí y en la
# tabla FICHAS de pipeline/zbe_geometria.py.
slug_nap: "a-coruna"

estado_zbe: "activa"

# AQUÍ ESTÁ LO ESPECIAL DE ESTA FICHA.
#
# La ZBE CENTRO de La Coruña no restringe por distintivo ambiental: restringe
# por quién eres y a qué vas. Ningún distintivo da acceso a un turismo
# particular, ni siquiera el 0. La etiqueta solo sirve para ampliar la franja
# horaria de la carga y descarga.
#
# `etiquetas_permitidas: []` a secas significaría "no lo hemos leído", que es
# falso: la ordenanza está leída entera. Esta marca es lo que distingue las
# dos cosas, y hace que la herramienta responda "No, salvo autorización" en
# vez de pedir un distintivo que no cambia nada.
acceso_por_distintivo: false
etiquetas_permitidas: []
horario_restriccion: "Permanente. La ordenanza no fija franja horaria para el acceso general"
articulo: "art. 20 de la Ordenanza de Movilidad Sostenible"
nota_zona: "Aquí el distintivo no decide: solo entran transporte público, taxis en calles concretas, vehículos autorizados y la carga y descarga."
excepciones:
  - "Transporte público colectivo de personas viajeras"
  - "Taxis, solo en la Avenida de la Marina, la Avenida Montoto hasta Puerta Real y la Ciudad Vieja"
  - "Vehículos autorizados conforme a los decretos de alcaldía de 27 de marzo de 2017 y 1 de junio de 2018"
  - "Carga y descarga de 6:00 a 11:00, para todo tipo de vehículos"
  - "Carga y descarga de 5:00 a 6:00 y de 11:00 a 12:00, solo con distintivo 0 emisiones o ECO"
  - "Vehículos de servicio público, con un máximo de 8 metros de largo dentro de la Ciudad Vieja"
  - "Vehículos habilitados para estacionar en las reservas de espacio autorizadas"
  - "Ciclos, bicicletas y vehículos de movilidad personal, a un máximo de 10 km/h"

fuente_nombre: "Ordenanza de Movilidad Sostenible del Concello da Coruña, arts. 20 y 190"
fuente_url: "https://www.coruna.gal/descarga/1453902501202/Ordenanza-de-Movilidad-Sostenible-del-Concello-da-Coruna_castellano.pdf"
fuente_boletin: "BOP A Coruña núm. 185, de 29 de septiembre de 2025. Aprobada definitivamente por el Pleno de 11 de septiembre de 2025"
fecha_verificacion: "2026-10-05"

estado_dato: "verificado"
draft: false
---

La Zona de Bajas Emisiones de La Coruña es **distinta de todas las demás que llevamos verificadas**, y conviene decirlo antes que nada porque tira abajo la pregunta habitual.

Aquí **el distintivo ambiental no decide nada**. No hay una lista de etiquetas que entran y otra que no. Lo que hay es una zona cerrada al tráfico general: entran unos pocos tipos de vehículo por lo que son y por lo que van a hacer, y el resto no entra, lleve la pegatina que lleve.

Un coche particular con distintivo 0 emisiones, el mejor que da la DGT, **tampoco puede entrar**.

## Quién puede entrar

El artículo 20.2 de la Ordenanza de Movilidad Sostenible lo enumera, y es una lista cerrada:

| Quién | Con qué condición |
|:---|:---|
| **Transporte público** colectivo de viajeros | Sin condición |
| **Taxis** | Solo en la Avenida de la Marina, la Avenida Montoto hasta Puerta Real y la Ciudad Vieja |
| **Vehículos autorizados** | Con el distintivo municipal de autorizado |
| **Carga y descarga** | De 6:00 a 11:00 cualquier vehículo. De 5:00 a 6:00 y de 11:00 a 12:00, **solo con distintivo 0 o ECO** |
| **Vehículos de servicio público** | Máximo 8 metros de largo dentro de la Ciudad Vieja |
| **Reservas de espacio autorizadas** | Los vehículos habilitados para estacionar en ellas |
| **Ciclos, bicicletas y VMP** | Respetando las normas de zona peatonal, máximo 10 km/h |

El único sitio donde la etiqueta ambiental aparece en toda la regulación es la cuarta fila: **el 0 y el ECO amplían en dos horas la ventana de reparto**. Para nada más sirve.

## Dónde es

La ZBE se llama **ZBE CENTRO** y está delimitada en el anexo II de la ordenanza. Comprende:

- La **Ciudad Vieja**
- La **Avenida de la Marina**
- El **Paseo del Parrote**
- Determinadas calles de la **Pescadería**

No es toda la ciudad ni se parece a las ZBE de perímetro amplio de otras capitales: es el casco histórico y su entorno inmediato.

## Cómo se consigue ser «vehículo autorizado»

Esta es la pregunta práctica, porque es la única puerta que queda.

La ordenanza no inventa un permiso nuevo: remite a dos normas municipales anteriores, que son las que fijan los requisitos (art. 20.3):

- El **decreto de alcaldía de 27 de marzo de 2017**, que regula las zonas peatonales reguladas (ZPR).
- El **decreto de alcaldía de 1 de junio de 2018**, que delimita la Ciudad Vieja como área de preferencia peatonal.

**No reproducimos aquí los requisitos concretos porque no hemos leído esos dos decretos.** Son normas distintas de la ordenanza que sí hemos verificado, y publicar de oído a quién dan permiso sería exactamente lo que este sitio no hace. Si te afecta, pregúntalo en el Concello citando esos dos decretos.

## Aparcar

El artículo 20.4 es tajante: **no se puede estacionar dentro de la ZBE CENTRO**, salvo las excepciones que recogen esos mismos dos decretos.

## Si te multan

La ordenanza distingue dos niveles (art. 190):

| Infracción | Importe |
|:---|:---|
| Leve: incumplir las normas de circulación y estacionamiento de la zona | **100 €** |
| **Grave: no respetar la prohibición de acceso, circulación o estacionamiento** dentro de la ZBE | **200 €** |

Los 200 euros de la grave coinciden con el importe general de las multas de ZBE en toda España, que explicamos en [multas por entrar en una ZBE](/multas/zbe/). Los 100 euros de la leve son propios de esta ordenanza.

## Desde cuándo

La ordenanza fue **aprobada definitivamente por el Pleno el 11 de septiembre de 2025** y su texto íntegro se publicó en el **Boletín Oficial de la Provincia de A Coruña número 185, de 29 de septiembre de 2025**.

Su disposición final primera dice que entra en vigor cuando el texto se publique íntegramente en el BOP **y transcurra el plazo del artículo 65.2 de la Ley de Bases del Régimen Local**, que son quince días hábiles. No damos una fecha exacta porque la ordenanza no la escribe: la hace depender de ese cómputo.

## Por qué esta ficha no responde «sí» a nadie

Nuestra herramienta pregunta qué distintivo tienes para decirte si puedes entrar. En La Coruña esa pregunta no tiene respuesta útil, y fingir que la tiene sería peor que no responder.

Por eso aquí la herramienta contesta **«No, salvo autorización»** a cualquier distintivo, incluido el 0. Es la respuesta correcta: lo que abre esta zona no es la etiqueta, es el permiso municipal.

## Un apunte sobre el dato de la DGT

El Punto de Acceso Nacional de la DGT publica para La Coruña un fichero que declara los distintivos 0, ECO, C y B con la marca `negate` activada. Leído de forma automática, cualquiera concluiría que esos cuatro distintivos entran.

Acabas de leer la ordenanza: **no entra ninguno**. Es el ejemplo más claro de por qué [no publicamos reglas deducidas de ese fichero](/datos/zbe/) y las leemos una a una.
