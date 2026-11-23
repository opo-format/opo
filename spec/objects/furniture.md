# Furniture & equipment — object sheets E-01 … E-08

Shared rules for this family:
- **No openly licensed parametric basis was found**; objects are generic, based on IFC and market sizes, and kept deliberately simple ("detailed, not a simulator"). Branded pieces come through product bindings (spec §4.12) with the maker's geometry.
- Freestanding: no host; placed on a level. A **use zone** (chair pull-out, bed access, desk legroom) is an optional 2D annotation, not a solid.
- Common components: legs (4 legs, trestle, sled, pedestal, plinth), tops, frames, cushions (sofas), simple material slots.
- Plan symbols follow drawing conventions: outline at low, outline + main divisions (cushions, pillows, chair backs) at medium, from 3D at high.
- IFC: `IfcFurniture` with PredefinedType (CHAIR, TABLE, DESK, BED, SHELF, SOFA, FILECABINET, USERDEFINED); `Pset_FurnitureTypeCommon` (NominalLength/Width/Height, Style, MainColour).

---

## E-01 Table

**IFC** IfcFurniture · TABLE · **P3**

**Scope** Rectangular, square, round, oval tables; dining, coffee, counter and bar heights; leg types; optional extension leaf (drawn as dashed extent). Nested chairs (E-02) around it as an option.

**Based on** — · market sizes.

**Parameters** `shape` rectangle | square | round | oval · `length`, `width` / `diameter` · `height` preset dining | counter | bar | coffee · `top_thickness` · `legs` four | trestle | pedestal | sled · `seats` (derived from perimeter, ~0.6 m / 24" per diner) · `chairs` (bool: place E-02 around).

**Rules** Dining: chair seat to table top 0.25–0.30 m / 10"–12" (warning) · seats derived vs. requested.

**Size catalogues** Heights: dining 0.71–0.76 m / 28"–30"; counter 0.86–0.91 m / 34"–36"; bar 1.02–1.07 m / 40"–42" · Rectangular: 4 seats 1.2–1.5 × 0.75–0.9 m (47"–60" × 30"–36"); 6 seats 1.5–1.8 × 0.9–1.0 m (60"–72" × 36"–40"); 8 seats 1.8–2.4 × 1.0–1.1 m · Round: 4 seats Ø 0.9–1.2 m (36"–48"); 6 seats Ø 1.2–1.5 m (48"–60").

**LOD** Plan: low outline · medium outline + legs (hidden) + chairs · high from 3D.

---

## E-02 Chair / stool

**IFC** IfcFurniture · CHAIR · **P3**

**Scope** Dining/side chair, armchair (dining), stool (counter/bar); four legs or sled; optional arms.

**Parameters** `type` chair | armchair | stool · `seat_height` (dining 0.43–0.48 m / 17"–19"; counter stool 0.61–0.66 m / 24"–26"; bar stool 0.71–0.76 m / 28"–30") · `seat_width`, `seat_depth` · `back_height` · `arms` (bool).

**Rules** Arm height clears the table apron when pushed in (warning, with E-01).

**LOD** Plan: low square · medium seat + back line · high from 3D.

---

## E-03 Sofa / armchair

**IFC** IfcFurniture · SOFA · **P3**

**Scope** Armchair, 2-, 3-seat sofa, corner sofa (L), chaise; base, seat cushions, back cushions, arms.

**Parameters** `seats` 1–4 · `shape` straight | corner_left | corner_right | chaise · `seat_width` per seat · `depth` · `seat_height` · `arm_width`, `arm_height` · `back_height` · `legs` visible | plinth.

**Size catalogues** By maker *(typical ranges to collect; no norm)*.

**LOD** Plan: outline + cushion divisions (medium).

---

## E-04 Bed

**IFC** IfcFurniture · BED · **P3**

**Scope** Bed frame sized from the mattress, headboard, optional footboard, base (legs / divan / storage), mattress, pillows and folded duvet in plan at medium.

**Parameters** `mattress_size` (catalogue entry) · `frame_margin` (frame beyond mattress) · `mattress_height`, `bed_height` · `headboard` (height, thickness) · `footboard` (bool) · `base` legs | divan | platform.

**Rules** Access zone beside the bed (annotation; wheelchair space from `accessibility`, ISO 21542 *(to verify)*).

**Size catalogues** (mattress W × L)
- EU: 90 × 200, 140 × 200, 160 × 200, 180 × 200, 200 × 200 cm
- UK: single 90 × 190, small double 120 × 190, double 135 × 190, king 150 × 200, super king 180 × 200 cm
- US: twin 38" × 75", twin XL 38" × 80", full 54" × 75", queen 60" × 80", king 76" × 80", California king 72" × 84"

**LOD** Plan: low outline · medium + pillows, duvet fold line · high from 3D.

---

## E-05 Desk / workstation

**IFC** IfcFurniture · DESK · **P3**

**Scope** Fixed or height-adjustable desk (EN 527 types A–D), straight or L, optional modesty panel, pedestal, monitor arm zone; workstation clusters via nesting.

**Based on** — · EN 527-1 (office desk dimensions, desk types by adjustability) · US practice.

**Parameters** `type` fixed | selectable | adjustable (EN 527 C / B / A) · `width`, `depth` · `height` (fixed default 0.74 m / 29"–30"; adjustable range) · `shape` straight | l_left | l_right · `legs` four | panel | c_frame | t_frame · `modesty_panel` (bool) · `pedestal` none | mobile | fixed.

**Rules** Legroom and height range per EN 527-1 Table 1 *(values to add — standard is not freely available)*.

**Size catalogues** Widths 1.2, 1.4, 1.6, 1.8 m; depths 0.7, 0.8 m · US 48", 60", 72" × 24", 30" *(typical, to verify)*.

**LOD** Plan: outline + legs (hidden) + chair (optional E-02).

---

## E-06 Shelving / bookcase

**IFC** IfcFurniture · SHELF · **P3**

**Scope** Freestanding or wall-fixed open shelving: bays, shelves (fixed or evenly spaced), sides, back panel optional, plinth; wall-mounted shelf rails as a variant.

**Parameters** `bays`, `bay_width` · `height`, `depth` · `shelves` per bay · `back_panel` (bool) · `material_thickness`.

**LOD** Plan: outline + bay divisions (medium) · elevation: shelves.

---

## E-07 Freestanding storage (sideboard, chest, cabinet)

**IFC** IfcFurniture · USERDEFINED (SIDEBOARD, CHEST_OF_DRAWERS, CABINET) · FILECABINET for office pedestals · **P3**

**Scope** Box furniture on legs or plinth with doors and/or drawers; reuses the F-08 front/handle components.

**Parameters** `width`, `height`, `depth` · `fronts` layout · `base` legs | plinth | wall_hung · `handle`.

**LOD** As F-08.

---

## E-08 Light fixture

**IFC** IfcLightFixture · POINTSOURCE / DIRECTIONSOURCE / SECURITYLIGHTING · `Pset_LightFixtureTypeCommon` · light source IfcLightSourceGoniometric with photometry as an external reference (`IfcLightDistributionDataSourceSelect`: Eulumdat, IES, CIBSE TM14) · **P3**

**Scope** Pendant, recessed downlight, surface ceiling light, wall light, track spot, floor lamp; housing geometry, light emitting surface, mounting (ceiling host, wall host, suspension length); photometric file attached as an asset in the package (spec §5.2 `assets/`). *Not:* lighting calculation (application's job).

**Based on** — · IFC lighting entities · Eulumdat (LDT) / IES LM-63 photometric formats. Rust parsing of IFC lighting and Eulumdat conversion exists in the `bimifc-parser` crate (MPL-2.0) — reference for the Curva implementation.

**Inputs** Host ceiling / slab / wall (optional; freestanding for floor lamps).

**Parameters** `kind` pendant | downlight | surface | wall | track_spot | floor · `diameter` or `length × width` · `height` / `suspension_length` · `cut_out` (recessed: ceiling void diameter) · `luminous_flux`, `colour_temperature`, `power` (data) · `photometry` (asset reference) · `beam_angle`.

**Rules** Recessed: ceiling void depth ≥ fixture depth (check against host).

**Size catalogues** Recessed downlight cut-outs by maker *(to collect)*.

**LOD** Plan: reflected ceiling plan symbol (circle + cross for downlights, outline for linear) at low/medium; 3D housing at medium/high.

---

## Sources

- Table and chair heights: castlery.com, wayfair.com, ikea.co.id, planner5d.com dining guides; table sizes per seats: tribesigns.com
- Beds: ikea.com (UK and EU mattress size guides), which.co.uk, tomsguide.com (US sizes), t3.com
- EN 527-1: standards.iteh.ai abstract (desk types A–D, dimensions in Table 1); din.de catalogue
- IFC lighting: ifc43-docs (IfcLightFixtureType, Pset_LightFixtureTypeCommon, IfcLightDistributionDataSourceSelect); docs.rs bimifc-parser lighting module (MPL-2.0)
