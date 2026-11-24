# 7. IFC mapping

Because an `.opo` is already IFCX, IFC5 tools read its IFC data directly. For IFC4.3 (the current ISO standard, STEP files), OPO defines an export mapping:

- Instance → IfcProduct of the declared class (IfcDoor, IfcWindow, IfcStair…), with its type object from the variant.
- Representations → IFC shape representations with matching contexts (Body, Plan/Annotation, target scale).
- Geometry exported as exact IFC solids/profiles where possible (e.g. opening = extruded arbitrary closed profile).
- Parameters also written to a property set so other tools see the data and Curva can rebuild on re-import.
