#!/usr/bin/env python3
"""Genera datos.json para el mapa interactivo de resultados y enlaza las referencias de los apuntes HTML.

Cada teorema, proposición, definición, observación, nota y ejemplo es un nodo, con su número
(el de la caja: "Teorema 1.5"), su número de clase si lo tiene (el de los apuntes de clase y las
diapositivas AF_1: "Teorema 1.12", que va en el título de la caja), enunciado y demostración.

Hay una arista A -> B ("B usa A") cuando el enunciado o la demostración de B cita a A:
  - con \\cref;
  - por su número de clase ("por el Teorema 1.20", "Corolario 1.14");
  - por su nombre en la demostración ("Lema de Riemann-Lebesgue", "Test de Dini"), si A va antes;
  - o porque está en la lista EXTRA (dependencias que el texto no dice explícitamente).
Las citas por número de clase también se convierten en enlaces en los apuntes HTML.

Uso: generar.py raiz_del_repo carpeta_con_los_aux carpeta_apuntes_html salida.json
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ARCHIVOS = [  # (archivo .tex, número de sección)
    ("SeriesFourier", 1),
    ("TransformadaFourier", 2),
    ("EspaciosHardy", 3),
]
# Bloques del mapa (colores y filtros): (sección, primera subsección, nombre, color).
# Cada subsección va al último bloque que empieza en ella o antes.
BLOQUES = [
    (1, 0, "Definiciones básicas", "#2f7d6d"),
    (1, 5, "𝕋, C(𝕋), Lₚ y densidad", "#c0662c"),
    (1, 7, "Coeficientes y convolución", "#4a5bc4"),
    (1, 10, "Dirichlet y Dini", "#9c3f8c"),
    (1, 12, "Cesàro y Fejér", "#b3182b"),
    (1, 16, "Series en L₂", "#1e6b66"),
    (2, 0, "Transformada", "#2448a8"),
    (3, 0, "Hardy", "#7a5a12"),
]
TIPOS = {  # entorno -> (nombre, prefijo de etiqueta)
    "teorema": ("Teorema", "thm"),
    "proposicion": ("Proposición", "prop"),
    "definicion": ("Definición", "def"),
    "observacion": ("Observación", "obs"),
    "nota": ("Nota", "not"),
    "ejemplo": ("Ejemplo", "ej"),
}
PREFIJO_A_TIPO = {p: t for t, (_, p) in TIPOS.items()}

# Número de clase de las cajas que no lo llevan en el título (según estructura_apuntes.md y las
# citas del propio texto: "Proposición 1.6 (||K*h|| <= ||K|| ||h||)", "Proposición 1.1", ...).
CLASE_MANUAL = {
    "prop:densidad_ct": "1.1",
    "prop:incl_dens_lp": "1.2",
    "def:conv_l1": "1.6",
    "prop:fourier_conv": "1.7",
    "prop:prop_dirichlet": "1.8",
    "thm:dini": "1.13",
}
# Citas por nombre (solo en demostraciones y solo hacia resultados anteriores).
NOMBRES = {
    r"H[öo]lder": "thm:holder",
    r"Riemann[- ]Lebesgue": "1.11",
    r"[Tt]est de Dini": "1.13",
    r"Stone[-–—]+Weierstra": "obs:recordatorio_densidad",
}
CITA = re.compile(r"\b(?:Teoremas?|Proposici(?:ó|o)n(?:es)?|Prop\.?|Propiedad|Corolarios?|Lemas?|Observaci(?:ó|o)n)"
                  r"\s+(\d+\.\d+)\b")
TITULO_CLASE = re.compile(r"^\s*(?:Teorema|Proposici(?:ó|o)n|Prop\.?|Propiedad|Lema|Corolario)\s+(\d+\.\d+)\b")

# Dependencias que no se citan en el texto. Cada línea: un resultado y después los que lo usan.
# Se puede nombrar un resultado por su clave (thm:holder) o por su número de clase (1.20).
EXTRA = """
def:coef_fourier def:serie_fourier not:notacion_coeficientes
def:serie_fourier not:notacion_coeficientes def:def_fourier_formal
not:notacion_coeficientes obs:recuperacion_coeficientes def:def_fourier_formal
def:toro obs:prop_toro not:homomorfismo_toro not:func_toro def:espacio_ct
def:espacio_ct 1.1 def:pol_trig
def:pol_trig 1.1 prop:coef_pol_trig
obs:recordatorio_densidad 1.1
1.1 not:interpretacion_prop obs:obs_jerarquia_espacios 1.4
def:espacio_lp thm:holder 1.2 def:def_fourier_formal
thm:holder 1.2
1.2 obs:obs_jerarquia_espacios 1.4 1.11 1.24
prop:coef_pol_trig 1.4
def:def_fourier_formal prop:coef_pol_trig obs:conv_uniforme_fourier 1.4 obs:obs_convergencia ej:ejemplo_signo ej:ejemplo_base_exp
1.4 not:nota_cvg
def:def_convolucion prop:prop_1_5
prop:prop_1_5 1.6
1.6 1.7 1.8 obs:obs_norma_fejer
1.7 obs:unidad_conv
def:nucleo_dirichlet 1.8
1.8 1.9 1.12 def:nucleo_fejer 1.19
1.9 obs:obs_banach_steinhaus_l1
thm:weierstrass_m ej:conv_unif_t2
1.11 1.12 1.13
1.12 obs:obs_phi_integrable
1.12 1.13
1.13 1.14
def:cesaro_sucesion 1.17 def:cesaro_serie
def:cesaro_serie not:nota_indices_cesaro def:media_cesaro_f
not:nota_indices_cesaro def:media_cesaro_f
def:media_cesaro_f def:nucleo_fejer
def:nucleo_fejer 1.18 1.19
1.18 1.19 obs:obs_norma_fejer 1.30
1.19 obs:obs_norma_fejer obs:obs_fejer_sumabilidad 1.30
obs:obs_norma_fejer obs:obs_fejer_sumabilidad
def:nucleo_sumabilidad 1.20 obs:obs_fejer_sumabilidad 1.24 1.28
obs:obs_fejer_sumabilidad 1.21
1.20 1.21 1.24
1.21 1.22 1.23
1.24 1.25 1.28
1.25 1.26 1.27
1.28 1.29
1.30 1.31
1.29 thm:thm_fejer_ae
def:prod_escalar_l2 1.32
1.32 def:prehilbert
def:son def:coef_son
def:coef_son not:nota_error_sn 1.33
not:nota_error_sn 1.33
"""

# Citas que no son dependencias (comparaciones: "es la Proposición 1.4 para funciones continuas").
EXCLUIR = {("1.4", "1.23"), ("1.1", "1.22")}

DEMO_DE = re.compile(r"Demostraci(?:ó|o)n del? (?:Teorema|Proposici(?:ó|o)n|Corolario|Lema) (\d+\.\d+)")
INICIO = re.compile(r"\\begin\{(" + "|".join(TIPOS) + r")\}")


# ---------------------------------------------------------------- lectura de LaTeX
def sin_comentarios(s):
    return re.sub(r"(?<!\\)%.*", "", s)


def grupo(s, i):
    """Lee el grupo {…} que empieza en s[i] (saltando espacios). Devuelve (contenido, fin)."""
    while s[i].isspace():
        i += 1
    assert s[i] == "{", s[i:i + 30]
    nivel, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            nivel += 1
        elif c == "}":
            nivel -= 1
            if nivel == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError("llave sin cerrar")


def entorno(s, nombre, desde):
    """Posiciones (fin_cuerpo, fin_total) del entorno `nombre` que empieza en `desde`."""
    abre, cierra = "\\begin{%s}" % nombre, "\\end{%s}" % nombre
    nivel, j = 0, desde
    while True:
        a, c = s.find(abre, j), s.find(cierra, j)
        if a != -1 and a < c:
            nivel, j = nivel + 1, a + len(abre)
        else:
            nivel -= 1
            if nivel == 0:
                return c, c + len(cierra)
            j = c + len(cierra)


def slug(texto):
    texto = re.sub(r"\$[^$]*\$", "", texto).replace("ß", "ss")
    texto = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"\\[a-zA-Z]+", "", texto)
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")[:40].strip("-")


# ---------------------------------------------------------------- LaTeX -> HTML (para el panel)
MATES = re.compile(r"\$\$.*?\$\$|\$(?:\\.|[^$])+\$|\\\[.*?\\\]|\\\(.*?\\\)"
                   r"|\\begin\{(align\*?|equation\*?|gather\*?|multline\*?)\}.*?\\end\{\1\}", re.S)
SIMPLES = {"textbf": "b", "emph": "i", "textit": "i", "texttt": "code", "underline": "u", "textsc": "span"}


def reemplazar_comando(s, cmd, f, nargs=1):
    patron = re.compile(r"\\" + cmd + r"(?![a-zA-Z])")
    while True:
        m = patron.search(s)
        if not m:
            return s
        j, args = m.end(), []
        try:
            while j < len(s) and s[j] == "[":  # argumento opcional
                j = s.index("]", j) + 1
            for _ in range(nargs):
                a, j = grupo(s, j)
                args.append(a)
        except (AssertionError, ValueError, IndexError):
            s = s[:m.start()] + s[m.end():]
            continue
        s = s[:m.start()] + f(*args) + s[j:]


def a_html(tex, nombre_ref, por_clase):
    tex = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
                 "\n\n[[FIG]]\n\n", tex, flags=re.S)
    tex = re.sub(r"\\begin\{tabular\}.*?\\end\{tabular\}", "\n\n[[TABLA]]\n\n", tex, flags=re.S)
    mates = []

    def guardar(m):
        mates.append(m.group(0))
        return f"\x00{len(mates) - 1}\x00"

    tex = MATES.sub(guardar, tex)
    tex = html.escape(tex, quote=False)
    tex = reemplazar_comando(tex, "texorpdfstring", lambda a, _b: a, 2)
    tex = reemplazar_comando(tex, "href", lambda u, t: f'<a href="{u}">{t}</a>', 2)
    for cmd in ("cref", "Cref"):
        tex = reemplazar_comando(tex, cmd, lambda ls: ", ".join(
            f'<a class="ref" data-id="{l.strip()}">{nombre_ref(l.strip())}</a>' for l in ls.split(",")))
    tex = CITA.sub(lambda m: f'<a class="ref" data-id="{por_clase[m.group(1)]}">{m.group(0)}</a>'
                   if m.group(1) in por_clase else m.group(0), tex)
    for cmd, etiqueta in SIMPLES.items():
        tex = reemplazar_comando(tex, cmd, lambda x, e=etiqueta: f"<{e}>{x}</{e}>")
    tex = reemplazar_comando(tex, "textcircled", lambda x: f"({x})")
    tex = reemplazar_comando(tex, "footnote", lambda x: f" ({x})")
    for cmd in ("label", "vspace", "hspace", "phantom"):
        tex = reemplazar_comando(tex, cmd, lambda *_: "")
    tex = re.sub(r"\\begin\{(itemize|description)\}", "<ul>", tex)
    tex = re.sub(r"\\end\{(itemize|description)\}", "</li></ul>", tex)
    tex = tex.replace("\\begin{enumerate}", "<ol>").replace("\\end{enumerate}", "</li></ol>")
    tex = re.sub(r"\\item\s*\[([^\]]*)\]", r"</li><li class='etq'><b>\1</b> ", tex)
    tex = re.sub(r"\\item\b", "</li><li>", tex)
    tex = re.sub(r"<(ul|ol)>\s*</li>", r"<\1>", tex)
    tex = re.sub(r"\\setcounter\{[^}]*\}\{[^}]*\}", "", tex)
    tex = re.sub(r"\\(begin|end)\{(center|flushleft|flushright|minipage|quote)\}(\{[^}]*\})?", "", tex)
    for a, b in (("\\\\", "<br>"), ("~", "&nbsp;"), ("``", "“"), ("''", "”"), ("---", "—"),
                 ("--", "–"), ("\\ldots", "…"), ("\\dots", "…"), ("\\quad", " "), ("\\qquad", "  "),
                 ("\\%", "%"), ("\\&amp;", "&amp;"), ("\\,", " "), ("\\_", "_")):
        tex = tex.replace(a, b)
    tex = re.sub(r"\\(noindent|medskip|bigskip|smallskip|hfill|centering|par|newline|clearpage|qedhere)\b", "", tex)
    tex = re.sub(r"\n\s*\n", "<br class='par'>", tex.strip())
    tex = tex.replace("[[FIG]]", "<span class='fig'>[figura: véase en los apuntes]</span>")
    tex = tex.replace("[[TABLA]]", "<span class='fig'>[tabla: véase en los apuntes]</span>")
    tex = re.sub(r"\x00(\d+)\x00", lambda m: html.escape(mates[int(m.group(1))], quote=False), tex)
    return tex


SIMBOLOS = {
    r"\mathbb{T}": "𝕋", r"\mathbb{R}": "ℝ", r"\mathbb{Z}": "ℤ", r"\mathbb{C}": "ℂ", r"\mathbb{N}": "ℕ",
    r"\mathcal{P}": "𝒫", r"\mathcal{C}": "𝒞", r"\Phi": "Φ", r"\delta": "δ", r"\varepsilon": "ε",
    r"\sigma": "σ", r"\sum": "Σ", r"\pi": "π", r"\to": "→", r"\infty": "∞", r"\dots": "…", r"\cdot": "·",
}
SUB = str.maketrans("0123456789pN", "₀₁₂₃₄₅₆₇₈₉ₚN")


def a_texto(tex):
    """Versión en texto plano (para la etiqueta del nodo, que no puede llevar MathJax)."""
    s = tex
    for a, b in sorted(SIMBOLOS.items(), key=lambda x: -len(x[0])):
        s = s.replace(a, b)
    s = re.sub(r"_\{?([0-9pN])\}?", lambda m: m.group(1).translate(SUB), s)
    s = re.sub(r"\\[a-zA-Z]+\*?", "", s)
    s = s.replace("$", "").replace("{", "").replace("}", "").replace("--", "–")
    return re.sub(r"\s+", " ", s).strip(" .")


# ---------------------------------------------------------------- extracción
def urls(carpeta_html):
    """(entorno, número) -> 'pagina.html#id' buscando las cajas en las páginas HTML."""
    destino = {}
    patron = re.compile(r'<div class=["\']tcolorbox (\w+)["\'] id=["\']([^"\']+)["\']>\s*(?:<a [^>]*></a>\s*)?'
                        r'<div class=["\']tcolorbox-title["\']>\s*(?:<!--[^>]*-->)?\s*<p[^>]*>\s*'
                        r'(?:[^\s<]+\s+){1,2}?([\d.]*\d)(?::|\s*</p>)')
    for pagina in sorted(Path(carpeta_html).glob("*.html")):
        for env, ident, num in patron.findall(pagina.read_text(encoding="utf-8")):
            destino.setdefault((env, num), f"{pagina.name}#{ident}")
    return destino


def bloque_de(seccion, subseccion):
    elegido = 0
    for i, (s, sub, _, _) in enumerate(BLOQUES):
        if (s, sub) <= (seccion, subseccion):
            elegido = i
    return elegido + 1


def extraer(raiz, destinos):
    nodos, orden = {}, 0
    for archivo, seccion in ARCHIVOS:
        ruta = Path(raiz) / f"{archivo}.tex"
        if not ruta.exists():
            continue
        s = sin_comentarios(ruta.read_text(encoding="utf-8"))
        subsecciones = [m.start() for m in re.finditer(r"\\subsection\{", s)]
        contador = {}  # cada tipo de caja se numera aparte dentro de su sección
        for m in INICIO.finditer(s):
            env = m.group(1)
            contador[env] = contador.get(env, 0) + 1
            numero = f"{seccion}.{contador[env]}"
            titulo, j = grupo(s, m.end())
            etiqueta, j = grupo(s, j)
            prefijo = TIPOS[env][1]
            clave = f"{prefijo}:{etiqueta.strip() or slug(titulo) or numero}"
            while clave in nodos:
                clave += "-bis"
            fin_cuerpo, fin = entorno(s, env, m.start())
            cuerpo = s[j:fin_cuerpo]
            # Demostraciones justo después de la caja (puede haber varias: una por apartado).
            sig = INICIO.search(s, fin)
            limite = min([len(s)] + ([sig.start()] if sig else [])
                         + [p for p in (s.find("\\section", fin), s.find("\\subsection", fin)) if p != -1])
            demos, k = [], s.find("\\begin{proof}", fin, limite)
            while k != -1:
                p_fin, p_total = entorno(s, "proof", k)
                demo = s[k:p_fin]
                cab = re.match(r"\\begin\{proof\}(?:\[([^\]]*)\])?", demo)
                k = s.find("\\begin{proof}", p_total, limite)
                if cab.group(1) and DEMO_DE.match(cab.group(1)):
                    continue  # es de otro resultado; se asigna abajo
                demos.append(((f"\\textbf{{{cab.group(1)}.}} " if cab.group(1) else "") + demo[cab.end():]).strip())
            sub = sum(1 for p in subsecciones if p < m.start())
            mc = TITULO_CLASE.match(titulo)
            clase = mc.group(1) if mc else CLASE_MANUAL.get(clave, "")
            orden += 1
            nodos[clave] = {
                "id": clave, "tipo": env, "nombreTipo": TIPOS[env][0], "numero": numero,
                "seccion": seccion, "subseccion": f"{seccion}.{sub}" if sub else str(seccion),
                "tema": bloque_de(seccion, sub), "clase": clase, "tituloTex": titulo,
                "cuerpo": cuerpo, "demo": "\n\n".join(demos), "orden": orden,
                "url": destinos.get((env, numero), ""),
            }
        # Demostraciones sueltas con título "Demostración del Teorema 1.20 (...)".
        for m in re.finditer(r"\\begin\{proof\}\[(" + DEMO_DE.pattern + r")[^\]]*\]", s):
            for n in nodos.values():
                if n["clase"] == m.group(2) and n["seccion"] == seccion:
                    p_fin, _ = entorno(s, "proof", m.start())
                    n["demo"] = (n["demo"] + "\n\n" + s[m.end():p_fin]).strip()
    return nodos


def enlazar_citas(t, por_clase, todos):
    """Convierte "Teorema 1.20" en enlace a su caja, fuera de etiquetas, de otros enlaces, de los
    títulos de las cajas y de la cabecera de la página."""
    trozos = re.split(r"(<[^>]+>)", t)
    dentro_a = dentro_titulo = dentro_cab = 0
    for i, trozo in enumerate(trozos):
        if trozo.startswith("<"):
            low = trozo.lower()
            if low.startswith("<a ") or low == "<a>":
                dentro_a += 1
            elif low.startswith("</a"):
                dentro_a = max(0, dentro_a - 1)
            elif "tcolorbox-title" in low:
                dentro_titulo = 1
            elif low.startswith("</div") and dentro_titulo:
                dentro_titulo = 0
            elif low.startswith(("<head", "<title", "<script", "<nav")):
                dentro_cab += 1
            elif low.startswith(("</head", "</title", "</script", "</nav")):
                dentro_cab = max(0, dentro_cab - 1)
            continue
        if dentro_a or dentro_titulo or dentro_cab or not trozo.strip():
            continue

        def cambio(m):
            clave = por_clase.get(m.group(1))
            url = todos[clave]["url"] if clave else ""
            return f'<a href="{url}">{m.group(0)}</a>' if url else m.group(0)
        trozos[i] = CITA.sub(cambio, trozo)
    return "".join(trozos)


def resolver_referencias(carpeta_html, todos, por_clase):
    """Cambia las marcas [[REF:a,b]] que deja \\cref en el HTML por enlaces ("Proposición 1.7")
    y enlaza las citas por número de clase."""
    def enlace(clave, mayuscula):
        n = todos.get(clave)
        tipo = PREFIJO_A_TIPO.get(clave.split(":")[0])
        nombre = TIPOS[tipo][0] if tipo else ""
        nombre = nombre if mayuscula else nombre.lower()
        texto = f"{nombre} {n['numero'] if n else '??'}".strip()
        return f'<a href="{n["url"]}">{texto}</a>' if n and n["url"] else texto

    def cambio(m):
        claves = [c.strip() for c in m.group(2).split(",")]
        partes = [enlace(c, m.group(1) == "M" and i == 0) for i, c in enumerate(claves)]
        return partes[0] if len(partes) == 1 else ", ".join(partes[:-1]) + " y " + partes[-1]

    for pagina in Path(carpeta_html).glob("*.html"):
        t = pagina.read_text(encoding="utf-8")
        nuevo = re.sub(r"\[\[REF(M?):([^\]]+)\]\]", cambio, t)
        nuevo = enlazar_citas(nuevo, por_clase, todos)
        if nuevo != t:
            pagina.write_text(nuevo, encoding="utf-8")


def main(raiz, carpeta_aux, carpeta_html, salida):
    destinos = urls(carpeta_html)
    nodos = extraer(raiz, destinos)
    por_clase = {}
    for clave, n in nodos.items():
        if n["clase"]:
            por_clase.setdefault(n["clase"], clave)

    def resolver(token):
        return token if token in nodos else por_clase.get(token)

    def nombre_ref(clave):
        n = nodos.get(clave)
        return f"{n['nombreTipo']} {n['numero']}" if n else "??"

    aristas = set()
    for clave, n in nodos.items():
        texto = n["cuerpo"] + "\n" + n["demo"]
        citados = set()
        for grupo_refs in re.findall(r"\\[cC]ref\{([^}]*)\}", texto):
            citados.update(x.strip() for x in grupo_refs.split(","))
        citados.update(por_clase[c] for c in CITA.findall(texto) if c in por_clase)
        for patron, destino in NOMBRES.items():
            otro = resolver(destino)
            if otro and re.search(patron, n["demo"]) and nodos[otro]["orden"] < n["orden"]:
                citados.add(otro)
        for otro in citados:
            if otro in nodos and otro != clave:
                aristas.add((otro, clave))  # otro -> clave: "otro se usa en clave"
    for a, b in EXCLUIR:
        aristas.discard((resolver(a), resolver(b)))
    for linea in EXTRA.strip().splitlines():
        origen, *usuarios = [resolver(x) or "?" + x for x in linea.split()]
        for u in usuarios:
            if origen in nodos and u in nodos:
                aristas.add((origen, u))
            else:
                print(f"aviso: arista desconocida {origen} -> {u}")

    usados = sorted({n["tema"] for n in nodos.values()})
    datos = {
        "temas": [{"n": i, "nombre": BLOQUES[i - 1][2], "color": BLOQUES[i - 1][3]} for i in usados],
        "nodos": [],
        "aristas": [{"de": a, "a": b} for a, b in sorted(aristas)],
    }
    for n in nodos.values():
        titulo = a_texto(n["tituloTex"]) or (f"{n['nombreTipo']} {n['clase']} de clase" if n["clase"] else "")
        datos["nodos"].append({
            "id": n["id"], "tipo": n["tipo"], "nombreTipo": n["nombreTipo"], "numero": n["numero"],
            "tema": n["tema"], "subseccion": n["subseccion"], "marcas": [],
            "clase": [n["clase"]] if n["clase"] else [],
            "titulo": titulo,
            "tituloHtml": a_html(n["tituloTex"], nombre_ref, por_clase),
            "enunciado": a_html(n["cuerpo"], nombre_ref, por_clase),
            "demostracion": a_html(n["demo"], nombre_ref, por_clase) if n["demo"].strip() else "",
            "url": n["url"],
        })
    resolver_referencias(carpeta_html, nodos, por_clase)
    Path(salida).write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")
    sin_url = sum(1 for n in datos["nodos"] if not n["url"])
    print(f"{len(datos['nodos'])} resultados, {len(aristas)} dependencias ({sin_url} sin enlace a los apuntes)")


if __name__ == "__main__":
    main(*sys.argv[1:5])
