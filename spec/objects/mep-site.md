# MEP terminals and site — object sheets M-01 … M-06, G-01 … G-03

These are the visible ends of building services and the common site elements that architects place and draw. Pipes, ducts, cables and their sizing belong to MEP tools, not OPO.

Shared rules for this family:
- **MEP terminals** (M-) are `IfcFlowTerminal` subtypes (or `IfcFlowController` for switches). Each has **ports** as data (`IfcDistributionPort`: system type, nominal size, flow direction) so an MEP tool can connect to it; OPO does not route anything.
- **Host:** a wall, ceiling (K-04) or floor. Wall-hosted items take a height above the finished floor; ceiling-hosted items snap to the ceiling grid when the host has one.
- **Symbols:** plan and reflected-ceiling symbols are part of the object's representations (semantic line classes, spec §4.6). There is no single EN/ISO symbol set for architectural drawings of these items, so OPO ships neutral default symbols and lets a project swap the symbol representation by layer.
- **LOD (all):** low — symbol only · medium — simple body + symbol · high — body detail (grille slots, radiator panels, plate and rocker).

---

## M-01 Radiator / convector

**IFC** IfcSpaceHeater · RADIATOR / CONVECTOR · **P3**

**Scope** Panel radiator, column radiator, towel rail, trench (floor) convector: body, brackets, valve and lockshield positions, connection side. Shown under windows as the typical case. *Not:* heat output calculation (output as data).

**Based on** — · EN 442 (radiators and convectors: test and rating) · market panel types.

**Inputs** Host wall (or floor for trench convectors) · optional host window (centres under it).

**Parameters** `kind` panel | column | towel_rail | trench · `panel_type` 10 | 11 | 20 | 21 | 22 | 33 (panel/convector count, market designation) · `height` (typical 0.3–0.9 m) · `length` (typical 0.4–3.0 m in 0.1 m steps) · `wall_distance` · `floor_clearance` (default 0.1 m / 4") · `connection` side | bottom (left/right) · `output` (data, W at EN 442 conditions).

**Rules** Fits under the hosted window sill (warning) · clear of door swings (check against doors in the same wall).

**Size catalogues** Panel types × heights × lengths (typical market range, not a norm).

**LOD** Plan: outline (medium), panels (high) · elevation: panel face with brackets.

---

## M-02 Air terminal

**IFC** IfcAirTerminal · DIFFUSER / GRILLE / LOUVRE / REGISTER · **P3**

**Scope** Ceiling diffuser (square, round, linear slot), wall grille, floor register, external louvre: face size, neck size, plenum box (high), throw direction as data.

**Based on** — · IFC.

**Inputs** Host ceiling, wall or floor.

**Parameters** `kind` (IFC type) · `face_size` (default 600 × 600 for lay-in diffusers / 24" × 24") · `neck_diameter` · `slots` (linear: count, length) · `airflow` (data) · `system` supply | extract | return (data, sets the symbol).

**Rules** Lay-in diffusers match the ceiling module (check against K-04).

**Size catalogues** Face sizes by maker *(to collect)*.

**LOD** RCP symbol (low) · face outline with pattern (medium/high).

---

## M-03 Socket outlet

**IFC** IfcOutlet · POWEROUTLET / DATAOUTLET / COMMUNICATIONSOUTLET / AUDIOVISUALOUTLET · **P3**

**Scope** Wall or floor outlet: plate size, number of gangs, mounting height; socket type as data (Schuko, BS 1363, NEMA 5-15, data RJ45). *Not:* circuits.

**Based on** — · IEC 60884 (plugs and socket-outlets) and national socket types as data only *(geometry is a generic plate; the socket face is not drawn)*.

**Inputs** Host wall or floor.

**Parameters** `kind` (IFC type) · `gangs` 1–4 · `plate` (default 86 × 86 mm; US 2¾" × 4½" single gang) · `height` (default 0.3 m / 15"; above worktops 1.05 m / 44") · `socket_standard` (data).

**Rules** `accessibility`: controls and outlets within the reach range (ISO 21542 controls 800–1100 mm; ADA reach range) where the rule set is on (warning).

**Size catalogues** Plate sizes per market (typical).

**LOD** Plan symbol · elevation plate outline.

---

## M-04 Switch

**IFC** IfcSwitchingDevice · TOGGLESWITCH / DIMMERSWITCH / MOMENTARYSWITCH / KEYPAD · **P3**

**Scope** Light switch, dimmer, push button, keypad: plate, gangs, height, placement on the lock side of a door.

**Based on** — · IFC.

**Inputs** Host wall · optional host door (places it on the handle side at a set distance from the frame).

**Parameters** `kind` (IFC type) · `gangs` · `plate` (as M-03) · `height` (default 1.0 m; ISO 21542 range 0.8–1.1 m; US 48" max reach) · `distance_from_frame` (default 0.15 m / 6").

**Rules** `accessibility` reach range as M-03 · clear of the door swing on the hinge side (check).

**Size catalogues** As M-03.

**LOD** As M-03.

---

## M-05 Sprinkler head

**IFC** IfcFireSuppressionTerminal · SPRINKLER · **P3**

**Scope** Pendent, upright, sidewall or concealed sprinkler head with its coverage area shown as an annotation. *Not:* hydraulic design, spacing design.

**Based on** — · EN 12845 (fixed firefighting systems, sprinkler design) · NFPA 13 (US) *(spacing and coverage values to collect; shown as data, not checked)*.

**Inputs** Host ceiling (K-04) or slab soffit.

**Parameters** `kind` pendent | upright | sidewall | concealed · `coverage_radius` (data, annotation) · `k_factor` (data) · `temperature_rating` (data).

**Rules** Heads clear of light fixtures and air terminals by a project distance (warning).

**Size catalogues** —

**LOD** RCP symbol + optional coverage circle.

---

## M-06 Fire hose reel / cabinet

**IFC** IfcFireSuppressionTerminal · HOSEREEL (FIREHYDRANT for landing valves) · **P3**

**Scope** Wall-mounted or recessed hose reel cabinet: cabinet size, recess into the host wall, door swing.

**Based on** — · EN 671-1 (hose reels with semi-rigid hose) *(scope to verify)*.

**Inputs** Host wall.

**Parameters** `mount` surface | recessed · `width`, `height`, `depth` (maker data) · `height_to_centre` (project value) · `door_swing` left | right.

**Rules** Recessed depth ≤ host wall thickness (check) · door swing clear (warning).

**Size catalogues** Maker sizes *(to collect)*.

**LOD** Plan: cabinet outline + swing · elevation: cabinet face.

---

## G-01 Tree / planting

**IFC** IfcGeographicElement · VEGETATION · **P2** (every site plan needs it)

**Scope** Tree, shrub or planting area: trunk, crown as a simple solid (sphere, ellipsoid, cone, column), crown and trunk diameters, height; for areas a boundary with planting height. Species as data. Plan symbol with crown outline. *Not:* realistic foliage (apps may swap a visual model).

**Based on** — · IFC.

**Inputs** Point (tree) or boundary (planting area) on the terrain.

**Parameters** `kind` tree | shrub | area · `crown_shape` round | oval | conical | columnar · `height` (default 8 m / 26') · `crown_diameter` (default 5 m / 16') · `trunk_diameter` · `crown_base` (clear trunk height) · `species` (data) · `existing` (bool: existing / new / to be removed, drawn with different line classes).

**Rules** Crown clear of buildings by a project distance (warning) · root protection zone as an annotation (radius from trunk diameter, project factor).

**Size catalogues** Presets by size class (small / medium / large tree; typical).

**LOD** Plan: circle (low), crown outline with trunk (medium), textured symbol (high) · elevation: crown and trunk solid.

---

## G-02 Site furniture

**IFC** IfcFurniture · USERDEFINED (`ObjectType` BENCH / BIKE_RACK / BOLLARD / BIN / PLANTER) · **P3**

**Scope** Bench, bicycle rack (stands with spacing), bollard, litter bin, planter box. Simple solids with the parameters that matter for layout.

**Based on** — · IFC (no predefined site-furniture types in IFC 4.3 `IfcFurnitureTypeEnum`).

**Inputs** Point + direction, or a line (rows of stands, bollards).

**Parameters** `kind` · `count` and `spacing` along the line (bike racks, bollards; bike stand spacing default 1.0 m / 3') · `length`, `height`, `width` per kind · `backrest`, `armrests` (bench).

**Rules** Bike stand spacing and clear aisle ≥ project values (warning).

**Size catalogues** Typical sizes per kind.

**LOD** Plan outline (low/medium) · 3D body (medium/high).

---

## G-03 Sign

**IFC** IfcSign · PICTORAL / MARKER · **P3**

**Scope** Wall, ceiling-hung or post-mounted sign panel: size, mounting height, text and a sign code as data. Safety signs reference their ISO 7010 code (e.g. E001) as data; the pictogram itself is not shipped in the library, so the app supplies its own graphic.

**Based on** — · ISO 7010 (safety sign codes, as data) · ISO 21542 (signage height and contrast, via `accessibility`) *(values to verify)*.

**Inputs** Host wall, ceiling or a point (post).

**Parameters** `mount` wall | hanging | projecting | post · `width`, `height` · `mount_height` · `text` · `code` (data).

**Rules** Hanging signs: headroom below ≥ project value (warning).

**Size catalogues** —

**LOD** Plan: line (wall) or outline · elevation: panel with text.

---

## Sources

- IFC 4.3 enums `IfcSpaceHeaterTypeEnum` (CONVECTOR, RADIATOR), `IfcAirTerminalTypeEnum` (DIFFUSER, GRILLE, LOUVRE, REGISTER), `IfcOutletTypeEnum`, `IfcSwitchingDeviceTypeEnum` (… DIMMERSWITCH, KEYPAD, MOMENTARYSWITCH, TOGGLESWITCH …), `IfcFireSuppressionTerminalTypeEnum` (… HOSEREEL, SPRINKLER …), `IfcGeographicElementTypeEnum` (VEGETATION …), `IfcSignTypeEnum` (MARKER, MIRROR, PICTORAL), `IfcFurnitureTypeEnum` (no site furniture types): ifcopenshell IFC4X3_ADD2 schema
- ISO 21542 controls height 800–1100 mm: see `rulesets.md`
- EN 442, EN 12845, EN 671-1, IEC 60884, ISO 7010, NFPA 13: catalogue titles *(scopes and values to verify before building)*
- Radiator panel types, plate sizes, outlet heights: typical market values
