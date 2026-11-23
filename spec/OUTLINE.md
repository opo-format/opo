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
Typed values: length, angle, number, integer, boolean, choice (enum), text, material slot, colour.
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
- numbers, strings, booleans, lists (`[x, y]` for points; FEEL indexes from 1, so `p[1]` is x), context access (`host.thickness`)
- arithmetic, comparisons (`=`, `!=`, `<`, `<=`, `>`, `>=`), `and`/`or`/`not`, `if … then … else`
- `min`, `max`, `abs`, `round`, `ceiling`, `floor`, `sqrt`
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

- **2D:** line, arc, polyline, rectangle, circle, profile, offset, fillet, boolean (2D)
- **Curve queries:** length, point at, divide into N, perpendicular at, offset
- **3D:** extrude, revolve, sweep, loft, boolean (union/difference/intersection)
- **Patterning:** repeat/array (linear, along curve, grid), mirror
- **Transform:** move, rotate, scale
- **Placement:** nested OPO instance

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

**Line and hatch semantics.** 2D representations carry meaning, not pen styles: every line is classed as *cut*, *projected*, *hidden*, *overhead* or *annotation*, and every hatch names the material it cuts. The application's drawing style maps classes to line weights, line types and hatch patterns, so drawings stay consistent with the office standard across a project.

### 4.7 Host behaviour
- Hosted objects (door, window, opening) declare the void they cut in their host (wall, slab, roof).
- Level-attached objects (stair) declare bottom/top attachment and the slab opening they cut.
- Flip/mirror axes, insertion point, snapping points.

### 4.8 Handles
Viewport handles mapped to parameters or input points (drag width, swing arc, sill height).

### 4.9 Nested OPOs
An OPO may place other OPOs (stair → railing → balusters; kitchen run → cabinets). Parameters can be passed down.

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
3. **Norms for standard sizes**: the national or industry standards its size catalogues come from, for both metric and imperial markets (e.g. DIN 18100/18101, BS 4787, US industry sizes).
4. **Rule sources**: the regulations behind its rule sets (e.g. DIN 18040, ADA).

Values that are typical practice rather than taken from a norm (e.g. hinge positions) are marked as such in a `note`.

**Size catalogues.** Standard sizes ship as layer files, one per norm or market. Each catalogue has one *system* node (inheriting the type) carrying that market's construction values (frame type, lining, gaps, leaf thickness, handle height…), and one variant node per standard size inheriting the system node. All markets use the same object; only the values differ.

### 4.15 Script step (optional, rare)
For generators too complex for the recipe (e.g. balanced winder stairs):
- Compiled to **WebAssembly**, run sandboxed (no files, network or system access, time and memory limits).
- **Inputs:** parameters + input slots. **Output:** an ordinary OPO recipe and representations — never raw drawing commands.
- Tools without a WASM runtime use the baked fallback.

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

`opo::*` attributes on the type node: `opo::object` (identity), `opo::parameters`, `opo::slots`, `opo::rules`, `opo::recipe`, `opo::representations`, `opo::host`, `opo::handles`, `opo::materials`, `opo::ifc`. They are declared in `schema/opo@v<version>.ifcx`, imported by every OPO file.

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
| `opo-format/opo` | Spec, JSON Schema, Rust reference crate, validator CLI, test objects |
| `opo-format/library` (later) | Free base objects |
| `curva3d/curva` | Curva app, depends on the `opo` crate at a pinned version |

## 10. Reference test objects (drive the spec)

1. **Door** — parameters, rules, 3 LODs, plan symbols, host void, IFC mapping, references, DIN/UK/US size catalogues *(written: `examples/door/`)*
2. **Window with custom outline** — closed-profile input slot, driving/driven modes, clipped glazing grid
3. **Straight / L / U stair** — level attachment, repeat, slab opening, nested railing, regional rule set
4. **Stair on a walkline with winders** — curve input, curve queries, WASM script step
5. **Branded product** — generic window + product binding + manufacturer geometry

The full list of planned objects (46 objects in four families: openings, circulation, fixtures, furniture & equipment), with one specification sheet per object and shared rule sets, is in [`spec/objects/`](objects/README.md). Test objects 1–4 are O-01, O-13, C-01…C-03 and C-04 there.

## 11. Decisions (23 Nov 2026)

| # | Question | Decision |
|---|---|---|
| 1 | Formula language | FEEL (OMG DMN) subset with OPO unit helpers and curve queries (§4.4) |
| 2 | Single file vs package | Always a zip container; CLI pack/unpack for version control (§5) |
| 3 | IFCX alignment | `.opo` is an IFCX document with an `opo::` extension; each OPO version pins an IFCX snapshot and follows IFCX releases (§5) |
| 4 | Plan-symbol styling | Semantic line classes and hatch materials; the application's drawing style chooses weights and patterns (§4.6) |
| 5 | Sketch constraints | Solved by the application; OPO stores resolved geometry and validity rules (§4.3) |
| 6 | Governance | Single maintainer until v0.1 (schema + door and window test objects); trademark search before any public announcement |
| — | Units | Stored in metres and degrees (IFCX defaults) at full precision; displayed in any unit; limits/steps and standard sizes per unit system (§4.2, §4.4). Changed from millimetres on 23 Nov 2026 for IFC5 compatibility |
| — | References | Library objects are based on openly licensed parametric objects, IFC parameters and published norms, named in `opo::object.references` (§4.14) |
| — | Object catalogue | 46 objects in four families, one sheet each, shared rule sets: `spec/objects/` |
| — | IFCX snapshot | IFCX alpha, IFC5-development commit `1a63082` (8 Sep 2026); mapping in §5.1 |

## 12. Open questions

1. Exact FEEL subset and the OPO function list (curve queries).
2. Zip details: manifest, compression, signing.
3. Full JSON Schema for each `opo::` attribute (the door example in `examples/door/` is the working draft).
4. Should variants always carry their own baked geometry, so plain IFC5 viewers show them at the right size?
5. 2D symbols in IFCX: hidden basiscurves tagged with `opo::representation` for now, until IFCX gains drawing contexts.
6. Portugal market (RGEU, DL 163/2006 accessibility) values for the size catalogues and rule sets.
