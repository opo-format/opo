---
status: accepted
date: 2026-11-23
deciders: maintainer
---

# 0004. Every .opo is a zip package

## Context

Objects can carry previews, textures, manufacturer geometry and WebAssembly modules.

## Decision

An `.opo` is always a zip (`object.ifcx`, `layers/`, `assets/`). Sources are stored unpacked; the CLI packs and unpacks.

## Consequences

One code path for readers.
