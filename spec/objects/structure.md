# Structure and coverings — object sheets K-01 … K-08

Shared rules for this family:
- **Architectural, not structural.** These objects place and size structural members and finishes for drawings, coordination and quantities. Loads, analysis and design are out of scope; members carry their profile and material so a structural tool can take over. Walls, slabs and roofs stay with the app's own tools (they are not OPO objects).
- **Profiles** (K-01…K-03) come from one shared profile library, stored as IFC profile definitions (`IfcIShapeProfileDef`, `IfcUShapeProfileDef`, `IfcLShapeProfileDef`, `IfcTShapeProfileDef`, `IfcRectangleHollowProfileDef`, `IfcCircleHollowProfileDef`, `IfcRectangleProfileDef`, `IfcCircleProfileDef`) so IFC export keeps the exact section:
  - **EU steel:** EN 10365 (hot rolled I, H and U sections: IPE, HE A/B/M, HL, HD, HP, UB, UC, IPN, UPE, PFC, UPN), EN 10210-2 / EN 10219-2 (hollow sections). Designation tables *(to collect from openly published maker section tables; check the licence of each source before it goes into the CC0 library)*.
  - **UK steel:** UB, UC, PFC (in EN 10365).
  - **US steel:** AISC shapes (W, M, S, HP, C, MC, L, HSS). The AISC Shapes Database v16.0 is a free download, but building it into software is under an AISC licence agreement *(licence to check before shipping the data in the CC0 library)*.
  - **Timber:** rectangular sections; glulam to EN 14080 *(sizes to collect)*; US dimensional lumber nominal vs. actual (2×4 = 1½" × 3½") *(table to collect)*.
  - **Concrete:** rectangular, circular, custom profile input.
- **Coverings** (K-04…K-07) are `IfcCovering` elements linked to the element they cover (`IfcRelCoversBldgElements`) or the space they finish (`IfcRelCoversSpaces`).
- **LOD (all):** low — centre line or outline · medium — profile outline / finished surfaces · high — fillets, joints, panel and grid lines, connection plates where the sheet says so.

---

## K-01 Column

**IFC** IfcColumn · COLUMN (PILASTER for engaged columns) · **P2**

**Scope** Vertical member between two levels (or base and top elevations): profile, rotation, material, optional base plate and cap plate (steel, high LOD), optional cladding or fire casing as an offset outline. *Not:* connection design.

**Based on** — · IFC profile definitions · profile library above.

**Inputs** Insertion point (or grid intersection) · base level and top level (or offsets).

**Parameters** `profile` (library or custom) · `rotation` · `base_level`, `top_level`, offsets · `material` steel | concrete | timber | other · `base_plate`, `cap_plate` (bool + size) · `casing` none | offset (thickness).

**Rules** Profile fits within an enclosing wall when the column is engaged (check, warning) · height derived from levels.

**Size catalogues** Profile library (all markets).

**LOD** Plan: cut profile, hatched by material (low: outline) · elevation and section: member with plates at high.

---

## K-02 Beam

**IFC** IfcBeam · BEAM (JOIST, LINTEL, SPANDREL where they fit) · **P2**

**Scope** Straight member between two points, at a level with a top-of-steel or soffit offset; optional camber and end cuts (square, mitred, coped at high LOD). Lintels over openings can be hosted by a door or window and take their length from the opening plus bearings. *Not:* connections beyond simple end plates.

**Based on** — · IFC profile definitions · profile library.

**Inputs** Start and end points (or two columns / grid lines) · level · or host opening (lintel).

**Parameters** `profile` · `justification` (top, centre, bottom; left, centre, right) · `offset` · `bearing` (lintels, default 0.15 m / 6") · `end_cut` square | mitre | cope · `material`.

**Rules** Lintel length = opening width + 2 × bearing (derived) · beam within the floor zone (soffit above ceiling void, warning when a K-04 ceiling is lower).

**Size catalogues** Profile library.

**LOD** Plan: dashed outline (above cut plane) · section: cut profile hatched.

---

## K-03 Member (brace, post, purlin, rafter, stud)

**IFC** IfcMember · BRACE / POST / PURLIN / RAFTER / STUD / STRUT / CHORD · **P3**

**Scope** Any other linear member: bracing, posts, purlins, rafters, studs, truss chords. Same geometry as K-02 with a free orientation (point to point in 3D).

**Based on** — · IFC 4.3 `IfcMemberTypeEnum`.

**Inputs** Start and end points in 3D.

**Parameters** `role` (IFC predefined type above) · `profile` · `rotation` about its axis · `end_cut`.

**Rules** —

**Size catalogues** Profile library.

**LOD** As K-02.

---

## K-04 Suspended ceiling

**IFC** IfcCovering · CEILING · **P2**

**Scope** Suspended ceiling in a room or a drawn boundary: grid (exposed, concealed or none), tiles or plasterboard, ceiling height, void depth to the slab, perimeter trim, bulkheads at changes in height, cut-outs for light fixtures (E-08) and air terminals (M-02) placed in the ceiling. *Not:* hanger and fixing design.

**Based on** — · EN 13964 (suspended ceilings: requirements) · market grid sizes.

**Inputs** Boundary (room/space or drawn polygon) · height above the level.

**Parameters** `system` exposed_grid | concealed_grid | plasterboard · `module` (default 600 × 600 mm; 600 × 1200, 625 × 625; US 2' × 2', 2' × 4') · `grid_origin` (centred, or a set point) · `grid_rotation` · `tile_thickness` · `height` (default 2.7 m / 9') · `void_depth` (derived from the slab above) · `trim` profile.

**Rules** Void ≥ deepest item above it (beams, ducts as data; warning) · cut tiles at the perimeter ≥ half a module (warning; suggests a grid origin that avoids slivers) · hosted light fixtures and air terminals snap to the grid (check).

**Size catalogues** Module sizes per market (typical, not norm values).

**LOD** Reflected ceiling plan: outline (low) · grid lines and hosted items (medium) · trim and bulkheads (high). Section: ceiling line and void.

---

## K-05 Raised access floor

**IFC** IfcCovering · FLOORING · **P3**

**Scope** Raised floor over a slab in a room or drawn boundary: panel grid, finished floor height, pedestals (high LOD), perimeter, ramps or steps to adjacent floors (nested C-06 or stair), cut-outs for floor boxes.

**Based on** — · EN 12825 (raised access floors) · market panel sizes.

**Inputs** Boundary · level.

**Parameters** `panel` (default 600 × 600 mm; US 2' × 2') · `finished_height` (default 0.15 m / 6") · `panel_thickness` · `grid_origin` · `pedestals` (bool).

**Rules** Finished height ≥ panel thickness + min void (warning) · step to adjacent floor flagged where no ramp/step is placed (warning).

**Size catalogues** Panel sizes per market (typical).

**LOD** Plan: grid lines (medium) · section: panels, void, pedestals (high).

---

## K-06 Cladding

**IFC** IfcCovering · CLADDING (each panel an `IfcCovering` part, or one covering with a panel pattern *(to decide)*) · **P2**

**Scope** Rainscreen or panel cladding on a wall or façade surface: panel layout on a grid (same grid input as curtain walls), open or closed joints, panel thickness, cavity and subframe depth (simple layers), returns at openings, corners. Panels of metal, fibre cement, stone, ceramic, timber boards (board widths and orientation). *Not:* fixing design.

**Based on** — · grid and surface logic shared with O-16 · IFC.

**Inputs** Host wall or façade surface (face or baseline + levels), like curtain walls.

**Parameters** `kind` panels | boards | tiles · `module` U × V (or board width + orientation) · `joint` open | closed, `joint_width` · `bond` stack | running (offset) · `panel_thickness` · `cavity` · `subframe_depth` · `return_at_openings` (bool).

**Rules** Cut panels at edges ≥ min width (warning) · openings in the host wall cut the cladding and add returns (derived).

**Size catalogues** Panel presets from public maker ranges *(to collect)*.

**LOD** Elevation: panel joints (medium) · plan/section: panel, cavity, subframe layers (medium), returns (high).

---

## K-07 Profile trim (skirting, coping, moulding)

**IFC** IfcCovering · SKIRTINGBOARD / COPING / MOLDING · **P3**

**Scope** A 2D profile swept along a path: skirtings along room boundaries (breaking at door openings), copings on parapets, cornices and mouldings. Profile from presets or a drawn 2D input.

**Based on** — · IFC.

**Inputs** Path (room boundary, wall top, or drawn polyline) · profile (preset or drawn).

**Parameters** `role` skirting | coping | moulding · `profile` · `height`, `depth` (preset profiles) · `break_at_openings` (bool, default true for skirting) · `overhang` (coping, default 0.05 m / 2").

**Rules** Coping overhang ≥ min each side (warning, project value).

**Size catalogues** Profile presets *(to collect)*.

**LOD** Low: hidden · medium: outline · high: profile.

---

## K-08 Chimney / fireplace

**IFC** IfcChimney · USERDEFINED (`ObjectType` CHIMNEY / FIREPLACE) · **P3**

**Scope** Masonry or system chimney stack through floors and roof (flue outline, casing, stack above roof, cap) and an optional fireplace or stove opening with hearth. Floor and roof openings derived. *Not:* flue calculations, distances to combustibles beyond a warning zone.

**Based on** — · EN 1443 (chimneys: general requirements) · EN 13229 (inset appliances and open fires) *(scope to verify)*.

**Inputs** Base level, top (roof), insertion point.

**Parameters** `flue` size (round or rectangular) · `casing_thickness` · `height_above_roof` · `fireplace` none | open | inset · `opening_width`, `opening_height` · `hearth_depth`.

**Rules** Stack height above the roof ≥ project value (warning; national rules not in OPO) · hearth projection ≥ project value (warning).

**Size catalogues** —

**LOD** Plan: flue and casing cut · section: stack through floors, fireplace opening.

---

## Sources

- IFC 4.3 enums `IfcColumnTypeEnum`, `IfcBeamTypeEnum`, `IfcMemberTypeEnum` (… BRACE, CHORD, POST, PURLIN, RAFTER, STRUT, STUD …), `IfcCoveringTypeEnum` (CEILING, CLADDING, COPING, FLOORING, MOLDING, SKIRTINGBOARD …), `IfcChimneyTypeEnum` (USERDEFINED / NOTDEFINED only): ifcopenshell IFC4X3_ADD2 schema
- EN 10365:2017 scope and section families (IPE, HE, HL, HLZ, HD, HP, UBP, UB, UC, IPN, J, UPE, PFC, UPN, U, CH); revision prEN 10365:2025 in progress: BSI, UNI, iTeh catalogue pages
- AISC Shapes Database v16.0 (free download; developer licence agreement for use in software): aisc.org
- EN 13964, EN 12825, EN 1443, EN 13229: CEN catalogue titles *(scopes to verify)*
- Ceiling and floor module sizes: typical market values
