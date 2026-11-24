---
stage: 1          # 0 idea | 1 draft | 2 candidate | 3 final | withdrawn | rejected
issue: "#13"
spec_version: "0.2"
---

# 0002. YAML source format for objects, layers, styles and class templates

## Summary

Decision 0014 says objects are written in YAML and compiled to `.opo`; `docs/library-sources.md` sketches the format. This proposal fixes it so `opo build` and the library repository (migration phase 4) can be built. It covers:

1. **Object sources**: one folder per object (`object.yaml`, `layers/*.yaml`).
2. **Values with provenance** (decision 0017).
3. **Registries**: references, materials and hatches.
4. **Class templates**: archetypes and the per-class table, from which the class templates are generated (decision 0010).
5. **Compilation**: deterministic node ids, baked geometry, the golden test.

The source format is not part of what a valid `.opo` is. Applications only ever read `.opo` packages. It is still defined by a JSON Schema (`schema/source/0.1/`), so that sources are checked before they are built.

## Motivation

- The class template generator (opo-rs #6) needs archetype definitions and a per-class table as data, not as Python code (`tools/gen_templates.py`), so that the Rust generator and humans edit the same source.
- Phase 4 converts the door and the nine templates into library sources. `opo build` must then produce the files that exist today.
- Hand-written IFCX is long and noisy: node UUIDs, repeated material and hatch definitions, baked meshes. Authors and reviewers should only see what they decide.

## Design

### 1. Object sources

```
objects/<id>/
├── object.yaml
├── layers/<name>.yaml        size catalogues, type examples, rule sets, product bindings
├── assets/                   optional; copied into the package
└── CHANGELOG.md
```

`object.yaml` maps one to one onto the `opo::` attributes of the type node, with four simplifications:

| Source key | Compiles to | Simplification |
|---|---|---|
| `id`, `name`, `version`, `status`, `license`, `authors`, `description`, `tags`, `archetype`, `kind` | `opo::object` | `id` is the folder name; the package id is `opo-format.org/<repository path>`; `license` defaults to `CC0-1.0`; `status` (draft, candidate, stable, decision 0018) is source-only |
| `sheet: {scope, not_in_scope, open_questions}` | nothing | source-only; the catalogue and docs are generated from it |
| `references: [{ref, role, used}]` | `opo::object.references` | `ref` is an id in `references.yaml`; its name, licence, URI and version are filled in |
| `parameters: {<name>: {...}}` | `opo::parameters` | **a map by name**, in file order; the name is the key |
| `slots`, `rules.derived`, `rules.checks`, `rules.rulesets`, `recipe`, `representations` | the matching attributes | **maps by name or id**, in file order; `derived: {name: "expr"}` or `{name: {expr, note}}` |
| `materials: [<id>]` | `opo::materials`, `opo::hatches` | ids in `styles/materials.yaml`; each material's hatches come from `styles/hatches.yaml`; materials used by parameter defaults and layers are added automatically |
| `host`, `handles`, `ports`, `ifc` | as written | `ifc.class` also writes `bsi::ifc::class` with its buildingSMART URI |

`name` also writes `bsi::ifc::prop::Name` and `bsi::ifc::prop::TypeName` on the type node; an optional `type_name` sets a different TypeName.

**Plain IFC values** (`bsi::ifc::prop::<Attribute>`, e.g. OverallWidth) are not written in sources. `opo build` computes them from the `opo::ifc.properties` formulas with those keys: at the defaults for the type node, and with each variant's values for its node. A variant may still give plain values under `ifc:`; they override the computed ones.

Layer files:

```yaml
# layers/sizes-us.yaml
kind: sizes                    # sizes | types | ruleset | binding
system:                        # optional: values every variant inherits
  name: "US doors (prehung, flush leaf 1-3/8 in)"
  values: {nominal_reference: leaf, frame_type: lining, lining_thickness: 0.01905}
variants:
  - name: "US 3'0\" × 6'8\" leaf"
    values: {nominal_width: 0.9144, nominal_height: 2.032}
    ifc: {OverallWidth: 0.9875, OverallHeight: 2.0669}     # plain bsi::ifc::prop values
```

```yaml
# layers/ruleset-iso-21542.yaml
kind: ruleset
id: accessibility
label: "ISO 21542:2021"
uri: https://opo-format.org/rulesets/accessibility/iso-21542-2021@0.1
source: "ISO 21542:2021 door criteria: …"
values: {min_clear_width: "mm(800)", handle_min: "mm(800)", handle_max: "mm(1000)"}
```

A `sizes` or `types` file compiles to one system node that inherits the type node, plus one variant node per entry that inherits the system node (spec §4.14). A `ruleset` file compiles to one `opo::ruleset` node (decision 0020). A `binding` file adds attributes to the type node.

### 2. Values with provenance

Anywhere a number, string or list is expected, a source may write a provenance object instead:

```yaml
handle_height:
  type: length
  default: {value: 1.0, source: iso-21542-2021, status: norm, note: "Top of the 800–1000 mm range."}
```

- `status`: `norm` | `maker` | `typical` | `illustrative` | `to_verify` (decision 0017).
- `source` is an id in `references.yaml`; required for `norm` and `maker`.
- `to_verify`, `typical` and `illustrative` need a `note`.
- `opo build` writes the plain value, and the provenance into `opo::provenance` on the same node (see Resolved).
- `opo check --sources` lists every `to_verify` value and fails a `stable` object that has any.

### 3. Registries

```
references.yaml        id → {title, kind, edition | version, licence, url}
styles/hatches.yaml    id → an opo::hatches entry
styles/materials.yaml  id → an opo::materials entry (its cut / surface name hatch ids)
```

Registries live in the library repository. Objects refer to registry entries by id and never copy them; `opo build` embeds what an object uses (decision 0011).

### 4. Class templates

```
templates/
├── archetypes/<archetype>.yaml    point, linear, area, wall, hosted, flight, fitting, assembly
└── classes.yaml                   one entry per IFC class (the per-class table)
```

An **archetype file** is an object source without identity. It carries:
- the parameters, slots, rules, recipe, representations, host, handles and material slots shared by every class on that archetype;
- `ifc.properties` and `ifc.quantities` formulas, by property or quantity name; a formula applies wherever the class has that property.

A **class entry** names the class and its archetype, and refines the archetype:

```yaml
IfcBoiler:
  archetype: point
  name: "Boiler (class template)"
  description: "…"
  default_type: WATER
  parameters: {width: {default: 0.45}, depth: {default: 0.35}, height: {default: 0.75}, symbol: {default: "BLR"}}
  materials: [painted_steel]
  ports: [...]
  ifc: {properties: {Pset_BoilerTypeCommon.WaterStorageCapacity: "…"}}
  references: [...]
```

Merging rules:
- Class parameters override archetype parameters key by key; new names are appended.
- Lists (`ports`, `references`, `materials`) are appended.
- Maps of formulas (`ifc.properties`, `ifc.quantities`) are merged by key.

The generator then adds what comes from IFC (`library/ifc/`, extracted from the pinned IFC release):
- the `predefined_type` choice (every value of `<Class>TypeEnum`, plus USERDEFINED and NOTDEFINED) and `object_type`;
- one `property_set` parameter per applicable property set, with `visible` following its applicable predefined types, `optional` when the set is generic, and `value` formulas taken from `ifc.properties`;
- the `Qto_` sets as `ifc.quantities`, with formulas from the archetype or the class and every other quantity listed under `from_geometry`;
- `opo::object` (`kind: class_template`, IFC and generator references).

The result is an ordinary object source, compiled like any other.

### 5. Compilation

- **Node ids** are UUID v5 in the namespace `6f706f2d-666f-726d-6174-2e6f72670000` (as today):
  - type node: `<path>/type`;
  - layer nodes: `<path>/layers/<file>.ifcx/system` and `<path>/layers/<file>.ifcx/<variant name>`;
  - rule-set node: `<path>/layers/<file>.ifcx/ruleset`;
  - baked nodes as `opo bake` (`<path>/baked/<representation>/<item>/<n>`).
- **Published ids never change.** Project files refer to variants by id, so renaming a variant must not change its id. A system, variant or rule-set entry may therefore give `node: <uuid>`, which is used instead of the generated id. `opo export` writes `node:` wherever an existing id differs from the generated one.
- **Baked geometry** is always generated by `opo build`, never written by hand (decision 0016).
- **Output** is `object.ifcx` and `layers/*.ifcx` in the repository JSON layout, or a `.opo` package.
- **Golden test** (phase 4): `opo build` of the converted door and nine templates gives the same `opo::` attributes and plain IFC values as today's files. Baked meshes are compared as point sets, as `opo check` does.

## Drawbacks

- A second format to learn and keep in step with the attribute schemas. Mitigation: the source schema is generated from the attribute schemas plus the four simplifications, so a new attribute appears in both.
- Maps by name rely on YAML keeping key order. Every YAML parser `opo` uses must do so; `opo fmt` writes a fixed order.

## Alternatives considered

- **Write IFCX JSON by hand.** Rejected (decision 0014): UUIDs, baked meshes and copied styles make review impossible.
- **Lists everywhere, exactly as the attributes.** Simpler mapping, but every entry repeats `name:` / `id:`, and merging an archetype with a class entry needs lookups by name anyway.
- **Templates as Rust code.** Rejected: humans and the generator must edit the same data; the per-class table is meant to be hand-edited (decision 0010).

## Conformance tests

- Source schema: valid and invalid examples per key.
- `opo build` golden test on the door and nine templates (phase 4).
- Generator: archetypes plus `classes.yaml` give today's nine templates.

## Open questions

None at this stage.

## Resolved

- **Provenance in packages** (maintainer, 24 Nov 2026): carried into the `.opo` as an optional attribute `opo::provenance` on the node whose value it describes: a map from a value path (`parameters.handle_height.default`, `values.nominal_width`, `ruleset.values.min_clear_width`) to `{source, status, note}`. Users of a library object can see which values are still `to_verify`.
- **Registries** (maintainer, 24 Nov 2026): `references.yaml` and `styles/` live at the root of the library repository.
