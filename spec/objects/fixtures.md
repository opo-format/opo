# Fixtures — object sheets F-01 … F-14

Shared rules for this family:
- **No openly licensed parametric basis was found** for sanitary ware or kitchen units (only commercial Revit families). These objects are based on IFC, the norms below and generic geometry; branded products attach later through **product bindings** (spec §4.12) with the maker's own geometry.
- **Sanitary terminals** (IfcSanitaryTerminal) carry: connection points (water supply, waste) as snapping points with nominal diameters, the **clearance zone** in front/beside the fixture as a separate 2D/3D zone (annotation class, not a solid), and mounting type (floor-standing, wall-hung on a frame, built-in). Property sets: `Pset_SanitaryTerminalTypeToiletPan`, `…WashHandBasin`, `…Bath`, `…Shower`, `…Sink`, etc.
- **Kitchen units** follow the EN 1116 / US coordinating sizes in `rulesets.md` (`kitchen`) and share components: carcase, plinth/toe kick, fronts (door / drawer / flap, styles: slab, frame), handles (bar, knob, recessed, none), worktop (F-11).
- **Rule sets:** `accessibility` (heights and clearances), `kitchen`.

---

## F-01 WC

**IFC** IfcSanitaryTerminal · TOILETPAN (+ CISTERN as nested or part) · **P2**

**Scope** Floor-standing (close-coupled or back-to-wall) and wall-hung WC with concealed or exposed cistern, seat and lid, flush plate; clearance zone. *Not:* the installation frame in detail (outline only at high LOD).

**Based on** — · EN 33 (connecting dimensions), EN 997 (WC pans with integral trap) · `accessibility`.

**Inputs** Host wall (rear).

**Parameters** `mounting` floor | wall_hung · `cistern` concealed | close_coupled | high_level · `projection` (wall to front of pan; default 0.52 m / 28" floor-standing US) · `pan_width` (0.36 m / 14½") · `seat_height` (0.40–0.42 m standard; 0.46–0.48 m accessible / 17"–19" ADA) · `frame_depth` (concealed cistern, default 0.15 m) · `flush_plate_height`.

**Rules** `accessibility`: seat height range, centreline to side wall (ADA 16"–18"), free space beside (DIN 18040 90 × 70 cm), clearance zone (ADA 60" × 56" wall-hung / 59" floor-standing).

**Size catalogues** EU wall-hung projections about 0.48–0.56 m, extended accessible pans about 0.70 m *(from maker data, typical)* · US elongated / round bowls: projection about 28"–30" *(to verify)*; seat heights standard 15" and "comfort height" 17"–19".

**LOD** 3D: low box · medium pan, seat, cistern box · high pan form, seat/lid, flush plate. Plan: low outline · medium outline + seat + cistern (dashed if concealed) · high outline from 3D. Clearance zone: plan annotation at medium/high.

---

## F-02 Bidet

**IFC** IfcSanitaryTerminal · BIDET · **P3**

**Scope** Floor-standing or wall-hung bidet, tap hole, clearance zone; matches F-01 sizes for pairing.

**Parameters** `mounting` · `projection` (default as F-01) · `width` · `rim_height`.

**Size catalogues** EU: pairs with WC series (projection 0.52–0.56 m) · US: rare; same as EU.

---

## F-03 Urinal

**IFC** IfcSanitaryTerminal · URINAL · **P3**

**Scope** Wall-hung urinal (bowl), optional privacy screen, flush valve / sensor box.

**Based on** — · EN 80 (wall-hung urinals, connecting dimensions) · `accessibility` (ADA rim ≤ 17").

**Parameters** `rim_height` (default 0.6 m adult, 0.43 m / 17" accessible) · `projection` · `screen` (bool, depth).

---

## F-04 Washbasin

**IFC** IfcSanitaryTerminal · WASHHANDBASIN · **P2**

**Scope** Wall-hung, pedestal, semi-pedestal, countertop / undercounter / vessel basin; tap holes; optional vanity unit (nested F-08 base unit variant); mirror zone above (annotation).

**Based on** — · `accessibility` (DIN 18040 height 80 cm + knee space 90 × 55 cm; ADA rim ≤ 34", knee ≥ 27").

**Inputs** Host wall; or host worktop for countertop types.

**Parameters** `type` wall_hung | pedestal | countertop | undercounter | vessel · `width` (default 0.6 m / 24") · `depth` (0.45 m / 18") · `rim_height` (default 0.85 m / 34"; typical) · `tap_holes` 0 | 1 | 3 · `overflow` (bool) · `accessible` (bool → knee space zone, shallow siphon).

**Rules** Rim height and knee clearance under `accessibility`.

**Size catalogues** EU widths 0.45–0.8 m in 50 mm steps *(typical maker range, to verify)* · US vanity tops 24", 30", 36", 48" *(typical, to verify)*.

**LOD** Plan: low outline · medium outline + bowl + tap · high from 3D.

---

## F-05 Shower

**IFC** IfcSanitaryTerminal · SHOWER (tray as part; screen as nested IfcPlate or part) · **P2**

**Scope** Shower tray (raised, low-profile, or level-access floor area with drain), screen/enclosure (none, fixed panel, hinged door, sliding, quadrant), shower head and mixer position, drain (point / linear).

**Based on** — · `accessibility` (level access; ADA shower seat and controls) · market tray sizes.

**Inputs** Host walls (corner or alcove); optional `outline` slot for walk-in areas.

**Parameters** `tray` raised | low | level · `width`, `depth` · `shape` rectangle | square | quadrant | pentagon · `enclosure` none | panel | door | sliding | quadrant · `drain` point | linear (+ position) · `head_height` · `mixer_height`.

**Size catalogues** EU/UK trays: squares 760, 800, 900, 1000 mm; rectangles 1000 × 800, 1200 × 800, 1200 × 900, 1400 × 800, 1700 × 800 mm (sizes made by all major UK makers) · US bases: 32" × 32", 36" × 36" (ADA minimum 36" × 36"), 48" × 36", 60" × 32".

**LOD** Plan: tray outline + drain + cross (annotation) · enclosure as glass line (cut) · door swing arc.

---

## F-06 Bathtub

**IFC** IfcSanitaryTerminal · BATH · **P2**

**Scope** Built-in (alcove, drop-in, corner) and freestanding baths; bath panel (front/end), overflow and waste, tap position, optional shower screen.

**Based on** — · market sizes.

**Inputs** Host walls (alcove / corner).

**Parameters** `type` alcove | drop_in | corner | freestanding · `length`, `width`, `rim_height` · `shape` rectangle | double_ended | oval · `panel` front | front_end | none · `tap_position` end | side | wall.

**Size catalogues** EU/UK lengths 1500, 1600, 1700, 1800 mm × widths 700, 750, 800 mm (1700 × 700 most common) · US alcove 60" × 30" / 32" (most common), compact 54", large 66"–72"; corner 60" × 60".

**LOD** Plan: outer outline + inner bowl outline (medium) · high from 3D.

---

## F-07 Kitchen sink

**IFC** IfcSanitaryTerminal · SINK · **P2**

**Scope** Inset, undermount or integrated sink, 1–2 bowls + optional drainer, tap position; cut-out declared to the host worktop (F-11) as a void.

**Based on** — · EN 1116 (sink base widths) · US sink base widths.

**Inputs** Host worktop (F-11).

**Parameters** `mount` inset | undermount | integrated · `bowls` 1 | 1.5 | 2 · `drainer` none | left | right · `width`, `depth`, `bowl_depth` · `tap_hole` position.

**Size catalogues** EU: to suit base unit widths 450–900 mm *(typical, to verify)* · US: for sink bases 30"–36" (single 30", double 33"–36").

---

## F-08 Kitchen base unit

**IFC** IfcFurniture · USERDEFINED (ObjectType KITCHEN_BASE_UNIT) · classification Uniclass/OmniClass to add · **P2**

**Scope** Floor unit under the worktop: carcase, plinth, fronts (doors, drawers, combinations), internal shelf, handles; special types: sink base, hob/oven housing, corner (blind / L), drawer stack. *Not:* internal fittings beyond shelves and drawer boxes (data only).

**Based on** — · EN 1116 · US industry sizes (`kitchen`).

**Inputs** None (placed along a run; F-12 places and sizes them).

**Parameters** `width` · `height` (carcase; derived from worktop height − worktop thickness − plinth) · `depth` (0.56 m EU / 24" US) · `plinth_height` (0.1–0.15 m EU / 4½" US) · `plinth_setback` · `fronts` (layout preset: 1 door, 2 doors, 1 drawer + 1 door, 3 drawers, 4 drawers…) · `front_style` slab | shaker · `handle` bar | knob | recessed | none · `carcase_thickness` (0.018 m / ¾").

**Rules** Height chain gives the EN 1116 worktop height (850/900/950) or US 36" · built-under recess for appliances ≥ EN 1116 minimum.

**Size catalogues** EU widths 0.15, 0.2, 0.3, 0.4, 0.45, 0.5, 0.6, 0.8, 0.9, 1.0, 1.2 m *(maker steps; appliance housings 0.4 / 0.5 / 0.6 / 0.9 m from EN 1116)* · US widths 9"–48" in 3" steps, height 34½", depth 24".

**LOD** 3D: low box · medium carcase, plinth, fronts with joints, handles · high + front style, drawer joints. Plan: low/medium outline + front line (front dashed where under worktop) · elevation: fronts and handles.

---

## F-09 Kitchen wall unit

**IFC** IfcFurniture · USERDEFINED (KITCHEN_WALL_UNIT) · **P2**

**Scope** Wall-hung unit above the worktop: doors, lift-up flaps, open shelves, extractor housing.

**Parameters** `width` · `height` · `depth` (0.32–0.35 m EU / 12" US) · `mount_height` (bottom above worktop: ≥ 450 mm EU, 18" US) · `fronts` · `handle`.

**Size catalogues** EU widths as F-08; heights by maker (0.36–0.96 m) *(to collect)* · US widths 9"–48" in 3" steps; heights 30", 36", 42"; depth 12" (24" over fridges).

**LOD** Plan: overhead class (dashed) outline · elevation: fronts.

---

## F-10 Kitchen tall unit

**IFC** IfcFurniture · USERDEFINED (KITCHEN_TALL_UNIT) · **P2**

**Scope** Floor-to-top unit: larder, broom, appliance housing (built-in oven, fridge), split fronts.

**Parameters** `width` · `height` · `depth` · `fronts` (split heights) · `housing` none | oven | oven_microwave | fridge | fridge_freezer.

**Size catalogues** EU: heights align with wall unit tops (maker) · US: heights 84", 90", 96"; widths 18", 24", 30", 33", 36"; depth 24" (12" pantry).

---

## F-11 Worktop

**IFC** IfcSystemFurnitureElement · WORKSURFACE · **P2**

**Scope** Worktop along a run or an outline (L, U, island, peninsula); edge profile, front overhang, upstand/splashback, cut-outs from sinks (F-07) and hobs (F-13).

**Inputs** Slot `outline` (closed profile in plan) or generated by F-12 from the run.

**Parameters** `thickness` (0.02–0.04 m EU / 1½" US) · `overhang_front` (≤ 30 mm EN 1116) · `overhang_sides` · `edge` square | eased | bullnose · `upstand` (height) · `material` slot.

**Rules** Overhang ≤ EN 1116 maximum · cut-outs keep minimum material at edges (warning).

**LOD** Plan: outline + cut-outs (cut class when above cut plane… normally below → projected) · elevation: edge line.

---

## F-12 Kitchen run

**IFC** IfcFurniture (aggregate) with nested F-07…F-11, F-13 · **P2**

**Scope** A kitchen along a wall path: lays out base, wall and tall units, fills the remainder with fillers, generates plinth, worktop (F-11), cornice/light pelmet optional, places sink, hob, oven, fridge from a sequence. Straight, L, U, galley, island.

**Inputs** Slot `path` (polyline along walls) · optional island outline.

**Parameters** `sequence` (list of unit types and widths, e.g. `[tall_fridge 600, base_drawer 400, sink_base 800, dishwasher 600, hob_base 600, …]`) · `worktop_height` (EN 1116: 850 / 900 / 950 mm; US 36") · `filler_min` · `wall_units` (bool) · `corner` blind | l_shaped.

**Rules** Sequence fits the path (fillers ≥ min, error if over-length) · appliance widths match housings · dishwasher next to sink (warning, ergonomics) · `kitchen` rule set values.

**LOD** Children's LODs.

---

## F-13 Kitchen / laundry appliance

**IFC** IfcElectricAppliance · REFRIGERATOR, FRIDGE_FREEZER, FREEZER, DISHWASHER, ELECTRICCOOKER, MICROWAVE, WASHINGMACHINE, TUMBLEDRYER (verify enum); cooker hood USERDEFINED · **P2**

**Scope** One object, many kinds: freestanding, built-under or built-in appliance as a clean box with front details (door, controls, hob zones), clearance/door-swing zone. Product bindings provide real models.

**Parameters** `kind` (enum above) · `installation` freestanding | built_under | built_in · `width`, `height`, `depth` (defaults per kind and market) · `door_swing` left | right | drop_down.

**Size catalogues** EU: 0.45 / 0.6 m wide built-under (height to EN 1116 recess 820–920 mm); fridge columns 0.6 m · US: dishwasher 24" × 34" × 25"; ranges 30" (36"/48" pro); fridges 30"–36" wide.

**LOD** Plan: outline + kind symbol (hob rings, "DW", "W"…) annotation.

---

## F-14 Built-in wardrobe

**IFC** IfcFurniture · USERDEFINED (WARDROBE) · **P3**

**Scope** Floor-to-ceiling built-in storage along a wall: carcase modules, hinged or sliding doors, internal rail/shelf zones (simple), scribe fillers.

**Inputs** Slot `path` (wall line) · room height from host.

**Parameters** `depth` (0.6 m / 24") · `module_width` · `doors` hinged | sliding · `height` (to ceiling − scribe) · `interior` preset.

**Size catalogues** Depths 0.6 m / 24"; module widths 0.5, 0.75, 1.0 m / 18", 24", 36" *(typical, to verify)*.

---

## Sources

- EN 33, EN 997, EN 80 scope: BSI / DIN catalogue pages; WC dimensions examples from maker data sheets (Laufen, Vitra, Armitage Shanks via NBS) — typical values only
- ADA and DIN 18040: see `rulesets.md`
- Shower trays: less.co.uk (sizes made by all of Mira, MX, Coram and Merlyn); screwfix.com; US: wayfair.com shower size guides
- Baths: screwfix.com, homebase.co.uk, bathroommountain.co.uk; US: homedepot.com, thisoldhouse.com, aquaticausa.com
- EN 1116 and US kitchen cabinets: see `rulesets.md`
- US appliances: bestonlinecabinets.com, coohom.com cabinet/appliance charts
