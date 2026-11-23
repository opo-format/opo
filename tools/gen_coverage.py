"""Generate spec/objects/ifc-coverage.md. Usage: python3 tools/gen_coverage.py <repo root>"""
import json, re, glob, sys
root = sys.argv[1] if len(sys.argv) > 1 else '.'
t = json.load(open(f'{root}/tools/ifc4x3_add2_elements.json'))
# parent branch for each class
branch = {}; stack = []
for d, n, a, p in t:
    stack = stack[:d] + [n]
    branch[n] = stack[1] if len(stack) > 1 else n
    if len(stack) > 2 and stack[1] == 'IfcDistributionElement': branch[n] = stack[2]
    if len(stack) > 3 and stack[2] == 'IfcDistributionFlowElement': branch[n] = stack[3]
A = {}
def put(arch, names):
    for x in names.split(): A[x] = arch
put('point', 'IfcBearing IfcBuildingElementProxy IfcFooting IfcMooringDevice IfcNavigationElement IfcDiscreteAccessory IfcFastener IfcImpactProtectionDevice IfcMechanicalFastener IfcSign IfcVibrationDamper IfcVibrationIsolator IfcTendonAnchor IfcFurniture IfcSystemFurnitureElement IfcGeographicElement IfcTransportElement IfcVehicle IfcBuildingElementPart IfcJunctionBox IfcDistributionChamberElement IfcCivilElement IfcBorehole')
put('linear', 'IfcBeam IfcColumn IfcMember IfcPile IfcCaissonFoundation IfcRail IfcKerb IfcRailing IfcTrackElement IfcReinforcingBar IfcTendon IfcTendonConduit IfcCableSegment IfcCableCarrierSegment IfcDuctSegment IfcPipeSegment IfcConveyorSegment')
put('area', 'IfcSlab IfcRoof IfcCovering IfcPavement IfcCourse IfcPlate IfcEarthworksFill IfcReinforcedSoil IfcReinforcingMesh IfcGeotechnicalStratum IfcGeomodel IfcGeoslice IfcVirtualElement')
put('wall', 'IfcWall IfcWallStandardCase IfcCurtainWall IfcChimney')
put('hosted', 'IfcDoor IfcWindow IfcShadingDevice IfcOpeningElement IfcVoidingFeature IfcProjectionElement IfcSurfaceFeature IfcEarthworksCut')
put('flight', 'IfcStair IfcStairFlight IfcRamp IfcRampFlight')
put('fitting', 'IfcCableCarrierFitting IfcCableFitting IfcDuctFitting IfcPipeFitting')
put('assembly', 'IfcElementAssembly')
put('any', 'IfcBuiltElement IfcBuildingElementProxy IfcCivilElement')
put('point', 'IfcDistributionElement IfcFurnishingElement')
put('linear', 'IfcDeepFoundation IfcFlowSegment')
put('area', 'IfcEarthworksElement')
put('fitting', 'IfcFlowFitting')
EQUIP_BRANCHES = {'IfcDistributionControlElement','IfcEnergyConversionDevice','IfcFlowController','IfcFlowMovingDevice','IfcFlowStorageDevice','IfcFlowTerminal','IfcFlowTreatmentDevice','IfcDistributionFlowElement'}
txt = {f: open(f).read() for f in glob.glob(f'{root}/spec/objects/*.md') if not f.endswith(('ifc-coverage.md','archetypes.md'))}
idre = re.compile(r'^## ([A-Z]-\d\d) ', re.M)
def sheets_for(n):
    hits = []
    for f, s in txt.items():
        parts = re.split(r'^(?=## [A-Z]-\d\d )', s, flags=re.M)
        for part in parts:
            m = idre.match(part)
            if m and re.search(r'\b' + n + r'\b', part.split('\n**Based on**')[0]):
                hits.append(m.group(1))
    return sorted(set(hits))
FAM = [('IfcBuiltElement','Built elements'),('IfcDistributionControlElement','Distribution: control (sensors, actuators, alarms)'),
       ('IfcEnergyConversionDevice','Distribution: energy conversion (plant)'),('IfcFlowController','Distribution: flow controllers'),
       ('IfcFlowFitting','Distribution: fittings'),('IfcFlowMovingDevice','Distribution: pumps, fans, compressors'),('IfcFlowSegment','Distribution: segments (pipes, ducts, cables)'),
       ('IfcFlowStorageDevice','Distribution: storage'),('IfcFlowTerminal','Distribution: terminals'),('IfcFlowTreatmentDevice','Distribution: treatment'),
       ('IfcDistributionChamberElement','Distribution: chambers'),('IfcElementComponent','Components'),('IfcFeatureElement','Features (voids, projections, surface treatments)'),
       ('IfcFurnishingElement','Furnishing'),('IfcGeographicElement','Geographic'),('IfcGeotechnicalElement','Geotechnical'),('IfcTransportationDevice','Transportation devices'),
       ('IfcCivilElement','Other'),('IfcElementAssembly','Other'),('IfcVirtualElement','Other')]
rows = {}; total = 0; covered = 0; ptotal = 0; nbuilt = [0]
from pathlib import Path
for d, n, a, p in t:
    if a: continue
    b = branch[n]
    arch = A.get(n) or ('point' if b in EQUIP_BRANCHES else '?')
    sh = sheets_for(n)
    note = ''
    if n == 'IfcWallStandardCase': note = 'deprecated in IFC 4.3; exported as IfcWall'
    if n in ('IfcFlowController','IfcFlowTerminal','IfcDistributionFlowElement','IfcDistributionControlElement','IfcEnergyConversionDevice','IfcFlowFitting','IfcFlowMovingDevice','IfcFlowSegment','IfcFlowStorageDevice','IfcFlowTreatmentDevice','IfcDistributionElement','IfcBuiltElement','IfcDeepFoundation','IfcEarthworksElement','IfcFurnishingElement','IfcCivilElement'):
        note = 'generic supertype; template for elements with no specific class'
    fam = next((lbl for key, lbl in FAM if key == b), 'Other')
    total += 1; ptotal += len(p or [])
    if sh: covered += 1
    pt = ', '.join(p) if p else '—'
    built = "✅" if (Path(root) / "library/templates" / n / "object.ifcx").exists() else "planned"
    if built == "✅": nbuilt[0] += 1
    rows.setdefault(fam, []).append(f"| `{n}` | {arch} | {built} | {len(p or [])} | {pt} | {', '.join(sh) if sh else '—'} | {note} |")
out = [f"""# IFC coverage — every IFC 4.3 element class has an OPO

**Draft v0.1 · 24 Nov 2026** · generated from the IFC 4.3 schema (ifcopenshell `IFC4X3_ADD2`) by `tools/gen_coverage.py`; do not edit the tables by hand.

**Goal.** Every IFC element type can be created parametrically in an OPO application and shared as a file, the way a Revit family is shared. That includes elements that Revit handles as non-shareable "system families" (walls, slabs, roofs, stairs, pipes, ducts): in OPO they are ordinary objects.

**How:** two tiers (spec §4.16).
1. **Class template** — one OPO per IFC class ({total} classes). Built on one of eight geometric **archetypes** (`archetypes.md`). It carries the class, every predefined type as a choice, the matching IFC property sets as parameters, ports for distribution elements, and a usable shape at three levels of detail. Templates are generated from the IFC schema, the IFC property set templates and a small hand-written per-class table, so they follow IFC releases.
2. **Library objects** — detailed objects with proper construction logic and drawing conventions, written from their sheets (`README.md`, {covered} classes have at least one sheet today). A library object is a refined template: same class, same IFC data.

Anyone (a firm, a manufacturer, Curva Pro) makes their own objects by starting from a template or a library object, the way a Revit user starts from a family template.

**Counts:** {total} concrete element classes · {ptotal} predefined types · {covered} classes with a detailed sheet · {total - covered} classes covered by their template only (for now) · class templates built: NBUILT.

Archetypes (`any` = the user picks one, for generic classes such as `IfcBuildingElementProxy`): **point** (placed equipment or component, optionally hosted, with ports) · **linear** (profile along a path) · **area** (boundary + thickness or layer build-up) · **wall** (path + height + layers or grid) · **hosted** (sits in or on a host and cuts or adds to it) · **flight** (level to level: stairs, ramps) · **fitting** (joins the ends of segments) · **assembly** (nests other OPOs).

Not covered: abstract classes (they cannot be instantiated), spatial elements (sites, buildings, storeys, spaces: project structure, not objects), annotations, grids and alignments, and type-only entities.
"""]
for key, lbl in FAM:
    if lbl in rows and rows[lbl] is not None:
        out.append(f"\n## {lbl}\n\n| Class | Archetype | Types | Predefined types | Detailed sheets | Note |\n|---|---|---|---|---|---|\n" + '\n'.join(rows[lbl]))
        rows[lbl] = None
open(f'{root}/spec/objects/ifc-coverage.md', 'w').write('\n'.join(out).replace('NBUILT', str(nbuilt[0])) + '\n')
print(total, covered, ptotal, [n for d,n,a,p in t if not a and (A.get(n) or ('point' if branch[n] in EQUIP_BRANCHES else '?'))=='?'])
