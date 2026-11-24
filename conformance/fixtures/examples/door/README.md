# Door — reference test object #1 (v0.3)

> Frozen fixture of the conformance suite. The maintained door is the library object `objects/door-single-swing` (YAML sources).

A single swing door written as a real IFCX document with the `opo::` extension. Detailed enough for 1:20 drawings and schedules, deliberately not a door configurator: frame, rebated or flush leaf, threshold, hinges and a lever handle with roses, nothing more.

```
single-swing-door/                  unpacked .opo (zip root)
├── object.ifcx                     type node, opo:: definition, baked fallback (opening 900 × 2100)
└── layers/
    ├── sizes-generic-metric.ifcx   openings 700–1100 × 2100 (generic: no EU door size norm exists)
    ├── sizes-uk-metric.ifcx        BS 4787: leaf 526–926 × 2040, 40 mm
    ├── sizes-uk-imperial.ifcx      UK imperial: leaf 2'0"–2'9" × 6'6", 35 mm
    ├── sizes-us.ifcx               US: leaf 2'0"–3'0" × 6'8", 1-3/8"
    ├── ruleset-iso-21542.ifcx      accessibility (EU / international): clear opening ≥ 800 mm, handle 800–1000 mm
    └── ruleset-us-ada.ifcx         accessibility: 32" clear with door open 90°, hardware 34–48"
project-snippet.ifcx                NOT part of the .opo: a placed instance
```

All lengths are in metres, angles in degrees (IFCX defaults).

## What it is based on

| Source | Licence | What was taken |
|---|---|---|
| [bim-all-doors](https://github.com/dormakaba/bim-all-doors) by dormakaba (commit `9a174ae`, v1.90) | CC0 | The dimension chain with a selectable **nominal reference** (wall opening, frame outside, leaf, clear passage), frame types, rebate and leaf-lap logic, frame-system default values, 115 mm default wall |
| IFC 4.3 `Pset_DoorLiningProperties`, `Pset_DoorPanelProperties` | buildingSMART | Parameter names and meaning: LiningDepth, LiningThickness, CasingThickness, CasingDepth, ThresholdThickness, PanelDepth |
| [OSArch door generator discussion](https://community.osarch.org/discussion/comment/24127/) | CC-BY 4.0 | Lining-with-stop and hollow metal frame types |
| ISO 21542:2021 (EU: EN 17210 functional requirements) | standard | EU / international accessibility rule set |
| BS 4787 and UK imperial sizes | norm / market | UK leaf sizes and thicknesses |
| US industry door sizes, 2010 ADA Standards §404 | market / regulation | US leaf sizes, rough opening rule, ADA rule set |

OPO uses EN/ISO norms only for Europe, no national norms. There is no EU-wide door size standard, so the metric catalogue is **generic** (round opening sizes) and labelled as not a norm.

## The dimension chain

One nominal size is entered; `nominal_reference` says what it measures. Everything else follows:

```
wall opening ── fit gap ──▶ frame outside ── lining thickness ──▶ frame rebate ── stop ──▶ clear passage
                                                                       └── ± leaf lap / gap ──▶ leaf
```

| Variant | Opening | Rebate | Clear passage (closed) | Leaf | Usable clear (open 90°) |
|---|---|---|---|---|---|
| Opening 900 × 2100 (default) | 900 × 2100 | 856 × 2078 | 826 × 2063 | 875 × 2080 | 786 |
| Opening 1000 × 2100 | 1000 × 2100 | 956 × 2078 | 926 × 2063 | 975 × 2080 | 886 |
| UK 2040 × 826 | 906 × 2088 | 832 × 2051 | 808 × 2039 | 826 × 2040 | 768 |
| US 3'0" × 6'8" | 38" × 82½" rough opening | 36¼" | 35⅜" | 36" × 80" | 34" |

US values match the industry rule of thumb (rough opening = leaf + 2" × + 2½", about 34" clear for a 36" door).

## Rule checks

| | No rule set (default) | ISO 21542 | ADA |
|---|---|---|---|
| Opening 900 × 2100 | ✅ | ⚠️ usable 786 < 800 | ⚠️ |
| Opening 1000 × 2100 | ✅ | ✅ | ✅ |
| UK 2040 × 926 | ✅ | ✅ | ✅ |
| US 2'8" | ✅ | ⚠️ | ⚠️ usable 30" < 32" |
| US 3'0" | ✅ | ✅ | ✅ |

An accessible door needs roughly a 1000 mm opening (or a 36" US leaf), which matches practice. The default handle height is 1.0 m, the top of the ISO 21542 range.

## Levels of detail

| | Low (≤ 1:200) | Medium (1:100–1:50) | High (≥ 1:20) |
|---|---|---|---|
| 3D | Slab in the frame outline | Lining, stop, casings, leaf (with rebate), simple lever both sides, threshold if set | + round lever handle with roses (Ø52), Ø19 × 130 lever, key rose 72 mm below, hinge knuckles |
| Plan | Leaf line + swing arc | Jambs with stop and casings (cut, hatched), open leaf, swing arc | Cut from 3D + open leaf and arc |
| Elevation | Frame outline | Casing, frame, leaf, lever, swing indicator | Projected from 3D + swing indicator |
| Section | Cut from 3D at each level |||

## Values that are typical practice (not norm values)

Frame-system defaults from bim-all-doors (lining 17 mm, stop 15 mm, leaf lap 9.5 mm, floor gap 7 mm); UK lining 32 mm, architrave 69 × 15, stop 12 × 38, backset 44 mm; US jamb ¾", casing 2¼" × 11/16", stop 7/16" × 1⅜", undercut ½", handle 36", backset 2⅜"; hinge positions 250 mm from the leaf ends; key rose 72 mm below the handle.

## How it was checked

- Every `opo::` attribute is declared in the schema; no dangling `children` / `inherits`.
- Every name in recipe arguments, `when` conditions, visibility conditions and the IFC mapping resolves.
- All FEEL formulas were evaluated with a FEEL-subset interpreter for the default and all 19 catalogue variants, under no rule set, ISO 21542 and ADA. Each variant's IFC `OverallWidth/OverallHeight` matches the formulas.
- Baked meshes (lining, stop, casings, leaf, handle, void) and the plan arc match the recipe for the default values.

## Known limits

- IFCX alpha has no exact solids; the baked fallback is a mesh. Variants reuse the default's baked geometry (open question in spec §12).
- No double doors, side lights, fanlights, closers or locks: other objects or nested OPOs.
