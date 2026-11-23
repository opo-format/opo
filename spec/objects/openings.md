# Openings — object sheets O-01 … O-18

Shared rules for this family:
- **Doors** reuse the O-01 dimension chain (wall opening → frame outside → rebate → clear passage, leaf by rebate ± lap/gap) with a selectable nominal reference, IFC `Pset_DoorLiningProperties` / `Pset_DoorPanelProperties`, the same frame types (wrap-around, block, lining, hollow metal) and the same handle and hinge components. Only what differs is listed below.
- **Windows** use one chain: wall opening → (fitting gap) → frame outside → frame (IFC `LiningThickness`) → sash outer → sash (`FrameThickness` in `Pset_WindowPanelProperties`) → glass. Nominal reference: opening, frame outside, or (US) rough opening. IFC `Pset_WindowLiningProperties` (LiningDepth, LiningThickness, TransomThickness, MullionThickness, First/SecondTransomOffset, First/SecondMullionOffset, LiningOffset) and `Pset_WindowPanelProperties` (OperationType, PanelPosition, FrameDepth, FrameThickness). Panel operation values from `IfcWindowPanelOperationEnum` (SIDEHUNGLEFTHAND, TILTANDTURNRIGHTHAND, TOPHUNG, BOTTOMHUNG, PIVOTHORIZONTAL, SLIDINGHORIZONTAL, SLIDINGVERTICAL, FIXEDCASEMENT…).
- **Every window has an editable outline.** All window objects (O-08…O-12, O-14) have an input slot `outline` (closed flat profile in the window plane: arch, circle, triangle, trapezoid, free polygon), edited in the app's sketch mode. **Driving/driven modes:** in rectangle mode width/height drive the outline; in custom mode the outline drives read-only width/height. Frame and sash follow the outline (2D offset), glazing bars are clipped to it, and opening sashes are limited to regions the operation can work in (e.g. a side-hung sash needs a straight hinge edge; otherwise the panel falls back to fixed). Validity: closed, non-self-intersecting, min edge 0.1 m, fits host.
- **Window components** shared by O-08…O-14: frame, sash, glazing (single/double/triple, given as total unit thickness), glazing bars (none / grid / custom), sill (interior board, exterior sill), handle (European espagnolette handle or US crank/latch), opening symbols.
- **Rule sets:** `accessibility` (doors), `escape_windows` (windows), `guards` (low sills / full-height glazing: a sill below the guard height raises a check that a guard or safety glazing is needed).

---

## O-01 Single swing door — ✅ written

See `examples/door/`. Reference for all doors.

---

## O-02 Double swing door

**IFC** IfcDoor · DOOR · OperationType DOUBLE_DOOR_SINGLE_SWING (DOUBLE_DOOR_DOUBLE_SWING if double-acting) · two `Pset_DoorPanelProperties` (PanelPosition LEFT / RIGHT, PanelWidth ratio) · **P2**

**Scope** Two leaves in one frame: equal pair, or unequal (active leaf + fixed/standing leaf). Rebated meeting stiles, flush bolts on the standing leaf (medium/high), handle on the active leaf, optional pull handle or second lever on the standing leaf. *Not:* panic hardware details, automatic operators.

**Based on** bim-all-doors (two-leaf configuration, standing-leaf width `gs_SecondLeaf_w`, meeting-stile rebate) · IFC as above · DIN 18101 two-leaf sizes, US pair sizes.

**Inputs** Host wall. No drawn input.

**Parameters** (beyond O-01) `leaf_split`: equal | unequal · `standing_leaf_width` (unequal; default 0.375 m / 12") · `meeting_rebate` · `double_acting` (bool; no stop, both swings drawn) · `standing_leaf_bolts` (bool).

**Rules** Active leaf ≥ 0.6 m (check) · `accessibility` measures the active leaf only (ADA, DIN 18040 practice).

**Size catalogues** DIN 18101 two-leaf sizes *(to verify against the norm table)* · UK pairs 1981 × 1067 / 1168 / 1220 mm (6'6" × 3'6" / 3'10" / 4'0") · US pairs from two standard leaves, e.g. 2 × 24", 2 × 30", 2 × 36" × 80" *(typical, to verify)*.

**LOD** 3D: low slab · medium frame, two leaves, levers · high + bolts, hinges, meeting stile rebate. Plan: low two lines + two arcs · medium jambs + leaves + arcs · high cut. Elevation: swing indicators on both leaves.

**Open** Standing leaf as a separate panel object or a parameter? (Parameter for now.)

---

## O-03 Sliding door

**IFC** IfcDoor · DOOR · OperationType SLIDING_TO_LEFT / SLIDING_TO_RIGHT / DOUBLE_DOOR_SLIDING · **P2**

**Scope** Leaf (or two bi-parting leaves) sliding on a track in front of the wall (surface-mounted) or inside a lining; top track and cover, floor guide, recessed pull handles. Optional glazed leaf (uses window glazing component). *Not:* lift-and-slide patio doors (later, as a window/door system).

**Based on** FreeCAD BIM "Sliding door" preset (LGPL, reference: opening value slides the leaf, invertible direction) · O-01 frame/lining types · IFC as above.

**Inputs** Host wall.

**Parameters** `track`: surface | in_lining · `leaves`: 1 | 2 (bi-parting) · `overlap` (leaf overlap onto wall at each side, default 0.05 m / 2") · `track_height` (above leaf) · `slide_side`: left | right · `open_fraction` (0–1, drawing only) · `leaf_glazing`: none | full | vision panel.

**Rules** Free wall length beside the opening ≥ leaf width (check against host) · `accessibility` uses clear width with the leaf fully open.

**Size catalogues** Same leaf sizes as O-01 per market (DIN 18101, UK, US); US closet bypass sizes *(to collect)*.

**LOD** 3D: low slab · medium leaf, track box, pulls · high + track profile, floor guide, handle recesses. Plan: low leaf line + arrow · medium leaf in open/closed position + track line (overhead class) · high cut. Elevation: leaf, track, arrow (annotation).

---

## O-04 Pocket door

**IFC** IfcDoor · DOOR · OperationType SLIDING_TO_LEFT / SLIDING_TO_RIGHT / DOUBLE_DOOR_SLIDING · **P2**

**Scope** Sliding leaf disappearing into a pocket frame inside the wall. Declares an enlarged host void (opening + pocket) and a pocket cassette (thin wall zone) in plan. *Not:* the wall build-up around the cassette (host's job).

**Based on** O-03 · IFC as above.

**Inputs** Host wall; checks host thickness ≥ pocket cassette thickness.

**Parameters** `leaves` 1 | 2 · `cassette_thickness` (default 0.1 m / 4") · `pocket_length` (= leaf width + allowance, derived) · `flush_pull` (bool).

**Rules** Host thickness ≥ cassette thickness + 2 × lining (error) · free wall length ≥ pocket length (error).

**Size catalogues** As O-03 (leaf sizes per market).

**LOD** Plan medium/high shows the pocket as hidden line extent of the leaf; void in host covers opening + pocket (pocket void is a recess, not a through opening).

---

## O-05 Folding door

**IFC** IfcDoor · DOOR · OperationType FOLDING_TO_LEFT / FOLDING_TO_RIGHT / DOUBLE_DOOR_FOLDING · **P3**

**Scope** Bifold (2 panels) or multi-panel folding door on a top track, one or both sides. *Not:* glazed folding façade systems (later).

**Based on** — · IFC as above · US bifold sizes.

**Parameters** `panels` (2–8) · `stack_side` left | right | split · `fold_angle` (drawing only) · panel thickness.

**Size catalogues** US bifold closet doors use the 24"–36" × 80" leaf range *(per-panel sizes to collect)* · EU: by maker, use O-01 opening sizes.

**LOD** Plan: zig-zag panels at fold angle + arcs (medium), stack only (low).

---

## O-06 Entrance door assembly

**IFC** IfcDoor · DOOR containing nested O-01/O-02 + fixed glazed panels (IfcWindow · WINDOW, FIXEDCASEMENT) or one IfcDoor with transom/mullions (`TransomOffset`, `TransomThickness`) · **P2**

**Scope** Door with sidelight(s) and/or fanlight in one outer frame. Glazed or solid panels, optional threshold drip, letter plate. *Not:* storefront systems (O-16).

**Based on** bim-all-doors sidelight and fanlight parameters (`gs_sidelight_left/right`, sidelight widths, `gs_transom_height`, transom frame widths; CC0) · IFC TransomOffset/TransomThickness.

**Inputs** Host wall.

**Parameters** `sidelight_left` / `sidelight_right` (bool + width) · `fanlight` (bool + height) · `mullion_width`, `transom_width` · panel fill: glass | solid · door: nested O-01 or O-02 with its own parameters passed down.

**Rules** Glazing next to doors and low glazing needs safety glazing under local rules (check; values to add to `rulesets.md` before building).

**Size catalogues** Built from the door catalogues + sidelight widths *(to collect per market)*.

**LOD** As O-01 for the door; fixed panels as O-11.

---

## O-07 Garage door

**IFC** IfcDoor · DOOR · OperationType ROLLINGUP or USERDEFINED (SECTIONAL, UP_AND_OVER) — verify enum · **P3**

**Scope** Sectional, up-and-over or roller door: closed panel face with section joints, guide rails, headroom box. Open position drawn as overhead (dashed) in plan. *Not:* opener mechanics.

**Based on** — · market standard sizes.

**Parameters** `type` sectional | up_and_over | roller · `sections` (derived from height) · `headroom` (lintel space required) · `side_room`.

**Rules** Lintel height in host ≥ required headroom (check).

**Size catalogues** EU sectional (makers' standard sizes, 125 mm steps): 2375, 2500 × 2000, 2125, 2250; double 5000 × 2000–2250 · UK: 7'0" × 6'6", 7'0" × 7'0"; double 14' × 7' · US: 8' × 7', 9' × 7'; double 16' × 7' / 8'.

**LOD** 3D medium: panel with joints + rails; high + track overhead (hidden in plan).

---

## O-08 Casement / tilt-turn window

**IFC** IfcWindow · WINDOW · PartitioningType SINGLE_PANEL / DOUBLE_PANEL_VERTICAL / TRIPLE_PANEL_VERTICAL / … (with transom: …_HORIZONTAL variants) · panel OperationType SIDEHUNGLEFTHAND/RIGHTHAND, TILTANDTURNLEFTHAND/RIGHTHAND, FIXEDCASEMENT · **P1**

**Scope** The reference rectangular window: 1–3 vertical panels, optional transom with top light, each panel fixed, side-hung (casement) or tilt-turn; frame, sash, glazing unit, glazing bars, sill, handles. Inward (EU) or outward (UK/US casement) opening. *Not:* shaped outlines (O-13), shutters and blinds (later accessory objects).

**Based on** FreeCAD window presets Fixed / Open 1-pane / Open 2-pane (LGPL, reference: frame + panel wires, opening modes "Arc 90", "Triangle" symbols) · IFC window psets · sizes per market.

**Inputs** Host wall.

**Parameters** `nominal_reference` opening | frame_outside | rough_opening · `width`, `height`, `sill_height` · `panels` 1–3 + `panel_operations` list (fixed | side_left | side_right | tilt_turn_left | tilt_turn_right) · `transom` (bool + height) · `opening_direction` in | out · frame: `lining_thickness` (frame width, default 0.07 m), `lining_depth` (frame depth, default 0.08 m) · sash: `sash_width` (default 0.06 m), `sash_depth` · `glazing_thickness` (default 0.024 m double, 0.044 m triple) · `glazing_bars` none | grid (rows × cols) · `reveal_offset` (frame position in wall depth) · sills: interior board (projection, thickness), exterior sill (projection, drip) · `handle_height` (on sash, default centre).

**Rules** Side-hung sash width limit from hardware data (warning; value to confirm) · net clear opening for `escape_windows` (US) · sill below guard height → guard check · total U-value not modelled (data only).

**Size catalogues** EU/DE: openings on the 125 mm modular grid of DIN 4172 *(catalogue to be drawn up; check for a current window-opening norm)* · UK: makers' sizes *(to collect)* · US casement: widths about 16"–48", heights 24"–84"; sizes typically step 2" in width and 6" in height.

**LOD** 3D: low pane in opening · medium frame, sash, glass, sills · high + glazing beads, handles, hinges. Plan: low frame lines + glass line · medium frame/sash cut (hatched) + glass + sills · high cut. Elevation: medium frame, sash outlines, opening triangles (annotation, apex at hinge side; tilt shown as triangle pointing down).

**Open** Exact frame/sash profiles: one generic profile (timber, PVC, aluminium as presets) vs. profile input slot.

---

## O-09 Hung window (single / double hung)

**IFC** IfcWindow · WINDOW · PartitioningType DOUBLE_PANEL_HORIZONTAL · panel OperationType SLIDINGVERTICAL (both sashes, or lower only for single hung) · **P2**

**Scope** Two vertically sliding sashes, meeting rail, check rails, optional grilles; the US/UK sash window. *Not:* counterweight boxes in detail (high LOD shows box outline only).

**Based on** FreeCAD "Sash 2-pane" preset (reference) · IFC as above · US standard sizes.

**Parameters** as O-08 plus `hung` single | double · `upper_ratio` (default 0.5) · `meeting_rail_height` · `open_fraction` (drawing).

**Rules** `escape_windows`: net clear = lower sash opening area (single hung) or the larger sash (double hung).

**Size catalogues** US: widths 24", 28", 32", 36", 40", 44", 48" × heights 36", 44", 48", 52", 54", 60", 62", 72"; size codes by rough opening in feet-inches (e.g. 2030 = 2'0" × 3'0", 2440 = 2'4" × 4'0"), actual unit ½" smaller than the rough opening · UK sash: makers' sizes (to collect).

**LOD** Elevation shows meeting rail and arrows; plan shows two sash lines.

---

## O-10 Sliding window

**IFC** IfcWindow · WINDOW · DOUBLE_PANEL_VERTICAL / TRIPLE_PANEL_VERTICAL · panel OperationType SLIDINGHORIZONTAL / FIXEDCASEMENT · **P2**

**Scope** Horizontal sliders, 2 or 4 panes (FreeCAD presets), one or more fixed. Tracks in frame.

**Based on** FreeCAD "Sliding 2-pane" / "Sliding 4-pane" presets (reference) · IFC · US sizes.

**Parameters** as O-08 plus `panes` 2 | 3 | 4 · `moving` pattern (e.g. XO, OX, XOX, OXXO) · `open_fraction`.

**Size catalogues** US: widths 36", 48", 60", 72", 84" × heights 24", 36", 48", 60" (rough openings; unit ½" smaller) · EU: as O-08.

**LOD** Elevation: arrows on moving panes; plan: overlapping sash lines in two tracks.

---

## O-11 Fixed window

**IFC** IfcWindow · WINDOW · SINGLE_PANEL (or grid) · FIXEDCASEMENT · **P2**

**Scope** Fixed glazing in a frame (direct glazed or in a fixed sash), optional grid of fixed panes. Also used as the glazed panel inside O-06.

**Based on** FreeCAD "Fixed" preset (reference) · IFC.

**Parameters** as O-08 without operations; `direct_glazed` (bool).

**Size catalogues** US picture windows: widths 24"–96", heights 12"–60"; common 36" × 24", 48" × 36", 48" × 60", 60" × 36", 72" × 48", 96" × 60" · EU: as O-08.

---

## O-12 Top / bottom hung window

**IFC** IfcWindow · WINDOW · panel OperationType TOPHUNG (awning) / BOTTOMHUNG (hopper) / PIVOTHORIZONTAL · **P3**

**Scope** Single sash hinged at top or bottom, or horizontally pivoting; stay arms at high LOD.

**Based on** FreeCAD "Awning" preset (reference) · IFC.

**Parameters** as O-08 plus `hinge` top | bottom | pivot · `open_angle` (drawing; restrictor default).

**Size catalogues** US awning: widths 24"–46", heights 20"–92" (makers' ranges) · EU: as O-08.

**LOD** Elevation triangle apex at the hinge edge.

---

## O-13 — merged into all windows

There is no separate shaped-window object: custom outlines are a feature of every window (see shared rules above). Reference test object #2 is therefore **O-08 with a custom outline** (arched top, round, gable). ID O-13 stays unused so other IDs don't change.

---

## O-14 Roof window

**IFC** IfcWindow · SKYLIGHT · panel OperationType PIVOTHORIZONTAL / TOPHUNG · **P2**

**Scope** Window in a pitched roof: frame, sash (centre-pivot or top-hung), glazing, flashing outline, interior lining (splay) at medium/high. Host: roof slab (IfcRoof / IfcSlab ROOF); oriented along the roof slope.

**Based on** — · market standard sizes shared across several makers.

**Inputs** Host roof slab (pitch read from host); flashing type by roof covering.

**Parameters** `width`, `height` (outer frame, along slope) · `operation` centre_pivot | top_hung · `flashing` none | profiled | flat · `lining_splay` (interior reveal angles) · `handle` top | bottom.

**Rules** Host pitch within window's allowed range (e.g. 15°–90°, maker data) · escape: top-hung sizes can satisfy `escape_windows` (computed).

**Size catalogues** EU (de facto, several makers): 55 × 78, 55 × 98, 66 × 98, 66 × 118, 78 × 98, 78 × 118, 78 × 140, 78 × 160, 94 × 118, 94 × 140, 114 × 118, 114 × 140, 134 × 98, 134 × 140 cm · US skylight sizes (curb/deck-mounted, inches) to collect.

**LOD** Plan: outline projected on plan with roof slope (overhead class when above cut plane).

**Open** Maker size codes are trademarks; catalogue uses dimensions only.

---

## O-15 Opening / niche

**IFC** IfcOpeningElement · OPENING (through) / RECESS (niche) · **P2**

**Scope** Void in a wall or slab without a filling: rectangular, arched, or custom outline; through or recess with depth. Optional reveal/lintel lines in plan.

**Based on** — · IFC.

**Inputs** Optional `outline` slot (as O-13) · host wall or slab.

**Parameters** `width`, `height`, `sill_height` · `type` through | recess · `depth` (recess) · `shape` rectangle | arch | custom.

**LOD** Plan: low gap lines · medium + lintel line above (overhead) · elevation outline.

---

## Curtain walls — shared rules (O-16, O-17, O-18)

Curtain walls are a key element for high-rise and complex façades, so they get their own sub-family.

- **IFC:** `IfcCurtainWall` (PredefinedType only USERDEFINED / NOTDEFINED → `ObjectType` STICK, UNITISED, STRUCTURAL_GLASS) aggregating `IfcMember` · MULLION (used for vertical mullions *and* horizontal transoms; IFC has no separate transom type), `IfcPlate` · CURTAIN_PANEL (glazed and opaque panels), glass fins as `IfcMember` · USERDEFINED (GLASS_FIN), fixings (spider fittings, clamps, brackets) as discrete accessories / fasteners *(exact IFC class to decide)*, nested windows and doors (O-08, O-12, O-02, O-03) in grid cells. `Pset_CurtainWallCommon` (IsExternal, etc.).
- **Input:** slot `surface` — either a `baseline` (polyline or curve in plan) + bottom/top levels, or a planar / single-curved face (vertical or sloped).
- **Grid:** U (along) and V (up) divisions, each by count, fixed spacing, list of positions, or **levels** (transoms follow storeys: sill, vision, spandrel zones per floor). Grid lines can be added/removed per bay. Corners: outside / inside, mitred or butt-glazed.
- **Panel types per cell:** vision glass (IGU, thickness and make-up as data), spandrel (opaque glass, metal, stone), shadow box, operable vent (nested O-08 / O-12), door (nested O-02 / O-03), louvre, open.
- **Joint types per grid line** (the key difference between systems): `captured` (pressure plate + cover cap), `butt_joint` (silicone joint, no outside cap), `ssg` (structural silicone glazing, 2- or 4-sided, outside flush glass), `open_joint`. Vertical and horizontal lines can differ (e.g. butt-jointed verticals with captured horizontals).
- **Slab edges:** fire-stop / smoke seal line and anchor brackets at each floor slab (high LOD), so the façade reads correctly in section.
- **Rules (all three):** panel size within maker glass limits (data, warning) · mullion depth vs. span (simple rule-of-thumb check; real structural design is out of scope) · joint widths ≥ min · operable vent sizes · `guards` where vision glass reaches the floor (barrier / safety glazing check) · deflection and wind loads are **data only**, not calculated.
- **Based on:** FreeCAD BIM CurtainWall tool (LGPL, reference only: subdivides a base face into panels with vertical, horizontal and diagonal mullions, profiles per direction, glass/solid panels from a multi-material) · IFC · EN 13830 (curtain walling product standard) · structural sealant glazing: ETAG 002 / EN 15434 (bonded glass) · glass design: DIN 18008 (DE), ASTM E1300 (US) *(values to add)*.
- **Size catalogues:** none (grid-driven). Presets per system type with typical module widths and profile families *(to collect from public maker data)*.
- **LOD (all three):** low — glass surface with grid lines · medium — mullion/transom sections, glass, spandrels, panel types, nested windows/doors · high — profiles with pressure plates/caps or SSG joints, fins, fixings, slab edge details. Plan: mullion sections cut (hatched) + glass lines; elevation: grid with panel types and opening symbols.

---

## O-16 Stick curtain wall

**IFC** IfcCurtainWall · USERDEFINED (STICK) · **P1** (high-rise core element; also exercises surface/grid inputs and nesting)

**Scope** Mullion-and-transom system assembled on site: continuous mullions anchored to slabs, transoms between them, glazing **captured** with pressure plates and caps, or **butt-jointed** (silicone joints, no caps) on one or both directions, or **SSG** (glass bonded, flush outside). Spandrel zones, shadow boxes, vents and doors in cells. Corners outside/inside. *Not:* thermal/structural analysis, bracket design.

**Parameters** grid U/V (see shared rules) · `mullion_profile` (face width × depth, default 0.05 × 0.15 m / 2" × 6") · `transom_profile` · `joint_vertical`, `joint_horizontal` captured | butt_joint | ssg · `cap_profile` (captured: depth, shape) · `butt_joint_width` (default 0.015–0.02 m) · `glass_thickness` (IGU, default 0.032 m) · `glass_offset` (glass plane vs. mullion face) · `spandrel_zone` per floor (height from slab) · `slab_edge` (fire stop line, bracket type).

**Rules** Shared rules + mullion span between anchors (floor-to-floor) vs. depth.

---

## O-17 Unitised curtain wall

**IFC** IfcCurtainWall · USERDEFINED (UNITISED) · each unit an `IfcElementAssembly` *(to decide)* · **P2**

**Scope** Factory-built units, typically one floor high and one module wide, hung from slab-edge brackets: split (male/female) mullions, stack joint at each floor (with the horizontal split transom), integrated spandrel and vision areas inside each unit, interlocking joints visible in plan/section at high LOD. The usual system for high-rise. Same joint options on the glass (captured, SSG).

**Parameters** `module_width` · `unit_height` (= floor-to-floor, from levels) · `stack_joint_height` (above slab) · `split_mullion` (profile pair) · unit types per cell (vision / spandrel split heights) · joint types as O-16.

**Rules** Units align with slab levels (error if a level falls inside a unit without a stack joint) · module width × height within transport/handling limits *(data)*.

---

## O-18 Structural glass façade (all-glass)

**IFC** IfcCurtainWall · USERDEFINED (STRUCTURAL_GLASS) · glass panels IfcPlate CURTAIN_PANEL · fins IfcMember USERDEFINED (GLASS_FIN) · **P2**

**Scope** Frameless, Apple-store-style glass walls: large laminated glass panes with **butt joints** (silicone), stabilised by **glass fins** (perpendicular glass beams) and/or a cable net or steel structure, fixed by **point fittings** (spider brackets, countersunk or clamp bolts), **linear clamps** or **structural bonding**. Floor and head channels (shoes), fin-to-pane connections, corner butt-glazing. Very tall single panes and laminated fin splices.

**Support types** `glass_fins` | `cable_net` | `steel_mullions` | `spider_on_steel` · **Fixing types** `point_fixed` (spider: 1-, 2-, 4-arm) | `clamped` | `bonded` | `channel` (top/bottom shoe only).

**Parameters** grid U (pane widths) and V (pane heights, may be a single pane floor-to-ceiling) · `pane_build_up` (laminated layers, e.g. 3 × 12 mm + interlayers; IGU optional) · `fin_depth`, `fin_thickness` (laminated plies), `fin_side` inside | outside · `fin_splice` (heights over max pane length: spliced fins with steel plates) · `fitting_type`, `fitting_spacing` (edge distance of point fixings) · `butt_joint_width` · `base_shoe` / `head_channel` (depth, recess into floor/ceiling).

**Rules** Shared rules + pane size within maker maximums *(data, warning)* · point fixing edge distances ≥ min *(values to add)* · fin depth vs. height rule of thumb (warning only; structural glass design under DIN 18008 / ASTM E1300 is the engineer's job).

**LOD** medium: panes, fins, simple fitting blocks · high: spider arms and bolt heads, shoe channels, splice plates · plan: pane lines + fins (cut, hatched as glass) + fittings symbols.

**Open** Exact IFC classes for spiders and clamps; whether cable-net façades become their own object.

---

## Sources

- bim-all-doors: github.com/dormakaba/bim-all-doors (CC0), parameters in `Source/Module/01 BAD main/…/90_Parameters.xml`
- FreeCAD BIM CurtainWall: wiki.freecad.org/Arch_CurtainWall (LGPL)
- IFC 4.3: IfcCurtainWallTypeEnum (USERDEFINED, NOTDEFINED), IfcMemberTypeEnum (MULLION…), IfcPlateTypeEnum (CURTAIN_PANEL…)
- EN 13830 scope: din.de, intertek.com; ETAG 002 (EOTA, structural sealant glazing kits); EN 15434 / EN 13022 (bonding) via BSI catalogue
- FreeCAD window presets: wiki.freecad.org/Arch_Window (Fixed, Open 1-pane, Open 2-pane, Sash 2-pane, Sliding 2-pane, Simple door, Glass door, Sliding 4-pane, Awning, Opening only, Sliding door); ArchWindow.py (opening modes)
- Bonsai/IfcOpenShell parametric features and licences: IfcOpenShell repository README (Bonsai GPL-3.0-or-later; libraries LGPL-3.0-or-later)
- US window sizes: angi.com, modernize.com, hansons.com, rustica.com, lowes.com, homeguide.com standard window size guides
- IRC R310: see `rulesets.md`
- Roof windows: velux.co.uk size guide; FAKRO flashing table; DAKEA technical data (shared size range)
- Garage doors: normstahl.com standard sizes; doorsuperstore.co.uk; homedepot.com, clopaydoor.com; garagedoorsonline.co.uk (125 mm steps)
- DIN 18101 / UK / US door sizes: see `examples/door/README.md`
