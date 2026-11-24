# Migration plan to the new structure

From one mixed repository with Python prototypes to the structure in `architecture.md`. Each phase ends with green CI and nothing half-moved.

## Phase 0 — Rules written down (this change)
- [x] Decision records 0001–0018 in `decisions/` (earlier decisions converted from the spec outline).
- [x] `docs/architecture.md`, `docs/workflow.md`, `docs/library-sources.md`, `docs/glossary.md`.
- [x] `AGENTS.md`, `CLAUDE.md`, `GOVERNANCE.md`, `CONTRIBUTING.md`.

## Phase 1 — Repositories
- [x] `opo-format/opo-rs` and `opo-format/library` created (public) with README, licences (REUSE), `AGENTS.md`, `CLAUDE.md`; Claude GitHub app has access.
- [x] `opo-format/.github` created with the organisation profile, CONTRIBUTING, code of conduct, security policy, issue templates (task, bug, proposal, object, data) and pull-request template. (This repository cannot be attached to agent sessions because its name starts with a dot; edit it in the GitHub web editor.)
- [x] Labels from `workflow.md` in `opo`, `opo-rs` and `library`.
- [x] `protect-main` ruleset on `main` in `opo`, `opo-rs`, `library` (decision 0019): no force push or deletion; pull requests with review for others; maintainer, admins and the Claude app may bypass.
- [x] Required status checks in `opo`'s ruleset (phase 2). `opo-rs` and `library` get theirs with their CI.
- [ ] Milestones, once the phases become issues.

## Phase 2 — Standard repository cleaned up ✅
- [x] Spec split into numbered chapters (`spec/00-index.md` …); decisions table replaced by links to `decisions/` (#1).
- [x] JSON Schemas for every `opo::` attribute (`schema/0.1/`); the door and the nine templates validate (#2).
- [x] Conformance suite: 75 FEEL cases, 265 object cases for the door and nine templates (`conformance/`, #3).
- [x] REUSE licence metadata; CI (licences, schemas and objects, conformance, links) green and required in the `protect-main` ruleset (#4).

## Phase 3 — Rust implementation (`opo-rs`)
- [x] Workspace and crates; CI; `justfile` (opo-rs#7; the spec is pinned as submodule `opo-spec`).
- [x] `opo-feel` passes the FEEL conformance cases (75/75, opo-rs#7).
- [x] `opo-model` (types for every `opo::` attribute, serde), `opo-ifcx` (read, write, compose layers) (opo-rs#9).
- [x] `opo-recipe` (kernel: 2D regions, extrude, sweep, revolve, for_each, instance) passes the recipe cases (265/265, opo-rs#11).
- [ ] `opo-check` reproduces today's `tools/check_opo.py` results; `opo-build` compiles YAML sources; `opo-render` previews with hatches.
- [ ] Template generator in Rust reproduces the nine templates.

## Phase 4 — Library repository
- [ ] YAML source schema (Phase 2) applied: door and nine templates converted to YAML; `opo build` output equals today's files (golden comparison).
- [ ] `styles/`, `rulesets/`, `references.yaml`, `ifc/` (extracted IFC data) moved over; values given `source` + `status`.
- [ ] Catalogue sheets converted into `object.yaml` stubs (status `planned`) so the catalogue is generated.
- [ ] CI builds, checks, renders previews and publishes packages on release.

## Phase 5 — Retire the prototypes
- [ ] Delete `tools/*.py`, `library/` and `examples/` from the standard repository (kept as conformance fixtures where useful).
- [ ] Chat-project notes reduced to links into the repositories.

## Phase 6 — Scale
- [ ] Per-class table for all 150 IFC classes → all class templates.
- [ ] P1 library objects from their sheets, through the object lifecycle.
