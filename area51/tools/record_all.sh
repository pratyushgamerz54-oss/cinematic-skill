#!/bin/bash
# Records the 3D pages and renders the HyperFrames graphics, one heavy job at a time.
cd "$(dirname "$0")/.."
REC=../.claude/skills/frame-capture/scripts/record.py
(python3 -m http.server 8765 --directory assets/3d >/dev/null 2>&1 &)
sleep 1
for spec in "terrain 58" "aircraft 40" "s4 10"; do
  set -- $spec
  [ -f assets/clips/$1.mp4 ] && continue
  echo "== $1 ($2 s)  $(date +%T)"
  python3 $REC "http://localhost:8765/$1.html" assets/clips/$1.mp4 --seconds $2 --fps 30 --size 1920x1080 --ready "window.__ready" --crf 18 2>&1 | tail -3
done
echo "== hyperframes  $(date +%T)"
(cd hf && node ../../.claude/skills/hyperframes/scripts/plugin-cli.mjs render --output ../assets/clips/hf_graphics.mp4 2>&1 | grep -v "npm notice" | tail -4)
echo "== done  $(date +%T)"
