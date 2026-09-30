# -*- coding: utf-8 -*-
"""
Extrae la geometria de las Zonas de Bajas Emisiones del NAP de la DGT.

Los ficheros DATEX2 ya descargados por zbe_nap.py en pipeline/estado/cache/
contienen los perimetros dentro de <loc:openlrPolygonCorners>. zbe_nap.py los
descarta porque solo le interesan las reglas; aqui se aprovechan.

Es el activo diferencial del proyecto: ningun competidor publica los poligonos.
Licencia CC-BY de la DGT, asi que la atribucion es obligatoria alli donde se
pinten.
"""

# Rectangulo que contiene Espana entera: peninsula, Baleares, Canarias, Ceuta
# y Melilla, con margen. Cualquier punto fuera es un error de lectura, no un
# municipio exotico.
import io
import os

LIMITES = {"lat": (27.0, 44.0), "lon": (-19.0, 5.0)}


def _dentro(lat, lon):
    return (LIMITES["lat"][0] <= lat <= LIMITES["lat"][1]
            and LIMITES["lon"][0] <= lon <= LIMITES["lon"][1])


def verificar_punto(lat, lon, contexto=""):
    """
    Revienta si el punto no cae en Espana.

    Distingue dos casos, porque la causa y el arreglo son distintos:
      - Encaja al darle la vuelta: latitud y longitud estan invertidas. Es el
        error habitual, porque DATEX2 las da por separado y GeoJSON las quiere
        como [longitud, latitud], al reves de como se leen en voz alta.
      - No encaja de ninguna manera: el dato de origen esta mal o se esta
        leyendo la etiqueta equivocada.
    """
    if _dentro(lat, lon):
        return
    if _dentro(lon, lat):
        raise ValueError(
            "%s: el punto (%s, %s) cae fuera de Espana, pero encaja al darle la "
            "vuelta. Latitud y longitud estan invertidas." % (contexto, lat, lon))
    raise ValueError(
        "%s: el punto (%s, %s) cae fuera de Espana y tampoco encaja invertido."
        % (contexto, lat, lon))


import xml.etree.ElementTree as ET

# El prefijo loc: es el mismo en los 50 ficheros del cache, comprobado.
NS = {"loc": "http://levelC/schema/3/locationReferencing"}


def anillos_de_fichero(ruta, incidencias=None):
    """
    Devuelve los anillos del fichero, cada uno como lista de pares
    [longitud, latitud].

    Cada <loc:openlrPolygonCorners> es un anillo: A Coruna tiene tres, con
    1.026 puntos entre los tres.

    El orden es [lon, lat] y no [lat, lon] porque es lo que exige GeoJSON, al
    reves de como lo da DATEX2 y al reves de como se dice en voz alta.

    Un anillo con algun punto fuera de Espana se descarta entero y se anota en
    `incidencias`. Esto no es paranoia: alicante.xml mezcla dos sistemas de
    coordenadas dentro del mismo fichero, 26 de sus 47 puntos en UTM y el
    resto en grados, sin declarar cual es cual. Adivinar la proyeccion
    dibujaria la zona en otro sitio, que es peor que no dibujarla.
    """
    raiz = ET.parse(ruta).getroot()
    nombre = os.path.basename(ruta)
    anillos = []

    for indice, corners in enumerate(raiz.iter("{%s}openlrPolygonCorners" % NS["loc"])):
        anillo = []
        problema = None
        for par in corners.findall("loc:openlrCoordinates", NS):
            lat = float(par.findtext("loc:latitude", namespaces=NS))
            lon = float(par.findtext("loc:longitude", namespaces=NS))
            try:
                verificar_punto(lat, lon, nombre)
            except ValueError as e:
                problema = str(e)
                break
            anillo.append([lon, lat])

        if problema:
            if incidencias is not None:
                incidencias.append(
                    "%s: anillo %d descartado, no esta en grados WGS84. %s"
                    % (nombre, indice, problema))
            continue

        # GeoJSON exige el anillo cerrado. El NAP no siempre lo cierra.
        if anillo and anillo[0] != anillo[-1]:
            anillo.append(list(anillo[0]))

        if len(anillo) >= 4:
            anillos.append(anillo)

    return anillos


import math


def _distancia_al_segmento(p, a, b):
    """
    Distancia perpendicular del punto p al segmento a-b.

    Si a y b coinciden, que es lo que pasa en la primera pasada de un anillo
    cerrado (el primer punto y el ultimo son el mismo), degenera en la
    distancia entre dos puntos. Eso hace que la primera division del anillo
    caiga en su vertice mas lejano, que es justo donde interesa partirlo.
    """
    if a == b:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    dx, dy = b[0] - a[0], b[1] - a[1]
    # Area del paralelogramo dividida por la base.
    return abs(dy * p[0] - dx * p[1] + b[0] * a[1] - b[1] * a[0]) / math.hypot(dx, dy)


def _rdp(puntos, tolerancia):
    """Ramer-Douglas-Peucker. A mano: no merece una dependencia nueva."""
    if len(puntos) < 3:
        return [list(p) for p in puntos]

    dmax, corte = 0.0, 0
    for i in range(1, len(puntos) - 1):
        d = _distancia_al_segmento(puntos[i], puntos[0], puntos[-1])
        if d > dmax:
            dmax, corte = d, i

    if dmax <= tolerancia:
        return [list(puntos[0]), list(puntos[-1])]

    izquierda = _rdp(puntos[:corte + 1], tolerancia)
    derecha = _rdp(puntos[corte:], tolerancia)
    return izquierda[:-1] + derecha


def simplificar(anillo, tolerancia):
    """
    Reduce los puntos de un anillo conservando su forma.

    La tolerancia va en grados: 0.0001 son unos once metros, de sobra para un
    mapa que se ve a escala de ciudad. El fichero completo se publica sin
    simplificar en /datos/; esto es solo para lo que carga el navegador.

    Nunca devuelve menos de cuatro puntos: con menos deja de ser un poligono
    valido en GeoJSON, y una tolerancia grande tiende a dejar dos.
    """
    if len(anillo) <= 4:
        return [list(p) for p in anillo]

    salida = _rdp(anillo, tolerancia)
    if salida[0] != salida[-1]:
        salida.append(list(salida[0]))

    if len(salida) < 4:
        paso = max(1, (len(anillo) - 1) // 3)
        salida = [list(anillo[i]) for i in range(0, len(anillo) - 1, paso)][:3]
        salida.append(list(salida[0]))

    return salida


import json
import re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(RAIZ, "pipeline", "estado", "cache")


# El NAP nombra sus ficheros como le conviene a la DGT y de ahi sale el slug
# de cada zona. Cuando la ficha se publica con otro nombre, la equivalencia va
# aqui: si no, el mapa enlaza a un 404.
FICHAS = {
    # RondasDeBarcelona.xml. La pagina se llama Barcelona porque es como la
    # busca la gente, y porque la ordenanza que se cita es la de la ciudad.
    "rondas-de-barcelona": "barcelona",
}

# Nombre con el que sale la zona en el mapa. El selector ordena los 45
# municipios alfabeticamente, y con el nombre del NAP la segunda ciudad del
# pais quedaba en la erre, donde nadie la busca.
#
# Los tres topominos bilingues estan por el mismo motivo, y ademas van en
# castellano a secas: aqui el visitante ya sabe que ciudad quiere, asi que la
# forma doble ("Gerona / Girona") solo alarga el desplegable. La forma doble,
# que es la que atiende las dos busquedas, vive en data/zbe.json y sale en el
# listado de /zbe/ y en las descargas de /datos/. La tabla de alla es
# NOMBRES_BILINGUES, en pipeline/zbe_nap.py.
NOMBRES = {
    "rondas-de-barcelona": "Barcelona (ZBE Rondas)",
    "girona": "Gerona",
    "lleida": "Lérida",
    "donostia-san-sebastian": "San Sebastián",
}


def _ficha_de(slug):
    """
    Devuelve (url, estado_dato) de la ficha publicada de ese municipio, o
    (None, "pendiente") si no hay ninguna.

    La URL no se construye a ciegas: si el fichero no existe o es borrador, el
    mapa enlazaria a un 404. Preferible que la zona salga sin enlace.
    """
    slug = FICHAS.get(slug, slug)
    ruta = os.path.join(RAIZ, "content", "zbe", slug + ".md")
    if not os.path.exists(ruta):
        return None, "pendiente"

    cabecera = io.open(ruta, encoding="utf-8").read().split("---")[1]
    if re.search(r"^draft:\s*true", cabecera, re.M):
        return None, "pendiente"

    m = re.search(r'^estado_dato:\s*"?([a-z_]+)"?', cabecera, re.M)
    return "/zbe/%s/" % slug, (m.group(1) if m else "pendiente")


# Cuanto mayor tiene que ser una zona respecto de la siguiente para
# considerarla el contexto de las demas y no una restriccion mas. Madrid esta
# en 183 veces; Las Rozas, donde las cinco zonas son hermanas, en 1,19.
FACTOR_ENVOLVENTE = 5.0


def indice_envolvente(areas):
    """
    Devuelve la posicion de la zona que hace de contexto, o None si no hay.

    Una zona es envolvente cuando el municipio declara varias y ella contiene
    a las demas. No se comprueba la contencion geometrica: basta con que sea
    la mayor por un margen amplio, que es como se presenta el unico caso real
    (Madrid, 1.152 km2 frente a 6,3 de Distrito Centro).

    El criterio anterior miraba solo el tamano absoluto, y dejaba la ZBE
    Rondes de Barcelona pintada en gris casi transparente pese a ser ella
    misma la que restringe: no tiene ninguna zona dentro.
    """
    if len(areas) < 2:
        return None
    orden = sorted(range(len(areas)), key=lambda i: -areas[i])
    mayor, segunda = areas[orden[0]], areas[orden[1]]
    if segunda <= 0 or mayor < segunda * FACTOR_ENVOLVENTE:
        return None
    return orden[0]


def construir_geojson(tolerancia=None):
    """
    Monta la coleccion completa: UNA FEATURE POR ZONA, no por municipio.

    Madrid tiene tres zonas con reglas distintas y tamanos que se diferencian
    en dos ordenes de magnitud. Fusionarlas pintaba el termino municipal
    entero de un color y las dos ZBEDEP desaparecian debajo.

    `km2` va en las propiedades para que el mapa pueda pintar las grandes
    debajo y las pequenas encima, sin inventarse una clasificacion que el dato
    no trae.

    `tolerancia` en grados simplifica la geometria; sin ella se devuelve tal
    cual. Se publican las dos versiones: la completa como dato abierto y la
    simplificada para el navegador.
    """
    datos = json.load(io.open(os.path.join(RAIZ, "data", "zbe.json"), encoding="utf-8"))
    features = []
    incidencias = []

    for slug in sorted(datos["municipios"]):
        m = datos["municipios"][slug]
        ruta = os.path.join(CACHE, slug + ".xml")
        if not os.path.exists(ruta):
            continue

        zonas = zonas_de_fichero(ruta, incidencias)
        if not zonas:
            continue

        url, estado = _ficha_de(slug)
        varias = len(zonas) > 1
        areas = [extension_km2(z) for z in zonas]
        envolvente = indice_envolvente(areas)

        for indice_zona, zona in enumerate(zonas):
            km2 = areas[indice_zona]
            anillos = zona["anillos"]
            if tolerancia:
                anillos = [simplificar(a, tolerancia) for a in anillos]
                anillos = [a for a in anillos if len(a) >= 4]
            if not anillos:
                continue

            if len(anillos) == 1:
                geometria = {"type": "Polygon", "coordinates": [anillos[0]]}
            else:
                # Varios anillos de la MISMA zona: partes separadas de ella,
                # no agujeros. Distrito Centro tiene seis.
                geometria = {"type": "MultiPolygon", "coordinates": [[a] for a in anillos]}

            features.append({
                "type": "Feature",
                "geometry": geometria,
                "properties": {
                    "slug": slug,
                    "id_zona": "%s-%d" % (slug, zona["indice"]),
                    "municipio": NOMBRES.get(slug, m.get("municipio", slug)),
                    # El nombre que le da el ayuntamiento. Solo se muestra
                    # aparte cuando el municipio tiene mas de una.
                    "zona": zona["nombre"] if varias else "",
                    "provincia": m.get("provincia", ""),
                    "km2": round(km2, 2),
                    # Marca la zona que solo sirve de contexto: el mapa la
                    # dibuja con trazo discontinuo para no dar a entender que
                    # toda la ciudad esta cerrada.
                    "envolvente": indice_zona == envolvente,
                    "estado_dato": estado,
                    "url_ficha": url,
                    "fuente_nombre": m.get("fuente_nombre", ""),
                    "fuente_url": m.get("fuente_url", ""),
                    "fecha_descarga": m.get("fecha_descarga", ""),
                },
            })

    # Las grandes primero: asi el mapa las dibuja debajo y las pequenas, que
    # son las que de verdad restringen, quedan encima y se pueden pulsar.
    features.sort(key=lambda f: -f["properties"]["km2"])

    return {
        "type": "FeatureCollection",
        "_meta": {
            "descripcion": "Perimetros de las Zonas de Bajas Emisiones de Espana, una por zona.",
            "fuente": "DGT, Punto de Acceso Nacional de Trafico y Movilidad",
            "licencia": "CC-BY. La atribucion a la DGT es obligatoria al reutilizar.",
            "generado_por": "pipeline/zbe_geometria.py",
            "ADVERTENCIA": "El perimetro oficial lo fija la ordenanza municipal. "
                           "Esta geometria es la que publica la DGT y sirve para "
                           "orientarse, no para decidir si se puede circular.",
            "incidencias": incidencias,
        },
        "features": features,
    }

def _local(elemento):
    return re.sub(r"^\{.*\}", "", elemento.tag)


# Erratas del propio origen. La sigla correcta es ZBEDEP, "Zona de Bajas
# Emisiones De Especial Proteccion", y el NAP la escribe mal en Madrid.
# Se corrige aqui y no en el JavaScript: el dato que publicamos en
# /datos/ tambien debe salir bien.
CORRECCIONES_ZONA = {
    "ZBEDPE Distrito Centro": "ZBEDEP Distrito Centro",
    "ZBEDPE  Distrito Centro": "ZBEDEP Distrito Centro",
}


def _nombre_de_zona(zona):
    """
    El nombre que el ayuntamiento le pone a la zona, dentro de <name><value>.

    Llega como "Madrid (ZBEDEP Plaza Eliptica)": se queda con lo de dentro del
    parentesis, que es lo que distingue una zona de otra dentro del mismo
    municipio. Si no hay parentesis, se devuelve tal cual.
    """
    for hijo in zona:
        if _local(hijo) != "name":
            continue
        for sub in hijo.iter():
            texto = (sub.text or "").strip()
            if not texto:
                continue
            m = re.search(r"\(([^)]+)\)", texto)
            bruto = re.sub(r"\s{2,}", " ", (m.group(1) if m else texto)).strip()
            return CORRECCIONES_ZONA.get(bruto, bruto)
    return ""


def zonas_de_fichero(ruta, incidencias=None):
    """
    Devuelve una lista de zonas, no de anillos.

    Cada <controlledZone> del DATEX2 es UNA zona con su nombre y sus poligonos.
    Madrid tiene tres: el termino municipal entero, la ZBEDEP de Distrito
    Centro y la de Plaza Eliptica.

    Esto existe porque fusionar los 52 anillos de Madrid en una sola geometria
    pintaba el municipio entero de un color y hacia desaparecer debajo las dos
    zonas que de verdad restringen. Una zona del mapa es una controlledZone.
    """
    raiz = ET.parse(ruta).getroot()
    nombre_fichero = os.path.basename(ruta)
    slug_municipio = os.path.splitext(nombre_fichero)[0]
    salida = []

    for indice, zona in enumerate(e for e in raiz.iter() if _local(e) == "controlledZone"):
        anillos = []
        for pos, corners in enumerate(zona.iter("{%s}openlrPolygonCorners" % NS["loc"])):
            anillo = []
            problema = None
            for par in corners.findall("loc:openlrCoordinates", NS):
                lat = float(par.findtext("loc:latitude", namespaces=NS))
                lon = float(par.findtext("loc:longitude", namespaces=NS))
                try:
                    verificar_punto(lat, lon, nombre_fichero)
                except ValueError as e:
                    problema = str(e)
                    break
                anillo.append([lon, lat])

            if problema:
                if incidencias is not None:
                    incidencias.append(
                        "%s: anillo %d descartado, no esta en grados WGS84. %s"
                        % (nombre_fichero, pos, problema))
                continue

            if anillo and anillo[0] != anillo[-1]:
                anillo.append(list(anillo[0]))
            if len(anillo) >= 4:
                anillos.append(anillo)

        if not anillos:
            continue

        salida.append({
            "nombre": _nombre_de_zona(zona) or slug_municipio,
            "slug_municipio": slug_municipio,
            "indice": indice,
            "anillos": anillos,
        })

    return salida


def extension_km2(zona):
    """
    Superficie aproximada del rectangulo que contiene la zona.

    No es el area del poligono y no pretende serlo: sirve para ordenar zonas
    por tamano y para decidir cual se pinta encima de cual.
    """
    puntos = [p for anillo in zona["anillos"] for p in anillo]
    lats = [p[1] for p in puntos]
    lons = [p[0] for p in puntos]
    alto = (max(lats) - min(lats)) * 111.0
    ancho = (max(lons) - min(lons)) * 111.0 * math.cos(math.radians(sum(lats) / len(lats)))
    return alto * ancho


def centroide(feature):
    """
    Devuelve (latitud, longitud) del centro de una zona, como media de sus
    vertices.

    No es el centroide geometrico exacto, y no hace falta: sirve para situar
    la zona en el mapa y para comprobar que cae sobre su ciudad.
    """
    g = feature["geometry"]
    poligonos = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
    puntos = [p for poly in poligonos for anillo in poly for p in anillo]
    return (sum(p[1] for p in puntos) / len(puntos),
            sum(p[0] for p in puntos) / len(puntos))


# Tolerancia de simplificacion, en grados. 0.00005 son unos cinco metros y
# medio: invisible a escala de ciudad, que es como se mira este mapa.
TOLERANCIA_MAPA = 0.00005

SALIDA_COMPLETA = os.path.join(RAIZ, "static", "datos", "zbe.geojson")
SALIDA_MAPA = os.path.join(RAIZ, "static", "datos", "zbe-simplificado.geojson")


import datetime

SALIDA_RESUMEN = os.path.join(RAIZ, "data", "zbe_resumen.json")


def resumen(coleccion):
    """
    Cuenta lo que hay en la coleccion para que la plantilla no tenga que
    escribir el numero a mano.

    La pagina del mapa decia "45 zonas" porque ese era el numero cuando cada
    municipio era una sola figura. Al separar las tres zonas de Madrid pasaron
    a ser 57 en 45 municipios, y el texto se quedo viejo sin que nada avisara.
    """
    zonas = coleccion["features"]
    por_municipio = {}
    for f in zonas:
        slug = f["properties"]["slug"]
        por_municipio[slug] = por_municipio.get(slug, 0) + 1
    envolventes = sum(1 for f in zonas if f["properties"].get("envolvente"))
    return {
        "zonas": len(zonas),
        # Las envolventes no se pintan: la de Madrid abarca el termino
        # municipal entero y hacia creer que toda la ciudad esta cerrada.
        "envolventes": envolventes,
        "zonas_con_restriccion": len(zonas) - envolventes,
        "municipios": len(por_municipio),
        "municipios_con_varias_zonas": sum(1 for n in por_municipio.values() if n > 1),
        "generado": datetime.date.today().isoformat(),
    }


def _escribir(ruta, coleccion, compacto):
    separadores = (",", ":") if compacto else (", ", ": ")
    with io.open(ruta, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(coleccion, ensure_ascii=False,
                            indent=None if compacto else 2,
                            separators=separadores))
    return os.path.getsize(ruta)


def main():
    completa = construir_geojson()
    simple = construir_geojson(TOLERANCIA_MAPA)

    # La completa se publica como dato abierto y va legible; la del mapa la
    # descarga el navegador en cada visita, asi que va compacta.
    a = _escribir(SALIDA_COMPLETA, completa, compacto=False)
    b = _escribir(SALIDA_MAPA, simple, compacto=True)

    # El resumen va a data/ para que Hugo lo lea sin plugins: es la unica via
    # de que los numeros de la pagina del mapa no se queden viejos.
    with io.open(SALIDA_RESUMEN, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(resumen(simple), ensure_ascii=False, indent=2))

    puntos = lambda c: sum(
        len(anillo)
        for f in c["features"]
        for poly in ([f["geometry"]["coordinates"]]
                     if f["geometry"]["type"] == "Polygon"
                     else f["geometry"]["coordinates"])
        for anillo in poly)

    print("zonas:                %d" % len(completa["features"]))
    print("puntos completos:     %d" % puntos(completa))
    print("puntos simplificados: %d" % puntos(simple))
    print("zbe.geojson:          %.0f KB" % (a / 1024.0))
    print("zbe-simplificado:     %.0f KB" % (b / 1024.0))
    for inc in completa["_meta"]["incidencias"]:
        print("INCIDENCIA: %s" % inc)


if __name__ == "__main__":
    main()
