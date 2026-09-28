# Cómo se verifica la ordenanza de un municipio

Guion fijo para que las fichas salgan todas iguales y ninguna se publique con
un hueco. Verificar ocho municipios a ojo garantiza que la octava no se
parezca a la primera.

**Antes de nada:** el dato sale del texto oficial. No de una noticia, no de un
resumen de un blog, no de lo que crea recordar un modelo de lenguaje. Si no
está en la ordenanza, en el boletín o en la web del ayuntamiento, no se
publica.

---

## 1. Crear la ficha

```bash
hugo new content/zbe/valencia.md --kind zbe
```

Nace con `estado_dato: "pendiente"` y `draft: true`, así que no se publica
aunque se te olvide. Es deliberado.

---

## 2. Encontrar la fuente

Por este orden, y parando en cuanto una sirva:

1. **La sede electrónica del ayuntamiento.** Busca «zona de bajas emisiones»
   en su buscador. Muchos tienen una sección propia con el texto de la
   ordenanza, el mapa y las preguntas frecuentes. Zaragoza es el mejor
   ejemplo.
2. **El boletín oficial de la provincia o de la comunidad**, donde se publicó
   la ordenanza. Es la fuente de más rango y la que se cita.
3. **El mapa del MITECO**, solo para confirmar que la ZBE existe y su estado.
   No sirve para las reglas de acceso.

El NAP de la DGT **no vale para esto**. Cada ayuntamiento codifica el mismo
campo con el significado contrario, y está explicado en `CLAUDE.md`. De ahí
solo se usan la existencia de la zona, la fuente y la geometría.

---

## 3. Los seis datos

De cada ordenanza hay que sacar exactamente estos seis. Ni más ni menos.

| Dato | Dónde acaba | Cómo tiene que estar |
|---|---|---|
| **Distintivos que pueden acceder** | `etiquetas_permitidas` o el bloque `zonas` | Tal cual los nombra la norma. Si dice «B con condiciones», se escribe así |
| **Horario de la restricción** | `horario_restriccion` | Literal. «De lunes a viernes de 7:00 a 20:00», no «en horario laboral» |
| **Perímetro** | El cuerpo de la ficha | Qué calles o qué anillo. Sin interpretarlo |
| **Excepciones** | `excepciones` | Residentes, movilidad reducida, vehículos históricos, servicios. Las que la norma recoja |
| **Artículo exacto** | `zonas[].articulo` o el cuerpo | «art. 23 y anexo III». Es lo que permite que alguien lo compruebe |
| **Boletín y fecha** | `fuente_nombre`, `fuente_boletin`, `fuente_url` | «BOCM núm. 80, de 6 de abril de 2026» |

Si el municipio tiene varias zonas con reglas distintas, **no se promedian**:
se usa el bloque `zonas`, como en `content/zbe/madrid.md`. Una respuesta única
para tres zonas distintas sería falsa.

---

## 4. La regla de parada

**Si un dato no aparece literalmente en el texto oficial, no se publica.**

Ante la duda, la ficha se queda en nivel C: se dice que la ZBE existe, se
enlaza la fuente oficial y **no se responde a «¿puedo entrar?»**. Eso es
`estado_dato: "pendiente"` y `draft: true`.

Publicar media ficha es peor que no publicarla. Quien llega buscando si puede
entrar en el centro se juega 200 euros, y una respuesta a medias con el sello
de verificado es exactamente lo que este proyecto dice no hacer.

Tres casos que parecen dudas y no lo son:

- **La ordenanza está derogada o modificada.** Se cita la vigente, y si hay una
  modificación se cita esa. Madrid es así: se cita la Ordenanza 2/2026 que
  modifica la de 2018.
- **La norma dice «vehículos clasificados como…» sin nombrar el distintivo.**
  Hay que seguir la remisión hasta el texto que sí los nombra. Si no se puede,
  nivel C.
- **El ayuntamiento anuncia una ZBE en una nota de prensa pero no hay
  ordenanza.** `estado_zbe: "prevista"` y nivel C. Una nota de prensa no es
  una norma.

---

## 5. Publicar

Solo cuando los seis datos están:

```yaml
estado_dato: "verificado"
draft: false
```

Y después, siempre:

```bash
hugo --gc --minify        # si falta un campo obligatorio, aborta
python pipeline/auditoria.py
```

El build **rompe a propósito** si una ficha publicada no tiene `codigo_ine`,
`fuente_url` o `fecha_verificacion`. Está comprobado: una ficha recién creada
del archetype y marcada como verificada aborta el build nombrando los tres
campos que faltan. No es una comprobación teórica.

Último paso, y no se delega: abrir la herramienta en el navegador, elegir ese
municipio con un vehículo de cada distintivo, y comprobar que los cinco
veredictos coinciden con lo que dice la ordenanza.

---

## 6. Cuando la fuente no se deja leer

Pasa: PDF escaneado sin texto, visor que no deja descargar, sede caída.

**No se adivina y no se busca en otro sitio menos fiable.** Se anota aquí
abajo con la URL exacta que se intentó y qué falló, se sigue con el siguiente
municipio, y se piden todas juntas al final del día.

### Fuentes que no he podido leer

_(vacío, de momento)_
