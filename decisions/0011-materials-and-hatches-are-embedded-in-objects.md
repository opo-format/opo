---
status: accepted
date: 2026-11-24
deciders: maintainer
---

# 0011. Materials and hatches are embedded in objects

## Context

Imported wall and slab types must keep their hatch detail. Tools that reference hatches by name lose them when the receiving file lacks the pattern.

## Decision

Objects embed their materials (`opo::materials`) and hatch definitions (`opo::hatches`, line families in model or paper scale). Project drawing styles may override; definitions always stay in the object. Joins merge by material.

## Consequences

Packages of only materials and hatches (`kind: styles`) share office standards.
