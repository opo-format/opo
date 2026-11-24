"""Starter hatches and materials for OPO class templates (spec §4.6). Written for OPO, CC0.

Hatch line family: angle (degrees), origin [x, y], offset [along, across] to the next parallel line,
dashes (positive = dash, negative = gap, 0 = dot; omitted = continuous). Lengths in metres:
real lengths when scale_mode = "model", printed lengths when scale_mode = "paper" (0.002 = 2 mm on the sheet).
Patterns are illustrative drawing conventions, not norm values.
"""
import math

def fam(angle, offset, origin=(0.0, 0.0), dashes=None):
    d = {"angle": angle, "origin": [round(origin[0], 9), round(origin[1], 9)], "offset": [round(offset[0], 9), round(offset[1], 9)]}
    if dashes: d["dashes"] = [round(x, 9) for x in dashes]
    return d

def zigzag(period, height):
    """Soft insulation zigzag built from two dashed families (rows of up and down strokes)."""
    th = math.degrees(math.atan2(height, period / 2))
    s = math.hypot(period / 2, height)
    t = math.radians(th)
    up = fam(th, (height * math.sin(t), height * math.cos(t)), (0, 0), [s, -s])
    down = fam(-th, (-height * math.sin(t), height * math.cos(t)), (period / 2, height), [s, -s])
    return [up, down]

HATCHES = {
    "solid_dark": {"label": "Solid, dark", "kind": "solid", "colour": "#3a3a3a"},
    "solid_light": {"label": "Solid, light grey", "kind": "solid", "colour": "#d4d4d4"},
    "none": {"label": "No hatch", "kind": "none"},
    "concrete": {"label": "Concrete", "kind": "lines", "scale_mode": "paper",
                 "lines": [fam(0, (0.0011, 0.0019), dashes=[0, -0.0027]), fam(37, (0.0017, 0.0031), (0.0007, 0.0004), [0.0005, -0.0041])]},
    "reinforced_concrete": {"label": "Reinforced concrete", "kind": "lines", "scale_mode": "paper",
                            "lines": [fam(45, (0, 0.0024)), fam(0, (0.0011, 0.0019), dashes=[0, -0.0027])]},
    "masonry": {"label": "Masonry", "kind": "lines", "scale_mode": "paper", "lines": [fam(45, (0, 0.0014))]},
    "block": {"label": "Concrete block", "kind": "lines", "scale_mode": "paper", "lines": [fam(45, (0, 0.0028)), fam(135, (0, 0.0028))]},
    "insulation_soft": {"label": "Insulation, soft (zigzag)", "kind": "lines", "scale_mode": "paper", "lines": zigzag(0.004, 0.0025)},
    "insulation_rigid": {"label": "Insulation, rigid", "kind": "lines", "scale_mode": "paper",
                         "lines": [fam(45, (0, 0.0035)), fam(135, (0, 0.0035)), fam(0, (0, 0.0035), dashes=[0.0005, -0.003])]},
    "plaster": {"label": "Plaster / render", "kind": "lines", "scale_mode": "paper", "lines": [fam(0, (0.0006, 0.0009), dashes=[0, -0.0013])]},
    "screed": {"label": "Screed", "kind": "lines", "scale_mode": "paper",
               "lines": [fam(0, (0.0009, 0.0013), dashes=[0, -0.0019]), fam(0, (0.0015, 0.0026), (0.0004, 0.0006), [0.0004, -0.0026])]},
    "timber": {"label": "Timber (sawn, in section)", "kind": "lines", "scale_mode": "paper", "lines": [fam(135, (0, 0.0022), dashes=[0.006, -0.0012])]},
    "earth": {"label": "Earth", "kind": "lines", "scale_mode": "paper",
              "lines": [fam(45, (0, 0.003), dashes=[0.004, -0.0015]), fam(45, (0.0025, 0.003), (0, 0.0015), [0.0008, -0.0047])]},
    "brick_stretcher_elevation": {"label": "Brickwork, stretcher bond (elevation, real size)", "kind": "lines", "scale_mode": "model",
                                  "lines": [fam(0, (0, 0.075)), fam(90, (0.075, -0.1125), dashes=[0.075, -0.075])],
                                  "note": "225 × 75 mm module (brick + joint), illustrative."},
}

def mat(label, category, colour, cut, surface=None, density=None, ifc=None):
    d = {"label": label, "category": category, "colour": colour, "cut": {"hatch": cut}}
    if surface: d["surface"] = {"hatch": surface}
    if density: d["density"] = density
    d["ifc_name"] = ifc or label
    return d

MATERIALS = {
    "concrete": mat("Concrete", "concrete", "#b9b6ad", "concrete", density=2400),
    "reinforced_concrete": mat("Reinforced concrete", "concrete", "#a9a69c", "reinforced_concrete", density=2500),
    "brick_masonry": mat("Brick masonry", "masonry", "#b5653f", "masonry", surface="brick_stretcher_elevation"),
    "concrete_block": mat("Concrete block masonry", "masonry", "#9e9b94", "block"),
    "mineral_wool": mat("Mineral wool insulation", "insulation", "#e9d27a", "insulation_soft"),
    "rigid_insulation": mat("Rigid insulation board", "insulation", "#e3e3e3", "insulation_rigid"),
    "plaster": mat("Gypsum plaster", "finish", "#efece5", "plaster"),
    "render": mat("External render", "finish", "#e6e0d2", "plaster"),
    "plasterboard": mat("Plasterboard", "finish", "#f2f2f2", "solid_light"),
    "cement_screed": mat("Cement screed", "finish", "#c8c4bb", "screed"),
    "timber": mat("Timber", "timber", "#c49a6c", "timber"),
    "steel": mat("Steel", "steel", "#7a8088", "solid_dark", density=7850),
    "stainless_steel": mat("Stainless steel", "steel", "#b8bcc2", "solid_dark"),
    "painted_timber": mat("Timber, painted", "timber", "#f1efe9", "timber"),
    "cast_iron": mat("Cast iron", "steel", "#4b4e52", "solid_dark"),
    "copper": mat("Copper", "metal", "#b87333", "solid_dark"),
    "sheet_metal": mat("Sheet metal, coated", "metal", "#d9dbde", "solid_dark"),
    "glass": mat("Glass", "glass", "#bcd8e6", "none", density=2500),
    "membrane": mat("Membrane", "membrane", "#333333", "solid_dark"),
    "ceramic_tile": mat("Ceramic tile", "finish", "#e8e4dc", "solid_light"),
    "earth": mat("Earth", "earth", "#8b6f4e", "earth"),
}

def subset(material_ids):
    """Materials used by a template plus the hatches they need, so each file is self-contained."""
    mats = {m: MATERIALS[m] for m in material_ids}
    hatch_ids = set()
    for m in mats.values():
        hatch_ids.add(m["cut"]["hatch"])
        if "surface" in m: hatch_ids.add(m["surface"]["hatch"])
    return mats, {h: HATCHES[h] for h in sorted(hatch_ids)}
