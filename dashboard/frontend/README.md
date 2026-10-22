# Dashboard frontend

**Owner:** R5 — Ethan  
**Status:** Not implemented — scaffold only.

React + TypeScript app showing station status, potential smoke detections (confidence, time, station, model), alert confirm/dismiss, and recent history.

## Planned contents

- Project not yet initialized. The build tool (e.g. Vite) is the owner's choice — record it in an ADR.
- Add `lint`, `typecheck`, `test` and `build` npm scripts; CI runs them automatically once `package.json` and `package-lock.json` exist.
- Use ESLint and Prettier.

## Boundaries

Offline review requires a representative image with each accepted event. Show incomplete evidence explicitly until metadata and image are complete. Add configuration, candidate/model approval, limited deployment/rollback and actor/action history per the v1.1 SRS. Image transport/storage and access details still need joint contracts.
