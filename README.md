# Marketing y comunicación — ecosistema general

Ecosistema general de marketing y comunicación, reutilizable en cualquier
proyecto. **El Memorial es UN perfil más**, no el sistema entero. El núcleo
(estrategia, biblioteca de ganchos/formatos, campañas, calendario,
experimentos) es general; cada proyecto aporta su perfil.

**Principio rector (orden del usuario, 21-nov-2026):** todos los
ecosistemas deben servir para otros proyectos, no solo para el Memorial.
El usuario los usará para crear contenido y probar cosas en redes en
proyectos personales. Lo general va en el núcleo; lo del Memorial es un
perfil más, no el sistema entero.

**Idioma:** español (es-419).

## Mapa del repo

```
marketing/
  profiles/    Perfiles de proyecto (JSON + esquema): memorial, personal.
  strategy/    Plantilla de estrategia + borrador de la estrategia personal.
  library/     Biblioteca general: 12 ganchos (G1-G12), 11 formatos (F1-F11).
  campaigns/   Plantilla de pack de campaña + ejemplo trabajado.
  experiments/ Registro de experimentos (un archivo por experimento + índice).
  calendar/    Plantilla de calendario semanal + semana de ejemplo.
  scripts/     validate.py — validador del repo (sin dependencias).
               sync_medicion.py — sincroniza la última medición de
               preprod a experiments/medicion-ultima.md.
  tests/       Suite (unittest, stdlib).
```

## Cómo se conectan las piezas

```
perfil (quiénes somos, a quién, con qué reglas)
   → estrategia (posicionamiento, pilares, canales, KPIs)
      → campaña (objetivo + piezas + calendario + medición)
         → calendario semanal (qué se publica cada día)
            → medición (measure.py) → experimento (qué se aprendió)
               → la biblioteca y la estrategia se actualizan
```

El escáner de outliers de preprod alimenta la biblioteca con patrones
nuevos (ver `library/README.md`). La medición de preprod alimenta los
experimentos con números reales (ver `experiments/README.md`).

## Motores de preprod que reutiliza (llamar, no duplicar)

| Motor | Ruta | Uso desde aquí |
|---|---|---|
| Escáner de outliers | `~/workspace/remotion-hub/repo/scripts/preprod/outliers.py` | `scan --platform all --max 30`; los informes en `preprod/research/` alimentan `library/` |
| Generador de propuestas | `~/workspace/remotion-hub/repo/scripts/preprod/propose.py` | `rank`/`daily` dan la shortlist de ideas del Memorial para el calendario |
| Medición | `~/workspace/remotion-hub/repo/scripts/preprod/measure.py` | **ACTIVA** (aterrizó 21-nov-2026, commit `50ac2f1`, rama `work/preprod-2026-11-21`). Sus informes en `preprod/research/` alimentan `experiments/` y los KPIs de `strategy/` vía `scripts/sync_medicion.py` (ver abajo) |

Ningún código de esos motores se copia aquí. Los informes se leen y se
referencian por ruta y fecha, nunca se duplican.

Documentos del Memorial que se referencian (no se copian):
`preprod/SULERIS.md` (9 vetos), `preprod/NARRATIVA.md` (30 reglas),
`preprod/FORMATOS.md` (versión específica del Memorial de la biblioteca),
`preprod/RANKING.md` (ranking del Memorial; su C2 no aplica a otros
perfiles).

## Sincronización de la medición

La medición de preprod (`measure.py`) ya existe y tiene informes reales
en `preprod/research/medicion-*.json`. La conexión con este ecosistema es
`scripts/sync_medicion.py`: lee el informe más reciente y regenera el
resumen `experiments/medicion-ultima.md` (top/bottom de la semana,
medianas y hallazgos) por referencia al informe original. Los números
salen del JSON por programa, nunca copiados a mano.

Procedimiento semanal:

```bash
cd ~/workspace/marketing
python3 scripts/sync_medicion.py   # tras cada medición semanal
```

No hace falta un cron nuevo: el cron `preprod-trends-weekly` (lunes
09:00, America/Puerto_Rico) ya corre `measure.py` junto al escáner de
outliers; el sync se corre después de esa corrida (o cuando se necesite
el resumen actualizado para un experimento, una campaña o los KPIs).
El resumen generado NO es un experimento: no entra en
`experiments/index.json` y el validador lo excluye de ese chequeo (ver
`experiments/README.md`).

## Cómo añadir un proyecto

1. Crear `profiles/<id>.json` siguiendo el esquema en `profiles/README.md`.
   Lo que no se sepa queda «por definir», nunca inventado.
2. Crear `strategy/<id>-estrategia.md` desde la plantilla.
3. Validar: `python3 scripts/validate.py`.
4. A partir de ahí: campañas, calendario y experimentos con ese perfil.

## Validación y pruebas

```bash
python3 scripts/validate.py              # valida todo el repo
python3 -m unittest discover -s tests -v # suite
```

El validador comprueba: esquema de perfiles, integridad del índice de
experimentos, secciones de plantillas y packs, 12 ganchos y 11 formatos
en la biblioteca, y ausencia de secretos en el contenido (teléfonos,
tokens, correos, enlaces de Drive).

## Skill del agente

`~/workspace/custom-skills/marketing_comms/SKILL.md` — flujos: nuevo
perfil, estrategia, campaña, experimento, planificación semanal y
actualización de la biblioteca.

## Reglas permanentes

- **Nunca se inventan hechos.** Lo desconocido queda «por definir».
- **Referencias, no copias.** Los documentos de preprod y sus informes se
  referencian por ruta y fecha.
- **Cada perfil publica en sus propios canales.**
- **Aprobación antes de publicar.** Memorial: Suleris Coss Diaz.
  Personal: el usuario. Este ecosistema planifica; no publica.
- **La medición manda sobre la intuición.** Un número sin fuente no se
  usa para decidir.

## Límites honestos

- El validador comprueba estructura, no verdad.
- La medición tiene límites propios (ver el informe de cada semana):
  Facebook se mide por vía de URLs porque el conector no descubre la
  Página, y los insights propios de Instagram necesitan reactivar la
  sesión de @memorialdenuncia (sin eso, solo likes públicos).
- El ranking de preprod es del Memorial: para otros perfiles, la
  selección de ideas es manual hasta que exista un ranking propio.
- La biblioteca nace de una investigación del 21-nov-2026 (15 videos +
  EditorOP/Scrptly): los patrones son evidencia de ese momento. El
  escaneo semanal es lo que los mantiene vivos.

## Verificado 21-nov-2026

Ecosistema construido y probado con la suite de `tests/` (en verde):
2 perfiles semilla, plantilla de estrategia + borrador personal,
biblioteca general (12 ganchos, 11 formatos), plantilla de campaña +
pack trabajado (lanzamiento del reel Martí-Fidel V6.1), registro de
experimentos con el retrospectivo presentadora-a-cámara, plantilla de
calendario + semana de ejemplo.

**21-nov-2026 (noche): integración con la medición activada.**
`scripts/sync_medicion.py` conecta los informes de `measure.py` con
`experiments/medicion-ultima.md`; primer informe real sincronizado
(21-nov: reel Pilar 222 likes, 10,09x la mediana; reels ~4x
fotos/carruseles en ambas plataformas). Validador + suite en verde.
