# Comparación: apuntes de papel vs. LaTeX vs. AF_1 (slides)

Written for: el propio estudiante, para revisar qué falta en `SeriesFourier.tex`.
No se ha modificado ningún archivo `.tex`.

## 1. Apuntes de papel, ordenados por día

Las fotos de 15/10 (24 JPG en la raíz de `apuntespapel/`) recogen páginas de varios días; la fecha que manda es la escrita en la página, no la del archivo. La carpeta `15-10-26/` está vacía. La carpeta `8-10-26/` contiene las 3 fotos de WhatsApp (enviadas el 8/10) con la cabecera "06/10/2026".

| Día (cabecera de la página) | Fuente | Contenido |
|---|---|---|
| ¿10/09/2026? (ilegible) | `PXL_…191207120` | Previos, series de Fourier, idea de coeficientes $a_n,b_n$ (Euler, D'Alembert, Bernoulli), plan del curso |
| Sin fecha (inicio) | `PXL_…191225230` | Series de Fourier, periodicidad, convergencia |
| 22/09/26 | `PXL_…191237587`, `PXL_…191249027` | $L_p(\mathbb T)$, Hölder, inclusiones $L_q\subset L_p$, densidad de $C(\mathbb T)$ en $L_1$ |
| 24/09/26 | `PXL_…191349048` | Ejemplo $f(t)=t^2$ (coeficientes complejos y reales) |
| 30/09/26 | `PXL_…191337271` (y relacionadas) | Convolución en $L_1$, exponenciales complejas, $\rho_\varepsilon$, coeficientes de $f*g$ |
| 01/10/26 | `PXL_…191500278`, `PXL_…191503452`, `PXL_…191515705` | Núcleo de Dirichlet, Teorema 1.9 (Banach–Steinhaus) y observación sobre $L_1$ |
| 01/10/26 (cont.) | `PXL_…191529435`, `PXL_…191536494` | Cotas de $\|D_N\|_1\sim\log N$ con sumas armónicas |
| "Del día anterior" (1/10) | `PXL_…191607820` | Suma armónica $\sum 1/k\sim\log M$ (cotas por integral) |
| 06/10/26 | `8-10-26/` (3 fotos, págs. 18–20) | Lema 1.11 (Riemann–Lebesgue), Teorema 1.12 (localización de Riemann), Test de Dini (1.13), Corolario 1.14 |
| Sin fecha (¿15/10?) | `PXL_…191433215`, `PXL_…191545987`, `PXL_…191554458`, `PXL_…191619060` | Cesàro, núcleo de Fejér $F_N$ y su positividad, sumabilidad, ejercicios de Cesàro ($\sum(-1)^n$, $1,-1,1,\dots$) |

Nota de confianza: las páginas están fotografiadas giradas y varias tienen cabeceras pequeñas o ilegibles. La asignación de fotos a días es **aproximada**; las fechas de 22/09, 24/09, 06/10 y 01/10 sí se leen con claridad, el resto no.

## 2. Papel vs. LaTeX (`SeriesFourier.tex`)

### Cubierto en ambos
- 22/09: $L_p$, Hölder, inclusiones y densidad.
- 24/09: ejemplo $t^2$ (complejo y real).
- 30/09: convolución en $L_1$, exponenciales, $\rho_\varepsilon$, Prop. de coeficientes de convolución.
- 01/10: núcleo de Dirichlet y Banach–Steinhaus (Teorema 1.9 en el LaTeX).
- 06/10: Riemann–Lebesgue, localización de Riemann, Dini, Corolario 1.14.

### Falta en el LaTeX (está en el papel)
1. **Cesàro y Fejér**: definición de convergencia de Cesàro, $\sigma_N$, núcleo de Fejér $F_N$, su positividad, la proposición 1.18 y el teorema de Fejér. Está en el papel del día de hoy y no aparece en ningún `.tex`.
2. **Núcleos de sumabilidad**: la definición $(K_\varepsilon)$ y sus propiedades (masa 1, $\sup\|K_\varepsilon\|_1<\infty$, $\int_{|t|>\delta}|K_\varepsilon|\to 0$).
3. **Cotas de $\|D_N\|_1\sim\log N$ con sumas armónicas**: el papel tiene la cota de $\sum 1/k$ por integral como lema previo; el LaTeX sólo tiene el paso final dentro de la demostración.
4. **Lema del "Caso 1" con cota $2/\alpha$ y observación sobre $\sin$ creciente**: está en el papel de 06/10 pero el LaTeX sólo lo recoge en parte.
5. **Ejercicios**: Cesàro de $\sum(-1)^n$ y de la sucesión $1,-1,1,\dots$; varias páginas del 15/10 tienen dibujos de funciones a trozos y ejercicios de coeficientes que no he podido leer con seguridad, así que no los incluyo aquí.

### Falta en el papel (está en el LaTeX)
- Observación sobre la unidad del álgebra de convolución: se menciona en el papel de 30/09 pero sin la demostración del LaTeX.
- Algunas observaciones teóricas largas (jerarquía $\mathcal P\subset C\subset L_1$, notación asintótica): el papel no las copia.

## 3. AF_1 (slides de Pablo Sevilla) vs. LaTeX

AF_1 es un documento de **teoría en diapositivas, no una lista de enunciados ni ejercicios**. Su contenido se compara con el orden de la LaTeX:

| Bloque | AF_1 (págs.) | LaTeX | Diferencia |
|---|---|---|---|
| Introducción, coeficientes reales/complejos | 2–9 | Sí | Orden casi igual |
| Previos: $C(\mathbb T)$, polinomios trig., Stone–Weierstrass, $L_p$ | 5–10 | Sí | AF_1 da Stone–Weierstrass como teorema; LaTeX no lo enuncia |
| Lema 1.3, Prop. 1.4 (propiedades de coeficientes) | 12–13 | Sí, pero **desplazada** | En el LaTeX la Prop. 1.4 aparece después de los ejemplos de $t^2$ y de la discusión de convergencia; en AF_1 va justo tras la definición |
| Preguntas de convergencia (precisas) | 13–14 | Parcial | Sin la lista numerada de preguntas |
| Convolución: definición, Prop. 1.5, **Prop. 1.6 (álgebra de Banach)** | 17–19 | Parcial | **Falta la Prop. 1.6** (conmutatividad, distributividad, $\|f*g\|_1\le\|f\|_1\|g\|_1$ como proposición) |
| Prop. 1.7 (coeficientes de convolución) | 15 | Sí | — |
| Núcleo de Dirichlet, Prop. 1.8 | 20–33 | Sí | Igual en contenido |
| "Recordemos las preguntas", "Resultados negativos" (Thm 1.9, Banach–Steinhaus) | 34–40 | Sí, sin nombre | El LaTeX deja el enunciado con título vacío `\begin{teorema}{}` |
| Du Bois-Reymond | 38–40 | Sí | **Año distinto: AF_1 dice 1876, el LaTeX dice 1873** |
| Resultados positivos: Lema 1.11, Thm 1.12, Dini 1.13, Cor. 1.14 | 41–46 | Sí | Igual en contenido |
| **Otros resultados positivos (condición de Hölder $\alpha$)** | 46 | **No** | Falta |
| **Cesàro y Fejér (Prop. 1.18, núcleo de Fejér)** | 47–69 | **No** | Falta el bloque completo |
| **Núcleos de sumabilidad** | 70 | **No** | Falta |

## 4. Errores y textos sueltos en el LaTeX (sólo señalados, no corregidos)

- Línea 628: "Creo, no lo he copiado" dentro de la Prop. 1.4 (3).
- Línea 656: "valdría con N?" y "(Nota: asumiendo max(M,N)…)" dentro de la demostración de la Prop. 1.4 (2).
- Líneas 711 y 725: **"Hobson-Tonelli"**; el nombre correcto es **Tonelli**.
- Línea 786: `\cref{prop:fourier_conv}` apunta a una etiqueta que no comprueba la compilación (revisar que exista).
- Títulos vacíos: `\begin{teorema}{}`, `\begin{observacion}{}{}`, `\begin{proposicion}{}{}` en Thm 1.9, Lema 1.11 y Thm 1.12 (los cuatro últimos).
- Formatos de fecha mezclados: "22/09/26", "30/09/2026", "1/10/26", "06/10/2026".
- Línea 618: "Du Bois Reymond ejemplo (1873)" vs. AF_1 "1876".
- Línea 1166: el Lema 1.11 se enuncia con $f\in L_1(I)$ pero en la demostración se usa $L_1(\mathbb T)$.
- El "Ejercicio sobre periodicidad de integrales" (línea 818) no tiene solución en el texto.

## 5. Resumen de lo que falta por añadir al LaTeX

1. Bloque de Cesàro y Fejér (defs., $F_N$, Prop. 1.18, teorema de Fejér).
2. Núcleos de sumabilidad.
3. Prop. 1.6 (propiedades algebraicas de la convolución en $L_1$).
4. Condición de Hölder $\alpha$ (resultado positivo).
5. Cambiar 1873 → 1876 (o confirmar la fecha en la bibliografía).
6. Corregir "Hobson-Tonelli" → "Tonelli".
7. Nombres de los teoremas de los títulos vacíos.
8. Mover la Prop. 1.4 a su posición de AF_1 si se quiere seguir el orden de la teoría.
9. Mover las fotos de la raíz de `apuntespapel/` a `apuntespapel/15-10-26/` (la carpeta está vacía).
