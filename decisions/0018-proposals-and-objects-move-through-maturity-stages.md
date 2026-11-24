---
status: accepted
date: 2026-11-24
deciders: maintainer
---

# 0018. Proposals and objects move through maturity stages

## Context

Changes to the standard need a predictable path; objects need a visible quality level.

## Decision

Spec changes are proposals (OPO Enhancement Proposals) with stages: 0 idea, 1 draft (problem and design written), 2 candidate (schema and conformance tests merged, implemented in opo-rs), 3 final (in a released spec version, used by an application). Objects have statuses: planned, draft, review, stable, deprecated.

## Consequences

Version 1.0 of the standard additionally needs a second independent implementation passing the conformance tests.
