# -*- coding: utf-8 -*-
"""
Tests de pipeline/auditoria.py.

    python pipeline/test_auditoria.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import auditoria as au

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _front_matter_de(ruta):
    with open(os.path.join(RAIZ, ruta), encoding="utf-8") as fh:
        return fh.read()


def test_madrid_declara_reglas_por_zonas():
    """
    Madrid no usa etiquetas_permitidas: tiene tres zonas con reglas distintas
    y las declara en un bloque `zonas`. Una ficha asi es valida.
    """
    assert au.declara_reglas(_front_matter_de("content/zbe/madrid.md"))


def test_una_ficha_con_etiquetas_permitidas_declara_reglas():
    texto = '---\nestado_dato: "verificado"\netiquetas_permitidas: ["0", "ECO"]\n---\n'
    assert au.declara_reglas(texto)


def test_una_lista_vacia_no_declara_reglas():
    """
    El caso peligroso: ficha marcada como verificada que no dice nada. El
    lector ve el sello de verificado y una pagina sin contenido util.
    """
    texto = '---\nestado_dato: "verificado"\netiquetas_permitidas: []\n---\n'
    assert not au.declara_reglas(texto)


def test_sin_ningun_campo_no_declara_reglas():
    texto = '---\nestado_dato: "verificado"\n---\n'
    assert not au.declara_reglas(texto)


def test_los_enlaces_rotos_se_detectan():
    """
    La comprobacion recibe el verificador como parametro para poder probarla
    sin red. En produccion se le pasa uno que hace la peticion de verdad.
    """
    respuestas = {"https://bien.example": 200, "https://roto.example": 404}
    rotos = au.enlaces_rotos(
        {"ficha-a.md": "https://bien.example", "ficha-b.md": "https://roto.example"},
        comprobador=lambda u: respuestas[u])
    assert len(rotos) == 1
    assert "ficha-b.md" in rotos[0]
    assert "404" in rotos[0]


def test_un_enlace_que_no_responde_cuenta_como_roto():
    def revienta(url):
        raise OSError("sin conexion")
    rotos = au.enlaces_rotos({"ficha.md": "https://loquesea.example"}, comprobador=revienta)
    assert len(rotos) == 1


def test_una_zbe_prevista_no_tiene_que_declarar_reglas():
    """
    Caso real de Valencia (28/09/2026): la ordenanza esta aprobada solo
    inicialmente y el propio ayuntamiento dice que la aprobacion definitiva
    sigue pendiente. No hay reglas en vigor que declarar, y exigirlas
    obligaria a inventarlas o a no publicar una ficha que si aporta.

    Solo se exigen reglas cuando la zona esta activa.
    """
    assert not au.exige_reglas({"estado_zbe": "prevista", "codigo_ine": "46250"})
    assert not au.exige_reglas({"estado_zbe": "sin_zbe", "codigo_ine": "46250"})


def test_una_zbe_activa_si_tiene_que_declarar_reglas():
    assert au.exige_reglas({"estado_zbe": "activa", "codigo_ine": "28079"})


def test_un_articulo_no_tiene_que_declarar_reglas():
    """Sin codigo_ine no es la ficha de un municipio, es un articulo."""
    assert not au.exige_reglas({"estado_zbe": "activa"})


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
