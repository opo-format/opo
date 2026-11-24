---
status: accepted
date: 2026-11-23
deciders: maintainer
---

# 0006. 2D drawings use semantic line classes

## Context

Drawings must follow each office's standard without editing objects.

## Decision

2D items are classed (cut, projected, hidden, overhead, annotation); the application's drawing style maps classes to weights and line types.

## Consequences

Line weights are never stored in objects.
