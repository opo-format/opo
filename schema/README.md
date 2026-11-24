# Schemas

| File | What it defines |
|---|---|
| `opo@v0.1.ifcx` | IFCX schema declarations of every `opo::` attribute (imported by every OPO file) |
| `0.1/*.json` | JSON Schema (draft 2020-12) for each attribute, at `https://opo-format.org/schema/0.1/<name>.json` |
| `0.1/common.json` | Shared definitions: FEEL expressions, names, points, planes, line classes, levels of detail |

A file is valid when every `opo::` attribute validates against the schema named by its declaration (spec §5.1). Changing a schema is a normative change: it needs a proposal or decision record and the maintainer's approval (`AGENTS.md`).

## Source schemas (`source/0.1/`)

JSON Schemas for the YAML sources of the library (proposal 0002): `object.json` (object.yaml), `layer.json` (layers/*.yaml), `archetype.json` and `classes.json` (class templates), `references.json`, `materials.json` and `hatches.json` (registries). They check the structure of a source. After `opo build`, every compiled `opo::` attribute must also validate against `0.1/`. Sources are not part of a valid `.opo`; applications only read packages.
