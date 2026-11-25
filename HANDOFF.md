# HANDOFF — read this first in every new session

**Hinglish summary for the user:** Is repo mein ek poora documentary system bana hai. Aap sirf ek topic
bhejenge, to Claude script, awaaz, photos, 3D, map, motion graphics, film, reel, captions aur thumbnails
sab banayega. Aapke saare order neeche aur `CLAUDE.md` mein likhe hain. Pehli film "पिछवाड़े के साँप"
(`saanp/`) taiyaar hai. Iska naya look (mood background, map, normal raftaar, naya reel format) code mein
hai aur test ho chuka hai, bas poora render baaki hai (neeche "Pending" dekhiye).

`CLAUDE.md` is the standing order (rules for every film). This file is the state of the work and the full
list of what the user asked for, in order, so nothing is lost between sessions.
Last updated: 25 Nov 2026. Branch `ccr-f795a8e0-qikje4`.

---

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
