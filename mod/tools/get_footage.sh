#!/bin/bash
# Slow, patient download of free-licence footage from Wikimedia (it answers 429 often). Accepts a file only if it has a video stream.
cd "$(dirname "$0")/../assets/footage"
isvid() { [ "$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_type -of csv=p=0 "$1" 2>/dev/null)" = "video" ]; }
get() { # path-with-hash name out
  for i in $(seq 1 12); do
    for v in "transcoded/$1/$2.480p.vp9.webm" "transcoded/$1/$2.480p.webm" "transcoded/$1/$2.360p.vp9.webm" "$1"; do
      curl -s -A "cinematic-film/1.0 (documentary research)" -o "$3" "https://upload.wikimedia.org/wikipedia/commons/$v"
      if isvid "$3"; then echo "ok $3 <- $v"; return 0; fi; rm -f "$3"; sleep 20
    done; echo "retry $i $3"; sleep 150
  done; return 1; }
[ -f border1989.webm ] || get "f/fe/Grenz%C3%B6ffnung_November_1989_-_Selmsdorf_%28DDR%29_-_L%C3%BCbeck-Schlutup.webm" "Grenz%C3%B6ffnung_November_1989_-_Selmsdorf_%28DDR%29_-_L%C3%BCbeck-Schlutup.webm" border1989.webm
[ -f brink.webm ] || get "2/2c/To_the_Brink-_JFK_and_the_Cuban_Missile_Crisis.webm" "To_the_Brink-_JFK_and_the_Cuban_Missile_Crisis.webm" brink.webm
