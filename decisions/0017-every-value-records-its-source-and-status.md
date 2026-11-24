---
status: accepted
date: 2026-11-24
deciders: maintainer
---

# 0017. Every value records its source and status

## Context

Notes like 'to verify' or 'typical' were buried in prose.

## Decision

Numeric values in library sources are written as plain numbers when they are design choices, or with `source` (a reference id from the references registry) and `status` (`norm`, `maker`, `typical`, `illustrative`, `to_verify`) when they come from somewhere. CI reports `to_verify` values and blocks a stable release of an object that has any.

## Consequences

Agents must never invent a norm value; unknown values are entered as `to_verify` with a note.
