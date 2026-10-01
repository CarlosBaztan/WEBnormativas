# -*- coding: utf-8 -*-
"""
Tests de los iconos del sitio.

    python pipeline/test_marca_favicon.py

POR QUE EXISTE ESTE FICHERO

Un icono roto no rompe el build ni sale en ningun aviso: la pestanya pone el
globo gris de siempre y nadie lo relaciona con el despliegue de ayer. Eso ya
paso: head.html declaraba cinco iconos y no existia ninguno de los cinco.

Lo que se vigila aqui:

  - que todo icono declarado exista,
  - que el tamanyo que se declara sea el real,
  - que sean cuadrados, porque Google solo acepta 1:1,
  - y que los ficheros de static/ sean de verdad los que produce
    pipeline/marca_favicon.py a partir del logotipo.

La ultima es la que mas sujeta. Sin ella, cualquiera puede dejar caer un PNG
a mano en static/ y a partir de ahi el script documentado y el fichero que se
sirve dicen cosas distintas, sin que se note hasta que alguien vuelva a
ejecutar el script meses despues y se pregunte por que cambia el icono.
"""

import io
import os
import re
import sys

from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "pipeline"))

import marca_favicon  # noqa: E402

HEAD = os.path.join(RAIZ, "layouts", "partials", "head.html")
STATIC = os.path.join(RAIZ, "static")


def _iconos_declarados():
    """
    Devuelve [(fichero, (ancho, alto) o None)] leyendo head.html.

    Las lineas tienen esta forma, con el nombre dentro del `default`:
      <link rel="icon" type="image/png" sizes="16x16"
            href="{{ site.Params.assets.favicon16x16
                     | default "favicon-16x16.png" | absURL }}">
    """
    texto = io.open(HEAD, encoding="utf-8").read()
    salida = []
    for linea in re.findall(r"<link[^>]*rel=\"(?:icon|apple-touch-icon)\"[^>]*>",
                            texto):
        fichero = re.search(r"default\s+\"([^\"]+)\"", linea)
        if not fichero:
            continue
        medida = re.search(r"sizes=\"(\d+)x(\d+)\"", linea)
        salida.append((fichero.group(1),
                       (int(medida.group(1)), int(medida.group(2)))
                       if medida else None))
    return salida


def test_head_declara_los_iconos():
    """Si esto falla, el resto de los tests no prueban nada."""
    declarados = _iconos_declarados()
    assert len(declarados) >= 4, (
        "head.html solo declara %d iconos; se esperaban al menos cuatro "
        "(ico, 16, 32 y apple-touch)." % len(declarados)
    )


def test_todo_icono_declarado_existe():
    """La trampa de siempre: declarado en el HTML, ausente en static/."""
    for fichero, _ in _iconos_declarados():
        ruta = os.path.join(STATIC, fichero)
        assert os.path.exists(ruta), (
            "head.html declara %s y no esta en static/. El navegador pinta "
            "el globo generico y el build termina en verde." % fichero
        )


def test_el_tamanyo_declarado_es_el_real():
    """Declarar sizes=32x32 sobre un fichero de otro tamanyo enganya al navegador."""
    for fichero, medida in _iconos_declarados():
        if medida is None:
            continue
        with Image.open(os.path.join(STATIC, fichero)) as im:
            assert im.size == medida, (
                "head.html dice que %s mide %dx%d y mide %dx%d"
                % (fichero, medida[0], medida[1], im.width, im.height)
            )


def test_los_iconos_son_cuadrados():
    """Google exige proporcion 1:1; un icono rectangular no se muestra."""
    for fichero, _ in _iconos_declarados():
        with Image.open(os.path.join(STATIC, fichero)) as im:
            assert im.width == im.height, (
                "%s mide %dx%d y Google solo acepta cuadrados"
                % (fichero, im.width, im.height)
            )


def test_el_ico_lleva_los_tres_tamanyos():
    """
    16 para la pestanya, 32 para pantallas densas y 48 porque es lo que
    Google recomienda tener por encima de 48 para otras superficies.
    """
    with Image.open(os.path.join(STATIC, "favicon.ico")) as ico:
        tiene = set(ico.info.get("sizes", []))
    for medida in ((16, 16), (32, 32), (48, 48)):
        assert medida in tiene, (
            "favicon.ico no trae el fotograma de %dx%d; tiene %s"
            % (medida[0], medida[1], sorted(tiene))
        )


def test_los_iconos_salen_del_logotipo():
    """
    Los PNG de static/ deben ser pixel a pixel los que genera el script.

    Se comparan pixeles y no bytes a proposito: dos versiones de Pillow pueden
    comprimir el mismo PNG de forma distinta, y eso no es un fallo.
    """
    f16, f32, f48, f180 = marca_favicon.construir()
    esperados = {
        "favicon-16x16.png": f16,
        "favicon-32x32.png": f32,
        "apple-touch-icon.png": f180,
    }
    for fichero, generado in esperados.items():
        with Image.open(os.path.join(STATIC, fichero)) as guardado:
            a = guardado.convert("RGB").tobytes()
        b = generado.convert("RGB").tobytes()
        distintos = sum(1 for x, y in zip(a[::3], b[::3]) if x != y)
        assert a == b, (
            "static/%s no coincide con lo que produce marca_favicon.py "
            "(al menos %d pixeles distintos de %d). O se edito a mano, o se "
            "cambio el script y no se regeneraron los iconos: "
            "python pipeline/marca_favicon.py"
            % (fichero, distintos, len(a) // 3)
        )


def test_el_fotograma_de_16_usa_el_coche_macizo():
    """
    A 16 px el coche se dibuja sin los bujes ni la ventanilla, porque a ese
    tamanyo esos huecos no se leen: se promedian con el negro y dejan una
    mancha gris. El fotograma de 16 debe salir de esa version, no del
    detallado, y eso se nota en cuanto negro solido queda en pie.
    """
    f16, _, _, _ = marca_favicon.construir()
    crudo = f16.convert("RGB").tobytes()
    pixeles = zip(crudo[0::3], crudo[1::3], crudo[2::3])
    solido = sum(1 for r, g, b in pixeles if max(r, g, b) < 110)
    assert solido >= 16, (
        "el icono de 16 px solo conserva %d pixeles de negro solido. El coche "
        "se esta deshaciendo: comprueba que cuadra() recibe la version maciza "
        "y que el margen no ha crecido." % solido
    )


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
