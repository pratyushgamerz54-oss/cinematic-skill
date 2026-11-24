# Project skills

Claude Code loads every skill in this folder when it works in this repo.

| Skill | From | Used for |
| --- | --- | --- |
| `cinematic-film` | this repo (`skills/cinematic-film`, linked) | the film: board, camera, maps, voice, sound, captions |
| `threejs-scene` | Open 3D Skills | 3D shots built in code: globes, terrain, landmarks, objects |
| `frame-capture` | Open 3D Skills | records a three.js or motion-graphics page to a frame-exact MP4 |
| `motion-assets` | Open 3D Skills | plans AI stills and clips in one style, with prompts and costs first |
| `exploded-view` | Open 3D Skills | 3D "how it works" explainers (weapons, machines, buildings) |
| `site-check` | Open 3D Skills | checks a 3D page renders (no blank WebGL, errors, frame time) before recording it |
| `alpha-cutout` | Open 3D Skills | keys a character or object out of a clip, for a transparent cut-out on the board |

The six Open 3D Skills are copied unchanged from https://github.com/Moh4696/open-3d-skills
(commit 53beb89, MIT License, copyright exploraX: see LICENSE-open-3d-skills).
`skills/cinematic-film/references/3d.md` says how they plug into a film.

Remotion's agent skills (`remotion-*`) are installed in `~/.claude/skills` by the `cinematic-skill`
environment's setup script from https://github.com/remotion-dev/skills, not copied here.
