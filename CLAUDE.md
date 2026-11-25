# Standing order for videos in this repo

**First, in every new session, read `HANDOFF.md`**: the state of the work, what is pending, and every
instruction the user has given so far, in order. Keep it up to date: add each new instruction there and
here, and update its "Pending" list when work is done.

The user will often send **only a topic** (in Hinglish or Hindi). That is a request for the full package
below, made with every tool listed here. Do not start a video unless the user asks for one or sends a topic
for one. `saanp/` (पिछवाड़े के साँप) is the finished reference project: copy its patterns.

## What one topic produces

| Deliverable | Spec |
| --- | --- |
| Film | about **5:18** (5 to 5:30), 1920x1080, 30 fps, Hindi narration, Hindi captions burned in |
| Caption-free film + SRT | for YouTube's own captions (burned captions can collide with on-screen quote cards) |
| Reel | about 60 s, 1080x1920, **its own separate script and its own voice recording** (not cut from the film), 9 to 11 lines, **always the fixed reel format** below, large captions |
| Thumbnails | YouTube 1280x720 and reel cover 1080x1920 (`saanp/thumbs.py` is the template) |
| Credits | `credits.md` (images, voice, music, map data, fonts) and `fact_notes` in `script.json` |

## Two scripts, two recordings (user, 25 Nov 2026)

Every topic gets **two separate scripts**: one written only for the YouTube film (`script.json`) and one
written only for the reel (`reel/script.json`, ~720 Hindi characters for ~60 s at Viraj's pace). The reel is
**not cut from the film**: cutting film lines into a reel leaves jumps ("beech mein cut lag ke...
discontinuity"). The reel script is one continuous story that stands on its own (opens on a question, ends on
"आप क्या सोचते हैं?"), the film script is written for YouTube. The user generates the voice for each
separately (film: one file per take; reel: one file `REEL`), so write two voiceover scripts (plain and v3
emotion tags) and send both copyable lists. Reel media may reuse the film's photos, globes and 3D clips.

## YouTube-style intro for the film (user, 25 Nov 2026)

"Isko chalu karo aise jaise YT chalu karta hai": every YouTube film opens with its own take `T00_intro`
before the cold open: (1) a welcome ("नमस्कार दोस्तों, आपका स्वागत है।"), (2) the topic in one or two
lines that tease the story and name it, (3) "तो चलिए, शुरू करते हैं।", then the cold open. The intro has
its **own motion graphic made for it** (HyperFrames: `welcome`, `topic`, `go` in `tut/hf/` are the
template: gold dust and frieze, teaser chips on the words, the subject photo in a cartouche with the title,
a light sweep and the year spinning back into the cold open). The title is shown there, once; no second
title card after the opening question. The reel keeps its own format (it opens on the question, no welcome).

## Real video footage (user, 25 Nov 2026)

"Jarurat pade to video bhi utha sakte ho... kisi bhi line ya scene ke liye... lagna chahiye ke usi scene ke
bare mein hai": when a line or scene is explained better by real moving footage, use a video clip (film and
reel). The clip must show that exact scene, place, person or object, so the viewer feels it is about that
moment, never generic filler. Sources: Wikimedia Commons video (`fetch_commons.py search` finds .webm/.ogv),
public-domain archive film (e.g. US government, NASA, Library of Congress, Internet Archive public-domain
items), always with a free licence; credit each clip in `clips.json` and `credits.md`. Cut it with `trim` in
`clips.json`, grade it like the photos (`grade: "bw"` or `"sepia"` for archive), and play it full-frame with
`screen()` + `into()` or inside the reel window. Label recreations or unrelated stand-ins plainly, or do not
use them; never show victims or militant propaganda.

## The reel format (the same every time: "ek consistent reel banao, na ki kuch bhi")

`saanp/reel/scene.py` is the template; copy it, change only the beats list and the media. Every beat
keeps the same layout, drawn as a screen-fixed overlay with `engine.Hud` so it never moves:
- top: a story-style progress bar (one segment per beat) and the series tag ("<title> · एक जाँच");
- headline: one hook headline per beat in the same place and size, yellow bar; red only for the
  opening and closing questions to the viewer;
- one 16:9 media window with the same frame and red corner ticks on every beat (clip, photo, map or
  document, always inside it), an exhibit tag on its corner ("प्रमाण 01", "प्रतीकात्मक 3D मॉडल",
  "सवाल") and a source line under it;
- bottom quarter: highlighter captions; a mood background per beat (`film.mood`).
Open on the question beat, end on "आप क्या सोचते हैं?". No beat breaks the layout.

## Style: suspenseful, dramatic, thriller, investigative documentary

- Shape: "Investigative documentary" in `skills/cinematic-film/references/story.md`. The YouTube intro
  (`T00_intro`, above), then a cold open on the most
  striking fact, then **a question** (the opening hook), the title, one bridge back in time, then sections
  strictly forward in time, each one an exhibit (a real source) with a stamp or pen mark on the key word.
- **Hooks:** open on a question; a mid-film hook at the end of almost every section ("लेकिन असली झटका...
  अभी बाक़ी था।", "तो क्या कहानी यहीं ख़त्म हो गई? ...नहीं।", "पर एक सवाल बाक़ी था..."); **end on a
  question to the viewer** ("आप क्या सोचते हैं?").
- Dark wall look, red accent, yellow date bars, heartbeat and riser cues on the hooks, a dark drone score.
- **Mix three styles in every film** (user's order): **Archival Documentary Aesthetic** (sepia, grain,
  scratches, flicker, real archive photos and papers), **Investigative Documentary Style** (evidence wall,
  exhibits, stamps, pen marks, red string), **Animated Map Visualization** (2D `GeoMap` with look `intel`:
  borderless land, coast glow, pins, `XMarker` labels, `Route` lines; plus the 3D globe).
- **Background follows the scene and its emotion, never one board for the whole film** (user: "background
  ko scene ya line ya style ke hisaab se... emotion ke hisaab se bhi"; the single cork wall "thoda sa ajeeb
  lag raha hai"). Use `film.mood(t, name)` (engine `MOODS`): `archive` for the past (sepia card + old-film
  effect), `evidence` for exhibits and testimony, `intel` for maps, networks, money trails and agencies,
  `tension` for attacks and hooks, `grief` for victims and loss, `verdict` for the summing up.
  `saanp/scene.py` (the `mood(...)` list before `tidy_keys`) shows a full schedule.
- If a motion graphic is needed, make it (engine items, three.js) or take a free-licensed one from the
  internet (credit it in `credits.md`).
- **Test before the full render:** render a short test (two or three 20 s spans covering different
  moods, `render.py --t0 --t1`), look at it as a viewer would ("kya ye audience ko engage kar payega?"),
  fix what looks odd, and send the test to the user when the look changed.
- Research and fact-check first, with sources in `fact_notes`. Say "लगभग", "आरोप", "के मुताबिक़" where
  sources disagree. On political topics state the other side's denial and its own losses, name
  organisations and officials (never a people), and show no images of victims or militant propaganda.
- Never draw disputed borders (Kashmir and the like): globes use `"borders": false`, skip country-border
  maps of the region, and crop inset maps out of archive images.

## Every film uses all of these

| Need | Tool |
| --- | --- |
| The board, camera, voice timing, sound, captions | `cinematic-film` (`skills/cinematic-film`) |
| 3D globe: flights, great-circle routes, labelled places (look `dark`, `grid: 5`) | `make_globe.py` (three.js) + `frame-capture`, then `prep_clips.py` and `Clip` |
| 3D elements: a building, compound, fort, ship, object (label it "प्रतीकात्मक 3D मॉडल") | three.js page like `saanp/assets/compound/`, or `threejs-scene` / `exploded-view`; check with `site-check`; record with `frame-capture` |
| Motion graphics: the opening question, title card, quote cards, checklists, reveals, closing question | HyperFrames, **used sparingly** (user: "agli baar hyperframe ka jyada use mat karna, lekin motion graphics phir bhi bahut badhiya hone chahiye"): keep it for a few hero graphics (opening question, title, closing question, one or two quote cards) and build the rest as engine motion graphics on the board (word-timed `Card`, `Stamp`, `PenMark`, `StringLine`, `Counter`, `BarChart`, `Timeline`, map pins) or three.js scenes (`saanp/hf/` is the template: one project, one scene per graphic, rendered once and cut with `trim` in `clips.json`) |
| 2D motion graphics on the board | `Timeline`, `Counter`, `BigText`, `Card`, `Stamp`, `PenMark`, `StringLine`, `PaperDoc`, `BarChart` |
| React motion graphics, map flights | Remotion skills, when a Mapbox/Cesium key exists; otherwise the globe |
| AI stills or clips (illustration only, never as evidence) | `motion-assets`, `alpha-cutout` |
| Charts | `dataviz` |

Every section gets at least one moving element beyond the camera (a globe shot, a 3D cutaway, a motion
graphic). Clips go full-frame by `screen()` + `into()` as in `saanp/scene.py`.

## The pipeline (commands as in `saanp/`)

1. **Research and script** (`script.json`): about 66 lines in 9 takes, about **4,600 Hindi characters**
   for ~5:18 at George's pace; numbers in words in `spoken`; `...` for dramatic pauses. Plus a **separate reel script** in `reel/script.json`
   (one take `REEL`, 9 to 11 lines, each with its beat headline, exhibit tag, source line and mood).
   Run `make_beats.py` until it shows 0 warnings.
2. **Stop once for approval:** send `beats.md`, ask (one AskUserQuestion) to approve the script and pick
   the voice. This is the only stop: voice credits are limited. Everything after it runs without asking.
3. **Voice:** ElevenLabs, one take per section. Also write `voiceover_script.md`, an emotion-tag version
   for Eleven v3, and a copyable list in chat if the user records it themselves.
   `split_takes.py` -> `build_narration.py --target 318` (tempo must stay within 0.90 to 1.15).
4. **Images:** Wikimedia Commons via `fetch_commons.py`; if it returns 429, download standard 960px
   thumbnails with curl, 20 s apart, and fill `photos.json` credits by hand. Grade `bw`.
5. **3D and motion graphics:** `globe.json` (+ `--still` checks) -> `make_globe.py`; the 3D model page;
   the HyperFrames project (`lint`, `check`, `snapshot`, `render`); then `prep_clips.py`.
6. **Scene:** `scene.py` from `saanp/scene.py` (sections along a wall, a timeline on top, screens below,
   `tidy_keys` at the end so the camera holds on each hero). Probe one still per line and fix every
   frame that is empty, cut off or on the wrong hero. Then the reel scene from `saanp/reel/scene.py`.
7. **Sound:** `render.py --cues`, `build_sfx.py`, an ElevenLabs sound-generation drone looped and
   cross-faded to the film's length, `mix_soundtrack.py --music`.
8. **Render** (film about 40 to 70 min, reel about 5 min), `burn_captions.py` (clean for the film,
   highlighter for the reel), SRTs, share copies (`-crf 30 -tune grain`), thumbnails. Look at a frame every
   10 s of the finished film before sending. Send the film, reel, caption-free copy, SRT and thumbnails.
9. Commit and push. Files over 100 MB (GitHub's limit) stay out of git: keep them in `.gitignore`.

## What the user decided (keep doing this)

- Liked: the 5:18 cut, the dark thriller look, Hindi labels everywhere, globe shots, quote cards.
- Found worse: a 6:21 version timed to a slow read. Keep films near 5:18 **at the voice's natural pace (1.0x,
  the user chose this over 1.17x)**. If a recorded read runs long, drop whole lines (`film_cut` in
  `saanp/script.json` shows how: guard their visuals with `has(i)`, use `nxt(i)` for clip ends) and cap the
  gaps between lines at 0.6 s; never stretch the film or speed up the voice.
- **Visuals (the user's own words: "visual ki kami hai, bahut jagah ruk jaata hai"):** every line gets its
  own visual that explains it, not text alone. Concretely:
  - **Documentary pace for the camera, a new element on the words:** the camera moves calmly (moves about
    1 s long, gentle push in and drift on holds: `tidy_keys(min_gap=0.6, hold_after=1.8, move=1.0)`, push
    1.035 in `saanp/scene.py`), but inside the held frame **something new lands on the narrator's key
    words**: a label, highlight, stamp, arrow, number, icon, map pin, line on a diagram, a photo sliding in.
    The frame builds up word by word, explainer style, instead of the camera jumping to a new spot. New
    image, clip or graphic every 4 to 6 s. Sound: few whooshes and pops (`saanp/thin_cues.py`). No stretch
    of empty wall or a long static card. (User: "har ek word pe kuch naya aaye elements ya visual... kuch
    jyada hi fast pace aagaya hai, thoda normal karo, documentary hai".) It is a documentary **and an
    explainer**: each visual explains its line and stays on screen long enough to be read.
  - **Many photos:** at least one real archive photo per section, usually two or three (aim for 15 to 20
    in a 5-minute film): people, places, documents, the scene after an event. Search Commons widely
    (e.g. White House, DoD, State Department photos are public domain).
  - **More 3D:** at least three 3D shots beyond the globe: a building or site model, a landscape or
    terrain, vehicles moving on globe routes (`"vehicle": "plane" | "boat"` in `globe.json`).
  - **Motion graphics, not only text:** animated diagrams for the ideas (networks, money trails, targets,
    clocks, counters as figure or dot grids, candles for victims, typed testimony), mostly built on the board with the engine items, timed to the words; HyperFrames only for a few hero graphics.
    Plain title text alone is not a visual.
  - **Never repeat the title card** inside the film; show it once after the opening question.
  - Before rendering, probe one still per line and fix every line that has no clear visual.
- Voice: the user prefers **Viraj** (ElevenLabs library voices "Viraj - Dramatic, Powerful and Epic"
  `CN3wrf4wja2qO5yPhs0E`, "TL10 Aarav - Viraj" `uuyFQegRan8rpIQCGu9K`). The free plan refuses library voices
  over the API (HTTP 402): then use George (`JBFqnCBsd6RMkjVDRZzb`, premade, verified for Hindi,
  `eleven_multilingual_v2`, stability 0.42, style 0.45, `mp3_44100_128`) or let the user generate Viraj on
  the website from the script. Viraj reads about 15% slower than George: a Viraj film needs about 15% fewer
  words (about 3,900 characters) to land near 5:18.
- HyperFrames usage note: the user said yes to sending it.

## Practical notes

- Hindi (Devanagari) is shaped by the engine (and label bars now reach vowel signs below the line). Give
  each project the fonts in `saanp/fonts/` (`cond` Teko, `label`/`labelm` Hind, `serif` Tiro Devanagari
  Hindi, `deva` Noto Sans Devanagari; licences in `saanp/fonts/LICENSES.txt`).
- ElevenLabs: the key is on both the Default and `cinematic-skill` environments. Check credits with
  `/v1/user/subscription` before recording (free plan: 10,000 characters a month).
- Network on `cinematic-skill`: Wikimedia allowed; cdn.jsdelivr.net blocked (use `npm pack world-atlas@2`
  and `npm pack gsap@3.15.0` / `three@0.169.0` for vendored copies).
- Chromium: `/opt/pw-browsers/chromium` (`CHROME_PATH`, `HYPERFRAMES_BROWSER_PATH`; set on the environment).
  WebGL runs in software: a 10 s 1080p globe takes 2 to 5 min; do `--still` checks first.
- HyperFrames CLI: `node .claude/skills/hyperframes/scripts/plugin-cli.mjs <command>` from the project folder.
- Remotion skills are installed by the environment's setup script (their repo has no licence file);
  Remotion maps need the user's Mapbox/MapTiler/Cesium keys.
- `render.py` may print a BrokenPipe trace after "wrote ... .mp4": the file is fine, but chain the next
  command with `;`, not `&&`.
