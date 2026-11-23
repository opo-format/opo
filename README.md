# OPO format — Open Parametric Object

OPO (pronounced "oh-poh", file extension `.opo`) is an open, vendor-neutral file format for **parametric architectural objects**: doors, windows, stairs, railings, furniture and more.

One `.opo` file is a *generator*. It describes how to build an object from parameters and drawn inputs, with:

- 3D geometry at three levels of detail,
- proper 2D plan, elevation and section symbols by drawing scale,
- IFC class, property sets and clean IFC export,
- baked fallback geometry, so simple tools can display objects without running the recipe.

Objects are data (JSON), with an optional sandboxed WebAssembly step for rare, complex generators. No object can touch files, the network or the computer.

[Curva](https://github.com/curva3d) is the first application to implement OPO, but the format belongs to no single application. Anyone is welcome to implement it.

> **Status:** early draft. Nothing is final yet. See the [spec outline](spec/OUTLINE.md).

## Repository contents

| Path | Contents |
|---|---|
| [`spec/OUTLINE.md`](spec/OUTLINE.md) | Draft spec outline (v0.0) |
| `schema/` *(planned)* | JSON Schema, published at `https://opo-format.org/schema/<version>/` |
| `crates/` *(planned)* | Rust reference reader and validator CLI |
| `examples/` *(planned)* | Reference test objects: door, window, stairs, branded product |

## Licences

| Part | Licence |
|---|---|
| Specification text and schema documentation | [CC-BY 4.0](LICENSE-CC-BY-4.0) |
| Reference code | [MIT](LICENSE-MIT) or [Apache-2.0](LICENSE-APACHE), at your option |

See [LICENSE](LICENSE) for details.

## Links

- Website: [opo-format.org](https://opo-format.org) *(coming)*
- Please call it the **OPO format** — opo.com and opo.org are unrelated.
