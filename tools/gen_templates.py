"""Generate OPO class templates (spec §4.16, spec/objects/archetypes.md).

Prototype in Python; the Rust generator in the reference crate replaces it later.
Usage: python3 tools/gen_templates.py [repo root]   →  library/templates/<IfcClass>/...
Inputs: tools/ifc4x3_add2_elements.json (classes, predefined types), tools/ifc4x3_psets.json (property and
quantity sets), tools/templates/styles.py (materials and hatches), and the archetype blocks below.
"""
import json, math, re, sys, uuid
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(ROOT / "tools"))
from templates.styles import subset, MATERIALS  # noqa: E402
import recipe as RX  # noqa: E402

VERSION = "0.1.0"
DATE = "2026-11-24"
NS = uuid.UUID("6f706f2d-666f-726d-6174-2e6f72670000")
def pid(name): return str(uuid.uuid5(NS, name))
IMPORTS = [
    {"uri": "https://ifcx.dev/@standards.buildingsmart.org/ifc/core/ifc@v5a.ifcx"},
    {"uri": "https://ifcx.dev/@standards.buildingsmart.org/ifc/core/prop@v5a.ifcx"},
    {"uri": "https://ifcx.dev/@openusd.org/usd@v1.ifcx"},
    {"uri": "https://opo-format.org/schema/0.1/opo@v0.1.ifcx"},
]
TREE = json.load(open(ROOT / "tools/ifc4x3_add2_elements.json"))
PTYPES = {n: p for d, n, a, p in TREE}
PSETS = json.load(open(ROOT / "tools/ifc4x3_psets.json"))
LIB = "library/templates"
S = {"low": {"min_scale": 200}, "medium": {"min_scale": 50, "max_scale": 200}, "high": {"max_scale": 50}}

def r9(x): return round(x, 9) + 0.0

def dump(obj):
    s = json.dumps(obj, indent=2, ensure_ascii=False)
    num = r"-?\d+(?:\.\d+)?(?:e-?\d+)?"
    s = re.sub(r"\[\s+(" + num + r"(?:,\s+" + num + r")*)\s+\]",
               lambda m: "[" + ", ".join(x.strip() for x in m.group(1).split(",")) + "]", s)
    s = re.sub(r"\[\s+((?:\[[^\[\]]*\],?\s*)+)\]",
               lambda m: "[" + ", ".join(p.strip().rstrip(",") for p in re.findall(r"\[[^\[\]]*\]", m.group(1))) + "]", s)
    return s + "\n"

def L(metric, imperial): return {"metric": metric, "imperial": imperial}

# ====================================================================== template builder
class Template:
    def __init__(self, cls, archetype, name, description, default_type):
        self.cls, self.archetype, self.name, self.description = cls, archetype, name, description
        self.base = f"{LIB}/{cls}"
        self.P, self.D, self.C, self.R, self.REPS, self.slots, self.ports = [], [], [], [], [], [], []
        self.host, self.handles, self.ifc_props, self.quantities = {}, [], {}, {}
        self.material_ids, self.slots_mat = set(), {}
        self.layers_files, self.references, self.extra_ifc = {}, [], {}
        types = PTYPES[cls] or []
        self.par("predefined_type", "choice", default_type, "Predefined type", "IFC",
                 options=types + ["USERDEFINED", "NOTDEFINED"],
                 description=f"IFC 4.3 {cls}TypeEnum. Property sets that apply only to some types follow this choice.")
        self.par("object_type", "text", "", "Object type (user-defined)", "IFC", visible='predefined_type = "USERDEFINED"')

    # --- builders
    def par(self, name, type_, default, label, group, **kw):
        d = {"name": name, "type": type_, "default": default, "label": label, "group": group}; d.update(kw); self.P.append(d)
    def dv(self, name, expr, note=None):
        d = {"name": name, "expr": expr}
        if note: d["note"] = note
        self.D.append(d)
    def check(self, id_, expr, severity, message): self.C.append({"id": id_, "expr": expr, "severity": severity, "message": message})
    def step(self, id_, op, args, plane=None, when=None, note=None):
        d = {"id": id_, "op": op}
        if plane: d["plane"] = plane
        if when: d["when"] = when
        d["args"] = args
        if note: d["note"] = note
        self.R.append(d)
    def rep(self, id_, context, lod, items, source="authored", **kw):
        ifc = {"model": ("Body", "MODEL_VIEW"), "plan": ("Plan", "PLAN_VIEW"), "elevation": ("Profile", "ELEVATION_VIEW"),
               "section": ("Profile", "SECTION_VIEW"), "axis": ("Axis", "GRAPH_VIEW"), "rcp": ("Plan", "REFLECTED_PLAN_VIEW")}[context]
        d = {"id": id_, "context": context, "lod": lod}
        if lod in S: d["scale"] = S[lod]
        d.update({"source": source, "ifc": {"context": ifc[0], "targetView": ifc[1]}})
        if items is not None: d["items"] = items
        d.update(kw); self.REPS.append(d)
    def material_slot(self, name, label, default):
        self.material_ids.add(default)
        self.par(name, "material", default, label, "Materials", options="materials")

    # --- IFC property sets → parameters
    def add_psets(self, overrides=None, qto_map=None):
        overrides = overrides or {}
        for ps in PSETS.get(self.cls, []):
            if ps["kind"] == "qto":
                q = {}; geom = []
                for p in ps["props"]:
                    if qto_map and p["name"] in qto_map: q[p["name"]] = qto_map[p["name"]]
                    else: geom.append(p["name"])
                self.quantities[ps["name"]] = {"values": q, "from_geometry": geom}
                continue
            props = []
            for p in ps["props"]:
                d = {"name": p["name"], "measure": p["measure"]}
                if p.get("enum"): d["enum"] = p["enum"]
                key = f'{ps["name"]}.{p["name"]}'
                if key in overrides: d["value"] = overrides[key]
                props.append(d)
            par = {"name": ps["name"], "type": "property_set", "default": {}, "label": ps["name"], "group": "IFC data",
                   "properties": props, "optional": bool(ps["generic"])}
            if ps["applies_to"]: par["visible"] = "list_contains(" + json.dumps(ps["applies_to"]) + ", predefined_type)"
            self.P.append(par)

    # --- output
    def type_attributes(self):
        mats, hatches = subset(sorted(self.material_ids | set(self.extra_materials())))
        ifc = {"class": self.cls, "predefinedType": "if predefined_type = \"USERDEFINED\" or predefined_type = \"NOTDEFINED\" then predefined_type else predefined_type",
               "objectType": 'if predefined_type = "USERDEFINED" then object_type else null',
               "property_sets": "all parameters of type property_set, with the values set by `value` formulas",
               "properties": self.ifc_props, "quantities": self.quantities, "parameter_pset": "OPO_Parameters"}
        ifc.update(self.extra_ifc)
        obj = {"id": f"opo-format.org/{self.base}", "name": self.name, "kind": "class_template", "archetype": self.archetype,
               "version": VERSION, "opo": "0.1", "license": "CC0-1.0", "author": "OPO format contributors",
               "description": self.description, "tags": [self.cls, self.archetype, "class template"],
               "references": [{"role": "IFC parameters", "name": f"IFC 4.3 ADD2 {self.cls}, {self.cls}TypeEnum and its property and quantity set templates",
                               "license": "buildingSMART", "uri": f"https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/{self.cls}",
                               "used": "Class, predefined types, property and quantity set names, property names, value types and enumerations (names only)."},
                              {"role": "generator", "name": "tools/gen_templates.py", "used": f"Generated from the `{self.archetype}` archetype (spec/objects/archetypes.md)."}]
               + self.references}
        attrs = {"bsi::ifc::class": {"code": self.cls, "uri": f"https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/{self.cls}"},
                 "bsi::ifc::prop::Name": self.name, "bsi::ifc::prop::TypeName": self.name,
                 "opo::object": obj, "opo::parameters": self.P, "opo::slots": self.slots,
                 "opo::rules": {"derived": self.D, "checks": self.C, "rulesets": getattr(self, "rulesets", [])},
                 "opo::recipe": self.R, "opo::representations": self.REPS, "opo::host": self.host, "opo::handles": self.handles,
                 "opo::materials": mats, "opo::hatches": hatches, "opo::ifc": ifc}
        if self.ports: attrs["opo::ports"] = self.ports
        return attrs

    def extra_materials(self):
        out = set()
        for p in self.P:
            if p["type"] == "layers":
                out |= {l["material"] for l in p["default"]}
        for layer in self.layers_files.values():
            for v in layer.get("variants", []):
                for val in v["values"].values():
                    if isinstance(val, list):
                        out |= {l["material"] for l in val if isinstance(l, dict) and "material" in l}
                    elif isinstance(val, str) and val in MATERIALS:
                        out.add(val)
        return out

    def header(self, rel):
        return {"id": f"opo-format.org/{self.base}/{rel}", "ifcxVersion": "ifcx_alpha", "dataVersion": VERSION,
                "author": "opo-format.org", "timestamp": DATE}

    def write(self):
        tpath = pid(f"{self.base}/type")
        attrs = self.type_attributes()
        doc = {"header": self.header("object.ifcx"), "imports": IMPORTS, "schemas": {}, "data": [{"path": tpath, "attributes": attrs}]}
        # bake: run the recipe for the defaults and store the medium 3D and plan items
        env, geo, T = RX.run(doc, base_dir=ROOT / LIB, resolver=resolver)
        children, nodes = {}, []
        for rid in ("model.medium", "plan.medium"):
            rep = next(r for r in self.REPS if r["id"] == rid)
            for k, it in enumerate(rep.get("items", [])):
                for j, g in enumerate(RX.flat(geo.get(it["geometry"]))):
                    mat = RX.resolve_material(it, env, g)
                    label = f'{rid.split(".")[0].capitalize()}_{it["geometry"]}_{j + 1}'
                    path = pid(f"{self.base}/baked/{rid}/{k}/{j}")
                    a = {"opo::representation": rid}
                    if g["kind"] == "solid":
                        faces = [i for f in g["faces"] for i in f]
                        a["usd::usdgeom::mesh"] = {"points": [[r9(c) for c in p] for p in g["points"]], "faceVertexIndices": faces}
                    else:
                        curves = []
                        for c in (RX.op_outline(None, g) if g["kind"] == "region" else [g] if g["kind"] in ("curve", "curve3") else []):
                            pts = c["points"]
                            pl = c.get("plane", "xy")
                            curves.append([[r9(x) for x in (p if len(p) == 3 else RX.to3(pl, p[0], p[1], 0.0))] for p in pts])
                        if not curves: continue
                        a["usd::usdgeom::basiscurves"] = {"points": [p for c in curves for p in c], "curveVertexCounts": [len(c) for c in curves]}
                        if it.get("class"): a["opo::line_class"] = it["class"]
                    if mat: a["bsi::ifc::material"] = {"code": mat, "uri": ""}
                    children[label] = path
                    nodes.append({"path": path, "attributes": a})
        doc["data"][0]["children"] = children
        doc["data"].extend(nodes)
        out = ROOT / self.base
        (out / "layers").mkdir(parents=True, exist_ok=True)
        for f in (out / "layers").glob("*.ifcx"): f.unlink()
        (out / "object.ifcx").write_text(dump(doc))
        for rel, layer in self.layers_files.items():
            data = []
            sysp = pid(f"{self.base}/{rel}/system")
            data.append({"path": sysp, "inherits": {"type": tpath},
                         "attributes": {"opo::values": layer.get("system_values", {}), "bsi::ifc::prop::Name": layer["name"]}})
            for v in layer["variants"]:
                data.append({"path": pid(f"{self.base}/{rel}/{v['name']}"), "inherits": {"system": sysp},
                             "attributes": {"opo::values": v["values"], "bsi::ifc::prop::TypeName": v["name"],
                                            **({"opo::note": v["note"]} if v.get("note") else {})}})
            (out / rel).write_text(dump({"header": self.header(rel), "imports": IMPORTS, "schemas": {}, "data": data}))
        return doc, env, geo

def resolver(object_id):
    """Map a library object id to its folder (prototype: library objects live in this repo)."""
    prefix = "opo-format.org/"
    return ROOT / object_id[len(prefix):] if object_id.startswith(prefix) else None

# ====================================================================== shared expressions
def polyline_length(name):
    return (f"sum(for i in 1..count({name}) - 1 return sqrt(({name}[i + 1][1] - {name}[i][1]) ** 2 + "
            f"({name}[i + 1][2] - {name}[i][2]) ** 2" + (f" + ({name}[i + 1][3] - {name}[i][3]) ** 2" if name.endswith("3") else "") + "))")
def shoelace(name):
    n = f"count({name})"
    return (f"abs(sum(for i in 1..{n} return {name}[i][1] * {name}[modulo(i, {n}) + 1][2] - "
            f"{name}[modulo(i, {n}) + 1][1] * {name}[i][2])) / 2")
LAYER_START = "for i in 1..count(layers) return sum(sublist(layers.thickness, 1, i)) - layers[i].thickness"
CORE_INDEX = "if count(index_of(layers.core, true)) > 0 then index_of(layers.core, true)[1] else ceiling(count(layers) / 2)"
LAYERS_DESC = ("Layer build-up: list of {material, thickness, function, core}. Each material carries its cut hatch "
               "(opo::materials, opo::hatches), so the type keeps its look when shared.")

def layer(material, thickness, function, core=False):
    d = {"material": material, "thickness": thickness, "function": function}
    if core: d["core"] = True
    return d

# ====================================================================== wall
def wall():
    t = Template("IfcWall", "wall", "Wall (class template)",
                 "Layered wall along a path: build-up of materials with hatches, location line, base and top constraints. Hosts doors, windows and openings.",
                 "STANDARD")
    t.slots.append({"name": "path", "type": "polyline", "plane": "xy", "default": [[0.0, 0.0], [5.0, 0.0]],
                    "rules": {"open": True, "min_segment_length": 0.01},
                    "description": "Wall path in plan. Layers are listed from the left of the direction of travel to the right."})
    t.par("layers", "layers", [layer("plaster", 0.015, "finish"), layer("concrete_block", 0.2, "structure", True), layer("plaster", 0.015, "finish")],
          "Layers (left to right)", "Construction", description=LAYERS_DESC, limits={"thickness": {"min": 0.001, "max": 2.0}})
    t.par("location_line", "choice", "wall_centre", "Location line", "Construction",
          options=["wall_centre", "core_centre", "finish_left", "finish_right", "core_left", "core_right"],
          description="Which line of the build-up sits on the path.")
    t.par("top_mode", "choice", "storey", "Top constraint", "Height", options=["storey", "unconnected"],
          option_labels={"storey": "Up to the next storey (+ top offset)", "unconnected": "Unconnected height"})
    t.par("unconnected_height", "length", 2.7, "Unconnected height", "Height", visible='top_mode = "unconnected"', limits={"min": 0.05, "max": 50})
    t.par("base_offset", "length", 0.0, "Base offset", "Height", limits={"min": -10, "max": 10})
    t.par("top_offset", "length", 0.0, "Top offset", "Height", visible='top_mode = "storey"', limits={"min": -10, "max": 10})
    t.par("load_bearing", "boolean", False, "Load bearing", "Data")
    t.par("is_external", "boolean", False, "External", "Data")
    t.dv("total_thickness", "sum(layers.thickness)")
    t.dv("layer_start", LAYER_START, "Distance of each layer's left face from the wall's left face.")
    t.dv("core_index", CORE_INDEX, "First layer marked core, else the middle layer.")
    t.dv("core_start", "layer_start[core_index]")
    t.dv("core_end", "core_start + layers[core_index].thickness")
    t.dv("left_face", 'if location_line = "wall_centre" then total_thickness / 2 else if location_line = "core_centre" then (core_start + core_end) / 2 '
         'else if location_line = "finish_left" then 0 else if location_line = "finish_right" then total_thickness '
         'else if location_line = "core_left" then core_start else core_end',
         "Offset of the left face from the path (positive = left).")
    t.dv("height", 'if top_mode = "storey" then level.height + top_offset - base_offset else unconnected_height')
    t.dv("bottom", "base_offset")
    t.dv("top", "base_offset + height")
    t.dv("path_length", polyline_length("path"))
    t.check("has_layers", "count(layers) >= 1", "error", "A wall needs at least one layer.")
    t.check("layer_thickness", "min(layers.thickness) > 0", "error", "Every layer needs a thickness above zero.")
    t.check("height_positive", "height > 0", "error", "The wall top is below its base.")
    t.step("layer_bands", "for_each", {"items": "layers", "as": "layer", "index": "i",
                                       "do": "band(path, left_face - layer_start[i], left_face - layer_start[i] - layer.thickness)"}, "xy")
    t.step("layer_solids", "for_each", {"items": "layer_bands", "as": "b", "index": "i", "do": "extrude(b, bottom, top)"}, "xy",
           note="Each item keeps its layer (each.material) from layer_bands.")
    t.step("outline", "band", {"path": "path", "left": "left_face", "right": "left_face - total_thickness"}, "xy")
    t.step("body", "extrude", {"profile": "outline", "from": "bottom", "to": "top"}, "xy")
    t.step("axis", "polyline", {"points": "path"}, "xy")
    core_mat = "layers[core_index].material"
    t.rep("model.low", "model", "low", [{"geometry": "body", "material": core_mat}])
    t.rep("model.medium", "model", "medium", [{"geometry": "layer_solids", "material": "each.material", "part": "Layer"}])
    t.rep("model.high", "model", "high", [{"geometry": "layer_solids", "material": "each.material", "part": "Layer"}])
    t.rep("plan.low", "plan", "low", [{"geometry": "outline", "class": "cut", "hatch": core_mat, "role": "outline"}],
          note="Whole wall in one outline, hatched with the core material.")
    t.rep("plan.medium", "plan", "medium", [{"geometry": "layer_bands", "class": "cut", "hatch": "each.material", "role": "layer"},
                                            {"geometry": "outline", "class": "cut", "role": "outline"}],
          note="Each layer hatched with its material's cut hatch; layer lines thin, outline heavy (weights from the drawing style).")
    t.rep("plan.high", "plan", "high", None, source="derived", derive={"from": "model.high", "method": "cut"},
          note="Cut from the layer solids; hatches from each layer's material.")
    t.rep("elevation", "elevation", "all", None, source="derived", derive={"from": "model.{lod}", "method": "project"},
          surface="each layer's material surface pattern on visible faces (e.g. brick coursing)")
    t.rep("section", "section", "all", None, source="derived", derive={"from": "model.{lod}", "method": "cut"})
    t.rep("axis", "axis", "all", [{"geometry": "axis", "class": "annotation"}])
    t.host = {"is_host": True, "accepts": ["IfcDoor", "IfcWindow", "IfcOpeningElement", "IfcVoidingFeature", "IfcProjectionElement", "IfcShadingDevice"],
              "provides": {"thickness": "total_thickness", "y_max": "left_face", "y_min": "left_face - total_thickness",
                           "bottom": "bottom", "top": "top"},
              "joins": {"by": "material", "rule": "Where walls meet, layers of the same material join without a line; core joins core, finishes wrap. Done by the application."},
              "level": "Placed on a storey; z = 0 is the storey elevation."}
    t.handles = [{"slot": "path", "kind": "points", "view": ["plan"]},
                 {"parameter": "unconnected_height", "view": ["elevation", "model"], "at": "[path[1][1], path[1][2], top]", "axis": "z", "visible": 'top_mode = "unconnected"'}]
    t.ifc_props = {"Pset_WallCommon.LoadBearing": "load_bearing", "Pset_WallCommon.IsExternal": "is_external"}
    t.extra_ifc = {"material_layer_set": {"layers": "layers", "LayerSetDirection": '"AXIS2"', "DirectionSense": '"NEGATIVE"',
                                          "OffsetFromReferenceLine": "left_face", "note": "First layer = left of the path; IfcMaterialLayer.Material from each layer's material."}}
    t.add_psets({"Pset_WallCommon.LoadBearing": "load_bearing", "Pset_WallCommon.IsExternal": "is_external"},
                {"Length": "path_length", "Width": "total_thickness", "Height": "height"})
    t.quantity_note = "Footprint, side areas and volumes come from the body geometry: with corners and an off-centre location line, path length × thickness is not exact."
    t.layers_files["layers/types-examples.ifcx"] = {"name": "Example wall types (illustrative build-ups, not norm values)", "variants": [
        {"name": "Concrete 200", "values": {"layers": [layer("reinforced_concrete", 0.2, "structure", True)], "load_bearing": True}},
        {"name": "Masonry 175, plastered both sides", "values": {"layers": [layer("plaster", 0.015, "finish"), layer("brick_masonry", 0.175, "structure", True), layer("plaster", 0.015, "finish")]}},
        {"name": "Partition, metal stud 75, 2 × 12.5 board each side", "values": {"layers": [
            layer("plasterboard", 0.0125, "finish"), layer("plasterboard", 0.0125, "finish"), layer("mineral_wool", 0.075, "insulation", True),
            layer("plasterboard", 0.0125, "finish"), layer("plasterboard", 0.0125, "finish")]},
         "note": "Studs are not modelled; the stud zone is drawn as its insulation."},
        {"name": "External, concrete 200 + 120 insulation and render", "values": {"layers": [
            layer("render", 0.01, "finish"), layer("rigid_insulation", 0.12, "insulation"), layer("reinforced_concrete", 0.2, "structure", True),
            layer("plaster", 0.015, "finish")], "is_external": True, "load_bearing": True, "location_line": "core_centre"}},
        {"name": "External cavity wall, brick / insulation / block", "values": {"layers": [
            layer("brick_masonry", 0.1025, "finish"), layer("mineral_wool", 0.1, "insulation"), layer("concrete_block", 0.1, "structure", True),
            layer("plaster", 0.013, "finish")], "is_external": True, "load_bearing": True}},
    ]}
    return t

# ====================================================================== slab
def slab():
    t = Template("IfcSlab", "area", "Slab (class template)",
                 "Layered slab from a boundary with holes: build-up from the top down with materials and hatches, reference face, offset from the storey.",
                 "FLOOR")
    t.slots.append({"name": "boundary", "type": "polygon", "plane": "xy", "default": [[0.0, 0.0], [6.0, 0.0], [6.0, 4.0], [0.0, 4.0]],
                    "rules": {"closed": True, "non_self_intersecting": True}})
    t.slots.append({"name": "holes", "type": "polygon_list", "plane": "xy", "default": [], "rules": {"inside": "boundary"}})
    t.par("layers", "layers", [layer("cement_screed", 0.06, "finish"), layer("rigid_insulation", 0.03, "insulation"), layer("reinforced_concrete", 0.2, "structure", True)],
          "Layers (top to bottom)", "Construction", description=LAYERS_DESC, limits={"thickness": {"min": 0.001, "max": 3.0}})
    t.par("reference", "choice", "top", "Reference face at the offset", "Construction", options=["top", "core_top", "bottom"])
    t.par("elevation_offset", "length", 0.0, "Offset from storey", "Construction", limits={"min": -20, "max": 20})
    t.par("load_bearing", "boolean", True, "Load bearing", "Data")
    t.par("is_external", "boolean", False, "External", "Data")
    t.dv("total_thickness", "sum(layers.thickness)")
    t.dv("layer_start", LAYER_START, "Depth of each layer's top face below the slab top.")
    t.dv("core_index", CORE_INDEX)
    t.dv("top_z", 'if reference = "top" then elevation_offset else if reference = "core_top" then elevation_offset + layer_start[core_index] else elevation_offset + total_thickness')
    t.dv("bottom_z", "top_z - total_thickness")
    t.dv("gross_area", shoelace("boundary"))
    t.dv("holes_area", "sum(append(for h in holes return " + shoelace("h") + ", 0))")
    t.dv("net_area", "gross_area - holes_area")
    t.dv("perimeter", polyline_length("append(boundary, boundary[1])").replace("append(boundary, boundary[1])", "closed_boundary"))
    t.dv("closed_boundary", "append(boundary, boundary[1])")
    t.D.insert(len(t.D) - 2, t.D.pop())  # closed_boundary before perimeter
    t.check("has_layers", "count(layers) >= 1", "error", "A slab needs at least one layer.")
    t.check("layer_thickness", "min(layers.thickness) > 0", "error", "Every layer needs a thickness above zero.")
    t.check("boundary_points", "count(boundary) >= 3", "error", "The boundary needs at least three points.")
    t.step("region", "difference", {"a": "polygon(boundary)", "b": "for h in holes return polygon(h)"}, "xy")
    t.step("layer_solids", "for_each", {"items": "layers", "as": "layer", "index": "i",
                                        "do": "extrude(region, top_z - layer_start[i] - layer.thickness, top_z - layer_start[i])"}, "xy")
    t.step("body", "extrude", {"profile": "region", "from": "bottom_z", "to": "top_z"}, "xy")
    t.step("edges", "boundary_curves", {"region": "region"}, "xy")
    core_mat = "layers[core_index].material"
    t.rep("model.low", "model", "low", [{"geometry": "body", "material": core_mat}])
    t.rep("model.medium", "model", "medium", [{"geometry": "layer_solids", "material": "each.material", "part": "Layer"}])
    t.rep("model.high", "model", "high", [{"geometry": "layer_solids", "material": "each.material", "part": "Layer"}])
    t.rep("plan.low", "plan", "low", [{"geometry": "edges", "class": "projected"}])
    t.rep("plan.medium", "plan", "medium", [{"geometry": "edges", "class": "projected"}],
          note="A floor slab lies below the plan cut: its edges and holes are drawn as projected lines. Cut slabs (e.g. in a section or a split-level plan) take the derived cut with layer hatches.")
    t.rep("plan.high", "plan", "high", [{"geometry": "edges", "class": "projected"}])
    t.rep("section", "section", "all", None, source="derived", derive={"from": "model.{lod}", "method": "cut"},
          note="Each cut layer hatched with its material's cut hatch.")
    t.host = {"is_host": True, "accepts": ["IfcOpeningElement", "IfcVoidingFeature", "IfcStair", "IfcRamp"],
              "provides": {"thickness": "total_thickness", "top": "top_z", "bottom": "bottom_z"},
              "joins": {"by": "material", "rule": "Layers of the same material join with walls and other slabs without a line."},
              "level": "Placed on a storey; z = 0 is the storey elevation."}
    t.handles = [{"slot": "boundary", "kind": "points", "view": ["plan"]}, {"slot": "holes", "kind": "points", "view": ["plan"]}]
    t.ifc_props = {"Pset_SlabCommon.LoadBearing": "load_bearing", "Pset_SlabCommon.IsExternal": "is_external"}
    t.extra_ifc = {"material_layer_set": {"layers": "layers", "LayerSetDirection": '"AXIS3"', "DirectionSense": '"NEGATIVE"',
                                          "OffsetFromReferenceLine": "top_z", "note": "First layer = top."}}
    t.add_psets({"Pset_SlabCommon.LoadBearing": "load_bearing", "Pset_SlabCommon.IsExternal": "is_external"},
                {"Width": "total_thickness", "Depth": "total_thickness", "Perimeter": "perimeter", "GrossArea": "gross_area",
                 "NetArea": "net_area", "GrossVolume": "gross_area * total_thickness", "NetVolume": "net_area * total_thickness"})
    t.layers_files["layers/types-examples.ifcx"] = {"name": "Example slab types (illustrative build-ups, not norm values)", "variants": [
        {"name": "Concrete 200", "values": {"layers": [layer("reinforced_concrete", 0.2, "structure", True)]}},
        {"name": "Floor, tiles on screed, insulation, concrete 250", "values": {"layers": [
            layer("ceramic_tile", 0.01, "finish"), layer("cement_screed", 0.065, "finish"), layer("rigid_insulation", 0.03, "insulation"),
            layer("reinforced_concrete", 0.25, "structure", True), layer("plaster", 0.01, "finish")]}},
        {"name": "Timber floor, boards 22 on structure 200", "values": {"layers": [
            layer("timber", 0.022, "finish"), layer("timber", 0.2, "structure", True), layer("plasterboard", 0.0125, "finish")]},
         "note": "Joists are not modelled; the joist zone is one timber layer."},
    ]}
    return t

# ====================================================================== linear (beam, member)
PROFILE_KINDS = ["rectangle", "i_section", "circle", "rect_hollow", "circ_hollow", "channel", "angle"]
def linear(cls, name, default_type, defaults, material, extra_types_note=""):
    t = Template(cls, "linear", name,
                 "Member with a profile swept along a path: parametric profile (rectangle, I, circle, hollow sections, channel, angle), justification, roll and end extensions.",
                 default_type)
    t.slots.append({"name": "path", "type": "polyline3", "default": defaults["path"], "rules": {"open": True, "min_segment_length": 0.01},
                    "description": "Axis of the member (the justification point of the profile follows it)."})
    t.par("profile_kind", "choice", defaults["kind"], "Profile", "Profile", options=PROFILE_KINDS,
          option_labels={"rectangle": "Rectangle", "i_section": "I / H section", "circle": "Circle", "rect_hollow": "Rectangular hollow",
                         "circ_hollow": "Circular hollow", "channel": "Channel (U)", "angle": "Angle (L)"},
          description="Profiles from the shared profile library set these values by variant.")
    t.par("profile_name", "text", "", "Profile designation", "Profile", description="E.g. IPE 270; written to IFC ProfileName.")
    t.par("width", "length", defaults["width"], "Width / diameter", "Profile", limits={"min": 0.005, "max": 5})
    t.par("depth", "length", defaults["depth"], "Depth", "Profile", visible='profile_kind != "circle" and profile_kind != "circ_hollow"', limits={"min": 0.005, "max": 5})
    t.par("web_thickness", "length", 0.008, "Web thickness", "Profile", visible='profile_kind = "i_section" or profile_kind = "channel"', limits={"min": 0.001, "max": 0.2})
    t.par("flange_thickness", "length", 0.012, "Flange thickness", "Profile", visible='profile_kind = "i_section" or profile_kind = "channel"', limits={"min": 0.001, "max": 0.2})
    t.par("wall_thickness", "length", defaults.get("wall", 0.006), "Wall / leg thickness", "Profile",
          visible='profile_kind = "rect_hollow" or profile_kind = "circ_hollow" or profile_kind = "angle"', limits={"min": 0.001, "max": 0.2})
    t.par("justification_h", "choice", "centre", "Horizontal justification", "Placement", options=["left", "centre", "right"])
    t.par("justification_v", "choice", defaults.get("jv", "centre"), "Vertical justification", "Placement", options=["top", "centre", "bottom"])
    t.par("roll", "angle", 0.0, "Rotation about the axis", "Placement", limits={"min": -180, "max": 180})
    t.par("start_extension", "length", 0.0, "Start extension", "Placement", limits={"min": -2, "max": 2})
    t.par("end_extension", "length", 0.0, "End extension", "Placement", limits={"min": -2, "max": 2})
    t.material_slot("material", "Material", material)
    t.par("load_bearing", "boolean", defaults.get("load_bearing", True), "Load bearing", "Data")
    t.dv("cu", 'if justification_h = "left" then -width / 2 else if justification_h = "right" then width / 2 else 0', "Profile centre, across.")
    t.dv("profile_height", 'if profile_kind = "circle" or profile_kind = "circ_hollow" then width else depth')
    t.dv("cv", 'if justification_v = "top" then -profile_height / 2 else if justification_v = "bottom" then profile_height / 2 else 0', "Profile centre, up.")
    t.dv("seg_start", "[path[2][1] - path[1][1], path[2][2] - path[1][2], path[2][3] - path[1][3]]")
    t.dv("seg_end", "[path[count(path)][1] - path[count(path) - 1][1], path[count(path)][2] - path[count(path) - 1][2], path[count(path)][3] - path[count(path) - 1][3]]")
    t.dv("len_start", "sqrt(seg_start[1] ** 2 + seg_start[2] ** 2 + seg_start[3] ** 2)")
    t.dv("len_end", "sqrt(seg_end[1] ** 2 + seg_end[2] ** 2 + seg_end[3] ** 2)")
    t.dv("p_start", "for k in 1..3 return path[1][k] - seg_start[k] / len_start * start_extension")
    t.dv("p_end", "for k in 1..3 return path[count(path)][k] + seg_end[k] / len_end * end_extension")
    t.dv("axis_path", "concatenate([p_start], sublist(path, 2, count(path) - 2), [p_end])", "Axis with the end extensions applied.")
    t.dv("length", polyline_length("axis_path3").replace("axis_path3", "axis_path"))
    t.dv("plan_path", "for p in axis_path return [p[1], p[2]]")
    t.dv("area", 'if profile_kind = "rectangle" then width * depth '
         'else if profile_kind = "i_section" then 2 * width * flange_thickness + (depth - 2 * flange_thickness) * web_thickness '
         'else if profile_kind = "circle" then 3.141592653589793 * (width / 2) ** 2 '
         'else if profile_kind = "rect_hollow" then width * depth - (width - 2 * wall_thickness) * (depth - 2 * wall_thickness) '
         'else if profile_kind = "circ_hollow" then 3.141592653589793 * ((width / 2) ** 2 - (width / 2 - wall_thickness) ** 2) '
         'else if profile_kind = "channel" then 2 * width * flange_thickness + (depth - 2 * flange_thickness) * web_thickness '
         'else (width + depth - wall_thickness) * wall_thickness', "Cross-section area (fillets ignored).")
    t.check("path_points", "count(path) >= 2", "error", "The path needs at least two points.")
    t.check("walls_fit", 'not((profile_kind = "rect_hollow" or profile_kind = "circ_hollow") and 2 * wall_thickness >= min(width, profile_height))',
            "error", "The wall thickness is too large for the profile.")
    t.check("flanges_fit", 'not((profile_kind = "i_section" or profile_kind = "channel") and (2 * flange_thickness >= depth or web_thickness >= width))',
            "error", "Flanges or web do not fit in the profile.")
    rect = lambda u0, v0, u1, v1: f"rectangle([cu + {u0}, cv + {v0}], [cu + {u1}, cv + {v1}])"
    prof = ('if profile_kind = "rectangle" then ' + rect("-width / 2", "-depth / 2", "width / 2", "depth / 2") +
            ' else if profile_kind = "i_section" then union([' + rect("-width / 2", "depth / 2 - flange_thickness", "width / 2", "depth / 2") + ", " +
            rect("-width / 2", "-depth / 2", "width / 2", "-depth / 2 + flange_thickness") + ", " +
            rect("-web_thickness / 2", "-depth / 2", "web_thickness / 2", "depth / 2") + "])"
            ' else if profile_kind = "circle" then circle([cu, cv], width / 2)'
            ' else if profile_kind = "rect_hollow" then difference(' + rect("-width / 2", "-depth / 2", "width / 2", "depth / 2") + ", " +
            rect("-width / 2 + wall_thickness", "-depth / 2 + wall_thickness", "width / 2 - wall_thickness", "depth / 2 - wall_thickness") + ")"
            ' else if profile_kind = "circ_hollow" then difference(circle([cu, cv], width / 2), circle([cu, cv], width / 2 - wall_thickness))'
            ' else if profile_kind = "channel" then union([' + rect("-width / 2", "depth / 2 - flange_thickness", "width / 2", "depth / 2") + ", " +
            rect("-width / 2", "-depth / 2", "width / 2", "-depth / 2 + flange_thickness") + ", " +
            rect("-width / 2", "-depth / 2", "-width / 2 + web_thickness", "depth / 2") + "])"
            ' else union([' + rect("-width / 2", "-depth / 2", "-width / 2 + wall_thickness", "depth / 2") + ", " +
            rect("-width / 2", "-depth / 2", "width / 2", "-depth / 2 + wall_thickness") + "])")
    t.step("profile", "union", {"items": f"[{prof}]"}, "profile", note="Profile in its own plane: u across (left of travel), v up.")
    t.step("body", "sweep", {"profile": "profile", "path": "axis_path", "roll": "roll"})
    t.step("axis", "path3", {"points": "axis_path"})
    t.step("plan_band", "band", {"path": "plan_path", "left": "cu + width / 2", "right": "cu - width / 2"}, "xy")
    t.step("plan_axis", "polyline", {"points": "plan_path"}, "xy")
    plan_class = defaults.get("plan_class", "overhead")
    t.rep("model.low", "model", "low", [{"geometry": "body", "material": "material"}])
    t.rep("model.medium", "model", "medium", [{"geometry": "body", "material": "material"}])
    t.rep("model.high", "model", "high", [{"geometry": "body", "material": "material"}])
    t.rep("plan.low", "plan", "low", [{"geometry": "plan_axis", "class": plan_class}])
    t.rep("plan.medium", "plan", "medium", [{"geometry": "plan_band", "class": plan_class}],
          note=f"Drawn as {plan_class} outline (members above the plan cut). Where the member is cut by the plan (columns), the derived cut applies.")
    t.rep("plan.high", "plan", "high", None, source="derived", derive={"from": "model.high", "method": "cut_or_project"})
    t.rep("section", "section", "all", None, source="derived", derive={"from": "model.{lod}", "method": "cut"})
    t.rep("axis", "axis", "all", [{"geometry": "axis", "class": "annotation"}])
    t.host = {"is_host": False, "level": "Placed on a storey; path z relative to the storey elevation."}
    t.handles = [{"slot": "path", "kind": "points", "view": ["plan", "model"]}]
    t.extra_ifc = {"profile_def": {
        "rectangle": {"entity": "IfcRectangleProfileDef", "XDim": "width", "YDim": "depth"},
        "i_section": {"entity": "IfcIShapeProfileDef", "OverallWidth": "width", "OverallDepth": "depth", "WebThickness": "web_thickness", "FlangeThickness": "flange_thickness"},
        "circle": {"entity": "IfcCircleProfileDef", "Radius": "width / 2"},
        "rect_hollow": {"entity": "IfcRectangleHollowProfileDef", "XDim": "width", "YDim": "depth", "WallThickness": "wall_thickness"},
        "circ_hollow": {"entity": "IfcCircleHollowProfileDef", "Radius": "width / 2", "WallThickness": "wall_thickness"},
        "channel": {"entity": "IfcUShapeProfileDef", "Depth": "depth", "FlangeWidth": "width", "WebThickness": "web_thickness", "FlangeThickness": "flange_thickness"},
        "angle": {"entity": "IfcLShapeProfileDef", "Depth": "depth", "Width": "width", "Thickness": "wall_thickness"},
        "select": "profile_kind", "ProfileName": "profile_name", "ProfileType": '"AREA"'},
        "body": "IfcExtrudedAreaSolid per straight segment along the axis (IfcFixedReferenceSweptAreaSolid for curved axes)"}
    common = f"Pset_{cls[3:]}Common"
    t.ifc_props = {f"{common}.LoadBearing": "load_bearing"}
    density = "if material = \"steel\" then 7850 else if material = \"reinforced_concrete\" then 2500 else if material = \"concrete\" then 2400 else null"
    t.dv("density", density, "From the material (null if the material has no density).")
    t.add_psets({f"{common}.LoadBearing": "load_bearing"},
                {"Length": "length", "CrossSectionArea": "area", "GrossVolume": "area * length", "NetVolume": "area * length",
                 "GrossWeight": "if density = null then null else area * length * density"})
    return t

def beam():
    t = linear("IfcBeam", "Beam (class template)", "BEAM",
               {"path": [[0.0, 0.0, 0.0], [5.0, 0.0, 0.0]], "kind": "rectangle", "width": 0.25, "depth": 0.5, "jv": "top"}, "reinforced_concrete")
    t.layers_files["layers/profiles-examples.ifcx"] = {"name": "Example profiles (values per row: see note)", "variants": [
        {"name": "IPE 270", "values": {"profile_kind": "i_section", "profile_name": "IPE 270", "width": 0.135, "depth": 0.27,
                                       "web_thickness": 0.0066, "flange_thickness": 0.0102, "material": "steel"},
         "note": "EN 10365:2017 table values (h 270, b 135, s 6.6, t 10.2 mm); root fillet not modelled. Full EN 10365 / AISC catalogue: to collect."},
        {"name": "Concrete 250 × 500", "values": {"profile_kind": "rectangle", "width": 0.25, "depth": 0.5, "material": "reinforced_concrete"},
         "note": "Generic size, not a norm."},
        {"name": "Glulam 140 × 400", "values": {"profile_kind": "rectangle", "width": 0.14, "depth": 0.4, "material": "timber"},
         "note": "Generic size; EN 14080 sizes to collect."},
    ]}
    return t

def member():
    return linear("IfcMember", "Member (class template)", "MEMBER",
                  {"path": [[0.0, 0.0, 0.0], [3.0, 0.0, 0.0]], "kind": "rect_hollow", "width": 0.1, "depth": 0.1, "wall": 0.005}, "steel")

# ====================================================================== point (boiler)
def boiler():
    t = Template("IfcBoiler", "point", "Boiler (class template)",
                 "Boiler as a cased body with its pipe and flue connections, wall-hung or floor-standing, with a service clearance zone.",
                 "WATER")
    t.par("mount", "choice", "wall", "Mounting", "Placement", options=["wall", "floor"])
    t.par("width", "length", 0.45, "Width", "Size", limits={"min": 0.1, "max": 5}, description="Typical wall-hung size; replace with maker data.")
    t.par("depth", "length", 0.35, "Depth", "Size", limits={"min": 0.1, "max": 5})
    t.par("height", "length", 0.75, "Height", "Size", limits={"min": 0.1, "max": 5})
    t.par("mount_height", "length", 1.2, "Underside above floor", "Placement", visible='mount = "wall"', limits={"min": 0, "max": 5})
    t.par("clearance_front", "length", 0.6, "Service clearance, front", "Clearance", limits={"min": 0, "max": 3}, description="Project or maker value.")
    t.par("clearance_side", "length", 0.05, "Service clearance, sides", "Clearance", limits={"min": 0, "max": 1})
    t.par("pipe_size", "length", 0.022, "Water connection outside diameter", "Connections", limits={"min": 0.008, "max": 0.3})
    t.par("gas_size", "length", 0.015, "Gas connection outside diameter", "Connections", limits={"min": 0.008, "max": 0.2})
    t.par("flue_size", "length", 0.1, "Flue diameter", "Connections", limits={"min": 0.04, "max": 0.6})
    t.par("symbol_code", "text", "BLR", "Plan symbol code", "Drawing")
    t.dv("bottom", 'if mount = "wall" then mount_height else 0')
    t.dv("top", "bottom + height")
    t.dv("port_x", "[-width / 2 + 0.07, -width / 2 + 0.15, width / 2 - 0.15]", "Pipe connections along the underside (flow, return, gas). Typical layout.")
    t.check("ports_fit", "width >= 0.3", "warning", "The body is narrower than the default connection layout; set port positions from maker data.")
    t.step("body", "box", {"min": "[-width / 2, 0, bottom]", "max": "[width / 2, depth, top]"})
    t.step("stubs", "union", {"items": "[cylinder([port_x[1], depth / 2, bottom], [port_x[1], depth / 2, bottom - 0.05], pipe_size / 2), "
                                       "cylinder([port_x[2], depth / 2, bottom], [port_x[2], depth / 2, bottom - 0.05], pipe_size / 2), "
                                       "cylinder([port_x[3], depth / 2, bottom], [port_x[3], depth / 2, bottom - 0.05], gas_size / 2), "
                                       "cylinder([0, depth / 2, top], [0, depth / 2, top + 0.1], flue_size / 2)]"})
    t.step("plan_body", "rectangle", {"min": "[-width / 2, 0]", "max": "[width / 2, depth]"}, "xy")
    t.step("plan_clearance", "rectangle", {"min": "[-width / 2 - clearance_side, depth]", "max": "[width / 2 + clearance_side, depth + clearance_front]"}, "xy")
    t.step("plan_code", "text", {"at": "[0, depth / 2]", "value": "symbol_code", "height": "0.0025"}, "xy")
    t.rep("model.low", "model", "low", [{"geometry": "body", "material": "casing_material"}])
    t.rep("model.medium", "model", "medium", [{"geometry": "body", "material": "casing_material"}])
    t.rep("model.high", "model", "high", [{"geometry": "body", "material": "casing_material"}, {"geometry": "stubs", "material": "\"copper\"", "part": "Connections"}])
    t.rep("plan.low", "plan", "low", [{"geometry": "plan_body", "class": "projected"}, {"geometry": "plan_code", "class": "annotation"}])
    t.rep("plan.medium", "plan", "medium", [{"geometry": "plan_body", "class": "projected"}, {"geometry": "plan_clearance", "class": "annotation", "role": "clearance"},
                                            {"geometry": "plan_code", "class": "annotation"}])
    t.rep("plan.high", "plan", "high", None, source="derived", derive={"from": "model.high", "method": "project"},
          overlay=[{"geometry": "plan_clearance", "class": "annotation", "role": "clearance"}])
    t.rep("elevation", "elevation", "all", None, source="derived", derive={"from": "model.{lod}", "method": "project"})
    t.rep("section", "section", "all", None, source="derived", derive={"from": "model.{lod}", "method": "cut"})
    t.material_slot("casing_material", "Casing", "sheet_metal")
    t.material_ids.add("copper")
    t.host = {"is_host": False, "mounting": {"wall": "on_face: back of the body on the wall face", "floor": "free: on the floor"},
              "insertion": {"point": "[0, 0, 0]", "description": "Centre of the back edge at floor level; y points away from the wall."},
              "clearance": "plan_clearance (annotation zone, used for clash checks; not exported as geometry)"}
    t.ports = [
        {"name": "heating_flow", "system_type": "HEATING", "flow_direction": "SOURCE", "port_type": "PIPE", "nominal_size": "pipe_size",
         "position": "[port_x[1], depth / 2, bottom - 0.05]", "direction": "[0, 0, -1]"},
        {"name": "heating_return", "system_type": "HEATING", "flow_direction": "SINK", "port_type": "PIPE", "nominal_size": "pipe_size",
         "position": "[port_x[2], depth / 2, bottom - 0.05]", "direction": "[0, 0, -1]"},
        {"name": "gas", "system_type": "GAS", "flow_direction": "SINK", "port_type": "PIPE", "nominal_size": "gas_size",
         "position": "[port_x[3], depth / 2, bottom - 0.05]", "direction": "[0, 0, -1]"},
        {"name": "flue", "system_type": "EXHAUST", "flow_direction": "SOURCE", "port_type": "DUCT", "nominal_size": "flue_size",
         "position": "[0, depth / 2, top + 0.1]", "direction": "[0, 0, 1]"},
    ]
    t.add_psets({}, {})
    return t

# ====================================================================== fitting (pipe fitting)
def pipe_fitting():
    t = Template("IfcPipeFitting", "fitting", "Pipe fitting (class template)",
                 "Pipe fitting whose form follows its predefined type: bend, junction (tee), transition (reducer), connector, cap, entry, exit. Sizes follow the connected pipes.",
                 "BEND")
    t.par("outer_diameter", "length", 0.05, "Outside diameter", "Size", limits={"min": 0.006, "max": 3})
    t.par("wall_thickness", "length", 0.003, "Wall thickness", "Size", limits={"min": 0.0005, "max": 0.1})
    t.par("bend_angle", "angle", 90.0, "Bend angle", "Bend", visible='predefined_type = "BEND"', limits={"min": 1, "max": 180})
    t.par("bend_radius_factor", "number", 1.5, "Bend radius ÷ outside diameter", "Bend", visible='predefined_type = "BEND"', limits={"min": 0.6, "max": 10})
    t.par("branch_diameter", "length", 0.05, "Branch outside diameter", "Junction", visible='predefined_type = "JUNCTION"', limits={"min": 0.006, "max": 3})
    t.par("outer_diameter_2", "length", 0.04, "Outlet outside diameter", "Transition", visible='predefined_type = "TRANSITION"', limits={"min": 0.006, "max": 3})
    t.par("fitting_length", "length", 0.1, "Length", "Size", visible='predefined_type != "BEND" and predefined_type != "JUNCTION"', limits={"min": 0.005, "max": 3})
    t.material_slot("material", "Material", "copper")
    t.dv("r", "outer_diameter / 2")
    t.dv("bend_radius", "bend_radius_factor * outer_diameter")
    t.dv("bend_end", "[bend_radius * sin(bend_angle), bend_radius - bend_radius * cos(bend_angle), 0]")
    t.dv("run_length", "max(3 * outer_diameter, 2 * branch_diameter)")
    t.dv("socket_d", "outer_diameter + 2 * wall_thickness", "Connector body diameter (sleeve over the pipe).")
    t.dv("is_bend", 'predefined_type = "BEND"')
    t.dv("is_junction", 'predefined_type = "JUNCTION"')
    t.dv("is_transition", 'predefined_type = "TRANSITION"')
    t.dv("is_cap", 'predefined_type = "OBSTRUCTION"')
    t.dv("is_straight", 'not(is_bend or is_junction or is_transition or is_cap)', "CONNECTOR, ENTRY, EXIT, USERDEFINED, NOTDEFINED: a straight sleeve.")
    t.dv("length", 'if is_bend then 3.141592653589793 * bend_radius * bend_angle / 180 else if is_junction then run_length else fitting_length')
    t.check("bend_radius_ok", "not(is_bend) or bend_radius > r", "error", "The bend radius must be larger than the pipe radius.")
    t.check("branch_ok", "not(is_junction) or branch_diameter <= outer_diameter", "warning", "A branch larger than the run is unusual; check the sizes.")
    t.step("bend_body", "revolve", {"profile": "circle([0, 0], r)", "center": "[0, bend_radius, 0]", "axis": "[0, 0, 1]", "angle": "bend_angle"}, "yz", when="is_bend")
    t.step("junction_body", "union", {"items": "[cylinder([0, 0, 0], [run_length, 0, 0], r), cylinder([run_length / 2, 0, 0], [run_length / 2, run_length / 2, 0], branch_diameter / 2)]"},
           when="is_junction")
    t.step("transition_body", "revolve", {"profile": "polygon([[0, 0], [fitting_length, 0], [fitting_length, outer_diameter_2 / 2], [0, r]])",
                                          "center": "[0, 0, 0]", "axis": "[1, 0, 0]", "angle": "360"}, "xy", when="is_transition",
           note="Concentric reducer.")
    t.step("cap_body", "cylinder", {"start": "[0, 0, 0]", "end": "[fitting_length, 0, 0]", "radius": "socket_d / 2"}, when="is_cap")
    t.step("sleeve_body", "cylinder", {"start": "[0, 0, 0]", "end": "[fitting_length, 0, 0]", "radius": "socket_d / 2"}, when="is_straight")
    t.step("body", "union", {"items": "[bend_body, junction_body, transition_body, cap_body, sleeve_body]"})
    t.step("bend_axis", "arc", {"center": "[0, bend_radius]", "radius": "bend_radius", "start_angle": "-90", "end_angle": "-90 + bend_angle"}, "xy", when="is_bend")
    t.step("straight_axis", "line", {"start": "[0, 0]", "end": "[length, 0]"}, "xy", when="not(is_bend)")
    t.step("branch_axis", "line", {"start": "[run_length / 2, 0]", "end": "[run_length / 2, run_length / 2]"}, "xy", when="is_junction")
    t.step("single_line", "union", {"items": "[bend_axis, straight_axis, branch_axis]"})
    t.step("plan_bend", "band", {"path": "bend_axis", "left": "r", "right": "-r"}, "xy", when="is_bend")
    t.step("plan_junction", "union", {"items": "[rectangle([0, -r], [run_length, r]), rectangle([run_length / 2 - branch_diameter / 2, 0], [run_length / 2 + branch_diameter / 2, run_length / 2])]"},
           "xy", when="is_junction")
    t.step("plan_transition", "polygon", {"points": "[[0, -r], [fitting_length, -outer_diameter_2 / 2], [fitting_length, outer_diameter_2 / 2], [0, r]]"}, "xy", when="is_transition")
    t.step("plan_straight", "rectangle", {"min": "[0, -socket_d / 2]", "max": "[fitting_length, socket_d / 2]"}, "xy", when="is_cap or is_straight")
    t.step("plan_outline", "union", {"items": "[plan_bend, plan_junction, plan_transition, plan_straight]"}, "xy")
    t.rep("model.low", "model", "low", [{"geometry": "body", "material": "material"}])
    t.rep("model.medium", "model", "medium", [{"geometry": "body", "material": "material"}])
    t.rep("model.high", "model", "high", [{"geometry": "body", "material": "material"}])
    t.rep("plan.low", "plan", "low", [{"geometry": "single_line", "class": "projected"}], note="Single-line drawing at small scales.")
    t.rep("plan.medium", "plan", "medium", [{"geometry": "plan_outline", "class": "projected"}])
    t.rep("plan.high", "plan", "high", [{"geometry": "plan_outline", "class": "projected"}])
    t.rep("section", "section", "all", None, source="derived", derive={"from": "model.{lod}", "method": "cut"})
    t.host = {"is_host": False, "placement": "Snapped to the ends of pipe segments; the application inserts fittings where segments meet.",
              "insertion": {"point": "[0, 0, 0]", "description": "Port 1 (inlet) at the origin, pointing along -x."}}
    t.ports = [
        {"name": "port_1", "system_type": "NOTDEFINED", "flow_direction": "SOURCEANDSINK", "port_type": "PIPE", "nominal_size": "outer_diameter",
         "position": "[0, 0, 0]", "direction": "[-1, 0, 0]"},
        {"name": "port_2", "system_type": "NOTDEFINED", "flow_direction": "SOURCEANDSINK", "port_type": "PIPE",
         "nominal_size": "if is_transition then outer_diameter_2 else outer_diameter", "when": "not(is_cap) and predefined_type != \"ENTRY\" and predefined_type != \"EXIT\"",
         "position": "if is_bend then bend_end else [length, 0, 0]",
         "direction": "if is_bend then [cos(bend_angle), sin(bend_angle), 0] else [1, 0, 0]"},
        {"name": "branch", "system_type": "NOTDEFINED", "flow_direction": "SOURCEANDSINK", "port_type": "PIPE", "nominal_size": "branch_diameter",
         "when": "is_junction", "position": "[run_length / 2, run_length / 2, 0]", "direction": "[0, 1, 0]"},
    ]
    t.add_psets({}, {"Length": "length", "GrossCrossSectionArea": "3.141592653589793 * r ** 2",
                     "NetCrossSectionArea": "3.141592653589793 * (r ** 2 - (r - wall_thickness) ** 2)"})
    t.ports_note = "System type is taken from the connected segments."
    return t

# ====================================================================== hosted (opening)
def opening():
    t = Template("IfcOpeningElement", "hosted", "Opening (class template)",
                 "Opening or recess in a wall or slab, from a width × height rectangle or an edited outline; cuts its host.",
                 "OPENING")
    t.slots.append({"name": "outline", "type": "polygon", "plane": "xz", "default": None, "optional": True,
                    "rules": {"closed": True, "fits_host": True}, "description": "Custom outline in the host plane (custom outline mode)."})
    t.par("outline_mode", "choice", "rectangle", "Shape", "Size", options=["rectangle", "custom"],
          option_labels={"rectangle": "Rectangle (width × height drive)", "custom": "Custom outline (outline drives, width and height read-only)"})
    t.par("width", "length", 1.0, "Width", "Size", visible='outline_mode = "rectangle"', limits={"min": 0.01, "max": 50})
    t.par("height", "length", 1.0, "Height", "Size", visible='outline_mode = "rectangle"', limits={"min": 0.01, "max": 50})
    t.par("sill_height", "length", 0.9, "Bottom above host base", "Placement", limits={"min": -5, "max": 50})
    t.par("host_kind", "choice", "wall", "Host", "Placement", options=["wall", "slab"],
          description="Set by the application from the host; slab openings use the plan plane.")
    t.par("recess_depth", "length", 0.1, "Recess depth", "Size", visible='predefined_type = "RECESS"', limits={"min": 0.001, "max": 5})
    t.par("recess_side", "choice", "front", "Recess from", "Size", visible='predefined_type = "RECESS"', options=["front", "back"])
    t.dv("profile_points", 'if outline_mode = "custom" and outline != null then outline else [[-width / 2, sill_height], [width / 2, sill_height], [width / 2, sill_height + height], [-width / 2, sill_height + height]]')
    t.dv("is_recess", 'predefined_type = "RECESS"')
    t.dv("y_from", 'if is_recess and recess_side = "front" then host.y_max - recess_depth else host.y_min - 0.01')
    t.dv("y_to", 'if is_recess and recess_side = "back" then host.y_min + recess_depth else host.y_max + 0.01')
    t.dv("z_from", 'if is_recess and recess_side = "front" then host.top - recess_depth else host.bottom - 0.01')
    t.dv("z_to", 'if is_recess and recess_side = "back" then host.bottom + recess_depth else host.top + 0.01')
    t.dv("open_width", "max(for p in profile_points return p[1]) - min(for p in profile_points return p[1])")
    t.dv("open_height", "max(for p in profile_points return p[2]) - min(for p in profile_points return p[2])")
    t.dv("depth", "if is_recess then recess_depth else host.thickness")
    t.dv("area", shoelace("profile_points"))
    t.dv("above_cut", "min(for p in profile_points return p[2]) > view.cut_height", "Opening starts above the plan cut: drawn dashed.")
    t.check("outline_given", 'outline_mode = "rectangle" or outline != null', "error", "Custom outline mode needs an outline.")
    t.check("recess_fits", "not(is_recess) or recess_depth < host.thickness", "error", "A recess must be shallower than its host.")
    t.step("profile", "polygon", {"points": "profile_points"}, "xz")
    t.step("void_wall", "extrude", {"profile": "profile", "from": "y_from", "to": "y_to"}, "xz", when='host_kind = "wall"')
    t.step("profile_plan", "polygon", {"points": "profile_points"}, "xy")
    t.step("void_slab", "extrude", {"profile": "profile_plan", "from": "z_from", "to": "z_to"}, "xy", when='host_kind = "slab"')
    t.step("void", "union", {"items": "[void_wall, void_slab]"})
    t.step("plan_wall", "rectangle", {"min": "[min(for p in profile_points return p[1]), host.y_min]", "max": "[max(for p in profile_points return p[1]), host.y_max]"},
           "xy", when='host_kind = "wall" and above_cut')
    t.step("plan_wall_cross", "union", {"items": "[line([min(for p in profile_points return p[1]), host.y_min], [max(for p in profile_points return p[1]), host.y_max]), "
                                                 "line([min(for p in profile_points return p[1]), host.y_max], [max(for p in profile_points return p[1]), host.y_min])]"},
           "xy", when='host_kind = "wall" and above_cut')
    t.step("plan_slab_cross", "union", {"items": "[boundary_curves(profile_plan), line(profile_points[1], profile_points[3]), line(profile_points[2], profile_points[4])]"},
           "xy", when='host_kind = "slab" and outline_mode = "rectangle"')
    t.step("elev_outline", "boundary_curves", {"region": "profile"}, "xz")
    t.step("elev_cross", "union", {"items": "[line(profile_points[1], profile_points[3]), line(profile_points[2], profile_points[4])]"}, "xz",
           when='outline_mode = "rectangle"')
    t.rep("model.low", "model", "low", [{"geometry": "void", "role": "void"}], note="The void is not drawn; it cuts the host.")
    t.rep("model.medium", "model", "medium", [{"geometry": "void", "role": "void"}])
    t.rep("model.high", "model", "high", [{"geometry": "void", "role": "void"}])
    t.rep("plan.low", "plan", "low", [{"geometry": "plan_wall", "class": "overhead"}, {"geometry": "plan_slab_cross", "class": "projected"}])
    t.rep("plan.medium", "plan", "medium", [{"geometry": "plan_wall", "class": "overhead"}, {"geometry": "plan_wall_cross", "class": "overhead"},
                                            {"geometry": "plan_slab_cross", "class": "projected"}],
          note="Wall openings below the cut show as a gap in the host's cut; openings above the cut are drawn dashed with a cross. Slab openings: outline with a cross.")
    t.rep("plan.high", "plan", "high", [{"geometry": "plan_wall", "class": "overhead"}, {"geometry": "plan_wall_cross", "class": "overhead"},
                                        {"geometry": "plan_slab_cross", "class": "projected"}])
    t.rep("elevation", "elevation", "all", [{"geometry": "elev_outline", "class": "projected"}, {"geometry": "elev_cross", "class": "annotation"}])
    t.host = {"hosts": ["IfcWall", "IfcSlab", "IfcRoof", "IfcCovering", "IfcPlate", "IfcCurtainWall", "IfcBeam", "IfcColumn", "IfcMember"],
              "inputs": {"thickness": {"type": "length", "default": 0.2}, "y_min": {"type": "length", "default": -0.1}, "y_max": {"type": "length", "default": 0.1},
                         "bottom": {"type": "length", "default": 0.0}, "top": {"type": "length", "default": 3.0}},
              "void": {"geometry": "void", "ifc": "this element (IfcRelVoidsElement to the host)"},
              "insertion": {"point": "[0, 0, 0]", "description": "Wall: centre of the width on the host axis at the host base. Slab: the outline's own coordinates on the slab."}}
    t.handles = [{"parameter": "width", "view": ["elevation", "model"], "at": "[width / 2, 0, sill_height + height / 2]", "axis": "x", "symmetric": True},
                 {"parameter": "height", "view": ["elevation", "model"], "at": "[0, 0, sill_height + height]", "axis": "z"},
                 {"slot": "outline", "kind": "points", "view": ["elevation"], "visible": 'outline_mode = "custom"'}]
    t.add_psets({}, {"Width": "open_width", "Height": "open_height", "Depth": "depth", "Area": "area", "Volume": "area * depth"})
    return t

# ====================================================================== flight (stair)
def stair():
    t = Template("IfcStair", "flight", "Stair (class template)",
                 "Straight-run stair between two storeys: riser count from the rise and the maximum riser, going, width, concrete waist or solid, plan symbol with cut line and walking line.",
                 "STRAIGHT_RUN_STAIR")
    t.par("rise_mode", "choice", "storey", "Total rise", "Rise", options=["storey", "value"], option_labels={"storey": "Storey height", "value": "Value"})
    t.par("rise_value", "length", 3.0, "Total rise", "Rise", visible='rise_mode = "value"', limits={"min": 0.1, "max": 10})
    t.par("max_riser", "length", 0.18, "Maximum riser", "Steps", limits={"min": 0.05, "max": 0.3},
          description="Generic default (no EN/ISO stair geometry norm); a rule set layer sets regional limits.")
    t.par("going", "length", 0.28, "Going", "Steps", limits={"min": 0.1, "max": 0.6})
    t.par("width", "length", 1.0, "Width", "Size", limits={"min": 0.4, "max": 10})
    t.par("structure", "choice", "waist", "Structure", "Structure", options=["waist", "solid"],
          option_labels={"waist": "Concrete waist slab", "solid": "Solid (on fill or masonry)"})
    t.par("waist_thickness", "length", 0.15, "Waist thickness", "Structure", visible='structure = "waist"', limits={"min": 0.05, "max": 0.5})
    t.material_slot("material", "Material", "reinforced_concrete")
    t.par("arrow_label", "text", "UP", "Walking line label", "Drawing")
    t.dv("total_rise", 'if rise_mode = "storey" then level.height else rise_value')
    t.dv("risers", "ceiling(total_rise / max_riser)")
    t.dv("riser", "total_rise / risers")
    t.dv("treads", "risers - 1")
    t.dv("run", "treads * going")
    t.dv("pitch", "atan2(riser, going)")
    t.dv("step_rule", "2 * riser + going", "Shown for information (2R + G); checked only by a rule set.")
    t.dv("waist_v", "waist_thickness / cos(pitch)", "Waist thickness measured vertically.")
    t.dv("under_x0", "max(0, (waist_v - riser) * going / riser)")
    t.dv("under_z0", "max(0, riser - waist_v)")
    t.dv("steps", "for j in 1..2 * treads return if modulo(j, 2) = 1 then [(j - 1) / 2 * going, (j + 1) / 2 * riser] else [j / 2 * going, j / 2 * riser]",
         "Nosing and back of each tread (two points per tread).")
    t.dv("profile_points", 'if structure = "waist" then concatenate([[0, 0]], steps, [[run, total_rise], [run, total_rise - waist_v], [under_x0, under_z0]]) '
         'else concatenate([[0, 0]], steps, [[run, total_rise], [run, 0]])')
    t.dv("x_cut", "min(run, max(0, (view.cut_height - riser) * going / riser))", "Where the plan cut height meets the stair.")
    t.dv("hw", "width / 2")
    t.rulesets = [{"id": "stairs", "default": None, "note": "No stair rule set by default (no EN/ISO stair geometry norm). Layers add regional limits (spec/objects/rulesets.md).",
                   "fields": {"riser_min": "length", "riser_max": "length", "going_min": "length", "going_max": "length",
                              "rule_min": "length", "rule_max": "length", "width_min": "length"}}]
    t.check("min_risers", "risers >= 2", "error", "A stair needs at least two risers.")
    t.check("riser_range", "rules.stairs = null or (riser >= rules.stairs.riser_min and riser <= rules.stairs.riser_max)", "warning", "Riser is outside the active rule set.")
    t.check("going_range", "rules.stairs = null or (going >= rules.stairs.going_min and going <= rules.stairs.going_max)", "warning", "Going is outside the active rule set.")
    t.check("step_rule_range", "rules.stairs = null or rules.stairs.rule_min = null or (step_rule >= rules.stairs.rule_min and step_rule <= rules.stairs.rule_max)",
            "warning", "2R + G is outside the active rule set.")
    t.check("width_min", "rules.stairs = null or rules.stairs.width_min = null or width >= rules.stairs.width_min", "warning", "Width is below the active rule set.")
    t.check("straight_only", 'predefined_type = "STRAIGHT_RUN_STAIR" or predefined_type = "USERDEFINED" or predefined_type = "NOTDEFINED"', "warning",
            "This class template draws a straight run; use the library objects (C-02…C-05) for other stair forms.")
    t.step("profile", "polygon", {"points": "profile_points"}, "xz")
    t.step("body", "extrude", {"profile": "profile", "from": "-hw", "to": "hw"}, "xz")
    t.step("outline_below", "rectangle", {"min": "[0, -hw]", "max": "[x_cut, hw]"}, "xy")
    t.step("outline_above", "rectangle", {"min": "[x_cut, -hw]", "max": "[run, hw]"}, "xy", when="x_cut < run")
    t.step("treads_below", "for_each", {"items": "for k in 1..treads return k", "as": "k", "index": "i",
                                        "do": "if k * going <= x_cut then line([k * going, -hw], [k * going, hw]) else null"}, "xy")
    t.step("treads_above", "for_each", {"items": "for k in 1..treads return k", "as": "k", "index": "i",
                                        "do": "if k * going > x_cut then line([k * going, -hw], [k * going, hw]) else null"}, "xy")
    t.step("cut_line", "polyline", {"points": "[[x_cut - 0.15, -hw], [x_cut - 0.05, -0.1 * width], [x_cut + 0.05, 0.1 * width], [x_cut + 0.15, hw]]"}, "xy",
           when="x_cut < run")
    t.step("walk_line", "polyline", {"points": "[[going / 2, 0], [run, 0]]"}, "xy")
    t.step("arrow", "polyline", {"points": "[[run - 0.15, -0.075], [run, 0], [run - 0.15, 0.075]]"}, "xy")
    t.step("label", "text", {"at": "[going / 2, -0.12]", "value": "arrow_label", "height": "0.0025"}, "xy")
    t.rep("model.low", "model", "low", [{"geometry": "body", "material": "material"}])
    t.rep("model.medium", "model", "medium", [{"geometry": "body", "material": "material"}])
    t.rep("model.high", "model", "high", [{"geometry": "body", "material": "material"}])
    plan_items = [{"geometry": "outline_below", "class": "projected"}, {"geometry": "treads_below", "class": "projected"},
                  {"geometry": "outline_above", "class": "overhead"}, {"geometry": "treads_above", "class": "overhead"},
                  {"geometry": "cut_line", "class": "cut"}, {"geometry": "walk_line", "class": "annotation", "role": "walking_line"},
                  {"geometry": "arrow", "class": "annotation", "role": "walking_line"}, {"geometry": "label", "class": "annotation"}]
    t.rep("plan.low", "plan", "low", plan_items[:1] + plan_items[2:3] + plan_items[4:])
    t.rep("plan.medium", "plan", "medium", plan_items, note="Treads below the cut drawn, above it dashed; break line at the cut; walking line with arrow and label.")
    t.rep("plan.high", "plan", "high", plan_items)
    t.rep("section", "section", "all", None, source="derived", derive={"from": "model.{lod}", "method": "cut"})
    t.host = {"is_host": False, "level": "Base on a storey, top at the next storey (or a set rise).",
              "slab_opening": {"note": "The application cuts the upper slab over the run plus headroom (detailed objects C-01…C-04 define this)."},
              "nested": "Railings (C-07) are nested by the library objects, not the class template."}
    t.handles = [{"parameter": "width", "view": ["plan"], "at": "[run / 2, hw, 0]", "axis": "y"}]
    t.ifc_props = {"Pset_StairCommon.NumberOfRiser": "risers", "Pset_StairCommon.NumberOfTreads": "treads", "Pset_StairCommon.RiserHeight": "riser",
                   "Pset_StairCommon.TreadLength": "going", "Pset_StairCommon.WaistThickness": 'if structure = "waist" then waist_thickness else null'}
    t.add_psets(t.ifc_props, {})
    t.extra_ifc = {"decomposition": "IfcStair aggregating one IfcStairFlight (predefined STRAIGHT) in the template; landings and further flights in the library objects."}
    return t

# ====================================================================== assembly (truss)
def assembly():
    t = Template("IfcElementAssembly", "assembly", "Element assembly (class template)",
                 "Assembly that nests other OPO objects. The template builds a flat truss (Warren or Pratt) from nested IfcMember class templates.",
                 "TRUSS")
    t.par("span", "length", 8.0, "Span", "Truss", limits={"min": 1, "max": 100})
    t.par("truss_depth", "length", 1.0, "Depth (chord centres)", "Truss", limits={"min": 0.2, "max": 10})
    t.par("panels", "integer", 8, "Panels", "Truss", limits={"min": 2, "max": 60})
    t.par("pattern", "choice", "warren", "Pattern", "Truss", options=["warren", "pratt"])
    t.par("chord_width", "length", 0.12, "Chord section", "Members", limits={"min": 0.02, "max": 1}, description="Square hollow section, width = depth.")
    t.par("chord_wall", "length", 0.006, "Chord wall thickness", "Members", limits={"min": 0.002, "max": 0.05})
    t.par("web_width", "length", 0.08, "Web member section", "Members", limits={"min": 0.02, "max": 1})
    t.par("web_wall", "length", 0.005, "Web wall thickness", "Members", limits={"min": 0.002, "max": 0.05})
    t.material_slot("material", "Material", "steel")
    t.dv("panel", "span / panels")
    t.dv("member_object", '"opo-format.org/library/templates/IfcMember"')
    t.dv("chord_values", '{predefined_type: "CHORD", profile_kind: "rect_hollow", width: chord_width, depth: chord_width, wall_thickness: chord_wall, material: material}')
    t.dv("web_values", '{predefined_type: "MEMBER", profile_kind: "rect_hollow", width: web_width, depth: web_width, wall_thickness: web_wall, material: material}')
    t.dv("diagonals", 'for k in 1..panels return if pattern = "warren" then (if modulo(k, 2) = 1 then [[(k - 1) * panel, 0, 0], [k * panel, 0, truss_depth]] '
         'else [[(k - 1) * panel, 0, truss_depth], [k * panel, 0, 0]]) '
         'else (if k <= panels / 2 then [[(k - 1) * panel, 0, truss_depth], [k * panel, 0, 0]] else [[(k - 1) * panel, 0, 0], [k * panel, 0, truss_depth]])',
         "Warren: alternating diagonals. Pratt: diagonals slope down towards the middle.")
    t.dv("verticals", 'if pattern = "pratt" then for k in 0..panels return [[k * panel, 0, 0], [k * panel, 0, truss_depth]] else []')
    t.dv("member_count", "2 + count(diagonals) + count(verticals)")
    t.check("panels_even", 'pattern != "warren" or modulo(panels, 2) = 0', "warning", "A Warren truss with an odd number of panels ends on a different chord at each support.")
    t.step("top_chord", "instance", {"object": "member_object", "values": "chord_values", "inputs": "{path: [[0, 0, truss_depth], [span, 0, truss_depth]]}"})
    t.step("bottom_chord", "instance", {"object": "member_object", "values": "chord_values", "inputs": "{path: [[0, 0, 0], [span, 0, 0]]}"})
    t.step("web_diagonals", "for_each", {"items": "diagonals", "as": "d", "index": "i", "do": "instance(member_object, web_values, {path: d})"})
    t.step("web_verticals", "for_each", {"items": "verticals", "as": "d", "index": "i", "do": "instance(member_object, web_values, {path: d})"})
    t.step("plan_line", "line", {"start": "[0, 0]", "end": "[span, 0]"}, "xy")
    t.step("plan_band", "rectangle", {"min": "[0, -chord_width / 2]", "max": "[span, chord_width / 2]"}, "xy")
    items = [{"geometry": g, "material": "material", "part": p} for g, p in
             [("top_chord", "Chord"), ("bottom_chord", "Chord"), ("web_diagonals", "Web"), ("web_verticals", "Web")]]
    t.rep("model.low", "model", "low", items)
    t.rep("model.medium", "model", "medium", items)
    t.rep("model.high", "model", "high", items)
    t.rep("plan.low", "plan", "low", [{"geometry": "plan_line", "class": "overhead"}])
    t.rep("plan.medium", "plan", "medium", [{"geometry": "plan_band", "class": "overhead"}])
    t.rep("plan.high", "plan", "high", None, source="derived", derive={"from": "model.high", "method": "project"})
    t.rep("elevation", "elevation", "all", None, source="derived", derive={"from": "model.{lod}", "method": "project"})
    t.host = {"is_host": False, "nested": {"objects": ["opo-format.org/library/templates/IfcMember"],
                                           "rule": "Nested objects are referenced by id and version; a packaged .opo embeds them (spec §4.9)."}}
    t.extra_ifc = {"decomposition": "IfcElementAssembly aggregating the nested members (IfcRelAggregates); each nested instance exports as its own class (IfcMember CHORD / MEMBER)."}
    t.add_psets({}, {})
    return t

ALL = [member, wall, slab, beam, boiler, pipe_fitting, opening, stair, assembly]  # member first: the truss nests it

if __name__ == "__main__":
    for f in ALL:
        t = f()
        doc, env, geo = t.write()
        n_mesh = sum(1 for n in doc["data"] if "usd::usdgeom::mesh" in n.get("attributes", {}))
        n_crv = sum(1 for n in doc["data"] if "usd::usdgeom::basiscurves" in n.get("attributes", {}))
        print(f"{t.cls:20s} {t.archetype:9s} params {len(t.P):3d}  steps {len(t.R):2d}  baked meshes {n_mesh:2d} curves {n_crv:2d}  layers {len(t.layers_files)}")
