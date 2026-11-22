#!/usr/bin/env python3
"""Validador del ecosistema de marketing y comunicación.

Comprueba, sin red y sin dependencias:
  - profiles/*.json cumplen el esquema (profiles/README.md).
  - experiments/index.json coincide con los archivos de experiments/.
  - Las plantillas y los packs de campaña tienen todas las secciones.
  - La biblioteca tiene sus 12 ganchos y 11 formatos.
  - Ningún archivo de contenido lleva secretos (teléfonos, tokens, correos).

Uso:
    python3 scripts/validate.py            # valida todo el repo
    python3 scripts/validate.py --quiet    # solo el código de salida

Exit 0 = todo válido. Exit 1 = hay errores (los lista por pantalla).
"""

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

PROFILE_REQUIRED = [
    "id", "nombre", "tipo", "version", "actualizado", "identidad",
    "publico", "pilares_mensaje", "tono", "canales", "objetivos",
    "restricciones", "flujo_aprobacion", "fuentes",
]
TIPOS_PERFIL = {"institucional", "personal", "comercial"}
ESTADOS_CANAL = {"activo", "inactivo", "restringido", "por_definir"}
FECHA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CAMPAIGN_SECTIONS = [
    "Objetivo", "Público", "Piezas", "Calendario",
    "Adaptaciones por plataforma", "CTAs", "Medición", "Aprobación",
    "Estado",
]
STRATEGY_SECTIONS = [
    "Posicionamiento", "Público", "Pilares de mensaje", "Plan de canales",
    "Calendario y ritmo", "KPIs", "Restricciones", "Revisión",
]
CALENDAR_HEADER = "| Día | Canal | Pieza | Formato | Gancho | Estado |"

CONTENT_DIRS = ["profiles", "strategy", "library", "campaigns",
                "experiments", "calendar"]
SECRET_PATTERNS = [
    (re.compile(r"\+53\s*\d"), "posible teléfono cubano"),
    (re.compile(r"gho_[A-Za-z0-9]+"), "posible token de GitHub"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
     "posible correo electrónico"),
    (re.compile(r"drive\.google\.com|docs\.google\.com"),
     "enlace de Google Drive/Docs (IDs internos fuera del repo)"),
]


def _display(path):
    """Ruta legible: relativa al repo si está dentro, si no el nombre."""
    try:
        return str(path.relative_to(REPO))
    except ValueError:
        return path.name


def _err(errors, where, msg):
    errors.append(f"{where}: {msg}")


def _non_empty_str(errors, where, value, field):
    if not isinstance(value, str) or not value.strip():
        _err(errors, where, f"el campo '{field}' debe ser un string no vacío")


def validate_profile(path):
    """Valida un profiles/<id>.json contra el esquema. Devuelve errores."""
    errors = []
    where = _display(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [f"{where}: JSON inválido ({exc})"]
    if not isinstance(data, dict):
        return [f"{where}: el perfil debe ser un objeto JSON"]

    for key in PROFILE_REQUIRED:
        if key not in data:
            _err(errors, where, f"falta el campo obligatorio '{key}'")
    if errors:
        return errors

    if data["id"] != path.stem:
        _err(errors, where,
             f"el 'id' ({data['id']}) no coincide con el archivo ({path.stem})")
    if data["tipo"] not in TIPOS_PERFIL:
        _err(errors, where,
             f"'tipo' debe ser uno de {sorted(TIPOS_PERFIL)}")
    if not FECHA_RE.match(str(data.get("actualizado", ""))):
        _err(errors, where, "'actualizado' debe tener formato AAAA-MM-DD")

    ident = data["identidad"]
    if not isinstance(ident, dict):
        _err(errors, where, "'identidad' debe ser un objeto")
    else:
        for key in ("nombre", "descripcion", "ambito"):
            _non_empty_str(errors, where, ident.get(key), f"identidad.{key}")

    publ = data["publico"]
    if not isinstance(publ, dict):
        _err(errors, where, "'publico' debe ser un objeto")
    else:
        _non_empty_str(errors, where, publ.get("descripcion"),
                       "publico.descripcion")
        if not isinstance(publ.get("segmentos"), list):
            _err(errors, where, "'publico.segmentos' debe ser una lista")
        _non_empty_str(errors, where, publ.get("notas"), "publico.notas")

    for field, sub in (("pilares_mensaje", ("pilar", "descripcion")),
                       ("canales", ("canal", "cuenta", "estado", "notas")),
                       ("objetivos", ("objetivo", "kpi", "estado")),
                       ("restricciones", ("restriccion", "fuente"))):
        items = data[field]
        if not isinstance(items, list) or not items:
            _err(errors, where, f"'{field}' debe ser una lista no vacía")
            continue
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                _err(errors, where, f"'{field}[{i}]' debe ser un objeto")
                continue
            for key in sub:
                _non_empty_str(errors, where, item.get(key),
                               f"{field}[{i}].{key}")
        if field == "canales":
            for i, item in enumerate(items):
                if (isinstance(item, dict)
                        and item.get("estado") not in ESTADOS_CANAL):
                    _err(errors, where,
                         f"'canales[{i}].estado' debe ser uno de "
                         f"{sorted(ESTADOS_CANAL)}")

    tono = data["tono"]
    if not isinstance(tono, dict):
        _err(errors, where, "'tono' debe ser un objeto")
    else:
        _non_empty_str(errors, where, tono.get("voz"), "tono.voz")
        if (not isinstance(tono.get("reglas"), list)
                or not tono["reglas"]):
            _err(errors, where, "'tono.reglas' debe ser una lista no vacía")

    for field in ("flujo_aprobacion", "fuentes"):
        items = data[field]
        if (not isinstance(items, list) or not items
                or not all(isinstance(x, str) and x.strip() for x in items)):
            _err(errors, where,
                 f"'{field}' debe ser una lista no vacía de strings")
    return errors


def validate_experiments_index(root):
    """El índice y los archivos de experiments/ deben coincidir."""
    errors = []
    exp_dir = root / "experiments"
    index_path = exp_dir / "index.json"
    where = "experiments/index.json"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, FileNotFoundError) as exc:
        return [f"{where}: no se pudo leer ({exc})"]
    entries = index.get("experiments")
    if not isinstance(entries, list):
        return [f"{where}: falta la lista 'experiments'"]

    indexed = set()
    for i, entry in enumerate(entries):
        entry_where = f"{where}[{i}]"
        for key in ("id", "titulo", "tipo", "estado", "fecha", "perfil",
                    "archivo", "veredicto"):
            if key not in entry:
                _err(errors, entry_where, f"falta el campo '{key}'")
        if entry.get("tipo") not in ("observacional", "controlado"):
            _err(errors, entry_where,
                 "'tipo' debe ser 'observacional' o 'controlado'")
        if entry.get("estado") not in ("propuesto", "en_curso", "cerrado"):
            _err(errors, entry_where,
                 "'estado' debe ser 'propuesto', 'en_curso' o 'cerrado'")
        archivo = entry.get("archivo", "")
        indexed.add(archivo)
        if archivo and not (root / archivo).is_file():
            _err(errors, entry_where,
                 f"el archivo '{archivo}' no existe")

    on_disk = {str(p.relative_to(root)) for p in exp_dir.glob("*.md")
               if p.name != "README.md"}
    for missing in sorted(on_disk - indexed):
        _err(errors, where,
             f"el archivo '{missing}' no está en el índice")
    return errors


def headings_of(path):
    """Devuelve las secciones '## ' de un Markdown (sin numeración)."""
    heads = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            head = line[3:].strip()
            head = re.sub(r"^\d+\.\s*", "", head)
            heads.append(head)
    return heads


def validate_sections(path, required):
    """Comprueba que un Markdown tiene todas las secciones requeridas."""
    errors = []
    where = _display(path)
    heads = headings_of(path)
    for section in required:
        if section not in heads:
            _err(errors, where, f"falta la sección '## {section}'")
    return errors


def validate_library(root):
    """La biblioteca tiene sus 12 ganchos (G1-G12) y 11 formatos (F1-F11)."""
    errors = []
    ganchos = (root / "library" / "ganchos.md").read_text(encoding="utf-8")
    formatos = (root / "library" / "formatos.md").read_text(encoding="utf-8")
    for n in range(1, 13):
        if f"## G{n}." not in ganchos:
            _err(errors, "library/ganchos.md", f"falta el gancho G{n}")
    for n in range(1, 12):
        if f"## F{n}." not in formatos:
            _err(errors, "library/formatos.md", f"falta el formato F{n}")
    return errors


def scan_no_secrets(root):
    """Ningún archivo de contenido lleva teléfonos, tokens ni correos."""
    errors = []
    for dirname in CONTENT_DIRS:
        for path in sorted((root / dirname).rglob("*")):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for pattern, label in SECRET_PATTERNS:
                if pattern.search(text):
                    _err(errors, _display(path),
                         f"contenido sensible: {label}")
    return errors


def validate_all(root=REPO):
    """Valida todo el repo. Devuelve la lista de errores (vacía = OK)."""
    errors = []
    for path in sorted((root / "profiles").glob("*.json")):
        errors += validate_profile(path)
    errors += validate_experiments_index(root)
    errors += validate_sections(root / "campaigns" / "plantilla-campana.md",
                                CAMPAIGN_SECTIONS)
    for pack in sorted((root / "campaigns").glob("*/pack.md")):
        errors += validate_sections(pack, CAMPAIGN_SECTIONS)
    errors += validate_sections(
        root / "strategy" / "plantilla-estrategia.md", STRATEGY_SECTIONS)
    errors += validate_sections(
        root / "strategy" / "personal-estrategia.md", STRATEGY_SECTIONS)
    calendar_tpl = (root / "calendar" / "plantilla-semana.md"
                    ).read_text(encoding="utf-8")
    if CALENDAR_HEADER not in calendar_tpl:
        errors.append("calendar/plantilla-semana.md: falta la cabecera "
                      "de la tabla semanal")
    errors += validate_library(root)
    errors += scan_no_secrets(root)
    return errors


def main(argv):
    quiet = "--quiet" in argv
    errors = validate_all()
    if not quiet:
        if errors:
            print(f"VALIDACIÓN: {len(errors)} error(es)")
            for err in errors:
                print(f"  - {err}")
        else:
            print("VALIDACIÓN: OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
