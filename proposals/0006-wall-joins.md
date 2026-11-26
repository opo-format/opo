---
stage: 2          # 0 idea | 1 draft | 2 candidate | 3 final | withdrawn | rejected
issue: "#NN"
spec_version: "0.2"
---

# 0006. Wall joins

## Summary

How walls join in plan when their paths meet (decision 0026), for walls that are one solid with drawn layers (decision 0028). The application gives the OPO engine the walls of a storey; the engine finds the meetings and trims each wall's plan shape; every application then draws the same corners.

## Motivation

A room of four external walls and two internal walls must draw as one clean outline, with the layers running round the corners, in Curva, in a Rhino plug-in and in an exported IFC. If each application joined walls its own way, the same project would look different in each.

## Design

### Input

The walls of one storey, each with its type and values: its path, the offset of its front face from the path, its total thickness and its layers (the wall class template's `path`, `left_face`, `total_thickness`, `layers`, `layer_start`).

### Meetings

A path end meets another wall when it lies within 1 mm of that wall's path.

- **L join**: the end meets the other wall's path at one of its ends. Both walls run past the corner and are split along the line through the corner that halves the angle between their paths (a mitre).
- **T join**: the end meets the other wall's path away from its ends. The meeting wall runs into the other and stops at its far face; the other runs through.
- **Any other overlap** (walls crossing): the wall placed first runs through.

### Result

For each wall: its plan shape after the joins, and each layer's band inside that shape. The wall's 3D solid is its plan shape extruded from its base to its top.

### Drawing

- Low detail: all joined walls are one region, filled solid where the core is mass construction.
- Medium and high detail: layers of the same material merge across walls, so a core runs into a core without a line; one outline is drawn round all walls.

### Wall type

`opo::host.joins.by` is `layer` for the wall class template. Butt joins, priorities between wall types and layer-by-layer clean-up (finish to finish, core to core across different build-ups) are left for a later proposal.

## Drawbacks

- Mitres are drawn through the corner point, so walls of different thickness meet on the angle's half line, not on the line joining the inner and outer corners.
- A T join does not cut the through wall's finish where the meeting wall's core arrives.

## Alternatives considered

- **Joins by the application.** Rejected by decision 0026.
- **Layer-by-layer joins now.** Too advanced for the first working setup (decision 0028).

## Conformance tests

- Two 0.2 m walls meeting at an L: their shapes cover the corner without gap or overlap.
- A 0.1 m wall meeting a 0.3 m wall at a T: the meeting wall stops at the near face; the other is unchanged.
- Two crossing walls: the first runs through.

## Open questions

- Should a project be able to choose butt joins instead of mitres at L corners?
