# -*- coding: utf-8 -*-
"""
Tests de pipeline/zbe_geometria.py.

El proyecto no usa framework de tests: se ejecuta con
    python pipeline/test_zbe_geometria.py
y devuelve codigo 1 si algo falla, para poder encadenarlo con auditoria.py.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import zbe_geometria as zg


def test_punto_de_a_coruna_se_acepta():
    """43.36 N, 8.39 O es el centro de A Coruna. Tiene que pasar."""
    zg.verificar_punto(43.369015, -8.39335, "A Coruna")


def test_coordenadas_invertidas_se_rechazan():
    """
    El error clasico: DATEX2 da latitud y longitud por separado y GeoJSON las
    quiere al reves. Si se copian en el orden que vienen, las ZBE espanolas
    acaban en el oceano Indico. Esto tiene que reventar, no pasar.
    """
    try:
        zg.verificar_punto(-8.39335, 43.369015, "A Coruna")
    except ValueError as e:
        assert "invert" in str(e).lower(), \
            "el mensaje debe apuntar a la inversion, no solo decir que esta fuera: %s" % e
    else:
        raise AssertionError("un punto con latitud y longitud intercambiadas debe rechazarse")


def test_punto_de_canarias_se_acepta():
    """Las islas no pueden quedarse fuera del rectangulo de validacion."""
    zg.verificar_punto(28.1, -15.4, "Las Palmas")


CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estado", "cache")


def test_a_coruna_produce_al_menos_un_anillo():
    anillos = zg.anillos_de_fichero(os.path.join(CACHE, "a-coruna.xml"))
    assert len(anillos) >= 1, "el fichero tiene 2.052 coordenadas, algo tiene que salir"


def test_el_orden_de_cada_par_es_lon_lat():
    """
    GeoJSON quiere [longitud, latitud], al reves de como se lee en voz alta y
    al reves de como lo da DATEX2. A Coruna esta en 43 N, 8 O: si sale al
    reves, el primer numero seria 43 y estaria mal.
    """
    anillo = zg.anillos_de_fichero(os.path.join(CACHE, "a-coruna.xml"))[0]
    lon, lat = anillo[0]
    assert -19.0 <= lon <= 5.0, "el primer numero debe ser la longitud, no %s" % lon
    assert 27.0 <= lat <= 44.0, "el segundo numero debe ser la latitud, no %s" % lat


def test_los_anillos_estan_cerrados():
    """GeoJSON exige que el primer punto y el ultimo coincidan."""
    for anillo in zg.anillos_de_fichero(os.path.join(CACHE, "a-coruna.xml")):
        assert anillo[0] == anillo[-1], "anillo sin cerrar"


def test_un_anillo_tiene_al_menos_cuatro_puntos():
    """Tres vertices mas el cierre. Con menos no es un poligono."""
    for anillo in zg.anillos_de_fichero(os.path.join(CACHE, "a-coruna.xml")):
        assert len(anillo) >= 4, "anillo de %d puntos" % len(anillo)


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
