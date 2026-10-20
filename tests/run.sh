#!/usr/bin/env bash
# Lance les tests fonctionnels et le balayage des débordements contre dist/ (généré par tools/build.py).
# Usage : bash tests/run.sh            (tout)      bash tests/run.sh sweep   (balayage seul)
set -euo pipefail
cd "$(dirname "$0")/.."
[ -d dist ] || { echo "dist/ absent : lancer d'abord python3 tools/build.py"; exit 1; }
python3 -m http.server 8111 --bind 127.0.0.1 --directory dist >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null || true' EXIT
sleep 1
status=0
if [ "${1:-all}" != "sweep" ]; then python3 tests/test_site.py || status=1; fi
if [ "${1:-all}" != "tests" ]; then python3 tests/sweep.py || status=1; fi
exit $status
