# -*- coding: utf-8 -*-
"""
Tests de las fechas de caducidad de los distintivos.

    python pipeline/test_caducidades.py

POR QUE EXISTE ESTE FICHERO

Varias ordenanzas escalonan las restricciones: el distintivo B deja de entrar
en Malaga el 30/11/2026, en Palma el 01/01/2027 y en Valladolid el 31/12/2027.
Esas fechas estan en el front matter, en `caducan`, y hay tres cosas que las
leen, cada una en un momento distinto:

  la herramienta       en el navegador, con la fecha del dia. Se entera sola
  la tabla comparativa al compilar. Desde el 06/10/2026 compara con `now`,
                       asi que tambien se entera sola
  el TEXTO de la ficha nunca. Lo escribio una persona y dice cosas como
                       «Hoy entran 0, ECO, C y B»

El dia que una fecha pasa, las dos primeras cambian solas y la tercera se
queda mintiendo. Y nadie recibe un aviso: no hay error, el build termina en
verde y la pagina sigue publicada diciendo lo de ayer.

Esta prueba es ese aviso. Falla el dia siguiente a cada caducidad y obliga a
tocar la ficha a mano, que es lo unico que no se puede automatizar.
"""

import datetime
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHAS = os.path.join(RAIZ, "content", "zbe")

# Como se escribe cada clave de `caducan` en las listas de distintivos.
EQUIVALE = {"sin": "sin distintivo"}


def _fichas():
    for nombre in sorted(os.listdir(FICHAS)):
        if not nombre.endswith(".md") or nombre.startswith("_"):
            continue
        ruta = os.path.join(FICHAS, nombre)
        yield nombre[:-3], io.open(ruta, encoding="utf-8-sig").read()


def _caducidades(texto):
    """[(clave, fecha)] de los bloques `caducan:` del front matter."""
    cabecera = re.match(r"^---\s*?\n(.*?)\n---\s*?\n", texto, re.S)
    if not cabecera:
        return []
    salida = []
    dentro = False
    for linea in cabecera.group(1).splitlines():
        if re.match(r"^\s*caducan:\s*$", linea):
            dentro = True
            continue
        if dentro:
            m = re.match(r"^\s+([A-Za-z0]+):\s*\"?(\d{4}-\d{2}-\d{2})\"?", linea)
            if m:
                salida.append((m.group(1), datetime.date.fromisoformat(m.group(2))))
                continue
            if linea.strip() and not linea.startswith((" ", "\t", "#")):
                dentro = False
    return salida


def _distintivos_listados(texto):
    """Todo lo que aparece en cualquier lista de distintivos de la ficha."""
    cabecera = re.match(r"^---\s*?\n(.*?)\n---\s*?\n", texto, re.S)
    if not cabecera:
        return set()
    listados = set()
    for m in re.finditer(r"(?:etiquetas_permitidas|distintivos_permitidos):\s*\[([^\]]*)\]",
                         cabecera.group(1)):
        for trozo in m.group(1).split(","):
            valor = trozo.strip().strip('"').strip("'").strip()
            if valor:
                listados.add(valor.lower())
    return listados


def test_se_leen_las_caducidades():
    """Si esto falla, la prueba de abajo no esta mirando nada."""
    total = sum(len(_caducidades(t)) for _, t in _fichas())
    assert total >= 4, (
        "se esperaban al menos cuatro fechas de caducidad declaradas en las "
        "fichas; se han encontrado %d" % total)


def test_ninguna_ficha_sigue_admitiendo_un_distintivo_caducado():
    """
    El dia despues de una caducidad, esta prueba falla.

    No es un fallo del codigo: es el recordatorio de que hay que reescribir el
    texto de esa ficha, que sigue diciendo «hoy entran...» con una lista que
    ya no es la de hoy.
    """
    hoy = datetime.date.today()
    vencidos = []
    for nombre, texto in _fichas():
        listados = _distintivos_listados(texto)
        for clave, fecha in _caducidades(texto):
            if fecha > hoy:
                continue
            buscado = EQUIVALE.get(clave.lower(), clave.lower())
            if any(d.startswith(buscado) for d in listados):
                vencidos.append("%s: el distintivo %s caduco el %s y sigue en la lista"
                                % (nombre, clave, fecha))
    assert not vencidos, (
        "Hay que actualizar estas fichas A MANO, incluido su texto:\n  %s\n"
        "La tabla comparativa y la herramienta ya se enteran solas; lo que no "
        "se entera es la prosa, que dira «hoy entran» con la lista de ayer."
        % "\n  ".join(vencidos))


def _ejecutar():
    nombres = [n for n in globals() if n.startswith("test_")]
    fallos = 0
    for nombre in sorted(nombres):
        try:
            globals()[nombre]()
            print("  OK   %s" % nombre)
        except Exception as e:
            fallos += 1
            print("  FALLA %s: %s" % (nombre, e))
    print("%d de %d" % (len(nombres) - fallos, len(nombres)))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(_ejecutar())
