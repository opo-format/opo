# Archetypes and class templates

**Draft v0.1 · 24 Nov 2026**

Every IFC 4.3 element class gets a **class template**: a working OPO that a user can place, edit and share, and that authors start from when they make a detailed object (like a Revit family template). Templates are built on eight **archetypes**. An archetype fixes the inputs, the base geometry, the host behaviour and the representations; the class template adds the IFC class, its predefined types, its property sets, its ports and its defaults.

The full class list with the archetype of each class is in `ifc-coverage.md`.

---

## 1. What every class template contains

| Part | Content | Source |
|---|---|---|
| Identity | `IfcXxx` class template, version, licence CC0 | generated |
| IFC class | `bsi::ifc::class` = the class; type node exports as its IFC type object (`IfcBoilerType`…) | schema |
| Predefined type | parameter `predefined_type`, a choice of every enumeration value of the class + USERDEFINED (with `object_type` text) + NOTDEFINED | schema |
| Property sets | for each IFC property set that applies to the class and the chosen predefined type, its properties as **data parameters** (typed by their IFC measure, grouped by property set, empty by default, written to IFC unchanged). Applicability changes with the predefined type, so the parameter list follows the choice | IFC 4.3 property set templates (760, with their applicable classes) |
| Quantities | the matching `Qto_` base quantities as **derived values** from the geometry (length, area, volume, weight where a density is set) | IFC 4.3 quantity set templates |
| Geometry | the archetype's base geometry and parameters (below), with per-class defaults | archetype + per-class defaults table |
| Ports | distribution elements only: one port per connection with system type, flow direction, nominal size and position (see §3) | per-class defaults table |
| Representations | three levels of detail per the archetype, plan symbol by class (§4) | archetype + symbol table |
| Materials | material slots named by role (`body`, `finish`, `insulation`…), per archetype | archetype |

**Generated, not hand-written.** A generator (Rust, part of the reference crate) builds every class template from: the IFC schema of the pinned IFC version, the IFC property and quantity set templates, the eight archetype definitions, and one small **per-class table** (`templates/classes.csv`): default size, archetype options, ports, plan symbol and default material. When IFC changes, the templates are regenerated. Hand edits go into the per-class table, never into the generated files.

**Template versus library object.** A template's geometry is honest but simple (a boiler is a cased box with its connections; a sensor is a small body on its host). A library object (from a sheet) replaces the archetype geometry with real construction logic and drawing conventions, but keeps the same class, types, property sets and ports. Users see one list per IFC class: the template first, then library objects, then their own.

---

## 2. The eight archetypes

### point — placed equipment or component

**Used by** most distribution elements (plant, terminals, controllers, sensors, alarms, storage, treatment), components (accessories, fasteners, signs, dampers, bearings), furniture, geographic elements, vehicles, lifts, footings, mooring and navigation devices.

**Inputs** insertion point + orientation; optional host (wall, slab, ceiling, roof, another element) with a mounting mode: `free` | `on_face` (offset from the face, e.g. a sensor on a wall) | `in_face` (recessed, cuts its own niche in the host) | `under` (hung from a slab or beam).

**Geometry parameters** `shape` box | cylinder | profile_extrusion | sphere · `width`, `depth`, `height` (or `diameter`) · `corner_radius` · `mount_height` (above the level or the host bottom) · `clearance` (service and access zone, front/sides/top: drawn as a dashed zone and used for clash checks).

**LOD** low: symbol only (class symbol in plan, outline in elevation) · medium: body with clearance zone · high: body with plinth/feet/brackets and port stubs.

**IFC export** extruded solid (box, cylinder, profile) or swept solid; the clearance zone is not exported as geometry by default *(optional export as a space or virtual element: to decide)*.

### linear — profile along a path

**Used by** beams, columns, members, piles, rails, kerbs, railings (simple), track elements, reinforcing bars, tendons, pipe, duct, cable, cable carrier and conveyor segments.

**Inputs** `path` (line, polyline, arc or curve; columns and piles default to a vertical line between two levels).

**Geometry parameters** `profile` (from the shared profile library or drawn: I, U, L, T, rectangle, circle, hollow sections, ducts rectangular/round/oval, pipe by nominal size) · `justification` (9-point) · `rotation` about the path · `start_extension`, `end_extension` · `end_cut` square | mitre | angle. Distribution segments add `nominal_size`, `insulation_thickness`, `lining_thickness`.

**LOD** low: centre line (single line for pipes and ducts ≤ the scale threshold, as drawing conventions require) · medium: profile outline, double line · high: insulation, flanges/joints at set spacing.

**IFC export** `IfcExtrudedAreaSolid` (straight) or `IfcSweptDiskSolid` / `IfcFixedReferenceSweptAreaSolid` (curved); the profile as the matching IFC profile definition.

### area — boundary with thickness or layers

**Used by** slabs, roofs (flat or by slopes), coverings, pavements, courses, plates, earthworks fill, reinforced soil, reinforcing mesh, geotechnical strata.

**Inputs** `boundary` (closed profile) + `holes`; plane (horizontal, sloped by angle or by a slope arrow, or a host face).

**Geometry parameters** `layers` (build-up: ordered list of material + thickness + function, e.g. finish / screed / insulation / structure; one layer = a simple thickness) · `reference` top | bottom | core (which face sits on the boundary plane) · `edge` square | perpendicular | chamfer per edge · roofs: `slopes` per edge (hip/gable/flat), `overhang`, `fascia`.

**LOD** low: outline · medium: total thickness with layer lines in section · high: every layer hatched, edge details.

**IFC export** extruded solids per layer, or one solid with `IfcMaterialLayerSetUsage`.

### wall — path, height and layers (or a grid)

**Used by** walls (all predefined types), curtain walls (with grid and panels, see O-16), chimneys (closed path).

**Inputs** `path` (line, polyline, arc or curve) · base and top constraint (levels + offsets, or an unconnected height, or attached to a roof/slab underside) · optional `profile` in elevation (non-rectangular wall shapes, as windows do with their outline).

**Geometry parameters** `layers` (as area) with `location_line` (core centre, finish face exterior/interior…) · `join` automatic | butt | mitre at ends and corners · curtain wall: grid, panels, joints (see O-16 shared rules).

**Hosting** walls are hosts: doors, windows and openings cut them; joins with other walls clean up layer by layer (core to core, finish to finish).

**LOD** low: two lines (poché by class) · medium: layer lines · high: every layer hatched and joined.

**IFC export** `IfcExtrudedAreaSolid` along the axis with `IfcMaterialLayerSetUsage`; axis representation for the path.

### hosted — sits in or on a host and changes it

**Used by** doors, windows, shading devices, openings and voids, projections, surface features (texturing, marking), earthworks cuts.

**Inputs** host (wall, slab, roof, curtain-wall cell, terrain) + position; `outline` (closed profile, rectangle by default, editable like windows).

**Geometry parameters** `width`, `height` (or the outline) · `depth` (through or a set depth) · `side` for one-sided features · the void it cuts or the volume it adds.

**LOD** per object (door and window conventions are in O-01 and the openings sheet); voids: dashed outline in plan where above the cut plane.

**IFC export** the element plus its `IfcOpeningElement` (`IfcRelVoidsElement` / `IfcRelFillsElement`), or an `IfcProjectionElement` (`IfcRelProjectsElement`), as IFC requires.

### flight — level to level

**Used by** stairs, stair flights, ramps, ramp flights (lifts and escalators use `point` and the transport sheets).

**Inputs** base level, top level, `walkline` (straight by default; curve for winders, see C-04).

**Geometry parameters** riser/going or slope rules from a rule set (`stairs`, `accessibility`), width, landings, structure type; nested railings.

**LOD** per the circulation sheets.

**IFC export** `IfcStair`/`IfcRamp` aggregating flights and landings.

### fitting — joins the ends of segments

**Used by** pipe, duct, cable and cable carrier fittings (elbows, tees, crosses, reducers/transitions, caps, junctions, offsets).

**Inputs** the ports it connects: placed by snapping to segment ends (the application places fittings automatically when segments meet, like routing tools do).

**Geometry parameters** `predefined_type` decides the form: BEND (angle, bend radius as a factor of size), JUNCTION (tee/cross, branch sizes), TRANSITION (size A → size B, length, concentric/eccentric), OBSTRUCTION/CAP, CONNECTOR · sizes follow the connected segments.

**LOD** low: symbol on the single line · medium: body · high: flanges/sockets.

**IFC export** swept solid along the fitting's centre line; ports as `IfcDistributionPort` nested with `IfcRelNests`.

### assembly — nests other OPOs

**Used by** `IfcElementAssembly` (all its predefined types: trusses, braced frames, rigid frames, slab fields, reinforcement units, abutments…) and any library object that is a composition (entrance door assembly, kitchen run, unitised curtain wall unit).

**Inputs** whatever the assembly needs (a path for a truss, a boundary for a slab field, a level range for a frame) + the nested OPOs with parameter passing (spec §4.9).

**IFC export** `IfcElementAssembly` with its parts by `IfcRelAggregates`.

`any` — for generic classes (`IfcBuildingElementProxy`, `IfcBuiltElement`, `IfcCivilElement`) the user picks the archetype.

---

## 3. Ports (distribution elements)

Every distribution element template has its ports in the per-class table: `name`, `system_type` (IFC `IfcDistributionSystemEnum`: e.g. DOMESTICHOTWATER, VENTILATION, ELECTRICAL), `flow_direction` SOURCE | SINK | SOURCEANDSINK, `connection` (pipe/duct/cable), `nominal_size` (parameter), and position on the body (a face + offset, from parameters). Ports export as `IfcDistributionPort` nested in the element. OPO does not route or size systems; ports exist so MEP tools and the app's routing can connect to the object.

---

## 4. Plan symbols for classes without a drawing convention

Many IFC classes (sensors, valves, dampers, alarms, plant) have no single international plan symbol. Templates use a neutral default: the body outline at medium/high, and at low a circle or square with a short class code (e.g. `SNS` sensor, `VLV` valve, `ALM` alarm), all as semantic line classes (spec §4.6). Offices or national standards replace symbols with a **symbol layer** (one layer file per symbol set) without touching the objects.

---

## 5. Per-class defaults table (`templates/classes.csv`)

One row per class (and optionally per predefined type) with: archetype, default shape and size (metric / imperial), mount mode, clearance zone, ports, symbol code, default material, and whether the class is a host. The first version fills sizes as "typical" values only where they are obvious (furniture, sanitary, doors); for the rest the default is a neutral size the user changes, and the row is marked *(to collect)* until real maker or norm sizes are added. Rows never invent precise norm values.

---

## 6. Status (24 Nov 2026)

One class template per archetype is built (sources in the library repository, `templates/`; built and checked by `opo generate` and `opo check`; frozen copies in `conformance/fixtures/library/templates/`):

| Archetype | Template | What it proves |
|---|---|---|
| wall | `IfcWall` | layer build-up with embedded materials and hatches, location line, storey or unconnected top, host for openings, 5 example wall types as a layer |
| area | `IfcSlab` | boundary + holes, layers from the top, reference face, areas and perimeter by formula, 3 example slab types |
| linear | `IfcBeam`, `IfcMember` | seven parametric profiles mapped to IFC profile definitions, justification, roll, end extensions; IPE 270 example |
| point | `IfcBoiler` | body, mounting, clearance zone, four ports (heating flow/return, gas, flue) |
| fitting | `IfcPipeFitting` | form follows the predefined type (bend, junction, transition, cap, connector), ports per type |
| hosted | `IfcOpeningElement` | wall or slab host, rectangle or custom outline, opening or recess, void cutting the host |
| flight | `IfcStair` | riser count from the rise, waist or solid, plan with cut line and walking line, rule-set checks |
| assembly | `IfcElementAssembly` | Warren/Pratt truss built from nested `IfcMember` templates |

Every template is checked for: declared attributes, resolvable names, evaluation at the defaults (no warnings), every predefined type, every choice and boolean option, every example type in its layers, IFC property names against the IFC 4.3 templates, mesh volumes against the quantity formulas, and baked geometry equal to the recipe output.

## 7. Order of work

1. ✅ One template per archetype (above).
2. The per-class table for all classes, then the generator → all class templates in the library repository.
3. Detailed library objects from the sheets, by priority, starting with the P1 objects.
