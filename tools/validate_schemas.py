"""Validate every opo:: attribute in the repository against schema/0.1 (JSON Schema 2020-12). Prototype until `opo check` in opo-rs.
Usage: python3 tools/validate_schemas.py [repo root]"""
import json, sys, pathlib
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
schemas = {json.loads(p.read_text())["$id"]: json.loads(p.read_text()) for p in (root / "schema/0.1").glob("*.json")}
reg = Registry().with_resources([(k, Resource.from_contents(v)) for k, v in schemas.items()])
for s in schemas.values(): Draft202012Validator.check_schema(s)
decl = json.loads((root / "schema/opo@v0.1.ifcx").read_text())["schemas"]
files = [p for p in root.rglob("*.ifcx") if "schema" not in p.parts]
errs = 0; n = 0
for f in files:
    for node in json.loads(f.read_text())["data"]:
        for k, v in node.get("attributes", {}).items():
            if not k.startswith("opo::"): continue
            if k not in decl: print(f"{f}: {k} not declared"); errs += 1; continue
            v_ = Draft202012Validator(schemas[decl[k]["uri"]], registry=reg)
            n += 1
            for e in sorted(v_.iter_errors(v), key=lambda e: list(e.path))[:5]:
                errs += 1
                print(f"{f.relative_to(root)} {k} /{'/'.join(map(str, e.path))}: {e.message[:160]}")
print(f"{n} attributes checked in {len(files)} files, {errs} problem(s)")
sys.exit(1 if errs else 0)
