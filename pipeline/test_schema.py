# -*- coding: utf-8 -*-
"""
Tests del JSON-LD propio del sitio (layouts/partials/schema.html).

    python pipeline/test_schema.py

POR QUE EXISTE ESTE FICHERO

Que un dato sea valido para schema.org no significa que lo sea para Google.
schema.org hereda `isPartOf` de CreativeWork y acepta cualquier CreativeWork
como valor, y un WebSite lo es. Google, en cambio, publica para cada tipo de
resultado enriquecido su propia lista de tipos esperados, y para un Dataset
solo admite ahi URL o Dataset:

    https://developers.google.com/search/docs/appearance/structured-data/dataset

Paso el 03/10/2026. Search Console aviso de «El tipo de objeto del campo
"isPartOf" no es valido» en los datos estructurados de Conjuntos de datos.
El JSON era correcto, el validador de schema.org lo aceptaba y el build
termino en verde: el unico sitio donde constaba el fallo era el correo.

La propiedad que Google si define para decir a que catalogo pertenece un
dataset es `includedInDataCatalog`, y espera un DataCatalog, que es justo lo
que emite la pagina de seccion /datos/.

Regla que vigilan estas pruebas: el nodo WebSite (`$sitio`) solo puede colgar
de un nodo de la familia WebPage, que es donde Google documenta `isPartOf`.
"""

import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARTIAL = os.path.join(RAIZ, "layouts", "partials", "schema.html")

# Los tipos a los que Google documenta `isPartOf` apuntando a un WebSite.
TIPOS_PAGINA = ("WebPage", "FAQPage", "CollectionPage", "ItemPage",
                "AboutPage", "ContactPage", "ProfilePage", "QAPage")


def _texto():
    return io.open(PARTIAL, encoding="utf-8").read()


def _bloques():
    """
    Un bloque por cada nodo que emite la plantilla.

    El ambito de un nodo no es su `dict`: es todo lo que hay hasta la rama
    siguiente, porque las propiedades se le van anadiendo con `merge` despues
    de declararlo. Mirar solo el `dict` dejaria fuera la mitad del nodo.
    """
    texto = _texto()
    for m in re.finditer(r"\$datos\s*=\s*dict(.*?)-\}\}", texto, re.S):
        linea = re.search(r'"@type".*', m.group(1))
        tipos = re.findall(r'"([A-Z][A-Za-z]*)"', linea.group(0)) if linea else []
        siguiente = texto.find("{{- else", m.end())
        fin = siguiente if siguiente != -1 else len(texto)
        yield (m.start(), fin, texto[m.start():fin], tipos)


def test_cada_bloque_declara_su_tipo():
    """Si esta prueba falla, las otras dos estan midiendo el aire."""
    bloques = list(_bloques())
    assert len(bloques) >= 3, (
        "se esperaban al menos los tres bloques de schema.html (FAQPage, "
        "datos y el general); se han encontrado %d" % len(bloques))
    for _, _, _, tipos in bloques:
        assert tipos, "hay un bloque de $datos sin \"@type\" reconocible"


def test_el_website_solo_cuelga_de_una_pagina():
    """
    `isPartOf` apuntando al WebSite solo vale en la familia WebPage.

    Es la comprobacion que habria cazado el aviso de Search Console: el
    Dataset de /datos/zbe/ colgaba de un WebSite, que Google no admite ahi.
    """
    texto = _texto()
    bloques = list(_bloques())
    hallados = 0
    for m in re.finditer(r'"isPartOf"', texto):
        dentro = [b for b in bloques if b[0] <= m.start() <= b[1]]
        assert dentro, (
            "hay un \"isPartOf\" fuera de los bloques que esta prueba sabe "
            "clasificar (posicion %d). Comprueba a mano de que tipo cuelga."
            % m.start())
        tipos = dentro[0][3]
        malos = [t for t in tipos if t not in TIPOS_PAGINA]
        assert not malos, (
            "un nodo de tipo %s lleva \"isPartOf\". Google solo documenta esa "
            "propiedad en la familia WebPage; para un Dataset espera URL o "
            "Dataset, y para decir de que catalogo forma parte la propiedad es "
            "includedInDataCatalog." % ", ".join(malos))
        hallados += 1
    assert hallados, "no se ha encontrado ningun \"isPartOf\" que revisar"


def test_el_dataset_declara_su_catalogo():
    """
    El bloque que emite el Dataset enlaza con el DataCatalog de /datos/.

    No es solo el repuesto de `isPartOf`: es la unica propiedad con la que
    Google entiende que la ficha de datos pertenece a un catalogo nuestro.
    """
    revisados = 0
    for _, _, cuerpo, tipos in _bloques():
        if "Dataset" not in tipos:
            continue
        assert '"includedInDataCatalog"' in cuerpo or \
               "includedInDataCatalog" in cuerpo, (
            "el bloque que emite el Dataset no declara includedInDataCatalog")
        revisados += 1
    assert revisados == 1, (
        "se esperaba un unico bloque que emita Dataset; hay %d" % revisados)


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
