# Edge video input

**Owner:** R2 — Tomiwa  
**Status:** Not implemented — scaffold only.

Frame source abstraction over a live camera or a prerecorded wildfire video file, with a controllable processing frame rate.

## Planned contents

- Camera source (Pi camera / USB — hardware choice per station)
- File source for prerecorded video (used for development and repeatable tests)
- Runtime-adjustable processing FPS (target of the required FPS adaptation)

## Boundaries

Do not commit video files; see CONTRIBUTING.md "Large files".
