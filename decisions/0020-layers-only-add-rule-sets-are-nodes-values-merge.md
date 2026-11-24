---
status: accepted
date: 2026-11-24
deciders: maintainer
---

# 0020. Layers only add; rule sets are their own nodes; values merge through inheritance

## Context

IFCX composes layers attribute by attribute: a later layer replaces a whole attribute. Two OPO patterns did not survive that (issue #9):

- The door's rule-set layers (`ruleset-iso-21542.ifcx`, `ruleset-us-ada.ifcx`) set `opo::rules` on the type node with only a `rulesets` entry. Composed with the base, they replaced the whole `opo::rules`, so the door lost its derived values and checks.
- Size variants inherit a system node, and both carry `opo::values` (spec §4.14). Pure IFCX inheritance lets the variant's `opo::values` replace the system's; the prototype and the conformance cases merge them key by key.

The spec also did not say in which order `layers/*.ifcx` apply.

## Options considered

- Rule sets as their own nodes with a new attribute `opo::ruleset`: layers only add nodes, so composition never overwrites. Needs a schema change.
- Merge `opo::rules.rulesets` by `id` across layers: keeps the files, but adds a merge rule IFCX does not have.

## Decision

1. A rule set is its own node carrying `opo::ruleset` (`id`, `label`, `uri`, `source`, `note`, `values`). The type node's `opo::rules.rulesets` only declares the rule sets the object reads (`id`, `default`, `note`, `fields`). The application picks at most one rule-set node per declared id.
2. `opo::values` merges key by key along `inherits`: a node's own keys win over inherited ones; a `null` key removes an inherited key; of several inherited nodes, the later one in `inherits` wins. All other attributes follow IFCX: the strongest whole value wins.
3. The layers of a package are independent: two layers must not set the same attribute of the same node. They may add nodes and add entries to `children` and `inherits`. Checking tools report overlaps.

## Consequences

The door's two rule-set layers are rewritten as rule-set nodes. `schema/0.1/ruleset.json` is added and declared in `schema/opo@v0.1.ifcx`. The prototype tools read rule sets from `opo::ruleset`. `opo-ifcx` already merges `opo::values` this way; `opo-model` gains the `opo::ruleset` type. The conformance cases do not change: they pass rule-set values through the case context.
