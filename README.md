# OPO format — Open Parametric Object

OPO (pronounced "oh-poh", file extension `.opo`) is an open, vendor-neutral file format for **parametric architectural objects**: doors, windows, stairs, railings, furniture and more.

One `.opo` file is a *generator*. It describes how to build an object from parameters and drawn inputs, with:

- 3D geometry at three levels of detail,
- proper 2D plan, elevation and section symbols by drawing scale,
- IFC class, property sets and clean IFC export,
- baked fallback geometry, so simple tools can display objects without running the recipe.

An `.opo` is an IFCX (IFC5) document with an `opo::` extension, packaged as a zip. It uses IFC vocabulary exactly and adds the recipe to rebuild the object, filling the parametric gap IFC leaves open. Formulas use a subset of FEEL (OMG DMN). An optional sandboxed WebAssembly step covers rare, complex generators. No object can touch files, the network or the computer.

[Curva](https://github.com/curva3d) is the first application to implement OPO, but the format belongs to no single application. Anyone is welcome to implement it.

> **Status:** early draft. Nothing is final yet. See the [spec outline](spec/OUTLINE.md).

## Repository contents

| Path | Contents |
|---|---|
| [`spec/OUTLINE.md`](spec/OUTLINE.md) | Draft spec outline (v0.1), with recorded decisions in §11 |
| [`spec/objects/`](spec/objects/README.md) | Object catalogue: 74 planned objects in eight families with one specification sheet each, and shared rule sets (stairs, guards, accessibility, escape windows, kitchens) |
| [`schema/`](schema/) | `opo@v0.1.ifcx`: IFCX declaration of the `opo::` attributes (draft). Will be published at `https://opo-format.org/schema/<version>/` |
| [`examples/door/`](examples/door/) | Reference test object #1: single swing door as IFCX, based on dormakaba bim-all-doors (CC0), with generic metric, UK and US size catalogues and accessibility rule sets |
| `crates/` *(planned)* | Rust reference reader and validator CLI |

## Licences

| Part | Licence |
|---|---|
| Specification text and schema documentation | [CC-BY 4.0](LICENSE-CC-BY-4.0) |
| Reference code | [MIT](LICENSE-MIT) or [Apache-2.0](LICENSE-APACHE), at your option |

See [LICENSE](LICENSE) for details.

## Links

- Website: [opo-format.org](https://opo-format.org) *(coming)*
- Please call it the **OPO format** — opo.com and opo.org are unrelated.
