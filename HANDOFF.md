# HANDOFF — read this first in every new session

**Hinglish summary for the user:** Is repo mein ek poora documentary system bana hai. Aap sirf ek topic
bhejenge, to Claude script, awaaz, photos, 3D, map, motion graphics, film, reel, captions aur thumbnails
sab banayega. Aapke saare order neeche aur `CLAUDE.md` mein likhe hain. Pehli film "पिछवाड़े के साँप"
(`saanp/`) taiyaar hai. Iska naya look (mood background, map, normal raftaar, naya reel format) code mein
hai aur test ho chuka hai, bas poora render baaki hai (neeche "Pending" dekhiye).

`CLAUDE.md` is the standing order (rules for every film). This file is the state of the work and the full
list of what the user asked for, in order, so nothing is lost between sessions.
Last updated: 26 Nov 2026. All work is on `main` (the user asked for it, so new sessions see everything); session branches start from it.

---

## NOW (26 Nov 2026): where the work stands, and how to continue

**Area 51 (`area51/`) is the newest and most complete reference.** Everything up to the final render is built and
committed: scripts (approved), voice (split), all assets, `scene.py`, `reel/scene.py`, sound mixes.
The final 1080p render was running when the session ended. **To finish it, a new session runs one command:**

    bash area51/tools/finish.sh

It renders the film (skips if `area51/out/film_raw.mp4` exists) and the reel, burns captions (film: clean;
reel: highlighter), writes both SRTs, makes the share copies (`*_share.mp4`, the only mp4s in git) and a
check sheet `area51/out/check_every_10s.jpg` (look at it before sending). Then send to the user: film with captions,
caption-free copy, `captions.srt`, reel + `captions_reel.srt`, `out/thumbnail_youtube.jpg`, `out/thumbnail_reel.jpg`.
Commit and push (files over 100 MB stay out: `out/*.mp4` is ignored except `*_share.mp4`).

**A new topic from the user = start the full package at once**, following the playbook below (copy `area51/`).

## PLAYBOOK: the exact order that worked for Area 51 (copy it for every topic)

1. **Research** with WebSearch (sources into `fact_notes`; say आरोप / के मुताबिक़ / दावा; give both sides).
2. **Film script** `script.json` (T00_intro + takes; length as the user asks; ≈ 11.4 Hindi characters/s at Viraj's pace,
   gaps included: 5:18 ≈ 3,800, 8 min ≈ 5,500). Open with curiosity questions, hooks before/at/after the middle and at
   the end. Generate it with a small Python script (spoken text with `...`, display text derived; see the area51
   history). **Reel script** `reel/script.json` (10 lines, ~720-760 chars, headline/tag/source/mood per line).
   `make_beats.py --project <p>` and `--project <p>/reel` until 0 warnings (split lines over ~22 words; never type and
   speak the same phrase).
3. **The one stop:** send both beats.md + `voiceover_script_emotions.md`, give one copyable v3 block per take
   (no line numbers inside the blocks), AskUserQuestion to approve. The user records Viraj on the website; one
   generation takes ~2,000-2,300 characters, so per-take files are best (they sent T00..T11 + REEL for Area 51).
4. **While waiting for the voice** (all of it, in this order; run heavy jobs one at a time):
   - photos.json (25+ Commons; per-photo `"grade": "natural"` for colour photos, `"crop"` to remove private people),
     `fetch_commons.py get --project <p> --pause 8` in the background (Commons 429s: it retries; a PDF page:
     `.../thumb/<a>/<ab>/<name>.pdf/page1-960px-<name>.pdf.jpg`).
   - globe.json (look dark, borders false, `"atmosphere"` and `"grid_rgb"` overrides for the topic palette), `--still`
     checks, then `make_globe.py` in the background.
   - 3D pages in `assets/3d/` (copy area51's `common.js`, `terrain.html`, `aircraft.html`, `s4.html`): check with
     `node tools/stills.js <url> <prefix> t1 t2 ...` (served by `python3 -m http.server 8765 --directory assets/3d`),
     then record all with `tools/record_all.sh` (frame-capture record.py, then the HyperFrames render).
   - **Real terrain**: `tools/make_terrain.py` (AWS Terrain Tiles, open data; s3.amazonaws.com works) gives height +
     coloured relief; the three.js terrain page drapes pins, routes, zones and labels on it.
   - HyperFrames hero graphics from `hf/gen.py` (one Python generator writes all compositions + index + segments):
     `plugin-cli.mjs lint`, `snapshot --at ...`, `render --output ../assets/clips/hf_graphics.mp4`.
   - Footage: Wikimedia refuses video originals (429); download the transcode
     `https://upload.wikimedia.org/wikipedia/commons/transcoded/<a>/<ab>/<name>/<name>.480p.vp9.webm` (or 1080p),
     trim with ffmpeg; label stand-ins plainly (e.g. "SR-71 · A-12 परिवार (NASA फ़ुटेज)").
   - clips.json (every clip, trims for the shots), credits.md (`fetch_commons.py credits` + clips, data, fonts),
     thumbs.py (copy area51's).
5. **Voice:** put takes in `audio/takes/<take>.wav` (reel: `reel/audio/takes/REEL.wav`), `split_takes.py`, set
   `gap_after` 0.45 (0.6 at take ends) in segments.json, `build_narration.py` (natural 1.0x). Too long: drop whole
   lines by deleting them from segments.json and record it in `film_cut` / `reel_cut`.
6. **Scene:** copy `area51/scene.py` (helpers photo/card/bar/tag/screen/into/cut(until=)/look, mood list, chips,
   tidy_keys). `prep_assets.py` and `prep_clips.py` first. Probe one still per line (times = segment middles from
   audio/timing.json), build contact sheets, fix, re-probe; `--strip t0:t1:8` to debug a line.
   **Lessons:** give each section enough room (sections were colliding; area51 XS spacing ~26-40k); a cutaway's
   last camera key must come before the next line's first key (into ends `nxt(i) - 0.5`); use `cut(..., until=t)` when
   a line goes on to another visual; GeoMap K is per radian (K≈24000 for a 20° map); flat 2D maps of an inland spot
   read as blank: use a motion graphic or the 3D terrain instead.
7. **Test** three 20 s spans (`render.py --t0 --t1 --size 1280x720 --out out/test_<t>.mp4 --audio audio/mix.m4a`,
   about 45 s each) and look at a frame every 2 s.
8. **Sound:** `render.py --cues` -> `saanp/thin_cues.py <p>/sfx_cues.json` -> `build_sfx.py` -> score (area51 built it
   from saanp's drone1/drone2 alternated with 4 s cross-fades, see the history) -> `mix_soundtrack.py --music
   audio/music/score.wav --music-db -4 --sfx-db -3 --duck-ratio 3 --duck-threshold 0.03 --music-level 0.07
   --music-eq-dip 4 --lufs -15`. Same for the reel with `--music ../audio/music/score.wav`.
9. **Render and finish:** `tools/finish.sh` (film 1080p took about 30-40 min for 8:39; the reel a few minutes).
10. Keep HANDOFF.md, CLAUDE.md and `NEW_SESSION.md` up to date; commit and push after every stage.

---

## 0. How a new session starts (the whole workflow in one place)

1. Read this file and `CLAUDE.md`. The user sends only a topic (or pastes the block in `NEW_SESSION.md` with a
   topic). That means the full package, made the way `tut/` was made (the newest reference; `saanp/` the first).
2. Research → `script.json` (T00_intro + 50 story lines in T01..T09, ~3,800 characters) and the separate
   `reel/script.json` (9-11 lines, ~720 characters) → `make_beats.py` for both until 0 warnings.
3. The one stop: send both `beats.md`, ask (one AskUserQuestion) to approve. The user records the voice
   themselves on the ElevenLabs website with Viraj: give **one copyable block per file** (T00_intro, T01..T09,
   REEL) with Eleven v3 emotion tags, plus `voiceover_script.md` and `voiceover_script_emotions.md`.
4. While waiting for the voice, build everything that does not need it: photos, globes, map, 3D pages,
   HyperFrames (intro welcome/topic/go, qopen, quote card, qend, reel question), thumbnails, and real
   scene-matched video footage where it explains a line.
5. The user may send the voice as three files (tut did): Greeting (= T00_intro), the whole story in one
   file, and Reel. Split the story as one take: make `audio/_split/` with a script.json of two takes
   (T00_intro, STORY), run `split_takes.py --project audio/_split`, copy `lines/` and fix `segments.json`
   (scene names, gaps 0.45, 0.6 at take ends). Never speed up; drop whole lines (`film_cut`, `reel_cut`).
6. `scene.py` from `tut/scene.py`, reel from `tut/reel/scene.py` (symlink `reel/assets -> ../assets`), probe
   every line, test spans, sound (cues → `saanp/thin_cues.py` → `build_sfx.py` → score from
   `saanp/audio/music/drone1.mp3` + `drone2.mp3` cross-faded to the length → `mix_soundtrack.py`), render,
   captions, SRT, share copies, look at a frame every 10 s, send, commit and push.
7. A fresh container may lack libEGL (skia) and Python Playwright: the "animation-studio" environment has a
   setup script for them; if they are still missing, `apt-get install -y libegl1 libgl1 libgles2` and
   `pip install playwright -r requirements.txt`.

## 1. What exists (built and committed)

### Skills installed in this repo (`.claude/skills/`, they work together with `cinematic-film`)
- `cinematic-film` (`skills/cinematic-film`): the main engine. It handles the board, the camera, voice timing,
  sound effects, captions and the render.
- HyperFrames: `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`,
  `remotion-to-hyperframes`, `reverse-any-video`, `slideshow`, `style-sampling`, `figma`. These are HTML to video
  motion graphics. CLI: `node .claude/skills/hyperframes/scripts/plugin-cli.mjs <cmd>`.
- 3D / web: `threejs-scene`, `exploded-view`, `frame-capture` (records a page to MP4), `site-check`.
- AI assets: `motion-assets`, `alpha-cutout`. Charts: `dataviz`.
- Remotion skills: the environment's setup script installs them. Maps need a Mapbox, MapTiler or Cesium key,
  which the user has not given, so we use the 3D globe and the 2D GeoMap instead.

### Engine features added in `skills/cinematic-film/scripts/engine.py`
- **Devanagari shaping:** Hindi renders correctly. Vowel signs below the line are not clipped, and word
  timing counts Hindi letters.
- **New items:** `Clip` (a video inside the world), `Timeline`, `BarChart`, and `Hud`.
  - `Hud` is a screen-fixed overlay. The reel format uses it.
- **Moods:** `film.mood(t, name, fade)` with `MOODS`. The background board and the film finish cross-fade by
  scene and emotion:
  - `evidence`: cork evidence wall.
  - `archive`: sepia card plus an old-film effect (sepia, flicker, gate weave, scratches, dust).
  - `intel`: navy with a grid.
  - `tension`: red-black.
  - `grief`: cold blue-black, desaturated.
  - `verdict`: charcoal.
  - Textures are made by `prep_assets.py`: `archive.png`, `intel.png`, `tension.png`, `grief.png`.
- **Animated 2D map:** `GeoMap(..., look="intel")`.
  - It shows borderless land only (all countries merged with PathOps union), so no disputed border is ever
    drawn.
  - It has a cyan coast glow and a grid. Add `MapPin`, `XMarker` and `Route` on top.
  - The data comes from `make_map.py` with `map.json` (see `saanp/map.json`). The source is world-atlas
    `countries-50m.json`, kept in `saanp/assets/data/`.
- **3D globe:** `make_globe.py` plus `assets/globe/globe.js` (three.js).
  - Looks: `dark`, `night`, `board`. Options: `borders: false`, `grid`, labels.
  - Route vehicles: `"vehicle": "plane" | "boat"` and `vehicle_hold`.
  - Use `--still` for checks.
- Other scripts:
  - `prep_clips.py`: clips, with `trim` support in `clips.json`.
  - `fetch_commons.py`: standard thumbnail widths, and it reports failures.
  - `captions.py`: captions scale for vertical video.

### The reference film `saanp/` — "पिछवाड़े के साँप" (how Pakistan's state is accused of using terror proxies)
- **Script:** `saanp/script.json`.
  - 66 lines in 9 takes, with `fact_notes` (sources), `reel.lines` and `film_cut`.
  - `film_cut` drops lines 15, 24, 29, 37, 38, 46 and 50 to fit the Viraj read at 1.0x.
- **Voice:**
  - The user generated **Viraj** on the ElevenLabs website, saved as `saanp/audio/viraj_full.mp3`.
  - It is split into `audio/lines_viraj` (`audio/lines` is a symlink to it).
  - The George backup is in `audio/lines_george` and `audio/george_backup/`.
  - Timing: `audio/timing.json`, 327.0 s at tempo 1.0, gaps capped at 0.6 s.
- **Images:** 16 Wikimedia Commons photos in `photos.json`, credited in `credits.md`.
  - P01 is the CIA aerial, cropped to remove an inset map.
  - The rest cover the Situation Room, Reagan 1983, the Soviet withdrawal, Kakul, the Kandahar airport, the CST
    bullet marks, APS Peshawar, Baisaran, Mullen, Clinton, Imran Khan and Khawaja Asif.
- **3D:**
  - Globes: `g_abbottabad`, `g_roots`, `g_ic814` (a plane on the route), `g_mumbai` (a boat), `g_pahalgam`,
    `g_verdict`.
  - Compound model: `assets/compound/`.
  - Baisaran valley: `assets/valley/`.
- **HyperFrames:**
  - `hf/`: qopen, title, proxy, mullen, clinton, fatf, mask, asif, qend.
  - `hf2/` (made by `gen_set2.py`): target, letnet, hours, headley, turn, money, forty, many, candles.
  - Line 14 no longer uses `hf2_letnet`; the 2D map replaced it.
- **Scene:** `saanp/scene.py`. Current state:
  - Sections along a wall, with a timeline on top and screens below.
  - Calm camera: `tidy_keys(min_gap=0.6, hold_after=1.8, move=1.0)`, push 1.035, and a fix that drops keys
    which made the camera swing back and forth.
  - **Word chips:** short explaining labels that land on key words, in a screen corner, through the `chip(...)`
    list.
  - **Mood schedule:** the `mood(...)` list before `tidy_keys`.
  - **2D map** at line 14 (LeT headquarters, Muridke).
  - The title card appears once only.
  - Every line has a visual.
- **Sound:**
  - `render.py --cues`, then `thin_cues.py` (fewer whooshes and pops), then `build_sfx.py`.
  - Then `mix_soundtrack.py --music audio/music/score.wav`. The score is an ElevenLabs drone, 385 s.
- **Reel:** `saanp/reel/scene.py` is now the **fixed reel format**.
  - It uses `Hud`: progress bar, series tag, headline, 16:9 window, exhibit tag, source line and mood per beat.
  - 9 beats from lines 5, 3, 4, 19, 41, 32, 35, 57+58 and 66, about 59 s.
- **Thumbnails:** `saanp/thumbs.py` writes `out/thumbnail_youtube.jpg` and `out/thumbnail_reel.jpg`.

### What the user has already received
- Film `out/pichhwade_ke_saanp_final.mp4` (5:27, captions), the caption-free copy (not in git, it is over
  100 MB), `captions.srt`, the reel `pichhwade_ke_saanp_reel.mp4` with `captions_reel.srt`, and both
  thumbnails.
  - **This is the older, fast-paced look, from before the moods, the map, the calm camera and the new reel
    format.**
- The mood test `out/mood_test_share.mp4` with `mood_test_stills.jpg`. The user said: **"Ha badhiya"**.
- The reel format preview `out/reel_format_preview.jpg`.

## 2. Pending

### mod/ — पाँच पल, जिन्होंने दुनिया बदल दी (new topic, 26 Nov 2026; series "World-Changing Turning Points")
- The user asked for the theme "World-Changing Turning Points", **about 4 min, timed to their recording**, informative
  mystery thriller, curiosity questions first, hooks at the start, before the middle, the middle, before the end and
  the end; separate reel and film scripts; "pura kaccha chittha"; **3D-style map animation** (colourful internet maps,
  2D fine too); **3D is a must**; real video where it explains. They chose **five turning points in one film**
  (asked 26 Nov). Chosen, all "a small slip or a single decision": Sarajevo 1914 (wrong turn), Fleming 1928 (open
  plate), Arkhipov 1962 (the third "no" on B-59), Petrov 1983 (false alarm, sunlight on clouds), Schabowski 1989
  (the note, "sofort"). Cold open in the 1983 bunker, then back to 1914 and forward.
- Scripts are generated by `mod/tools/gen_script.py` (edit the lists there, rerun, then `make_beats.py`): film 38 lines
  in T00_intro + T01..T07, 2,916 characters (~4:15 at Viraj's pace); reel 10 lines, 726 characters (~64 s). Both
  beats.md 0 warnings. `voiceover_script.md` and `voiceover_script_emotions.md` written. **Waiting for approval.**
- After approval (no more stops): photos (Sarajevo 1914 film/photos, Princip, the car in Vienna, Fleming, culture
  plate, 1940s production, U-2 Cuba photo, B-59 surfaced (US Navy), Arkhipov, Petrov, Schabowski (Bundesarchiv),
  wall 1989), footage (1914 Sarajevo film, Berlin Wall 1989), globes (Moscow bunker, Sarajevo→London, Caribbean,
  Oko satellite, verdict), 3D pages (Sarajevo 3D map with the wrong turn, petri dish, B-59 underwater + cutaway,
  bunker console, Berlin 3D map), HyperFrames only intro + one quote card + qend + reel question, thumbnails.

### area51/ — एरिया 51 (new topic, 25 Nov 2026)
- Script `area51/script.json`: T00_intro (6 lines: welcome, three curiosity questions, title, go) + 63
  story lines in T01..T11, about 5,630 characters, about 8:15 at Viraj's pace (user: total about 8 min,
  timed to their recording). `fact_notes` hold the sources. Reel `area51/reel/script.json`: 10 lines, 756
  characters. Both `beats.md` have 0 warnings. `voiceover_script.md` and `voiceover_script_emotions.md` written.
- Approved by the user (25 Nov 2026). **Waiting for the voice** (Viraj, recorded by the user in parts, see 18c).
- Done before the voice: 26 Commons photos (`photos.json`, per-photo "grade"; P04 cropped to the signs), 5 globes
  (teal palette), 3D terrain map `assets/3d/terrain.html` (8 shots, 58 s), `aircraft.html` (U-2, A-12, HAVE BLUE,
  40 s), `s4.html` (claim, 10 s), HyperFrames `hf/` (gen.py: welcome, topic, go, qopen, haines, aaro, qend, rq; 73 s),
  NASA footage (SR-71 take-off, ER-2 take-off), `clips.json` (all of them, cut by trim), `credits.md`, `thumbs.py`.
  Wikimedia 429s video originals: use the `transcoded/.../<name>.480p.vp9.webm` (or 1080p) copies instead.
- **Voice arrived (26 Nov 2026)** as one file per take (Greeting = T00_intro, T01..T11) + REEL. Split with 0 flagged;
  natural pace 1.0x: film **8:39** with gaps 0.45/0.6 s, no line dropped (user: length follows the recording);
  reel 69 s -> line 3 dropped (`reel_cut`) -> **63 s**.
- New engine features (skills/cinematic-film): moods **`radar`** (night teal; hooks without red) and **`desert`**
  (dusk amber), textures radar.png/desert.png in prep_assets.py; **`Atmos(film)`**: a moving screen-space background
  layer (dust, stars, snow, light sweep, radar rings) coloured by the current mood; per-photo `"grade"` in photos.json.
- `area51/scene.py` (12 sections, screens below, cut() helper with `until=` for lines that go on to another visual;
  into() ends 0.5 s before the next line so tidy_keys keeps the order), `area51/reel/scene.py` (fixed format, teal
  progress bar). All 69 lines probed; test spans 40-60, 100-120, 380-400 s looked right. Sound: cues -> thin_cues ->
  build_sfx; score = drone1/drone2 alternated with 4 s cross-fades to 525 s; mixes at -15 LUFS.
- Original plan, before the voice: Commons photos (15-20), globe, a 3D-style tilted map and a 3D terrain map of
  Groom Lake (colourful NASA/USGS imagery), 3D models (the base with runway and hangars, U-2, A-12,
  Have Blue, the S-4 hangar in the mountain), real public-domain footage (U-2, A-12/SR-71 take-offs),
  a few HyperFrames graphics only (intro welcome/topic/go, qopen, two quote cards, qend, reel question),
  thumbnails. Palette with less red (desert amber, night blue, radar green).


### tut/ — तूतनख़ामुन (new topic, 25 Nov 2026)
- Script `tut/script.json` (film, **50 lines**: the user asked for 50, about 5:10 at Viraj's pace) and
  `tut/reel/script.json` (reel, separate script, 10 lines, about 64 s). Beats and voiceover scripts
  (`tut/voiceover_script.md`, `tut/voiceover_script_emotions.md`) sent. The user approved and is
  **generating the voice themselves** (film takes T01..T09, reel `REEL`).
- Done before the voice (user: "upar wale kaam suru kar do"):
  - Photos: `tut/photos.json`, 22 Commons entries (Carter, Carnarvon, mask, Akhenaten, Aten relief, Restoration
    Stela, throne panel, Ay, Horemheb, KV62 wall, Abydos list, valley, Burton 1922-24 photos, coffin, dagger,
    KV62 today, mask 2025). `fetch_commons.py get --project . --pause 20` fills the rest when Commons stops
    answering 429 (run it again until every entry has a file).
  - Globes (`tut/globe.json`): g_luxor (descent), g_carnarvon (boat England → Egypt → Luxor), g_verdict (Luxor → Giza).
  - 2D map `tut/map.json` (Egypt: Thebes, Amarna, Abydos, Akhmim, Memphis, Giza).
  - 3D pages `tut/assets/3d/` (shared `common.js`): `tomb.html` (0-6 s sealed door + candle = clip `door`,
    6-15 s KV62 cutaway = clip `tomb`), `coffins.html`, `valley.html` (KV9 debris buries KV62), `ctscan.html`
    (symbolic scan, not the mummy). Recorded to `assets/clips/*.mp4`.
  - HyperFrames `tut/hf/`: welcome, topic, go (the YouTube intro, T00_intro), qopen, wonder (quote card), qend, rq (reel opening question) → `hf_graphics.mp4`, cut by `trim` in `clips.json`. The old `title` card is no longer used (the intro carries the title).
  - Thumbnails: `tut/thumbs.py` → `tut/out/thumbnail_youtube.jpg`, `thumbnail_reel.jpg`.
- Voice arrived (25 Nov 2026): `audio/original/Greeting.mp3` (T00_intro), `whole_yt_video.mp3` (T01..T09 in one
  file, split as one take STORY via `audio/_split/`), `reel/audio/original_Reel.mp3`. All 54 + 10 lines split with
  0 flagged. Natural pace 1.0x: film 5:44 → dropped lines 11, 30, 52 (`film_cut`) → **5:27**; reel 68 s → dropped
  line 9 (`reel_cut`, gaps 0.3 s) → **62.7 s**.
- `tut/scene.py` (film) and `tut/reel/scene.py` (fixed reel format) written, probed line by line, test spans
  rendered (0-20, 60-82, 296-326 s). Sound: cues thinned, sfx built, score = saanp's ElevenLabs drones
  (drone1/drone2) cross-faded to 340 s; mixes at -15 LUFS.
- Final render chain: /tmp script `final.sh` (film 1080p → clean captions → SRT → share copies → reel 1080x1920
  → highlighter captions → SRT → share). Outputs in `tut/out/` and `tut/reel/out/`.
- Still to do after the render: look at a frame every 10 s, send film, caption-free copy, SRTs, reel, thumbnails.
- Environment "animation-studio" now has a setup script (libEGL for skia, Python Playwright, requirements):
  a fresh container lacked them.

### saanp/ (do this if the user says go)
1. Probe one still per line of `saanp/scene.py` and fix anything empty or cut off.
   - Known small issues: about 0.5 s of empty sepia wall just before line 11's "प्रॉक्सी वॉर"; the grief mood
     at Peshawar could read more blue.
2. Regenerate the sound for the film: `render.py --cues`, then `thin_cues.py saanp/sfx_cues.json`, then
   `build_sfx.py`, then `mix_soundtrack.py --music audio/music/score.wav`.
3. Render the film: `render.py --project saanp --size 1920x1080 --out out/film_raw.mp4 --audio audio/mix.m4a --workers 3`.
   - It takes about 36 min.
   - Run one heavy job at a time: two ffmpeg/render jobs together were killed for lack of memory.
4. Burn captions with `burn_captions.py --style clean` (about 25 min), then write the SRT.
5. Make the share copies (`-crf 30 -tune grain`): one with captions, one caption-free.
6. Render the reel:
   - `render.py --cues` and `build_sfx.py` for `saanp/reel`.
   - `mix_soundtrack.py --project saanp/reel --music ../audio/music/score.wav`.
   - Render at 1080x1920 (about 10 min).
   - Burn captions with `--style highlighter`, write the SRT, make the share copy.
7. Check a frame every 10 s. Send the film, reel, caption-free copy, SRTs and thumbnails. Commit and push
   (keep files over 100 MB out of git).

## 3. Every instruction the user gave, in order (all still apply unless replaced)
1. Install the cinematic-skill repo, its requirements and setup scripts.
2. Install skills for documentary style, investigation style, 3D elements, 2D and 3D motion graphics, map
   animation and all kinds of animation, plus anything else needed for a better documentary. They must work
   together with cinematic-film.
   - **Install only, do not make a video then.**
   - Remotion and HyperFrames were also asked for: "Hyperframe ka use karna motion graphics ke liye bhi".
3. Save everything so a new session uses all of it. **The user will send only a topic; that means the full
   video.**
4. The first film: how Pakistan promotes terrorism.
   - Hindi, 1920x1080, about 5 min, plus a reel of about 1 min.
   - Hooks at the start, the middle and the end.
   - **Start with a question and end with a question.**
   - Suspenseful, dramatic, thriller, engaging, with hooks throughout for view duration.
   - Connect ElevenLabs.
   - Make thumbnails at the end.
5. Voice:
   - Viraj, or the best narrator available.
   - The user generated Viraj on the website themselves (the free plan returns 402 on library voices).
   - They asked for the voiceover lines as a copyable list, with emotion tags between lines, in at most
     50-line batches.
6. **Never speed up the audio.**
   - The user chose 1.0x over 1.17x.
   - A 6:21 version looked bad; they want about **5:18**. Fit it by dropping lines, never by stretching.
7. "visual ki kami hai, bahut jagah ruk jaata hai": more visuals.
   - A visual on every line, many photos, 3D models and motion graphics, not just text.
   - **Do not keep showing the title "पिछवाड़े के साँप"** (once only).
8. "har ek word pe kuch naya aaye elements ya visual... kuch jyada hi fast pace aagaya hai, thoda normal
   karo, documentary hai". It is also an **explainer**:
   - Calm documentary camera.
   - New elements land on the key words inside the frame.
   - Each visual explains its line and stays long enough to read.
9. "agli baar hyperframe ka jyada use mat karna, lekin motion graphics phir bhi bahut badhiya hone chahiye":
   - HyperFrames only for a few hero graphics.
   - Build the rest with engine items, maps and three.js.
10. "background ko scene ya line ya style ke hisaab se... emotion ke hisaab se bhi" (the single background
    looked "ajeeb"):
    - Mood backgrounds.
    - Mix the **Archival Documentary Aesthetic**, the **Investigative Documentary Style** and **Animated Map
      Visualization**.
    - Make or download motion graphics when needed.
    - **Test first** whether it will engage the audience.
    - Follow all the earlier orders.
11. Reel: "ek format do, bhale ek mint ka banao lekin ek consistent reel banao, na ki kuch bhi". Always the
    fixed reel format (`saanp/reel/scene.py`).
12. "ye sab jo maine bola hai wo bhi save karte jaao": keep saving every new instruction to `CLAUDE.md` and
    to this file.
13. (25 Nov 2026) **Two scripts per topic: one for the reel, one for the long video, each voiced separately**
    by the user, so neither has breaks in continuity (a reel cut from the MP4 "beech mein cut lag ke...
    discontinuity" lagta hai). The reel script should feel made only for reels, the film only for YouTube.
14. (25 Nov 2026) Next topic: **Tutankhamun**, a history documentary and explainer (`tut/`).
15. (25 Nov 2026) The film script stays at **50 story lines** ("ab sirf 50 line ki kar do"); the user
    generates the voice themselves and wants **one copyable block per file** ("single single karo").
16. (25 Nov 2026) **Start the film like a YouTube video**: welcome, then the topic, then "चलिए शुरू करते
    हैं", then the story, with **a separate motion graphic made for this intro** (`T00_intro`; HyperFrames
    `welcome`, `topic`, `go`). See `CLAUDE.md`.
17. (25 Nov 2026) **Use real video footage when needed**, for any line or scene, to explain it; it must look
    like it is about that very scene ("lagna chahiye ke usi scene ke bare mein hai"). Save it and use it from
    the next film on. See `CLAUDE.md` ("Real video footage").
18. (25 Nov 2026) The new-session block (`NEW_SESSION.md`) is the standing brief: T00_intro + 50 story lines
    (~3,700-3,900 characters), a separate reel (9-11 lines, ~720 characters), one stop for approval with one
    copyable v3 block per file, 15-20 photos, globe, 2D map, **at least 3-4 3D models**, HyperFrames hero
    graphics only, voice possibly as Greeting + whole story + Reel, 1.0x always, gaps 0.45-0.6 s.

18b. (25 Nov 2026) Topic **Area 51** (`area51/`): total about **8 min**, timed to the user's own recording;
    mystery, suspense, thriller; **first questions to build curiosity, not explaining at once**; hooks at the
    start, before the middle, the middle and the end; separate reel and film scripts; "pura kaccha chittha";
    a **3D-style map animation** and colourful maps from the internet (2D is fine too); **less red**,
    palette by topic; **more engaging backgrounds** for retention; motion graphics may come from the
    internet; **HyperFrames very little**. See `CLAUDE.md` ("Area 51 orders").

18c. (25 Nov 2026) One ElevenLabs generation cannot take 50 lines ("ek baar me 50 line na ayegi"): the Area 51
    story comes as **several MP3s**; join them in order and split as one story take. Suggested parts (with tags):
    A = T01-T03 (lines 7-25, ~2,240 chars), B = T04-T06 (26-44, ~2,160), C = T07-T09 (45-59, ~1,810),
    D = T10-T11 (60-69, ~1,250); Greeting (~635) and Reel separate. If even that is too long, one file per take.

18d. (26 Nov 2026) Topic **World-Changing Turning Points** (`mod/`): about **4 min, length follows the user's
    recording** ("pehle main audio bhejunga, jitna der ka hoga uske hisaab se"); informative mystery suspense thriller;
    questions first, hooks at start / before the middle / middle / end; separate reel and film scripts; pura kaccha
    chittha; **3D-style 2D map animation** (colourful from the internet if possible, plain 2D fine); **3D must be
    used** ("uske bina samajh nahi aayega"); real video where available. User picked **5 turning points in one film**.

## 4. Environment notes (cloud environment "cinematic-skill")
- **ElevenLabs:** the key is injected by the proxy, so send `xi-api-key: dummy`.
  - Free plan: 10,000 characters a month. Check `/v1/user/subscription` before recording.
  - Use `mp3_44100_128`.
- **Hosts:** Wikimedia is allowed. Commons often returns 429: download 960px thumbnails 20 s apart and fill the
  credits by hand. `cdn.jsdelivr.net` is blocked: use `npm pack` for gsap, three and world-atlas.
- **Chromium:** `/opt/pw-browsers/chromium`. WebGL runs in software, so it is slow.
- **render.py:** it may print a BrokenPipe after "wrote", but the file is fine. Chain commands with `;`.
- **Memory:** one render or encode at a time. Splicing patches works by encoding pieces separately and then
  joining them with the concat demuxer (`-map 0:v`).
