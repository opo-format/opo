# Lifts and escalators — object sheets T-01 … T-03

Shared rules for this family:
- **IFC:** `IfcTransportElement` (subtype of `IfcTransportationDevice`) with IFC 4.3 `IfcTransportElementTypeEnum`: **ELEVATOR, ESCALATOR, MOVINGWALKWAY** (also CRANEWAY, HAULINGGEAR, LIFTINGGEAR, not used here). Property sets `Pset_TransportElementCommon` and, for lifts, `Pset_TransportElementElevator` *(names to verify against the IFCX snapshot)*.
- **Scope rule:** these objects give the architect the **spaces** a lift or escalator needs and a recognisable body: shaft, pit, headroom, car, landing doors, truss, balustrades, the floor openings they cut. Machinery, guide rails, counterweights, controllers and drives are not modelled ("detailed, not a simulator"). Maker data replaces the defaults when a product is chosen.
- **Host:** the building's levels. Each object spans a list of levels and cuts openings in the slabs it passes (`IfcOpeningElement` per slab, like the door's void).
- **Norms:** EU — EN 81-20 (lifts: construction and installation), EN 81-70 (accessibility of lifts; ISO 8100-7 is the international counterpart), EN 115-1 (escalators and moving walks) · US — ASME A17.1 (safety code for elevators and escalators), 2010 ADA Standards §407 (lift cars) · UK — the same EN standards.
- **LOD (all):** low — outline of shaft or truss with the symbol (cross in a lift shaft, arrow on an escalator) · medium — car, doors, steps/pallets as a surface, balustrades · high — door panels and frames, handrail profiles, comb plates.

---

## T-01 Lift (elevator)

**IFC** IfcTransportElement · ELEVATOR · landing doors as nested `IfcDoor` · DOOR (OperationType SLIDING_TO_LEFT / SLIDING_TO_RIGHT / DOUBLE_DOOR_SLIDING) · shaft walls are **not** part of the object (they are walls); the object reserves the shaft space and checks it · **P2** (core of every high-rise)

**Scope** One lift in a shaft: car (internal clear width × depth × height), car door and one landing door per served level (front, or front and rear for through-cars), shaft clear space, pit depth below the lowest level, headroom above the highest level, slab openings. Shown in plan with the car, the doors and the shaft symbol. *Not:* machine room design, guide rails, counterweight, lift calculations (traffic analysis).

**Based on** — · EN 81-70 car types · EN 81-20 · ISO 4190-1 (lift installation dimensions: car, shaft, pit and headroom tables) *(values to collect)* · ASME A17.1 · ADA §407.

**Inputs** Levels served (list) · position and orientation of the shaft (insertion point + front direction).

**Parameters** `car_type` (EN 81-70 type 1–5, or custom) · `car_width`, `car_depth`, `car_height` (default 2.2 m / 7'4") · `door_width`, `door_height` (default 2.1 m / 7'0") · `door_type` side_opening | centre_opening · `door_position` centred | side · `entrances` front | front_rear | front_side · `shaft_width`, `shaft_depth` (derived from car and door with clearance defaults, or entered) · `pit_depth`, `headroom` (derived from speed class or entered *(defaults to collect from ISO 4190-1)*) · `rated_load` (data, kg) · `speed` (data, m/s) · `fire_lift` (bool, data).

**Rules** Car and door ≥ minimum for the chosen car type (rule set `lifts`, below) · shaft ≥ car + door clearances (check) · pit and headroom fit between the lowest/highest served level and the building's slabs (check against levels) · landing in front of each door free of obstacles (annotation zone; size from `accessibility`).

**Rule set `lifts`** (EU, EN 81-70 car types: minimum car width × depth / minimum door clear width):

| Type | Car (mm) | Door (mm) | Typical use |
|---|---|---|---|
| 1 | 1000 × 1250 (450 kg) / 1000 × 1300 | 800 | one wheelchair user |
| 2 | 1100 × 1400 | 900 | wheelchair user + companion |
| 3 | 1100 × 2100 | 900 | wheelchair user + companion, through or adjacent doors |
| 4 | 1600 × 1400 or 1400 × 1600 | 900 | wheelchair turning in the car |
| 5 | 2000 × 1400 or 1400 × 2000 | 1100 | stretcher / large wheelchairs |

US: ADA §407.4 car sizes by door position *(values to collect from the ADA text)*.

**Size catalogues** EN 81-70 types 1–5 as variants · rated loads and matching car sizes from ISO 4190-1 *(to collect)* · US typical car sizes by maker *(to collect)*.

**LOD** Plan low: shaft rectangle with a cross · medium: car outline, doors (open line), shaft · high: door panels, frames, car wall thickness. Section: pit, car at the lowest level, headroom zone.

**Open** Whether the shaft walls should be generated as a nested wall assembly (option) or always left to the wall tool.

---

## T-02 Escalator

**IFC** IfcTransportElement · ESCALATOR · **P2**

**Scope** One escalator between two levels: truss (with supports at top and bottom), steps, balustrades (glass or panel) with moving handrails, comb plates and landing plates, floor openings and the clearance zones at each end. Direction up/down as data and symbol. *Not:* drive station internals.

**Based on** — · EN 115-1 · ASME A17.1.

**Inputs** Lower level, upper level, insertion point at the lower landing + direction.

**Parameters** `inclination` 30° | 35° | 27.3° (default 30°) · `step_width` 0.6 | 0.8 | 1.0 m · `rise` (derived from the levels) · `horizontal_steps` at each end (default 2 *(EN 115-1 minimum per speed, to verify)*) · `balustrade` glass | panel · `balustrade_height` (default 0.9 m, typical) · `speed` (data, m/s) · `truss_depth` (maker data; default *(to collect)*) · `direction` up | down | reversible.

**Rules** Inclination: ≤ 30°, or ≤ 35° only when rise ≤ 6 m and speed ≤ 0.5 m/s (EN 115-1; error otherwise) · free zone at each end ≥ min *(EN 115-1 value to verify)* (annotation and check against walls) · headroom above the steps ≥ min *(to verify)* · slab opening derived from the truss and clearances.

**Size catalogues** Step width × inclination combinations (0.6 / 0.8 / 1.0 m × 27.3° / 30° / 35°) as variants.

**LOD** Plan: outline with direction arrow and step lines (low: outline + arrow) · section: truss, steps, balustrade, handrail · high: comb plates, handrail profile.

---

## T-03 Moving walkway

**IFC** IfcTransportElement · MOVINGWALKWAY · **P3**

**Scope** Horizontal or inclined moving walk: pallet band, balustrades, handrails, landing plates, pit. Same structure as T-02.

**Based on** — · EN 115-1 · ASME A17.1.

**Inputs** Start and end points (same level or two levels).

**Parameters** `inclination` 0–12° (derived from the two points) · `pallet_width` 0.8 | 1.0 m (EN 115-1) · `length` (derived) · `balustrade` glass | panel · `balustrade_height` (default 0.9 m, typical) · `speed` (data).

**Rules** Inclination ≤ 12° (EN 115-1; error) · free zones at the ends as T-02.

**Size catalogues** Pallet widths 0.8 and 1.0 m.

**LOD** As T-02.

---

## Sources

- IFC 4.3 `IfcTransportElementTypeEnum` (CRANEWAY, ELEVATOR, ESCALATOR, HAULINGGEAR, LIFTINGGEAR, MOVINGWALKWAY): ifcopenshell IFC4X3_ADD2 schema
- EN 81-70 car types 1–5: maker and consultant summaries of EN 81-70:2021 (car and door minimums); ISO 8100-7:2024 counterpart
- EN 115-1 inclination (≤ 30°, 35° up to 6 m rise at ≤ 0.5 m/s), step widths 600/800/1000 mm, moving walks 0–12° with 800/1000 mm pallets: escalator maker planning guides
- ASME A17.1 / CSA B44: SAI Global catalogue page (scope)
