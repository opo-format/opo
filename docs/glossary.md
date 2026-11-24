# Glossary

One meaning per word, used the same way in the spec, code, objects and conversations.

| Term | Meaning |
|---|---|
| **OPO** | Open Parametric Object, the format (say "oh-poh"). Write "OPO format" when the name alone is ambiguous. |
| **.opo / package** | A zip containing `object.ifcx`, optional `layers/` and `assets/`. |
| **Object** (definition) | One parametric generator, e.g. a single swing door. |
| **Source** | The YAML files an object is written in (`library/objects/<id>/`). Compiled into a package. |
| **Class template** | The generated object for one IFC class, built on an archetype; the starting point for library objects. |
| **Archetype** | One of eight geometric patterns templates are built on: point, linear, area, wall, hosted, flight, fitting, assembly. |
| **Library object** | A detailed object written from its sheet, refining a class template. |
| **Sheet** | The scope and specification part of an object (`sheet:` in `object.yaml`). |
| **Variant / type** | A named set of parameter values, e.g. "Concrete 200" wall type or "IPE 270". |
| **Size catalogue** | A layer of variants for one market or norm. |
| **System node** | The node in a size catalogue carrying that market's construction values; variants inherit it. |
| **Instance** | One placed object in a project file; not part of a package. |
| **Parameter** | A typed input value (length, choice, layers, property set…). |
| **Slot** | A drawn input (path, outline, boundary). |
| **Derived value** | A FEEL formula over parameters, slots and context. |
| **Check** | A FEEL condition with a severity and message. |
| **Rule set** | Swappable regional limits (stairs, accessibility…), switched on by a layer. |
| **Recipe** | The ordered geometry steps that build an object. |
| **Representation** | One drawable version of an object for a view and level of detail. |
| **LOD** | Level of detail: low (≤ 1:200), medium (1:100–1:50), high (≥ 1:20). |
| **Line class** | Semantic class of a 2D line: cut, projected, hidden, overhead, annotation. |
| **Hatch** | A fill pattern defined by line families, embedded in the object. |
| **Material** | Name, category, colour, cut hatch, surface pattern and data; embedded in the object. |
| **Port** | A connection point of a distribution element. |
| **Baked fallback** | Ready-made geometry for viewers that do not run recipes. |
| **Provenance** | `source` + `status` of a value (norm, maker, typical, illustrative, to_verify). |
| **Decision record** | A numbered file in `decisions/` recording one decision. |
| **Proposal** | A numbered file in `proposals/` changing the standard, moving through stages 0–3. |
| **Conformance suite** | Inputs and expected results every implementation must reproduce. |
