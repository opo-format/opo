"""Extract IFC 4.3 property and quantity set templates per element class.

Needs ifcopenshell (used only to read the buildingSMART templates). Only names, value
types, enumeration values and applicability are kept; descriptions are not copied.
Writes tools/ifc4x3_psets.json: {class: [{name, kind, generic, applies_to, props: [...]}, ...]}
"""
import json, sys
import ifcopenshell.util.pset as P

tree = json.load(open("tools/ifc4x3_add2_elements.json"))
classes = [n for d, n, a, p in tree if not a]
t = P.get_template("IFC4X3")
out = {}
for cls in classes:
    sets = []
    for ps in t.get_applicable(cls):
        ents = [e.strip() for e in (ps.ApplicableEntity or "").split(",") if e.strip()]
        mine = [e for e in ents if e.split("/")[0] in (cls, cls + "Type")]
        if not mine:
            continue  # inherited from a supertype (IfcElement, IfcProduct…): offered by name in the app, not per class
        applies = sorted({e.split("/")[1] for e in mine if "/" in e})
        props = []
        for p in ps.HasPropertyTemplates or []:
            d = {"name": p.Name, "template": p.TemplateType if hasattr(p, "TemplateType") else None,
                 "measure": getattr(p, "PrimaryMeasureType", None)}
            en = getattr(p, "Enumerators", None)
            if en:
                d["enum"] = [v.wrappedValue for v in en.EnumerationValues]
            props.append(d)
        sets.append({"name": ps.Name, "kind": "qto" if ps.Name.startswith("Qto_") else "pset",
                     "generic": len({e.split("/")[0].removesuffix("Type") for e in ents}) > 6,
                     "applies_to": applies, "props": props})
    out[cls] = sets
json.dump(out, open("tools/ifc4x3_psets.json", "w"), indent=0)
print(len(out), sum(len(v) for v in out.values()))
