---
title: "Zona de Bajas Emisiones (ZBE) de Alicante: qué restringe de verdad"
description: "En Alicante la etiqueta ambiental no abre ninguna puerta: el Casco Antiguo sigue con su régimen de residentes y autorizados, y en el resto de la ZBE no hay restricción por distintivo."
date: 2026-10-04

tipo: "municipio"
municipio: "Alicante"
codigo_ine: "03014"
provincia: "Alicante"
ccaa: "Comunidad Valenciana"

estado_zbe: "activa"

# CORREGIDO EL 06/10/2026, y la corrección importa.
#
# Esta ficha decía que en el Anillo I entran los distintivos 0, ECO, C y B.
# Es falso, o al menos incompleto hasta el punto de inducir a error: el anexo 2
# dice «todos aquellos vehículos YA AUTORIZADOS, no industriales, con etiqueta
# ambiental del tipo B, C, ECO y CERO». La etiqueta es un SEGUNDO filtro sobre
# quien ya tiene permiso de acceso al casco antiguo, no una llave por sí sola.
#
# Lo confirma la FAQ del propio Ayuntamiento: la ZBE «no implica restricciones
# de acceso automáticas para los vehículos, ni sanciones directas, salvo en el
# caso del anillo correspondiente al Casco Antiguo, en el que sigue vigente su
# régimen de accesos restringidos a vehículos residentes y autorizados».
acceso_por_distintivo: false
etiquetas_permitidas: []
horario_restriccion: "Permanente: la ordenanza declara la ZBE de vigencia permanente y no fija franja horaria"
articulo: "art. 9.1 y anexo 2, apartado 1"
nota_zona: "En el Casco Antiguo manda el régimen de residentes y autorizados, no la etiqueta. En los anillos del Centro y la Gran Vía no hay restricción por etiqueta."
excepciones:
  - "Vehículos de personas empadronadas, residentes o propietarias de viviendas o garajes en la zona, con o sin distintivo"
  - "Propietarios y arrendatarios de plaza de garaje dentro de la zona, con o sin distintivo"
  - "Vehículos históricos declarados y clasificados como tales por la DGT"
  - "Personas con tarjeta TED de movilidad reducida, previa alta en la plataforma de gestión, con o sin distintivo"
  - "Ciclos, bicicletas y vehículos de movilidad personal"
  - "Taxis, VTC y autobuses discrecionales con distintivo B, C, ECO o 0"
  - "Vehículos industriales y de reparto con distintivo B, C, ECO o 0 y autorización previa"
  - "Reparto de medicamentos a centros médicos y farmacias, con o sin distintivo"

fuente_nombre: "Ordenanza reguladora de la Zona de Bajas Emisiones de Alicante, arts. 9 y 17 y anexo 2"
fuente_url: "https://www.alicante.es/sites/default/files/documentos/202501/ordenanza-zbe-alicante.pdf"
fuente_boletin: "BOP Alicante núm. 5, de 9 de enero de 2025"
fecha_verificacion: "2026-10-06"

estado_dato: "verificado"
draft: false
---

La ZBE de Alicante se cuenta casi siempre mal, y nosotros también la contamos mal durante dos días. La corrección está al final de esta página.

Lo importante, dicho de una vez: **en Alicante la etiqueta ambiental no abre ninguna puerta**. No hay una lista de distintivos que entran y otra que no.

## Qué restringe de verdad

La zona declarada abarca tres anillos, y el mayor, el de la Gran Vía, son 7,49 km², el 19,4 % del municipio, con 157.498 habitantes dentro. Pero el perímetro no es la restricción:

| Anillo | Qué pasa hoy |
|:---|:---|
| **I, Casco Antiguo** | Sigue vigente su **régimen de accesos restringidos a residentes y autorizados**, que ya existía. La etiqueta no sustituye a la autorización |
| **II, Centro Tradicional** | **Sin restricción por etiqueta** |
| **III, Gran Vía** | **Sin restricción por etiqueta** |

El Ayuntamiento lo dice así en sus preguntas frecuentes: la ZBE «no implica restricciones de acceso automáticas para los vehículos, ni sanciones directas, **salvo en el caso del anillo correspondiente al Casco Antiguo (en el que sigue vigente su régimen de accesos restringidos a vehículos residentes y autorizados)**».

### Entonces, ¿para qué sirve la etiqueta aquí?

Para nada por sí sola, y esta es la frase que hay que leer despacio. El anexo 2 de la ordenanza autoriza a los turismos así:

> «Todos aquellos vehículos **ya autorizados**, no industriales, con etiqueta ambiental del tipo B, C, ECO y CERO.»

«Ya autorizados» es la clave. La etiqueta es un **segundo filtro sobre quien ya tiene permiso** de acceso al casco antiguo, no una llave por sí misma. Lo mismo dice de las motocicletas («ya autorizados con distintivo ambiental B, C, ECO y CERO»), de los comercios («con autorización previa... podrán acceder libremente si tienen distintivo») y del personal que trabaja dentro («con acceso al casco antiguo autorizado, con distintivo»).

Dicho en corto: **si no tienes autorización para el casco antiguo, tu etiqueta da igual. Y si la tienes, en algunos casos además te piden etiqueta.**

## Los otros dos anillos

El Anillo II es el Centro Tradicional y el Anillo III el de la Gran Vía. Los dos forman parte de la ZBE declarada, **y la ordenanza no les impone ninguna restricción permanente por distintivo**. Puedes circular por ellos con cualquier vehículo.

Lo que sí prevé para ellos es el artículo 10: ante un **episodio de contaminación** declarado por la administración competente, se activa el protocolo municipal y pueden restringirse accesos de forma temporal, por zonas y horarios concretos, a los vehículos más contaminantes.

O sea: en el día a día, por la Gran Vía circulas con cualquier distintivo. En un episodio de alta contaminación, puede dejar de ser así durante unos días.

## Una confirmación que no viene de la ordenanza

Hay una forma independiente de comprobar que la restricción es solo del Casco Antiguo, y nos parece justo enseñarla.

El propio Ayuntamiento de Alicante publica la geometría de su ZBE en el [Punto de Acceso Nacional de la DGT](/datos/zbe/). Ese polígono **ocupa 0,35 km²** y cae entre las longitudes -0,485 y -0,477 y las latitudes 38,344 y 38,349: el Casco Antiguo, no los 7,49 km² del anillo de la Gran Vía.

Es decir, la zona que el ayuntamiento declara como restringida ante la DGT coincide con lo que dice el artículo 9.1, y no con el perímetro completo de los tres anillos.

## Horario: no hay franja

El artículo 4.2 dice que la ZBE «tendrá una vigencia permanente». La ordenanza no fija ninguna franja horaria para el Anillo I, así que la restricción **no depende de la hora ni del día de la semana**.

## Quién entra aunque no tenga distintivo

Esta es la parte donde Alicante es más generosa que la mayoría, y conviene leerla entera porque cubre a mucha gente:

- **Empadronados, residentes y propietarios de vivienda o garaje en la zona.** El anexo lo dice con todas las letras: «con o sin distintivo ambiental de la DGT».
- **Propietarios y arrendatarios de una plaza de garaje** dentro de la zona, «tengan o no distintivo ambiental».
- **Vehículos históricos** declarados y clasificados como tales por la DGT: autorizados directamente.
- **Personas con tarjeta TED** de estacionamiento para personas con discapacidad y movilidad reducida. Hay que darse de alta en la plataforma de gestión de la ZBE indicando las matrículas, hasta un máximo de dos vehículos, y llevar la TED visible. El vehículo puede estar adaptado o no y tener distintivo o no.
- **Reparto de medicamentos** a centros médicos y farmacias, con o sin distintivo.
- **Ciclos, bicicletas y vehículos de movilidad personal**, sin autorización ninguna.

En cambio, **sí necesitan distintivo B, C, ECO o 0**, aunque tengan autorización: los taxis, los VTC, los autobuses discrecionales, los vehículos de comercios, bares y restaurantes de la zona, los industriales de reparto y los de quienes trabajan dentro de la ZBE.

## Si te multan

No respetar las restricciones del Anillo I es **infracción grave**, con **multa de hasta 200 euros** (art. 17.2).

**Una cosa que no podemos confirmarte, y preferimos decirlo.** La ordenanza establece en su artículo 4.3 una **moratoria** para que la ciudadanía se adapte: durante ese periodo, a quien infrinja la norma se le puede enviar «un documento informativo de la infracción cometida, sin que lleve aparejada la sanción». Lo que la ordenanza **no** dice es cuánto dura esa moratoria, y no hemos encontrado ninguna publicación oficial del Ayuntamiento de Alicante que fije su final.

Así que la regla de acceso está clara y verificada, pero **no afirmamos si a día de hoy ya te multan o todavía estás en periodo de aviso**. Si necesitas esa certeza, pregúntala en el Ayuntamiento de Alicante antes de entrar.

El régimen general de las multas de ZBE lo explicamos en [multas por entrar en una ZBE](/multas/zbe/).

## Cuándo entró en vigor

La ordenanza fue **aprobada definitivamente por el Pleno el 30 de diciembre de 2024** y publicada en el **BOP de Alicante núm. 5, de 9 de enero de 2025**.

Su disposición final tercera remite, para la entrada en vigor, al plazo del artículo 65.2 de la Ley 7/1985 reguladora de las Bases del Régimen Local, que son quince días hábiles desde la publicación. No damos una fecha exacta de entrada en vigor porque la ordenanza no la escribe: la hace depender de ese cómputo.

## Qué decía esta ficha antes, y por qué estaba mal

Entre el 4 y el 6 de octubre de 2026 esta página decía que en el Anillo I entran los distintivos 0, ECO, C y B, y que los vehículos sin distintivo no entran salvo excepción.

**Era engañoso**, y conviene explicar por qué para que se entienda el error: nos quedamos con la parte de la frase del anexo que habla de etiquetas y pasamos por alto las dos palabras que la gobiernan, «ya autorizados». Leída entera, esa línea no dice que un turismo con etiqueta C pueda entrar: dice que, **entre los que ya tienen autorización**, pueden hacerlo los que además lleven B, C, ECO o CERO.

Lo destapó la página de preguntas frecuentes del propio Ayuntamiento, que afirma que no hay restricciones automáticas por etiqueta y que el casco antiguo mantiene su régimen anterior.

La consecuencia práctica de la versión antigua habría sido la peor posible: alguien de fuera con etiqueta C podía leernos y entender que podía entrar en el casco antiguo de Alicante. No podía. Lo dejamos escrito aquí porque corregir en silencio deja al lector sin saber cuál de las dos versiones leyó.
