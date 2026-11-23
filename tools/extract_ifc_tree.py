"""Extract the IfcElement class tree and predefined types from the IFC 4.3 schema.

Needs ifcopenshell (used here only as a schema reader; nothing from it is copied into OPO).
Writes tools/ifc4x3_add2_elements.json: [[depth, class, is_abstract, [predefined types] | null], ...]
"""
import json, sys
import ifcopenshell.ifcopenshell_wrapper as w

s = w.schema_by_name("IFC4X3_ADD2")
ents = {d.name(): d for d in s.declarations() if hasattr(d, "supertype")}
children = {}
for d in ents.values():
    st = d.supertype()
    if st:
        children.setdefault(st.name(), []).append(d.name())

def ptypes(n):
    try:
        return [x for x in s.declaration_by_name(n + "TypeEnum").enumeration_items() if x not in ("USERDEFINED", "NOTDEFINED")]
    except Exception:
        return None

out = []
def walk(n, depth):
    out.append([depth, n, ents[n].is_abstract(), ptypes(n)])
    for c in sorted(children.get(n, [])):
        walk(c, depth + 1)
walk("IfcElement", 0)
json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "tools/ifc4x3_add2_elements.json", "w"))
