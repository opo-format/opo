# Class templates

One OPO per IFC 4.3 element class (spec §4.16, `spec/objects/archetypes.md`). A class template is the starting point for any object of that class, like a Revit family template, and is itself a usable, shareable object.

**Generated — do not edit by hand.** Run `python3 tools/gen_templates.py`, then check with `python3 tools/check_opo.py` and render previews with `python3 tools/render_templates.py`. Generator inputs: `tools/ifc4x3_add2_elements.json` and `tools/ifc4x3_psets.json` (from the IFC 4.3 schema and property set templates, names only), `tools/templates/styles.py` (materials and hatches) and the archetype blocks in the generator.

| Template | Archetype | Example types (layers/) |
|---|---|---|
| [`IfcWall`](IfcWall/) | wall | 5 wall build-ups |
| [`IfcSlab`](IfcSlab/) | area | 3 slab build-ups |
| [`IfcBeam`](IfcBeam/) | linear | IPE 270, concrete 250 × 500, glulam 140 × 400 |
| [`IfcMember`](IfcMember/) | linear | — |
| [`IfcBoiler`](IfcBoiler/) | point (with ports) | — |
| [`IfcPipeFitting`](IfcPipeFitting/) | fitting | — |
| [`IfcOpeningElement`](IfcOpeningElement/) | hosted | — |
| [`IfcStair`](IfcStair/) | flight | — |
| [`IfcElementAssembly`](IfcElementAssembly/) | assembly (nests IfcMember) | — |

The other 141 classes follow from the same archetypes once the per-class defaults table exists.

**Materials and hatches travel with the object.** Each file embeds the materials it uses (`opo::materials`) and their hatch patterns (`opo::hatches`), so a wall type opened in another project or application draws with the same hatches. [`previews/wall-types-hatches.png`](previews/wall-types-hatches.png) is drawn only from the definitions inside `IfcWall`.

Example build-ups, profile sizes and equipment sizes are illustrative unless a source is named in the variant's note (e.g. IPE 270 from EN 10365:2017).

All files: CC0-1.0.
