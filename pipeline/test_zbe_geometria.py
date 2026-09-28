# -*- coding: utf-8 -*-
"""
Tests de pipeline/zbe_geometria.py.

El proyecto no usa framework de tests: se ejecuta con
    python pipeline/test_zbe_geometria.py
y devuelve codigo 1 si algo falla, para poder encadenarlo con auditoria.py.
"""

import io
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


def test_simplificar_quita_un_punto_alineado():
    """
    Tres puntos en linea recta: el del medio no aporta forma y sobra.
    Es el caso mas simple de Ramer-Douglas-Peucker.
    """
    cuadrado = [[0, 0], [1, 0], [2, 0], [2, 2], [0, 2], [0, 0]]
    salida = zg.simplificar(cuadrado, 0.1)
    assert [1, 0] not in salida, "el punto alineado deberia desaparecer: %s" % salida
    assert [2, 0] in salida, "las esquinas se quedan"


def test_simplificar_reduce_un_anillo_real():
    anillo = zg.anillos_de_fichero(os.path.join(CACHE, "a-coruna.xml"))[0]
    salida = zg.simplificar(anillo, 0.0001)
    assert len(salida) < len(anillo), "de %d puntos no bajo nada" % len(anillo)


def test_simplificar_deja_el_anillo_cerrado():
    anillo = zg.anillos_de_fichero(os.path.join(CACHE, "a-coruna.xml"))[0]
    salida = zg.simplificar(anillo, 0.001)
    assert salida[0] == salida[-1], "la simplificacion abrio el anillo"


def test_simplificar_nunca_baja_de_cuatro_puntos():
    """
    Con una tolerancia brutal el algoritmo tenderia a dejar dos puntos, y eso
    ya no es un poligono valido en GeoJSON.
    """
    anillo = zg.anillos_de_fichero(os.path.join(CACHE, "a-coruna.xml"))[0]
    salida = zg.simplificar(anillo, 99.0)
    assert len(salida) >= 4, "quedaron %d puntos" % len(salida)


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _coleccion():
    if not hasattr(_coleccion, "cache"):
        _coleccion.cache = zg.construir_geojson()
    return _coleccion.cache


def test_la_coleccion_es_un_featurecollection():
    c = _coleccion()
    assert c["type"] == "FeatureCollection"
    assert len(c["features"]) >= 40, "solo %d zonas" % len(c["features"])


def test_cada_feature_trae_lo_que_consume_el_mapa():
    """
    Contrato con T7 (mapa general), T8 (mapa por ficha) y T10 (mi calle).
    Si falta una de estas claves, esas tres tareas se rompen.
    """
    for f in _coleccion()["features"]:
        for clave in ("slug", "municipio", "estado_dato", "fuente_url", "fecha_descarga"):
            assert clave in f["properties"], "falta %s en %s" % (clave, f["properties"])


def test_los_slugs_coinciden_con_los_de_zbe_json():
    """
    Si los slugs no cuadran, el mapa enlaza a fichas que no existen. Es el
    unico punto donde las dos mitades del proyecto se tienen que encontrar.
    """
    import json
    datos = json.load(io.open(os.path.join(RAIZ, "data", "zbe.json"), encoding="utf-8"))
    conocidos = set(datos["municipios"].keys())
    for f in _coleccion()["features"]:
        s = f["properties"]["slug"]
        assert s in conocidos, "el slug %s no esta en data/zbe.json" % s


def test_la_geometria_es_un_poligono_valido():
    for f in _coleccion()["features"]:
        g = f["geometry"]
        assert g["type"] in ("Polygon", "MultiPolygon"), g["type"]
        anillos = g["coordinates"] if g["type"] == "Polygon" else [
            a for poly in g["coordinates"] for a in poly]
        for anillo in anillos:
            assert len(anillo) >= 4, "anillo de %d puntos" % len(anillo)
            assert anillo[0] == anillo[-1], "anillo sin cerrar"


def test_la_ficha_se_enlaza_solo_si_existe():
    """
    Madrid tiene ficha publicada; un municipio sin verificar no. Inventar la
    URL daria 404 desde el mapa.
    """
    por_slug = {f["properties"]["slug"]: f["properties"] for f in _coleccion()["features"]}
    assert por_slug["madrid"].get("url_ficha") == "/zbe/madrid/", por_slug["madrid"].get("url_ficha")


def test_alicante_descarta_los_anillos_proyectados():
    """
    Regresion de un hallazgo real del 28/09/2026: alicante.xml mezcla dos
    sistemas de coordenadas dentro del mismo fichero. 26 de sus 47 puntos
    vienen en UTM (metros) y el resto en grados. El XML no declara cual es
    cual.

    No se convierten: adivinar la proyeccion dibujaria la zona en otro sitio,
    que es peor que no dibujarla. Se descarta el anillo entero y se registra.
    """
    incidencias = []
    anillos = zg.anillos_de_fichero(
        os.path.join(CACHE, "alicante.xml"), incidencias)
    assert incidencias, "descartar un anillo sin decirlo es esconder el problema"
    assert "alicante" in " ".join(incidencias).lower()
    for anillo in anillos:
        for lon, lat in anillo:
            assert -19.0 <= lon <= 5.0 and 27.0 <= lat <= 44.0,                 "se colo un punto proyectado: %s" % ([lon, lat],)


def test_un_fichero_sano_no_genera_incidencias():
    incidencias = []
    zg.anillos_de_fichero(os.path.join(CACHE, "a-coruna.xml"), incidencias)
    assert incidencias == [], incidencias


def test_la_coleccion_registra_lo_descartado():
    c = _coleccion()
    assert "incidencias" in c["_meta"], "el dato abierto tiene que decir que se dejo fuera"


# Posiciones reales, para contrastar que cada zona cae donde debe. Si alguien
# invierte un par de coordenadas o se cuela una proyeccion, esto se entera.
CIUDADES = {
    "madrid": (40.42, -3.70), "valencia": (39.47, -0.38), "bilbao": (43.26, -2.93),
    "granada": (37.18, -3.60), "malaga": (36.72, -4.42), "palma": (39.57, 2.65),
    "a-coruna": (43.36, -8.41),
}


def test_cada_zona_cae_sobre_su_ciudad():
    import math
    por_slug = {f["properties"]["slug"]: f for f in _coleccion()["features"]}
    for slug, (lat_real, lon_real) in CIUDADES.items():
        lat, lon = zg.centroide(por_slug[slug])
        km = math.hypot((lat - lat_real) * 111.0,
                        (lon - lon_real) * 111.0 * math.cos(math.radians(lat)))
        # Diez kilometros de margen: una ZBE grande como la de Madrid tiene su
        # centro desplazado del centro historico, y eso es correcto.
        assert km < 10, "%s sale a %.0f km de donde esta la ciudad" % (slug, km)


def test_madrid_produce_una_zona_por_controlledzone():
    """
    Regresion de un fallo real: el pipeline fusionaba los 52 anillos de Madrid
    en una sola geometria, asi que el mapa pintaba el termino municipal entero
    de un color y las dos ZBEDEP desaparecian debajo.

    El XML ya trae la agrupacion buena: tres <controlledZone>, cada una con su
    nombre. Una zona del mapa es una controlledZone, no un municipio.
    """
    zonas = zg.zonas_de_fichero(os.path.join(CACHE, "madrid.xml"))
    assert len(zonas) == 3, "salen %d zonas, deberian ser 3" % len(zonas)
    nombres = [z["nombre"] for z in zonas]
    assert any("Distrito Centro" in n for n in nombres), nombres
    assert any(u"Elíptica" in n or "Eliptica" in n for n in nombres), nombres


def test_la_zbe_de_ciudad_y_las_zbedep_tienen_tamanos_muy_distintos():
    """
    Lo que hace util el mapa: la zona municipal es dos ordenes de magnitud
    mayor que las de especial proteccion. Si se pintan igual, no se ven.
    """
    zonas = {z["nombre"]: z for z in zg.zonas_de_fichero(os.path.join(CACHE, "madrid.xml"))}
    grande = max(zonas.values(), key=lambda z: zg.extension_km2(z))
    pequena = min(zonas.values(), key=lambda z: zg.extension_km2(z))
    assert zg.extension_km2(grande) > 50 * zg.extension_km2(pequena),         "%.1f km2 frente a %.1f km2" % (zg.extension_km2(grande), zg.extension_km2(pequena))


def test_cada_zona_sabe_de_que_municipio_es():
    """El slug del municipio es lo que une el mapa con la ficha."""
    for z in zg.zonas_de_fichero(os.path.join(CACHE, "madrid.xml")):
        assert z["slug_municipio"] == "madrid", z


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
