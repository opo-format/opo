# OPO object catalogue

**Draft v0.2 · 24 Nov 2026** · 74 objects in eight families

Every IFC 4.3 element class gets a generated **class template** (`archetypes.md`, `ifc-coverage.md`). On top of those, this is the list of detailed **library objects** the OPO project intends to build, with one specification sheet per object. Every object is built from its sheet; the sheet is updated first when something changes. Spec §4.14 (references) applies to all of them.

| File | Contents |
|---|---|
| [`archetypes.md`](archetypes.md) | The eight archetypes and what every IFC class template contains (the OPO equivalent of family templates) |
| [`ifc-coverage.md`](ifc-coverage.md) | Points to the coverage table generated in the library (all 150 IFC 4.3 element classes with archetype, template, predefined types and library objects) |
| [`rulesets.md`](rulesets.md) | Shared rule sets used by many objects: stairs, guards, handrails, accessibility, escape windows, kitchens (lifts in `transport.md`). EU values from EN/ISO only; UK and US columns. Values with sources, metric and imperial. |
| [`openings.md`](openings.md) | O-01…O-18: doors, windows, openings, curtain walls (stick, unitised, structural glass) |
| [`circulation.md`](circulation.md) | C-01…C-08: stairs, ramps, railings, handrails |
| [`fixtures.md`](fixtures.md) | F-01…F-14: sanitary, kitchen, appliances, built-in storage |
| [`furniture.md`](furniture.md) | E-01…E-08: furniture and lighting |
| [`shading.md`](shading.md) | S-01…S-07: louvres, fins, external blinds, shutters, awnings, screens |
| [`transport.md`](transport.md) | T-01…T-03: lifts, escalators, moving walkways |
| [`structure.md`](structure.md) | K-01…K-08: columns, beams, members, ceilings, raised floors, cladding, trims, chimneys |
| [`mep-site.md`](mep-site.md) | M-01…M-06, G-01…G-03: radiators, air terminals, outlets, switches, sprinklers, hose reels; trees, site furniture, signs |

## Catalogue

Priority: **P1** reference test objects that shape the spec (spec §10) · **P2** core library for a first release · **P3** later.

| ID | Object | IFC class · predefined type | Pri. | Parametric basis | Status |
|---|---|---|---|---|---|
| **O-01** | Single swing door | IfcDoor · DOOR | P1 | bim-all-doors (CC0) | ✅ written |
| O-02 | Double swing door | IfcDoor · DOOR | P2 | bim-all-doors (CC0) | planned |
| O-03 | Sliding door | IfcDoor · DOOR | P2 | FreeCAD Sliding door preset (LGPL, reference only) | planned |
| O-04 | Pocket door | IfcDoor · DOOR | P2 | — (derived from O-03) | planned |
| O-05 | Folding door | IfcDoor · DOOR | P3 | — | planned |
| O-06 | Entrance door assembly (sidelights, fanlight) | IfcDoor · DOOR (nested) | P2 | bim-all-doors sidelight/fanlight (CC0) | planned |
| O-07 | Garage door | IfcDoor · DOOR | P3 | — | planned |
| **O-08** | Casement / tilt-turn window (test object #2 with a custom outline) | IfcWindow · WINDOW | P1 | FreeCAD window presets (LGPL, reference only) | planned |
| O-09 | Hung window (single / double hung) | IfcWindow · WINDOW | P2 | FreeCAD Sash 2-pane preset (reference) | planned |
| O-10 | Sliding window | IfcWindow · WINDOW | P2 | FreeCAD Sliding 2/4-pane presets (reference) | planned |
| O-11 | Fixed window | IfcWindow · WINDOW | P2 | FreeCAD Fixed preset (reference) | planned |
| O-12 | Top / bottom hung window | IfcWindow · WINDOW | P3 | FreeCAD Awning preset (reference) | planned |
| O-13 | *(merged: every window has an editable outline)* | — | — | — | merged into O-08…O-14 |
| O-14 | Roof window | IfcWindow · SKYLIGHT | P2 | — | planned |
| O-15 | Opening / niche | IfcOpeningElement · OPENING / RECESS | P2 | — | planned |
| **O-16** | Stick curtain wall (captured, butt-joint, SSG) | IfcCurtainWall · USERDEFINED (+ IfcMember MULLION, IfcPlate CURTAIN_PANEL) | P1 | FreeCAD CurtainWall (LGPL, reference only) | planned |
| O-17 | Unitised curtain wall | IfcCurtainWall · USERDEFINED | P2 | FreeCAD CurtainWall (reference) | planned |
| O-18 | Structural glass façade (glass fins, point-fixed) | IfcCurtainWall · USERDEFINED (+ glass fins IfcMember) | P2 | — | planned |
| **C-01** | Straight stair | IfcStair · STRAIGHT_RUN_STAIR | P1 | Bonsai stair generator (GPL, reference only) | planned |
| **C-02** | L-shaped stair | IfcStair · QUARTER_TURN_STAIR / QUARTER_WINDING_STAIR | P1 | Bonsai (reference) | planned |
| **C-03** | U-shaped stair | IfcStair · HALF_TURN_STAIR / HALF_WINDING_STAIR | P1 | Bonsai (reference) | planned |
| **C-04** | Stair on a walkline (winders) | IfcStair · CURVED_RUN_STAIR / …_WINDING_STAIR | P1 | — (test object #4, WASM step) | planned |
| C-05 | Spiral stair | IfcStair · SPIRAL_STAIR | P2 | — | planned |
| C-06 | Ramp | IfcRamp · STRAIGHT_RUN_RAMP … HALF_TURN_RAMP | P2 | — | planned |
| **C-07** | Railing / guard | IfcRailing · GUARDRAIL / BALUSTRADE | P1 | Bonsai railing generator (GPL, reference only) | planned |
| C-08 | Wall handrail | IfcRailing · HANDRAIL | P2 | Bonsai WALL_MOUNTED_HANDRAIL (reference) | planned |
| F-01 | WC | IfcSanitaryTerminal · TOILETPAN | P2 | — | planned |
| F-02 | Bidet | IfcSanitaryTerminal · BIDET | P3 | — | planned |
| F-03 | Urinal | IfcSanitaryTerminal · URINAL | P3 | — | planned |
| F-04 | Washbasin | IfcSanitaryTerminal · WASHHANDBASIN | P2 | — | planned |
| F-05 | Shower | IfcSanitaryTerminal · SHOWER | P2 | — | planned |
| F-06 | Bathtub | IfcSanitaryTerminal · BATH | P2 | — | planned |
| F-07 | Kitchen sink | IfcSanitaryTerminal · SINK | P2 | — | planned |
| F-08 | Kitchen base unit | IfcFurniture · USERDEFINED (KITCHEN_BASE_UNIT) | P2 | — | planned |
| F-09 | Kitchen wall unit | IfcFurniture · USERDEFINED (KITCHEN_WALL_UNIT) | P2 | — | planned |
| F-10 | Kitchen tall unit | IfcFurniture · USERDEFINED (KITCHEN_TALL_UNIT) | P2 | — | planned |
| F-11 | Worktop | IfcSystemFurnitureElement · WORKSURFACE | P2 | — | planned |
| F-12 | Kitchen run | IfcFurniture (nested F-08…F-11, F-07, F-13) | P2 | — | planned |
| F-13 | Kitchen / laundry appliance | IfcElectricAppliance · REFRIGERATOR, DISHWASHER, … | P2 | — | planned |
| F-14 | Built-in wardrobe | IfcFurniture · USERDEFINED (WARDROBE) | P3 | — | planned |
| E-01 | Table | IfcFurniture · TABLE | P3 | — | planned |
| E-02 | Chair / stool | IfcFurniture · CHAIR | P3 | — | planned |
| E-03 | Sofa / armchair | IfcFurniture · SOFA | P3 | — | planned |
| E-04 | Bed | IfcFurniture · BED | P3 | — | planned |
| E-05 | Desk / workstation | IfcFurniture · DESK | P3 | — | planned |
| E-06 | Shelving / bookcase | IfcFurniture · SHELF | P3 | — | planned |
| E-07 | Freestanding storage (sideboard, chest) | IfcFurniture · USERDEFINED | P3 | — | planned |
| E-08 | Light fixture | IfcLightFixture · POINTSOURCE / DIRECTIONSOURCE | P3 | — | planned |
| S-01 | Louvres / brise-soleil | IfcShadingDevice · USERDEFINED (LOUVRE) | P2 | — | planned |
| S-02 | Façade fins | IfcShadingDevice · USERDEFINED (FIN) | P2 | — | planned |
| S-03 | External venetian blind | IfcShadingDevice · JALOUSIE | P2 | — | planned |
| S-04 | Roller shutter | IfcShadingDevice · SHUTTER | P2 | — | planned |
| S-05 | Hinged / sliding shutters | IfcShadingDevice · SHUTTER | P3 | — | planned |
| S-06 | Awning | IfcShadingDevice · AWNING | P3 | — | planned |
| S-07 | External screen | IfcShadingDevice · USERDEFINED (SCREEN) | P3 | — | planned |
| T-01 | Lift (elevator) | IfcTransportElement · ELEVATOR | P2 | — | planned |
| T-02 | Escalator | IfcTransportElement · ESCALATOR | P2 | — | planned |
| T-03 | Moving walkway | IfcTransportElement · MOVINGWALKWAY | P3 | — | planned |
| K-01 | Column | IfcColumn · COLUMN / PILASTER | P2 | — | planned |
| K-02 | Beam | IfcBeam · BEAM / JOIST / LINTEL | P2 | — | planned |
| K-03 | Member (brace, post, purlin, rafter, stud) | IfcMember · BRACE / POST / PURLIN / RAFTER / STUD … | P3 | — | planned |
| K-04 | Suspended ceiling | IfcCovering · CEILING | P2 | — | planned |
| K-05 | Raised access floor | IfcCovering · FLOORING | P3 | — | planned |
| K-06 | Cladding | IfcCovering · CLADDING | P2 | — | planned |
| K-07 | Profile trim (skirting, coping, moulding) | IfcCovering · SKIRTINGBOARD / COPING / MOLDING | P3 | — | planned |
| K-08 | Chimney / fireplace | IfcChimney · USERDEFINED | P3 | — | planned |
| M-01 | Radiator / convector | IfcSpaceHeater · RADIATOR / CONVECTOR | P3 | — | planned |
| M-02 | Air terminal | IfcAirTerminal · DIFFUSER / GRILLE / LOUVRE / REGISTER | P3 | — | planned |
| M-03 | Socket outlet | IfcOutlet · POWEROUTLET / DATAOUTLET … | P3 | — | planned |
| M-04 | Switch | IfcSwitchingDevice · TOGGLESWITCH / DIMMERSWITCH … | P3 | — | planned |
| M-05 | Sprinkler head | IfcFireSuppressionTerminal · SPRINKLER | P3 | — | planned |
| M-06 | Fire hose reel / cabinet | IfcFireSuppressionTerminal · HOSEREEL | P3 | — | planned |
| G-01 | Tree / planting | IfcGeographicElement · VEGETATION | P2 | — | planned |
| G-02 | Site furniture (bench, bike rack, bollard, bin) | IfcFurniture · USERDEFINED | P3 | — | planned |
| G-03 | Sign | IfcSign · PICTORAL / MARKER | P3 | — | planned |

"Reference only" means the source's licence (GPL/LGPL) is not compatible with copying code or data into OPO's MIT/Apache crate or CC0 library: we study how it parametrises the object, we do not copy it. "—" means no openly licensed parametric basis was found; those sheets are based on IFC and the norms alone, and a basis should be looked for again before building.

**Parametric bases searched (Nov 2026):** dormakaba bim-all-doors (CC0, doors only); Bonsai/IfcOpenShell parametric door, window, stair, railing, roof (Bonsai GPL-3.0, IfcOpenShell LGPL-3.0); FreeCAD BIM window/door presets (LGPL); OSArch door/window generator discussion (CC-BY 4.0, spec stage). For kitchens, sanitary, furniture, shading, lifts and MEP terminals only commercial maker families were found.

## Markets and unit systems

Every object ships size catalogues for these markets unless the sheet says otherwise:

| Market | Units | Main sources |
|---|---|---|
| **EU** | metric | EN and ISO norms only (ISO 21542, EN 1116, EN 527, EN 81-70, EN 115-1, EN 13830…). National norms are not used; where no EN/ISO norm exists, sizes are generic and labelled as such |
| **UK** | metric and imperial | Approved Documents K and M, BS 4787, UK imperial sizes |
| **US** | imperial | IRC / IBC, 2010 ADA Standards, US industry sizes |

National rules (e.g. Portugal's RGEU and DL 163/2006, Germany's DIN) are not part of OPO; a project can add them as its own rule set layer.

## Sheet template

Every sheet has these parts:

1. **IFC** — class, predefined type, operation/partitioning type, main property sets
2. **Scope** — what the object covers and what it does not (keep objects "detailed, not a simulator")
3. **Based on** — parametric basis, IFC parameters, norms (spec §4.14)
4. **Inputs** — input slots (drawn geometry) and host
5. **Parameters** — the key parameters with metric and imperial defaults
6. **Rules** — derived values, checks, rule sets used (see `rulesets.md`)
7. **Size catalogues** — per market
8. **Levels of detail** — 3D / plan / elevation at low / medium / high
9. **Open questions**

Conventions shared by all objects:
- Lengths stored in metres, angles in degrees (IFCX). Defaults are given as metric / imperial.
- LOD scale ranges: low ≤ 1:200, medium 1:100–1:50, high ≥ 1:20.
- Object axes: x along the host or the object's front, y depth (positive = front / swing side), z up.
- Accessibility and other regulations are **rule-set layers**, off by default.
- IFC enumeration values in the sheets follow IFC 4.3; check them against the pinned IFCX snapshot when building.
