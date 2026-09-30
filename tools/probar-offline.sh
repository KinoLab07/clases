#!/usr/bin/env bash
# Levanta este sitio en local, enlazado con el sitio principal si está al lado.
#
#   ./tools/probar-offline.sh            busca kinolab07 en ../kinolab07-web
#   ./tools/probar-offline.sh /otra/ruta
set -euo pipefail

cd "$(dirname "$0")/.."
CLASES=$(pwd)
PRINCIPAL="${1:-$CLASES/../kinolab07-web}"

echo "Generando en modo local..."
python3 build.py --local

limpiar() {
  echo
  echo "Parando los servidores..."
  kill $(jobs -p) 2>/dev/null || true
  echo "Recuerda: 'python3 build.py' sin --local antes de publicar."
}
trap limpiar EXIT

python3 -m http.server 4709 --directory "$CLASES" >/dev/null 2>&1 &
echo "  clases     ->  http://localhost:4709"

if [ -d "$PRINCIPAL" ]; then
  python3 -m http.server 4707 --directory "$PRINCIPAL" >/dev/null 2>&1 &
  echo "  kinolab07  ->  http://localhost:4707"
fi

sleep 1
echo
echo "Ctrl+C para parar."
wait
