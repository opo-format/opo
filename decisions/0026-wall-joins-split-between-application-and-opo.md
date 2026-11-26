---
status: accepted
date: 2026-11-26
deciders: maintainer
---

# 0026. Wall joins: the application finds them, OPO computes them

## Context

The strategy review first gave wall joins, corners and openings to Curva. The maintainer then asked who should compute a join when the location lines of two walls meet. If each application computed joins its own way, the same project would draw differently in Curva, in a Rhino plug-in and in the exported IFC.

## Options considered

- A: the application computes joins.
- B: the application finds where walls meet; the join rules live in the wall type and the shared OPO engine computes the clean-up.

## Decision

B. The application detects that walls meet (end to end, end to side, crossing) and passes the meeting to the OPO engine with both wall types. The wall type's join rules (`opo::host.joins`) say how layers meet: core to core, finish to finish, which wall runs through, butt or mitre. The OPO engine computes the resulting layer outlines, so every application gets the same corner.

Openings follow proposal 0004: the application places the hosted object, the wall applies the void and the reveal rules.

## Consequences

- The spec defines the join input (the two walls, their meeting point, the angle) and the result (trimmed layer outlines per wall).
- The opo-rs engine gets a join module; conformance gets L, T and X join fixtures.
- Decision 3 of the strategy review is refined by this record.
