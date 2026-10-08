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
    """Cada .md de content/zbe/, con su ruta publicada, front matter y texto.

    LA RUTA SALE DEL FRONT MATTER, NO DEL NOMBRE DEL FICHERO (08/10/2026).

    Antes se componia `/zbe/<nombre del fichero>/`, y eso dejaba CIEGAS a
    cuatro de estas pruebas justo en las dos paginas donde mas importa:
    `madrid-distrito-centro.md` y `madrid-plaza-eliptica.md` declaran
    `url: "/zbe/madrid/distrito-centro/"`. La ruta inventada no existia en el
    build, `_html_de` devolvia None y los bucles hacian `continue` sin
    comprobar nada.

    Medido: de 23 fichas, 21 encontraban su HTML y esas dos no. Y son
    exactamente el caso 2 del docstring de arriba, en la ciudad con mas
    busquedas del nicho. Reintroducir esa regresion dejaba las diez pruebas
    en verde.

    Por eso ademas existe `_exigir_cobertura()`: «no he podido mirar» no
    puede parecerse a «he mirado y esta bien».
    """
    carpeta = os.path.join(RAIZ, "content", "zbe")
    for nombre in sorted(os.listdir(carpeta)):
        if not nombre.endswith(".md") or nombre == "_index.md":
            continue
        texto = io.open(os.path.join(carpeta, nombre), encoding="utf-8").read()
        fm = front_matter(texto)
        slug = nombre[:-3]
        ruta = fm.get("url") or "/zbe/%s/" % slug
        if not ruta.endswith("/"):
            ruta += "/"
        yield slug, ruta, fm, texto


def _exigir_cobertura(vistas, total, prueba):
    """Falla si la prueba no llego a mirar todo lo que decia mirar.

    El silencio es el modo de fallo de esta clase de prueba: un `continue`
    que trata «no encontre el HTML» igual que «lo mire y estaba bien». Si se
    renombra una pagina o se le pone un `url:` propio, esto lo dice en vez de
    seguir en verde.
    """
    assert vistas == total, (
        "%s solo pudo mirar %d de %d paginas: a las otras no les encontro el "
        "HTML, asi que no ha comprobado nada en ellas." % (prueba, vistas, total))


def test_toda_pagina_de_zbe_declara_su_tipo(destino):
    """
    En content/zbe/ conviven fichas de municipio, paginas de zona, articulos y
    una herramienta, y Hugo les da la misma plantilla a todas: elige por
    seccion, no por lo que la pagina sea. `tipo` es lo unico que las
    distingue.

    Mientras el valor por defecto de la plantilla sostenga alguna pagina real,
    cambiarlo rompe esa pagina y no cambiarlo deja la trampa armada para la
    siguiente. Exigiendo que TODAS lo declaren, el defecto deja de importar y
    se puede dejar en el lado seguro, que es "articulo": una pagina nueva no
    hereda el tratamiento de ficha sin pedirlo.

    Comprobado antes de escribir esto: un articulo normal sin `tipo` salia con
    el recuadro rojo de «Datos sin verificar», con «Las reglas de acceso de
    esta ZBE no estan verificadas» y con la tabla de normativa llena de «No
    consta». Seria la sexta vez que esta trampa se pisa.

    Esta prueba NO lee el HTML: mira el front matter. Esta aqui porque es la
    pareja de las otras, que si lo leen y que replicaban el mismo valor por
    defecto que la plantilla, de modo que una pagina sin declararlo pasaba por
    ficha para las dos y nadie se quejaba.
    """
    sin_tipo = [slug for slug, _, fm, _ in _fichas() if not fm.get("tipo")]
    assert not sin_tipo, (
        "Estas paginas de /zbe/ no declaran `tipo`, asi que dependen del valor "
        "por defecto de la plantilla: %s" % ", ".join(sin_tipo))


def test_ninguna_ficha_verificada_dice_que_no_lo_esta(destino):
    """Lo que paso el 07/10/2026 con Alicante, La Coruna y Pamplona."""
    malas = []
    candidatas = vistas = 0
    for slug, ruta, fm, texto in _fichas():
        # SIN el filtro de `declara_reglas`, a proposito. Estaba y dejaba
        # fuera las dos paginas de zona de Madrid, que responden en prosa y en
        # una tabla escrita a mano, no con `etiquetas_permitidas`. O sea que
        # la prueba escrita por el caso 2 del docstring no cubria el caso 2.
        # `estado_dato: verificado` ya es la senal fuerte: si una pagina dice
        # que esta verificada, no puede publicar que no lo esta, se declaren
        # sus reglas como se declaren.
        if fm.get("estado_dato") != "verificado":
            continue
        candidatas += 1
        html = _html_de(destino, ruta)
        if html is None:
            continue
        vistas += 1
        if AVISO_SIN_VERIFICAR in html:
            malas.append(slug)
    _exigir_cobertura(vistas, candidatas, "ninguna_ficha_verificada_dice_que_no_lo_esta")
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
    candidatas = vistas = 0
    for slug, ruta, fm, _ in _fichas():
        candidatas += 1
        html = _html_de(destino, ruta)
        if html is None:
            continue
        vistas += 1
        if AVISO_SIN_FUENTE not in html:
            continue
        # `tipo` NO se lee con un valor por defecto: replicar aqui el que usa
        # la plantilla hacia que una pagina sin declararlo pasara por ficha
        # para las dos, y la prueba se daba por satisfecha. Lo vigila
        # test_toda_pagina_de_zbe_declara_su_tipo.
        es_ficha = fm.get("tipo") in ("municipio", "zona")
        if not es_ficha or fm.get("estado_dato") == "verificado":
            malas.append("%s (tipo=%s, estado=%s)" % (
                slug, fm.get("tipo", "sin declarar"),
                fm.get("estado_dato", "sin declarar")))
    _exigir_cobertura(vistas, candidatas, "el_aviso_de_datos_sin_verificar_solo_sale_donde_toca")
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
    candidatas = vistas = 0
    for slug, ruta, fm, texto in _fichas():
        # Mismo motivo que arriba: sin el filtro de `declara_reglas`.
        if fm.get("estado_dato") != "verificado":
            continue
        candidatas += 1
        html = _html_de(destino, ruta)
        if html is None:
            continue
        vistas += 1
        if "Sin verificar. No publicamos esta lista" in html:
            malas.append(slug)
    _exigir_cobertura(vistas, candidatas, "la_tabla_de_datos_tampoco_dice_sin_verificar")
    assert not malas, (
        "Estas fichas tienen la ordenanza leida y su tabla de datos dice "
        "«sin verificar»: %s" % ", ".join(malas)
    )


def test_cada_fila_de_la_tabla_comparativa_lleva_su_procedencia(destino):
    """
    /zbe/distintivos-por-ciudad/ da diecisiete respuestas que no existen
    juntas en ningun otro sitio de Espana. Sin la ordenanza y la fecha en la
    misma fila, quien extrae la tabla se lleva la respuesta y no tiene nada
    que atribuir: eso es dar la respuesta, no ser la fuente de la respuesta.

    POR QUE ESTA PRUEBA EXISTE. El dato nacio sin ella. Los campos se leen con
    `| default ""` y se pintan con un `{{- if $f.norma }}`, asi que la
    ausencia no da error: da una celda vacia. Comprobado vaciando
    `fuente_nombre` en zbe-verificados.html: las diecisiete celdas de
    procedencia desaparecen y NINGUNA de las once suites del proyecto falla.
    La pagina vuelve a estar como antes del arreglo y nadie se entera.

    Es el patron que CLAUDE.md llama «un tubo a medio hacer no da ningun
    error»: paso con la ADVERTENCIA del pipeline, con la columna
    `etiquetas_permitidas` vacia y con `dataset_formatos`. Tres veces.

    LA IGUALDAD ES LO IMPORTANTE: tantas procedencias como filas. Asi no se
    puede «arreglar» un fallo quitando la procedencia de todas.
    """
    html = _html_de(destino, "/zbe/distintivos-por-ciudad/")
    assert html, "no se publico /zbe/distintivos-por-ciudad/"
    filas = len(re.findall(r"<th scope=[\"']?row", html))
    conProcedencia = html.count("tabla-distintivos__norma")
    conFecha = html.count("tabla-distintivos__fecha")
    assert filas >= 10, (
        "Solo %d filas en la tabla comparativa. O se han perdido municipios "
        "verificados, o esta prueba ya no esta mirando la tabla." % filas)
    assert conProcedencia == filas, (
        "%d filas y %d con su norma: hay filas que dan una respuesta sin "
        "decir de donde sale." % (filas, conProcedencia))
    assert conFecha == filas, (
        "%d filas y %d con fecha de verificacion: un dato normativo sin "
        "fecha no se puede contrastar." % (filas, conFecha))


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
    # BARRIDO COMPLETO, NO TRES URL A MANO.
    #
    # Estaban escritas: /zbe/granada/, /zbe/pamplona/ y /etiquetas/b/. Una
    # seccion nueva, o una plantilla nueva que rompiera el @id, no estaba
    # cubierta por nadie.
    #
    # Las paginas de /datos/ se saltan a proposito y hay que decir por que:
    # ahi nuestro nodo es un `Dataset` con @id acabado en `#dataset`, no hay
    # ningun `WebPage` nuestro, y la prueba daria un fallo falso. Es una
    # entidad distinta de la pagina que la describe, asi que su @id tambien
    # tiene que serlo.
    fallos = []
    comprobadas = 0
    for ruta in _urls_publicadas(destino):
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
        # El filtro se hace sobre los nodos YA PARSEADOS, no buscando texto en
        # el HTML: el espaciado del JSON depende de como lo serialice Hugo y
        # un `"@type": "Dataset"` con otra separacion no casaba. Comprobado:
        # con el filtro por texto, /datos/zbe/ daba un fallo falso.
        if any(n.get("@type") in ("Dataset", "DataCatalog") for n in nodos):
            continue
        comprobadas += 1
        propios = [n.get("@id") for n in nodos if n.get("@type") == "WebPage"]
        for n in nodos:
            meop = n.get("mainEntityOfPage")
            if not isinstance(meop, dict):
                continue
            if meop.get("@id") not in propios:
                fallos.append(
                    "%s: el %s apunta a %s y nuestro WebPage es %s"
                    % (ruta, n.get("@type"), meop.get("@id"), propios or "(ninguno)"))
    assert comprobadas >= 40, (
        "Solo se han comprobado %d paginas. O el barrido esta roto, o el "
        "filtro de Dataset se esta llevando por delante medio sitio."
        % comprobadas)
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


def _ventana_del_menu(html, ruta):
    """El HTML del menu lateral de una pagina ya compilada.

    TRES COSAS QUE PARECEN DETALLE Y CIEGAN LA PRUEBA ENTERA:

      1. `<nav\b[^>]*\bid=...`, y no `<nav id=...`. Exigir que `id` sea el
         PRIMER atributo convierte un reordenamiento inocente en una prueba
         que no comprueba nada. Verificado: moviendo `class` delante de `id`
         y reintroduciendo a la vez los dos bugs reales del menu, las diez
         pruebas pasaban.
      2. `(.*)` avido y no `(.*?)`. El perezoso corta en el PRIMER `</nav>`,
         asi que un `<nav>` anidado dentro del menu dejaria los enlaces fuera
         de la ventana.
      3. `assert` y no `continue`. Es lo que de verdad importa: si manana
         cambia el marcado y esta expresion deja de casar, la prueba tiene
         que DECIRLO. Un `continue` silencioso convierte «no he podido mirar»
         en «he mirado y esta bien», que es la forma de silencio que
         CLAUDE.md ya tiene anotada con varios nombres.
    """
    m = re.search(r"<nav\b[^>]*\bid=[\"']?menu-lateral[\"']?[^>]*>(.*)</nav>",
                  html, re.S)
    assert m, (
        "No se encontro el menu lateral en %s. Si el marcado ha cambiado hay "
        "que actualizar esta expresion: mientras no case, las pruebas del "
        "menu no comprueban nada." % ruta)
    return m.group(1)


def _secciones_en_el_menu():
    """Las secciones que el menu lateral cubre, SACADAS DEL MISMO DATO.

    Estaba escrita a mano: anadir una seccion al menu y olvidarse de esta
    tupla dejaba sus paginas sin comprobar, en silencio. Ahora sale de
    data/menu_lateral.json, que es lo que lee la plantilla.
    """
    ruta = os.path.join(RAIZ, "data", "menu_lateral.json")
    datos = json.loads(io.open(ruta, encoding="utf-8").read())
    secciones = set()
    for grupo in datos.get("grupos", []):
        for enlace in grupo.get("enlaces", []):
            if enlace.get("proximamente"):
                continue
            trozos = (enlace.get("url") or "").strip("/").split("/")
            if trozos and trozos[0]:
                secciones.add(trozos[0])
    assert secciones, "no se han podido leer las secciones de menu_lateral.json"
    return secciones


SECCIONES_EN_EL_MENU = _secciones_en_el_menu()


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
        menu = _ventana_del_menu(html, ruta)
        # `open` minificado va sin valor, igual que `alt`.
        if not re.search(r"<details[^>]*\bopen\b", menu):
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
        menu = _ventana_del_menu(html, ruta)
        n = len(re.findall(r"aria-current=[\"']?page", menu))
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
    candidatas = 0
    for slug, ruta, fm, texto in _fichas():
        if fm.get("estado_dato") == "verificado" and declara_reglas(texto):
            continue
        if fm.get("draft") == "true" or not fm.get("codigo_ine"):
            continue
        if fm.get("estado_zbe") != "activa":
            continue
        candidatas += 1
        html = _html_de(destino, ruta)
        if html is None:
            continue
        comprobadas += 1
        if AVISO_SIN_VERIFICAR not in html:
            faltan.append(slug)
    _exigir_cobertura(comprobadas, candidatas, "la_ficha_sin_reglas_leidas_si_lo_dice")
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
