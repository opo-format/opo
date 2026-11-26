---
status: accepted
date: 2026-11-26
deciders: maintainer
---

# 0025. Curva work happens in Curva, under its own rules; wall and door first

## Context

The real test of OPO is wall and door working in Curva, later in a Rhino plug-in. Curva has its own rules: issues as the backlog, specs approved before code, work streams.

## Decision

- OPO work is done in the OPO repositories; the Curva integration is done in Curva's own sessions, starting its Architecture milestone with a spec the maintainer approves.
- Wall and door are made to work end to end first, against an acceptance checklist the maintainer approved on 26 November 2026. The other objects follow the same pattern only after that.
- Drawing conventions chosen along the way (which parts each plan level leaves out, elevation direction) become written rules.

## Consequences

- The other P1 objects stay as drafts until wall and door pass the checklist.
