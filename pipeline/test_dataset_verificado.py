# -*- coding: utf-8 -*-
"""
Tests del puente entre las fichas verificadas y el dataset publicado.

    python pipeline/test_dataset_verificado.py

POR QUE EXISTE ESTE FICHERO

El activo de este proyecto es haber leido las ordenanzas una a una. Esa lectura
vive en el front matter de content/zbe/*.md. El dataset que publicamos bajo
CC-BY, que anunciamos en /datos/zbe/ y al que apunta el nodo Dataset del
JSON-LD, lo escribe pipeline/zbe_nap.py a partir del NAP de la DGT.

Hasta el 04/10/2026 esos dos caminos no se tocaban. El dataset salia con las 45
filas del NAP y la columna `etiquetas_permitidas` VACIA en todas, incluidas las
doce cuya ordenanza ya habiamos leido, y `con_reglas_verificadas: 0`.

Lo mas revelador es que el pipeline ya estaba escrito para esto: su propia
ADVERTENCIA dice que las reglas se publican «tras leerlas en la ordenanza, una
a una, y entonces `confianza` pasa a 'oficial'». El estado 'oficial' existia,
estaba documentado y no lo alcanzaba ningun municipio, porque nadie habia
escrito el paso que lo promueve. El fichero se generaba sin error y nadie
miraba la columna.

Lo encontro una auditoria de visibilidad en motores generativos, buscando por
que ningun motor podia citar el dato diferencial del sitio. La respuesta era
que el dato diferencial no era legible por maquina.
"""

import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import zbe_nap as zn

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _dataset():
    return json.loads(io.open(os.path.join(RAIZ, "data", "zbe.json"),
                              encoding="utf-8").read())


def test_se_leen_las_reglas_de_las_fichas():
    """
    `reglas_de_las_fichas()` encuentra las ordenanzas ya verificadas.

    Es la funcion que cruza content/zbe/*.md con los slugs del NAP. Si
    devuelve vacio, el resto de pruebas de este fichero no prueban nada.
    """
    reglas = zn.reglas_de_las_fichas()
    assert len(reglas) >= 8, (
        "se esperaban al menos ocho fichas verificadas cruzadas con el NAP; "
        "se han encontrado %d" % len(reglas))
    for clave, datos in reglas.items():
        assert datos.get("fecha_verificacion"), (
            "%s: una ficha verificada sin fecha_verificacion no puede entrar "
            "en el dataset" % clave)
        assert datos.get("ordenanza_url"), (
            "%s: una ficha verificada sin fuente_url no puede entrar en el "
            "dataset: el dato sin su enlace no vale" % clave)


def test_las_ordenanzas_leidas_llegan_al_dataset():
    """
    Lo que hemos verificado sale publicado como verificado.

    Si esta prueba falla despues de publicar una ficha nueva, es que falta
    volver a generar el dataset: python pipeline/zbe_nap.py
    """
    dataset = _dataset()["municipios"]
    reglas = zn.reglas_de_las_fichas()
    faltan = []
    for clave in reglas:
        registro = dataset.get(clave)
        if registro is None:
            continue   # la ficha no corresponde a ningun municipio del NAP
        if registro.get("confianza") != "oficial":
            faltan.append("%s (confianza: %s)" % (clave, registro.get("confianza")))
    assert not faltan, (
        "estos municipios tienen la ordenanza leida y el dataset publicado "
        "sigue diciendo que no: %s. Vuelve a generar el dataset."
        % ", ".join(faltan))


def test_el_dataset_no_llama_verificado_a_lo_que_no_lo_esta():
    """
    Al reves: nada marcado como 'oficial' sin ficha que lo respalde.

    Es la mitad que de verdad importa. Publicar de menos cuesta visitas;
    publicar de mas cuesta una multa de 200 euros al lector.
    """
    dataset = _dataset()["municipios"]
    reglas = zn.reglas_de_las_fichas()
    sin_respaldo = [c for c, r in dataset.items()
                    if r.get("confianza") == "oficial" and c not in reglas]
    assert not sin_respaldo, (
        "el dataset da por verificados municipios sin ficha que lo sostenga: "
        "%s" % ", ".join(sin_respaldo))


def test_toda_regla_publicada_lleva_su_trazabilidad():
    """
    Cada municipio 'oficial' trae ordenanza, enlace y fecha.

    Es la misma regla que ya rompe el build en zbe-verificados.html, aplicada
    al otro extremo del tubo: un dataset abierto sin fuente no es reutilizable
    y contradice lo que promete /datos/zbe/.
    """
    faltan = []
    for clave, r in _dataset()["municipios"].items():
        if r.get("confianza") != "oficial":
            continue
        for campo in ("ordenanza_nombre", "ordenanza_url", "fecha_verificacion", "ficha_url"):
            if not r.get(campo):
                faltan.append("%s sin %s" % (clave, campo))
    assert not faltan, "; ".join(faltan)


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
