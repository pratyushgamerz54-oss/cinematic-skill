#!/bin/bash
# Download public-domain footage from Wikimedia (retries while it answers 429), keep only the parts we use.
cd "$(dirname "$0")/../assets/footage"
get() { # url out
  for i in 1 2 3 4 5 6 7 8; do
    curl -s -A "cinematic-film/1.0 (documentary research)" -o "$2" "$1"
    if ffprobe -v error "$2" >/dev/null 2>&1; then echo "ok $2"; return 0; fi
    echo "retry $i for $2"; sleep $((60 * i))
  done; return 1; }
get "https://upload.wikimedia.org/wikipedia/commons/b/b9/SR-71_Takeoff_at_Edwards_Air_Force_Base.webm" sr71.webm
get "https://upload.wikimedia.org/wikipedia/commons/3/39/Geological_Earth_Mapping_Experiment_%28GEMx%29_B-roll_%28SVS14728_-_ER-2_Pilot_from_Suit_up_to_Takeoff%29.webm" er2_full.webm && \
  D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 er2_full.webm) && \
  ffmpeg -v error -y -ss $(python3 -c "print(max(0,$D-45))") -i er2_full.webm -vf scale=1920:-2 -c:v libx264 -crf 18 -an er2_takeoff.mp4 && rm -f er2_full.webm && echo "ok er2_takeoff.mp4 (last 45 s)"
