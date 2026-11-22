#!/usr/bin/env python3
"""Sincroniza la última medición de preprod con el ecosistema de marketing.

Lee el informe JSON más reciente de `measure.py`
(`preprod/research/medicion-*.json`, solo lectura) y regenera el resumen
`experiments/medicion-ultima.md` a partir de sus cifras. Los números salen
del JSON por programa, nunca copiados a mano.

El resumen es una referencia, no una copia: el informe completo sigue
viviendo en `preprod/research/` (JSON + Markdown) y el resumen lo cita
por ruta y fecha. El archivo generado NO es un experimento: no entra en
`experiments/index.json` y `validate.py` lo excluye del chequeo de
coincidencia índice↔archivos.

Uso:
    python3 scripts/sync_medicion.py
    python3 scripts/sync_medicion.py --informe <ruta-a-medicion-AAAA-MM-DD.json>
    python3 scripts/sync_medicion.py --research-dir <dir> --salida <ruta>

Exit 0 = resumen actualizado. Exit 2 = no hay informe, el JSON es
inválido o le falta estructura (mensaje claro por stderr, sin traza).

Solo stdlib. No toca nada bajo `~/workspace/remotion-hub/repo/`.
"""

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESEARCH_DIR = Path.home() / "workspace" / "remotion-hub" / "repo" / \
    "preprod" / "research"
SALIDA_DEFECTO = REPO / "experiments" / "medicion-ultima.md"
FUENTE_RELATIVA = "~/workspace/remotion-hub/repo/preprod/research"


class SyncError(Exception):
    """Error esperado de la sincronización (mensaje claro, sin traza)."""


def fmt_num(valor):
    """Número en formato español: coma decimal, sin ceros sobrantes.

    60.0 -> "60"; 14.5 -> "14,5"; 10.09 -> "10,09"; 222 -> "222".
    None -> "s/d".
    """
    if valor is None:
        return "s/d"
    if isinstance(valor, bool):
        return "s/d"
    if isinstance(valor, int):
        return str(valor)
    if isinstance(valor, float):
        texto = f"{valor:.2f}".rstrip("0").rstrip(".")
        return texto.replace(".", ",")
    return str(valor)


def encontrar_ultimo_informe(research_dir):
    """El medicion-*.json más reciente por fecha del nombre. None si no hay."""
    informes = sorted(Path(research_dir).glob("medicion-*.json"))
    return informes[-1] if informes else None


def cargar_informe(path):
    """Lee y valida la estructura mínima del JSON de medición."""
    try:
        datos = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SyncError(f"no existe el informe: {path}")
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise SyncError(f"el informe no es un JSON válido: {path} ({exc})")
    if not isinstance(datos, dict):
        raise SyncError(f"el informe no es un objeto JSON: {path}")
    for clave in ("fecha", "perfil", "plataformas"):
        if clave not in datos:
            raise SyncError(
                f"al informe le falta la clave '{clave}': {path}")
    if not isinstance(datos["plataformas"], list):
        raise SyncError(f"'plataformas' debe ser una lista: {path}")
    for plat in datos["plataformas"]:
        for clave in ("plataforma", "senial", "n_ventana", "n_base",
                      "mediana", "top", "bottom"):
            if clave not in plat:
                raise SyncError(
                    f"a una plataforma le falta la clave '{clave}': {path}")
    return datos


def _linea_post(post, unidad):
    """Una línea de top/bottom con enlace, señal y multiplicadores."""
    titulo = post.get("titulo", "sin título")
    url = post.get("url", "")
    partes = [f"[{titulo}]({url})",
              f"{fmt_num(post.get('senial'))} {unidad}",
              f"{fmt_num(post.get('multiplicador'))}x"]
    if post.get("multiplicador_tipo") is not None:
        partes.append(f"{fmt_num(post.get('multiplicador_tipo'))}x su tipo")
    if post.get("publicado"):
        partes.append(str(post["publicado"]))
    if post.get("tipo"):
        partes.append(str(post["tipo"]))
    if post.get("comentarios") is not None:
        n_com = post["comentarios"]
        partes.append(f"{n_com} comentario"
                      f"{'' if n_com == 1 else 's'}")
    linea = " — ".join(partes)
    clasificacion = post.get("clasificacion")
    if clasificacion == "destacado":
        linea += " · **DESTACADO**"
    elif clasificacion == "flojo":
        linea += " · **FLOJO**"
    return f"- {linea}"


def _seccion_plataforma(plat):
    """Sección Markdown de una plataforma."""
    nombre = plat["plataforma"]
    unidad = plat["senial"]
    lineas = [f"## {nombre}", ""]
    seguidores = plat.get("seguidores")
    lineas.append(
        f"Señal: {unidad} · Seguidores: "
        f"{fmt_num(seguidores) if seguidores is not None else 's/d'} · "
        f"Semana: {plat['n_ventana']} publicaciones · "
        f"Base de mediana: {plat['n_base']} · "
        f"Mediana: {fmt_num(plat['mediana'])} {unidad}")
    medianas_tipo = plat.get("medianas_tipo") or {}
    if medianas_tipo:
        detalles = []
        for tipo in ("reel", "carrusel", "foto", "post"):
            dato = medianas_tipo.get(tipo)
            if dato:
                detalles.append(
                    f"{tipo}: {fmt_num(dato.get('mediana'))} {unidad} "
                    f"(n={dato.get('n')})")
        for tipo, dato in sorted(medianas_tipo.items()):
            if tipo not in ("reel", "carrusel", "foto", "post"):
                detalles.append(
                    f"{tipo}: {fmt_num(dato.get('mediana'))} {unidad} "
                    f"(n={dato.get('n')})")
        lineas.append(f"Medianas por tipo: {'; '.join(detalles)}.")
    lineas.append("")
    lineas.append("### Top 3 de la semana")
    lineas.append("")
    if plat["top"]:
        lineas += [_linea_post(p, unidad) for p in plat["top"]]
    else:
        lineas.append("Sin publicaciones con señal en la ventana.")
    lineas.append("")
    lineas.append("### Bottom 3 de la semana")
    lineas.append("")
    if plat["bottom"]:
        lineas += [_linea_post(p, unidad) for p in plat["bottom"]]
    else:
        lineas.append("Sin publicaciones con señal en la ventana.")
    lineas.append("")
    return lineas


def render_resumen(datos, origen):
    """El contenido completo de medicion-ultima.md desde el JSON."""
    fecha = datos["fecha"]
    perfil = datos["perfil"]
    ventana = datos.get("ventana") or {}
    desde = ventana.get("desde", "s/d")
    hasta = ventana.get("hasta", "s/d")
    nombre_json = Path(origen).name
    nombre_md = nombre_json.replace(".json", ".md")

    lineas = [
        f"# Última medición sincronizada — {perfil} — {fecha}",
        "",
        "> Generado por `scripts/sync_medicion.py` — NO editar a mano. Se",
        "> regenera en cada sincronización desde el informe de `measure.py`.",
        ">",
        f"> Fuente: `{FUENTE_RELATIVA}/{nombre_json}` (informe completo en",
        f"> `{FUENTE_RELATIVA}/{nombre_md}`, mismo directorio).",
        ">",
        f"> Ventana: {desde} → {hasta} (últimos 7 días). Mediana por",
        "> plataforma sobre publicaciones de más de 7 días; destacado ≥3x,",
        "> flojo ≤0,5x.",
        "",
    ]
    for plat in datos["plataformas"]:
        lineas += _seccion_plataforma(plat)

    lineas.append("## Hallazgos")
    lineas.append("")
    hallazgos = datos.get("hallazgos") or []
    if hallazgos:
        for i, hallazgo in enumerate(hallazgos, 1):
            lineas.append(f"{i}. **{hallazgo.get('texto', '')}**")
            if hallazgo.get("evidencia"):
                lineas.append(f"   Evidencia: {hallazgo['evidencia']}")
    else:
        lineas.append("Sin hallazgos en esta corrida.")
    lineas.append("")

    lineas.append("## Bloqueos de la corrida")
    lineas.append("")
    bloqueos = datos.get("bloqueos") or []
    if bloqueos:
        for bloqueo in bloqueos:
            lineas.append(
                f"- **{bloqueo.get('plataforma', '')}** "
                f"({bloqueo.get('via', '')}): {bloqueo.get('error', '')} "
                f"Qué falta: {bloqueo.get('que_falta', '')}")
    else:
        lineas.append("Sin bloqueos en esta corrida.")
    lineas.append("")

    lineas.append("## Cómo usar este resumen")
    lineas.append("")
    lineas.append("Este archivo es la referencia rápida de la última medición "
                  "para experimentos, campañas y KPIs: los números de aquí "
                  "salen del JSON por programa. Para el detalle completo "
                  "(ventana entera, fallos parciales), leer el informe "
                  "original en `preprod/research/`.")
    lineas.append("")
    return "\n".join(lineas)


def sincronizar(research_dir=RESEARCH_DIR, salida=SALIDA_DEFECTO,
                informe=None):
    """Ejecuta la sincronización. Devuelve (informe_usado, salida).

    Lanza SyncError con un mensaje claro si no hay informe o es inválido.
    """
    if informe is not None:
        origen = Path(informe)
        if not origen.is_file():
            raise SyncError(f"no existe el informe: {origen}")
    else:
        origen = encontrar_ultimo_informe(research_dir)
        if origen is None:
            raise SyncError(
                "no se encontró ningún informe de medición "
                f"(medicion-*.json) en {research_dir}. "
                "Corre primero measure.py (el cron de los lunes ya lo "
                "hace) o pasa --informe con la ruta del JSON.")
    datos = cargar_informe(origen)
    texto = render_resumen(datos, origen)
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(texto, encoding="utf-8")
    return origen, salida


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Sincroniza la última medición de preprod con "
                    "experiments/medicion-ultima.md.")
    parser.add_argument("--informe",
                        help="ruta a un medicion-AAAA-MM-DD.json concreto")
    parser.add_argument("--research-dir", default=str(RESEARCH_DIR),
                        help="directorio con los informes de measure.py")
    parser.add_argument("--salida", default=str(SALIDA_DEFECTO),
                        help="ruta del resumen a generar")
    parser.add_argument("--quiet", action="store_true",
                        help="sin salida por pantalla")
    args = parser.parse_args(argv)
    try:
        origen, salida = sincronizar(
            research_dir=args.research_dir, salida=args.salida,
            informe=args.informe)
    except SyncError as exc:
        print(f"sync-medicion: error: {exc}", file=sys.stderr)
        return 2
    if not args.quiet:
        print(f"sync-medicion: OK — {origen.name} → "
              f"{salida.relative_to(REPO) if salida.is_relative_to(REPO) else salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
