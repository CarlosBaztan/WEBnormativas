"""
Auditoria de frescura y coherencia del contenido.

Comprueba tres cosas y devuelve codigo de salida 1 si encuentra algo:

  1. Fichas cuya `fecha_verificacion` tiene mas de 6 meses.
  2. Desincronizacion entre `estado_dato` y `draft`.
     La regla del proyecto es: estado_dato: pendiente  <=>  draft: true.
     Si se rompe, un dato sin verificar puede acabar publicado.
  3. Fichas marcadas como verificadas a las que les falta la trazabilidad
     (fuente_nombre, fuente_url o fecha_verificacion). El flag por si solo
     no basta para afirmar nada.

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


def main() -> int:
    ap = argparse.ArgumentParser(description="Audita frescura y coherencia de las fichas.")
    ap.add_argument("--meses", type=int, default=6, help="antiguedad maxima admitida (por defecto 6)")
    args = ap.parse_args()

    limite = date.today() - timedelta(days=args.meses * 30)

    caducadas: list[str] = []
    incoherentes: list[str] = []
    sin_trazabilidad: list[str] = []
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
        if estado == "pendiente" and not draft:
            incoherentes.append(f"{rel}: estado_dato=pendiente pero draft=false (SE PUBLICARIA)")
        elif estado == "verificado" and draft:
            incoherentes.append(f"{rel}: estado_dato=verificado pero draft=true (no se publica)")

        if estado != "verificado":
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

    print(f"Fichas con estado_dato revisadas: {revisadas}\n")

    problemas = 0
    for titulo, lista in (
        ("INCOHERENCIAS estado_dato / draft", incoherentes),
        ("TRAZABILIDAD INCOMPLETA", sin_trazabilidad),
        (f"PENDIENTES DE REVISAR (mas de {args.meses} meses)", caducadas),
    ):
        if lista:
            problemas += len(lista)
            print(f"{titulo} ({len(lista)}):")
            for x in lista:
                print(f"  - {x}")
            print()

    if problemas == 0:
        print("Sin incidencias.")
        return 0

    print(f"Total de incidencias: {problemas}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
