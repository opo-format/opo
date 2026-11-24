# 5. Encoding and packaging

- **Structure: IFCX.** The object definition is an IFCX document. OPO's parametric content (parameters, input slots, rules, recipe, representations metadata, handles) lives in components under an `opo::` namespace, the way IFCX extensions work. Variants and product bindings are IFCX layers over the base. Goal: an `.opo` is instantly readable by IFC5 tools, and `opo::` can later be proposed to buildingSMART as an official extension.
- **IFCX tracking.** IFC5/IFCX is still alpha with no release date. Each OPO spec version pins a named IFCX snapshot, so upstream changes never break existing files. OPO follows each new IFCX release with a matching OPO update.
  - OPO 0.1 pins **IFCX alpha** (`ifcxVersion: "ifcx_alpha"`), as in buildingSMART/IFC5-development commit `1a63082` (8 Sep 2026), importing `ifc@v5a`, `prop@v5a` and `usd@v1`.

## 5.1 IFCX mapping

An IFCX file has a `header`, `imports` (schema URIs), `schemas` (new attribute definitions) and `data` (a flat list of nodes with `path`, `children`, `inherits`, `attributes`). Nodes with the same path in several layers are composed into one. OPO maps onto this as follows:

| OPO concept | IFCX |
|---|---|
| Definition | One **type node** with `bsi::ifc::class` (e.g. `IfcDoor`), plain `bsi::ifc::prop::*` values for the default variant, and all `opo::*` attributes |
| Parts (frame, leaf, void…) | `children` of the type node, carrying baked geometry |
| Variant | A node that `inherits` the type node and sets `opo::values` and its own `bsi::ifc::prop::TypeName` |
| Instance (in a project file) | A node that `inherits` a variant (or the type), with its own `opo::values`, `opo::inputs` (drawn geometry) and `usd::xformop` placement |
| Product binding, regional values | Layer files adding attributes to existing paths |
| Baked fallback | `usd::usdgeom::mesh` on part nodes (3D), `usd::usdgeom::basiscurves` on hidden 2D symbol nodes, both in metres |
| IFC data | `opo::ifc` maps FEEL expressions to `bsi::ifc::prop::*` names, so every instance writes correct IFC properties (e.g. OverallWidth, OperationType) |

`opo::*` attributes on the type node: `opo::object` (identity), `opo::parameters`, `opo::slots`, `opo::rules`, `opo::recipe`, `opo::representations`, `opo::host`, `opo::handles`, `opo::materials`, `opo::hatches`, `opo::ports`, `opo::ifc`. They are declared in `schema/opo@v<version>.ifcx`, imported by every OPO file.

IFCX alpha has only meshes and polylines, no exact solids. Exact geometry comes from the OPO recipe (used by OPO-aware tools and the IFC4.3 export); the baked mesh lets any IFC5 viewer display the object today.

## 5.2 Package layout (draft)

```
door.opo                (zip)
├── object.ifcx         base document: type node, opo:: definition, baked fallback
├── layers/*.ifcx       optional layers: variants, product bindings, regional values
└── assets/             optional: previews, textures, manufacturer geometry, WASM
```
Source repositories store the same structure unpacked as a folder.
- **Canonical encoding:** JSON, validated by a published JSON Schema at `https://opo-format.org/schema/<version>/`.
- **Packaging: always a zip.** Every `.opo` is a zip container (like `.3mf` or `.docx`) holding the IFCX/JSON document plus any previews, textures, manufacturer geometry or WASM module. One code path for all readers. For version control, the reference CLI packs and unpacks `.opo` files, and source repositories store objects unpacked as folders.
- Units: metres and degrees, as IFCX (see §4.2).
