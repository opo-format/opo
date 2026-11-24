---
stage: 1          # 0 idea | 1 draft | 2 candidate | 3 final | withdrawn | rejected
issue: "#5"
spec_version: "0.2"
---

# 0001. Grid systems and swappable components

## Summary

Some building elements are not one shape built from one drawn input. They are **systems**: a generator (a baseline with a height, a path, a face) is divided by rules into a grid, and member objects are placed on the grid's lines, nodes and cells. Curtain walls (mullions, transoms, panels, spandrels, junctions), railings (posts, rails, balusters, infill panels) and sloped glazing all work this way.

This proposal adds five things to OPO:

1. A `layout` operation: divide a length by architectural rules (fixed sizes, best division, count, maximum spacing, explicit positions, within intervals such as storeys).
2. A `grid` operation: lay out two directions on a surface and return its nodes, segments and cells, each with a class.
3. `component` parameters and `opo::interface`: swappable nested objects (a mullion, a panel, a window in a cell) with a contract for what the parent passes them and what they report back.
4. Two input slot types: `surface` (baseline + heights, or a flat face) and `points` (a fixed number of placement points).
5. An instance `overrides` slot: per-instance edits to a grid (remove a segment to merge cells, change a cell's or segment's class or component) that are kept out of the object type.

## Motivation

OPO 0.1 builds an object from parameters, drawn inputs, formulas and a geometry recipe, and can nest other objects. That covers simple objects: a door, a beam, a boiler, a slab.

A stick curtain wall (catalogue O-16) shows what is missing:

- **No rule-based division.** `for` and `for_each` can repeat things at a computed spacing, but each object would re-implement "fixed size with leftover", "best division" or "maximum spacing" in FEEL, and two applications would round differently. Users expect these rules from the design tools they already use.
- **No grid topology.** A curtain wall needs to know which segment lies between which nodes, which cells it bounds, which segments are on the border, and which cell is in which row and column, so that a transom stops at a mullion and a spandrel row gets spandrel panels.
- **Nested objects are fixed.** `instance(object, …)` names one object id. Users must be able to choose which mullion or panel object a class uses, and swap one cell to a door. A swapped object needs a contract: what inputs it receives and what it reports back (a mullion's face width, so panels can shrink to fit).
- **No per-instance edits.** Removing one transom to make a tall panel is an edit to one placed curtain wall, not a new type.
- **No surface or point-set input.** Slots are curves and closed profiles; a curtain wall needs a baseline with a height, and a panel object needs its four corners.

The same gaps block railings (C-07, C-08), sloped glazing, louvre screens, cladding panel systems, raised floors and suspended ceiling grids.

## Design

All lengths are metres and all angles degrees (decision 0005). All new operations are deterministic: the same arguments give the same result to within the 1e-9 equality of spec §4.4.

### 1. `layout`: divide a length

```
layout(length, pattern, [distribution, origin, infill, end_with, within])
```

| Argument | Type | Meaning |
|---|---|---|
| `length` | number | Length to divide, > 0. |
| `pattern` | list of contexts | Pattern entries `{size, flexible?, cls?}`. `size` > 0. `flexible` defaults to false. `cls` (class name) defaults to `"main"`. |
| `distribution` | string | `fixed` (default), `best_division`, `count`, `max_spacing`, `positions`. |
| `origin` | string | `fixed` only: `start` (default), `end`, `center`. |
| `infill` | string | `fixed` only: `"partial"` (default) or a class name. |
| `end_with` | integer | `best_division` only: index (1-based) of the pattern entry that ends the sequence. Default: the last entry. |
| `within` | list of numbers | Optional break points in (0, length). The layout runs separately in each interval between break points. |

The result is a context:

```
{ bays: [ {index, start, end, size, cls} … ],
  lines: [ {index, at, cls} … ] }
```

`bays` are the intervals in order from 0 to `length`. `lines` are the division positions including both ends; the end lines have `cls` `"border"`, lines at `within` break points have `cls` `"break"`, the others `"division"`.

Distributions:

- **`fixed`.** The pattern repeats at its given sizes; flexible flags are ignored. `origin: start` starts the first entry at 0; `end` lays the pattern backwards from `length`; `center` puts the midpoint of the repeated sequence at `length / 2` with whole patterns placed outwards from it. The pattern is cut at the ends. With `infill: "partial"` a cut bay keeps its entry's class; with a class name, every bay that is shorter than its entry's size gets that class.
- **`best_division`.** At least one entry must be flexible. The sequence is the pattern repeated *k* times, followed by entries 1..`end_with` of one more repetition when `end_with` is smaller than the number of entries. Fixed entries keep their size; flexible entries are all scaled by one factor *s* (so they keep their ratios) so the sequence fills `length` exactly. *k* is the whole number ≥ 1 with *s* > 0 for which |*s* − 1| is smallest; on a tie, the larger *k*. If no *k* gives *s* > 0, the layout is invalid and a check fails.
- **`count`.** `pattern` holds one entry; its `size` is read as the number of equal bays (a whole number ≥ 1).
- **`max_spacing`.** `pattern` holds one entry; the fewest equal bays whose size is ≤ the entry's `size`.
- **`positions`.** `pattern` is a list of numbers in (0, `length`), sorted ascending: the division positions. Classes are `"main"`. (Lines at levels, or lines drawn by the user.)

With `within`, each interval is laid out on its own with the same arguments, and bay and line indices run on across intervals. This is how a curtain wall gets a spandrel zone and a vision zone in every storey even when storey heights differ: `within` is the list of level heights.

### 2. `grid`: a two-way layout on a surface

```
grid(surface, u, v, [join, classes, overrides])
```

| Argument | Meaning |
|---|---|
| `surface` | A `surface` input (§4 below). |
| `u` | Arguments of a `layout` (a context with `pattern`, `distribution`, …) applied along the surface: along the developed baseline, per baseline segment. |
| `v` | Arguments of a `layout` applied up the surface (from base to top). |
| `classes` | Optional FEEL rules for member classes (see Member classes). |
| `join` | `u_continuous` (default: vertical members run through, like stick-system mullions) or `v_continuous`. Decides which segments break at a node. |
| `overrides` | The instance `overrides` input (§5), or empty. |

**Baseline with several segments.** Each baseline segment is laid out on its own with `u`; the pattern restarts on every straight run, and baseline vertices become grid lines of class `"corner"`.

**Result.** A context with three lists:

- `nodes`: `{id, point, u_index, v_index}` at every line intersection.
- `segments`: one per piece of a grid line between two nodes: `{id, direction ("u" or "v"), line_cls, cls, start, end, path, length, normal, trim_start, trim_end, cells}`. `line_cls` is the class of its line from the layout (`border`, `corner`, `break`, `division`); `cls` is the member class (below). `path` is the 3D line from `start` to `end`. `cells` holds the ids of the one or two cells on either side.
- `cells`: `{id, column, row, cls, column_cls, row_cls, outline, panel_outline, width, height, origin, x_axis, y_axis, normal, segments}`. `outline` is the four 3D corners, counter-clockwise seen from the front (+normal side); `width` and `height` are measured on the surface between the grid lines (before member sizes are taken off, see §3 outputs).

**Ids** are stable for a given layout: lines are numbered from 0 along u and v; a cell is `"c{column}.{row}"`; a u-direction segment on line *j* between columns is `"h{j}.{column}"`, a v-direction segment on line *i* between rows is `"v{i}.{row}"`; a node is `"n{i}.{j}"`. (u-direction segments run horizontally on a vertical wall: transoms; v-direction segments run vertically: mullions.)

**Member classes.** By default a segment's `cls` is `"boundary"` on the surface outline, `"corner"` on corner lines, `"mullion"` for other v-direction segments and `"transom"` for other u-direction segments. A cell's `cls` is its row's class when that is not `"main"`, otherwise its column's class (so a spandrel row of the v-pattern makes spandrel cells). Objects may replace both rules with FEEL expressions in the grid's optional `classes` argument: `{segment: <expr over segment>, cell: <expr over cell>}`.

**Join.** With `u_continuous`, v-direction segments (mullions) run from node to node unbroken through every intersection and u-direction segments (transoms) are trimmed between them; `v_continuous` is the reverse. The trimming itself is done by the members, from the `trim_start` and `trim_end` widths the grid passes them (§3).

The grid produces no geometry. Members are placed with `for_each` and `instance` over its lists:

```yaml
- id: g
  op: grid
  args:
    surface: surface
    u: "{pattern: [{size: module, flexible: true}], distribution: 'best_division'}"
    v: "{pattern: [{size: spandrel_height, cls: 'spandrel'}, {size: 1, flexible: true, cls: 'vision'}], distribution: 'best_division', within: levels}"
- id: frames
  op: for_each
  args:
    items: g.segments
    as: s
    do: "instance(component_for(frame_classes, s.cls), inputs: {path: s.path, normal: s.normal, trim_start: s.trim_start, trim_end: s.trim_end})"
- id: panels
  op: for_each
  args:
    items: g.cells
    as: c
    do: "instance(component_for(panel_classes, c.cls), inputs: {outline: c.panel_outline, normal: c.normal})"
```

`component_for(map, cls)` is a new FEEL function: the component value for `cls` in a class map, or the map's `default` entry.

### 3. `component` parameters and `opo::interface`

**Component parameter.** A new parameter type, `component`: a nested object chosen by the user.

```yaml
mullion:
  type: component
  interface: frame
  default: opo:library/mullion-pressure-plate
  allowed: { ifc_class: IfcMember }      # or a list of object ids
```

A **class map** is a `component` parameter with one entry per class:

```yaml
panel_classes:
  type: component
  interface: panel
  classes:
    main: opo:library/glazed-panel-igu
    spandrel: opo:library/spandrel-panel-opaque
    default: opo:library/glazed-panel-igu
```

`instance(object, …)` accepts a component value wherever it accepts an object id. A packaged `.opo` embeds every object a component parameter's default and classes name (spec §4.9); objects the user picks later travel with the project.

**Interface.** A nested object that can fill a component slot declares `opo::interface`: its name, the inputs it accepts from the parent and the derived values it reports back. The spec defines the first four standard interfaces:

| Interface | Inputs from the parent | Reported back (derived values) | Typical IFC class |
|---|---|---|---|
| `frame` | `path` (3D line), `normal` (front of the surface), `trim_start`, `trim_end` (lengths to stop short of the end nodes), `left_cell`, `right_cell` (sizes, may be null) | `face_width`, `depth`, `offset` (from the surface to the member's front face) | `IfcMember` MULLION |
| `panel` | `outline` (closed polygon on the cell plane, counter-clockwise from the front), `normal`, `insets` (per edge, from the surrounding frames' `face_width`) | `thickness`, `offset` | `IfcPlate` CURTAIN_PANEL; `IfcWindow`, `IfcDoor` when a window or door fills a cell |
| `node` | `point`, `normal`, `directions` (unit vectors of the segments meeting there) | — | `IfcMember`, `IfcDiscreteAccessory` *(to decide)* |
| `post` | `point`, `direction` (along the path), `height`, `normal` | `face_width` | `IfcMember` |

The grid uses reported values: each segment's `trim_start` and `trim_end` are half the `face_width` of the continuous members it meets, and each cell's `panel_outline` is its `outline` inset by half the `face_width` of each bounding member. It lets a door object sit in a cell of any mullion system.

A check fails if an object placed in a component slot does not declare the slot's interface, or if a required interface input is not passed.

### 4. Input slot types `surface` and `points`

- **`surface`**: either `{baseline, base, top}`, where `baseline` is a polyline or arc in plan and `base` and `top` are heights (or level references resolved by the application to heights), or `{face}`, a flat closed polygon in 3D (sloped glazing, a sloped roof light). The surface's u direction runs along the baseline (or the face's first edge), v runs up (or across). Validity: baseline not self-intersecting; `top` > `base`; face planar within 1e-6 m.
- **`points`**: an ordered list of a fixed number of 3D points (`count` in the slot declaration). Used by panel-type objects placed on four corners and by line-based objects (two points).

### 5. Instance `overrides`

`overrides` is an input slot of type `overrides` that belongs to the placed instance, never to a variant or type (spec §4.11). It is a list of edits addressed by grid ids:

| Edit | Effect |
|---|---|
| `{remove: "<segment id>"}` | The segment and its member are removed; the two cells on either side merge into one cell, whose id is the lower-left of the two and whose class is that cell's class. Removing a border segment is invalid. |
| `{segment: "<id>", cls: "<class>"}` | The segment's member class changes. |
| `{cell: "<id>", cls: "<class>"}` | The cell's class changes. |
| `{cell: "<id>" or segment: "<id>", component: <object id>, values: {…}}` | One member uses another object, or other values (a door in one cell, a deeper mullion at one line). |

Edits whose id no longer exists after the layout changes are kept but ignored, and a check reports them, so a user who changes the module and changes it back gets their edits back. Keeping them means no edit is silently discarded.

### 6. IFC export

The element that owns the grid exports as the assembly it is in IFC (`IfcCurtainWall` aggregating its members with `IfcRelAggregates`); each placed member exports as its own object's IFC class, with its own property sets and type. Railings export as `IfcRailing` with their posts, rails and balusters as parts where IFC's element decomposition allows it *(status: to_verify against IFC 4.3 element decomposition)*.

### 7. Archetypes

No new archetype. The `grid` operation is a recipe capability that any archetype may use:

- **wall** archetype: curtain walls (`IfcCurtainWall`) keep the wall archetype's base and top constraints, location line, joins and hosting, with a grid in place of layers.
- **area** archetype: sloped glazing and roof lights on a `face` surface; cladding and ceiling grids.
- **linear** archetype: railings use `layout` per path segment with `post` components at nodes and in the pattern.

### Example: catalogue object O-16, stick curtain wall (outline)

Parameters: `module` (u size, flexible), `spandrel_height`, `frame_classes` (`boundary`, `mullion`, `transom`, `corner`), `panel_classes` (`vision`, `spandrel`, `default`), `join` (default `u_continuous`), plus O-16's joint and glass parameters passed down to the components. Inputs: `surface` (baseline + base and top), `levels` (heights of the floors the façade passes), `overrides`. Recipe: the grid step above, `for_each` over segments and cells, and `instance` of the components. A user who removes transom `h2.3` gets one tall panel in column 3; a user who sets cell `c4.0` to a door component gets a door that fits the mullions on either side.

## Drawbacks

- The spec grows by two operations, one parameter type, two slot types, one instance slot, one attribute and four interfaces; every implementation must build them. The grid topology is the largest new piece in opo-recipe.
- Stable ids based on line numbers shift when lines are added at the start of a layout. Overrides then point at other members. Keeping orphaned overrides (rather than deleting them) limits the damage but does not remove it.
- Component slots make an object depend on other objects. Packaging must embed them (already required by §4.9) and libraries must version them together.

## Alternatives considered

- **Do it all in FEEL.** Each object writes its own division and cell logic with `for` loops. Rejected: results would differ between objects and between applications, and every curtain wall author would rewrite the same logic.
- **A dedicated curtain wall attribute** (`opo::curtain_wall` with fixed fields). Rejected: it fits curtain walls only, and the same machinery is needed for railings, cladding, ceilings and louvres.
- **Script step (WebAssembly, spec §4.15).** Rejected for this: grids are common, must be editable member by member, and must work in tools without a WebAssembly runtime.
- **Constraint-driven geometry** (reference planes and labelled dimensions, as some family editors use). Rejected by decision 0007: applications solve constraints; OPO stores rules and resolved geometry.

## Conformance tests

- `layout`: every distribution, origin and infill; `best_division` choice of *k* including the tie rule and the invalid case; `end_with`; `within` with unequal intervals; index numbering across intervals.
- `grid`: node, segment and cell counts and ids for straight, two-segment and arc baselines and a sloped face; default classes; `join` trimming values; panel outlines inset by reported face widths.
- `overrides`: segment removal and cell merge, class changes, component swap, orphaned overrides reported.
- Component checks: wrong interface, missing input.
- Object cases for a minimal stick curtain wall and a minimal railing (member counts, IFC classes of parts, volumes).

## Open questions

1. **Junction class.** Which IFC class do junctions and fixings (spider fittings, clamps, brackets) export as: `IfcMember`, `IfcDiscreteAccessory` or `IfcMechanicalFastener`?
2. **Non-rectangular grids.** Diagonal grid lines are left out of this version. Add later as a third grid direction?

## Resolved

- **Corners** (maintainer, 24 Nov 2026): the pattern restarts on each straight run of the baseline; corners get their own `corner` lines.
- **Archetype** (maintainer, 24 Nov 2026): curtain walls stay on the wall archetype, with a grid in place of layers.

## Prior art

OPO is vendor-neutral: nothing in this design depends on another tool. The design is checked against the tools architects already use, so that objects behave as users expect and can be mapped on import and export.

| This proposal | Archicad (GDL) | Revit | IFC 4.3 |
|---|---|---|---|
| `layout` distributions | Scheme grid: fixed size with pattern origin and infill, best division with "end with", number of divisions | Grid layout: fixed distance with justification, fixed number, maximum spacing | — |
| `grid` nodes, segments, cells | Curtain wall scheme grid | Curtain grid: lines, segments, cells | — |
| Segment and cell classes | Frame classes (boundary, mullion, transom), panel classes (main, distinct) | Border and interior mullion types; panel type | — |
| `component` parameters, `opo::interface` | GDL subtypes (curtain wall frame, panel, junction, accessory; railing post, panel) | Family-type parameters; mullion profile and curtain panel families | `IfcMember` MULLION, `IfcPlate` CURTAIN_PANEL |
| `join` | Frame junction settings | Join condition | — |
| `overrides` | Editing members in curtain wall edit mode | Removing grid segments; swapping panels | — |
| `points` slot | — | Adaptive placement points | — |
| Railing via `layout` along a path | Railing tool: nodes, segments, pattern | Railing type | `IfcRailing` |

## Sources

Behaviour described in our own words from the vendors' public help pages (no text or data copied):
- Graphisoft Archicad help: Curtain Wall Components; Set up Grid Pattern in Scheme Settings; Curtain Wall Junctions; Railing Settings overview; About the Railing Tool. GDL Reference Guide and GDL Basics (scripts, hotspots).
- Autodesk Revit help: About Family Templates; Curtain Wall Editing; curtain wall type properties.
- buildingSMART IFC 4.3: IfcCurtainWall, IfcMemberTypeEnum, element decomposition.
