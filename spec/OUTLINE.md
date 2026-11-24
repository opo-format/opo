# OPO — Open Parametric Object

**Draft spec outline · v0.1 · 23 Nov 2026**
Status: strategy draft, not yet a specification. Decisions recorded in §11; everything else may still change.

OPO is an open, vendor-neutral file format for parametric architectural objects: doors, windows, stairs, railings, furniture and more. One OPO file is a *generator*: it describes how to build an object from parameters, with 3D at several levels of detail and proper 2D plan, elevation and section symbols at several scales.

Curva is the first application to implement OPO, but the format belongs to no single application.

- Name: OPO — Open Parametric Object (pronounced "oh-poh")
- File extension: `.opo`
- Home: github.com/opo-format · opo-format.org
- Schema addresses: `https://opo-format.org/schema/<version>/...`

---

## 1. Goals

1. **Objects that remember how they were made.** Change a parameter, redraw an outline, and the object rebuilds.
2. **Real architectural drawings.** Plan and elevation symbols follow drawing conventions by scale, not just slices of the 3D.
3. **Three levels of detail.** A door is a line and an arc at 1:200 and every layer of frame and leaf at 1:5.
4. **Adoptable by other software.** Small, strictly specified, text-based, openly licensed.
5. **IFC-native.** OPO complements the IFC family. An `.opo` is an IFCX document with an `opo::` extension: IFC vocabulary (classes, predefined types, property sets, representation contexts) used exactly, plus the recipe to rebuild the object. Exports clean IFC geometry (no meshes where exact geometry is possible). IFC5's first version leaves out parametric geometry; OPO fills that gap.
6. **Safe to open from anyone.** No object can touch files, the network or the computer.

## 2. Non-goals

- Not a mechanical/engineering CAD format.
- Not a project/model file. OPO defines objects; the project file stores placed instances.
- Not a rendering format. Materials are slots and references, not full shader definitions.

## 3. Core concepts

| Term | Meaning |
|---|---|
| **OPO** (definition) | One `.opo` file: a generator, e.g. "single swing door" |
| **Variant** | A saved set of parameter values (and optionally a saved outline), e.g. "90×210 oak" |
| **Instance** | One placed object in a model. Stores its own parameter values and input geometry. Lives in the project file, not the `.opo` |
| **Input slot** | A drawn-geometry input: point, line, polyline/curve, closed profile, region |
| **Representation** | One drawable version of the object for a given view and detail level / scale range |

## 4. Anatomy of an `.opo` file

### 4.1 Identity
Name, unique ID, object version, author, licence, OPO spec version, description, tags, preview image.

### 4.2 Parameters
Typed values: length, angle, number, integer, boolean, choice (enum), text, material slot, colour, and two structured types:
- `layers` — an ordered build-up, each entry `{material, thickness, function, core}` (walls, slabs, roofs, coverings). A wall or slab *type* is a set of layers.
- `property_set` — one IFC property set with its properties (name, IFC measure type, enumeration values). Values are data entered by the user or set by a `value` formula; they are written to IFC unchanged. Class templates generate one per applicable IFC property set; sets that apply to many classes are marked `optional`.
Each has: unit, default, limits (min/max/step or allowed list), UI label and group, visibility conditions.

**Units.** Values are always *stored* in IFCX's default units: lengths in **metres**, angles in degrees (IFCX alpha still lists radians vs degrees as undecided; OPO follows whatever IFCX settles on). Applications *display* and accept any unit (mm, m, ft-in…). Stored numbers are full double precision and never rounded on save (1/16" = 0.0015875 m must round-trip exactly). Limits and steps may be given per unit system (e.g. step 10 mm metric, ½" imperial), so sliders and snapping feel native in both.

### 4.3 Input slots
Drawn geometry the object is built from. Examples:
- Window/door: `outline` (closed flat profile in the object's plane), default = rectangle from width × height
- Stair: `walkline` (flat curve) with segments marked flight/landing and corners marked landing/winder
- Railing, fence: `path`
- Slab, roof: `boundary` + `holes`

Each slot declares: geometry type, plane, default, validity rules (closed, non-self-intersecting, min size, fits host).
Applications edit slots in their own way (in Curva: double-click → sketch mode). The format only defines the slot.

**Driving vs driven:** an object may switch between parameters driving the input (rectangle mode) and the input driving read-only parameters (custom outline mode).

**Constraints:** sketch constraints (dimensions, parallel, tangent) are solved by the application. OPO stores only the resolved geometry and the slot's validity rules. Optional constraint hints may be added in a later version.

### 4.4 Rules
- **Derived values:** formulas from parameters and inputs (leaf width = width − 2 × frame; riser count = ceil(height ÷ max riser)).
- **Checks:** conditions with messages ("double leaf needs width ≥ 1200 mm").
- **Regional rule sets:** referenced, swappable sets of limits (stair riser/going, guard heights) per country or code. Rule sets and variants carry each market's standard sizes (a US door is 36"×80", not a converted 900×2100).

**Formula language: FEEL subset.** Formulas use FEEL (Friendly Enough Expression Language) from the OMG DMN standard: an open standard by a neutral body, readable by non-programmers, with several open implementations. OPO allows a listed subset only:
- numbers, strings, booleans, `null`, lists (`[x, y]` for points; FEEL indexes from 1, so `p[1]` is x, and `p[-1]` is the last item), contexts (`{width: 0.1, depth: 0.2}`) and context access (`host.thickness`); a path on a list maps over it (`layers.thickness` is the list of thicknesses)
- arithmetic, comparisons (`=`, `!=`, `<`, `<=`, `>`, `>=`), `and`/`or`/`not`, `if … then … else`
- `min`, `max`, `abs`, `round`, `ceiling`, `floor`, `sqrt`, `modulo`
- lists: `for x in list return expr`, ranges `1..n` (FEEL: a range runs downwards when the start is larger), `sum`, `count`, `sublist`, `append`, `concatenate`, `reverse`, `index_of`, `list_contains`, `flatten` (deep, as in FEEL)
- `null` propagates through arithmetic and comparisons; `and`/`or` use three-valued logic; `sum([])` is `null` (FEEL), so formulas append a 0 where a list may be empty
- reference interpreter and conformance tests: `tools/feel.py`
- OPO additions: trigonometry in degrees (`sin`, `cos`, `tan`, `atan2`); unit helpers returning canonical values (`mm()`, `cm()`, `m()`, `inch()`, `ft()`, `deg()`); curve queries (`length(curve)`, `point_at(curve, t)`…)

Formulas only ever see canonical units (metres, degrees), so the same object gives the same result everywhere. Examples:
```
leaf_width = width - 2 * frame_width
risers     = ceiling(height / max_riser)
leaves     = if width >= mm(1200) then 2 else 1
```
Names are `snake_case`. Every value in a recipe argument, derived value or check is a FEEL expression string; text literals are FEEL strings (`"left"`). The exact subset and its conformance tests are defined in the spec; implementations may use any FEEL engine or OPO's own evaluator.

### 4.5 Geometry recipe
A chain of operations from a small, strictly specified vocabulary (a node graph stored as data):

- **2D:** `line`, `arc`, `polyline`, `polygon`, `rectangle`, `circle`, `band` (region between two offsets of a path, mitred: wall layers, beams in plan), `difference`, `union`, `boundary_curves` (edges of a region), `text`; planned: fillet, offset of regions
- **Curve queries:** length, point at, divide into N, perpendicular at, offset *(planned)*
- **3D:** `extrude` (a region along its plane's normal), `sweep` (a profile drawn in its own u/v plane along a 3D path), `revolve`, `box`, `cylinder`, `path3` (3D axis curve); `union` of solids is a collection (no CSG needed for drawing); planned: loft, solid difference
- **Patterning:** `for_each` (repeat a geometry expression over a list or range; each result keeps its item, so representations can use `each.material`), mirror
- **Transform:** `move`, `rotate`, `mirror`
- **Placement:** `instance(object_id, values, inputs)` places a nested OPO by id with values and drawn inputs; a packaged `.opo` embeds the nested objects it uses (§4.9)

Planes: `xy`, `xz`, `yz`, and `profile` (the local plane of a swept profile: u across, to the left of the direction of travel; v up). Reference evaluator: `tools/recipe.py`.

Keep this list short: every operation is a cost for other implementers.

Each recipe step is `{ "id", "op", "plane"?, "when"?, "args" }`. Arguments are FEEL expressions over parameters, derived values, host inputs and the ids of earlier steps. Operations may also be called inline inside an argument (`extrude(profile, from, to)`, `circle(center, radius)`), so small helper shapes need no step of their own. `when` is a FEEL condition: a step whose condition is false produces nothing, and unions skip it (e.g. a threshold, or a key rose that is switched off). Planes: `xy` (plan, normal +z), `xz` (object face, normal +y), `yz`. Object axes: x along the host (wall), y through the host (positive = swing/front side), z up.

### 4.6 Representations
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

### 4.7 Host behaviour
- Hosted objects (door, window, opening) declare the void they cut in their host (wall, slab, roof).
- Level-attached objects (stair) declare bottom/top attachment and the slab opening they cut.
- Flip/mirror axes, insertion point, snapping points.

### 4.8 Handles
Viewport handles mapped to parameters or input points (drag width, swing arc, sill height).

### 4.9 Nested OPOs
An OPO may place other OPOs (stair → railing → balusters; kitchen run → cabinets). Parameters can be passed down.

### 4.9a Ports (distribution elements)
`opo::ports` lists the connection points of distribution elements: `name`, `system_type` (IFC `IfcDistributionSystemEnum`), `flow_direction` (SOURCE / SINK / SOURCEANDSINK), `port_type` (PIPE / DUCT / CABLE…), and FEEL expressions for `nominal_size`, `position`, `direction` and an optional `when`. They export as `IfcDistributionPort` nested in the element. OPO does not route or size systems.

### 4.10 Data
- IFC class and predefined type (e.g. IfcDoor / DOOR)
- Property sets (standard IFC psets + custom)
- Classifications (bSDD URIs, ETIM, Uniclass…)
- Material slots mapped to parts

### 4.11 Variants
Named parameter sets, optionally with saved input geometry. Basis for "types" in schedules.

### 4.12 Product binding (optional)
Manufacturer, product code, link, the sizes actually sold (constrains parameters), product data, and optionally the manufacturer's detailed geometry (e.g. from their IFC file) wrapped inside the generic object's representations.

### 4.13 Baked fallback
Ready-built geometry and plan symbols for the default variant, so viewers and tools that don't run the recipe can still show and export the object.

### 4.14 References (required for library objects)
OPO objects are not invented from scratch. Every object in an OPO library states, in `opo::object.references`:
1. **Parametric basis**: an established, openly licensed parametric object it is modelled on (e.g. dormakaba's CC0 *bim-all-doors* for doors), and what was taken from it. Only licences compatible with the target library (CC0, CC-BY) may be used; proprietary manufacturer objects can inform dimensions but not be copied.
2. **IFC parameters**: the IFC classes, property sets and properties its parameters map to, using IFC names wherever IFC has them.
3. **Norms for standard sizes**: the national or industry standards its size catalogues come from, for both metric and imperial markets (e.g. EN/ISO norms in Europe, BS 4787, US industry sizes; national norms of EU countries are not used).
4. **Rule sources**: the regulations behind its rule sets (e.g. ISO 21542, ADA).

Values that are typical practice rather than taken from a norm (e.g. hinge positions) are marked as such in a `note`.

**Size catalogues.** Standard sizes ship as layer files, one per norm or market. Each catalogue has one *system* node (inheriting the type) carrying that market's construction values (frame type, lining, gaps, leaf thickness, handle height…), and one variant node per standard size inheriting the system node. All markets use the same object; only the values differ.

### 4.15 Script step (optional, rare)
For generators too complex for the recipe (e.g. balanced winder stairs):
- Compiled to **WebAssembly**, run sandboxed (no files, network or system access, time and memory limits).
- **Inputs:** parameters + input slots. **Output:** an ordinary OPO recipe and representations — never raw drawing commands.
- Tools without a WASM runtime use the baked fallback.

### 4.16 Class templates (every IFC class)
Every concrete IFC element class (150 in IFC 4.3) has an OPO **class template**, so any IFC element can be created parametrically and shared as a file, like a Revit family. This includes elements that other tools treat as non-shareable system types (walls, slabs, roofs, stairs, pipes, ducts).
- A class template is built on one of eight **archetypes**: point, linear, area, wall, hosted, flight, fitting, assembly. The archetype fixes inputs, base geometry, host behaviour and representations.
- The template adds the IFC class, every predefined type as a choice, the applicable IFC property sets as data parameters (they follow the chosen predefined type), base quantities as derived values, ports for distribution elements, and per-class defaults.
- Templates are **generated** from the pinned IFC schema, the IFC property and quantity set templates, the archetype definitions and one hand-written per-class table. They are regenerated when IFC changes.
- **Library objects** refine a template with real construction logic and drawing conventions, keeping the same class, types, property sets and ports. Authors (firms, manufacturers) start from a template or a library object.
- Details: `spec/objects/archetypes.md`; class list: `spec/objects/ifc-coverage.md`.
- Built so far (one per archetype, plus IfcBeam): `library/templates/` — IfcWall, IfcSlab, IfcBeam, IfcMember, IfcBoiler, IfcPipeFitting, IfcOpeningElement, IfcStair, IfcElementAssembly. Generated by `tools/gen_templates.py`, checked by `tools/check_opo.py`.

## 5. Encoding and packaging

- **Structure: IFCX.** The object definition is an IFCX document. OPO's parametric content (parameters, input slots, rules, recipe, representations metadata, handles) lives in components under an `opo::` namespace, the way IFCX extensions work. Variants and product bindings are IFCX layers over the base. Goal: an `.opo` is instantly readable by IFC5 tools, and `opo::` can later be proposed to buildingSMART as an official extension.
- **IFCX tracking.** IFC5/IFCX is still alpha with no release date. Each OPO spec version pins a named IFCX snapshot, so upstream changes never break existing files. OPO follows each new IFCX release with a matching OPO update.
  - OPO 0.1 pins **IFCX alpha** (`ifcxVersion: "ifcx_alpha"`), as in buildingSMART/IFC5-development commit `1a63082` (8 Sep 2026), importing `ifc@v5a`, `prop@v5a` and `usd@v1`.

### 5.1 IFCX mapping

An IFCX file has a `header`, `imports` (schema URIs), `schemas` (new attribute definitions) and `data` (a flat list of nodes with `path`, `children`, `inherits`, `attributes`). Nodes with the same path in several layers are composed into one. OPO maps onto this as follows:

| OPO concept | IFCX |
|---|---|
| Definition | One **type node** with `bsi::ifc::class` (e.g. `IfcDoor`), plain `bsi::ifc::prop::*` values for the default variant, and all `opo::*` attributes |
| Parts (frame, leaf, void…) | `children` of the type node, carrying baked geometry |
| Variant | A node that `inherits` the type node and sets `opo::values` and its own `bsi::ifc::prop::TypeName` |
| Instance (in a project file) | A node that `inherits` a variant (or the type), with its own `opo::values`, `opo::inputs` (drawn geometry) and `usd::xformop` placement |
| Product binding, regional values | Layer files adding attributes to existing paths |
| Baked fallback | `usd::usdgeom::mesh` on part nodes (3D), `usd::usdgeom::basiscurves` on hidden 2D symbol nodes, both in metres |
| IFC data | `opo::ifc` maps FEEL expressions to `bsi::ifc::prop::*` names, so every instance writes correct IFC properties (e.g. OverallWidth, OperationType) |

`opo::*` attributes on the type node: `opo::object` (identity), `opo::parameters`, `opo::slots`, `opo::rules`, `opo::recipe`, `opo::representations`, `opo::host`, `opo::handles`, `opo::materials`, `opo::hatches`, `opo::ports`, `opo::ifc`. They are declared in `schema/opo@v<version>.ifcx`, imported by every OPO file.

IFCX alpha has only meshes and polylines, no exact solids. Exact geometry comes from the OPO recipe (used by OPO-aware tools and the IFC4.3 export); the baked mesh lets any IFC5 viewer display the object today.

### 5.2 Package layout (draft)

```
door.opo                (zip)
├── object.ifcx         base document: type node, opo:: definition, baked fallback
├── layers/*.ifcx       optional layers: variants, product bindings, regional values
└── assets/             optional: previews, textures, manufacturer geometry, WASM
```
Source repositories store the same structure unpacked as a folder.
- **Canonical encoding:** JSON, validated by a published JSON Schema at `https://opo-format.org/schema/<version>/`.
- **Packaging: always a zip.** Every `.opo` is a zip container (like `.3mf` or `.docx`) holding the IFCX/JSON document plus any previews, textures, manufacturer geometry or WASM module. One code path for all readers. For version control, the reference CLI packs and unpacks `.opo` files, and source repositories store objects unpacked as folders.
- Units: metres and degrees, as IFCX (see §4.2).

## 6. Versioning and compatibility

- Spec uses semantic versions (1.0, 1.1, 2.0). Every file states its spec version.
- Minor versions only add; readers ignore unknown fields.
- Objects made for 1.x open in every later 1.x reader.
- Long-term rule: files made today must still open in ten years.

## 7. IFC mapping

Because an `.opo` is already IFCX, IFC5 tools read its IFC data directly. For IFC4.3 (the current ISO standard, STEP files), OPO defines an export mapping:

- Instance → IfcProduct of the declared class (IfcDoor, IfcWindow, IfcStair…), with its type object from the variant.
- Representations → IFC shape representations with matching contexts (Body, Plan/Annotation, target scale).
- Geometry exported as exact IFC solids/profiles where possible (e.g. opening = extruded arbitrary closed profile).
- Parameters also written to a property set so other tools see the data and Curva can rebuild on re-import.

## 8. Libraries and licensing

| | Licence |
|---|---|
| Spec text | CC-BY 4.0 |
| Reference code (Rust reader/validator) | MIT / Apache-2.0 |
| Free base library (`opo-format/library`, later) | CC0 or CC-BY |
| Curva Pro library (private) | Commercial: use in projects, no redistribution |

Rules: community contributions to the free library stay free. Contributors sign a CLA.

## 9. Repositories

| Repo | Contents |
|---|---|
| `opo-format/opo` | The standard: spec, schemas, conformance tests, decisions, proposals |
| `opo-format/opo-rs` | Rust reference implementation and `opo` CLI |
| `opo-format/library` | Object sources (YAML), class templates, rule sets, styles; releases publish packages |
| `opo-format/.github` | Organisation-wide contributor files and templates |
| `curva3d/curva` | Curva app, depends on `opo-rs` at a pinned version |

Details: [`docs/architecture.md`](../docs/architecture.md) (decision 0013).

## 10. Reference test objects (drive the spec)

1. **Door** — parameters, rules, 3 LODs, plan symbols, host void, IFC mapping, references, generic metric / UK / US size catalogues *(written: `examples/door/`)*
2. **Window with custom outline** — closed-profile input slot, driving/driven modes, clipped glazing grid (any window: outlines are editable on all windows)
3. **Straight / L / U stair** — level attachment, repeat, slab opening, nested railing, regional rule set
4. **Stair on a walkline with winders** — curve input, curve queries, WASM script step
5. **Branded product** — generic window + product binding + manufacturer geometry

The full list of planned objects (74 objects in eight families: openings, circulation, fixtures, furniture & equipment, shading devices, lifts & escalators, structure & coverings, MEP terminals & site), with one specification sheet per object and shared rule sets, is in [`spec/objects/`](objects/README.md). Test objects 1–4 are O-01, O-08 (with a custom outline; every window has an editable outline), C-01…C-03 and C-04 there.

## 11. Decisions

Decisions are recorded one per file in [`decisions/`](../decisions/README.md) (decision 0001). The project's organisation (repositories, workflow, source format, provenance, stages) is described in [`docs/architecture.md`](../docs/architecture.md) and [`docs/workflow.md`](../docs/workflow.md).

## 12. Open questions

1. Exact FEEL subset and the OPO function list (curve queries).
2. Zip details: manifest, compression, signing.
3. Full JSON Schema for each `opo::` attribute (the door example in `examples/door/` is the working draft).
4. Should variants always carry their own baked geometry, so plain IFC5 viewers show them at the right size?
5. 2D symbols in IFCX: hidden basiscurves tagged with `opo::representation` for now, until IFCX gains drawing contexts.
6. Values still marked *(to verify)* or *(to collect)* in the object sheets, mainly ISO 21542 ramp, WC and turning-space values (full text not yet reviewed) and maker size ranges.
