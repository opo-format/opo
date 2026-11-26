---
status: accepted
date: 2026-11-26
deciders: maintainer
---

# 0028. A wall is one solid; its layers are drawn, not modelled

## Context

Implementing proposal 0004 raised how wall layers finish at openings (finishes and insulation turning into the reveal, cavity closers). Real practice varies by build-up, and Archicad keeps it in its doors and windows and mostly shows it in 2D only. The maintainer judged this too advanced for the current stage: the first goal is a working wall and door in Curva.

## Decision

- A wall is one closed solid in 3D at every level of detail.
- Its layers are shown by hatching where the wall is cut: in plans and sections, each layer's band hatched with its material. At low detail the wall is one solid fill.
- Openings cut the wall square. No layer turns into the reveal; `reveal` rules (proposal 0004) are deferred and are not used by objects or applications for now.
- Layers in 3D (real layer solids, reveal returns, closers) may come later, by proposal.

## Consequences

- The wall class template uses its one body solid for every 3D level; layer bands stay for drawings.
- The door drops its reveal rule.
- The reference implementation drops reveal handling and draws the wall as one solid in 3D and elevation, hatching layers only in cuts.
