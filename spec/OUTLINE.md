# OPO — Open Parametric Object

**Draft spec outline · v0.0 · 23 Nov 2026**
Status: strategy draft, not yet a specification. Nothing here is final.

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
5. **IFC-native.** Every object carries its IFC class and properties and exports clean IFC geometry (no meshes where exact geometry is possible). Structure aligned with IFC5 / IFCX ideas.
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

### 4.3 Input slots
Drawn geometry the object is built from. Examples:
- Window/door: `outline` (closed flat profile in the object's plane), default = rectangle from width × height
- Stair: `walkline` (flat curve) with segments marked flight/landing and corners marked landing/winder
- Railing, fence: `path`
- Slab, roof: `boundary` + `holes`

Each slot declares: geometry type, plane, default, validity rules (closed, non-self-intersecting, min size, fits host).
Applications edit slots in their own way (in Curva: double-click → sketch mode). The format only defines the slot.

**Driving vs driven:** an object may switch between parameters driving the input (rectangle mode) and the input driving read-only parameters (custom outline mode).

### 4.4 Rules
- **Derived values:** formulas from parameters and inputs (leaf width = width − 2 × frame; riser count = ceil(height ÷ max riser)).
- **Checks:** conditions with messages ("double leaf needs width ≥ 1200 mm").
- **Regional rule sets:** referenced, swappable sets of limits (stair riser/going, guard heights) per country or code.

Formula language: small, side-effect-free expression language (arithmetic, comparisons, conditionals, min/max/round, curve queries). To be specified.

### 4.5 Geometry recipe
A chain of operations from a small, strictly specified vocabulary (a node graph stored as data):

- **2D:** line, arc, polyline, rectangle, circle, profile, offset, fillet, boolean (2D)
- **Curve queries:** length, point at, divide into N, perpendicular at, offset
- **3D:** extrude, revolve, sweep, loft, boolean (union/difference/intersection)
- **Patterning:** repeat/array (linear, along curve, grid), mirror
- **Transform:** move, rotate, scale
- **Placement:** nested OPO instance

Keep this list short: every operation is a cost for other implementers.

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

### 4.14 Script step (optional, rare)
For generators too complex for the recipe (e.g. balanced winder stairs):
- Compiled to **WebAssembly**, run sandboxed (no files, network or system access, time and memory limits).
- **Inputs:** parameters + input slots. **Output:** an ordinary OPO recipe and representations — never raw drawing commands.
- Tools without a WASM runtime use the baked fallback.

## 5. Encoding and packaging

- **Canonical encoding:** JSON, validated by a published JSON Schema at `https://opo-format.org/schema/<version>/`.
- **Single file** for simple objects. **Package** (zip container, still `.opo`) when it includes textures, previews, manufacturer geometry or a WASM module. *(To decide.)*
- Units explicit (SI, millimetres default for lengths).
- Layered/composable structure inspired by IFCX (variants and product bindings as layers over a base). *(To explore.)*

## 6. Versioning and compatibility

- Spec uses semantic versions (1.0, 1.1, 2.0). Every file states its spec version.
- Minor versions only add; readers ignore unknown fields.
- Objects made for 1.x open in every later 1.x reader.
- Long-term rule: files made today must still open in ten years.

## 7. IFC mapping

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

1. **Door** — parameters, rules, 3 LODs, plan symbols, host void, IFC mapping
2. **Window with custom outline** — closed-profile input slot, driving/driven modes, clipped glazing grid
3. **Straight / L / U stair** — level attachment, repeat, slab opening, nested railing, regional rule set
4. **Stair on a walkline with winders** — curve input, curve queries, WASM script step
5. **Branded product** — generic window + product binding + manufacturer geometry

## 11. Open questions

1. Formula language: write our own minimal one or adopt an existing expression syntax?
2. Single file vs package: when is a zip needed?
3. How far to align the internal structure with IFCX now, given IFC5 is still alpha?
4. Plan-symbol styling: line weights, hatches, and how much is left to the application's drawing style.
5. Constraint solving in sketch inputs (dimensions, parallel, tangent) — in OPO or left to the application?
6. Governance: when to invite other maintainers; trademark search before public launch.
