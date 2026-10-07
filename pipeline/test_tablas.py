# -*- coding: utf-8 -*-
"""
Tests de las tablas con <colgroup>.

    python pipeline/test_tablas.py

POR QUE EXISTE ESTE FICHERO

El navegador asocia cada <col> de un <colgroup> a una columna POR POSICION,
no por su clase. Eso tiene dos consecuencias que no se ven leyendo el codigo:

  1. Si sobra un <col>, los anchos se desplazan uno a la derecha a partir de
     ahi, y el ultimo se lo lleva una columna que no existe.
  2. Si los porcentajes suman menos de 100, la tabla deja hueco muerto a la
     derecha AUNQUE lleve `width: 100%`, porque ninguna columna reclama el
     resto. Si suman mas, el navegador los reescala y los numeros escritos
     dejan de ser los reales.

Paso el 02/10/2026. Al retirar la columna «Fuente oficial» de la tabla de
/zbe/ se borraron su <th> y su <td> pero se olvido su <col>. Quedaron cinco
para cuatro columnas: «¿Verificado?» heredo el ancho de col-fuente (15 %) y
el 25 % de col-verificado se lo llevaba una columna fantasma. En pantalla
eran 189 px de tabla vacia a la derecha, y la tabla parecia no llegar al
borde de su recuadro. Lo vio Carlos.

El HTML era valido, el build termino en verde y ninguna prueba fallo. Lo
unico que lo delata es contar.
"""

import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYOUTS = os.path.join(RAIZ, "layouts")
CSS = os.path.join(RAIZ, "assets", "css", "extended")


def _plantillas():
    for carpeta, _, ficheros in os.walk(LAYOUTS):
        for nombre in sorted(ficheros):
            if nombre.endswith(".html"):
                ruta = os.path.join(carpeta, nombre)
                yield (os.path.relpath(ruta, RAIZ).replace("\\", "/"),
                       io.open(ruta, encoding="utf-8").read())


def _sin_comentarios_hugo(texto):
    """Quita los {{/* ... */}}, que mencionan clases sin usarlas."""
    return re.sub(r"\{\{-?\s*/\*.*?\*/\s*-?\}\}", "", texto, flags=re.S)


def test_un_col_por_cada_columna():
    """
    Tantos <col> en el colgroup como <th scope="col"> en la cabecera.

    Es la comprobacion que habria cazado el fallo de la columna «Fuente
    oficial» en el momento de borrarla.
    """
    revisadas = 0
    for nombre, texto in _plantillas():
        texto = _sin_comentarios_hugo(texto)
        for grupo in re.findall(r"<colgroup>(.*?)</colgroup>", texto, re.S):
            cols = len(re.findall(r"<col\b", grupo))
            # La cabecera que sigue a ese colgroup
            resto = texto.split(grupo, 1)[1]
            cabecera = re.search(r"<thead>(.*?)</thead>", resto, re.S)
            assert cabecera, "%s: hay un <colgroup> sin <thead> detras" % nombre
            ths = len(re.findall(r'<th scope="col"', cabecera.group(1)))
            assert cols == ths, (
                "%s declara %d <col> y %d columnas. El navegador los asigna "
                "por posicion, asi que los anchos se desplazan y el sobrante "
                "se lo lleva una columna que no existe."
                % (nombre, cols, ths))
            revisadas += 1
    assert revisadas, "no se ha encontrado ningun <colgroup> que revisar"


def test_los_anchos_de_columna_suman_cien():
    """
    En cada bloque de reglas `.col-*`, los porcentajes suman 100.

    Se mira por bloque (el general y el de cada @media) porque cada uno
    describe una tabla completa por separado.
    """
    hallados = 0
    for fichero in sorted(os.listdir(CSS)):
        if not fichero.endswith(".css"):
            continue
        texto = re.sub(r"/\*.*?\*/", "",
                       io.open(os.path.join(CSS, fichero), encoding="utf-8").read(),
                       flags=re.S)
        # Un "bloque" es cada tramo separado por una llave de apertura de media
        for tramo in re.split(r"@media[^{]*\{", texto):
            anchos = re.findall(r"\.col-[a-z]+\s*\{\s*width:\s*([0-9.]+)%", tramo)
            if not anchos:
                continue
            suma = sum(float(a) for a in anchos)
            assert abs(suma - 100) < 0.5, (
                "%s: un bloque de anchos de columna suma %g %% y no 100. "
                "Si suma menos, la tabla deja hueco muerto a la derecha aunque "
                "lleve width: 100%%; si suma mas, el navegador los reescala."
                % (fichero, suma))
            hallados += 1
    assert hallados >= 2, (
        "se esperaban al menos dos bloques de anchos (el general y el de "
        "movil); se han encontrado %d" % hallados)


def test_toda_tabla_va_en_un_envoltorio_desplazable():
    """
    Una tabla ancha no puede quedarse suelta en la pagina.

    LO QUE PASO EL 07/10/2026, y por que esta prueba mira las tres tablas:

    El sitio resolvia lo mismo de tres maneras distintas, y solo una estaba
    bien.

      render-table.html (tablas de Markdown)  .tabla-envoltorio + tabindex  OK
      tabla-zbe.html    (listado de /zbe/)    .tabla-scroll, sin tabindex    a medias
      tabla-distintivos.html                  nada                           roto

    La rota es la peor de las tres, porque es la tabla que compara que
    distintivo entra en cada ciudad, o sea el argumento del sitio. Medido a
    375 px: la tabla ocupaba 420 px y, sin envoltorio, empujaba el documento
    entero a 434. El movil no desplazaba la tabla, desplazaba la pagina: el
    titular, los parrafos y el pie se iban hacia la derecha y habia que
    arrastrar de lado para leer cualquier cosa.

    La de en medio tenia su desplazamiento pero no se podia enfocar, asi que
    con el teclado no habia forma de llegar a sus columnas de la derecha. Es
    el fallo `scrollable-region-focusable` que axe-core ya canto una vez en la
    ficha de Madrid, corregido entonces en un sitio de los tres.
    """
    sin_envoltorio = []
    for ruta, texto in _plantillas():
        texto = _sin_comentarios_hugo(texto)
        for m in re.finditer(r"<table\b", texto):
            # El envoltorio tiene que ser lo inmediatamente anterior.
            antes = texto[:m.start()]
            div = re.search(r"<div[^>]*>\s*$", antes)
            if not div or 'tabindex="0"' not in div.group(0):
                linea = antes.count("\n") + 1
                sin_envoltorio.append("%s:%d" % (ruta, linea))
    assert not sin_envoltorio, (
        "Estas tablas no van dentro de un envoltorio enfocable, asi que "
        "desbordan la pagina en movil y sus columnas de la derecha quedan "
        "fuera del alcance del teclado: %s" % ", ".join(sin_envoltorio))


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
