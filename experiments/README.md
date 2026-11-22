# Registro de experimentos

Un archivo por experimento + un índice (`index.json`). El registro es la
memoria de lo que se probó, qué pasó y qué se aprendió. Sin registro, cada
decisión se toma de cero.

## Formato

- Un archivo por experimento: `experiments/<fecha>-<slug>.md`.
- Índice: `experiments/index.json` — una entrada por experimento, con
  `id`, `titulo`, `tipo`, `estado`, `fecha`, `perfil`, `archivo` y
  `veredicto` (una línea).
- El índice y los archivos deben coincidir: cada entrada del índice tiene
  su archivo y cada archivo de experimento está en el índice (excepto este
  README). Lo comprueba `scripts/validate.py`.

## Tipos

- `observacional` — comparación retrospectiva de cosas que ya pasaron, sin
  control. Da señales, no pruebas. Siempre con la sección de confusores.
- `controlado` — test diseñado: misma variable, dos variantes, métrica
  fijada antes de publicar. Es el único que puede decir «esto funciona
  mejor que aquello».

## Estados

- `propuesto` — diseñado, sin ejecutar.
- `en_curso` — publicado, esperando datos.
- `cerrado` — con resultado y veredicto.

## Estructura de cada experimento

1. **Contexto** (qué se sabía antes).
2. **Hipótesis** (qué se esperaba; en retrospectiva, qué hipótesis explican
   los datos).
3. **Diseño / comparación** (qué se comparó, con qué datos).
4. **Resultados** (números con fuente; referencia a los informes de
   `measure.py`, no copia).
5. **Confusores** (qué más podría explicar el resultado; obligatorio en
   observacionales).
6. **Veredicto** (qué se decide a partir de esto).
7. **Siguiente paso** (qué test seguiría, si lo hay).

## De dónde vienen los resultados

Los números de un experimento salen de los informes de medición de
preprod (`measure.py`, en `preprod/research/`), referenciados por ruta y
fecha. Nunca se copian los informes enteros aquí y nunca se anota un
número sin su fuente.

## El resumen sincronizado (`medicion-ultima.md`)

`experiments/medicion-ultima.md` es la referencia rápida de la última
medición: top/bottom de la semana, medianas y hallazgos, generados por
`scripts/sync_medicion.py` desde el JSON del informe más reciente. Los
números salen del JSON por programa, nunca copiados a mano, y el archivo
cita su informe fuente por ruta y fecha.

No es un experimento: no entra en `index.json` y el validador lo excluye
del chequeo índice↔archivos. No se edita a mano: se regenera corriendo
el sync tras cada medición semanal (el cron de los lunes ya corre
`measure.py`; no hace falta un cron nuevo).

## Regla

Un experimento sin veredicto no está cerrado. Un experimento cerrado sin
confusores (si es observacional) no es válido.
