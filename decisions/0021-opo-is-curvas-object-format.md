---
status: accepted
date: 2026-11-26
deciders: maintainer
---

# 0021. OPO is Curva's object format

## Context

Curva's architecture (section 5b) planned its own smart-object file, `.curvaobj`, with logic written in Rhai or as WebAssembly modules. OPO was started as Curva's object format. Two formats would drift apart and split the library. The strategy review of 26 November 2026 asked the maintainer to choose.

## Options considered

- A: OPO is Curva's object format; `.curvaobj` is dropped.
- B: Curva keeps its own format and imports OPO.

## Decision

A. Curva adopts OPO for smart objects, and `.curvaobj` is cancelled. The Curva side records the same decision in its own repository.

`.curvaobj` was never specified beyond a few lines of Curva's architecture. Ideas kept from it: one definition with many placements, each with its own values; representations that may be generated, fixed (an imported model) or hand-drawn; downloaded objects must not be able to harm the user's computer. OPO meets the last one by construction: its formulas are a small FEEL subset with no loops, files or network.

## Consequences

- Curva's architecture section 5b and its risk table are updated in a Curva pull request.
- Objects made in Curva are saved as `.opo` and read by any OPO application, including the planned Rhino plug-in.
