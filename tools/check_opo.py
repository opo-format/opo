"""Check OPO objects: schema, composition, names, FEEL evaluation of defaults, every predefined type and every
variant, recipe execution, IFC mapping, quantities against mesh volumes, materials/hatches, baked geometry.
Usage: python3 tools/check_opo.py [repo root] [object folder ...]   (default: every folder in library/templates)
"""
import json, math, sys
from pathlib import Path
import numpy as np

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(ROOT / "tools"))
from feel import feel, names, BUILTINS  # noqa: E402
import recipe as RX  # noqa: E402

SCHEMA = json.loads((ROOT / "schema/opo@v0.1.ifcx").read_text())["schemas"]
PSETS = json.loads((ROOT / "tools/ifc4x3_psets.json").read_text())
CONTEXT_ROOTS = {"host", "level", "view", "rules", "flip"}

def resolver(object_id):
    p = "opo-format.org/"
    return ROOT / object_id[len(p):] if object_id.startswith(p) else None

def mesh_volume(g):
    P = np.asarray(g["points"], float); F = np.asarray(g["faces"], int)
    return float(abs(np.einsum("ij,ij->i", P[F[:, 0]], np.cross(P[F[:, 1]], P[F[:, 2]])).sum()) / 6)

def check_folder(folder):
    errs, notes = [], []
    docs = {p.relative_to(folder).as_posix(): json.loads(p.read_text()) for p in sorted(folder.rglob("*.ifcx"))}
    base = docs["object.ifcx"]
    nodes = {}
    for rel, d in docs.items():
        for n in d["data"]:
            c = nodes.setdefault(n["path"], {"children": {}, "inherits": {}, "attributes": {}, "file": rel})
            for k in ("children", "inherits"): c[k].update(n.get(k, {}))
            for k, v in n.get("attributes", {}).items():
                if k.startswith("opo::") and k not in SCHEMA: errs.append(f"{rel}: attribute {k} not declared in the schema")
                c["attributes"].setdefault(k, v)
    for p, c in nodes.items():
        for r in list(c["children"].values()) + list(c["inherits"].values()):
            if r not in nodes: errs.append(f"dangling reference {r} from {p}")
    T = RX.type_node(base)
    cls = T["opo::ifc"]["class"]
    params = {p["name"]: p for p in T["opo::parameters"]}
    slots = {s["name"] for s in T.get("opo::slots", [])}
    derived = [d["name"] for d in T["opo::rules"]["derived"]]
    steps = [s["id"] for s in T["opo::recipe"]]
    known = set(params) | slots | set(derived) | CONTEXT_ROOTS | set(RX.OPS) | {"instance"}

    def need(expr, where, extra=()):
        if not isinstance(expr, str): return
        try: used = names(expr)
        except Exception as e: errs.append(f"{where}: does not parse: {e}"); return
        miss = used - known - set(extra)
        if miss: errs.append(f"{where}: unknown names {sorted(miss)} in {expr!r}")

    # --- names
    seen = set()
    for d in T["opo::rules"]["derived"]:
        need(d["expr"], f"derived {d['name']}", extra=[n for n in derived if n not in seen and n != d["name"]] and ())
        seen.add(d["name"])
    for p in T["opo::parameters"]:
        if "visible" in p: need(p["visible"], f"parameter {p['name']}.visible")
        for pr in p.get("properties", []):
            if "value" in pr: need(pr["value"], f"{p['name']}.{pr['name']}")
    for c in T["opo::rules"]["checks"]: need(c["expr"], f"check {c['id']}")
    done = set()
    for s in T["opo::recipe"]:
        avail = done | ({s["args"].get("as", "item"), s["args"].get("index", "i")} if s["op"] == "for_each" else set())
        if "when" in s: need(s["when"], f"step {s['id']}.when", done)
        for k, v in s["args"].items():
            if k == "object" and s["op"] == "instance": need(v, f"step {s['id']}.object", done); continue
            need(v, f"step {s['id']}.{k}", avail)
        done.add(s["id"])
    for r in T["opo::representations"]:
        for it in r.get("items", []) + r.get("overlay", []):
            if it["geometry"] not in steps: errs.append(f"representation {r['id']}: unknown geometry {it['geometry']}")
            for k in ("material", "hatch"):
                v = it.get(k)
                if v and not v.startswith("each."): need(v, f"representation {r['id']}.{k}")
    for pt in T.get("opo::ports", []):
        for k in ("nominal_size", "position", "direction", "when"): need(pt.get(k), f"port {pt['name']}.{k}")
    ifc = T["opo::ifc"]
    for k, v in ifc.get("properties", {}).items(): need(v, f"ifc property {k}")
    for q, qd in ifc.get("quantities", {}).items():
        for k, v in qd["values"].items(): need(v, f"quantity {q}.{k}")
    for k, v in (ifc.get("material_layer_set") or {}).items():
        if k != "note": need(v, f"material_layer_set.{k}")
    for kind, pd in (ifc.get("profile_def") or {}).items():
        if isinstance(pd, dict):
            for k, v in pd.items():
                if k != "entity": need(v, f"profile_def.{kind}.{k}")
        else: need(pd, f"profile_def.{kind}")
    for k, v in (T["opo::host"].get("provides") or {}).items(): need(v, f"host.provides.{k}")

    # --- IFC property names exist in the IFC templates
    ps_index = {ps["name"]: {p["name"] for p in ps["props"]} for ps in PSETS.get(cls, [])}
    for key in ifc.get("properties", {}):
        ps, _, prop = key.partition(".")
        if ps not in ps_index or prop not in ps_index[ps]: errs.append(f"ifc property {key} is not in the IFC 4.3 templates for {cls}")
    for q, qd in ifc.get("quantities", {}).items():
        for k in qd["values"]:
            if k not in ps_index.get(q, set()): errs.append(f"quantity {q}.{k} is not in the IFC 4.3 templates")

    # --- materials and hatches
    mats, hatches = T["opo::materials"], T["opo::hatches"]
    for m, md in mats.items():
        for role in ("cut", "surface"):
            if role in md and md[role]["hatch"] not in hatches: errs.append(f"material {m}: hatch {md[role]['hatch']} missing from opo::hatches")
    def mats_in(values):
        out = set()
        for v in values.values():
            if isinstance(v, list): out |= {l["material"] for l in v if isinstance(l, dict) and "material" in l}
        for p in T["opo::parameters"]:
            if p["type"] == "material": out.add(values.get(p["name"], p["default"]))
        return out

    # --- evaluation: defaults, every predefined type, every variant
    cases = [("default", {})]
    for opt in params["predefined_type"]["options"]:
        cases.append((f"type {opt}", {"predefined_type": opt}))
    for p in T["opo::parameters"]:
        if p["type"] == "choice" and p["name"] != "predefined_type":
            for opt in p["options"]:
                if opt != p["default"]: cases.append((f"{p['name']} = {opt}", {p["name"]: opt}))
        if p["type"] == "boolean":
            cases.append((f"{p['name']} = {not p['default']}", {p["name"]: not p["default"]}))
    for rel, d in docs.items():
        if rel == "object.ifcx": continue
        for n in d["data"]:
            if "bsi::ifc::prop::TypeName" in n.get("attributes", {}):
                sysvals = {}
                for ref in n.get("inherits", {}).values():
                    sysvals.update(nodes[ref]["attributes"].get("opo::values", {}))
                cases.append((f"{rel}: {n['attributes']['bsi::ifc::prop::TypeName']}", {**sysvals, **n["attributes"].get("opo::values", {})}))
    results = []
    # sample drawn input for optional slots that start empty (e.g. a custom opening outline: arched top)
    arch = [[-0.5, 0.9], [0.5, 0.9], [0.5, 1.9]] + [[0.5 * math.cos(math.radians(a)), 1.9 + 0.5 * math.sin(math.radians(a))] for a in range(15, 180, 15)] + [[-0.5, 1.9]]
    sample = {s["name"]: arch for s in T.get("opo::slots", []) if s.get("default") is None and s["type"] == "polygon"}
    for label, vals in cases:
        try:
            env, geo, _ = RX.run(base, values=vals, inputs=sample, base_dir=folder.parent, resolver=resolver)
        except Exception as e:
            errs.append(f"{label}: recipe failed: {type(e).__name__}: {e}"); continue
        for m in mats_in({**{p: params[p]["default"] for p in params}, **vals}):
            if m not in mats: errs.append(f"{label}: material {m} not in opo::materials")
        failed = []
        for c in T["opo::rules"]["checks"]:
            r = feel(c["expr"], env)
            if r is not True and not (label != "default" and c["severity"] == "warning"):
                failed.append(f"{c['id']} ({c['severity']})")
        if failed and (label == "default" or any("error" in f for f in failed)):
            errs.append(f"{label}: checks not passing: {failed}")
        solids = []
        rep = next(r for r in T["opo::representations"] if r["id"] == "model.medium")
        for it in rep["items"]:
            solids += [g for g in RX.flat(geo.get(it["geometry"])) if g["kind"] == "solid"]
        if not solids and cls != "IfcOpeningElement":
            errs.append(f"{label}: model.medium is empty")
        if cls == "IfcOpeningElement":
            solids = [g for g in RX.flat(geo.get("void")) if g["kind"] == "solid"]
            if not solids: errs.append(f"{label}: no void")
        for k, v in ifc.get("properties", {}).items():
            try: feel(v, env)
            except Exception as e: errs.append(f"{label}: ifc {k}: {e}")
        qv = {}
        for q, qd in ifc.get("quantities", {}).items():
            for k, v in qd["values"].items():
                try: qv[f"{q}.{k}"] = feel(v, env)
                except Exception as e: errs.append(f"{label}: quantity {q}.{k}: {e}")
        for pt in T.get("opo::ports", []):
            if "when" in pt and feel(pt["when"], env) is not True: continue
            for k in ("nominal_size", "position", "direction"):
                if feel(pt[k], env) is None: errs.append(f"{label}: port {pt['name']}.{k} is null")
        vol = sum(mesh_volume(g) for g in solids)
        gross = next((v for k, v in qv.items() if k.endswith(".GrossVolume")), None)
        if gross:
            dev = abs(vol - gross) / gross
            if dev > 0.02: errs.append(f"{label}: mesh volume {vol:.4f} m³ vs quantity GrossVolume {gross:.4f} m³ ({dev:.1%})")
        results.append((label, vol, gross))

    # --- baked geometry matches the recipe at the defaults
    env, geo, _ = RX.run(base, base_dir=folder.parent, resolver=resolver)
    baked = [n for n in base["data"] if "usd::usdgeom::mesh" in n.get("attributes", {})]
    expect = []
    rep = next(r for r in T["opo::representations"] if r["id"] == "model.medium")
    for it in rep["items"]: expect += [g for g in RX.flat(geo.get(it["geometry"])) if g["kind"] == "solid"]
    if len(baked) != len(expect): errs.append(f"baked meshes {len(baked)} != recipe solids {len(expect)}")
    else:
        for b, g in zip(baked, expect):
            if not np.allclose(np.asarray(b["attributes"]["usd::usdgeom::mesh"]["points"]), np.asarray(g["points"]), atol=1e-8):
                errs.append("baked mesh differs from the recipe"); break
    return errs, results, len(cases)

if __name__ == "__main__":
    folders = [Path(a) for a in sys.argv[2:]] or sorted(p for p in (ROOT / "library/templates").iterdir() if (p / "object.ifcx").exists())
    total = 0
    for f in folders:
        errs, results, n = check_folder(f)
        vols = [(l, v, g) for l, v, g in results if g]
        vtxt = f"; volume check {len(vols)} cases" if vols else ""
        print(f"{f.name:20s} {n:3d} cases{vtxt}: " + ("OK" if not errs else f"{len(errs)} problem(s)"))
        for e in errs[:12]: print("   -", e)
        total += len(errs)
    print("OK: no errors" if total == 0 else f"{total} problem(s)")
    sys.exit(1 if total else 0)
