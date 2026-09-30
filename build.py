#!/usr/bin/env python3
"""Genera el sitio estático de clases.kinolab07.co.

    python3 build.py            para publicar
    python3 build.py --local    el enlace al sitio principal apunta a localhost

Salida: index.html y los demás .html en la raíz.
"""
import json, os, re, html, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = json.load(open(f'{ROOT}/src/site.json', encoding='utf-8'))
TEMPLATE = open(f'{ROOT}/src/template.html', encoding='utf-8').read()

LOCAL = '--local' in sys.argv
PRINCIPAL = SITE['sitio_principal_local'] if LOCAL else SITE['sitio_principal']

CHEVRON = ('<svg viewBox="0 0 10 6" aria-hidden="true" focusable="false">'
           '<path d="M1 1l4 4 4-4" fill="none" stroke="currentColor" '
           'stroke-width="1.4"/></svg>')


def archivo(page):
    return 'index.html' if page == 'index' else f'{page}.html'


def render_menu(actual, sangria='                '):
    t = SITE['titles']
    out = [f'{sangria}<ul class="menu-primary-items">']
    for page in SITE['menu']:
        clases = 'menu-item current-menu-item' if page == actual else 'menu-item'
        aria = ' aria-current="page"' if page == actual else ''
        out.append(f'{sangria}  <li class="{clases}">'
                   f'<a href="{archivo(page)}"{aria}>{html.escape(t[page])}</a></li>')
    out.append(f'{sangria}</ul>')
    return '\n'.join(out)


def resumen(contenido, limite=155):
    texto = re.sub(r'<[^>]+>', ' ', contenido)
    texto = html.unescape(re.sub(r'\s+', ' ', texto)).strip()
    return texto if len(texto) <= limite else texto[:limite].rsplit(' ', 1)[0] + '…'


def build_page(page):
    titulo = SITE['titles'][page]
    contenido = open(f'{ROOT}/content/{page}.html', encoding='utf-8').read()

    head_title = (SITE['site_title'] if page == 'index'
                  else f'{titulo} – {SITE["site_title"]}')
    canonical = (f'{SITE["base_url"]}/' if page == 'index'
                 else f'{SITE["base_url"]}/{archivo(page)}')

    valores = {
        'html_lang': SITE['html_lang'],
        'page': page,
        'head_title': html.escape(head_title),
        'description': html.escape(resumen(contenido)),
        'canonical': canonical,
        'site_title': html.escape(SITE['site_title']),
        'skip': html.escape(SITE['skip']),
        'open_menu': html.escape(SITE['open_menu']),
        'sidebar_label': html.escape(SITE['sidebar_label']),
        'sitio_principal': PRINCIPAL,
        'sitio_principal_texto': html.escape(SITE['sitio_principal_texto']),
        'footer': html.escape(SITE['footer']),
        'title': html.escape(titulo),
        'menu': render_menu(page),
        'content': contenido,
    }

    out = TEMPLATE
    for k, v in valores.items():
        out = out.replace('{{' + k + '}}', v)

    sobrantes = re.findall(r'\{\{(\w+)\}\}', out)
    if sobrantes:
        sys.exit(f'marcador sin sustituir en {page}: {set(sobrantes)}')

    open(f'{ROOT}/{archivo(page)}', 'w', encoding='utf-8').write(out)


def main():
    for page in SITE['menu']:
        build_page(page)
    print(f'{len(SITE["menu"])} páginas generadas.')
    if LOCAL:
        print(f'Modo local: el enlace al sitio principal apunta a {PRINCIPAL}')
        print('Vuelve a ejecutar "python3 build.py" sin --local antes de publicar.')


if __name__ == '__main__':
    main()
