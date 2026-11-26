#!/bin/bash
# Finish Area 51 after scene.py is final: render, captions, SRTs, share copies, check sheet.
# Run from the repo root:  bash area51/tools/finish.sh      (one heavy job at a time; ~60-90 min in all)
set -u
S=skills/cinematic-film/scripts
P=area51
[ -f $P/out/film_raw.mp4 ] || python3 $S/render.py --project $P --size 1920x1080 --out out/film_raw.mp4 --audio audio/mix.m4a
[ -f $P/reel/out/reel_raw.mp4 ] || python3 $S/render.py --project $P/reel --size 1080x1920 --out out/reel_raw.mp4 --audio audio/mix.m4a
# film: clean captions + SRT; caption-free copy is film_raw itself
python3 $S/burn_captions.py --project $P --video out/film_raw.mp4 --audio audio/mix.m4a --style clean --out out/area51_final.mp4
python3 $S/burn_captions.py --project $P --srt-only --out out/captions.srt
# reel: highlighter captions + SRT
python3 $S/burn_captions.py --project $P/reel --video out/reel_raw.mp4 --audio audio/mix.m4a --style highlighter --out out/area51_reel.mp4
python3 $S/burn_captions.py --project $P/reel --srt-only --out out/captions_reel.srt
# share copies (small enough for git and chat)
ffmpeg -v error -y -i $P/out/area51_final.mp4 -c:v libx264 -crf 30 -tune grain -preset medium -c:a aac -b:a 128k $P/out/area51_final_share.mp4
ffmpeg -v error -y -i $P/out/film_raw.mp4 -c:v libx264 -crf 30 -tune grain -preset medium -c:a aac -b:a 128k $P/out/area51_nocaptions_share.mp4
ffmpeg -v error -y -i $P/reel/out/area51_reel.mp4 -c:v libx264 -crf 28 -tune grain -preset medium -c:a aac -b:a 128k $P/out/area51_reel_share.mp4
cp $P/reel/out/captions_reel.srt $P/out/ 2>/dev/null
# a frame every 10 s of the finished film, for the look-over before sending
ffmpeg -v error -y -i $P/out/area51_final.mp4 -vf "fps=0.1,scale=384:-2,tile=6x9" -frames:v 1 $P/out/check_every_10s.jpg
ls -la $P/out
