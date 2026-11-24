# Standing order for videos in this repo

When the user asks for a video or documentary, make it with **all of these together**, not only the
2D board. Do not start a video unless the user asks for one.

## Style: documentary + investigation, mixed

- Use the "Investigative documentary" shape in `skills/cinematic-film/references/story.md`: a cold open
  that states the outcome, the question, a bridge back in time, exhibits (real sources as evidence,
  labelled `सबूत 1` / `EXHIBIT A`, with stamps and pen marks on the key word), strings tying exhibits to
  places, the turn, and a verdict with the whole board in the final pull-back.
- Research and fact-check first; keep sources in `fact_notes`; say "about", "reported" or "according to"
  where sources disagree.

## Every film uses

| Need | Skill / tool |
| --- | --- |
| The film itself: board, camera, voice timing, sound, captions | `cinematic-film` (`skills/cinematic-film`) |
| 2D map animation: country fills, routes, markers | `make_map.py` + `GeoMap`, `RegionFill`, `Route`, `XMarker` |
| 3D map animation: globe flights, great-circle routes, labelled places | `make_globe.py` (three.js) + `frame-capture`, then `prep_clips.py` and `Clip` |
| 3D elements: places, forts, battlefields, ships, objects | `threejs-scene` (and `exploded-view` for cutaways), checked with `site-check`, recorded with `frame-capture`, placed as `Clip` |
| 2D motion graphics | `Timeline`, `BarChart`, `Counter`, `BigText`, `Card`, `PenMark`, `Stamp`, `StringLine` |
| 3D / web motion graphics (GSAP, CSS, canvas) | any page recorded with `frame-capture`, placed as `Clip` |
| AI stills and clips (only for illustration, never as evidence) | `motion-assets`; `alpha-cutout` to key a subject out for a transparent cut-out |
| Charts and data colours | `dataviz` |
| HTML motion graphics: titles, kinetic type, lower thirds, charts, map overlays, transitions, 3D blocks (about 450 ready-made blocks) | HyperFrames skills (`hyperframes` first, then `hyperframes-registry`, `hyperframes-cli`, `media-use`, `style-sampling` e.g. "3D True Crime"): render to MP4, then place it as a `Clip` |
| React motion graphics, kinetic type, animated captions, 2D/3D scenes, map flights (MapLibre, Cesium terrain) | Remotion skills (`remotion-best-practices` routes to the rest; `remotion-maps`, `remotion-markup`, `remotion-captions`, `remotion-render`): render a Remotion composition to MP4, then place it as a `Clip` |

Aim for every section of the film to have at least one moving element beyond the camera: a 3D shot,
a map animation, a motion graphic or a clip. Keep rule 1 of the skill: one hero per line.

## Practical notes

- Language: the user writes in Hinglish and usually wants Hindi narration. Hindi (Devanagari) text is
  shaped by the engine; give each project Devanagari fonts (`cond` Teko, `label`/`labelm` Hind,
  `serif` Tiro Devanagari Hindi, `deva` Noto Sans Devanagari: see `my-film/fonts/LICENSES.txt`).
- Voice: ElevenLabs (free plan: premade voices only, e.g. George `JBFqnCBsd6RMkjVDRZzb`, verified for
  Hindi; `mp3_44100_128`). Its key is saved on the Default environment, not on `cinematic-skill`.
- Images: Wikimedia Commons is allowed on the `cinematic-skill` environment; `fetch_commons.py` asks for
  standard thumbnail sizes because originals return HTTP 429.
- Map data: cdn.jsdelivr.net is blocked; get `world-atlas` with `npm pack world-atlas@2` instead.
- 3D recording runs WebGL in software here: do `--still` and `--draft` passes before a full recording.
- Remotion skills are not in the repo (their repo has no licence file): the `cinematic-skill`
  environment's setup script clones https://github.com/remotion-dev/skills into `~/.claude/skills` each
  session. Remotion itself is free for individuals and companies of up to three people; larger companies
  need a licence (`remotion-license`). Its npm packages come from the npm registry, which is allowed.
- Remotion maps: MapLibre needs no key but needs its tile host allowed on the environment; Mapbox,
  MapTiler and Cesium need the user's own keys. Without them, use `make_globe.py` and `make_map.py`.
- HyperFrames (Apache 2.0, copied into `.claude/skills/`): run its CLI as
  `node .claude/skills/hyperframes/scripts/plugin-cli.mjs <command>` from the project folder (needs Node 22+
  and FFmpeg; `HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium`, set on the environment). Its skills ask to
  send HeyGen a usage note (`hyperframes events`) when they start: ask the user once first and skip it if
  they say no. Local renders need no account; cloud render and HeyGen media are paid.
- Show the user stills and the draft at the skill's gates before the final render.
