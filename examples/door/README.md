# Door — reference test object #1

A generic single swing door, written as a real IFCX document with the `opo::` extension. It is the first object used to shape the OPO spec (see [spec outline §10](../../spec/OUTLINE.md)). It is a working draft: the attribute layouts here are what the JSON Schema for each `opo::` attribute will be written from.

```
single-swing-door/          unpacked .opo (zip root)
├── object.ifcx             type node, opo:: definition, baked fallback
└── layers/
    ├── variants-metric.ifcx      80×210, 90×210, 100×210 with frame = wall (overall sizes)
    ├── variants-imperial.ifcx    2'6" × 6'8" and 3'0" × 6'8" (US sizes name the leaf)
    └── ruleset-us-ada.ifcx       replaces the accessibility minimum with ADA's 32"
project-snippet.ifcx        NOT part of the .opo: how a project places an instance
```

All lengths are in metres and angles in degrees (IFCX defaults).

## What it demonstrates

| Spec feature | Where |
|---|---|
| IFC class, IFC properties readable by any IFC5 tool | `bsi::ifc::class` = IfcDoor; `bsi::ifc::prop::OverallWidth/OverallHeight/OperationType` on the type node |
| Parameters with per-unit-system steps | `opo::parameters` (e.g. width step 10 mm metric, ½" imperial) |
| Visibility conditions | `frame_depth` hidden when `frame_follows_wall` |
| FEEL derived values and checks | `opo::rules` — leaf size, clear width, hinge point; four checks |
| Regional rule set, swapped by a layer | `accessibility` rule set: generic 800 mm, ADA layer `inch(32)` |
| Host input | `host.thickness` drives the void and, optionally, the frame depth |
| Geometry recipe | `opo::recipe` — rectangles, 2D difference, extrude, rotate, line, arc, polyline |
| Three levels of detail × model / plan / elevation / section | `opo::representations` (10 entries) |
| Authored vs derived 2D, with overlays | `plan.high` = cut from `model.high` + authored open leaf and swing arc |
| Semantic line classes and hatches | `class: cut / projected / annotation`, `hatch: frame_material` |
| Void cut in the host | `opo::host.void` → recipe step `void`; baked as an invisible `IfcOpeningElement` child |
| Flip axes, insertion point, snap points, handles | `opo::host`, `opo::handles` |
| IFC mapping per instance | `opo::ifc` — e.g. OperationType from the hinge-side flip |
| Variants as IFCX inheritance | variant nodes `inherits` the type node and set `opo::values` |
| Instance in a project | `project-snippet.ifcx`: inherits the 90×210 variant, overrides width and hinge side, placed with `usd::xformop` |
| Baked fallback | `usd::usdgeom::mesh` on Frame, Leaf, Void; plan symbol as `usd::usdgeom::basiscurves` under a hidden `PlanMedium` node |

## How it was checked

- Every `opo::` attribute used is declared in [`schema/opo@v0.1.ifcx`](../../schema/opo@v0.1.ifcx); no dangling `children`/`inherits` references.
- Every name used in a recipe argument resolves to a parameter, derived value, host input or earlier recipe step; every representation and the host void point at existing recipe steps.
- All formulas were evaluated for the defaults and every variant. Baked meshes and the plan arc match the recipe exactly for the default values.
- Check results: the default 90 cm (overall) door gives 760 mm clear width and **warns** under the generic 800 mm accessibility rule, which is intended. The US 3'0" door gives 876 mm clear and passes ADA; the 2'6" door fails it.

## Known limits of this draft

- IFCX alpha has no exact solids, so the baked fallback is a mesh. Exact geometry comes from the recipe.
- Variants inherit the baked geometry of the default size. A plain IFC5 viewer shows every variant at 90×210 unless the variant carries its own baked children. Whether variants should always bake is an open question.
- IFCX has no 2D drawing contexts yet; the baked plan symbol is stored as hidden curves tagged with `opo::representation`.
- FEEL lists are 1-indexed: `hinge[1]` is x, `hinge[2]` is y.
- Material slots use names and colours only; classification URIs (bSDD) are still to be added.
- The schema and rule set URIs on opo-format.org are not published yet.
