"""Run the conformance suite against the Python prototypes (until opo-rs takes over).
Usage: python3 tools/run_conformance.py [repo root]"""
import json, sys
from pathlib import Path
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(ROOT / "tools"))
from feel import feel  # noqa: E402
import recipe as RX  # noqa: E402
from check_opo import mesh_volume, resolver  # noqa: E402

def same(a, b, path=""):
    if isinstance(a, bool) or isinstance(b, bool) or a is None or b is None or isinstance(a, str) or isinstance(b, str):
        return [] if a == b else [f"{path}: expected {b!r}, got {a!r}"]
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return [] if abs(a - b) <= 1e-9 * max(1.0, abs(b)) else [f"{path}: expected {b}, got {a}"]
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): return [f"{path}: expected {len(b)} items, got {len(a)}"]
        return [e for i, (x, y) in enumerate(zip(a, b)) for e in same(x, y, f"{path}[{i}]")]
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b): return [f"{path}: keys differ {sorted(set(a) ^ set(b))}"]
        return [e for k in b for e in same(a[k], b[k], f"{path}.{k}")]
    return [f"{path}: expected {b!r}, got {a!r}"]

fails = 0; n = 0
for c in json.loads((ROOT / "conformance/feel/cases.json").read_text())["cases"]:
    n += 1
    try: got = feel(c["expr"], c.get("context", {}))
    except Exception as e: got = f"error: {e}"
    errs = same(got, c["expected"], c["id"])
    if errs: fails += 1; print("FEEL", errs[0])
for f in sorted((ROOT / "conformance/objects").glob("*.json")):
    suite = json.loads(f.read_text())
    folder = (f.parent / suite["object"]).resolve()
    doc = json.loads((folder / "object.ifcx").read_text())
    for c in suite["cases"]:
        n += 1
        env, geo, T = RX.run(doc, values=c.get("values"), inputs=c.get("inputs"), context=c.get("context"), base_dir=folder.parent, resolver=resolver)
        exp = c["expected"]; errs = []
        errs += same({d["name"]: env[d["name"]] for d in T["opo::rules"]["derived"]}, exp["derived"], "derived")
        errs += same({k["id"]: feel(k["expr"], env) for k in T["opo::rules"]["checks"]}, exp["checks"], "checks")
        if "ifc_properties" in exp: errs += same({k: feel(v, env) for k, v in T["opo::ifc"]["properties"].items()}, exp["ifc_properties"], "ifc")
        if "quantities" in exp: errs += same({f"{q}.{k}": feel(v, env) for q, qd in T["opo::ifc"]["quantities"].items() for k, v in qd["values"].items()}, exp["quantities"], "qto")
        for rid, items in exp["geometry"].items():
            for it in items:
                g = [x for x in RX.flat(geo.get(it["geometry"])) if x["kind"] == "solid"]
                vol = sum(mesh_volume(x) for x in g)
                if len(g) != it["solids"]: errs.append(f"{rid}.{it['geometry']}: {len(g)} solids, expected {it['solids']}")
                elif abs(vol - it["volume"]) > it["tolerance"] * max(abs(it["volume"]), 1e-12): errs.append(f"{rid}.{it['geometry']}: volume {vol} vs {it['volume']}")
        if errs: fails += 1; print(f.stem, c["id"], errs[:2])
print(f"{n - fails}/{n} conformance cases pass")
sys.exit(1 if fails else 0)
