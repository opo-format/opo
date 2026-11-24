---
status: accepted
date: 2026-11-24
deciders: maintainer
---

# 0014. Objects are written in YAML and compiled to .opo

## Context

Objects were Python code or large generated JSON; neither is reviewable or editable by non-programmers.

## Decision

Each object is a folder of YAML source files validated by a published JSON Schema. `opo build` compiles sources to IFCX/.opo with baked geometry. YAML is restricted to a safe subset (no anchors or tags, quoted strings where ambiguous) and formatted by the CLI.

## Consequences

The YAML schema becomes part of the standard repository; editors autocomplete from it.
