# -*- coding: utf-8 -*-
"""
Tests de hugo.toml.

    python pipeline/test_configuracion.py

POR QUE EXISTE ESTE FICHERO

TOML no tiene llaves ni indentacion significativa: una cabecera de tabla abre
un ambito que dura hasta la siguiente cabecera. Todo par clave = valor que
venga detras pertenece a esa tabla, aunque este escrito al mismo nivel que el
resto y aunque el fichero se lea perfectamente bien.

Eso convierte "insertar un bloque nuevo" en una operacion peligrosa: si el
bloque lleva cabecera y se coloca por delante de ajustes sueltos, se los traga
todos. Hugo no avisa, el build termina en verde y la web se despliega.

Ya ha pasado dos veces:

  - `disableKinds` colocado detras de una cabecera, y dejo de aplicarse. Esta
    anotado en CLAUDE.md desde entonces.
  - El 01/10/2026, el bloque [params.fuseOpts] del buscador se inserto justo
    detras de [params]. Sus diecisiete ajustes siguientes (description, author,
    ShowBreadCrumbs, ShowPostNavLinks, hideMeta, mainSections...) quedaron
    dentro del tercer [[params.fuseOpts.keys]]. El sitio se quedo sin migas de
    navegacion ni enlaces de anterior/siguiente en las 37 paginas, con el
    <meta name=author> vacio y con el titulo del logotipo partido en
    "Coche Apto:  (Alt + H)". Nadie lo vio hasta el dia siguiente.

La leccion no es "tener cuidado", que ya se tuvo. Es que el dano no se ve
leyendo el fichero: hay que parsearlo. Eso lo hace una maquina mejor.
"""

import io
import os
import sys
import tomllib

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG = os.path.join(RAIZ, "hugo.toml")


def _config():
    with io.open(CONFIG, "rb") as f:
        return tomllib.load(f)


# Ajustes que tienen que colgar directamente de [params]. No es la lista
# completa a proposito: son los que cambian lo que ve el visitante o lo que
# lee Google, de modo que perderlos en silencio sale caro.
AJUSTES_DE_PARAMS = (
    "description",      # titulo del logotipo, JSON-LD y meta de las secciones
    "author",           # <meta name=author>
    "mainSections",     # sin esto, las paginas legales salen en la portada
    "noindex",          # el interruptor de abrir o cerrar a los buscadores
    "ShowBreadCrumbs",  # migas: navegacion y dato estructurado para Google
    "ShowPostNavLinks",  # anterior / siguiente
    "ShowToc",          # indice de las fichas largas
    "hideMeta",         # la fecha bajo cada tarjeta, que se quito a proposito
    "defaultTheme",
    "adsEnabled",       # regla dura 4: ningun anuncio encima del formulario
)


def test_los_ajustes_de_params_cuelgan_de_params():
    """Y no de la ultima tabla que alguien haya insertado por delante."""
    params = _config().get("params", {})
    perdidos = [c for c in AJUSTES_DE_PARAMS if c not in params]
    assert not perdidos, (
        "estos ajustes no estan en [params]: %s. Casi seguro que hay una "
        "cabecera de tabla por delante de ellos y TOML los ha anidado dentro. "
        "Las claves sueltas de [params] van ANTES de [params.loquesea]."
        % ", ".join(perdidos)
    )


def test_las_claves_del_buscador_solo_llevan_nombre_y_peso():
    """
    Senyal temprana del mismo fallo, y mas precisa.

    Cada [[params.fuseOpts.keys]] describe un campo del indice: que campo es y
    cuanto pesa. Nada mas. Si una de estas entradas aparece con mas claves, es
    que se ha tragado ajustes que iban detras, y entonces el problema no es
    solo del buscador: es que todo lo que venia despues esta fuera de sitio.
    """
    claves = _config().get("params", {}).get("fuseOpts", {}).get("keys", [])
    assert claves, "hugo.toml no declara params.fuseOpts.keys"
    for i, entrada in enumerate(claves):
        sobra = sorted(set(entrada) - {"name", "weight"})
        assert not sobra, (
            "params.fuseOpts.keys[%d] (%s) lleva ademas %s. Son ajustes de "
            "[params] que han quedado anidados aqui."
            % (i, entrada.get("name", "?"), ", ".join(sobra))
        )


def test_disablekinds_sigue_en_la_raiz():
    """La primera vez que se piso esta trampa. Que no vuelva."""
    config = _config()
    assert "disableKinds" in config, (
        "disableKinds no esta en la raiz de hugo.toml. Si se ha colocado "
        "detras de una cabecera [tabla], TOML lo ha anidado ahi y han vuelto "
        "las paginas vacias de /tags/ y /categories/."
    )
    assert "taxonomy" in config["disableKinds"]


def test_el_fichero_declara_la_zona_horaria():
    """
    Sin timeZone, una ficha fechada hoy pero creada de madrugada queda en el
    futuro y buildFuture = false la descarta sin decir nada.
    """
    assert _config().get("timeZone") == "Europe/Madrid"


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
