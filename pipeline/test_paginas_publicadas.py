# -*- coding: utf-8 -*-
"""
Pruebas sobre el HTML que de verdad se publica.

    python pipeline/test_paginas_publicadas.py

POR QUE ESTE FICHERO ES DISTINTO DE LOS DEMAS

Los otros tests leen plantillas, front matter o CSS. Este compila el sitio con
Hugo y lee lo que sale. Es mas lento y es el unico que puede responder a la
pregunta que ya ha fallado CUATRO veces en este proyecto:

    "¿esta pagina dice de si misma algo que no es verdad?"

Las cuatro, repasadas, porque todas tienen la misma forma:

  1. Articulos de /zbe/ («que es una ZBE», «excepciones», «camaras») coronados
     con «las reglas de acceso de esta ZBE no estan verificadas», sobre una
     ZBE que no existe porque la pagina no es de un municipio.
  2. Las dos paginas de zona de Madrid, con ese mismo aviso DOS LINEAS ENCIMA
     de su propia tabla de distintivos verificada.
  3. /itv/pegatina/ servida con la calculadora de periodicidad de la ITV y su
     texto de «que hace esta herramienta», que hablaba de otra cosa.
  4. Alicante, La Coruna y Pamplona (07/10/2026): las tres con la ordenanza
     leida articulo por articulo, las tres publicando que no la hemos
     contrastado. Ver abajo.

En las cuatro, el build termino en verde y lo descubrio una persona mirando.

LO QUE VIGILA, por ahora

Que ninguna pagina marcada como verificada publique el aviso de que sus reglas
no lo estan. Y al reves, que una ficha que de verdad no tiene reglas leidas lo
siga diciendo: una prueba que solo mira en una direccion se cumple borrando el
aviso de todas partes.

EL CASO DE 2026-10-07, para que se entienda la regla

Hay tres ZBE donde la etiqueta ambiental NO es lo que abre la puerta: en
Alicante, La Coruna y Pamplona lo que da acceso es una autorizacion municipal,
y la etiqueta, cuando se pide, es un filtro de segunda vuelta. Eso se declara
con `acceso_por_distintivo: false` y `etiquetas_permitidas: []`.

La lista vacia ahi NO significa «no lo hemos mirado». Significa «lo hemos
mirado y la respuesta es que ninguna etiqueta vale». auditoria.py ya lo
entendia asi desde el 05/10 (ver declara_reglas), pero la plantilla seguia
mirando solo si la lista tenia elementos. Mismo criterio escrito dos veces y
corregido en uno solo, que es el error de fondo de casi todo lo anotado en
CLAUDE.md.
"""

import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auditoria import declara_reglas, front_matter  # noqa: E402

AVISO_SIN_VERIFICAR = "Las reglas de acceso de esta ZBE no est"
AVISO_SIN_FUENTE = "Datos sin verificar."


def _compilar():
    """Compila el sitio en un directorio temporal y devuelve su ruta.

    `--destination` fuera del proyecto a proposito: public/ no se limpia sola
    entre builds, y una prueba que leyera restos de una compilacion anterior
    seria peor que no tenerla.
    """
    destino = tempfile.mkdtemp(prefix="cocheapto-test-")
    r = subprocess.run(
        ["hugo", "--quiet", "--destination", destino,
         "--baseURL", "http://localhost/", "--logLevel", "error"],
        cwd=RAIZ, capture_output=True, text=True,
    )
    if r.returncode != 0:
        shutil.rmtree(destino, ignore_errors=True)
        raise RuntimeError("hugo fallo:\n" + (r.stderr or r.stdout))
    return destino


def _html_de(destino, ruta):
    """Lee el index.html de una URL ya compilada. None si no se publico."""
    f = os.path.join(destino, ruta.strip("/").replace("/", os.sep), "index.html")
    if not os.path.exists(f):
        return None
    return io.open(f, encoding="utf-8").read()


def _urls_publicadas(destino):
    """Cada carpeta con index.html del build, como ruta de URL."""
    for carpeta, _, ficheros in os.walk(destino):
        if "index.html" not in ficheros:
            continue
        rel = os.path.relpath(carpeta, destino).replace(os.sep, "/")
        yield "/" if rel == "." else "/%s/" % rel


def _fichas():
    """Cada .md de content/zbe/, con su front matter y su texto crudo."""
    carpeta = os.path.join(RAIZ, "content", "zbe")
    for nombre in sorted(os.listdir(carpeta)):
        if not nombre.endswith(".md") or nombre == "_index.md":
            continue
        texto = io.open(os.path.join(carpeta, nombre), encoding="utf-8").read()
        yield nombre[:-3], front_matter(texto), texto


def test_ninguna_ficha_verificada_dice_que_no_lo_esta(destino):
    """Lo que paso el 07/10/2026 con Alicante, La Coruna y Pamplona."""
    malas = []
    for slug, fm, texto in _fichas():
        if fm.get("estado_dato") != "verificado":
            continue
        if not declara_reglas(texto):
            continue
        html = _html_de(destino, "/zbe/%s/" % slug)
        if html and AVISO_SIN_VERIFICAR in html:
            malas.append(slug)
    assert not malas, (
        "Estas fichas tienen la ordenanza leida y publican que no la hemos "
        "contrastado: %s" % ", ".join(malas)
    )


def test_el_aviso_de_datos_sin_verificar_solo_sale_donde_toca(destino):
    """
    Quinta vez que una plantilla se dispara en una pagina que no es la suya.

    LO QUE PASO (08/10/2026). /zbe/distintivos-por-ciudad/ abria con un recuadro
    rojo: «Datos sin verificar. No hemos contrastado todavia esta informacion
    con el texto oficial... No tomes decisiones a partir de esta pagina.
    Todavia no tenemos una fuente oficial publicable para este municipio.»

    En la pagina cuyo contenido entero son diecisiete zonas leidas ordenanza por
    ordenanza, con el articulo citado en cada ficha. Y hablando de «este
    municipio», que no es ninguno: es una tabla de todos.

    La causa: layouts/zbe/single.html llamaba a fuente-verificacion.html para
    TODA pagina de la seccion, y ese partial trata «no declara estado_dato»
    igual que «sin verificar». Para una ficha eso esta bien (la ausencia es
    falta de verificacion); para un articulo derivado de otras paginas, no.

    No se arreglo inventandole una fuente: esta pagina no tiene una, tiene
    quince, y cada fila ya enlaza la suya. Lo que se arreglo es que solo se
    pida trazabilidad a quien puede darla.

    LA REGLA: ese aviso solo puede salir en una pagina de municipio o de zona
    que de verdad no este verificada.
    """
    malas = []
    for slug, fm, _ in _fichas():
        html = _html_de(destino, "/zbe/%s/" % slug)
        if not html or AVISO_SIN_FUENTE not in html:
            continue
        es_ficha = fm.get("tipo", "municipio") in ("municipio", "zona")
        if not es_ficha or fm.get("estado_dato") == "verificado":
            malas.append("%s (tipo=%s, estado=%s)" % (
                slug, fm.get("tipo", "municipio"),
                fm.get("estado_dato", "sin declarar")))
    assert not malas, (
        "Estas paginas publican el aviso de «datos sin verificar» sin ser una "
        "ficha pendiente: %s" % ", ".join(malas))


def test_la_tabla_de_datos_tampoco_dice_sin_verificar(destino):
    """El mismo fallo tenia dos salidas, y la segunda es la tabla.

    Quitado el aviso de arriba, la fila «Distintivos que la ordenanza permite
    circular» del bloque de datos seguia imprimiendo «Sin verificar. No
    publicamos esta lista hasta haberla leido en el texto oficial» en las tres
    fichas. Una pagina puede desmentirse en mas de un sitio, y arreglar el
    primero no arregla el segundo.
    """
    malas = []
    for slug, fm, texto in _fichas():
        if fm.get("estado_dato") != "verificado" or not declara_reglas(texto):
            continue
        html = _html_de(destino, "/zbe/%s/" % slug)
        if html and "Sin verificar. No publicamos esta lista" in html:
            malas.append(slug)
    assert not malas, (
        "Estas fichas tienen la ordenanza leida y su tabla de datos dice "
        "«sin verificar»: %s" % ", ".join(malas)
    )


def test_el_json_ld_de_una_ficha_describe_un_solo_documento(destino):
    """
    Una pagina emite TRES bloques JSON-LD: el WebPage nuestro y el
    BreadcrumbList y el BlogPosting del tema. Tienen que hablar del mismo
    documento, y para eso sirve `@id`.

    LO QUE PASO (08/10/2026). Nuestro WebPage se llamaba
    `https://cocheapto.com/zbe/granada/#webpage` y el BlogPosting del tema
    declaraba `mainEntityOfPage: {"@id": "https://cocheapto.com/zbe/granada/"}`.
    Dos nodos distintos para la misma pagina.

    O sea que `lastReviewed`, `citation` y `about`, que es TODO lo que este
    sitio aporta de propio y el motivo por el que existe, colgaban de un
    documento que para un consumidor de JSON-LD no era el mismo que el que
    lleva el titular, la fecha y el autor.

    Se vio porque los tres bloques solo se emiten en el build de produccion:
    con `hugo server` sale uno, asi que auditando en local se ve un tercio de
    lo que ve Google. Esta prueba compila como produccion.
    """
    fallos = []
    for ruta in ("/zbe/granada/", "/zbe/pamplona/", "/etiquetas/b/"):
        html = _html_de(destino, ruta)
        if not html:
            continue
        nodos = []
        for b in re.findall(r"<script type=[\"']?application/ld\+json[\"']?>(.*?)</script>",
                            html, re.S):
            try:
                nodos.append(json.loads(b))
            except ValueError:
                fallos.append("%s: un bloque JSON-LD no parsea" % ruta)
        propios = [n.get("@id") for n in nodos if n.get("@type") == "WebPage"]
        for n in nodos:
            meop = n.get("mainEntityOfPage")
            if not isinstance(meop, dict):
                continue
            if meop.get("@id") not in propios:
                fallos.append(
                    "%s: el %s apunta a %s y nuestro WebPage es %s"
                    % (ruta, n.get("@type"), meop.get("@id"), propios or "(ninguno)"))
    assert not fallos, (
        "El JSON-LD de estas paginas describe dos documentos distintos: %s"
        % "; ".join(fallos))


def test_ningun_enlace_a_la_fuente_oficial_lleva_nofollow(destino):
    """
    Citar la fuente oficial con un enlace normal es la senal mas barata que
    tiene este sitio, y es literalmente su argumento de negocio.

    La regla esta escrita en docs/seo-arquitectura.md, apartado 7: «Sin
    `rel="nofollow"`. Poner nofollow a un enlace a .gob.es no protege de nada
    y desperdicia la senal».

    Estaba implementada en layouts/_markup/render-link.html, para los enlaces
    escritos en el Markdown, y NO en fuente-verificacion.html, que es el
    bloque de fuente del que habla ese apartado. Los tres enlaces de ahi
    llevaban `nofollow`, o sea que la senal se anulaba justo en el sitio donde
    el apartado 7 dice que importa.

    Y el detalle que lo hace peor: el comentario de render-link.html decia «Es
    la misma convencion que ya usa partials/fuente-verificacion.html». No lo
    era. Un comentario afirmando un comportamiento que nadie comprobo.

    El sitio no tiene enlaces pagados ni contenido de terceros, asi que no hay
    ningun caso legitimo de nofollow. Si alguna vez lo hay (publicidad), esta
    prueba tendra que cambiar, y ese es justo el momento de pensarlo.
    """
    con_nofollow = []
    for ruta in _urls_publicadas(destino):
        html = _html_de(destino, ruta)
        if not html:
            continue
        if re.search(r'rel=["\']?[^"\'>]*nofollow', html):
            con_nofollow.append(ruta)
    assert not con_nofollow, (
        "Estas paginas anulan la senal de su propia fuente oficial con "
        "nofollow: %s" % ", ".join(sorted(con_nofollow)))


def test_quien_declara_una_fuente_la_publica(destino):
    """
    La promesa del sitio es que cada dato lleva fuente, enlace y fecha de
    verificacion VISIBLES. Esta prueba vigila el caso en que el dato esta y no
    se pinta, que no da ningun error y no se ve leyendo el front matter.

    LO QUE PASO (08/10/2026). Siete paginas lo declaraban y no lo publicaban:
    las cinco de distintivo, /etiquetas/ y /multas/zbe/. Las dos plantillas que
    las sirven (una copia del single.html del tema y el single.html del tema
    mismo) no llamaban nunca a fuente-verificacion.html.

    En su lugar habia una linea escrita a mano al final del Markdown,
    «**Fuente:** Distintivo ambiental de la DGT», SIN ENLACE y SIN FECHA, en
    paginas que afirman que anos y que combustibles llevan cada distintivo.

    Y un segundo efecto, peor porque era futuro: el aviso automatico de
    «pendiente de revision» a los seis meses vive en ese partial. Sin el, esas
    paginas habrian pasado el 23/03/2027 sin decir nada mientras una ficha de
    ZBE se marca sola.
    """
    sin_publicar = []
    for ruta in _urls_publicadas(destino):
        md = _fuente_declarada(ruta)
        if not md:
            continue
        html = _html_de(destino, ruta)
        if not html:
            continue
        if "fuente__linea" not in html:
            sin_publicar.append(ruta)
    assert not sin_publicar, (
        "Estas paginas declaran una fuente en el front matter y no la "
        "publican: %s" % ", ".join(sorted(sin_publicar)))


def _fuente_declarada(ruta):
    """True si el .md de esa URL declara `fuente_nombre`."""
    rel = ruta.strip("/")
    candidatos = [os.path.join(RAIZ, "content", rel + ".md"),
                  os.path.join(RAIZ, "content", rel, "_index.md")]
    for c in candidatos:
        if not os.path.exists(c):
            continue
        texto = io.open(c, encoding="utf-8-sig").read()
        m = re.match(r"^---\s*?\n(.*?)\n---\s*?\n", texto, re.S)
        if m and re.search(r"^fuente_nombre:\s*\S", m.group(1), re.M):
            return True
    return False


def test_ningun_enlace_publicado_apunta_a_ninguna_parte(destino):
    """
    Un `<a href="">` no da 404: recarga la pagina en la que estas. Por eso no
    lo caza un comprobador de enlaces, y por eso lleva ahi sin que nadie lo
    vea.

    LO QUE PASO (08/10/2026). /itv/ esta en borrador y sus dos paginas si
    estan publicadas, asi que la miga de pan de /itv/cuando-me-toca/ y de
    /itv/pegatina/ decia «Inicio > ITV >» con la ITV enlazada a `href=""`.
    Quien la pulsa no va a ningun sitio; quien navega con lector de pantalla
    oye «ITV, enlace» y al activarlo se recarga la misma pagina.

    Un barrido de los 48 enlaces internos distintos del sitio dio CERO rotos,
    porque `""` resuelve a la URL actual y devuelve 200. Lo unico que lo
    delata es buscar el atributo vacio.

    Que /itv/ se publique o se cierre es otra decision, y es de Carlos. Esto
    vale igual para las dos: una miga sin destino se pinta como texto, no
    como enlace.
    """
    malas = []
    for ruta in _urls_publicadas(destino):
        html = _html_de(destino, ruta)
        if not html:
            continue
        # OJO: el minificador NO escribe `href=""`, escribe `<a href>` a
        # secas, igual que convierte `alt=""` en `alt`. La primera version de
        # esta prueba buscaba `href=""` y pasaba sin comprobar nada. Es la
        # tercera vez hoy que esta trampa muerde, y ya estaba anotada en
        # CLAUDE.md por el `alt`.
        if re.search(r'<a(?=[\s>])[^>]*?\shref(=(?:""|\'\')|(?=[\s>]))', html):
            malas.append(ruta)
    assert not malas, (
        "Estas paginas publican un enlace sin destino, que al pulsarlo "
        "recarga la misma pagina: %s" % ", ".join(sorted(malas)))


SECCIONES_EN_EL_MENU = ("zbe", "etiquetas", "itv", "multas", "datos")


def test_el_menu_se_abre_por_la_seccion_de_la_pagina(destino):
    """
    En 24 de las 46 paginas, mas de la mitad, el menu lateral salia con los
    seis grupos cerrados y ninguna fila marcada. Entre ellas, CATORCE DE LAS
    QUINCE FICHAS DE MUNICIPIO.

    O sea: quien llega desde Google a /zbe/granada/, que es la entrada mas
    comun del sitio, ve a la izquierda una columna de seis acordeones cerrados
    que no le dicen ni donde esta ni que mas hay de lo suyo. El menu no hacia
    ninguno de sus dos trabajos justo en las paginas que traen el trafico.

    Pasaba porque el grupo solo se abria cuando alguno de sus enlaces era
    EXACTAMENTE la pagina actual, y las fichas de municipio no estan en el
    menu una a una (seria una lista de quince y creciendo).

    La regla que fija esta prueba: si la seccion de la pagina aparece en el
    menu, algun grupo tiene que estar abierto. /legal/ queda fuera a
    proposito: sus cuatro paginas no estan en el menu ni deben estarlo, se
    llega a ellas por el pie.
    """
    cerradas = []
    for ruta in _urls_publicadas(destino):
        seccion = ruta.strip("/").split("/")[0]
        if seccion not in SECCIONES_EN_EL_MENU:
            continue
        html = _html_de(destino, ruta)
        if not html:
            continue
        menu = re.search(r"<nav id=[\"']?menu-lateral[\"']?.*?</nav>", html, re.S)
        if not menu:
            continue
        # `open` minificado va sin valor, igual que `alt`.
        if not re.search(r"<details[^>]*\bopen\b", menu.group(0)):
            cerradas.append(ruta)
    assert not cerradas, (
        "Estas paginas abren con todos los grupos del menu cerrados, sin "
        "decirle al lector donde esta: %s" % ", ".join(sorted(cerradas)))


def test_el_menu_marca_una_sola_pagina_como_actual(destino):
    """
    `aria-current="page"` responde a «¿donde estoy?», y esa pregunta tiene una
    respuesta.

    /etiquetas/ esta en el menu lateral DOS VECES, con dos nombres: «Que
    etiqueta tengo», en el grupo de herramientas, y «Todas las etiquetas», en
    el de etiquetas. Las dos son utiles y las dos se quedan. Lo que no puede
    ser es que al abrir esa pagina las DOS salgan marcadas como la actual:
    dos filas resaltadas a la vez, y un lector de pantalla anunciando dos
    veces «pagina actual».

    Se marca la primera que aparece y ya esta. El enlace sigue estando en los
    dos sitios.
    """
    malas = []
    for ruta in _urls_publicadas(destino):
        html = _html_de(destino, ruta)
        if not html:
            continue
        # OJO CON LAS COMILLAS: el sitio se compila MINIFICADO, asi que en el
        # HTML publicado pone `aria-current=page` y `id=menu-lateral`, sin
        # comillas. La primera version de esta prueba buscaba
        # `aria-current="page"` y pasaba siempre, sin comprobar nada: una
        # prueba que no puede fallar. Es la misma trampa que ya dio un falso
        # positivo con `alt=""`, anotada en CLAUDE.md.
        menu = re.search(r"<nav id=[\"']?menu-lateral[\"']?.*?</nav>", html, re.S)
        if not menu:
            continue
        n = len(re.findall(r"aria-current=[\"']?page", menu.group(0)))
        if n > 1:
            malas.append("%s (%d)" % (ruta, n))
    assert not malas, (
        "Estas paginas marcan mas de un enlace del menu como la pagina "
        "actual: %s" % ", ".join(malas))


def test_la_ficha_sin_reglas_leidas_si_lo_dice(destino):
    """La otra mitad, la que impide 'arreglar' esto borrando el aviso.

    Hoy el caso real es Benidorm: consta que su ZBE opera desde enero de 2025,
    pero el ayuntamiento no publica de forma legible que distintivos restringe.
    Es el nivel C del CLAUDE.md y el aviso tiene que salir.

    Se exige SOLO a las zonas en vigor. A una zona «prevista» no se le pide
    este aviso: la ficha publica otro distinto, el de que todavia no hay nada
    que cumplir, y decir ademas «no hemos contrastado que distintivos pueden
    circular» seria mentir sobre nuestro propio trabajo. Es el caso de
    Valencia, y esta razonado en la plantilla.
    """
    comprobadas = 0
    faltan = []
    for slug, fm, texto in _fichas():
        if fm.get("estado_dato") == "verificado" and declara_reglas(texto):
            continue
        if fm.get("draft") == "true" or not fm.get("codigo_ine"):
            continue
        if fm.get("estado_zbe") != "activa":
            continue
        html = _html_de(destino, "/zbe/%s/" % slug)
        if html is None:
            continue
        comprobadas += 1
        if AVISO_SIN_VERIFICAR not in html:
            faltan.append(slug)
    assert comprobadas, (
        "No queda ninguna ficha sin reglas leidas, asi que esta prueba ya no "
        "vigila nada. Si es verdad, borrarla; si no, el filtro esta mal."
    )
    assert not faltan, (
        "Estas fichas no tienen reglas leidas y no lo advierten: %s"
        % ", ".join(faltan)
    )


def main():
    destino = _compilar()
    try:
        fallos = 0
        for nombre, f in sorted(globals().items()):
            if not nombre.startswith("test_"):
                continue
            try:
                f(destino)
                print("  ok   %s" % nombre)
            except AssertionError as e:
                fallos += 1
                print("  FALLA %s\n        %s" % (nombre, e))
        print("\n%d prueba(s), %d fallo(s)" % (
            len([n for n in globals() if n.startswith("test_")]), fallos))
        return 1 if fallos else 0
    finally:
        shutil.rmtree(destino, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
