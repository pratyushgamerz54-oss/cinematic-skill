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
| React video components, extra animation, map and 3D templates | the Remotion plugin (`remotion-*` skills), when it is installed |

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
- Show the user stills and the draft at the skill's gates before the final render.
