"""
Pipeline ZBE del Punto de Acceso Nacional de la DGT (NAP).

Descarga los ficheros DATEX2 v3 de Zonas de Bajas Emisiones publicados por la
DGT, extrae las restricciones de acceso por distintivo ambiental y genera:

    data/zbe.json            consumo de Hugo
    static/datos/zbe.json    descarga publica
    static/datos/zbe.csv     descarga publica
    pipeline/estado/         cache e historico de cambios

Licencia de los datos de origen: Creative Commons Attribution (CC-BY).
Hay que citar a la DGT como fuente en cualquier publicacion derivada.

PRINCIPIO DE DISENO
-------------------
El parser es deliberadamente conservador. Si la estructura del XML no encaja
con lo que sabemos interpretar, el municipio se marca como
`pendiente_verificacion` y NO se publica ninguna afirmacion sobre sus
distintivos. Es preferible no decir nada a decir algo al reves.

Esto importa especialmente por la semantica de DATEX2: los distintivos
permitidos vienen dentro de un bloque NEGADO. La regla real es

    prohibido entrar   Y NO (distintivo in {0, ECO, C})

es decir, esa lista son los que SI pueden pasar. Un parser que ignore el
`<tra:negate>true</tra:negate>` invertiria el significado por completo.

Uso:
    python pipeline/zbe_nap.py              descarga y regenera
    python pipeline/zbe_nap.py --sin-red    reutiliza la cache
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import unicodedata
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

RAIZ = Path(__file__).resolve().parent.parent
ESTADO = Path(__file__).resolve().parent / "estado"
CACHE = ESTADO / "cache"

URL_DATASET = "https://nap.dgt.es/dataset/zonas-de-bajas-emisiones"
URL_RECURSO = "https://nap.dgt.es/dataset/zonas-de-bajas-emisiones/resource/{id}"

FUENTE_NOMBRE = "Punto de Acceso Nacional de la DGT, Zonas de Bajas Emisiones (DATEX2 v3)"
LICENCIA = "CC-BY (Direccion General de Trafico)"

PAUSA_SEGUNDOS = 0.5  # cortesia con el servidor
AGENTE = "WEBnormativas/0.1 (proyecto de datos abiertos sobre normativa del vehiculo)"

NS = {
    "com": "http://levelC/schema/3/common",
    "tra": "http://levelC/schema/3/trafficRegulation",
    "conz": "http://levelC/schema/3/controlledZone",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

DISTINTIVOS_CONOCIDOS = {"0", "ECO", "C", "B"}

# El NAP nombra algunos recursos de forma confusa o directamente con el
# nombre del fichero. Se corrigen aqui, no en la plantilla, para que el
# dato publicado en /datos/ salga tambien bien.
CORRECCIONES_NOMBRE = {
    "Valencia.xml": "Valencia",
    "Cartuja": "Sevilla (Cartuja)",
    "Sevilla-Cartuja": "Sevilla (Cartuja)",
    "Gasteiz": "Vitoria-Gasteiz",
    "Pamplona Ensanche": "Pamplona (Ensanche)",
}


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------

def slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t


def descargar(url: str, destino: Path, usar_cache: bool) -> str:
    if usar_cache and destino.exists():
        return destino.read_text(encoding="utf-8")
    peticion = urllib.request.Request(url, headers={"User-Agent": AGENTE})
    with urllib.request.urlopen(peticion, timeout=60) as r:
        contenido = r.read().decode("utf-8", errors="replace")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(contenido, encoding="utf-8")
    time.sleep(PAUSA_SEGUNDOS)
    return contenido


def tipo_xsi(el: ET.Element) -> str:
    """Devuelve el xsi:type sin prefijo de espacio de nombres."""
    valor = el.get("{http://www.w3.org/2001/XMLSchema-instance}type", "")
    return valor.split(":")[-1]


# --------------------------------------------------------------------------
# Descubrimiento de recursos
# --------------------------------------------------------------------------

def listar_recursos(usar_cache: bool) -> list[str]:
    html = descargar(URL_DATASET, CACHE / "dataset.html", usar_cache)
    ids = re.findall(r"/dataset/zonas-de-bajas-emisiones/resource/([0-9a-f-]{36})", html)
    vistos, unicos = set(), []
    for i in ids:
        if i not in vistos:
            vistos.add(i)
            unicos.append(i)
    return unicos


def url_xml_de_recurso(id_recurso: str, usar_cache: bool) -> tuple[str, str] | None:
    """Devuelve (nombre_recurso, url_xml) o None si no se encuentra."""
    html = descargar(URL_RECURSO.format(id=id_recurso),
                     CACHE / f"recurso-{id_recurso}.html", usar_cache)
    m = re.search(r'href="(https://nap\.dgt\.es/datex2/[^"]+\.xml)"', html)
    if not m:
        return None
    titulo = re.search(r"<title>(.*?)</title>", html, re.S)
    nombre = id_recurso
    if titulo:
        t = titulo.group(1)
        # El titulo es "... (ZBE) - ZBE <Municipio> | Punto de Acceso...".
        # Se busca "ZBE " seguido del nombre hasta la barra. Partir por "-"
        # rompia los toponimos con guion: "Vitoria-Gasteiz" quedaba en
        # "Gasteiz" y "Donostia - San Sebastian" en "San Sebastian".
        m2 = re.search(r"ZBE\s+(.+?)\s*\|", t, re.S)
        nombre = (m2.group(1) if m2 else t.split("|")[0]).strip()
    nombre = re.sub(r"^ZBE\s+", "", nombre).strip()
    # Recursos mal nombrados en origen: algunos traen el titulo completo del
    # conjunto de datos, o el nombre del fichero con su extension.
    nombre = re.sub(r"^Zonas de Bajas Emisiones\s*\(ZBE\)\s*-\s*", "", nombre).strip()
    nombre = re.sub(r"\.xml$", "", nombre, flags=re.I).strip()
    nombre = CORRECCIONES_NOMBRE.get(nombre, nombre)
    return nombre, m.group(1)


# --------------------------------------------------------------------------
# Parseo DATEX2
# --------------------------------------------------------------------------

def stickers_de(conjunto: ET.Element) -> list[str]:
    """Distintivos declarados dentro de un ConditionSet (sin mirar el negate)."""
    valores = []
    for cond in conjunto.findall("tra:conditions", NS):
        if tipo_xsi(cond) != "NonCodableCondition":
            continue
        if (cond.findtext("tra:active", default="", namespaces=NS) or "").strip() != "true":
            continue
        if (cond.findtext("conz:type", default="", namespaces=NS) or "").strip() != "stickerCondition":
            continue
        for v in cond.findall("conz:condition/com:values/com:value", NS):
            if v.text:
                valores.append(v.text.strip())
    return valores


def horarios_de(raiz: ET.Element) -> list[str]:
    horarios = []
    for periodo in raiz.iter("{%s}recurringTimePeriodOfDay" % NS["com"]):
        ini = periodo.findtext("com:startTimeOfPeriod", default="", namespaces=NS)
        fin = periodo.findtext("com:endTimeOfPeriod", default="", namespaces=NS)
        if ini or fin:
            # "de X a Y" en vez de un guion: las rayas y los guiones largos
            # no se usan en el texto de cara al usuario.
            horarios.append(f"{ini} a {fin}" if (ini and fin) else (ini or fin))
    # sin duplicados, conservando orden
    vistos, unicos = set(), []
    for h in horarios:
        if h not in vistos:
            vistos.add(h)
            unicos.append(h)
    return unicos


def analizar(xml: str, municipio: str, url: str) -> dict:
    """
    Extrae permitidos/prohibidos de un fichero DATEX2 de ZBE.

    Devuelve siempre un registro; la clave `confianza` dice si es publicable:
      oficial                 estructura entendida, distintivos extraidos
      pendiente_verificacion  algo no encaja; no se publica nada sobre stickers
    """
    base = {
        "municipio": municipio,
        "slug": slug(municipio),
        "fuente_nombre": FUENTE_NOMBRE,
        "fuente_url": url,
        "licencia": LICENCIA,
        "fecha_descarga": datetime.now(timezone.utc).date().isoformat(),
        "etiquetas_permitidas": [],
        "etiquetas_prohibidas": [],
        "horario_restriccion": "",
        "publicacion_origen": "",
        "confianza": "pendiente_verificacion",
        "incidencias": [],
    }

    try:
        raiz = ET.fromstring(xml)
    except ET.ParseError as e:
        base["incidencias"].append(f"XML ilegible: {e}")
        return base

    base["publicacion_origen"] = (raiz.findtext("com:publicationTime", default="", namespaces=NS) or "")[:10]

    # ------------------------------------------------------------------
    # Las condiciones por distintivo NO se traducen a reglas publicables.
    #
    # Motivo (comprobado el 22/09/2026 sobre los 45 ficheros del NAP):
    # la misma estructura -- noEntry + ConditionSet con negate=true -- se
    # usa con significados opuestos segun el ayuntamiento que la envia.
    #
    #   A Coruna  negate=true  [0, ECO, C, B]
    #   Madrid    negate=true  [Sin distintivo]
    #   Bilbao    negate=true  [0, ECO, C, B, Sin distintivo]
    #
    # Si el bloque negado fueran los PERMITIDOS, en Madrid solo podrian
    # circular los vehiculos sin distintivo, lo que es falso. Si fueran los
    # PROHIBIDOS, en A Coruna estarian prohibidos todos los distintivos, lo
    # que tambien es falso. Y Bilbao resulta absurdo en ambas lecturas.
    #
    # Es decir: cada ayuntamiento codifica el fichero a su manera. Una
    # interpretacion automatica acertaria en unos municipios y diria justo
    # lo contrario de la verdad en otros. Dado que el error se paga con una
    # multa de 200 EUR, no se publica.
    #
    # Lo que si hacemos es guardar la evidencia en bruto para que la
    # verificacion manual contra la ordenanza sea rapida.
    # ------------------------------------------------------------------
    evidencia = []
    for regulacion in raiz.iter("{%s}trafficRegulation" % NS["tra"]):
        tipo = regulacion.find("tra:typeOfRegulation", NS)
        restriccion = tipo.findtext("tra:accessRestrictionType", default="", namespaces=NS) if tipo is not None else ""
        for conjunto in regulacion.iter("{%s}conditions" % NS["tra"]):
            if tipo_xsi(conjunto) != "ConditionSet":
                continue
            stickers = stickers_de(conjunto)
            if not stickers:
                continue
            negado = (conjunto.findtext("tra:negate", default="false", namespaces=NS) or "false").strip() == "true"
            evidencia.append({
                "restriccion": restriccion,
                "negado": negado,
                "distintivos_declarados": stickers,
            })

    base["evidencia_sin_interpretar"] = evidencia
    base["horario_restriccion"] = "; ".join(horarios_de(raiz))

    if evidencia:
        base["incidencias"].append(
            "Condiciones por distintivo presentes, pero el NAP las codifica de forma "
            "inconsistente entre ayuntamientos. Requiere verificacion manual contra la ordenanza."
        )
    else:
        base["incidencias"].append("El fichero no declara condiciones por distintivo ambiental.")

    # `zbe_existe` si es publicable: lo avala la propia presencia del fichero
    # oficial. Es informacion de nivel C: sabemos que hay zona, no sus reglas.
    base["zbe_existe"] = True
    return base


# --------------------------------------------------------------------------
# Salidas
# --------------------------------------------------------------------------

def registrar_cambios(nuevos: dict) -> list[str]:
    ESTADO.mkdir(parents=True, exist_ok=True)
    anterior_path = ESTADO / "zbe-anterior.json"
    anteriores = {}
    if anterior_path.exists():
        anteriores = json.loads(anterior_path.read_text(encoding="utf-8"))

    cambios = []
    for s, m in nuevos.items():
        if s not in anteriores:
            cambios.append(f"NUEVO    {m['municipio']} ({m['confianza']})")
        else:
            a = anteriores[s]
            for campo in ("etiquetas_permitidas", "horario_restriccion", "confianza"):
                if a.get(campo) != m.get(campo):
                    cambios.append(f"CAMBIO   {m['municipio']}: {campo}: {a.get(campo)!r} -> {m.get(campo)!r}")
    for s, a in anteriores.items():
        if s not in nuevos:
            cambios.append(f"DESAPARECE {a['municipio']}")

    if cambios:
        historico = ESTADO / "cambios.log"
        with historico.open("a", encoding="utf-8") as f:
            f.write(f"\n=== {datetime.now(timezone.utc).isoformat(timespec='seconds')} ===\n")
            f.write("\n".join(cambios) + "\n")

    anterior_path.write_text(json.dumps(nuevos, ensure_ascii=False, indent=1), encoding="utf-8")
    return cambios


def escribir_salidas(municipios: dict) -> None:
    publicables = {s: m for s, m in municipios.items() if m["confianza"] == "oficial"}

    hoy = datetime.now(timezone.utc).date().isoformat()
    meta = {
        "descripcion": "Municipios con Zona de Bajas Emisiones registrada en el NAP de la DGT.",
        "fuente_nombre": FUENTE_NOMBRE,
        "fuente_url": URL_DATASET,
        "licencia": LICENCIA,
        "fecha_actualizacion": hoy,
        "generado_por": "pipeline/zbe_nap.py",
        "ADVERTENCIA": (
            "Este fichero acredita que existe una ZBE y de donde sale el dato. NO contiene "
            "reglas de acceso por distintivo: el NAP las codifica de forma inconsistente "
            "entre ayuntamientos y una lectura automatica diria lo contrario de la verdad en "
            "algunos municipios. Las reglas solo se publican tras leerlas en la ordenanza, "
            "una a una, y entonces `confianza` pasa a 'oficial'."
        ),
        "municipios_con_zbe": len(municipios),
        "con_reglas_verificadas": len(publicables),
    }

    # data/zbe.json — lo consume Hugo.
    # Van TODOS los municipios: saber que existe una ZBE ya es informacion util
    # y verificada. La herramienta distingue por `confianza` y, mientras no sea
    # "oficial", dice que las reglas no estan verificadas en vez de inventarlas.
    (RAIZ / "data").mkdir(exist_ok=True)
    (RAIZ / "data" / "zbe.json").write_text(
        json.dumps({"_meta": meta, "municipios": municipios}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    # static/datos/ — descarga publica, incluidos los descartados con su motivo
    destino = RAIZ / "static" / "datos"
    destino.mkdir(parents=True, exist_ok=True)
    (destino / "zbe.json").write_text(
        json.dumps({"_meta": meta, "municipios": municipios}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    columnas = ["slug", "municipio", "zbe_existe", "etiquetas_permitidas", "horario_restriccion",
                "publicacion_origen", "confianza", "evidencia_sin_interpretar",
                "fuente_url", "fecha_descarga", "incidencias"]
    with (destino / "zbe.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        w.writeheader()
        for m in municipios.values():
            fila = dict(m)
            fila["etiquetas_permitidas"] = "|".join(m.get("etiquetas_permitidas", []))
            fila["incidencias"] = " / ".join(m.get("incidencias", []))
            fila["evidencia_sin_interpretar"] = json.dumps(
                m.get("evidencia_sin_interpretar", []), ensure_ascii=False)
            w.writerow(fila)


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Genera los datos de ZBE desde el NAP de la DGT.")
    ap.add_argument("--sin-red", action="store_true", help="usa la cache local, no descarga nada")
    args = ap.parse_args()
    usar_cache = args.sin_red

    print("Descubriendo recursos en el NAP...")
    ids = listar_recursos(usar_cache)
    print(f"  {len(ids)} recursos")

    municipios: dict[str, dict] = {}
    fallos = 0

    for n, id_recurso in enumerate(ids, 1):
        info = url_xml_de_recurso(id_recurso, usar_cache)
        if not info:
            fallos += 1
            print(f"  [{n}/{len(ids)}] sin URL de descarga ({id_recurso})")
            continue
        nombre, url = info
        try:
            xml = descargar(url, CACHE / f"{slug(nombre)}.xml", usar_cache)
        except Exception as e:  # noqa: BLE001
            fallos += 1
            print(f"  [{n}/{len(ids)}] error descargando {nombre}: {e}")
            continue

        reg = analizar(xml, nombre, url)
        municipios[reg["slug"]] = reg
        marca = "ok " if reg["confianza"] == "oficial" else "-- "
        detalle = ",".join(reg["etiquetas_permitidas"]) or (reg["incidencias"][0] if reg["incidencias"] else "")
        print(f"  [{n}/{len(ids)}] {marca}{nombre}: {detalle}")

    cambios = registrar_cambios(municipios)
    escribir_salidas(municipios)

    publicables = sum(1 for m in municipios.values() if m["confianza"] == "oficial")
    print()
    print(f"Municipios procesados : {len(municipios)}")
    print(f"  publicables         : {publicables}")
    print(f"  sin publicar        : {len(municipios) - publicables}")
    print(f"  fallos de descarga  : {fallos}")
    print(f"Cambios desde la ultima ejecucion: {len(cambios)}")
    for c in cambios[:20]:
        print(f"  {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
