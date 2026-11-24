---
status: accepted
date: 2026-11-24
deciders: maintainer
supersedes: part of 0012 (who merges)
---

# 0019. Protected main, with direct push and merge for the maintainer and agents

## Context

Decision 0012 said the maintainer merges every change. The maintainer wants AI agents to be able to push and merge their own work, while `main` stays protected against outside contributors and accidents. Agent sessions push under the maintainer's GitHub account (or as the Claude GitHub app).

## Decision

`main` in `opo`, `opo-rs` and `library` is protected by a repository ruleset named `protect-main`:

- no force pushes, no deletion of `main`;
- everyone else changes `main` only through a pull request with 1 approving review, resolved conversations and squash merge;
- organisation admins, repository admins and the Claude GitHub app may bypass: they can push to `main` and merge directly.

Agents may push and merge their own work. They still follow `AGENTS.md`: normative changes (spec, schema, conformance, decisions, proposals) need the maintainer's explicit approval in the conversation or on the pull request before they are merged. When CI exists, "required status checks" is added to the ruleset and agents merge only on green CI.

## Consequences

The protection guards against outside contributors and accidents, not against anything acting with the maintainer's account. `opo-format/.github` is not covered (agent sessions cannot attach it; it is edited in the GitHub web editor).
