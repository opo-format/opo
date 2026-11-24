---
status: accepted
date: 2026-11-23
deciders: maintainer
---

# 0005. Values are stored in metres and degrees

## Context

Objects must work in mm, m, feet and inches; IFCX stores metres.

## Decision

Values are stored in metres and degrees at full precision; applications display any unit. Limits, steps and standard sizes may be given per unit system.

## Consequences

Formulas only see canonical units, so results are identical everywhere.
