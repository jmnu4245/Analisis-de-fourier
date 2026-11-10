#!/usr/bin/env python3
"""Convierte el HTML único de make4ht (main.html) en la web de los apuntes: una sola página continua.

Todo queda en index.html. Donde la versión anterior cortaba en páginas (por sección, y por subsección
dentro de las partes largas) se deja un ancla (#tema3), y cada página antigua (tema3.html) queda como
redirección a ese ancla para no romper enlaces. También escribe ids.tsv (id -> página) para el mapa.

Uso: partir_html.py carpeta   (lee carpeta/main.html y escribe index.html y las redirecciones, tema1-1.html, ...)
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
    # Una sola página continua: en cada punto donde antes se cortaba se pone un ancla (#tema3) y
    # las páginas antiguas (tema3.html#...) quedan como redirecciones, para no romper enlaces.
    anclas = [nombre[:-len(".html")] for nombre, _ in paginas[1:]]
    trozos = [contenido[posiciones[i]:posiciones[i + 1]] for i in range(len(paginas))]
    cuerpo = trozos[0] + "".join(f'<span class="ancla-apartado" id="{a}"></span>{t}' for a, t in zip(anclas, trozos[1:]))
    cuerpo = re.sub(r'href=(["\'])(?:main\.html)?#', r'href=\1#', cuerpo)
    cab = re.sub(r"<title>.*?</title>", lambda _: f"<title>{paginas[0][1]}</title>", cabecera, count=1, flags=re.S)
    cab = cab.replace("</head>", '<script src="vista_previa.js" defer></script>\n</head>', 1)
    (carpeta / "index.html").write_text(cab + cuerpo + pie, encoding="utf-8")
    (carpeta / "main.html").unlink()
    for a in anclas:
        (carpeta / f"{a}.html").write_text(
            f'<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><title>{paginas[0][1]}</title>'
            f'<meta http-equiv="refresh" content="0; url=index.html#{a}">'
            f'<script>location.replace("index.html" + (location.hash || "#{a}"))</script></head>'
            f'<body><a href="index.html#{a}">Ir a los apuntes</a></body></html>', encoding="utf-8")

    # Para el mapa: todo está en index.html.
    ids = re.findall(r'id=["\']([^"\']+)["\']', cuerpo)
    (carpeta / "ids.tsv").write_text("".join(f"{k}\tindex.html\n" for k in dict.fromkeys(ids)), encoding="utf-8")
    print("Una página continua con", len(anclas), "apartados:", ", ".join(anclas))


if __name__ == "__main__":
    main(sys.argv[1])
