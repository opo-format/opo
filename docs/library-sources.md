# Library source format (draft)

Objects are written in YAML and compiled by `opo build` into `.opo` packages (decision 0014). The JSON Schema for this format will live in `schema/source/`; this page is the working draft it is written from.

## One folder per object

```
objects/door-single-swing/
├── object.yaml          identity, scope, references, parameters, rules, recipe, representations, IFC mapping
├── layers/
│   ├── sizes-generic-metric.yaml
│   ├── sizes-uk-metric.yaml
│   ├── sizes-us.yaml
│   └── ruleset-iso-21542.yaml
├── assets/              previews made by hand, textures, maker geometry (optional)
└── CHANGELOG.md
```

- The folder name is the object id: lower case, words joined by hyphens, never reused.
- The **sheet** (scope, what the object is and is not, open questions) is part of `object.yaml`, so the catalogue and documentation are generated from it. There is no separate sheet file to keep in sync.
- Materials and hatches are referenced by id from `styles/`; `opo build` embeds them (decision 0011).

## Safe YAML

- No anchors, aliases, merge keys or custom tags.
- Formulas are always quoted strings: `"width - 2 * frame_width"`.
- Choices and text values that YAML could misread are quoted: `"no"`, `"on"`, `"1.0"`.
- `opo fmt` writes keys in a fixed order and normalises numbers, so diffs show only real changes.

## Values with provenance

A plain number is a design choice of the object author. A value taken from somewhere carries its source and status (decision 0017):

```yaml
handle_height:
  value: 1.0
  source: iso-21542-2021        # id in references.yaml
  status: norm                  # norm | maker | typical | illustrative | to_verify
  note: "Top of the 800–1000 mm range."
```

- `to_verify` needs a `note` saying what to check. CI lists all of them and blocks a `stable` object that has any.
- `typical` and `illustrative` values need a note on where the practice comes from.
- Every `source` id exists in `references.yaml`.

## References registry

```yaml
iso-21542-2021:
  title: "ISO 21542:2021 Building construction — Accessibility and usability of the built environment"
  kind: norm
  edition: 2021
  licence: proprietary (cited, not copied)
  url: https://www.iso.org/standard/71860.html
bim-all-doors:
  title: "dormakaba bim-all-doors"
  kind: parametric_basis
  version: "v1.90 (commit 9a174ae)"
  licence: CC0-1.0
  url: https://github.com/dormakaba/bim-all-doors
```

## Example (excerpt)

```yaml
id: door-single-swing
version: 0.3.0
status: draft
ifc: { class: IfcDoor, predefined_type: DOOR }
template: IfcDoor
sheet:
  scope: "Single swing door with frame, rebated or flush leaf, threshold, hinges and lever handle."
  not_in_scope: ["double doors", "sidelights", "closers and locks"]
references: [bim-all-doors, ifc-4.3-add2, iso-21542-2021, bs-4787]
parameters:
  nominal_width: { type: length, default: 0.9, label: "Nominal width", group: Size,
                   limits: { min: 0.4, max: 1.4, step: { metric: 0.01, imperial: 0.0127 } } }
rules:
  derived:
    clear_width: "rebate_width - 2 * stop_width"
  checks:
    - id: accessible_width
      expr: "rules.accessibility = null or usable_clear_width >= rules.accessibility.min_clear_width"
      severity: warning
      message: "Clear width below the active accessibility rule set."
```
