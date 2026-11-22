# Plantilla de calendario semanal de contenido

Un archivo por semana y perfil: `calendar/<fecha-lunes>-<perfil>.md`.
La semana empieza el lunes. Una fila por pieza; si un día no tiene pieza,
no se inventa una.

## Semana del [lunes, fecha] — Perfil [id]

| Día | Canal | Pieza | Formato | Gancho | Estado |
|---|---|---|---|---|---|
| Lun | | | | | |
| Mar | | | | | |
| Mié | | | | | |
| Jue | | | | | |
| Vie | | | | | |
| Sáb | | | | | |
| Dom | | | | | |

## Columnas

- **Día:** Lun–Dom.
- **Canal:** desde el perfil (`profiles/<id>.json`). Nada en un canal con
  estado `inactivo` o `restringido` sin decisión explícita.
- **Pieza:** título corto + enlace al pack (`campaigns/…`) o a la propuesta
  (`preprod/propuestas/…`) cuando exista.
- **Formato:** código de `library/formatos.md` (F1–F11).
- **Gancho:** código de `library/ganchos.md` (G1–G12).
- **Estado:** `idea`, `borrador`, `en_produccion`, `listo`,
  `pendiente_aprobacion`, `publicado`.

## De dónde salen las piezas

- **Preprod diario** (`preprod-daily`, 07:50): la shortlist de la mañana
  es la fuente principal de ideas para el Memorial.
- **Escaneo semanal de tendencias** (lunes 09:00): outliers y breakouts
  de la semana anterior.
- **Archivo propio:** material ya producido pendiente de publicar.
- **Campañas:** los packs de `campaigns/` fijan sus propias fechas.

## Reglas

- Ninguna pieza entra al calendario sin formato ni gancho asignados: una
  fila sin F ni G es una idea, no un plan.
- Las fechas dependen de las aprobaciones: una pieza `pendiente_aprobacion`
  no tiene fecha de publicación, tiene fecha de revisión.
- Al cerrar la semana, anotar qué se publicó, qué se movió y por qué (dos
  líneas al final del archivo).
