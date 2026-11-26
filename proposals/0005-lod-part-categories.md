---
stage: 2          # 0 idea | 1 draft | 2 candidate | 3 final | withdrawn | rejected
issue: "#NN"
spec_version: "0.2"
---

# 0005. Levels of detail follow part categories

## Summary

Every part of an object gets a category from a fixed list. One shared table says, for each view (plan, section, elevation) and each level of detail (low, medium, high), whether parts of that category are drawn from the 3D, left out, or replaced by the object's symbol. Objects follow the table instead of keeping their own `exclude_parts` lists, and a project can change the table once for every object (decision 0027).

## Motivation

Today the door's low plan leaves out `Leaf` and `Hardware`, its medium plan also `Stop` and `Casing`; the window, stairs and railings each chose their own lists. An office that wants casings shown at medium detail would have to edit every object. A new object author has no rule to follow.

## Design

### 1. Part categories

A geometry item with a `part` also names its `category`. The list is fixed by the spec:

| Category | Examples |
|---|---|
| `structure` | wall core, slab, stringer, landing, beam |
| `insulation` | insulation layer |
| `finish` | plaster, render, cladding, floor finish layers |
| `membrane` | vapour barrier, waterproofing |
| `frame` | door lining, window frame, curtain-wall mullion and transom |
| `leaf` | door leaf, moving door panel |
| `sash` | window sash, opening light |
| `glass` | glazing, glass infill |
| `panel` | solid infill, spandrel, back panel |
| `trim` | casing, architrave, stop, cover strip, bead |
| `sill` | sill, threshold |
| `lintel` | lintel, head member |
| `hardware` | handles, hinges, locks, brackets, fixings |
| `tread` | treads, risers, nosings |
| `railing` | posts, rails, balusters, infill of a guard |
| `other` | anything else (must carry a `note`) |

The part name stays free text (`"Casing"`); the category is what drawing rules use.

### 2. The level-of-detail table

Each cell is one of:

- `show` — drawn from the 3D (cut or projected, as the view's method says);
- `hide` — left out;
- `symbol` — left out of the 3D-derived drawing; the object's overlay for that category is drawn instead (a door leaf drawn open with its swing). If the object has no overlay for it, the category is shown.

Default table (a drafting convention, provenance `typical`):

| Category | Plan low | Plan medium | Plan high | Section and elevation low | medium | high |
|---|---|---|---|---|---|---|
| structure | show | show | show | show | show | show |
| insulation | hide | show | show | hide | show | show |
| finish | hide | show | show | hide | show | show |
| membrane | hide | hide | show | hide | hide | show |
| frame | show | show | show | show | show | show |
| leaf | symbol | symbol | symbol | show | show | show |
| sash | symbol | symbol | symbol | hide | show | show |
| glass | show | show | show | show | show | show |
| panel | show | show | show | show | show | show |
| trim | hide | hide | show | hide | show | show |
| sill | show | show | show | show | show | show |
| lintel | hide | hide | hide | hide | show | show |
| hardware | hide | hide | hide | hide | hide | show |
| tread | show | show | show | show | show | show |
| railing | show | show | show | show | show | show |
| other | show | show | show | show | show | show |

At low detail a window sash is left out of sections and elevations (the frame shows the opening); a door leaf stays. Lintels are not drawn in plan at any level (they sit above the cut); a project can switch them on.

At low detail a wall is drawn as its outline with one fill (decision 0011 poché rules); hiding finish and insulation layers gives exactly that.

### 3. 3D views

The table applies to plans, sections and elevations only. A 3D view shows the high-detail model by default. Objects still carry their low and medium models, so an application with a level-of-detail switch for 3D (for large models or slow machines) can show them; the choice is the application's or the user's, not the object's.

### 4. Where the table lives, and overrides

- The default table is part of the spec, in `spec/` and as a schema-validated file (`schema/<version>/lod-table.json`).
- A project (or an office drawing style) may override any cell; the override applies to every object in the project.
- An object may override a cell for itself in its representation (`derive.lod_exceptions: {trim: show}`) with a `note` saying why. The project override wins over the object's exception, so an office keeps control.

### 5. Replaces `exclude_parts`

`derive.exclude_parts` stays readable for one version and is then removed. Library objects move to categories.

## Drawbacks

- One more field per geometry item. The class templates fill it for their standard parts.
- A fixed list will miss some cases; `other` with a note covers them until the list grows by proposal.

## Alternatives considered

- **Keep per-object lists.** The current drift.
- **Free-form tags chosen by authors.** Flexible, but two authors would invent different tags and the table could not be shared.

## Conformance tests

- The fixture door's three plans, generated from the default table, match today's output (leaf as symbol, hardware hidden, trim hidden at low and medium).
- A project override `trim: show` at plan medium adds the casings to the medium plan of every fixture object.
- An item without a category fails the check.
- A project override `lintel: show` at plan high draws the fixture window's lintel in its high plan.
- The fixture window's low elevation has no sash; its medium elevation has one.

## Open questions

None. Settled by the maintainer on 26 November 2026: 3D shows high detail by default, with lower levels available to applications that offer a switch; lintels are hidden in plan by default (projects can switch them on); a window sash is hidden in low-detail sections and elevations and shown from medium; a door leaf is always shown there (maintainer, 26 November 2026, which split `sash` from `leaf`).
