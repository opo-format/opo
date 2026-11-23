# Circulation — object sheets C-01 … C-08

Shared rules for this family:
- **Level attachment:** stairs and ramps attach bottom and top to levels (IfcBuildingStorey elevations or explicit heights). Total rise = top − bottom. They declare the **slab opening** they need in the upper slab (outline of the stair + clearance), as a void in the host slab.
- **Stair geometry chain:** total rise → riser count = `ceiling(total_rise / max_riser)` → riser = total_rise / risers → going chosen from the step rule (2R + G target) within the active `stairs` rule set → run length. Walkline at a set offset (default 0.5 m / 18" from the inner edge on winding stairs; IRC measures winders 12" from the narrow side).
- **Stair parts:** flights (IfcStairFlight), landings (IfcSlab · LANDING), treads, risers (closed/open), stringers (side strings: none / cut / closed / wall string), nosing, structure type (timber stringers, steel stringers, concrete waist slab), nested railings (C-07) and handrails (C-08).
- **IFC data:** `Pset_StairCommon` / `Pset_StairFlightCommon` — NumberOfRiser, NumberOfTreads, RiserHeight, TreadLength, NosingLength, WalkingLineOffset, TreadLengthAtOffset, TreadLengthAtInnerSide, WaistThickness, RequiredHeadroom, HandicapAccessible, FireExit.
- **Plan symbol by convention:** cut line at the view's cut height (zig-zag break line), lower part solid, upper part dashed (overhead class), walkline with arrow and "UP"/"DN" text (annotation), riser numbering optional.
- **Rule sets:** `stairs`, `guards`, `handrails`, `accessibility`.
- **Parametric basis:** Bonsai's stair and railing generators (GPL-3.0, reference only); no openly licensed stair basis found yet.

---

## C-01 Straight stair — reference test object #3 (with C-02, C-03)

**IFC** IfcStair · STRAIGHT_RUN_STAIR · 1 IfcStairFlight · **P1**

**Scope** One straight flight between two levels; optional landings part-way (makes TWO_STRAIGHT_RUN_STAIR). Treads, risers, stringers or concrete waist, nosing, nested railing(s) and handrail(s). *Not:* structural design of stringers.

**Based on** Bonsai stair generator (reference: types CONCRETE / WOOD-STEEL / GENERIC, tread and riser parameters) · IFC `Pset_StairFlightCommon` · DIN 18065, AD K, IRC/IBC (via `stairs`).

**Inputs** Bottom and top level (or `total_rise`) · host slab for the opening · optional `start_point` + direction (placement).

**Parameters** `total_rise` · `max_riser` (from rule set; default 0.18 m / 7½") · `target_step` (2R+G; default 0.63 m / 25") · `going` (derived, overridable) · `width` (default 1.0 m / 36") · `nosing` (default 0.03 m / 1") · `riser_type` closed | open · `structure` timber_stringers | steel_stringers | concrete · `tread_thickness`, `stringer_width` / `waist_thickness` · `landing_after` (riser number or none) + `landing_depth` · `railing_left/right` (none | guard | handrail; nested C-07 / C-08) · `first_riser_offset`, `last_tread_flush` (bool).

**Rules** Riser within rule set min/max · going within min/max · step rule · pitch ≤ max · width ≥ min · headroom ≥ min (checked against the slab opening edge: opening length derived so headroom is met) · uniform risers (computed) · landing depth ≥ factor × going (DIN) · guard required where fall height > threshold.

**Size catalogues** None (rise-driven). Presets per market: DE residential 17/29 cm, 1.0 m wide; UK private 200/250 mm, 0.9 m; US residential 7½"/10½", 36".

**LOD** 3D: low solid wedge per flight · medium treads, risers, stringers/waist, landing, simple railing · high + nosing profile, railing details. Plan: low outline + walkline + arrow · medium treads, cut line, overhead dashed, walkline, UP/DN · high + nosings, handrails. Section: cut from 3D (all LODs).

---

## C-02 L-shaped stair

**IFC** IfcStair · QUARTER_TURN_STAIR (landing) / QUARTER_WINDING_STAIR (winders) · 2 IfcStairFlight + IfcSlab LANDING · **P1**

**Scope** Two flights at 90° with a quarter landing or winders at the corner; left or right turn.

**Based on** as C-01.

**Inputs** as C-01.

**Parameters** (beyond C-01) `turn` left | right · `corner` landing | winders · `winders` (count, default 3) · `split_riser` (risers in first flight) · `walkline_offset`.

**Rules** as C-01 + winder going at walkline ≥ min and at narrow end ≥ min (`stairs.winders`).

**LOD** Plan: winder lines radiating to the walkline geometry; walkline curved through the corner.

---

## C-03 U-shaped stair

**IFC** IfcStair · HALF_TURN_STAIR / HALF_WINDING_STAIR · 2 flights + half landing · **P1**

**Scope** Two parallel flights with a half landing (or winders), stairwell gap between flights (well width).

**Parameters** (beyond C-02) `well_width` (default 0.1 m / 4"; 0 = no well) · landing depth ≥ flight width.

**Rules** as C-02 + well width affects guard requirement (DE: guard height rules depend on stairwell width, see `guards`).

---

## C-04 Stair on a walkline (winders) — reference test object #4

**IFC** IfcStair · CURVED_RUN_STAIR or matching …_WINDING_STAIR type (derived from the walkline) · **P1**

**Scope** Stair defined by a drawn walkline (polyline/curve) with segments marked flight or landing and corners marked landing or winders; balanced winders computed by a **sandboxed WASM script step** that outputs an ordinary recipe. Free-form stairs, any number of turns.

**Based on** — · spec §4.14 script step · `stairs` rule set (winder rules).

**Inputs** Slot `walkline` (flat curve; per-segment flags flight | landing; per-corner flags landing | winders) · width either side of the walkline (`inner_width`, `outer_width`) · levels.

**Parameters** as C-01 + `balancing` none | balanced (WASM) · `min_inner_going`.

**Rules** All C-01 rules at the walkline; winder going at narrow end ≥ min; even tread depth along the walkline.

**LOD** As C-01; baked fallback contains the computed treads so tools without WASM can show it.

---

## C-05 Spiral stair

**IFC** IfcStair · SPIRAL_STAIR · **P2**

**Scope** Centre column with fan-shaped treads around it, optional outer stringer, helical handrail, landing at top. *Not:* helical stairs without a column (later).

**Based on** — · IRC spiral rules; DIN 18065 spiral (Spindeltreppe) walking-zone rules.

**Inputs** Levels · centre point.

**Parameters** `outer_diameter` (default 1.6 m / 5'), `column_diameter` (default 0.1 m / 4") · `rotation` (total angle, derived from risers × tread angle) · `direction` cw | ccw · `tread_angle` · `top_landing` (angle) · balusters per tread.

**Rules** IRC: clear width ≥ 26", rise ≤ 9½", tread ≥ 7½" at 12" from the narrow edge, headroom ≥ 6'6" · DE: walking zone rules for Spindeltreppen (to add).

**Size catalogues** Makers' standard diameters *(to collect, metric and imperial)*.

**LOD** Plan: circle, tread radials, walkline arc, cut line, UP arrow.

---

## C-06 Ramp

**IFC** IfcRamp · STRAIGHT_RUN_RAMP / TWO_STRAIGHT_RUN_RAMP / QUARTER_TURN_RAMP / HALF_TURN_RAMP · IfcRampFlight + landings · `Pset_RampCommon` · **P2**

**Scope** Ramp along a path with automatic intermediate landings, level landings at top/bottom, edge protection (kerbs / wheel guards), nested handrails both sides.

**Based on** — · `accessibility` (DIN 18040, ADA, AD M).

**Inputs** Slot `path` (polyline centreline) or straight start + direction · bottom/top levels.

**Parameters** `slope` (default from rule set: 6 % DE, 1:12 US) · `width` (default 1.2 m / 36" clear) · `max_run` (from rule set: 6 m DE, 30" rise US) · `landing_length` (1.5 m / 60") · `edge_protection` none | kerb | rail (height 0.1 m) · `handrails` both | left | right | none.

**Rules** Slope ≤ max · run between landings ≤ max (landings inserted automatically) · width ≥ min · turning landings ≥ 1.5 × 1.5 m / 60" × 60" · handrails both sides when required.

**LOD** Plan: outline, slope arrow with % or ratio text, landings, handrails · elevation/section: sloped surface.

---

## C-07 Railing / guard

**IFC** IfcRailing · GUARDRAIL / BALUSTRADE · `Pset_RailingCommon` (Height, Diameter, IsExternal) · **P1**

**Scope** Guard along a path: on a stair (follows the pitch line), a landing, a balcony edge or a void. Infill types: balusters, horizontal rails, glass panel, mesh/sheet; posts; top rail; optional handrail on posts. Nested by stairs and ramps.

**Based on** Bonsai railing generator (reference: FRAMELESS_PANEL and other types) · IFC · `guards`, `handrails`.

**Inputs** Slot `path` (polyline / curve in plan; on stairs the host stair supplies the 3D pitch path) · host: slab edge, stair flight, ramp.

**Parameters** `height` (default from rule set: 0.9 m DE, 42" IBC / 36" IRC) · `infill` balusters | rails | glass | mesh · `baluster_spacing` (max clear gap from rule set: 0.12 m DE, 4" US, 0.1 m UK where required) · `post_spacing` (default 1.2 m / 4') · profiles: top rail, posts, balusters (preset sections) · `mount` top | side (fascia) · `glass_thickness`, `clamp_type`.

**Rules** Height ≥ rule set (on stairs measured from the pitch line) · clear gap ≤ rule set (computed from spacing and baluster width) · if top rail is the handrail: height within handrail range.

**LOD** 3D: low panel · medium posts, top rail, balusters/panel · high + fixings, end returns. Plan: line + posts (medium). Elevation: infill pattern.

---

## C-08 Wall handrail

**IFC** IfcRailing · HANDRAIL · **P2**

**Scope** Handrail on brackets along a wall (stairs, ramps, corridors), with end returns or extensions.

**Based on** Bonsai WALL_MOUNTED_HANDRAIL type (reference) · `handrails`, `accessibility` (extensions at ends of ramps/stairs).

**Inputs** Slot `path` or host stair / ramp side.

**Parameters** `height` (default 0.9 m / 36") · `profile` round Ø 0.04 m / 1½" | rectangular · `wall_clearance` (≥ 0.05 m / 1½") · `bracket_spacing` (default 1.0 m / 4') · `extension_top`, `extension_bottom` (ADA: 12" at ramps; to add for stairs) · `end` return_to_wall | rounded.

**Rules** Height within rule set range · profile within grippable range · clearance ≥ min.

**LOD** Plan: line (medium), brackets (high).

---

## Sources

- See `rulesets.md` for DIN 18065, AD K, IRC, IBC, DIN 18040, ADA, AD M values and their sources.
- Bonsai parametric stair/railing: IfcOpenShell repository (Bonsai GPL-3.0-or-later); railing types FRAMELESS_PANEL and WALL_MOUNTED_HANDRAIL in Bonsai's railing gizmo commits.
- IFC 4.3 documentation: IfcStair, IfcStairFlight, IfcRamp, IfcRailing and their property sets (ifc43-docs.standards.buildingsmart.org).
