---
status: accepted
date: 2026-11-24
deciders: maintainer
---

# 0010. Every IFC element class has a class template

## Context

Every IFC object type must be creatable parametrically and shareable as a file, like a Revit family, including types other tools keep as system families.

## Decision

Every concrete IFC element class gets a generated class template on one of eight archetypes (point, linear, area, wall, hosted, flight, fitting, assembly). Detailed library objects refine templates and keep their IFC data.

## Consequences

Templates are regenerated when IFC changes; hand edits go into the per-class table.
