---
title: "Zona de Bajas Emisiones (ZBE) de Oviedo: qué distintivos pueden entrar"
description: "Oviedo tiene dos anillos con calendarios distintos. En el interior, los vehículos sin distintivo están fuera desde el 31 de diciembre de 2025. En el exterior entran todos hasta el 31 de diciembre de 2027."
date: 2026-10-05

tipo: "municipio"
municipio: "Oviedo"
codigo_ine: "33044"
provincia: "Asturias"
ccaa: "Principado de Asturias"

estado_zbe: "activa"
fecha_vigor: "2026-01-01"

# Dos anillos con el mismo mapa de etiquetas pero distinto calendario, así que
# van como zonas separadas: meterlos en una sola fila sería mentir en uno de
# los dos. Anexo I, tablas 1 y 2.
zonas:
  - id: "anillo-interior"
    nombre: "Anillo interior"
    estado: "activa"
    distintivos_permitidos: ["0", "ECO", "C", "B"]
    horario: "Permanente. La ordenanza no fija franja horaria"
    articulo: "anexo I, tabla 1"
    nota: "Los vehículos sin distintivo están fuera desde el 31 de diciembre de 2025."
  - id: "anillo-exterior"
    nombre: "Anillo exterior"
    estado: "activa"
    distintivos_permitidos: ["0", "ECO", "C", "B", "Sin distintivo"]
    horario: "Permanente. La ordenanza no fija franja horaria"
    articulo: "anexo I, tabla 2"
    nota: "Aquí todavía entra cualquier vehículo. Los que no tienen distintivo quedan fuera el 31 de diciembre de 2027."
    caducan:
      sin: "2027-12-31"

excepciones:
  - "Residentes empadronados en un domicilio de la ZBE, con autorización municipal"
  - "Vehículos destinados al desplazamiento de personas con movilidad reducida"
  - "Transporte de mercancías y actividades profesionales"
  - "Empresas concesionarias de servicios públicos y personal de las administraciones"
  - "Servicios de emergencia y esenciales, y transporte público"
  - "Vehículos con matrícula extranjera que acrediten requisitos equivalentes, con autorización de seis meses"
  - "Vehículos que transportan a residentes dependientes empadronados, aunque el coche no sea suyo"
  - "Vinculados a establecimientos o comercios, y clientes con pernoctación en hoteles"
  - "Propietarios de inmuebles en la ZBE no empadronados"
  - "Propietarios o arrendatarios de plaza de garaje, y acceso a talleres"
  - "Vehículos históricos y clientes de aparcamientos subterráneos públicos, sin necesidad de autorización"

fuente_nombre: "Ordenanza de la Zona de Bajas Emisiones del Ayuntamiento de Oviedo, art. 8, art. 18 y anexos I y II"
fuente_url: "https://www.oviedo.es/documents/35127/1038783/ORDENANZA+ZONA+DE+BAJAS+EMISIONES.pdf"
fuente_boletin: "BOPA núm. 243, de 18 de diciembre de 2025. Aprobada definitivamente por acuerdo del Pleno de 2 de diciembre de 2025"
fecha_verificacion: "2026-10-05"

estado_dato: "verificado"
draft: false
---

Oviedo no tiene una zona, tiene **dos anillos con el mismo mapa de etiquetas y dos calendarios distintos**. Si no te fijas en cuál de los dos pisas, la respuesta te sale al revés.

## Qué distintivos pueden entrar

| Distintivo | Anillo interior | Anillo exterior |
|:---|:---|:---|
| **[0 emisiones](/etiquetas/0-emisiones/)** | Sí | Sí |
| **[ECO](/etiquetas/eco/)** | Sí | Sí |
| **[C](/etiquetas/c/)** | Sí | Sí |
| **[B](/etiquetas/b/)** | Sí | Sí |
| **[Sin distintivo](/etiquetas/sin-distintivo/)** | **No**, desde el 31 de diciembre de 2025 | **Sí**, hasta el 31 de diciembre de 2027 |

El anexo I lo dice en dos tablas de una sola línea cada una. En los dos anillos tienen **libre acceso sin autorización** los ciclos, las bicicletas, los vehículos de movilidad personal y los vehículos con distintivo B, C, ECO y 0.

La diferencia está abajo del todo de la tabla: **el vehículo sin etiqueta**. En el anillo interior quedó fuera el 31 de diciembre de 2025. En el exterior tiene dos años más, hasta el 31 de diciembre de 2027.

## Dónde está cada anillo

Las calles que forman el contorno **no están dentro** de la zona; las interiores sí. Eso vale para los dos anillos y conviene saberlo, porque se puede circular por el borde.

**Anillo interior.** Delimitado por Adelantado de la Florida, Postigo Bajo, Postigo Alto, Padre Suárez entre Postigo Alto y Marqués de Gastañaga, Marqués de Gastañaga, Campomanes, Santa Susana, Conde de Toreno, Uría, Doctor Casal, Melquiades Álvarez, Covadonga, Manuel García Conde y Víctor Chavarri.

**Anillo exterior.** Delimitado por General Elorza, Adelantado de La Florida, la Ronda Sur, Muñoz Degraín, González Besada, la avenida Padre Vinjoy, la avenida Hermanos Menéndez Pidal, Real Oviedo, Independencia y la avenida de Santander.

## El aparcamiento del anillo exterior

Hay una medida que no es una prohibición de entrada y conviene no perderla de vista: en el anillo exterior la ordenanza prevé **limitaciones o tarifas de estacionamiento diferenciadas según las emisiones del vehículo**, controladas con la lectura de matrículas.

O sea que puedes entrar, pero aparcar puede costarte distinto según tu etiqueta.

## Excepciones

La ordenanza las agrupa en tres clases, según el trámite:

**Necesitan autorización municipal de acceso, circulación y estacionamiento**: residentes empadronados en la ZBE, vehículos para el desplazamiento de personas con movilidad reducida, transporte de mercancías y actividades profesionales, concesionarias de servicios públicos, personal de las administraciones, servicios de emergencia y esenciales, transporte público, matrículas extranjeras, quien transporta a un residente dependiente aunque el coche no sea suyo, vehículos vinculados a comercios, clientes que pernoctan en hoteles, propietarios de inmuebles no empadronados y casos de urgencia.

**Necesitan autorización solo de acceso y circulación**: propietarios o arrendatarios de plaza de garaje, acceso a talleres de reparación y vehículos vinculados a obras.

**No necesitan autorización ninguna**: residentes empadronados, **vehículos históricos**, clientes de aparcamientos subterráneos públicos y vehículos adaptados y homologados para servicios singulares.

Las matrículas extranjeras tienen su propia tabla de equivalencias: turismos y furgonetas ligeras de gasolina matriculados desde enero de 2000 con norma Euro 3, y diésel desde enero de 2006 con Euro 4 o 5. Su autorización dura un máximo de seis meses.

## Si te multan

No respetar las restricciones es **infracción grave**, con **multa de 200 euros** (art. 18.2).

Y hay un recargo que solo hemos visto aquí y en Palma: **la sanción sube un 30 % por reincidencia**, entendiendo por tal haber cometido más de una infracción de la misma naturaleza en el plazo de un año, declarada por resolución firme.

Lo general de las multas de ZBE lo explicamos en [multas por entrar en una ZBE](/multas/zbe/).

## Si hay un episodio de contaminación

El artículo 9 permite endurecer temporalmente las restricciones cuando se active el protocolo del Principado de Asturias: pueden restringirse otros tipos de vehículo y extenderse la zona a otras áreas del municipio. Se hace por resolución de alcaldía publicada en la web municipal, y no puede durar más de tres meses prorrogables hasta el año.

También funciona al revés: por motivos excepcionales de interés público se puede **suspender** la restricción general, con el mismo procedimiento y los mismos plazos.

## Desde cuándo

La ordenanza fue **aprobada definitivamente por acuerdo del Pleno de 2 de diciembre de 2025** y su texto íntegro se publicó en el **Boletín Oficial del Principado de Asturias número 243, de 18 de diciembre de 2025**.

La primera restricción, la del anillo interior, se aplica **desde el 31 de diciembre de 2025**.
