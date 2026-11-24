# AGENTS.md — instructions for AI agents (and a checklist for humans)

This is the **standard** repository of the OPO format (Open Parametric Object). The project is run by one maintainer working with AI agents (decision 0012). Read this file fully before changing anything.

## Read first
- `docs/architecture.md`: which repository and file is the source of truth for what.
- `docs/workflow.md`: issues, branches, pull requests, checks, proposals, object lifecycle.
- `decisions/README.md`: what has been decided. Do not reopen a decision without a new decision record.
- `docs/glossary.md`: use these words with these meanings.

## Hard rules
1. **Never invent a value from a norm or a maker.** If you cannot cite it, enter it as `status: to_verify` with a note on what to check (decision 0017). Say so in the pull request.
2. **Never edit generated files** (built packages, catalogue and coverage tables, previews, indexes marked "generated"). Change the source or the generator (decision 0016).
3. **One concern per pull request.** Don't mix formatting with content, or two objects in one pull request.
4. **Normative changes need a proposal or a decision record** and the maintainer's explicit approval: anything in `spec/`, `schema/`, `conformance/`, `decisions/` or `proposals/` that changes meaning.
5. **European values come from EN and ISO norms only**; no national norms (decision 0009). UK and US are separate markets.
6. **Units are metres and degrees** in every stored value (decision 0005).
7. **No Google services, libraries or standards** in the project (maintainer policy).
8. **Licences:** spec text CC-BY-4.0; schemas, tests and code MIT OR Apache-2.0; library objects CC0-1.0. Never copy text, tables or data from a source whose licence does not allow it; cite the source and enter values in your own structure.

## Before you open a pull request
- `just check` passes (until the `justfile` exists: run the commands listed in `docs/workflow.md` §3 that apply).
- The pull request links its issue, says what was checked, and lists every value entered as `to_verify`.
- Commit messages follow Conventional Commits: `feat(scope): …`, `fix(scope): …`, `docs(scope): …`.

## Style
- Plain, direct English; short sentences; British spelling in the spec (metres, colour).
- Spec text uses "must", "should" and "may" as defined in the spec's conventions chapter.
- File names: lower case with hyphens; decision and proposal files start with a four-digit number.

## Current state (keep this short; details live in issues)
The repository is being migrated to the layout in `docs/architecture.md` (plan: `docs/migration.md`). `tools/*.py` are prototypes that will be deleted (phase 5); do not extend them. The door and class templates are maintained in the library repository; `conformance/fixtures/` holds frozen copies for the conformance suite.
