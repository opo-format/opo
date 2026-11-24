---
status: accepted
date: 2026-11-23
deciders: maintainer
---

# 0008. Library objects are based on open sources, IFC and published norms

## Context

We do not reinvent objects, and values must be traceable.

## Decision

Every library object names its parametric basis (openly licensed only), the IFC classes and properties it maps to, and the norms behind its sizes and rules, in `opo::object.references`. Sizes follow industry standards in metric and imperial.

## Consequences

Proprietary maker objects can inform dimensions but are never copied.
