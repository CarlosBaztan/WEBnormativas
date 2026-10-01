"""
Auditoria de frescura y coherencia del contenido.

Comprueba cinco cosas y devuelve codigo de salida 1 si encuentra algo:

  1. Fichas cuya `fecha_verificacion` tiene mas de 6 meses.
  2. Desincronizacion entre `estado_dato` y `draft`.
     La regla del proyecto es: estado_dato: pendiente  <=>  draft: true.
     Si se rompe, un dato sin verificar puede acabar publicado.
  3. Fichas marcadas como verificadas a las que les falta la trazabilidad
     (fuente_nombre, fuente_url o fecha_verificacion). El flag por si solo
     no basta para afirmar nada.
  4. Fichas de municipio verificadas que no declaran ninguna regla de acceso.
  5. Notas internas ({{VERIFICAR}}, "pendiente de verificar") que se quedan
     en el cuerpo de una pagina publicada. Hugo no las interpreta: se
     imprimen tal cual y las lee el visitante.

Uso:
    python pipeline/auditoria.py
    python pipeline/auditoria.py --meses 3
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONTENIDO = RAIZ / "content"


def front_matter(texto: str) -> dict[str, str]:
    """Parseo superficial del front matter YAML: solo claves escalares."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.S)
    if not m:
        return {}
    campos = {}
    for linea in m.group(1).splitlines():
        km = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*)\s*:\s*(.*)$", linea)
        if km:
            campos[km.group(1)] = km.group(2).strip().strip('"').strip("'")
    return campos


# Los tres estados posibles de una ficha, que se corresponden con los niveles
# de confianza de CLAUDE.md:
#
#   verificado  nivel A o B: reglas leidas en el texto oficial. Responde
#               "¿puedo entrar?" y alimenta la herramienta.
#   parcial     nivel C: consta que la ZBE existe, con su fuente y su fecha,
#               pero no hemos podido leer las reglas de acceso. La ficha SE
#               PUBLICA, dice lo que sabe y NO responde "¿puedo entrar?".
#   pendiente   nivel D: no hay nada solido. No se publica.
ESTADOS_PUBLICABLES = ("verificado", "parcial")


def publicable(fm: dict) -> bool:
    """Si esta ficha puede llegar a produccion con lo que sabemos de ella."""
    return fm.get("estado_dato", "") in ESTADOS_PUBLICABLES


def incoherente(fm: dict) -> bool:
    """
    Detecta el desajuste entre lo que la ficha dice saber y si se publica.

    Lo grave es publicar un "pendiente": seria un dato sin verificar en
    produccion. Al reves, un "verificado" en borrador es trabajo tirado, y
    tambien se avisa.
    """
    estado = fm.get("estado_dato", "")
    draft = str(fm.get("draft", "")).lower() == "true"
    if estado == "pendiente" and not draft:
        return True
    if estado in ESTADOS_PUBLICABLES and draft:
        return True
    return False


# Notas internas que nunca pueden llegar al lector.
#
# `{{VERIFICAR}}` es la marca que se deja en el cuerpo cuando un dato no esta
# contrastado todavia. Parece una plantilla, pero Hugo no la interpreta:
# Goldmark imprime las llaves tal cual, asi que la nota se publica. Estuvo
# cuatro veces a la vista en /multas/zbe/ y dos mas en otras paginas sin que
# nada avisara, porque ninguna comprobacion miraba el cuerpo del texto.
#
# Solo se vigila la marca literal, a proposito.
#
# El primer intento incluia tambien la frase "pendiente de verificar", y daba
# un falso positivo en la ficha de Madrid, donde cinco celdas de la tabla de
# distintivos dicen exactamente eso. Ahi no es un descuido: es la respuesta
# honesta que exigen las reglas de publicacion del proyecto cuando una zona no
# se ha podido contrastar. Distinguir por el texto entre "no lo sabemos y lo
# decimos" y "nota que se me olvido borrar" no se puede hacer con una busqueda,
# asi que la comprobacion se queda con lo que no admite duda.
# La segunda marca, `<!-- PENDIENTE`, es la nota que se deja en un comentario
# de HTML. El visitante no la ve, pero viaja en el codigo fuente de la pagina
# publicada y delata que algo quedo a medias. Habia tres sin cerrar el dia que
# se conecto el dominio: dos en /sobre/ y una en /legal/contacto/, las tres
# diciendo "antes de lanzar".
#
# Se busca con el comentario y en mayusculas a proposito, para no confundirla
# con la palabra "pendiente" en prosa, que aqui es vocabulario corriente.
MARCADORES = (
    "{{VERIFICAR}}",
    "<!-- PENDIENTE",
)


def cuerpo(texto: str) -> str:
    """
    Lo que ve el lector: todo lo que va despues del front matter.

    La distincion importa. Una nota en el front matter es para nosotros y no
    se publica; la misma frase tres lineas mas abajo si.
    """
    m = re.match(r"^---\s*\n.*?\n---\s*\n", texto, re.S)
    return texto[m.end():] if m else texto


def marcadores_sin_resolver(texto: str) -> list[str]:
    """Marcas de MARCADORES que se han quedado en el cuerpo de la pagina."""
    visible = cuerpo(texto).lower()
    return [m for m in MARCADORES if m.lower() in visible]


def paginas_publicadas():
    """
    Cada pagina que llega a produccion, como (ruta relativa, texto completo).

    Incluye los `_index.md`, al reves que el recorrido de fichas de `main`:
    son paginas de seccion con texto propio, y una nota olvidada ahi se ve
    igual de bien. El primer caso real fue el de /etiquetas/.
    """
    for ruta in sorted(CONTENIDO.rglob("*.md")):
        texto = ruta.read_text(encoding="utf-8")
        if str(front_matter(texto).get("draft", "")).lower() == "true":
            continue
        yield ruta.relative_to(RAIZ).as_posix(), texto


def declara_reglas(texto: str) -> bool:
    """
    Dice si la ficha declara algo sobre quien puede circular.

    Una ficha marcada como verificada que no declara reglas es el peor caso
    posible: el lector ve el sello de comprobado y una pagina que no responde
    a nada. Vale cualquiera de las dos formas que usa el proyecto:

      - `etiquetas_permitidas` con contenido, para municipios de una sola zona.
      - un bloque `zonas`, para los que tienen varias con reglas distintas,
        como Madrid.

    Se mira sobre el texto crudo porque front_matter() solo lee escalares y
    las dos son listas.
    """
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", texto, re.S)
    if not m:
        return False
    cabecera = m.group(1)

    if re.search(r"^zonas:\s*$", cabecera, re.M):
        return True

    et = re.search(r"^etiquetas_permitidas:\s*(.*)$", cabecera, re.M)
    if not et:
        return False
    resto = et.group(1).strip()
    if resto in ("", "[]"):
        # Puede continuar en lineas con guion debajo.
        return bool(re.match(r"\s*\n\s*-\s*\S", cabecera[et.end():]))
    return True


def exige_reglas(fm: dict) -> bool:
    """
    Dice si a esta ficha hay que exigirle reglas de acceso.

    Solo se le exigen a la ficha de un municipio (la distingue codigo_ine)
    cuya ZBE esta activa. Una zona "prevista" no tiene reglas en vigor que
    declarar, y exigirselas obligaria a inventarlas o a no publicar una ficha
    que si aporta.

    Sale del caso de Valencia (28/09/2026): ordenanza aprobada solo
    inicialmente, con el propio ayuntamiento diciendo que la aprobacion
    definitiva sigue pendiente. Que eso conste, fechado y con su fuente, es
    justamente lo que no publica nadie.
    """
    if not fm.get("codigo_ine"):
        return False
    if fm.get("tipo", "municipio") != "municipio":
        return False
    # A una ficha "parcial" no se le exigen reglas: no tenerlas es
    # precisamente lo que la hace parcial.
    if fm.get("estado_dato", "") != "verificado":
        return False
    return fm.get("estado_zbe", "") == "activa"


def enlaces_rotos(fuentes: dict, comprobador=None) -> list:
    """
    Comprueba que las fuentes citadas siguen en pie.

    `fuentes` es {ruta de la ficha: url}. `comprobador` recibe una url y
    devuelve su codigo HTTP; se inyecta para poder probar esto sin red, y para
    que la auditoria de cada dia no dependa de que los ayuntamientos esten
    levantados.

    Un enlace que no responde cuenta como roto: para el lector es lo mismo.
    """
    if comprobador is None:
        comprobador = _codigo_http

    rotos = []
    for ficha, url in sorted(fuentes.items()):
        try:
            codigo = comprobador(url)
        except Exception as e:
            rotos.append("%s: %s no responde (%s)" % (ficha, url, e))
            continue
        if codigo >= 400:
            rotos.append("%s: %s devuelve %s" % (ficha, url, codigo))
    return rotos


def _codigo_http(url: str) -> int:
    """Peticion real. Aislada aqui para que enlaces_rotos sea testeable."""
    import urllib.request

    peticion = urllib.request.Request(url, method="HEAD", headers={
        "User-Agent": "CocheApto/auditoria (+https://cocheapto.com)"})
    with urllib.request.urlopen(peticion, timeout=20) as r:
        return r.status


def main() -> int:
    ap = argparse.ArgumentParser(description="Audita frescura y coherencia de las fichas.")
    ap.add_argument("--meses", type=int, default=6, help="antiguedad maxima admitida (por defecto 6)")
    ap.add_argument("--enlaces", action="store_true",
                    help="comprueba ademas que las fuentes citadas siguen respondiendo "
                         "(hace peticiones de red; se usa en la auditoria semanal)")
    args = ap.parse_args()

    limite = date.today() - timedelta(days=args.meses * 30)

    caducadas: list[str] = []
    incoherentes: list[str] = []
    sin_trazabilidad: list[str] = []
    sin_reglas: list[str] = []
    fuentes: dict[str, str] = {}
    revisadas = 0

    for ruta in sorted(CONTENIDO.rglob("*.md")):
        if ruta.name == "_index.md":
            continue
        fm = front_matter(ruta.read_text(encoding="utf-8"))
        if "estado_dato" not in fm:
            continue

        revisadas += 1
        rel = ruta.relative_to(RAIZ).as_posix()
        estado = fm.get("estado_dato", "")
        draft = fm.get("draft", "").lower() == "true"

        # 2. Coherencia estado_dato <-> draft
        if incoherente(fm):
            if estado == "pendiente":
                incoherentes.append(f"{rel}: estado_dato=pendiente pero draft=false (SE PUBLICARIA)")
            else:
                incoherentes.append(f"{rel}: estado_dato={estado} pero draft=true (no se publica)")

        # La trazabilidad y la frescura se exigen a todo lo que se publica,
        # tambien a las fichas parciales: si decimos que hay una ZBE, hay que
        # decir de donde lo sabemos y cuando lo miramos.
        if not publicable(fm):
            continue

        # 3. Trazabilidad completa
        faltan = [c for c in ("fuente_nombre", "fuente_url", "fecha_verificacion") if not fm.get(c)]
        if faltan:
            sin_trazabilidad.append(f"{rel}: verificada pero le falta {', '.join(faltan)}")
            continue

        # 1. Frescura
        fv = fm["fecha_verificacion"]
        try:
            fecha = date.fromisoformat(fv)
        except ValueError:
            sin_trazabilidad.append(f"{rel}: fecha_verificacion invalida ({fv!r})")
            continue
        if fecha < limite:
            dias = (date.today() - fecha).days
            caducadas.append(f"{rel}: verificada hace {dias} dias ({fv})")

        fuentes[rel] = fm["fuente_url"]

        # 4. Una ficha de municipio verificada tiene que decir algo sobre quien
        #    puede circular. El sello de verificado sobre una pagina que no
        #    responde a nada es peor que no tener la pagina.
        #    codigo_ine distingue la ficha de un municipio de un articulo.
        if exige_reglas(fm):
            if not declara_reglas(ruta.read_text(encoding="utf-8")):
                sin_reglas.append(
                    f"{rel}: verificada pero no declara etiquetas_permitidas ni zonas")

    # 5. Notas internas publicadas. Se recorre aparte porque esto no mira el
    #    front matter sino el cuerpo, y afecta a cualquier pagina que se
    #    publique, tenga estado_dato o no.
    con_marcadores = [
        f"{rel}: {', '.join(marcas)}"
        for rel, texto in paginas_publicadas()
        if (marcas := marcadores_sin_resolver(texto))
    ]

    print(f"Fichas con estado_dato revisadas: {revisadas}\n")

    problemas = 0
    for titulo, lista in (
        ("INCOHERENCIAS estado_dato / draft", incoherentes),
        ("NOTAS INTERNAS PUBLICADAS", con_marcadores),
        ("TRAZABILIDAD INCOMPLETA", sin_trazabilidad),
        ("VERIFICADAS PERO SIN REGLAS", sin_reglas),
        (f"PENDIENTES DE REVISAR (mas de {args.meses} meses)", caducadas),
    ):
        if lista:
            problemas += len(lista)
            print(f"{titulo} ({len(lista)}):")
            for x in lista:
                print(f"  - {x}")
            print()

    if args.enlaces and fuentes:
        print(f"Comprobando {len(fuentes)} fuentes oficiales...")
        rotos = enlaces_rotos(fuentes)
        if rotos:
            problemas += len(rotos)
            print(f"FUENTES QUE NO RESPONDEN ({len(rotos)}):")
            for x in rotos:
                print(f"  - {x}")
            print()
        else:
            print("Todas responden.")
            print()

    if problemas == 0:
        print("Sin incidencias.")
        return 0

    print(f"Total de incidencias: {problemas}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
