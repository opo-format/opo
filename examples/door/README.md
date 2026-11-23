# Door — reference test object #1 (v0.2)

A single swing door written as a real IFCX document with the `opo::` extension. Detailed enough for 1:20 drawings and schedules, deliberately not a door configurator: frame, rebated or flush leaf, threshold, hinges and a lever handle with roses, nothing more.

```
single-swing-door/                unpacked .opo (zip root)
├── object.ifcx                   type node, opo:: definition, baked fallback (DIN 875 × 2125)
└── layers/
    ├── sizes-din18101.ifcx       DIN 18101: 625–1125 × 2000 / 2125 (modular sizes)
    ├── sizes-uk-metric.ifcx      BS 4787: leaf 526–926 × 2040, 40 mm
    ├── sizes-uk-imperial.ifcx    UK imperial: leaf 2'0"–2'9" × 6'6", 35 mm
    ├── sizes-us.ifcx             US: leaf 2'0"–3'0" × 6'8", 1-3/8"
    ├── ruleset-de-din18040.ifcx  accessibility: clear passage ≥ 900 mm
    └── ruleset-us-ada.ifcx       accessibility: 32" clear with door open 90°, hardware 34–48"
project-snippet.ifcx              NOT part of the .opo: a placed instance
```

All lengths are in metres, angles in degrees (IFCX defaults).

## What it is based on

| Source | Licence | What was taken |
|---|---|---|
| [bim-all-doors](https://github.com/dormakaba/bim-all-doors) by dormakaba (commit `9a174ae`, v1.90) | CC0 | The dimension chain with a selectable **nominal reference** (wall opening, modular size, frame outside, leaf, clear passage), frame types, rebate and leaf-lap logic, 115 mm default wall |
| IFC 4.3 `Pset_DoorLiningProperties`, `Pset_DoorPanelProperties` | buildingSMART | Parameter names and meaning: LiningDepth, LiningThickness, CasingThickness, CasingDepth, ThresholdThickness, PanelDepth |
| [OSArch door generator discussion](https://community.osarch.org/discussion/comment/24127/) | CC-BY 4.0 | Lining-with-stop and hollow metal frame types |
| DIN 18100 / DIN 18101 | norm | Opening = modular + 10 mm (w) / + 5 mm (h); rebate, clear passage and leaf sizes |
| BS 4787 and UK imperial sizes | norm / market | UK leaf sizes and thicknesses |
| US industry door sizes | market | Leaf widths 24–36", 80" high; rough opening = leaf + 2" × + 2½" |
| DIN 18040-1, 2010 ADA Standards §404 | regulation | Accessibility rule sets |

## The dimension chain

One nominal size is entered; `nominal_reference` says what it measures. Everything else follows:

```
wall opening ── fit gap ──▶ frame outside ── lining thickness ──▶ frame rebate ── stop ──▶ clear passage
                                                                       └── ± leaf lap / gap ──▶ leaf
```

Checked against the norm tables:

| Variant | Opening | Rebate | Clear passage | Leaf | Usable clear (open 90°) |
|---|---|---|---|---|---|
| DIN 875 × 2125 (default) | 885 × 2130 | 841 × 2108 | 811 × 2093 | 860 × 2110 | 771 |
| DIN 1000 × 2125 | 1010 × 2130 | 966 × 2108 | 936 × 2093 | 985 × 2110 | 896 |
| UK 2040 × 826 | 906 × 2088 | 832 × 2051 | 808 × 2039 | 826 × 2040 | 768 |
| US 3'0" × 6'8" | 38" × 82½" rough opening | 36¼" | 35⅜" | 36" × 80" | 34" |

DIN values match DIN 18101 exactly (e.g. 885 / 841 / 811 / 860 × 2110). US values match the industry rule of thumb (rough opening leaf + 2" × + 2½", ~34" clear for a 36" door).

## Rule checks

| | No rule set (default) | DIN 18040 | ADA |
|---|---|---|---|
| DIN 875 × 2125 | ✅ | ⚠️ clear 811 < 900 | ⚠️ |
| DIN 1000 × 2125 | ✅ | ✅ | ✅ |
| UK 2040 × 926 | ✅ | ✅ | ✅ |
| US 2'8" | ✅ | ⚠️ | ⚠️ usable 30" < 32" |
| US 3'0" | ✅ | ⚠️ | ✅ |

This matches practice: German accessible doors are the 1010 nominal size; under ADA a 32" door does not give 32" clear, a 36" door does.

## Levels of detail

| | Low (≤ 1:200) | Medium (1:100–1:50) | High (≥ 1:20) |
|---|---|---|---|
| 3D | Slab in the frame outline | Lining, stop, casings, leaf (with rebate), simple lever both sides, threshold if set | + round lever handle with roses (Ø52), Ø19 × 130 lever, key rose 72 mm below, hinge knuckles |
| Plan | Leaf line + swing arc | Jambs with stop and casings (cut, hatched), open leaf, swing arc | Cut from 3D + open leaf and arc |
| Elevation | Frame outline | Casing, frame, leaf, lever, swing indicator | Projected from 3D + swing indicator |
| Section | Cut from 3D at each level |||

## Market values that are typical practice (not norm values)

UK lining 32 mm, architrave 69 × 15, stop 12 × 38, handle 1000 mm, backset 44 mm; US jamb ¾", casing 2¼" × 11/16", stop 7/16" × 1⅜", undercut ½", handle 36", backset 2⅜"; hinge positions 250 mm from the leaf ends. These are marked in the object and should be reviewed by someone working in those markets.

## How it was checked

- Every `opo::` attribute is declared in the schema; no dangling `children` / `inherits`.
- Every name in recipe arguments, `when` conditions, visibility conditions and the IFC mapping resolves.
- All FEEL formulas were evaluated with a FEEL-subset interpreter for the default and all 24 catalogue variants, under no rule set, DIN 18040 and ADA (table above). Each variant's IFC `OverallWidth/OverallHeight` matches the formulas.
- Baked meshes (lining, stop, casings, leaf, handle, void) and the plan arc match the recipe for the default values; the rebated leaf lap clears the lining and the front casing.

## Known limits

- IFCX alpha has no exact solids; the baked fallback is a mesh. Variants reuse the default's baked geometry (open question in spec §12).
- No double doors, side lights, fanlights, closers or locks: later objects or nested OPOs.
