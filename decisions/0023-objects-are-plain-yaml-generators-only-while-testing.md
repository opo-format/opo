---
status: accepted
date: 2026-11-26
deciders: maintainer
---

# 0023. Objects are plain YAML with shared building blocks; generator scripts only while testing

## Context

Most library objects were produced by helper scripts kept outside the repositories. That breaks decision 0016 (one source of truth) and decision 0015 (all tooling is Rust).

## Options considered

- A: plain YAML, with shared building blocks kept in the library, and no hidden scripts.
- B: keep generator scripts and commit them.
- C: a Rust authoring tool.

## Decision

A. Objects are written as plain YAML that anyone can read, reusing shared building blocks from the library. During the current testing phase (wall and door first), helper scripts may still be used outside the repositories. Once wall and door work in Curva, everything moves into the repositories and the scripts are retired.

## Consequences

- The YAML source format gains the shared building blocks the objects need (proposal 0002 or a follow-up).
- Wall and door are written this way first, and become the pattern for the other objects.
