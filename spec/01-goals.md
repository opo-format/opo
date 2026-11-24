# 1. Goals

1. **Objects that remember how they were made.** Change a parameter, redraw an outline, and the object rebuilds.
2. **Real architectural drawings.** Plan and elevation symbols follow drawing conventions by scale, not just slices of the 3D.
3. **Three levels of detail.** A door is a line and an arc at 1:200 and every layer of frame and leaf at 1:5.
4. **Adoptable by other software.** Small, strictly specified, text-based, openly licensed.
5. **IFC-native.** OPO complements the IFC family. An `.opo` is an IFCX document with an `opo::` extension: IFC vocabulary (classes, predefined types, property sets, representation contexts) used exactly, plus the recipe to rebuild the object. Exports clean IFC geometry (no meshes where exact geometry is possible). IFC5's first version leaves out parametric geometry; OPO fills that gap.
6. **Safe to open from anyone.** No object can touch files, the network or the computer.
