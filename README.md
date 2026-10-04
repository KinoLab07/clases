# clases.kinolab07.co

Material de clase de **Enrico Mandirola**: programa de curso y listas de
referencias para asignaturas de artes electrónicas, imagen, sonido y vídeo.

Reconstruido a partir del WordPress que había en `clases.kinolab07.co`
(descargado el 30 de septiembre de 2026) para poder editarlo sin depender de
WordPress. Usa el mismo tema —Cele— que el sitio principal, así que comparte
con él la hoja de estilo, la tipografía y el script del menú.

## Cómo trabajar

```bash
python3 build.py                 # regenera las 5 páginas
python3 -m http.server 4709      # y abre http://localhost:4709
```

Solo hace falta Python 3.

Para probarlo junto al sitio principal, con el enlace de la barra lateral
apuntando al servidor local en vez de al dominio:

```bash
./tools/probar-offline.sh
```

**Antes de publicar hay que volver a generar sin `--local`.**

## Estructura

```
build.py              genera el sitio  ->  python3 build.py
src/
  site.json           menú, títulos, textos de la interfaz
  template.html       plantilla común
content/*.html        el contenido de cada página, editable
assets/
  css/style.css       el diseño (el mismo del sitio principal)
  css/fuentes.css     las @font-face de Open Sans
  fonts/              Open Sans (4 archivos woff2)
  js/menu.js          el menú hamburguesa
reference/            el WordPress original, como material de consulta
  html/               las 5 páginas tal como las servía WordPress
  pages.json          volcado de la REST API
tools/convert.py      el conversor de un solo uso que generó content/
```

**Los `.html` de la raíz son generados: no los edites a mano.** Edita
`content/` o `src/` y vuelve a ejecutar `python3 build.py`.

## Qué se encontró y qué se arregló

### Dos fallos del sitio publicado

**Los cinco vídeos incrustados no se veían.** WordPress no llegó a resolver los
bloques de YouTube y Vimeo de REFERENTES VARIOS, así que en la web salían como
texto plano: ni reproductor, ni enlace en el que pinchar. Ahora son
reproductores de verdad (YouTube en modo `nocookie`).

**La página de VÍDEO mostraba LaTeX en crudo.** Donde debía leerse
`1280 × 720 px` se leía `$1280 \times 720$`. Pasa en las tres resoluciones.

### Ocho enlaces muertos

De los 69 enlaces únicos, ocho ya no responden. Están en las listas que usan
los estudiantes, así que conviene sustituirlos o quitarlos:

| Página | Enlace | Estado |
|---|---|---|
| referentes-varios | `jsc.art/jsc-video-lounge/` | 403 |
| referentes-varios | `unstumm.com/augemented-voyage-ar-vr-platform/` | 404 |
| referentes-varios | `rode.com/blog/all/what-is-ambisonics` | 404 |
| referentes-varios | `arup.com/projects/rewild-our-planet` | 404 |
| referentes-varios | `zoowoman.website/wp/movies/no-intenso-agora/` | no conecta |
| referentes-varios | `es-mx.sennheiser.com/ambeo-abconverter` | no conecta |
| referentes-varios | `davidbowieisreal.com/` | no conecta |
| introduccion | `extracine.com/2013/02/correspondencia-jonas-mekas-j-l-guerin` | 404 |

### Limpieza

El contenido venía pegado desde Word y desde otros editores, con atributos
`data-ccp-*`, `data-path-to-node`, clases `TextRun`/`SCXW` y divs de
maquetación de PDF. Fuera todo: las páginas de SONIDO y VÍDEO adelgazan un 32%
y un 43%.

Se revisaron los 82 enlaces uno a uno: todos son referencias de clase.

### Erratas

En el menú decía **"INTRODUCCIÓN A LAS ÁRTES ELECTRONICAS"**; ahora dice
"ARTES ELECTRÓNICAS". Si prefieres dejarlo como estaba, se cambia en
`src/site.json`.

Quedan otras dos sin tocar, por estar dentro del texto: **"CONTENIDOS
TÉMTAICOS"** (por "TEMÁTICOS") en la página de introducción, y la página de
VÍDEO repite el título "VÍDEO" justo debajo del encabezado.

### Lo que no se trajo

La barra lateral tenía un **buscador** de WordPress. Un sitio estático no puede
buscar en el servidor; en su lugar hay un enlace al sitio principal. Para cinco
páginas no parece que haga falta, pero si lo quieres se puede hacer un filtro
en el navegador —sería útil sobre todo en REFERENTES VARIOS, que tiene más de
cincuenta enlaces.

## Publicar en GitHub Pages

Incluye `.nojekyll`. En *Settings → Pages*, rama `main`, carpeta `/ (root)`.
Para el subdominio, un archivo `CNAME` con `clases.kinolab07.co` y el DNS
apuntando a GitHub Pages.
