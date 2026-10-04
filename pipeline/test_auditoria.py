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
    # estado_dato explicito: desde que existe el nivel "parcial", solo a una
    # ficha que se declara verificada se le exigen reglas de acceso.
    assert au.exige_reglas({"estado_zbe": "activa", "codigo_ine": "28079",
                            "estado_dato": "verificado"})


def test_un_articulo_no_tiene_que_declarar_reglas():
    """Sin codigo_ine no es la ficha de un municipio, es un articulo."""
    assert not au.exige_reglas({"estado_zbe": "activa"})


def test_parcial_se_publica_sin_ser_incoherente():
    """
    Nivel C de CLAUDE.md: sabemos que la ZBE existe y de donde sale el dato,
    pero no hemos podido leer las reglas de acceso. La tabla de confianza dice
    que eso SI se publica, con su enlace oficial y sin responder "puedo
    entrar". Hasta ahora el proyecto no tenia como expresarlo: "pendiente"
    obliga a draft y la ficha no salia.

    Caso de Benidorm: la ZBE opera desde el 1 de enero de 2025, pero ni la
    pagina municipal ni el portal dicen que distintivos quedan restringidos.
    """
    assert au.publicable({"estado_dato": "parcial", "draft": "false"})
    assert not au.incoherente({"estado_dato": "parcial", "draft": "false"})


def test_pendiente_publicado_sigue_siendo_incoherente():
    """Lo de siempre no cambia: pendiente con draft false es un dato sin
    verificar que se colaria a produccion."""
    assert au.incoherente({"estado_dato": "pendiente", "draft": "false"})


def test_parcial_no_tiene_que_declarar_reglas():
    assert not au.exige_reglas({"estado_dato": "parcial", "estado_zbe": "activa",
                                "codigo_ine": "03031"})


def test_verificada_activa_si_tiene_que_declarar_reglas():
    assert au.exige_reglas({"estado_dato": "verificado", "estado_zbe": "activa",
                            "codigo_ine": "28079"})


def test_un_marcador_de_verificar_se_detecta():
    """
    {{VERIFICAR}} es la nota que me dejo a mi mismo cuando un dato no esta
    contrastado. No es una plantilla de Hugo: Goldmark la imprime tal cual, o
    sea que llega al lector. Aparecio cuatro veces en /multas/zbe/ sin que
    nada avisara.
    """
    texto = '---\nestado_dato: "verificado"\n---\nImporte: {{VERIFICAR}} en el art. 80.1.\n'
    assert au.marcadores_sin_resolver(texto) == ["{{VERIFICAR}}"]


def test_pendiente_de_verificar_en_una_tabla_es_legitimo():
    """
    El falso positivo que tuvo la primera version de esta comprobacion.

    La ficha de Madrid tiene cinco celdas que dicen "Pendiente de verificar",
    y son correctas: las reglas de publicacion del proyecto obligan a decir en
    voz alta lo que no se ha contrastado, en vez de callarlo. Marcarlo como
    incidencia empujaria justo a lo contrario.
    """
    texto = ('---\nestado_dato: "verificado"\n---\n'
             '| Distintivo | ZBE |\n|:---|:---|\n| B | Pendiente de verificar |\n')
    assert au.marcadores_sin_resolver(texto) == []


def test_el_front_matter_no_cuenta_como_marcador():
    """
    Solo importa lo que ve el lector. Una nota en el front matter no se
    publica, asi que no es una incidencia.
    """
    texto = '---\nestado_dato: "verificado"\nnota: "pendiente de verificar el importe"\n---\nTexto limpio.\n'
    assert au.marcadores_sin_resolver(texto) == []


def test_una_pagina_limpia_no_da_marcadores():
    texto = '---\nestado_dato: "verificado"\n---\nLa multa son 200 euros (art. 80.1 LTSV).\n'
    assert au.marcadores_sin_resolver(texto) == []


def test_una_nota_pendiente_en_comentario_html_se_detecta():
    """
    Las notas que se dejan como comentario de HTML no las ve el visitante,
    pero viajan en el codigo fuente de la pagina publicada y delatan que algo
    quedo a medias. Habia tres: dos en /sobre/ y una en /legal/contacto/, con
    el texto "completar con los datos del responsable antes de lanzar".

    Se busca la marca exacta, en mayusculas y dentro del comentario, para no
    confundirla con la palabra "pendiente" en prosa, que en este sitio es
    legitima y frecuente: estado_dato pendiente, "pendiente de verificacion".
    """
    texto = '---\nestado_dato: "verificado"\n---\n<!-- PENDIENTE: poner el correo -->\nTexto.\n'
    assert au.marcadores_sin_resolver(texto) == ["<!-- PENDIENTE"]


def test_la_palabra_pendiente_en_prosa_no_es_una_nota():
    """El caso que no se puede marcar: es vocabulario normal del proyecto."""
    texto = '---\nestado_dato: "parcial"\n---\nEsta zona esta pendiente de verificacion.\n'
    assert au.marcadores_sin_resolver(texto) == []


def test_ninguna_pagina_publicada_lleva_marcadores():
    """
    La comprobacion de verdad, sobre el contenido real del sitio. Si esto
    falla, hay una nota interna publicada.
    """
    sucias = []
    for ruta, texto in au.paginas_publicadas():
        marcas = au.marcadores_sin_resolver(texto)
        if marcas:
            sucias.append("%s: %s" % (ruta, ", ".join(marcas)))
    assert not sucias, "paginas con notas sin resolver:\n   " + "\n   ".join(sucias)


# ---------------------------------------------------------------------------
# La cola de municipios de data/cobertura.json
#
# 04/10/2026. Al publicar Palma y Alicante, la frase de cobertura de la
# portada quedo diciendo «Con respuesta verificada: ... Palma, Sevilla ...
# Siguientes: ... Palma y Alicante»: los anunciaba como proximos y ya estaban
# hechos. La lista de la cola es la unica parte de esa frase que sigue escrita
# a mano, porque son municipios que todavia no tienen pagina y no hay dato del
# que sacarlos; el precio es que nadie la limpia.
#
# El build termino en verde y la auditoria no dijo nada: el fallo solo se ve
# leyendo la frase entera en la portada.
# ---------------------------------------------------------------------------

def test_la_cola_no_anuncia_municipios_que_ya_tienen_ficha():
    """
    Ningun municipio de `proximos` puede tener ya ficha publicada.

    Si la tiene, o responde (y entonces la frase se contradice sola) o no
    responde (y entonces ya sale en «Siguientes» por su propia ficha, dos
    veces).
    """
    repetidos = au.cola_ya_cubierta()
    assert not repetidos, (
        "data/cobertura.json anuncia como proximos municipios que ya tienen "
        "ficha: %s. Quitalos de `proximos`." % ", ".join(repetidos))


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
