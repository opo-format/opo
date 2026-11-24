---
status: accepted
date: 2026-11-24
deciders: maintainer
---

# 0001. Record decisions as numbered decision records

## Context

Decisions were kept in a table inside the spec outline, mixed with draft text. Humans and AI agents need one place to find what was decided, why, and what it replaced.

## Decision

Every decision that shapes the standard, the implementation or the library is a short Markdown file in `decisions/` of the standard repository, numbered `NNNN-title.md`, in the MADR (Markdown Any Decision Records) style: context, decision, consequences. Accepted records are never rewritten; a new record supersedes an old one and both link to each other.

## Consequences

The decisions table in the spec outline becomes a list of links. Agents read `decisions/` before proposing changes.
