---
status: accepted
date: 2026-11-23
deciders: maintainer
---

# 0007. Sketch constraints are solved by the application

## Context

Constraint solving is application-specific and hard to standardise.

## Decision

OPO stores resolved input geometry and its validity rules; applications solve their own sketch constraints.

## Consequences

Optional constraint hints may be added later.
