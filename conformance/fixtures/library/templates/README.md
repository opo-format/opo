# Class template fixtures

Frozen copies of the nine prototype class templates, used by the conformance suite (`../../../objects/template-*.json`). They are not maintained here: the class templates are generated from their sources in the library repository (`templates/archetypes/*.yaml`, `templates/classes.yaml`) by `opo generate`.

| Template | Archetype |
|---|---|
| [`IfcWall`](IfcWall/) | wall |
| [`IfcSlab`](IfcSlab/) | area |
| [`IfcBeam`](IfcBeam/) | linear |
| [`IfcMember`](IfcMember/) | linear |
| [`IfcBoiler`](IfcBoiler/) | point (with ports) |
| [`IfcPipeFitting`](IfcPipeFitting/) | fitting |
| [`IfcOpeningElement`](IfcOpeningElement/) | hosted |
| [`IfcStair`](IfcStair/) | flight |
| [`IfcElementAssembly`](IfcElementAssembly/) | assembly (nests IfcMember) |
