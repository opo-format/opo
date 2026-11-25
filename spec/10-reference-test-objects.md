# 10. Reference test objects (drive the spec)

1. **Door** — parameters, rules, 3 LODs, plan symbols, host void, IFC mapping, references, generic metric / UK / US size catalogues *(written: library `objects/door-single-swing`; fixture `conformance/fixtures/examples/door/`)*
2. **Window with custom outline** — closed-profile input slot, driving/driven modes, clipped glazing grid (any window: outlines are editable on all windows)
3. **Straight / L / U stair** — level attachment, repeat, slab opening, nested railing, regional rule set
4. **Stair on a walkline with winders** — curve input, curve queries, WASM script step
5. **Branded product** — generic window + product binding + manufacturer geometry

The full list of planned objects (74 objects in eight families: openings, circulation, fixtures, furniture & equipment, shading devices, lifts & escalators, structure & coverings, MEP terminals & site), with one specification sheet per object and shared rule sets, is in the library repository (`objects/*/object.yaml`; see [`spec/objects/`](objects/README.md)). Test objects 1–4 are O-01, O-08 (with a custom outline; every window has an editable outline), C-01…C-03 and C-04 there.
