# Shading devices — object sheets S-01 … S-07

Shared rules for this family:
- **IFC:** `IfcShadingDevice` (a built element). IFC 4.3 `IfcShadingDeviceTypeEnum` has only **AWNING, JALOUSIE, SHUTTER** (+ USERDEFINED, NOTDEFINED). Louvres, fins and screens use USERDEFINED with `ObjectType` LOUVRE / FIN / SCREEN. Property set `Pset_ShadingDeviceCommon` *(name to verify against the IFCX snapshot)* (operation, solar and visible transmittance and reflectance as data).
- **Host:** a window or door (sits in front of, inside or above its opening and takes its size from it), a curtain wall (follows its grid), or a free façade surface. Hosted devices update when the host opening changes size, including windows with an edited outline (shading follows the outline's bounding box, or the outline itself where the device type allows).
- **Position** relative to the host: `in_reveal` | `face_fixed` (on the wall face) | `projecting` (brackets off the face). Positions per type below.
- **Operation:** `fixed` | `manual` | `motorised` (data only; motors and controls are not modelled). Movable devices have an `open_state` parameter (0–1, or slat angle) so drawings can show them open, closed or at an angle.
- **Norms (EU):** EN 13659 (shutters and external venetian blinds) and EN 13561 (external blinds and awnings) are performance standards: wind resistance class, operating force, safety. They set **no sizes**, so OPO carries their classes as data and sizes come from maker ranges. EN 12216 is the terminology standard that names the product types. UK uses the same EN standards; the US has no matching product standard (wind loads per ASCE 7, data only).
- **Rules (all):** device within host and maker size limits *(data, warning)* · movable devices clear of opening sashes (check against the hosted window's swing, warning) · box/headbox fits the lintel or is surface-mounted (check).
- **LOD (all):** low — outline or box only · medium — slats/panels at the drawn open state, guide rails, box · high — slat profiles, brackets, end caps. Plan and section show the box and the projection; elevation shows the slats or panel pattern.

---

## S-01 Louvres / brise-soleil

**IFC** IfcShadingDevice · USERDEFINED (`ObjectType` LOUVRE) · **P2**

**Scope** Fixed or adjustable horizontal or vertical blades on a frame or on brackets in front of a façade, window or curtain wall: blade arrays over one or many bays, end frames, support brackets or outriggers. *Not:* solar calculation (the app uses the geometry), structural design of outriggers.

**Based on** — · EN 13561 lists brise-soleil (wind resistance of non-retractable products is outside its scope) · IFC as above.

**Inputs** Host (window, curtain wall bay range, or façade surface) or a drawn rectangle on a face.

**Parameters** `direction` horizontal | vertical · `blade_profile` flat | aerofoil | rectangular tube | custom (2D profile input) · `blade_depth` (default 0.2 m / 8") · `blade_thickness` · `spacing` (default 0.3 m / 12") or `count` · `blade_angle` (fixed, or range if adjustable) · `projection` (distance from face) · `frame` none | perimeter | end plates · `bracket_spacing`.

**Rules** Shared rules + blade span between supports ≤ maker maximum *(data)* · cut-off angle derived (shows the sun angle at which blades block direct sun: derived value, no check).

**Size catalogues** None (host-driven). Blade presets from public maker ranges *(to collect)*.

**LOD** As shared; high adds blade end caps and pivot pins.

---

## S-02 Façade fins

**IFC** IfcShadingDevice · USERDEFINED (`ObjectType` FIN) · **P2**

**Scope** Vertical or horizontal fins projecting from a façade or curtain wall at each grid line or at a set rhythm: deep single blades, often running full height on high-rise towers. Straight, tapered or twisted along their length (angle at bottom and top). *Not:* fins that are structural glass (those belong to O-18).

**Based on** — · IFC as above.

**Inputs** Host curtain wall (attaches to chosen grid lines) or façade surface + a list of positions.

**Parameters** `orientation` vertical | horizontal · `depth` (default 0.4 m / 16") · `thickness` (default 0.05 m / 2") · `angle_start`, `angle_end` (twist along the fin; equal = straight) · `taper` (depth at the far end) · `positions` every grid line | every n-th | list · `fixing_spacing`.

**Rules** Shared rules + fins clear of opening vents in the host curtain wall (check).

**Size catalogues** None.

**LOD** Low: line in plan, rectangle in elevation · medium: fin solid · high: fixing brackets.

---

## S-03 External venetian blind

**IFC** IfcShadingDevice · JALOUSIE · **P2**

**Scope** Retractable slat blind outside a window: headbox (exposed, concealed in the lintel, or in an insulated box), slats (flat, curved C or Z profile), guide rails or guide wires, bottom rail. Slat tilt angle and lowered height shown. *Not:* drive and tilt mechanics.

**Based on** — · EN 13659 · EN 12216 (terms).

**Inputs** Host window or door (default), or a drawn rectangle.

**Parameters** `slat_profile` flat | C | Z · `slat_width` (default 0.08 m; common 60, 80, 90 mm) · `guide` rails | wires · `box` exposed | concealed | none · `box_height` (stack height derived from blind height and slat width *(formula from maker data, to collect)*) · `lowered` (0–1) · `slat_angle` (0–90°) · `wind_class` (data, EN 13659).

**Rules** Shared rules + lintel depth ≥ stack height when `box` = concealed (check).

**Size catalogues** Maker min/max widths and heights per slat type *(to collect from public maker data)*.

**LOD** Medium: box, rails, slats as a surface with lines at the slat pitch · high: individual slats at the set angle.

---

## S-04 Roller shutter

**IFC** IfcShadingDevice · SHUTTER · **P2**

**Scope** Roller shutter with a coil box (surface, top-mounted on the window frame, or built into the lintel), guide rails, slats (aluminium, PVC, steel), optional ventilation gaps. Shown fully or partly lowered. *Not:* drive mechanics.

**Based on** — · EN 13659 (roller shutters, including snow load resistance) · EN 12216.

**Inputs** Host window or door.

**Parameters** `box_type` surface | frame_top | lintel · `box_size` (derived from height and slat height *(maker table, to collect)*) · `slat_height` (common 37–55 mm) · `slat_thickness` · `guide_rail` width × depth · `lowered` (0–1) · `wind_class` (data).

**Rules** Shared rules + frame-top box fits within the window head (check against the hosted window).

**Size catalogues** Maker ranges *(to collect)*.

**LOD** Medium: box, rails, curtain as a surface · high: slat lines and box section.

---

## S-05 Hinged / sliding shutters

**IFC** IfcShadingDevice · SHUTTER · **P3**

**Scope** Wing shutters (one or two leaves hinged at the reveal or the face), folding (concertina) shutters and sliding panel shutters on a top track. Panel infill: solid, louvred (fixed slats) or perforated. *Not:* ironmongery detail beyond hinges and track.

**Based on** — · EN 13659 (wing, concertina and sliding panel shutters) · EN 12216.

**Inputs** Host window or door.

**Parameters** `kind` hinged | folding | sliding · `leaves` 1 | 2 | n · `infill` solid | louvred | perforated · `leaf_thickness` · `open_angle` (hinged) or `slide_position` · `track` (sliding: top track length, parking position beside the opening).

**Rules** Shared rules + open leaves clear of adjacent openings and façade elements (warning) · sliding: parking space beside the opening ≥ leaf width (check).

**Size catalogues** None (host-driven).

**LOD** Plan: leaf lines with swing arcs (hinged) or track and parked panels (sliding).

---

## S-06 Awning

**IFC** IfcShadingDevice · AWNING · **P3**

**Scope** Folding-arm awning (cassette or open), drop-arm awning and fixed (Dutch) awning over windows, doors or terraces: cassette or roller tube, fabric, front bar, arms at the set projection and pitch. *Not:* fabric patterns, arm mechanics.

**Based on** — · EN 13561 (folding arm, pivot arm, Dutch awnings; Dutch awning wind resistance outside its scope) · EN 12216.

**Inputs** Host window/door, or wall face + width.

**Parameters** `kind` folding_arm | drop_arm | dutch · `width` · `projection` (default 2.5 m / 8') · `pitch` (default 15°) · `extended` (0–1) · `cassette` none | semi | full · `valance` (height) · `wind_class` (data).

**Rules** Shared rules + headroom under the front bar ≥ min (default 2.0 m / 6'8", project value; warning).

**Size catalogues** Maker width × projection ranges *(to collect)*.

**LOD** Plan: projection outline (dashed when retracted state is shown) · elevation: cassette and front bar.

---

## S-07 External screen (vertical roller blind)

**IFC** IfcShadingDevice · USERDEFINED (`ObjectType` SCREEN) · **P3**

**Scope** Fabric screen rolling down in front of a window or curtain wall bay: cassette, zip or cable guides, bottom bar. Fabric openness as data (affects visible and solar transmittance in `Pset_ShadingDeviceCommon`).

**Based on** — · EN 13561 (vertical roller blinds) · EN 12216.

**Inputs** Host window, door or curtain wall bay.

**Parameters** `cassette` size · `guide` zip | cable | none · `lowered` (0–1) · `openness` (data, %) · `wind_class` (data).

**Rules** Shared rules.

**Size catalogues** Maker ranges *(to collect)*.

**LOD** As S-03 without slats.

---

## Sources

- IFC 4.3 `IfcShadingDeviceTypeEnum` (AWNING, JALOUSIE, SHUTTER, USERDEFINED, NOTDEFINED): ifcopenshell IFC4X3_ADD2 schema
- EN 13659:2015 scope (external venetian blind, roller shutter, wing shutter, Venetian shutter, concertina shutter, sliding panel shutter): BSI / EVS catalogue pages
- EN 13561:2015 scope (folding arm, pivot arm, vertical roller blind, façade awning, Dutch awning, brise-soleil…; no wind resistance for non-retractable products): DIN catalogue page (EN text)
- Slat widths, shutter slat heights: typical maker values, to verify against public data sheets before building
