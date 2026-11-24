---
status: accepted
date: 2026-11-23
deciders: maintainer
---

# 0003. Formulas use a FEEL subset

## Context

Objects need a small, safe, readable expression language with open implementations, from a neutral standards body. Google's CEL was rejected on principle.

## Decision

Formulas use a listed subset of FEEL (OMG DMN) plus OPO helpers: unit functions, trigonometry in degrees, list functions, contexts. The subset is defined in the spec and pinned by conformance tests.

## Consequences

Implementations may use any FEEL engine that passes the OPO conformance tests.
