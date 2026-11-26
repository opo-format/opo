---
status: accepted
date: 2026-11-26
deciders: maintainer
---

# 0022. Recipes describe exact geometry; each application builds it with its own engine

## Context

The reference implementation turns recipes straight into triangle meshes. Curva builds walls as exact extrusions and curved shapes as exact surfaces, and exports IFC with exact geometry. IFC 4.3 supports exact solids (extrusions, sweeps, revolutions) and NURBS faces (advanced B-reps). IFCX alpha carries only triangle meshes today. The planned Rhino plug-in will use Rhino's own geometry.

## Options considered

- A: recipe operations describe exact construction steps (profiles with straight and curved edges, extrusions, sweeps, revolutions, lofts); the OPO engine evaluates parameters, rules and steps, and each application builds the shapes with its own geometry engine. Meshes are baked into the file only for plain viewers.
- B: applications display the meshes the OPO engine produces.

## Decision

A. The meaning of every operation is its exact result. Tessellation (`segments` and similar hints) only affects meshes made for display and for plain IFCX viewers. The reference implementation separates evaluation from geometry: a geometry interface with a mesh builder for tests and previews, and room for exact builders (Curva's kernel, Rhino).

## Consequences

- opo-rs is restructured so geometry building sits behind an interface.
- The spec states that operations are exact and that baked meshes are a display copy.
- Conformance keeps checking results within a tolerance, so mesh and exact builders both pass.
- Exports to IFC 4.3 can carry exact solids and NURBS; IFCX exports keep meshes until IFCX gains exact geometry.
