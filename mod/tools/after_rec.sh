#!/bin/bash
# waits for record_all.sh, then renders the HyperFrames graphics
cd "$(dirname "$0")/.."
while pgrep -f record_all.sh >/dev/null; do sleep 20; done
echo "== hyperframes $(date +%T)"
(cd hf && node ../../.claude/skills/hyperframes/scripts/plugin-cli.mjs render --output ../assets/clips/hf_graphics.mp4 2>&1 | grep -v "npm notice" | tail -4)
echo "== done $(date +%T)"
