#!/usr/bin/env bash
# Lance les tests fonctionnels et le balayage des débordements contre dist/ (généré par tools/build.py).
# Usage : bash tests/run.sh            (tout)      bash tests/run.sh sweep   (balayage seul)
# Dans GitHub Actions, chaque échec est aussi remonté en annotation (::error::) pour être lisible sans le journal.
set -uo pipefail
cd "$(dirname "$0")/.."
[ -d dist ] || { echo "dist/ absent : lancer d'abord python3 tools/build.py"; exit 1; }
python3 -m http.server 8111 --bind 127.0.0.1 --directory dist >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER 2>/dev/null || true' EXIT
sleep 1
status=0
if [ "${1:-all}" != "sweep" ]; then
  python3 tests/test_site.py > /tmp/tests.log 2>&1 || status=1
  grep -E "^(ok |KO |ÉCHEC|OK   )" /tmp/tests.log | grep -vE "^(ok |OK   )" ; tail -1 /tmp/tests.log
  grep -E "^ÉCHEC" /tmp/tests.log | sed 's/^/::error::/'
  grep -E "Traceback|Error" /tmp/tests.log | head -5 | sed 's/^/::error::/'
fi
if [ "${1:-all}" != "tests" ]; then
  python3 tests/sweep.py > /tmp/sweep.log 2>&1 || status=1
  cat /tmp/sweep.log
  grep -E "cas, ex\." /tmp/sweep.log | sed 's/^/::error::/'
fi
exit $status
