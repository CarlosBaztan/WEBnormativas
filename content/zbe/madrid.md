---
title: "Zona de Bajas Emisiones (ZBE) de Madrid: qué coches entran"
description: "Madrid tiene tres zonas de bajas emisiones con reglas distintas. Qué distintivo necesitas en cada una, excepciones y sanción, con la ordenanza citada."
date: 2026-09-23

tipo: "municipio"
municipio: "Madrid"
codigo_ine: "28079"
provincia: "Madrid"
ccaa: "Comunidad de Madrid"

# activa | prevista | sin_zbe
estado_zbe: "activa"

fuente_nombre: "Ordenanza 2/2026, de 24 de marzo, que modifica la Ordenanza de Movilidad Sostenible de 5 de octubre de 2018"
fuente_url: "https://www.bocm.es/boletin/CM_Orden_BOCM/2026/04/06/BOCM-20260406-32.PDF"
fuente_boletin: "BOCM núm. 80, de 6 de abril de 2026, págs. 129-219"
fecha_vigor_ordenanza: "2026-04-07"
fecha_verificacion: "2026-10-06"
verificado_por: "Carlos Baztán"

zonas:
  - id: "madrid-ciudad"
    nombre: "Madrid ZBE (todo el municipio)"
    estado: "activa"
    # Verificado el 06/10/2026 en la pagina oficial del Ayuntamiento de Madrid,
    # actualizada el 07/04/2026. El art. 21 prohibe circular a los «A» desde el
    # 1 de enero de 2025, y la disposicion transitoria septima que introdujo la
    # Ordenanza 2/2026 les deja volver de forma temporal y CONDICIONADA desde
    # el 7 de abril de 2026. De ahi «con condiciones» y no un si a secas.
    distintivos_permitidos: ["0", "ECO", "C", "B", "Sin distintivo con condiciones"]
    horario: "Permanente, todos los días"
    articulo: "art. 21 OMS y disposición transitoria séptima"
    nota: "Desde el 7 de abril de 2026, algunos vehículos sin distintivo pueden circular de forma temporal y condicionada, y solo fuera de Distrito Centro y Plaza Elíptica."

  - id: "distrito-centro"
    nombre: "ZBEDEP Distrito Centro"
    estado: "activa"
    distintivos_permitidos: ["0", "ECO", "C con condiciones", "B con condiciones"]
    horario: "permanente, con horarios propios para industriales y motos"
    articulo: "art. 23 y anexo III"

  - id: "plaza-eliptica"
    nombre: "ZBEDEP Plaza Elíptica"
    estado: "activa"
    distintivos_permitidos: ["0", "ECO", "C", "B"]
    prohibidos: ["sin distintivo (A)"]
    horario: "permanente"
    articulo: "art. 24 y anexo IV"

sancion_tipificacion: "Infracción grave, art. 76.z3) LTSV; sanción conforme a arts. 80.1 y 81 LTSV"
sancion_importe: "pendiente"

estado_dato: "verificado"
draft: false
---

Madrid no tiene una zona de bajas emisiones, sino **tres, con reglas distintas**. Antes de entrar hay que saber en cuál vas a circular.

## Respuesta rápida

| Tu distintivo | Madrid ciudad | Distrito Centro | Plaza Elíptica |
|:---|:---|:---|:---|
| **0 emisiones** | Sí | Sí | Sí |
| **ECO** | Sí | Sí (industriales, de 7:00 a 21:00) | Sí |
| **C** | Sí | Solo en casos concretos | Sí |
| **B** | Sí | Solo en casos concretos | Sí |
| **Sin distintivo** | **Solo con condiciones**, y desde el 7 de abril de 2026 | No | **No** |

"Casos concretos" en Distrito Centro significa, sobre todo: estar empadronado dentro, ser invitado de alguien que lo esté, tener empresa o local dentro, o acreditar que vas a un aparcamiento dentro de la zona. Lo detallamos abajo.

## Madrid ciudad: toda la ciudad es zona de bajas emisiones

Esto sorprende a mucha gente, y es lo primero que hay que entender de Madrid: **la ZBE no es un barrio, es el municipio entero**. El artículo 21 de la Ordenanza de Movilidad Sostenible la define como una ordenación del tráfico establecida de forma permanente «en el ámbito territorial constituido por todas las vías públicas urbanas del municipio de Madrid».

Desde el **1 de enero de 2025** prohíbe circular a todos los vehículos que figuran con clasificación ambiental **'A'** en el Registro Nacional de Vehículos de la DGT. O sea, los que no tienen derecho a ningún distintivo.

Si tu vehículo tiene distintivo 0, ECO, C o B, esta zona no te afecta: circulas por toda la ciudad sin restricción por etiqueta, y lo que te puede afectar son las otras dos zonas.

### El giro de abril de 2026: algunos coches sin etiqueta han vuelto

Es el cambio más reciente de las tres zonas, y el que peor recogen los resúmenes que siguen circulando.

La **Ordenanza 2/2026, de 24 de marzo** introdujo una nueva disposición transitoria séptima que, **desde las 00:00 del 7 de abril de 2026**, permite circular otra vez a parte de los vehículos 'A'. Pero con tres límites que conviene leer despacio, porque cada uno puede dejarte fuera:

**Primero, solo por fuera de las otras dos zonas.** El permiso vale para las vías de Madrid ZBE «que no formen parte del ámbito territorial de las ZBEDEP Distrito Centro y Plaza Elíptica». Dentro de esas dos sigue prohibido.

**Segundo, solo dos grupos de vehículos:**

- Los **'A' domiciliados en Madrid**, que desde el 1 de enero de 2022 y **de forma ininterrumpida** figuren domiciliados en la ciudad en el Registro Nacional de Vehículos **y** de alta en el padrón del IVTM del Ayuntamiento. Las dos cosas, sin interrupción.
- Los **'A' que no sean turismos**: camiones, furgonetas, motocicletas, ciclomotores y demás, con independencia del municipio donde estén domiciliados.

**Tercero, y es el más frágil: está condicionado a la calidad del aire.** El permiso dura mientras se cumplan los valores límite de dióxido de nitrógeno **en todas** las estaciones de vigilancia de la ciudad. Si se incumple en cualquiera de ellas, la Junta de Gobierno declara extinguido el régimen transitorio y **se empieza a sancionar seis meses después** de publicarlo en el BOCM.

Además, estos vehículos **tienen prohibido circular los días con episodio de contaminación**, según el artículo 35 de la ordenanza y el protocolo de dióxido de nitrógeno.

### Quiénes quedan fuera del régimen transitorio

No se benefician los **turismos 'A'** de las categorías por criterio de utilización 00 (sin especificar), 02 (familiar) y 33 (todoterreno) que a 1 de enero de 2022 no cumplieran a la vez el requisito de estar domiciliados en Madrid y de alta en el padrón del IVTM.

Dicho en corto: si tu turismo sin etiqueta no era de Madrid en enero de 2022, no entra.

### Las dos excepciones permanentes

El artículo 21.3 exceptúa siempre, con independencia de todo lo anterior:

- Los vehículos **conducidos por o que transporten a titulares de la tarjeta TEPMR**, siempre que estén de alta en el sistema de gestión de accesos y exhiban la tarjeta.
- Los vehículos reconocidos como **históricos** conforme al reglamento de vehículos históricos.

## Distrito Centro

Es la zona del centro histórico, la que antes se llamaba Madrid Central. Se puede **circular libremente por las calles del perímetro**, pero no atravesar el interior.

Pueden entrar, entre otros:

- Vehículos **0 y ECO**.
- Vehículos **0, ECO, C y B de personas empadronadas** dentro de la zona, y de las personas a las que inviten.
- Turismos **0, ECO, C y B de empresas y autónomos** con local u oficina dentro.
- Vehículos de personas con **tarjeta de estacionamiento por movilidad reducida** (TEPMR), dadas de alta en el sistema municipal.
- El resto de vehículos **B o C**, únicamente si acreditan que van a un aparcamiento o reserva de estacionamiento dentro de la zona.

Dos horarios, y no son el mismo:

- **Vehículos industriales** que prestan servicios o hacen reparto: los 0 emisiones, las 24 horas; los ECO, de 7:00 a 21:00; los C, de 7:00 a 15:00.
- **Motos y ciclomotores B o C** no autorizados por otra vía: solo de 7:00 a 22:00.

<details>
<summary>Ver el perímetro exacto de la zona</summary>

Calle Alberto Aguilera, glorieta de Ruiz Jiménez, calle Carranza, glorieta de Bilbao, calle Sagasta, plaza de Alonso Martínez, calle Génova, plaza de Colón, paseo de Recoletos, plaza de Cibeles, paseo del Prado, plaza de Cánovas del Castillo, plaza del Emperador Carlos V, ronda de Atocha, ronda de Valencia, glorieta de Embajadores, ronda de Toledo, glorieta de la Puerta de Toledo, ronda de Segovia, cuesta de la Vega, calle Mayor, calle Bailén, plaza de España (lateral continuación de la cuesta de San Vicente), calle Princesa y calle Serrano Jover.

Además de estas calles, hay nueve viales interiores de libre circulación, entre ellos Mártires de Alcalá, Seminario de Nobles, Gran Vía de San Francisco, Bailén, Algeciras y cuesta Ramón.

*Fuente: art. 23.2 de la ordenanza y apartado 3 del anexo III.*

</details>

## Plaza Elíptica

Mucho más simple: **los vehículos sin distintivo ambiental no pueden circular** por su interior, incluido el tramo de la A-42 comprendido dentro. El resto sí.

Las excepciones son tres: vehículos de personas con TEPMR dadas de alta en el sistema, vehículos históricos reconocidos como tales, y transporte colectivo de personas con discapacidad.

<details>
<summary>Ver el perímetro exacto de la zona</summary>

Calle Faro, avenida de Abrantes, calle Portalegre, avenida de Oporto, travesía de Antonia Lancha, calle Santa Lucrecia, calle Antonio Leyva, calle de Enrique Pérez, lateral del paseo de Santa María de la Cabeza en sentido entrada a Madrid hasta el puente de los Capuchinos, calle Manuel Noya, calle Cerecinos, calle Fornillos, calle Ricardo Beltrán y Rozpide hasta el número 8, avenida Princesa Juana de Austria en sentido entrada a Madrid y calle Vía Lusitana.

*Fuente: art. 24.2 de la ordenanza.*

</details>

## Cómo está señalizada

{{< senales-madrid >}}

## Si te multan

Entrar incumpliendo las restricciones es **infracción grave** de tráfico, tipificada en el artículo 76.z3) de la Ley de Tráfico y sancionada conforme a sus artículos 80.1 y 81. El importe no lo fija el Ayuntamiento, sino la ley estatal.

*Importe: 200 euros, que es lo que el art. 80.1 de la Ley de Tráfico señala para las infracciones graves. No quita puntos. Ver [multas por entrar en una ZBE](/multas/zbe/).*

El control se hace con cámaras con lector de matrículas (art. 22.10 de la ordenanza). Ver [cómo funcionan las cámaras](/zbe/camaras/).

## Excepciones y autorizaciones

Si crees que te corresponde una excepción (residencia, movilidad reducida, vehículo histórico, actividad profesional dentro de la zona), se tramita en la sede electrónica del Ayuntamiento. Dos detalles útiles:

- **Una sola alta para toda la ciudad si tienes la TEPMR.** Con independencia de la categoría ambiental del vehículo, se garantiza la circulación de los conducidos por titulares de la tarjeta de estacionamiento para personas con movilidad reducida, o empleados para transportarlas, por todas las ZBE, y basta **una única alta** en el sistema de gestión municipal: vale a la vez para Madrid ZBE, Distrito Centro y Plaza Elíptica. **El vehículo asociado se puede cambiar una vez al día**, que es lo que resuelve el caso de quien no siempre va en el mismo coche.
- El Ayuntamiento se compromete a responder en **10 días naturales**. Si no responde, se entiende permitida provisionalmente la circulación.

## Un apunte sobre la situación legal

La regulación anterior de estas dos zonas, aprobada en 2021, fue **anulada por el Tribunal Superior de Justicia de Madrid** en su sentencia 405/2024, de 17 de septiembre, que no es firme porque hay recurso de casación pendiente. La Ordenanza 2/2026 vuelve a regularlas, y es la norma que está en vigor desde el 7 de abril de 2026.

---

**Fuente:** Ordenanza 2/2026, de 24 de marzo, por la que se modifica la Ordenanza de Movilidad Sostenible de 5 de octubre de 2018 · [BOCM núm. 80, de 6 de abril de 2026](https://www.bocm.es/boletin/CM_Orden_BOCM/2026/04/06/BOCM-20260406-32.PDF) · En vigor desde el 7 de abril de 2026 · El régimen de la TEPMR, además, en [Ordenanza de Movilidad Sostenible y PMR](https://www.madrid.es/portales/munimadrid/es/Inicio/Movilidad-y-transportes/Personas-con-movilidad-reducida/?vgnextfmt=default&vgnextchannel=220e31d3b28fe410VgnVCM1000000b205a0aRCRD) (Ayuntamiento de Madrid)


*¿Has visto algo incorrecto en esta ficha? Escríbenos.*
