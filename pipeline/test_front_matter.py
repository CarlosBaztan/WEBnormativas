# -*- coding: utf-8 -*-
"""
Tests del front matter: que lo declarado lo lea alguien.

    python pipeline/test_front_matter.py

POR QUE EXISTE ESTE FICHERO

Una clave de front matter que ninguna plantilla lee no da ningun error. Hugo
guarda cualquier cosa en .Params y no se queja, el build termina en verde y la
pagina sale perfecta. Lo que no sale es el dato.

Paso el 03/10/2026, al arreglar el aviso de Search Console sobre el Dataset.
La pagina /datos/zbe/ declaraba `dataset_formatos: ["CSV", "JSON"]` y
`dataset_licencia`, pero schema.html lee `descargas` y `licencia`. Resultado:
el Dataset se publicaba sin `distribution`, es decir sin decirle a Google que
el dato se puede descargar, que es justo para lo que sirve publicar un
Dataset. Nadie lo vio en once dias porque no hay nada que mirar: el fallo es
la ausencia.

Es el mismo patron que las trampas de CLAUDE.md: lo mismo escrito dos veces y
corregido en un solo sitio. Aqui, con dos nombres distintos para el mismo dato.
"""

import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Claves que consume Hugo por su cuenta, sin que ninguna plantilla las nombre.
HUGO = (
    "aliases", "build", "cascade", "date", "description", "draft",
    "expiryDate", "headless", "isCJKLanguage", "keywords", "layout",
    "lastmod", "linkTitle", "markup", "menu", "menus", "outputs", "params",
    "publishDate", "resources", "sitemap", "slug", "summary", "title",
    "translationKey", "type", "url", "weight",
)

# Deuda declarada: datos que estan en el front matter y que ninguna plantilla
# usa todavia. Estan escritos en el texto de su pagina, asi que no falta nada
# a la vista; lo que falta es decidir si se publican de forma legible por
# maquina o se borran. Decision de Carlos, pendiente al 03/10/2026.
#
# Esta lista tiene que encoger, nunca crecer. Si una clave nueva acaba aqui,
# es que se ha escrito un dato que nadie lee.
HUERFANAS_CONOCIDAS = {
    "fecha_vigor_ordenanza": "fecha de entrada en vigor; esta en la linea de fuente de Barcelona y Madrid",
    "sancion_importe": "los 200 € de Madrid; estan en el cuerpo de la ficha",
    "verificado_por": "quien leyo la ordenanza; hoy solo consta la fecha",
}


def _claves_del_front_matter():
    """{clave: [paginas]} de todo content/, solo claves de primer nivel."""
    claves = {}
    for carpeta, _, ficheros in os.walk(os.path.join(RAIZ, "content")):
        for nombre in sorted(ficheros):
            if not nombre.endswith(".md"):
                continue
            ruta = os.path.join(carpeta, nombre)
            texto = io.open(ruta, encoding="utf-8-sig").read()
            m = re.match(r"^---\s*?\n(.*?)\n---\s*?\n", texto, re.S)
            if not m:
                continue
            for linea in m.group(1).splitlines():
                km = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:", linea)
                if km:
                    rel = os.path.relpath(ruta, RAIZ).replace("\\", "/")
                    claves.setdefault(km.group(1), []).append(rel)
    return claves


def _pajar():
    """
    Todo el codigo que podria leer una clave: plantillas, tema y pipeline.

    Los ficheros de pruebas quedan fuera a proposito. Esta misma prueba
    nombra las claves que vigila, asi que si se incluyeran, cada clave se
    daria por usada por el hecho de estar en la lista de las no usadas.
    """
    trozos = []
    for base in ("layouts", "themes", "pipeline"):
        for carpeta, _, ficheros in os.walk(os.path.join(RAIZ, base)):
            for nombre in ficheros:
                if nombre.startswith("test_"):
                    continue
                if nombre.endswith((".html", ".py", ".js", ".json", ".toml")):
                    ruta = os.path.join(carpeta, nombre)
                    trozos.append(io.open(ruta, encoding="utf-8",
                                          errors="ignore").read())
    return "\n".join(trozos)


def test_ninguna_clave_del_front_matter_se_queda_sin_leer():
    """
    Cada clave del front matter la nombra alguna plantilla, el tema o el
    pipeline. Si no, el dato esta escrito y no se publica.

    La comprobacion es por nombre, asi que una clave que se llame como una
    palabra corriente puede colarse. No vale para dar por bueno un nombre
    generico; vale para cazar el nombre equivocado, que es lo que pasa.
    """
    claves = _claves_del_front_matter()
    assert len(claves) > 20, (
        "se han leido solo %d claves; el parseo del front matter no esta "
        "funcionando" % len(claves))
    pajar = _pajar()
    huerfanas = []
    for clave in sorted(claves):
        if clave in HUGO or clave in HUERFANAS_CONOCIDAS:
            continue
        if not re.search(r"\b%s\b" % re.escape(clave), pajar):
            huerfanas.append("%s (en %s)" % (clave, ", ".join(sorted(set(claves[clave])))))
    assert not huerfanas, (
        "hay %d clave(s) de front matter que ninguna plantilla lee. El dato "
        "esta escrito y no se publica, y el build termina en verde:\n  %s"
        % (len(huerfanas), "\n  ".join(huerfanas)))


def test_la_deuda_declarada_sigue_siendo_deuda():
    """
    Si una de las huerfanas conocidas ya se usa, sale de la lista.

    Una lista de excepciones que no se limpia deja de describir la realidad y
    acaba tapando lo que decia vigilar.
    """
    pajar = _pajar()
    resueltas = [c for c in HUERFANAS_CONOCIDAS
                 if re.search(r"\b%s\b" % re.escape(c), pajar)]
    assert not resueltas, (
        "estas claves ya las lee alguien: quitalas de HUERFANAS_CONOCIDAS: %s"
        % ", ".join(resueltas))


LIMITE_DESCRIPCION = 160


def _paginas_publicadas():
    """(ruta relativa, front matter) de cada .md que no sea borrador."""
    for carpeta, _, ficheros in os.walk(os.path.join(RAIZ, "content")):
        for nombre in sorted(ficheros):
            if not nombre.endswith(".md"):
                continue
            ruta = os.path.join(carpeta, nombre)
            texto = io.open(ruta, encoding="utf-8-sig").read()
            m = re.match(r"^---\s*?\n(.*?)\n---\s*?\n", texto, re.S)
            if not m or re.search(r"^draft:\s*true", m.group(1), re.M):
                continue
            yield os.path.relpath(ruta, RAIZ).replace("\\", "/"), m.group(1)


def test_ninguna_descripcion_se_pasa_de_lo_que_google_ensena():
    """
    La descripcion es el unico texto del sitio que se escribe PARA el
    resultado de busqueda, y Google la corta sobre los 160 caracteres.

    Medidas las 46 el 07/10/2026: veintidos se pasaban, y Barcelona llegaba a
    257, o sea que su ultimo tercio no lo leia nadie. Reescritas todas.

    Esta prueba existe porque ese trabajo se pierde sin hacer ruido. El mismo
    dia, al devolver una fecha de prueba con `git checkout -- malaga.md`, se
    deshizo tambien su descripcion: el fichero volvio entero, no solo la
    linea que interesaba. Nadie lo habria visto hasta el proximo repaso.

    No se comprueba un minimo: una descripcion corta no engana a nadie, solo
    desaprovecha sitio, y /search/ o /legal/ no necesitan 150 caracteres.
    """
    largas = []
    raras = []
    for ruta, fm in _paginas_publicadas():
        m = re.search(r"^description:\s*(.*)$", fm, re.M)
        if not m:
            continue
        valor = m.group(1).strip()
        # SE EXIGE LA FORMA CANONICA, Y NO POR gusto: la version anterior
        # buscaba `description: "..."` y por tanto NO VEIA las descripciones
        # escritas sin comillas, con comillas simples o plegadas con `>-`.
        # Las tres son YAML valido. Comprobado: una descripcion de 200
        # caracteres en cualquiera de esas tres formas dejaba la prueba en
        # verde. O sea que el trabajo que esta prueba existe para proteger
        # (22 descripciones reescritas, una de ellas perdida sola con un
        # `git checkout`) se podia perder otra vez sin ruido.
        #
        # Convertir la forma rara en FALLO, y no en exencion, es lo que cierra
        # el agujero: si alguna vez hace falta otra forma, que se decida a
        # sabiendas y se cambie aqui.
        if not (len(valor) >= 2 and valor[0] == '"' and valor[-1] == '"'):
            raras.append(ruta)
            continue
        if len(valor) - 2 > LIMITE_DESCRIPCION:
            largas.append("%s (%d)" % (ruta, len(valor) - 2))
    assert not raras, (
        "Estas descripciones no van entre comillas dobles, asi que esta "
        "prueba no puede medirlas: %s" % ", ".join(sorted(raras)))
    assert not largas, (
        "Descripciones de mas de %d caracteres, que Google corta a mitad de "
        "frase: %s" % (LIMITE_DESCRIPCION, ", ".join(sorted(largas))))


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
