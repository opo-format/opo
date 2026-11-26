---
status: accepted
date: 2026-11-26
deciders: maintainer
---

# 0024. Elevations are seen from outside

## Context

The reference renderer drew elevations from inside the building, a choice made without a decision. Opening symbols, surrounds and cladding are normally drawn as seen from outside.

## Decision

Elevation representations and derived elevations are seen from the outside face of the host (the side that is not the room side). Opening symbols are drawn as seen from there.

## Consequences

- The renderer and objects whose elevation symbols assume the inside view are updated.
