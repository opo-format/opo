# 4. Anatomy of an `.opo` file

## 4.1 Identity
Name, unique ID, object version, author, licence, OPO spec version, description, tags, preview image.

## 4.2 Parameters
Typed values: length, angle, number, integer, boolean, choice (enum), text, material slot, colour, and two structured types:
- `layers` — an ordered build-up, each entry `{material, thickness, function, core}` (walls, slabs, roofs, coverings). A wall or slab *type* is a set of layers.
- `property_set` — one IFC property set with its properties (name, IFC measure type, enumeration values). Values are data entered by the user or set by a `value` formula; they are written to IFC unchanged. Class templates generate one per applicable IFC property set; sets that apply to many classes are marked `optional`.
Each has: unit, default, limits (min/max/step or allowed list), UI label and group, visibility conditions.

**Units.** Values are always *stored* in IFCX's default units: lengths in **metres**, angles in degrees (IFCX alpha still lists radians vs degrees as undecided; OPO follows whatever IFCX settles on). Applications *display* and accept any unit (mm, m, ft-in…). Stored numbers are full double precision and never rounded on save (1/16" = 0.0015875 m must round-trip exactly). Limits and steps may be given per unit system (e.g. step 10 mm metric, ½" imperial), so sliders and snapping feel native in both.

## 4.3 Input slots
Drawn geometry the object is built from. Examples:
- Window/door: `outline` (closed flat profile in the object's plane), default = rectangle from width × height
- Stair: `walkline` (flat curve) with segments marked flight/landing and corners marked landing/winder
- Railing, fence: `path`
- Slab, roof: `boundary` + `holes`

Each slot declares: geometry type, plane, default, validity rules (closed, non-self-intersecting, min size, fits host).
Applications edit slots in their own way (in Curva: double-click → sketch mode). The format only defines the slot.

**Driving vs driven:** an object may switch between parameters driving the input (rectangle mode) and the input driving read-only parameters (custom outline mode).

**Constraints:** sketch constraints (dimensions, parallel, tangent) are solved by the application. OPO stores only the resolved geometry and the slot's validity rules. Optional constraint hints may be added in a later version.

## 4.4 Rules
- **Derived values:** formulas from parameters and inputs (leaf width = width − 2 × frame; riser count = ceil(height ÷ max riser)).
- **Checks:** conditions with messages ("double leaf needs width ≥ 1200 mm").
- **Regional rule sets:** referenced, swappable sets of limits (stair riser/going, guard heights) per country or code. Rule sets and variants carry each market's standard sizes (a US door is 36"×80", not a converted 900×2100).
  - The object declares the rule sets it reads in `opo::rules.rulesets` (`id`, `default`, `note`, `fields`). Each regional rule set is its **own node** with `opo::ruleset` (`id`, `label`, `uri`, `source`, `note`, `values`), usually in a layer file (`layers/ruleset-iso-21542.ifcx`). The application picks at most one rule-set node per declared id; formulas read its values as `rules.<id>.<field>`, and `rules.<id>` is `null` when none is picked (decision 0020).

**Formula language: FEEL subset.** Formulas use FEEL (Friendly Enough Expression Language) from the OMG DMN standard: an open standard by a neutral body, readable by non-programmers, with several open implementations. OPO allows a listed subset only:
- numbers, strings, booleans, `null`, lists (`[x, y]` for points; FEEL indexes from 1, so `p[1]` is x, and `p[-1]` is the last item), contexts (`{width: 0.1, depth: 0.2}`) and context access (`host.thickness`); a path on a list maps over it (`layers.thickness` is the list of thicknesses)
- arithmetic, comparisons (`=`, `!=`, `<`, `<=`, `>`, `>=`), `and`/`or`/`not`, `if … then … else`
- `min`, `max`, `abs`, `round`, `ceiling`, `floor`, `sqrt`, `modulo`
- lists: `for x in list return expr`, ranges `1..n` (FEEL: a range runs downwards when the start is larger), `sum`, `count`, `sublist`, `append`, `concatenate`, `reverse`, `index_of`, `list_contains`, `flatten` (deep, as in FEEL)
- `null` propagates through arithmetic and comparisons; `and`/`or` use three-valued logic; `sum([])` is `null` (FEEL), so formulas append a 0 where a list may be empty
- numbers are IEEE 754 double precision (not FEEL's 34-digit decimals); `=` and `!=` treat numbers within 1e-9 of each other as equal, so formulas on lengths compare reliably; `<`, `<=`, `>` and `>=` use the same tolerance, so numbers that are equal are never also less or greater
- ranges (`1..n`) are only used as the source of a `for` loop, as in FEEL
- FEEL functions whose names contain spaces are spelled with underscores: `index_of`, `list_contains` (FEEL: `index of`, `list contains`)
- `round(n)` / `round(n, scale)` rounds half to even, like FEEL `decimal(n, scale)`; a value within 1e-9 of a half (after scaling) counts as a half, so `round(2.675, 2)` is 2.68 as with decimals, although the double 2.675 is slightly below it
- conformance cases: `conformance/feel/` in this repository (created with the prototype interpreter, since retired; opo-rs is the reference implementation)
- OPO additions: trigonometry in degrees (`sin`, `cos`, `tan`, `atan2`); unit helpers returning canonical values (`mm()`, `cm()`, `m()`, `inch()`, `ft()`, `deg()`); curve queries (`length(curve)`, `point_at(curve, t)`…)

Formulas only ever see canonical units (metres, degrees), so the same object gives the same result everywhere. Examples:
```
leaf_width = width - 2 * frame_width
risers     = ceiling(height / max_riser)
leaves     = if width >= mm(1200) then 2 else 1
```
Names are `snake_case`. Every value in a recipe argument, derived value or check is a FEEL expression string; text literals are FEEL strings (`"left"`). The exact subset and its conformance tests are defined in the spec; implementations may use any FEEL engine or OPO's own evaluator.

## 4.5 Geometry recipe
A chain of operations from a small, strictly specified vocabulary (a node graph stored as data):

- **2D:** `line`, `arc`, `polyline`, `polygon`, `rectangle`, `circle`, `band` (region between two offsets of a path, mitred: wall layers, beams in plan), `difference`, `union`, `boundary_curves` (edges of a region), `text`; planned: fillet, offset of regions
- **Curve queries:** length, point at, divide into N, perpendicular at, offset *(planned)*
- **3D:** `extrude` (a region along its plane's normal), `sweep` (a profile drawn in its own u/v plane along a 3D path), `revolve`, `loft` (a solid through closed 3D sections), `box`, `cylinder`, `path3` (3D axis curve); `union` of solids is a collection (no CSG needed for drawing); planned: solid difference
- **Patterning:** `for_each` (repeat a geometry expression over a list or range; each result keeps its item, so representations can use `each.material`), mirror
- **Transform:** `move`, `rotate`, `mirror`
- **Placement:** `instance(object_id, values, inputs)` places a nested OPO by id with values and drawn inputs; a packaged `.opo` embeds the nested objects it uses (§4.9)

**Operations and their arguments.** Argument names are fixed; optional arguments in brackets. Every argument is a FEEL expression (or a literal). Points are `[x, y]` in the step's plane or `[x, y, z]` in object space.

| Operation | Arguments | Result |
|---|---|---|
| `rectangle` | `min`, `max` | 2D region, axis-aligned |
| `polygon` | `points` | 2D region from a closed point list |
| `circle` | `center`, `radius`, [`segments`] | 2D region |
| `polyline` | `points` | 2D open curve |
| `line` | `start`, `end` | 2D curve |
| `arc` | `center`, `radius`, `start_angle`, `end_angle`, [`segments`] | 2D curve, angles in degrees, counter-clockwise |
| `band` | `path`, `left`, `right` | 2D region between two offsets of a path (positive = left of travel), mitred joins |
| `difference` | `a`, `b` | 2D region `a` minus `b` (either may be a list) |
| `union` | `items` | regions on one plane: exact union; anything else: a collection |
| `boundary_curves` | `region` | the boundary curves of a region |
| `text` | `at`, `value`, [`height`] | annotation text; height in printed metres (default 0.0025) |
| `extrude` | `profile`, `from`, `to` | solid: the region moved along its plane's normal from `from` to `to` |
| `sweep` | `profile`, `path`, [`roll`] | solid: a `profile`-plane region along a 3D path; `roll` in degrees about the path |
| `loft` | `sections` | solid through two or more closed 3D point lists with the same number of points: point *i* of each section joins point *i* of the next by straight lines (two triangles per quad), and the first and last sections are capped; a closing point equal to the first is ignored (proposal 0003) |
| `revolve` | `profile`, `center`, `axis`, `angle`, [`segments`] | solid: region revolved about an axis through `center` |
| `box` | `min`, `max` | solid, axis-aligned, 3D corners |
| `cylinder` | `start`, `end`, `radius`, [`segments`] | solid between two 3D points |
| `path3` | `points` | 3D curve (axes, paths) |
| `move` | `geometry`, `by` | translated copy (2D or 3D vector) |
| `rotate` | `geometry`, `center`, `angle` | rotated copy about `center` (2D) or the z axis through `center` (3D), degrees |
| `mirror` | `geometry`, `axis` | mirrored copy across the object's x or y axis (`"x"` or `"y"`) |
| `for_each` | `items`, `do`, [`as`, `index`] | `do` evaluated per item (`as` default `item`, `index` from 1); each result keeps its item as `each` |
| `instance` | `object`, [`values`, `inputs`, `representation`] | a nested object's geometry (default representation `model.medium`) |

`segments` is a hint for tessellation; implementations may use more. Conformance checks volumes of curved solids with a tolerance (see `conformance/README.md`).

Planes: `xy`, `xz`, `yz`, and `profile` (the local plane of a swept profile: u across, to the left of the direction of travel; v up). Reference evaluator: `opo-recipe` in opo-rs.

Keep this list short: every operation is a cost for other implementers.

Each recipe step is `{ "id", "op", "plane"?, "when"?, "args" }`. Arguments are FEEL expressions over parameters, derived values, host inputs and the ids of earlier steps. Operations may also be called inline inside an argument (`extrude(profile, from, to)`, `circle(center, radius)`), so small helper shapes need no step of their own. `when` is a FEEL condition: a step whose condition is false produces nothing, and unions skip it (e.g. a threshold, or a key rose that is switched off). Planes: `xy` (plan, normal +z), `xz` (object face, normal +y), `yz`. Object axes: x along the host (wall), y through the host (positive = swing/front side), z up.

## 4.6 Representations
Each representation is tagged with:
- **View context:** model (3D), plan, reflected plan, elevation, section
- **Detail level / scale range:** e.g. low (≤1:200), medium (1:100–1:50), high (≥1:20)
- **Source:** authored 2D (symbols, drawing conventions) or derived from 3D (cut / projected)

Typical door:
| | Low | Medium | High |
|---|---|---|---|
| 3D | Box with opening | Frame + leaf | Frame, leaf layers, hardware, seals |
| Plan | Line + arc (authored) | Frame + leaf + arc (authored) | Cut from 3D |
| Elevation | Outline | Outline + frame | Projected from 3D |

Aligns with IFC geometric representation sub-contexts (target view + target scale).

**Materials, hatches and styles travel with the object.** An imported wall, slab or any other object keeps its look: OPO embeds the full definitions, not just names that the receiving file may not have.
- `opo::hatches` — hatch pattern definitions, embedded in the file:
  - `kind`: `solid` | `lines` | `none`.
  - `lines`: a list of **line families**, each with `angle`, `origin` [x, y], `offset` [along, across] and optional `dashes` (positive = dash, negative = gap, 0 = dot, repeating from the line's origin; omitted = continuous). This is the model used by IFC (`IfcFillAreaStyleHatching`) and by common CAD pattern files, so patterns convert both ways without loss. Brick coursing, insulation zigzag (as short dashed families), concrete, timber grain and earth patterns are all expressible.
  - `scale_mode`: `model` (sizes are real lengths, e.g. 65 mm brick courses that stay true at every scale) or `paper` (sizes in mm on the printed sheet, for symbolic patterns that keep the same density at every scale).
  - optional `colour`, `background` (fill colour behind the lines), `line_weight` (otherwise from the line class).
- `opo::materials` — material definitions: `name`, `category` (concrete, masonry, steel, timber, insulation, glass, finish, membrane, earth, other), IFC material name, render `colour`, `cut` (hatch used where the material is cut in plan and section), `surface` (optional pattern on surfaces seen in elevation or plan, e.g. tile or cladding joints) and data (density, thermal conductivity) for quantities.
- Every layer of a layered element (walls, slabs, roofs, coverings) and every material slot points to a material. Plans and sections draw each cut layer with its material's cut hatch; layer boundaries are `cut` lines, the outer boundary a heavier `cut` line (weights from the drawing style).
- **Joins merge by material, not by hatch:** where two walls or slabs meet, layers of the same material join without a line between them, others keep their boundary.
- **Precedence** when drawing: (1) the project's drawing style, if it overrides a material or category; (2) the hatch embedded in the object's material; (3) the application's default for the category. The project chooses per import whether to keep the object's hatches (default) or map them onto the office standard by material category. Either way the embedded definitions stay in the object, so nothing is lost when it is passed on.
- **Shared styles:** a wall or slab type (layer build-up + materials + hatches) is a variant of the wall or slab class template. Types are shared as a `.opo` with several variants (one file per office wall library) or as a layer file, like VisualARQ style libraries or Revit types, but readable by any OPO application. A package may also hold only materials and hatches (`opo::object.kind` = `styles`) to share an office's material and hatch standard.
- **IFC export:** materials as `IfcMaterial` with `IfcMaterialLayerSet`; cut hatches as `IfcFillAreaStyle` with `IfcFillAreaStyleHatching` per line family (or a solid `IfcColourRgb`), and render colour as `IfcSurfaceStyle`, attached through `IfcMaterialDefinitionRepresentation`. IFCX alpha only stores a material name (`bsi::ifc::material` with a code), so in IFCX the definitions live in `opo::materials` / `opo::hatches` until IFCX gains presentation styles.

**Line and hatch semantics.** 2D representations carry meaning, not pen styles: every line is classed as *cut*, *projected*, *hidden*, *overhead* or *annotation*, and every hatch names the material it cuts. The application's drawing style maps classes to line weights, line types and hatch patterns, so drawings stay consistent with the office standard across a project.

## 4.7 Host behaviour
- Hosted objects (door, window, opening) declare the void they cut in their host (wall, slab, roof).
- Level-attached objects (stair) declare bottom/top attachment and the slab opening they cut.
- Flip/mirror axes, insertion point, snapping points.

## 4.8 Handles
Viewport handles mapped to parameters or input points (drag width, swing arc, sill height).

## 4.9 Nested OPOs
An OPO may place other OPOs (stair → railing → balusters; kitchen run → cabinets). Parameters can be passed down.

## 4.9a Ports (distribution elements)
`opo::ports` lists the connection points of distribution elements: `name`, `system_type` (IFC `IfcDistributionSystemEnum`), `flow_direction` (SOURCE / SINK / SOURCEANDSINK), `port_type` (PIPE / DUCT / CABLE…), and FEEL expressions for `nominal_size`, `position`, `direction` and an optional `when`. They export as `IfcDistributionPort` nested in the element. OPO does not route or size systems.

## 4.10 Data
- IFC class and predefined type (e.g. IfcDoor / DOOR)
- Property sets (standard IFC psets + custom)
- Classifications (bSDD URIs, ETIM, Uniclass…)
- Material slots mapped to parts

## 4.11 Variants
Named parameter sets, optionally with saved input geometry. Basis for "types" in schedules.

## 4.12 Product binding (optional)
Manufacturer, product code, link, the sizes actually sold (constrains parameters), product data, and optionally the manufacturer's detailed geometry (e.g. from their IFC file) wrapped inside the generic object's representations.

## 4.13 Baked fallback
Ready-built geometry and plan symbols for the default variant, so viewers and tools that don't run the recipe can still show and export the object.

## 4.14 References (required for library objects)
OPO objects are not invented from scratch. Every object in an OPO library states, in `opo::object.references`:
1. **Parametric basis**: an established, openly licensed parametric object it is modelled on (e.g. dormakaba's CC0 *bim-all-doors* for doors), and what was taken from it. Only licences compatible with the target library (CC0, CC-BY) may be used; proprietary manufacturer objects can inform dimensions but not be copied.
2. **IFC parameters**: the IFC classes, property sets and properties its parameters map to, using IFC names wherever IFC has them.
3. **Norms for standard sizes**: the national or industry standards its size catalogues come from, for both metric and imperial markets (e.g. EN/ISO norms in Europe, BS 4787, US industry sizes; national norms of EU countries are not used).
4. **Rule sources**: the regulations behind its rule sets (e.g. ISO 21542, ADA).

Values that are typical practice rather than taken from a norm (e.g. hinge positions) are marked as such in a `note`.

**Provenance.** A node may carry `opo::provenance`: a map from the path of one of its values (`parameters.handle_height.default`, `values.nominal_width`, `ruleset.values.min_clear_width`) to `{source, status, note}`. `status` is `norm`, `maker`, `typical`, `illustrative` or `to_verify`; `norm` and `maker` need a `source`, the others a `note`. Applications may show the status next to a value; library objects marked stable have no `to_verify` value (decision 0017, proposal 0002).

**Size catalogues.** Standard sizes ship as layer files, one per norm or market. Each catalogue has one *system* node (inheriting the type) carrying that market's construction values (frame type, lining, gaps, leaf thickness, handle height…), and one variant node per standard size inheriting the system node. All markets use the same object; only the values differ. `opo::values` merges key by key along `inherits`: a variant's own values win over its system node's, a `null` value removes an inherited one, and of several inherited nodes the later one in `inherits` wins (decision 0020).

## 4.15 Script step (optional, rare)
For generators too complex for the recipe (e.g. balanced winder stairs):
- Compiled to **WebAssembly**, run sandboxed (no files, network or system access, time and memory limits).
- **Inputs:** parameters + input slots. **Output:** an ordinary OPO recipe and representations — never raw drawing commands.
- Tools without a WASM runtime use the baked fallback.

## 4.16 Class templates (every IFC class)
Every concrete IFC element class (150 in IFC 4.3) has an OPO **class template**, so any IFC element can be created parametrically and shared as a file, like a Revit family. This includes elements that other tools treat as non-shareable system types (walls, slabs, roofs, stairs, pipes, ducts).
- A class template is built on one of eight **archetypes**: point, linear, area, wall, hosted, flight, fitting, assembly. The archetype fixes inputs, base geometry, host behaviour and representations.
- The template adds the IFC class, every predefined type as a choice, the applicable IFC property sets as data parameters (they follow the chosen predefined type), base quantities as derived values, ports for distribution elements, and per-class defaults.
- Templates are **generated** from the pinned IFC schema, the IFC property and quantity set templates, the archetype definitions and one hand-written per-class table. They are regenerated when IFC changes.
- **Library objects** refine a template with real construction logic and drawing conventions, keeping the same class, types, property sets and ports. Authors (firms, manufacturers) start from a template or a library object.
- Details: `spec/objects/archetypes.md`; class list: the coverage table generated in the library repository (`opo coverage`).
- Built: all 150 IFC 4.3 element classes. Their sources are in the library repository (`templates/`); `opo generate` builds them. Frozen copies of the first nine are conformance fixtures (`conformance/fixtures/library/templates/`).
