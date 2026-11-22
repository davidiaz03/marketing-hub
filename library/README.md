# Biblioteca general de ganchos y formatos

Patrones generales de contenido corto, reutilizables en cualquier proyecto.
**No es la versión del Memorial**: esa vive en
`preprod/FORMATOS.md` (con sus reglas propias, vetos y contexto). Esta
biblioteca generaliza los patrones y deja fuera lo específico del Memorial.

## Contenido

- `ganchos.md` — 12 tipos de gancho (G1–G12) + 3 principios + qué evitar.
- `formatos.md` — 11 formatos (F1–F11) + duración + qué no funciona.

## Convención de evidencia

- `[VERIFICADO]` — se vio directamente en el video.
- `[SEGÚN FUENTE]` — viene de un estudio consultado (EditorOP oct-2026,
  Scrptly 8-nov-2026, Hook Studio, Viralkey).
- Un ejemplo sin URL y fecha no entra; una cifra sin fuente no se usa para
  decidir. Misma regla que en `preprod/FORMATOS.md`.

## Cómo se alimenta del escáner de outliers

La biblioteca se actualiza desde los informes del escáner de preprod, sin
duplicarlos:

1. Correr el escáner (procedimiento en `preprod/README.md`):
   `python3 scripts/preprod/outliers.py scan --platform all --max 30`
   desde `~/workspace/remotion-hub/repo/`.
2. Leer los informes en `preprod/research/` (`outliers-`,
   `outliers-instagram-` y `outliers-facebook-YYYY-MM-DD.md`).
3. Ver los 2–3 outliers principales de la semana y transcribir su gancho:
   ¿qué tipo de los 12 es? ¿O es un tipo nuevo?
4. Si aparece un patrón nuevo con URL y fecha, añadirlo aquí como nuevo
   tipo (G13, F12…) con su ejemplo. Si un principio deja de cumplirse en
   los ganadores, marcarlo «en revisión», no borrarlo.
5. Registrar el escaneo como entrada fechada en `preprod/research/`
   (ahí vive el registro de tendencias, no aquí).

Señales por plataforma (importa al leer los informes): vistas en YouTube,
likes en Instagram (el conector no expone vistas de publicaciones ajenas) y
reacciones en Facebook (por lista de URLs: el conector no lista las
publicaciones de una Página). Un múltiplo de Instagram no es comparable
directo con uno de YouTube: son señales distintas.

## Investigación base

21-nov-2026: 15 videos hispanos analizados fotograma a fotograma
(`preprod/research/tendencias-2026-11-21.md`) + estudios EditorOP y
Scrptly. Los ejemplos de esta biblioteca son los de esa investigación,
generalizados: el patrón es lo que se reutiliza, no el tema.
