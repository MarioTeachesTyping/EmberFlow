# EmberFlow specification revision package

Revision 1.1 dated October 22, 2026. These are revised review drafts, not records of completed hardware or software implementation and not evidence of faculty or full-team signoff.

## Documents

- EmberFlow_Tomiwa_Edge_Subsystem_Specification_v1_1: Tomiwa's hardware-first individual subsystem specification, physical and logical diagrams, interfaces, requirements, test procedures, and handoff expectations.
- EmberFlow_Roles_and_Requirements_Specification_v1_1: six named owners, revised hardware responsibilities, preserved shared requirement IDs, and SRS mappings.
- EmberFlow_Senior_Design_SRS_v1_1: aligned system interfaces, requirements, data/image contracts, acceptance gates, and ownership/verification traceability.

Each document is provided as an editable Word file, a Markdown source, and a rendered PDF. The diagrams folder contains PNG figures plus editable Mermaid sources. The Mermaid sources express the same architecture and may use a different automatic layout when rendered.

## Agreed revision baseline

- Three physical Raspberry Pi 5 stations; indoor demonstration; no custom PCB required.
- One USB webcam initially, verified on each station; recorded footage on the other two stations.
- Existing team laptop/desktop for central services; wired Ethernet through a switch/router.
- Offline detections retain metadata and one representative image; synchronization completes only after both are durable and reviewable centrally.
- Tomiwa owns hardware/platform integration; Diego owns model and image/model algorithms; James owns controller policy and ingestion; Ethan owns central persistence/review; Anthony coordinates architecture; Dylan coordinates validation.

## Open decisions

Budget and exact hardware variants remain open. Numerical performance limits, model/runtime, address/service configuration, messaging/image transport, and bounded storage policy require the named owners' decisions. The documents include closure gates rather than invented prices, measured results, or performance promises. No purchases, shared Google Docs edits, Jira changes, or platform implementation were performed as part of this document revision.

## Important wording changes

- Existing document identifiers are retained within their original namespaces. SRS and team ownership assignments now name the people responsible.
- R2 camera support is mandatory for the shared USB platform, tested with one camera across stations.
- Pi 5 is the selected document baseline; historical Jetson/TensorRT alternatives do not become extra acceptance obligations.
- Buffered records now include representative images and retained telemetry with quotas and lifecycle rules.
- R2 synchronization wording now permits safe retransmission after a missing receipt and requires idempotent central completion, rather than prohibiting all repeat transmissions.
- Known-good model retention is aligned with the original mandatory SRS rollback requirement.
- Simulations support development; the revised final gate requires three physical nodes.
- Existing shadow/candidate/rollback, image/model trust monitoring, workload movement, human review, and comparative-evaluation requirements remain in scope.
- Remaining evidence gates replace elapsed generic month labels. Archived ECE dates are labeled historical and require reconciliation with the CS-led team calendar.

## Verification

The Validation_Record.json records source hashes, preserved original identifier counts, successful PDF generation, no detected horizontal text overflow, and no empty pages. Rendered pages were reviewed for layout. These are document-quality checks, not execution of the specified platform tests. The three original attached PDFs were not modified.
