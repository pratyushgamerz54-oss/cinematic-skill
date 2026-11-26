#!/bin/bash
# Records the mod 3D pages one at a time (frame-capture), skipping clips that exist.
cd "$(dirname "$0")/.."
REC=../.claude/skills/frame-capture/scripts/record.py
(python3 -m http.server 8767 --directory assets/3d >/dev/null 2>&1 &)
sleep 1
for spec in "sarajevo 40" "carib 24" "dish 16" "sub 24" "bunker 18" "berlin 22"; do
  set -- $spec
  [ -f assets/clips/$1.mp4 ] && continue
  echo "== $1 ($2 s)  $(date +%T)"
  python3 $REC "http://localhost:8767/$1.html" assets/clips/$1.part.mp4 --seconds $2 --fps 30 --size 1920x1080 --ready "window.__ready" --crf 18 2>&1 | tail -2
  [ -s assets/clips/$1.part.mp4 ] && mv assets/clips/$1.part.mp4 assets/clips/$1.mp4
done
echo "== done  $(date +%T)"
