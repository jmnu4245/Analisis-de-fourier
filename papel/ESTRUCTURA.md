# Estructura de los apuntes

Fuentes: fotos de papel en `papel/AAAA-MM-DD/` (los escaneos de WhatsApp están en `v2/`), `material/AF_1_series_fourier_comp.pdf` (diapositivas, hasta la 50/50) y `papel/teorema_1_33.pdf`.

## Por día → sección del LaTeX (`teoria/SeriesFourier.tex`)

| Día | Fotos | Sección | Contenido |
|---|---|---|---|
| 10/09 | 2 PXL | 1.1–1.3 | Previos, historia, periódicas, coeficientes $a_n,b_n$ |
| 18/09 | 2 v2 (págs. 3–4) | 1.4–1.6 | Forma compleja ($n\le-1$), toro, $C(\mathbb T)$, polinomios trigonométricos, Stone–Weierstraß, Prop. 1.1 |
| 22/09 | 3 PXL | 1.6–1.7 | $L_p$, Hölder, Prop. 1.2, $\hat f(n)$, ejemplo signo |
| 24/09 | 3 PXL | 1.7–1.8 | Ejemplo $t^2$, Prop. 1.4, Prop. 1.5 |
| 30/09 | 4 PXL | 1.9–1.10 | Convolución en $L_1$, Prop. 1.7, Dirichlet (Prop. 1.8) |
| 01/10 | 3 PXL | 1.10 | $\|D_N\|_1\sim\log N$, Teorema 1.9 (Banach–Steinhaus) |
| 06/10 | 4 PXL + 3 v2 (págs. 18–20) | 1.11 | Weierstraß M, Lema 1.11, Teoremas 1.12 y 1.13 (Dini), Corolario 1.14 |
| 08/10 | 3 v2 | 1.11.1, 1.12 | Ejemplos de Dini, Cesàro, Prop. 1.17 |
| 15/10 | 4 PXL (hojas 0–6) | 1.12–1.14 | Repaso de Cesàro, $f_\delta$, $\sigma_N=f*F_N$, Fejér (1.18, 1.19), núcleos de sumabilidad, enunciado 1.20 |
| 20/10 | 3 v2 | 1.14–1.15 | Demostración 1.20, Teoremas 1.21–1.24, Teorema 1.30 (incompleto) |
| ¿22/10? | `teorema_1_33.pdf` | 1.16 | Notación del s.o.n., Teorema 1.33 con demostración |

Las fechas en negrita (`\textbf{dd/mm/aa}`) marcan en el LaTeX dónde empieza cada clase.

## Sacado solo de AF_1 (sin apuntes de clase)

Cada uno lleva una `nota` en el LaTeX que lo indica.

- 1.6: nota sobre Stone–Weierstraß (que $K$ sea compacto y el caso de $C([a,b])$).
- 1.14: Teorema 1.25, Corolarios 1.26 y 1.27, Teoremas 1.28 y 1.29.
- 1.15: Corolario 1.31 y teorema de convergencia en casi todo punto.
- 1.16: producto escalar en $L_2$, Prop. 1.32, pre-Hilbert/Hilbert, s.o.n.

## Lo que no cuadra

1. **Hueco entre el 10/09 y el 18/09.** El principio de la forma compleja (Euler, $n\ge1$) está en el LaTeX pero en ninguna foto. Faltan las págs. 1–2 del cuaderno escaneado. ¿Hubo clase el 15 o el 17/09?
2. **Hueco tras el 20/10.** La prueba del Teorema 1.30 queda en "continuará". `teorema_1_33.pdf` no tiene fecha. Falta el 22/10.
3. **13/10 sin apuntes.** El 15/10 repite Cesàro del 8/10. Probablemente no hubo clase.
4. **En AF_1 y nunca en clase:** Teorema 1.10 (no convergencia en $L_1$), Corolarios 1.15 y 1.16, condición de Hölder y variación acotada. Tampoco están en el LaTeX.
5. **Línea ilegible del 20/10:** "$\varepsilon_n\in\{1,-1\}\Rightarrow\sum\varepsilon_n/n^3\dots$ HR escrita". Está copiada literal.
6. **Cambios respecto al papel:**
   - $f_\delta=\frac1{2\delta}$ (en la foto pone "$-\frac12\delta$").
   - Cota $\eta/(2(1+M))$ en el Teorema 1.24 (en el papel, $\eta/2$ con interrogación).
   - Índice $k=1$ en $\sigma_N$ real (en el papel, $k=-N$).
7. **Erratas del LaTeX antiguo, sin corregir:**
   - "Hobson-Tonelli" (debería ser Tonelli).
   - Du Bois-Reymond 1873 (AF_1: 1876).
   - Notas al margen "Creo, no lo he copiado" y "valdría con N?".
8. **Orden distinto de AF_1:** la Prop. 1.4 va tras el ejemplo $t^2$; en AF_1, tras las definiciones.

