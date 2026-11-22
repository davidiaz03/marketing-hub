# Plantilla de pack de campaña

Una carpeta por campaña: `campaigns/<fecha>-<slug>/pack.md`. La campaña
agrupa varias piezas con un objetivo común, un calendario y una medición
única. Sin objetivo medible no es campaña, es una lista de piezas.

## Objetivo

- **Objetivo** (una frase: qué se quiere conseguir):
- **Perfil** (`profiles/<id>.json`):
- **Éxito = ** (cómo se sabe que funcionó, con número o sin él; si no hay
  línea base, la meta queda `[POR DEFINIR]`):

## Público

- **A quién va dirigida** (desde el perfil; si el perfil dice «por
  definir», aquí también):

## Piezas

Tabla: pieza | formato (library/formatos.md) | canal | gancho
(library/ganchos.md) | estado.

| Pieza | Formato | Canal | Gancho | Estado |
|---|---|---|---|---|
| | | | | |

Estados: `idea`, `borrador`, `en_produccion`, `listo`, `publicado`.

## Calendario

Tabla: fecha | pieza | canal | estado. Sin fecha inventada: si la fecha
depende de una aprobación pendiente, se escribe «pendiente de aprobación».

| Fecha | Pieza | Canal | Estado |
|---|---|---|---|
| | | | |

## Adaptaciones por plataforma

Por pieza, qué cambia entre plataformas (duración, formato, texto, CTA).
Si una pieza es idéntica en todas partes, sobra la adaptación: se anota
«misma pieza en todas las plataformas».

## CTAs

- **CTA principal** (qué se le pide al espectador que HAGA):
- **CTA secundaria**:
- Regla: la CTA es contenido, no crecimiento. Ningún cierre con «sígueme»
  o «dale like» hablado (ver `library/formatos.md`, estructura en 5
  tiempos).

## Medición

- **Métricas** (qué se mide: reacciones, comentarios, compartidos, vistas,
  alcance — según lo que cada plataforma exponga):
- **Fuente** (informe de `measure.py` con fecha; referencia, no copia):
- **Línea base** (el número contra el que se compara, con su fuente):

## Aprobación

- **Quién aprueba** (perfil Memorial: Suleris Coss Diaz; perfil personal:
  el usuario):
- **Estado** (`pendiente`, `aprobada`, `con_cambios`):
- **Notas**:

## Estado

- **Estado de la campaña** (`plan`, `en_curso`, `cerrada`):
- **Cierre** (al cerrar: qué se consiguió, qué se aprendió, enlace al
  experimento en `experiments/` si lo hubo):
