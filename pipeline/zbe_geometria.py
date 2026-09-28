# -*- coding: utf-8 -*-
"""
Extrae la geometria de las Zonas de Bajas Emisiones del NAP de la DGT.

Los ficheros DATEX2 ya descargados por zbe_nap.py en pipeline/estado/cache/
contienen los perimetros dentro de <loc:openlrPolygonCorners>. zbe_nap.py los
descarta porque solo le interesan las reglas; aqui se aprovechan.

Es el activo diferencial del proyecto: ningun competidor publica los poligonos.
Licencia CC-BY de la DGT, asi que la atribucion es obligatoria alli donde se
pinten.
"""

# Rectangulo que contiene Espana entera: peninsula, Baleares, Canarias, Ceuta
# y Melilla, con margen. Cualquier punto fuera es un error de lectura, no un
# municipio exotico.
import os

LIMITES = {"lat": (27.0, 44.0), "lon": (-19.0, 5.0)}


def _dentro(lat, lon):
    return (LIMITES["lat"][0] <= lat <= LIMITES["lat"][1]
            and LIMITES["lon"][0] <= lon <= LIMITES["lon"][1])


def verificar_punto(lat, lon, contexto=""):
    """
    Revienta si el punto no cae en Espana.

    Distingue dos casos, porque la causa y el arreglo son distintos:
      - Encaja al darle la vuelta: latitud y longitud estan invertidas. Es el
        error habitual, porque DATEX2 las da por separado y GeoJSON las quiere
        como [longitud, latitud], al reves de como se leen en voz alta.
      - No encaja de ninguna manera: el dato de origen esta mal o se esta
        leyendo la etiqueta equivocada.
    """
    if _dentro(lat, lon):
        return
    if _dentro(lon, lat):
        raise ValueError(
            "%s: el punto (%s, %s) cae fuera de Espana, pero encaja al darle la "
            "vuelta. Latitud y longitud estan invertidas." % (contexto, lat, lon))
    raise ValueError(
        "%s: el punto (%s, %s) cae fuera de Espana y tampoco encaja invertido."
        % (contexto, lat, lon))


import xml.etree.ElementTree as ET

# El prefijo loc: es el mismo en los 50 ficheros del cache, comprobado.
NS = {"loc": "http://levelC/schema/3/locationReferencing"}


def anillos_de_fichero(ruta):
    """
    Devuelve los anillos del fichero, cada uno como lista de pares
    [longitud, latitud].

    Cada <loc:openlrPolygonCorners> es un anillo: A Coruna tiene tres, con
    1.026 puntos entre los tres.

    El orden es [lon, lat] y no [lat, lon] porque es lo que exige GeoJSON, al
    reves de como lo da DATEX2 y al reves de como se dice en voz alta. Cada
    punto pasa por verificar_punto, que revienta si el par acaba invertido.
    """
    raiz = ET.parse(ruta).getroot()
    nombre = os.path.basename(ruta)
    anillos = []

    for corners in raiz.iter("{%s}openlrPolygonCorners" % NS["loc"]):
        anillo = []
        for par in corners.findall("loc:openlrCoordinates", NS):
            lat = float(par.findtext("loc:latitude", namespaces=NS))
            lon = float(par.findtext("loc:longitude", namespaces=NS))
            verificar_punto(lat, lon, nombre)
            anillo.append([lon, lat])

        # GeoJSON exige el anillo cerrado. El NAP no siempre lo cierra.
        if anillo and anillo[0] != anillo[-1]:
            anillo.append(list(anillo[0]))

        if len(anillo) >= 4:
            anillos.append(anillo)

    return anillos
