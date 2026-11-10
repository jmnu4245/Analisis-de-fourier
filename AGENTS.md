# Guía para contribuir (personas y agentes)

Apuntes de Análisis de Fourier (curso 2026/27) en LaTeX, con versión web. Idioma: **español**.

## Estructura

| Ruta | Qué va ahí |
|---|---|
| `main.tex` | Documento principal: orden de las partes y `\input`s. |
| `preambulo.tex` | Paquetes, cajas (`teorema`, `definicion`, `proposicion`, `observacion`, `nota`, `ejemplo`) y macros. |
| `teoria/` | Contenido: `intro.tex` y un `.tex` por capítulo (`SeriesFourier`, `TransformadaFourier`, `EspaciosHardy`). |
| `papel/` | Fotos de los apuntes manuscritos en `aaaa-mm-dd/`, y `ESTRUCTURA.md` (qué día → qué sección, qué falta, qué no cuadra). |
| `web/` | Web (HTML + mapa de resultados). No tocar salvo que cambies la web. |
| `material/` | Local, **ignorado por git** (diapositivas del profesor, etc.). No subir. |

Los archivos generados (`*.aux`, `*.pdf`, `.web/`...) están en `.gitignore`: no se suben.

## Dónde meter cada cosa

- **Apuntes de una clase nueva**: en el `.tex` del capítulo, dentro de `teoria/`, empezando con la fecha en negrita `\textbf{dd/mm/aa}`. Las fotos van en `papel/aaaa-mm-dd/`, y se añade una fila en la tabla de `papel/ESTRUCTURA.md` (día, fotos, sección, contenido). Lo que no cuadre con las fotos se anota en ese mismo archivo.
- **Contenido sacado solo de las diapositivas** (sin apuntes de clase): lleva una `nota` en el LaTeX que lo indica y se lista en `ESTRUCTURA.md`.
- **Capítulo nuevo**: crea `teoria/Nombre.tex` (empieza con `\section{...}`), añade `\input{teoria/Nombre}` en `main.tex` y añade `("Nombre", n)` a `ARCHIVOS` en `web/mapa/generar.py` (y bloques/colores en `BLOQUES` si procede).

## Convenciones de los apuntes

- Resultados en cajas con etiqueta única: `\begin{teorema}{Título}{etiqueta}`. Referencias con `\cref{tipo:etiqueta}`; la web y el mapa de dependencias se construyen a partir de esas citas (una cita en un enunciado o demostración crea una arista).
- Rutas en `\input` relativas a la raíz (`teoria/...`), no al archivo.
- Nombres de archivo sin espacios ni tildes.

## Comprobar antes de subir

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -usepretex='\def\versionfinal{}' main.tex   # PDF
web/construir.sh   # web en .web/sitio/ (necesita make4ht); debe acabar con "0 sin enlace a los apuntes"
```

La CI (`.github/workflows/`) compila el PDF, publica un *release* y la web en cada push a `main`.

## Pasar apuntes a LaTeX (flujo automático)

**Disparador**: cuando alguien diga algo como «pasa los apuntes», «pasa la clase del dd/mm a LaTeX» o «transcribe las fotos del dd/mm», hazlo directamente, sin pedir más instrucciones. Si no dice qué día, usa la carpeta más reciente de `papel/` que aún no tenga su fecha en `teoria/`.

1. **Fuentes**: lee todas las fotos de `papel/aaaa-mm-dd/` en orden de numeración (los escaneos de WhatsApp pueden estar en `v2/`), `papel/ESTRUCTURA.md` (qué día → qué sección, qué falta) y, si el tema aparece, las diapositivas de `material/` (sirven para resolver letra dudosa y la numeración de resultados; no copies de ellas lo que no esté en clase, salvo con una `nota`).
2. **Destino**: añade al final del capítulo correspondiente de `teoria/`, empezando con la fecha en negrita `\textbf{dd/mm/aa}`. Si el capítulo no existe, sigue «Capítulo nuevo». Un día por vez.
3. **Formato**: cajas con etiqueta única, `\cref` solo donde el resultado se use de verdad (ver «Convenciones»). Respeta el orden de la clase, aunque difiera del de las diapositivas, y anótalo en `ESTRUCTURA.md`.
4. **Fidelidad**: no inventes pasos ni resultados. Lo ilegible o dudoso va como `% REVISAR: <duda>` y se lista al final; lo que completes para que la demostración sea coherente, indícalo. Lo que no cuadre con las fotos o las diapositivas, a «Lo que no cuadre» de `ESTRUCTURA.md`.
5. **Comprobar** (ver «Comprobar antes de subir»): compila el PDF y `web/construir.sh` debe acabar con «0 sin enlace a los apuntes».
6. **Git**: rama nueva, commit `Teoría: clase del dd/mm (<tema>)`, sin push a `main`. Cuenta al final qué has añadido, las dudas `REVISAR` y las suposiciones.

Si el usuario manda fotos nuevas, primero colócalas en `papel/aaaa-mm-dd/` (derechas, con nombre descriptivo, 1800×2400 como máximo) y añade su fila a la tabla de `papel/ESTRUCTURA.md`.

## Git

- Trabaja en una rama y abre una pull request a `main`; no subas archivos generados ni `material/`.
- Mensajes de commit en español, breves y con prefijo del área (`Teoría:`, `Web:`, `Papel:`).

## La web (`web/`)

- `construir.sh` convierte los apuntes a HTML con make4ht y genera el mapa; la salida es una sola página (`index.html`) con anclas por apartado (`#tema3`), y las URLs antiguas (`tema3.html`) quedan como redirecciones (`partir_html.py`).
- `vista_previa.js`: al pasar el ratón por una referencia, el resultado aparece en un panel a la derecha.
- `apuntes.cfg` y `estilo.css`: configuración de make4ht y estilos (modo claro y oscuro).
- `mapa/generar.py` lee las cajas de `teoria/` y escribe `datos.json`: nodos, aristas (dependencias) y color de cada tema/bloque. `mapa/index.html` dibuja el grafo.
- Al añadir un archivo de teoría, regístralo en `ARCHIVOS` de `mapa/generar.py`.
