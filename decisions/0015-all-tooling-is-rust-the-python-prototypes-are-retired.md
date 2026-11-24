---
status: accepted
date: 2026-11-24
deciders: maintainer
---

# 0015. All tooling is Rust; the Python prototypes are retired

## Context

The project is Rust-only, and Curva must reuse the same code. The Python prototypes (FEEL interpreter, recipe evaluator, generator, checker) proved the design.

## Decision

`opo-rs` implements FEEL, the recipe kernel, IFCX read/write/compose, build, check, render and the template generator. The Python results become test fixtures; the scripts are deleted once the Rust CLI reproduces them.

## Consequences

One implementation to maintain; conformance tests guard behaviour.
