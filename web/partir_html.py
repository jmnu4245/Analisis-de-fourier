#!/usr/bin/env python3
"""Parte el HTML único que genera make4ht (main.html) en una página por subsección.

Casi todos los apuntes están en la sección 1 (Series de Fourier), así que se parte por
\\subsection: tema1-1.html, tema1-2.html, ... La cabecera de cada sección va con su primera
subsección, y una sección sin subsecciones es una sola página (tema2.html). Lo anterior a la
primera sección (portada, índice e información de la asignatura) queda en index.html.
Se reescriben los enlaces internos para que apunten a la página donde está cada id.

Uso: partir_html.py carpeta   (lee carpeta/main.html y escribe index.html, tema1-1.html, ...)
"""
import re
import sys
from pathlib import Path

SECCION = re.compile(r'<h3 class=["\']sectionHead["\'][^>]*>')
SUBSECCION = re.compile(r'<h4 class=["\']subsectionHead["\'][^>]*>')
FECHA = re.compile(r'<p[^>]*>(?:(?!</p>).)*\b\d{1,2}/\d{1,2}/\d{2,4}\b(?:(?!</p>).)*</p>\s*$', re.S)


def texto(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html)).strip()


def inicio_de_bloque(contenido, pos):
    """Retrocede hasta el principio de la línea y, si justo antes hay un párrafo con la fecha
    de la clase (p. ej. 30/09/2026), lo incluye en la página nueva."""
    pos = contenido.rfind("\n", 0, pos) + 1
    previo = contenido[max(0, pos - 600):pos]
    m = FECHA.search(previo)
    if m:
        pos -= len(previo) - m.start()
    return pos


def titulo_limpio(t):
    t = re.sub(r"\\\((.*?)\\\)", lambda m: m.group(1), t)  # quita \( \) de MathJax
    t = t.replace("\\mathbb {T}", "𝕋").replace("\\mathbb {R}", "ℝ").replace("\\mathbb {Z}", "ℤ")
    t = re.sub(r"L_(\w)", lambda m: "L" + {"p": "ₚ", "1": "₁", "2": "₂"}.get(m.group(1), m.group(1)), t)
    return re.sub(r"\\[a-zA-Z]+\s*", "", t).replace("{", "").replace("}", "").strip()


def main(carpeta):
    carpeta = Path(carpeta)
    html = (carpeta / "main.html").read_text(encoding="utf-8")
    fin_nav = html.index("</nav>") + len("</nav>")
    fin_body = html.rindex("</body>")
    cabecera, contenido, pie = html[:fin_nav], html[fin_nav:fin_body], html[fin_body:]

    # Puntos de corte: cada sección y cada subsección salvo la primera de su sección.
    cortes = []  # (posición, nombre de página, título)
    secciones = [m.start() for m in SECCION.finditer(contenido)]
    for i, s in enumerate(secciones):
        cab_sec = contenido[s:contenido.index("</h3>", s)]
        num_sec = re.search(r"titlemark[^>]*>\s*(\d+)", cab_sec).group(1)
        titulo_sec = re.sub(r"^[\d.]+\s*", "", texto(cab_sec))
        limite = secciones[i + 1] if i + 1 < len(secciones) else len(contenido)
        subs = list(SUBSECCION.finditer(contenido, s, limite))
        if not subs:
            cortes.append((s, f"tema{num_sec}.html", f"{num_sec}. {titulo_sec}"))
        for j, m in enumerate(subs):
            cab = contenido[m.start():contenido.index("</h4>", m.start())]
            num = re.search(r"titlemark[^>]*>\s*([\d.]*\d)", cab).group(1)
            titulo = f"{num} {re.sub(r'^[\d.]+\s*', '', texto(cab))}"
            cortes.append((s if j == 0 else m.start(), f"tema{num.replace('.', '-')}.html", titulo))

    posiciones = [0] + [inicio_de_bloque(contenido, c[0]) for c in cortes] + [len(contenido)]
    paginas = [("index.html", "Apuntes de Análisis de Fourier")]
    paginas += [(nombre, titulo_limpio(titulo)) for _, nombre, titulo in cortes]
    trozos = [contenido[posiciones[i]:posiciones[i + 1]] for i in range(len(paginas))]

    # Qué ids hay en cada página, para reescribir los enlaces internos.
    donde = {}
    for (nombre, _), trozo in zip(paginas, trozos):
        for ident in re.findall(r'id=["\']([^"\']+)["\']', trozo):
            donde.setdefault(ident, nombre)

    def reescribir(trozo, nombre):
        def cambio(m):
            ident = m.group(2)
            destino = donde.get(ident)
            if destino is None or destino == nombre:
                return f'href="#{ident}"'
            return f'href="{destino}#{ident}"'
        return re.sub(r'href=["\'](main\.html)?#([^"\']+)["\']', cambio, trozo)

    for i, ((nombre, titulo), trozo) in enumerate(zip(paginas, trozos)):
        nuevo = f"<title>{titulo} · Análisis de Fourier</title>" if i else "<title>Apuntes de Análisis de Fourier</title>"
        cab = re.sub(r"<title>.*?</title>", lambda _: nuevo, cabecera, count=1, flags=re.S)
        cab = cab.replace("</head>", '<script src="vista_previa.js" defer></script>\n</head>', 1)
        enlaces = []
        if i > 0:
            enlaces.append(f'<a href="{paginas[i - 1][0]}">← {paginas[i - 1][1]}</a>')
        enlaces.append('<a href="index.html">Índice</a>')
        if i + 1 < len(paginas):
            enlaces.append(f'<a href="{paginas[i + 1][0]}">{paginas[i + 1][1]} →</a>')
        navegacion = f'<nav class="paginas">{" ".join(enlaces)}</nav>'
        cuerpo = reescribir(trozo, nombre)
        (carpeta / nombre).write_text(cab + navegacion + cuerpo + navegacion + pie, encoding="utf-8")
    (carpeta / "main.html").unlink()

    # Para el mapa: en qué página está cada id.
    (carpeta / "ids.tsv").write_text("".join(f"{k}\t{v}\n" for k, v in donde.items()), encoding="utf-8")
    print(f"{len(paginas)} páginas:", ", ".join(p for p, _ in paginas))


if __name__ == "__main__":
    main(sys.argv[1])
