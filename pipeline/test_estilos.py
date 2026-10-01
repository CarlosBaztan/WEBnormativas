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


# ---------------------------------------------------------------------------
# ESCALA TIPOGRAFICA
#
# El sitio tiene siete tamanos de letra y ni uno mas: 13, 15, 17, 19, 22, 26
# y 34 px, declarados como --txt-xs .. --txt-3xl en sistema.css.
#
# El 02/10/2026 se midieron 1.513 elementos de texto en 17 paginas y
# aparecieron cuatro tamanos que no estaban en esa lista, los cuatro
# heredados de PaperMod: titulares de listado a 40 px (mas grandes que los de
# las fichas), pies de figura a 16 px (por encima de las notas, que van a 15)
# y `code` en 0.78em, que dentro de una nota caia a 11,7 px.
#
# La leccion no es "revisar la escala de vez en cuando". Es que un tamano
# fuera de escala no se ve leyendo el CSS propio, porque viene del tema, y
# solo aparece midiendo la pagina ya montada. Lo que si puede vigilar una
# maquina es que NOSOTROS no metamos valores absolutos nuevos.
# ---------------------------------------------------------------------------

TOKENS_DE_TEXTO = ("--txt-xs", "--txt-sm", "--txt-md", "--txt-lg",
                   "--txt-xl", "--txt-2xl", "--txt-3xl")

# Reglas del tema que estaban fuera de la escala y que pisamos a proposito.
# Si alguien borra una de estas lineas, vuelve el tamano del tema sin avisar.
RESCATES = {
    ".page-header h1": "titulares de las paginas de listado, que venian a 40 px",
    "figcaption": "pies de figura, que venian a 16 px",
    "code": "`code`, que venia en 0.78em y caia a 11,7 px dentro de una nota",
    ".breadcrumbs": "migas de pan, que venian a 16 px",
}


def test_la_escala_tiene_siete_pasos_y_vive_en_sistema():
    """Los siete tokens, declarados y en un solo sitio."""
    ruta = os.path.join(CSS, "sistema.css")
    texto = _sin_comentarios(io.open(ruta, encoding="utf-8").read(), "css")
    for token in TOKENS_DE_TEXTO:
        assert ("%s:" % token) in texto,             "sistema.css no declara %s" % token
    for nombre, otro in _ficheros(CSS, ".css"):
        if nombre == "sistema.css":
            continue
        for token in TOKENS_DE_TEXTO:
            assert ("%s:" % token) not in otro,                 "%s vuelve a declarar %s; los tokens van solo en sistema.css" % (nombre, token)


def test_ningun_tamano_de_letra_absoluto_fuera_de_sistema():
    """
    Un `font-size: 16px` suelto se sale de la escala y nadie lo nota.

    Se permiten los relativos (`1em`, `0.8em`): esos heredan del padre a
    proposito, que es otra intencion distinta de fijar un tamano.
    """
    for nombre, texto in _ficheros(CSS, ".css"):
        if nombre == "sistema.css":
            continue
        for valor in re.findall(r"font-size:\s*([^;}]+)", texto):
            valor = valor.strip()
            if valor.startswith("var(--txt-"):
                continue
            if re.fullmatch(r"[0-9.]+em", valor):
                continue
            raise AssertionError(
                "%s fija font-size: %s. Usa uno de los siete tokens "
                "(%s) o un valor en em si lo que quieres es heredar."
                % (nombre, valor, ", ".join(TOKENS_DE_TEXTO)))


def test_siguen_pisadas_las_reglas_del_tema_fuera_de_escala():
    """
    PaperMod trae tamanos que no son de nuestra escala. Estan corregidos, y
    esto comprueba que las correcciones no se hayan borrado.
    """
    todo = "".join(t for _, t in _ficheros(CSS, ".css"))
    for selector, porque in RESCATES.items():
        assert selector in todo, (
            "ya no se corrige %s (%s). Sin esa regla vuelve el tamano del "
            "tema, que no esta en la escala del sitio." % (selector, porque))


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
