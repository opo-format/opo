"""Create the conformance suite (conformance/) once from the prototypes. After review the JSON files are the
reference; this script is deleted with the other prototypes (docs/migration.md phase 5).
Usage: python3 tools/gen_conformance.py [repo root]
"""
import json, math, re, sys
from pathlib import Path

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(ROOT / "tools"))
from feel import feel  # noqa: E402
import recipe as RX  # noqa: E402
from check_opo import mesh_volume, resolver  # noqa: E402

OUT = ROOT / "conformance"
CURVED = {"circle", "arc", "revolve", "cylinder"}
TOL_EXACT, TOL_CURVED = 1e-6, 0.03

def clean(v):
    if isinstance(v, float):
        return 0.0 if abs(v) < 1e-15 else float(repr(round(v, 12)))
    if isinstance(v, list): return [clean(x) for x in v]
    if isinstance(v, dict): return {k: clean(x) for k, x in v.items()}
    return v

def dumpj(obj):
    s = json.dumps(obj, indent=1, ensure_ascii=False)
    s = re.sub(r"\[\s+([^\[\]{}]*?)\s+\]", lambda m: "[" + re.sub(r"\s*\n\s*", " ", m.group(1)) + "]", s)
    return s + "\n"

# ------------------------------------------------------------------ FEEL cases
FEEL = [
    # (id, expression, context, note)
    ("arith-precedence", "1 + 2 * 3", {}, None), ("arith-parens", "(1 + 2) * 3", {}, None),
    ("arith-power", "2 ** 3", {}, None), ("arith-unary-minus", "-(2 - 5)", {}, None),
    ("arith-div-zero", "1 / 0", {}, "division by zero gives null"),
    ("null-arith", "null + 1", {}, "null propagates"), ("null-compare", "null < 1", {}, None),
    ("null-equals-null", "null = null", {}, None),
    ("cmp-float-eq", "0.1 + 0.2 = 0.3", {}, "numbers within 1e-9 are equal"),
    ("cmp-float-ne", "0.1 != 0.1000001", {}, None),
    ("cmp-string", "\"left\" = \"left\"", {}, None),
    ("logic-and-null", "false and null", {}, "three-valued logic"), ("logic-or-null", "true or null", {}, None),
    ("logic-and-unknown", "true and null", {}, None), ("logic-not", "not(false)", {}, None),
    ("logic-not-null", "not(null)", {}, None),
    ("if-true", "if 2 > 1 then \"a\" else \"b\"", {}, None), ("if-null-condition", "if null then 1 else 2", {}, "a null condition takes the else branch"),
    ("if-nested", "if w >= mm(1200) then 2 else if w >= mm(900) then 1 else 0", {"w": 0.9}, None),
    ("unit-mm", "mm(900)", {}, None), ("unit-cm", "cm(5)", {}, None), ("unit-m", "m(2.5)", {}, None),
    ("unit-inch", "inch(36)", {}, None), ("unit-ft", "ft(6) + inch(8)", {}, None), ("unit-deg", "deg(90)", {}, None),
    ("trig-sin", "sin(30)", {}, "degrees"), ("trig-cos", "cos(60)", {}, None), ("trig-tan", "tan(45)", {}, None),
    ("trig-atan2", "atan2(1, 1)", {}, None),
    ("num-min-args", "min(3, 1, 2)", {}, None), ("num-min-list", "min([3, 1, 2])", {}, None), ("num-max-list", "max([1, 5, 2])", {}, None),
    ("num-abs", "abs(-0.2)", {}, None), ("num-sqrt", "sqrt(2)", {}, None),
    ("num-ceiling", "ceiling(2.8 / 0.175)", {}, "16 exactly: values within 1e-9 of an integer are not rounded up"),
    ("num-ceiling-frac", "ceiling(2.1)", {}, None), ("num-floor", "floor(-2.5)", {}, None),
    ("num-round-half-even-1", "round(2.5)", {}, "half to even"), ("num-round-half-even-2", "round(3.5)", {}, None),
    ("num-round-scale", "round(1.23456, 2)", {}, None), ("num-modulo", "modulo(7, 3)", {}, None),
    ("num-modulo-negative", "modulo(-7, 3)", {}, "result has the sign of the divisor"),
    ("list-literal", "[1, 2, 3]", {}, None), ("list-index-first", "[1, 2, 3][1]", {}, "1-based"),
    ("list-index-last", "[1, 2, 3][-1]", {}, "negative counts from the end"), ("list-index-out", "[1, 2, 3][4]", {}, "out of range gives null"),
    ("list-index-zero", "[1, 2, 3][0]", {}, None),
    ("list-sum", "sum([1, 2, 3.5])", {}, None), ("list-sum-empty", "sum([])", {}, "empty sum is null"),
    ("list-count", "count([1, 2, 3])", {}, None), ("list-sublist", "sublist([1, 2, 3, 4], 2, 2)", {}, None),
    ("list-sublist-tail", "sublist([1, 2, 3, 4], 3)", {}, None), ("list-sublist-negative", "sublist([1, 2, 3, 4], -2)", {}, None),
    ("list-append", "append([1, 2], 3)", {}, None), ("list-concatenate", "concatenate([1], [2, 3], [])", {}, None),
    ("list-reverse", "reverse([1, 2, 3])", {}, None), ("list-index-of", "index_of([\"a\", \"b\", \"a\"], \"a\")", {}, None),
    ("list-contains", "list_contains([1, 2], 2)", {}, None), ("list-flatten-deep", "flatten([[1, [2]], [3]])", {}, "deep, as in FEEL"),
    ("for-basic", "for i in 1..3 return i * 2", {}, None), ("for-descending", "for i in 3..1 return i", {}, "a range runs downwards when the start is larger"),
    ("for-list", "for x in [0.1, 0.2] return x * 10", {}, None),
    ("for-nested", "for i in 1..2, j in 1..2 return i * 10 + j", {}, None),
    ("for-points", "for j in 1..4 return if modulo(j, 2) = 1 then [(j - 1) / 2, (j + 1) / 2] else [j / 2, j / 2]", {}, None),
    ("ctx-literal", "{a: 1, b: \"x\"}", {}, None), ("ctx-access", "{a: 1, b: 2}.b", {}, None),
    ("ctx-quoted-key", "{\"a b\": 3}", {}, None),
    ("ctx-path", "host.thickness", {"host": {"thickness": 0.2}}, None),
    ("path-on-list", "layers.thickness", {"layers": [{"thickness": 0.015}, {"thickness": 0.2}]}, "a path on a list maps over it"),
    ("path-missing", "host.missing", {"host": {"thickness": 0.2}}, "missing key gives null"),
    ("layers-total", "sum(layers.thickness)", {"layers": [{"thickness": 0.015}, {"thickness": 0.2}, {"thickness": 0.015}]}, None),
    ("layers-start", "for i in 1..count(layers) return sum(sublist(layers.thickness, 1, i)) - layers[i].thickness",
     {"layers": [{"thickness": 0.015}, {"thickness": 0.2}, {"thickness": 0.015}]}, "the layer offsets used by walls and slabs"),
    ("core-index", "if count(index_of(layers.core, true)) > 0 then index_of(layers.core, true)[1] else ceiling(count(layers) / 2)",
     {"layers": [{"thickness": 0.01}, {"thickness": 0.2, "core": True}, {"thickness": 0.01}]}, None),
    ("polygon-area", "abs(sum(for i in 1..count(p) return p[i][1] * p[modulo(i, count(p)) + 1][2] - p[modulo(i, count(p)) + 1][1] * p[i][2])) / 2",
     {"p": [[0, 0], [6, 0], [6, 4], [0, 4]]}, "shoelace area as used by slabs"),
    ("string-concat", "\"IPE \" + \"270\"", {}, None),
]

def feel_cases():
    out = []
    for cid, expr, ctx, note in FEEL:
        c = {"id": cid, "expr": expr}
        if ctx: c["context"] = ctx
        c["expected"] = clean(feel(expr, ctx))
        if note: c["note"] = note
        out.append(c)
    return out

# ------------------------------------------------------------------ object cases
def curved_steps(T):
    steps = {s["id"]: s for s in T["opo::recipe"]}
    memo = {}
    def is_curved(sid, seen=()):
        if sid in memo: return memo[sid]
        s = steps[sid]
        txt = json.dumps(s["args"])
        r = s["op"] in CURVED or any(f"{op}(" in txt for op in CURVED) or s["op"] == "instance" or "instance(" in txt
        if not r:
            for other in steps:
                if other != sid and other not in seen and re.search(r"\b" + re.escape(other) + r"\b", txt):
                    if is_curved(other, seen + (sid,)): r = True; break
        memo[sid] = r
        return r
    return {sid for sid in steps if is_curved(sid)}

def object_cases(folder, extra_cases, label):
    doc = json.loads((folder / "object.ifcx").read_text())
    T = RX.type_node(doc)
    params = {p["name"]: p for p in T["opo::parameters"]}
    curved = curved_steps(T)
    nodes = {}
    for f in sorted(folder.rglob("*.ifcx")):
        for n in json.loads(f.read_text())["data"]:
            c = nodes.setdefault(n["path"], {"f": f, "inherits": {}, "attributes": {}})
            c["inherits"].update(n.get("inherits", {}))
            for k, v in n.get("attributes", {}).items(): c["attributes"].setdefault(k, v)
    cases = [("default", {}, {}, {})]
    if "predefined_type" in params:
        for opt in params["predefined_type"]["options"]:
            if opt != params["predefined_type"]["default"]: cases.append((f"type-{opt.lower()}", {"predefined_type": opt}, {}, {}))
    for p in T["opo::parameters"]:
        if p["type"] == "choice" and p["name"] != "predefined_type":
            for opt in p["options"]:
                if opt != p["default"]: cases.append((f"{p['name']}-{opt}".replace("_", "-").lower(), {p["name"]: opt}, {}, {}))
        if p["type"] == "boolean":
            cases.append((f"{p['name']}-{str(not p['default']).lower()}".replace("_", "-"), {p["name"]: not p["default"]}, {}, {}))
    rulesets = {}
    for path, n in nodes.items():
        a = n.get("attributes", {})
        if "bsi::ifc::prop::TypeName" in a and n["f"].name != "object.ifcx":
            vals = {}
            for ref in n.get("inherits", {}).values():
                vals.update(nodes.get(ref, {}).get("attributes", {}).get("opo::values", {}))
            vals.update(a.get("opo::values", {}))
            slug = re.sub(r"[^a-z0-9]+", "-", f'{n["f"].stem}-{a["bsi::ifc::prop::TypeName"]}'.lower()).strip("-")
            cases.append((slug, vals, {}, {}))
    for f in sorted(folder.glob("layers/*.ifcx")):
        for n in json.loads(f.read_text())["data"]:
            for rs in (n.get("attributes", {}).get("opo::rules") or {}).get("rulesets", []):
                if "values" in rs: rulesets[(f.stem, rs["id"])] = {k: feel(v, {}) for k, v in rs["values"].items()}
    variant_cases = [c for c in cases if c[0].startswith("sizes-") or c[0].startswith("types-") or c[0].startswith("profiles-")]
    for (stem, rid), rvals in sorted(rulesets.items()):
        cases.append((stem, {}, {}, {"rules": {rid: rvals}}))
        for vid, vvals, _, _ in variant_cases:
            cases.append((f"{stem}--{vid}", vvals, {}, {"rules": {rid: rvals}}))
    cases += extra_cases
    out = []
    for cid, vals, ins, ctx in cases:
        env, geo, _ = RX.run(doc, values=vals, inputs=ins, context=ctx, base_dir=folder.parent, resolver=resolver)
        derived = {d["name"]: clean(env[d["name"]]) for d in T["opo::rules"]["derived"]}
        checks = {c["id"]: feel(c["expr"], env) for c in T["opo::rules"]["checks"]}
        props = {k: clean(feel(v, env)) for k, v in T["opo::ifc"].get("properties", {}).items()}
        qto = {f"{q}.{k}": clean(feel(v, env)) for q, qd in (T["opo::ifc"].get("quantities") or {}).items() for k, v in qd["values"].items()}
        ports = {}
        for pt in T.get("opo::ports", []) or []:
            if "when" in pt and feel(pt["when"], env) is not True: continue
            ports[pt["name"]] = {k: clean(feel(pt[k], env)) for k in ("nominal_size", "position", "direction")}
        geom = {}
        for rid in ("model.medium", "model.high"):
            rep = next((r for r in T["opo::representations"] if r["id"] == rid), None)
            if not rep or "items" not in rep: continue
            items = []
            for it in rep["items"]:
                g = [x for x in RX.flat(geo.get(it["geometry"])) if x["kind"] == "solid"]
                items.append({"geometry": it["geometry"], "solids": len(g), "volume": clean(sum(mesh_volume(x) for x in g)),
                              "tolerance": TOL_CURVED if it["geometry"] in curved else TOL_EXACT})
            geom[rid] = items
        if T["opo::ifc"]["class"] == "IfcOpeningElement":
            g = [x for x in RX.flat(geo.get("void")) if x["kind"] == "solid"]
            geom["void"] = [{"geometry": "void", "solids": len(g), "volume": clean(sum(mesh_volume(x) for x in g)), "tolerance": TOL_EXACT}]
        case = {"id": cid}
        if vals: case["values"] = clean(vals)
        if ins: case["inputs"] = clean(ins)
        if ctx: case["context"] = clean(ctx)
        case["expected"] = {"derived": derived, "checks": checks}
        if props: case["expected"]["ifc_properties"] = props
        if qto: case["expected"]["quantities"] = qto
        if ports: case["expected"]["ports"] = ports
        case["expected"]["geometry"] = geom
        out.append(case)
    rel = Path("..") / ".." / folder.relative_to(ROOT)
    return {"object": str(rel).replace("\\", "/"), "label": label, "cases": out}

ARCH = [[-0.5, 0.9], [0.5, 0.9], [0.5, 1.9]] + [[round(0.5 * math.cos(math.radians(a)), 9), round(1.9 + 0.5 * math.sin(math.radians(a)), 9)] for a in range(15, 180, 15)] + [[-0.5, 1.9]]
UK_STAIRS = {"stairs": {"riser_min": 0.15, "riser_max": 0.22, "going_min": 0.22, "going_max": 0.30, "rule_min": 0.55, "rule_max": 0.70, "width_min": None}}
EXTRA = {
    "IfcWall": [("l-shaped-path", {}, {"path": [[0, 0], [5, 0], [5, 4]]}, {}),
                ("l-shaped-path-finish-left", {"location_line": "finish_left"}, {"path": [[0, 0], [5, 0], [5, 4]]}, {})],
    "IfcSlab": [("hole", {}, {"holes": [[[1, 1], [2, 1], [2, 2], [1, 2]]]}, {})],
    "IfcBeam": [("sloped-with-extensions", {"start_extension": 0.2, "end_extension": 0.3}, {"path": [[0, 0, 0], [3, 0, 1]]}, {})],
    "IfcStair": [("ruleset-uk-private", {}, {}, {"rules": UK_STAIRS}), ("ruleset-uk-private-going-too-short", {"going": 0.2}, {}, {"rules": UK_STAIRS})],
    "IfcOpeningElement": [("custom-outline-arch", {"outline_mode": "custom"}, {"outline": ARCH}, {}),
                          ("slab-host", {"host_kind": "slab"}, {}, {})],
}

def main():
    (OUT / "feel").mkdir(parents=True, exist_ok=True)
    (OUT / "objects").mkdir(parents=True, exist_ok=True)
    cases = feel_cases()
    (OUT / "feel/cases.json").write_text(dumpj({"suite": "feel", "spec": "0.1", "cases": cases}))
    objs = [(ROOT / "examples/door/single-swing-door", "door-single-swing", "Door example (O-01)")]
    objs += [(p, f"template-{p.name}", f"Class template {p.name}") for p in sorted((ROOT / "library/templates").iterdir()) if (p / "object.ifcx").exists()]
    total = 0
    for folder, name, label in objs:
        data = object_cases(folder, EXTRA.get(folder.name, []), label)
        data = {"suite": "objects", "spec": "0.1", **data}
        (OUT / "objects" / f"{name}.json").write_text(dumpj(data))
        total += len(data["cases"])
        print(f"{name:32s} {len(data['cases']):3d} cases")
    print(f"feel: {len(cases)} cases; objects: {total} cases")

if __name__ == "__main__":
    main()
