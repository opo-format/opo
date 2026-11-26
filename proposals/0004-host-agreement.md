---
stage: 2          # 0 idea | 1 draft | 2 candidate | 3 final | withdrawn | rejected
issue: "#NN"
spec_version: "0.2"
---

# 0004. Host agreement: what a wall gives a door, and what a door gives back

## Summary

Today a door only asks its wall for one number, `host.thickness`, and gives back one solid, `void`. That is too thin for a real wall with layers: the door cannot sit on the right layer, cannot tell inside from outside, and the wall cannot draw its layers neatly round the opening. This proposal fixes the agreement between a host (wall) and a hosted object (door, window, opening) in both directions, so any application placing an OPO door in an OPO wall gets the same result.

## Motivation

A door in a 300 mm external wall (render, 200 mm block, insulation, plasterboard):

- the frame should sit against the core, not centred on the wall axis;
- the swing side and the elevation (decision 0024: seen from outside) need to know which face is outside;
- the plan should show the finish layers returning into the reveal, not cut off square;
- the application needs to know where the head is, to place a lintel later.

None of this can be expressed now. Each application would guess, and Curva and the Rhino plug-in would draw different doors.

## Design

### 1. What the host provides (`opo::host.provides` on the wall)

A wall type declares these values, evaluated at the insertion point. The names are fixed by the spec so every hosted object can rely on them.

| Name | Type | Meaning |
|---|---|---|
| `thickness` | length | Total wall thickness. |
| `face_front` | length | Offset of the front face from the wall's location line, along +y (positive). |
| `face_back` | length | Offset of the back face, along −y (positive number). |
| `exterior` | choice `front` / `back` / `none` | Which face is outside. `none` for internal walls. |
| `layers` | layers | The build-up from front to back (the order IFC uses with AXIS2 and NEGATIVE sense): `thickness`, `material`, `function` (`structure`, `insulation`, `finish`, `membrane`, `air`, `other`). |
| `core_front`, `core_back` | length | Offsets of the faces of the structural core (the `structure` layers). |
| `base` | length | Height of the wall's base above the level, at the insertion point. |
| `height` | length | Wall height at the insertion point (top minus base). |

A hosted object reads them as `host.<name>`. Values it does not use are ignored. An application that places a hosted object in something that is not an OPO wall supplies what it can and leaves the rest at the hosted object's defaults (as `host.thickness` works today).

### 2. What the hosted object asks for (`opo::host.inputs`)

Unchanged in form; the `from` text becomes one of the names above (`from: thickness`) instead of free text, so a checker can verify it.

### 3. Where the hosted object sits (`opo::host.seat`)

New. Says which plane of the wall the object's y = 0 lines up with:

- `axis` — the location line (today's behaviour, the default);
- `core_front`, `core_back`, `core_centre` — a face or the centre of the core;
- `face_front`, `face_back` — a finished face;
- plus an optional `offset` (FEEL length, along +y).

Example: a door with its frame against the front of the core: `seat: {to: core_front, offset: "-frame_depth"}`.

### 4. What the hosted object gives back

- `void` (unchanged): the solid cut from the host.
- `reveal` (new, optional): how the host's layers finish at the sides and head of the void, as a list of rules by layer `function`:
  - `return` — the layer turns into the reveal up to a given plane (e.g. finishes return to the frame);
  - `stop` — the layer stops square at the void (default for all layers);
  - the plane is one of the seat names above or `frame` (a FEEL expression giving the y of the frame face).
- `head` (new, optional): a FEEL point list for the head line of the opening (top of the structural opening), so the application or a lintel object can find it.
- `sill` (new, optional): the same for the bottom line, for windows.

The host applies the void and the reveal to its own geometry and drawings. The hosted object never draws the host's layers.

### 5. Who draws what

- The **wall** draws its own layers, with the void cut out and the reveal rules applied, in plan, section and 3D.
- The **door** draws only itself: frame, leaf, swing, symbols.
- The **application** places the door, passes the host values in, and asks the wall to rebuild with the door's void and reveal.

## Drawbacks

- Wall types must declare more values. The wall class template generates them from its `layers`, so authors rarely write them by hand.
- Reveal rules are a small new language. They are kept to two words (`return`, `stop`) on purpose.

## Alternatives considered

- **Pass the whole wall to the door.** Simple, but every door would need wall logic, and two doors could treat the same wall differently.
- **Let the application decide reveals.** Then Curva and Rhino would draw them differently, which is what OPO exists to avoid.

## Conformance tests

- A fixture wall (300 mm, four layers, exterior `front`) and the fixture door seated at `core_front`: the door's frame sits at the expected y; the evaluated `host.*` values match.
- The wall's derived plan with the door: finish layers return to the frame on both sides; the core stops square.
- The door's elevation is drawn as seen from the `exterior` face.
- A door placed in a non-OPO host with only `thickness`: falls back to `axis` seating and the defaults.

## Open questions

- Should `reveal` rules also cover the head (a finish returning under a lintel), or only the sides for now?
- Curved walls: `face_front` and `face_back` are offsets along the local normal at the insertion point; is that enough for a door in a curved wall, or does the door need the curve?
