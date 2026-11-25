# OPO format — Open Parametric Object

OPO (pronounced "oh-poh", file extension `.opo`) is an open, vendor-neutral file format for **parametric architectural objects**: doors, windows, stairs, railings, furniture and more.

One `.opo` file is a *generator*. It describes how to build an object from parameters and drawn inputs, with:

- 3D geometry at three levels of detail,
- proper 2D plan, elevation and section symbols by drawing scale,
- IFC class, property sets and clean IFC export,
- baked fallback geometry, so simple tools can display objects without running the recipe.

An `.opo` is an IFCX (IFC5) document with an `opo::` extension, packaged as a zip. It uses IFC vocabulary exactly and adds the recipe to rebuild the object, filling the parametric gap IFC leaves open. Formulas use a subset of FEEL (OMG DMN). An optional sandboxed WebAssembly step covers rare, complex generators. No object can touch files, the network or the computer.

[Curva](https://github.com/curva3d) is the first application to implement OPO, but the format belongs to no single application. Anyone is welcome to implement it.

> **Status:** early draft. Nothing is final yet. See the [draft specification](spec/00-index.md).

## How the project is organised

One source of truth, everything else generated, everything checked: see [`docs/architecture.md`](docs/architecture.md), [`docs/workflow.md`](docs/workflow.md), [`decisions/`](decisions/README.md) and, for AI agents, [`AGENTS.md`](AGENTS.md). The repository is being split into `opo`, `opo-rs` and `library` ([`docs/migration.md`](docs/migration.md)).

## Repository contents

| Path | Contents |
|---|---|
| [`spec/`](spec/00-index.md) | Draft specification (v0.1), one file per chapter |
| [`spec/objects/`](spec/objects/README.md) | The archetypes of the class templates (150 IFC 4.3 element classes on nine archetypes), and where the catalogue, sheets, family rules and rule sets live in the library repository |
| [`schema/`](schema/) | `opo@v0.1.ifcx`: IFCX declaration of the `opo::` attributes (draft). Will be published at `https://opo-format.org/schema/<version>/` |
| [`conformance/`](conformance/README.md) | Conformance suite: FEEL and object cases, with fixture objects (the reference door and nine class templates, frozen) in `conformance/fixtures/` |
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
