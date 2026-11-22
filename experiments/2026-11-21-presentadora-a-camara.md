# Experimento — Presentadora a cámara vs sin presentadora (retrospectivo)

**ID:** 2026-11-21-presentadora-a-camara · **Tipo:** observacional ·
**Estado:** cerrado · **Perfil:** Memorial · **Fecha:** 2026-11-21.

> **Este NO es un test controlado.** Es una comparación retrospectiva de
> reels ya publicados, sin diseño previo ni variables controladas. Da una
> señal fuerte, no una prueba.

## Contexto

La cuenta del Memorial tiene 2 reels virales de referencia y una serie de
reels con rendimiento bajo. La diferencia visible entre ambos grupos es la
presencia de presentadoras a cámara. Este experimento registra esa
comparación con sus números y sus límites.

## Hipótesis (retrospectiva)

Los reels con presentadoras a cámara en diálogo rinden mucho más que los
reels sin presentadora, porque la cara hace el trabajo de atención que el
montaje por sí solo no compensa.

## Comparación

| Grupo | Piezas | Reacciones | Vistas |
|---|---|---|---|
| Con presentadoras a cámara en diálogo (karaoke grande con palabra clave en rojo, overlays de evidencia, tema indignante) | 2 reels virales de referencia | 14K y 9,1K | 115K y 119K |
| Sin presentadora | Varios reels | 32–69 | por definir (no consta el dato de vistas) |

**Fuentes:** `~/MEMORY.md` («Trabajo — Memorial de la Denuncia», 16 sep
2026); `preprod/NARRATIVA.md` R30; `preprod/FORMATOS.md` («Contexto
propio»).

## Resultados

La brecha es de dos órdenes de magnitud: los reels con cara rinden entre
~130x y ~440x las reacciones de los reels sin presentadora (14.000/9.100
frente a 32–69). El dato de vistas de los reels sin presentadora no
consta: no se compara lo que no se tiene.

## Confusores

Todo lo siguiente podría explicar parte de la brecha, y ninguno está
controlado:

1. **Tema distinto:** los virales tenían tema indignante; no se sabe si
   los reels sin presentadora trataban temas de igual fuerza.
2. **Fecha distinta:** los virales y los de bajo rendimiento se publicaron
   en momentos distintos, con audiencias y algoritmos distintos.
3. **Muestra pequeña:** n=2 en el grupo con cara. Dos éxitos no son una
   ley.
4. **Calidad de producción:** los virales llevaban karaoke grande,
   overlays de evidencia y diálogo; los de bajo rendimiento podrían
   diferir en más de una variable a la vez.
5. **Sin línea base por fecha:** no hay mediana de la cuenta por periodo
   contra la que normalizar.

## Veredicto

Señal fuerte pero observacional. Decisión vigente: **la cara a cámara es
el formato por defecto cuando hay presentadora disponible**; sin cara, el
motion graphics y el dato tienen que hacer TODO el trabajo de atención
que antes hacía la presentadora (de ahí la exigencia de cambio visual
cada 2–3 s y de un gancho-cifra en el fotograma 0 — NARRATIVA.md R30).

Lo que este experimento NO dice: que un reel sin presentadora no pueda
rendir. Los referentes documentales sin cara (NOVA, MapSody, 60SecHistory)
rinden cuando el formato es documental con datos.

## Siguiente paso

Test controlado propuesto (aún no diseñado): mismo tema, dos versiones —
una con presentadora a cámara y otra documental faceless con el mismo
guion — publicadas en días comparables y medidas con `measure.py`. El
reel «Martí-Fidel: leer, pensar» (V6.1, sin presentadora, máxima
producción) es la primera prueba natural: si se acerca al rango de los
virales, la brecha se estrecha; si queda en 32–69, la señal se refuerza.
Ver la campaña en `campaigns/2026-11-21-lanzamiento-marti-fidel/pack.md`.
