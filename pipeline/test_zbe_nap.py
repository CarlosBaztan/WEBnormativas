# -*- coding: utf-8 -*-
"""
Tests de pipeline/zbe_nap.py.

Como el resto del pipeline, sin framework:
    python pipeline/test_zbe_nap.py

Aqui solo se prueba el nombrado de municipios. El parseo DATEX2 no se prueba a
proposito: lo que ese codigo extrae no se publica (ver el hallazgo del 22/09
sobre la codificacion inconsistente del NAP), asi que no hay contrato que
proteger.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import zbe_nap as zn


# XML deliberadamente roto: `analizar` devuelve el registro base con la
# incidencia puesta, que es justo la parte que interesa aqui. Asi los tests no
# dependen de tener la cache descargada.
ROTO = "<esto no es xml"


def _registro(nombre):
    return zn.analizar(ROTO, nombre, "https://nap.dgt.es/ejemplo.xml")


def test_gerona_se_publica_con_las_dos_formas():
    """
    Castellano primero y lengua propia despues: quien busca "ZBE Gerona" y
    quien busca "ZBE Girona" tienen que encontrar la misma pagina.
    """
    assert _registro("Girona")["municipio"] == "Gerona / Girona"


def test_lerida_se_publica_con_las_dos_formas():
    assert _registro("Lleida")["municipio"] == "Lérida / Lleida"


def test_san_sebastian_se_publica_con_las_dos_formas():
    """
    El NAP lo llama "Donostia - San Sebastián", con la forma vasca delante.
    Se invierte el orden y se quita el guion.
    """
    assert _registro("Donostia - San Sebastián")["municipio"] == "San Sebastián / Donostia"


def test_un_municipio_con_un_solo_nombre_no_se_toca():
    r = _registro("Granada")
    assert r["municipio"] == "Granada"
    assert r["slug"] == "granada"


def test_ningun_nombre_bilingue_cambia_el_slug():
    """
    La trampa que ya costo tres cruces rotos en silencio: el slug sale del
    nombre, y el nombre acaba de cambiar. Si al anteponer la forma castellana
    el slug pasara de "girona" a "gerona-girona", cambiarian la clave de
    data/zbe.json, el nombre del fichero de cache y el slug del GeoJSON, y el
    mapa dejaria de encontrar su ficha. El nombre que se muestra y el
    identificador con el que se cruzan los datos van por separado.
    """
    for original in zn.NOMBRES_BILINGUES:
        r = _registro(original)
        assert r["slug"] == zn.slug(original), \
            "%s: el slug paso a %r y deberia seguir siendo %r" % (
                original, r["slug"], zn.slug(original))


def test_los_slugs_bilingues_son_los_que_ya_estan_publicados():
    """
    Comprobacion de la de arriba con los valores literales, por si algun dia
    cambia `slug()`: estos tres son los que ya estan en data/zbe.json, en el
    GeoJSON y en los ficheros de cache.
    """
    esperados = {
        "Girona": "girona",
        "Lleida": "lleida",
        "Donostia - San Sebastián": "donostia-san-sebastian",
    }
    for original, slug_esperado in esperados.items():
        assert _registro(original)["slug"] == slug_esperado, original


def test_sin_red_no_estampa_una_fecha_de_descarga_nueva():
    """
    Con --sin-red no se baja nada: el XML que se analiza es el de la ultima
    descarga de verdad. Poner la fecha de hoy diria que el dato se ha vuelto a
    comprobar hoy, y eso es justo lo que este proyecto no puede decir sin
    haberlo hecho.
    """
    previas = {"girona": "2026-09-23"}
    reg = {"slug": "girona", "fecha_descarga": "2026-12-31"}
    zn.conservar_fecha_de_descarga(reg, previas)
    assert reg["fecha_descarga"] == "2026-09-23"


def test_un_municipio_que_no_estaba_antes_se_queda_con_la_fecha_de_hoy():
    """Si no hay fecha anterior, la de hoy es lo unico que se sabe."""
    previas = {"girona": "2026-09-23"}
    reg = {"slug": "manlleu", "fecha_descarga": "2026-12-31"}
    zn.conservar_fecha_de_descarga(reg, previas)
    assert reg["fecha_descarga"] == "2026-12-31"


def test_las_fechas_previas_se_leen_del_json_publicado():
    previas = zn.fechas_de_descarga_previas()
    assert previas.get("a-coruna"), "data/zbe.json deberia traer la fecha de A Coruna"


def test_la_coruna_se_publica_con_las_dos_formas():
    """
    05/10/2026, al publicar su ficha. Mismo caso que Gerona y Lerida: la forma
    oficial es la gallega y la mayoria escribe la castellana, asi que en el
    dataset y en el listado van las dos, castellano primero.
    """
    assert _registro("A Coruña")["municipio"] == "La Coruña / A Coruña"


def _ejecutar():
    fallos = 0
    for nombre, fn in sorted(globals().items()):
        if not nombre.startswith("test_"):
            continue
        try:
            fn()
            print("  OK   %s" % nombre)
        except Exception as e:
            fallos += 1
            print("  FALLA %s: %s" % (nombre, e))
    print("%d de %d" % (
        sum(1 for n in globals() if n.startswith("test_")) - fallos,
        sum(1 for n in globals() if n.startswith("test_"))))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(_ejecutar())
