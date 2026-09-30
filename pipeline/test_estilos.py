# -*- coding: utf-8 -*-
"""
Tests del sistema visual.

    python pipeline/test_estilos.py

No prueban como se ve nada, que eso hay que mirarlo. Prueban que cada decision
de diseno este escrita en un solo sitio, que es lo unico que una maquina puede
vigilar y lo primero que se rompe cuando hay prisa.
"""

import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = os.path.join(RAIZ, "assets", "css", "extended")
JS = os.path.join(RAIZ, "assets", "js")

# Los tres colores del mapa. No son decorativos: distinguen una zona con la
# ordenanza leida de una que solo consta en el registro de la DGT, que es la
# diferencia entre "puedes fiarte" y "compruebalo tu".
PALETA_MAPA = ("#d6006e", "#d35400", "#7209b7")


def _sin_comentarios(texto, estilo):
    """Quita los comentarios, que mencionan colores sin usarlos."""
    if estilo == "css":
        return re.sub(r"/\*.*?\*/", "", texto, flags=re.S)
    texto = re.sub(r"/\*.*?\*/", "", texto, flags=re.S)
    return re.sub(r"^\s*//.*$", "", texto, flags=re.M)


def _ficheros(carpeta, extension):
    for nombre in sorted(os.listdir(carpeta)):
        if nombre.endswith(extension):
            ruta = os.path.join(carpeta, nombre)
            yield nombre, _sin_comentarios(
                io.open(ruta, encoding="utf-8").read(),
                "css" if extension == ".css" else "js")


def test_cada_color_del_mapa_se_declara_una_sola_vez_en_el_css():
    """
    El color con el que se pinta una zona estaba escrito cuatro veces: en la
    leyenda del CSS y en los dos ficheros de mapa del JavaScript. El comentario
    que habia encima decia "si cambian alli, cambian aqui", que es un contrato
    que se cumple hasta el dia que no.

    Si la leyenda y el mapa dejan de coincidir, la leyenda miente sobre lo
    unico que el mapa tiene que comunicar.
    """
    for color in PALETA_MAPA:
        sitios = []
        for nombre, texto in _ficheros(CSS, ".css"):
            for linea in texto.splitlines():
                if color in linea.lower():
                    sitios.append("%s: %s" % (nombre, linea.strip()[:70]))
        assert len(sitios) == 1, \
            "%s aparece en %d sitios del CSS y deberia estar solo en sistema.css:\n   %s" % (
                color, len(sitios), "\n   ".join(sitios))
        assert sitios[0].startswith("sistema.css"), \
            "%s se declara en %s y su sitio es sistema.css" % (color, sitios[0])


def test_el_javascript_del_mapa_lee_el_color_del_css():
    """
    Los dos mapas piden el color a la variable CSS en vez de traerlo escrito.
    """
    for nombre in ("mapa-zbe.js", "mapa-municipio.js"):
        texto = _sin_comentarios(
            io.open(os.path.join(JS, nombre), encoding="utf-8").read(), "js")
        assert "--mapa-" in texto, \
            "%s no lee ninguna variable --mapa-*; estara pintando con un color escrito a mano" % nombre


def test_el_color_de_reserva_del_javascript_no_se_desvia_del_token():
    """
    En el JavaScript se permite un color escrito, y solo uno: el valor de
    reserva para cuando la hoja de estilos aun no ha llegado. Sin el, la
    variable viene vacia y Leaflet pinta las zonas de negro sin avisar.

    Lo que no se permite es que ese respaldo se quede atras. Si alguien cambia
    el token y no el respaldo, vuelve el problema que esto venia a resolver,
    solo que mas dificil de ver: fallaria unicamente en las cargas lentas.
    """
    declarados = io.open(os.path.join(CSS, "sistema.css"), encoding="utf-8").read().lower()
    for nombre, texto in _ficheros(JS, ".js"):
        for hex_encontrado in set(re.findall(r"#[0-9a-f]{6}", texto.lower())):
            assert hex_encontrado in declarados, \
                "%s usa %s y ese color no esta declarado en sistema.css" % (nombre, hex_encontrado)


def test_los_colores_del_mapa_son_variables_css():
    """Y la declaracion esta donde se puede encontrar: el fichero de tokens."""
    ruta = os.path.join(CSS, "sistema.css")
    assert os.path.exists(ruta), "falta assets/css/extended/sistema.css"
    texto = io.open(ruta, encoding="utf-8").read()
    for token in ("--mapa-verificado", "--mapa-parcial", "--mapa-pendiente"):
        assert token in texto, "sistema.css no declara %s" % token


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
