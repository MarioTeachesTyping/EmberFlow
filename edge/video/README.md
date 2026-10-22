# Edge video input

**Owner:** R2 — Tomiwa  
**Status:** Not implemented — scaffold only.

Frame source abstraction over a live camera or a prerecorded wildfire video file, with a controllable processing frame rate.

## Planned contents

- One USB webcam initially, to be verified on each of the three Pis; exact model/video mode open
- File source for prerecorded video (used for development and repeatable tests)
- Runtime-adjustable processing FPS and preprocessing resolution; keep capture FPS distinct
- Frame identity/timestamps and camera loss/recovery status for the ML/platform contract

## Boundaries

Do not commit video files; see CONTRIBUTING.md "Large files".
