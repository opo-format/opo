---
status: accepted
date: 2026-11-24
deciders: maintainer
---

# 0013. Split into separate repositories

## Context

The standard, its reference implementation and the object library change at different speeds, have different licences and different reviewers.

## Decision

The `opo-format` organisation has: `opo` (the standard: spec, schemas, conformance tests, decisions, proposals), `opo-rs` (Rust reference implementation and CLI), `library` (object sources, templates, rule sets, styles; releases publish built packages), `.github` (organisation-wide contributor files and templates). A website repository follows later.

## Consequences

Each repo pins the versions it depends on (library pins the CLI; the CLI pins the spec and its conformance suite). Cross-repo changes are linked by issue.
