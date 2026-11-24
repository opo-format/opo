---
status: accepted
date: 2026-11-23
deciders: maintainer
---

# 0002. An .opo file is an IFCX document with an opo:: extension

## Context

OPO must complement the IFC family and be readable by IFC5 tools without conversion.

## Decision

An `.opo` is an IFCX document whose parametric content lives in attributes under the `opo::` namespace. Each OPO spec version pins one IFCX snapshot (OPO 0.1: IFCX alpha, IFC5-development commit `1a63082`) and follows new IFCX releases with an OPO update.

## Consequences

IFCX changes upstream never break existing files. `opo::` can later be proposed to buildingSMART as an official extension.
