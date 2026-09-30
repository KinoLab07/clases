#!/usr/bin/env python3
"""Convierte el HTML de WordPress (reference/pages.json) en fragmentos limpios
dentro de content/.

Lo que más pesa aquí no son las imágenes —no hay— sino la morralla que deja el
pegado desde Word: atributos data-ccp-*, clases TextRun/SCXW y divs de
maquetación de PDF.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGINA_DE_SLUG = {
    'referentes-varios': 'index',
    'introduccion-a-las-artes-electronicas': 'introduccion',
    'imagen-fija': 'imagen-fija',
    'sonido': 'sonido',
    'video': 'video',
}

ENLACE_A_PAGINA = {
    'referentes-varios': 'index.html',
    'introduccion-a-las-artes-electronicas': 'introduccion.html',
    'imagen-fija': 'imagen-fija.html',
    'sonido': 'sonido.html',
    'video': 'video.html',
}


def embeber(url):
    """Un bloque de vídeo incrustado. En el sitio publicado estos bloques se
    quedaron sin resolver y salían como texto plano: ni reproductor ni enlace.
    """
    url = html.unescape(url).strip()

    m = re.search(r'(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)', url)
    if m:
        return (f'<div class="video">'
                f'<iframe src="https://www.youtube-nocookie.com/embed/{m.group(1)}" '
                f'title="YouTube" loading="lazy" '
                f'allow="accelerometer; clipboard-write; encrypted-media; '
                f'gyroscope; picture-in-picture" allowfullscreen></iframe></div>')

    m = re.search(r'vimeo\.com/(\d+)', url)
    if m:
        return (f'<div class="video">'
                f'<iframe src="https://player.vimeo.com/video/{m.group(1)}?dnt=1" '
                f'title="Vimeo" loading="lazy" '
                f'allow="fullscreen; picture-in-picture" allowfullscreen></iframe></div>')

    return f'<p><a href="{url}" target="_blank" rel="noopener">{url}</a></p>'


CLASES_FUERA = re.compile(
    r'^(wp-block-[\w-]*|wp-embed-[\w-]*|wp-has-aspect-ratio|is-type-\w+|'
    r'is-provider-\w+|has-alpha-channel-opacity|has-css-opacity|is-style-\w+|'
    r'TextRun|NormalTextRun|EOP|SCXW\d*|BCX\d*|math-inline|layoutArea|column|page)$')

MAPA_CLASES = {'has-text-align-center': 'center'}


def limpiar_clases(v):
    fuera = []
    for c in v.split():
        if c in MAPA_CLASES:
            fuera.append(MAPA_CLASES[c])
        elif not CLASES_FUERA.match(c):
            fuera.append(c)
    vistos, res = set(), []
    for c in fuera:
        if c not in vistos:
            vistos.add(c); res.append(c)
    return ' '.join(res)


def convertir(c):
    # --- bloques de vídeo incrustado ---
    c = re.sub(r'<figure class="wp-block-embed[^"]*">\s*'
               r'<div class="wp-block-embed__wrapper">(.*?)</div>\s*</figure>',
               lambda m: embeber(m.group(1)), c, flags=re.S)

    # --- morralla del pegado desde Word y desde otros editores ---
    c = re.sub(r'\sdata-(ccp-[\w-]+|contrast|fontsize|usefontface|math|'
               r'index-in-node|path-to-node|wplink-edit)="[^"]*"', '', c)
    c = re.sub(r'\s(xml:)?lang="[^"]*"', '', c)
    # divs de maquetación que venían de un PDF
    c = re.sub(r'<div class="(page|layoutArea|column)"[^>]*>', '<div>', c)
    # un .post-content pegado a mano dentro del contenido: la plantilla ya lo pone
    c = re.sub(r'<div class="post-content">', '<div>', c)

    # --- LaTeX que se quedó sin convertir y se leía en crudo en la web ---
    c = re.sub(r'\$\s*([\d.,]+)\s*\\times\s*([\d.,]+)\s*\$', r'\1 × \2', c)

    # --- estilos en línea ---
    c = c.replace('style="text-align: center;"', 'class="center"')
    c = c.replace('style="text-align: center"', 'class="center"')
    c = re.sub(r'<span style="color: #993300;">(.*?)</span>',
               r'<span class="destacado">\1</span>', c, flags=re.S)

    # --- clases ---
    c = re.sub(r'\sclass="([^"]*)"',
               lambda m: (f' class="{limpiar_clases(m.group(1))}"'
                          if limpiar_clases(m.group(1)) else ''), c)

    # --- separadores ---
    c = re.sub(r'<hr[^>]*/?>', '<hr>', c)

    # --- enlaces ---
    def enlace(m):
        u = html.unescape(m.group(1))
        if 'clases.kinolab07.co' in u:
            slug = u.rstrip('/').split('/')[-1]
            destino = ENLACE_A_PAGINA.get(slug)
            if destino:
                return f'<a href="{destino}"{m.group(2)}>'
            return f'<a href="index.html"{m.group(2)}>'
        return f'<a href="{m.group(1)}" target="_blank" rel="noopener"{m.group(2)}>'
    c = re.sub(r'<a href="([^"]+)"([^>]*)>', enlace, c)
    c = re.sub(r'\s(target|rel)="[^"]*"(?=[^>]*\s\1=)', '', c)

    # --- envoltorios vacíos y espacios ---
    for _ in range(4):
        c = re.sub(r'<span>([^<]*(?:<(?!/?span)[^>]*>[^<]*)*)</span>', r'\1', c)
    c = re.sub(r'<div>\s*</div>', '', c)
    c = re.sub(r'<div>\s*(<div>\s*)+', '<div>', c)
    c = c.replace('\r\n', '\n').replace('\r', '\n')
    c = re.sub(r'[ \t]+\n', '\n', c)
    c = re.sub(r'\n{3,}', '\n\n', c)
    return c.strip() + '\n'


if __name__ == '__main__':
    paginas = {p['slug']: p for p in json.load(open(f'{ROOT}/reference/pages.json'))}
    for slug, nombre in PAGINA_DE_SLUG.items():
        salida = convertir(paginas[slug]['content']['rendered'])
        open(f'{ROOT}/content/{nombre}.html', 'w', encoding='utf-8').write(salida)
        antes = len(paginas[slug]['content']['rendered'])
        print(f'  {nombre + ".html":22} {antes:>6} -> {len(salida):>6} B '
              f'({100 - len(salida) * 100 // antes}% menos)  <- {slug}')
