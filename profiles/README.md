# Perfiles de proyecto — esquema

Un perfil es la ficha de identidad de un proyecto dentro del ecosistema de
marketing y comunicación. El Memorial es UN perfil más; el núcleo es general.

## Formato

JSON, un archivo por proyecto: `profiles/<id>.json`. JSON (y no Markdown)
porque el perfil lo leen tanto el agente como los scripts de validación.

## Esquema (v1)

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `id` | string | sí | Identificador corto, minúsculas, sin espacios (`memorial`, `personal`). Coincide con el nombre del archivo. |
| `nombre` | string | sí | Nombre legible del proyecto. |
| `tipo` | string | sí | `institucional`, `personal` o `comercial`. |
| `version` | string | sí | Versión del perfil (`1.0`, `1.1`…). |
| `actualizado` | string | sí | Fecha ISO de la última revisión (`2026-11-21`). |
| `identidad` | objeto | sí | `nombre`, `descripcion`, `ambito`. Qué es el proyecto y qué hace. |
| `publico` | objeto | sí | `descripcion`, `segmentos` (lista), `notas`. A quién se dirige. |
| `pilares_mensaje` | lista de objetos | sí | Cada uno: `pilar`, `descripcion`. Mínimo 1 entrada. |
| `tono` | objeto | sí | `voz` (string) y `reglas` (lista de strings). Cómo suena el proyecto. |
| `canales` | lista de objetos | sí | Cada uno: `canal`, `cuenta`, `estado`, `notas`. |
| `objetivos` | lista de objetos | sí | Cada uno: `objetivo`, `kpi`, `estado`. |
| `restricciones` | lista de objetos | sí | Cada uno: `restriccion`, `fuente`. Líneas rojas con su fuente. |
| `flujo_aprobacion` | lista de strings | sí | Pasos, en orden, antes de publicar. |
| `fuentes` | lista de strings | sí | Rutas de los documentos de donde sale cada hecho del perfil. |

## Estados de canal

- `activo` — se publica ahí hoy.
- `inactivo` — existe la cuenta pero no se usa (con el motivo en `notas`).
- `restringido` — existe pero con un veto o límite vigente (en `notas`).
- `por_definir` — no se ha decidido si se usará.

## Convención «por definir»

Lo que no se sabe queda literalmente como `"por definir"`, nunca inventado.
Un perfil con «por definir» es un perfil válido: la validación exige
estructura, no respuestas. El campo `notas` puede listar lo que falta
decidir y de dónde saldrá la respuesta.

## Referencias, no copias

El perfil del Memorial NO copia `SULERIS.md` ni `NARRATIVA.md`: los
referencia por ruta en `fuentes` y en las `restricciones`. Si esos
documentos cambian, el perfil sigue siendo válido porque apunta a ellos.

## Validación

```bash
python3 scripts/validate.py
```

Comprueba que cada perfil cumple este esquema (campos obligatorios, tipos,
estados de canal válidos, `id` igual al nombre del archivo).
