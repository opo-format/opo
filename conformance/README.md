# Conformance suite

Inputs and expected results that every OPO implementation must reproduce. `opo-rs` runs this suite at the spec version it supports; a second implementation passing it is required for OPO 1.0 (decision 0018).

The expected results were created once from the prototype interpreter and evaluator (retired in migration phase 5), reviewed, and are now the reference. CI runs the opo-rs tests at the commit in `opo-rs-version` against this suite. They are not regenerated: if an implementation disagrees, the case is examined and either the implementation or the case is fixed by a pull request labelled `conformance` and `normative`.

## FEEL — `feel/cases.json`

Each case: `id`, `expr`, optional `context` (names available to the expression), `expected` (JSON value; `null` for FEEL null), optional `note`.

- Numbers compare with an absolute tolerance of 1e-9 (spec §4.4: IEEE doubles, `=` within 1e-9). Lists and contexts compare element by element.
- Integer-valued results may be written as `7.0` or `7`; they are equal.

## Objects — `objects/*.json`

Each file names one fixture object (`object`, a folder relative to the file) and its cases. A case:

| Field | Meaning |
|---|---|
| `id` | case name |
| `values` | parameter values to set (on top of the object's defaults) |
| `inputs` | drawn inputs (slots) to set |
| `context` | host, level, view or rule-set context to set (e.g. `{"rules": {"accessibility": {…}}}`); defaults: host thickness 0.2 m, storey height 3.0 m, plan cut 1.2 m, no rule sets, each flip axis at its first value |
| `expected.derived` | every derived value, in order |
| `expected.checks` | every check: `true`, `false` or `null` |
| `expected.ifc_properties` | IFC properties written from formulas |
| `expected.quantities` | IFC base quantities written from formulas (`Qto_….Name`) |
| `expected.ports` | evaluated `nominal_size`, `position`, `direction` of each active port |
| `expected.steps` | FEEL expressions over the environment and the step results (`[{expr, expected}]`), for data steps such as a grid |
| `expected.geometry` | per representation (`model.medium`, `model.high`, and `void` for openings): for each item, the number of solids and their total volume (m³) |

Tolerances:
- derived values, checks, properties, quantities, ports: absolute 1e-9 (relative 1e-9 for values above 1);
- solid counts: exact;
- volumes: relative `tolerance` given per item — 1e-6 for items built only from straight edges, 0.03 for items that contain circles, arcs, cylinders, revolutions or nested objects (their volume depends on tessellation).

Cases cover: the defaults, every predefined type, every option of every choice parameter, every boolean flipped, every variant in the object's layer files, every rule set (alone and with each variant), and hand-picked cases (L-shaped walls, a slab with a hole, a sloped beam with extensions, a stair under a rule set, an arched opening, a slab opening).

## Fixtures

The fixture objects live in `fixtures/`, at the paths their ids name (`opo-format.org/<path>` resolves to `fixtures/<path>`). They are frozen copies of the prototype door and class templates; the maintained objects are in the library repository.

| File | Object | Cases |
|---|---|---|
| `door-single-swing.json` | `fixtures/examples/door/single-swing-door` | sizes for four markets × ISO 21542 / ADA rule sets |
| `template-*.json` | `fixtures/library/templates/<IfcClass>` | the nine class templates |
| `grid-stick-wall.json` | `fixtures/examples/grid/stick-wall` (with `mullion` and `panel`) | proposal 0001: default, joins, module, overrides, sloped face |

When objects move to the library repository (migration phase 4), the fixtures stay here as copies under `conformance/fixtures/`.
