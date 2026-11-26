---
status: accepted
date: 2026-11-26
deciders: maintainer
---

# 0027. Levels of detail follow shared part categories

## Context

Each object chose on its own which parts to leave out of its low and medium detail drawings (`exclude_parts` per object). Objects drift apart, and an office cannot change the convention in one place.

## Decision

Every part of an object has a category from a fixed list (for example structure, frame, leaf, glass, hardware, trim, finish, insulation, railing, tread). One shared table says which categories appear in plan, section and elevation at low, medium and high detail. Objects follow the table; a project may override it once for all objects. An object may still add an exception, with a note saying why.

## Consequences

- A proposal (0005) defines the category list, the default table and how a project overrides it.
- `exclude_parts` lists in library objects are replaced by part categories.
