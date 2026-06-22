#!/usr/bin/env bash
# Construye el sitio estático completo en web/public/ :
#   - El sitio (MkDocs Material)         -> public/
#   - El entorno JupyterLite + datos     -> public/lite/
# Solo notebooks del ESTUDIANTE (se excluyen las soluciones).
# Corre en la máquina de desarrollo; la Pi solo sirve el resultado.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
PUBLIC="$HERE/public"
CONTENTS="$HERE/contents"
VENV="$HERE/.buildenv"
PYBOOT="${PYBOOT:-python3}"

echo "==> [1/4] Entorno de build aislado ($VENV)"
if [ ! -d "$VENV" ]; then
  "$PYBOOT" -m venv "$VENV"
fi
"$VENV/bin/pip" install -q --upgrade pip
"$VENV/bin/pip" install -q -r "$HERE/requirements-build.txt"

echo "==> [2/4] Construyendo el sitio (MkDocs) en public/"
rm -rf "$PUBLIC"
( cd "$REPO" && "$VENV/bin/mkdocs" build --strict --site-dir "$PUBLIC" )

echo "==> [3/4] Reuniendo contenidos para JupyterLite (notebooks de estudiante + datos)"
rm -rf "$CONTENTS"; mkdir -p "$CONTENTS"
cd "$REPO"
shopt -s nullglob
for d in P[1-4]-* A[1-8]-* B[1-8]-* C[1-4]-*; do
  [ -d "$d" ] || continue
  mkdir -p "$CONTENTS/$d"
  for f in "$d"/*.ipynb "$d"/*.csv "$d"/*.joblib; do
    [ -e "$f" ] || continue
    case "$(basename "$f")" in
      *solucion*) continue ;;   # NO publicar soluciones
    esac
    cp "$f" "$CONTENTS/$d/"
  done
  # si la carpeta quedó vacía (p. ej. solo tenía soluciones), eliminarla
  rmdir "$CONTENTS/$d" 2>/dev/null || true
done

echo "==> [4/4] Construyendo JupyterLite en public/lite/"
cd "$HERE"
rm -rf "$PUBLIC/lite"
"$VENV/bin/jupyter" lite build \
  --contents "$CONTENTS" \
  --output-dir "$PUBLIC/lite" \
  --lite-dir "$HERE/.lite"

echo
echo "OK. Estático listo en: $PUBLIC"
du -sh "$PUBLIC" 2>/dev/null || true
echo "Notebooks publicados en JupyterLite:"
find "$CONTENTS" -name '*.ipynb' | sed "s#$CONTENTS/#  #" | sort
