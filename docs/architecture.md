# How the OPO project is organised

Three rules hold everything together (decisions 0013, 0016, 0017):

1. **One source of truth.** Every fact is written once, in one source file. Everything else (tables, coverage lists, previews, documentation pages, built `.opo` packages) is generated.
2. **Generated files are never edited or committed.** CI builds and publishes them. Pull requests contain only sources, so a human or an agent can review every line.
3. **Everything is checked.** A change is done when CI is green: schemas validate, conformance tests pass, objects build and check, generated outputs are reproducible.

## Layers and repositories

| Layer | Repository | Contains | Licence | Changes need |
|---|---|---|---|---|
| **Standard** | `opo-format/opo` | spec text, JSON Schemas (IFCX attributes and YAML source format), FEEL subset, conformance tests, decision records, proposals, glossary | CC-BY-4.0 (text), MIT OR Apache-2.0 (schemas, tests) | a proposal (normative) or a decision record; maintainer approval |
| **Implementation** | `opo-format/opo-rs` | Rust workspace: FEEL, recipe kernel, IFCX read/write/compose, build, check, render, template generator, `opo` CLI | MIT OR Apache-2.0 | green CI incl. the pinned conformance suite |
| **Library** | `opo-format/library` | object sources (YAML), archetypes and the per-class table, rule sets, materials and hatches, size catalogues, references registry | CC0-1.0 (objects), CC-BY-4.0 where a source requires it | green `opo check`; every sourced value has `source` + `status` |
| **Community** | `opo-format/.github` | organisation-wide CONTRIBUTING, code of conduct, security policy, issue and pull-request templates | CC0-1.0 | maintainer |
| **Website** (later) | `opo-format/website` | generated from the three repos above | — | — |

Dependency direction is one way: **library → opo-rs → opo**. Each repository pins the version it depends on:

- `opo-rs` pins a spec version and its conformance suite (a tagged release of `opo`).
- `library` pins an `opo` CLI version (a tagged release of `opo-rs`).
- Upgrading a pin is its own pull request, so a break is visible and reversible.

## What lives where (single-source map)

| Fact | Source of truth | Generated from it |
|---|---|---|
| What OPO is, normative rules | `opo/spec/` | website spec pages |
| Shape of `opo::` attributes | `opo/schema/` (JSON Schema + IFCX schema) | Rust types (checked against it), editor autocomplete |
| Shape of object sources | `opo/schema/source/` (JSON Schema for YAML) | editor autocomplete, `opo check` |
| FEEL behaviour | `opo/conformance/feel/` | — (opo-rs must pass) |
| Why something is as it is | `opo/decisions/` | decisions index |
| Proposed changes | `opo/proposals/` | proposals index with stages |
| IFC classes, predefined types, property sets | read at build time from buildingSMART's UML sources at the commit in library `ifc-version` (`opo ifc`; IFC is CC BY-ND 4.0, so nothing is committed) | class templates, coverage table |
| An object | `library/objects/<id>/` | `.opo` package, catalogue row, preview images, docs page |
| A class template | `library/templates/archetypes/*.yaml` + `library/templates/classes.yaml` | 150 template packages |
| Materials and hatches | `library/styles/` | embedded into each object at build |
| Rule sets | `library/rulesets/` | rule-set layers, docs tables |
| References (norms, sources) | `library/references.yaml` | citations in docs, `opo::object.references` |
| Plans, open tasks, status | GitHub issues and milestones | — (chat projects and notes only link here) |

## Target layout

```
opo/                                 the standard
├── spec/                            numbered chapters, one file each (01-scope.md …)
├── schema/                          opo@<version>.ifcx, JSON Schemas per opo:: attribute, source/ (YAML format)
├── conformance/                     feel/, recipe/, objects/ (input + expected output)
├── decisions/                       NNNN-title.md
├── proposals/                       NNNN-title.md with stage in front matter
├── docs/                            architecture, workflow, glossary, migration
├── AGENTS.md  CLAUDE.md  GOVERNANCE.md  CONTRIBUTING.md  CHANGELOG.md
└── LICENSES/  REUSE.toml            per-file licences (REUSE convention)

opo-rs/                              reference implementation
├── crates/opo-feel  opo-model  opo-recipe  opo-ifcx  opo-build  opo-check  opo-render  opo-cli
├── tests/                           runs opo/conformance at the pinned version
└── AGENTS.md  CLAUDE.md  justfile  CHANGELOG.md

library/                             objects
├── objects/<id>/                    object.yaml, layers/*.yaml, assets/
├── templates/                       archetypes/*.yaml, classes.yaml
├── rulesets/  styles/  ifc/         rule sets, materials + hatches, extracted IFC data
├── references.yaml                  every cited source, with licence and edition
├── opo-version                      pinned CLI version
└── AGENTS.md  CLAUDE.md  justfile  CHANGELOG.md
```

## Versions

- **Spec:** semantic versions (0.1, 0.2 … 1.0). Minor versions only add; files state their spec version.
- **Crates and CLI:** semantic versions, independent of the spec; each release states the spec versions it supports.
- **Objects:** each object has its own semantic version (`object.version`); a breaking parameter change is a major bump.
- **Library releases:** dated (e.g. `2027.03`), listing the objects and their versions.
- **Changelogs** are generated from commit messages (Conventional Commits).
