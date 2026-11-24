# How work gets done

The same workflow applies to humans and AI agents. The maintainer decides and merges (decision 0012); CI is the gate.

## 1. Every piece of work starts as an issue

An issue states:
- **Goal**: one sentence.
- **Acceptance criteria**: checkable statements ("`opo check` passes for `objects/door-single-swing`", "riser limits for UK AD K entered with `source: uk-adk-2013`").
- **Sources needed**: norms or data the work depends on. If a source is missing, the work enters values as `to_verify` (decision 0017); it never guesses.
- **Labels**: area (`spec`, `schema`, `conformance`, `rust`, `object`, `template`, `ruleset`, `styles`, `docs`, `process`), type (`bug`, `feature`, `data`, `chore`), and `normative` when the standard changes.

Small fixes (typos, broken links) may skip the issue.

## 2. One branch, one pull request, one concern

- Branch names: `<area>/<short-topic>`, e.g. `object/casement-window`.
- A pull request does one thing: one object, one proposal, one feature. Mechanical changes (formatting, renames) go in their own pull request.
- Commit messages follow **Conventional Commits**: `feat(object): add casement window`, `fix(feel): ranges run downwards`, `docs(spec): clarify units`. Changelogs are generated from them.
- The pull request description links the issue and lists what was checked.

## 3. CI decides whether it is done

Required checks, by repository:

| Check | opo | opo-rs | library |
|---|---|---|---|
| Format and lint (Markdown, YAML, Rust) | ✓ | ✓ | ✓ |
| JSON Schemas valid; examples validate | ✓ | | ✓ |
| Conformance suite | (self-test) | ✓ | |
| Unit tests | | ✓ | |
| `opo build` + `opo check` on every object | | | ✓ |
| Generated outputs reproducible, none committed | ✓ | | ✓ |
| Licence metadata complete (REUSE lint) | ✓ | ✓ | ✓ |
| Links resolve | ✓ | | ✓ |
| `to_verify` report (blocks `stable` objects) | | | ✓ |

## 4. Review and merge

- The maintainer reviews and merges. Anything labelled `normative` (spec, schema, conformance, decisions, proposals) needs the maintainer's explicit approval, never an automatic merge.
- Agents may review each other's pull requests as a first pass; the maintainer has the final say.
- Squash-merge, with the pull request title as the commit message.

## Changing the standard: proposals

Use a proposal for anything that changes what a valid `.opo` is or how it must be read (new attribute, new recipe operation, FEEL change, packaging rule). Editorial clarifications do not need one.

| Stage | Name | Entry criteria |
|---|---|---|
| 0 | Idea | An issue describing the problem. |
| 1 | Draft | `proposals/NNNN-title.md` with motivation, design, drawbacks, alternatives and examples; merged as draft. |
| 2 | Candidate | Schema changes and conformance tests merged in `opo`; implemented in `opo-rs` behind the next spec version. |
| 3 | Final | Included in a released spec version and used by at least one application (Curva). For 1.0, a second independent implementation must pass the conformance tests. |

A proposal can be withdrawn or rejected at any stage; the file stays, with the reason.

## Object lifecycle

| Status | Meaning | Required |
|---|---|---|
| `planned` | listed in the catalogue | id, IFC class, priority, scope sentence |
| `draft` | builds, may have gaps | builds and checks; `to_verify` values allowed |
| `review` | complete, awaiting review | all values sourced or marked as design choices; previews look right |
| `stable` | released | no `to_verify` values; at least one size catalogue per market it claims; changelog entry |
| `deprecated` | kept for old files | `replaced_by` names the successor |

Changing a stable object's parameters in a breaking way bumps its major version.

## Commands

Each repository has a `justfile`, so humans and agents run the same commands:

| Command | Does |
|---|---|
| `just check` | everything CI runs, locally |
| `just fmt` | format all sources |
| `just build` | build packages / binaries |
| `just new-object <id> <IfcClass>` | library: scaffold an object folder from its class template |
| `just new-decision "<title>"` | opo: copy the decision template with the next number |
| `just new-proposal "<title>"` | opo: copy the proposal template with the next number |
