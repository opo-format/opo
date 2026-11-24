# IFC coverage — moved

Every IFC 4.3 element class (150) has a class template. The coverage table — each class with its archetype, template, predefined types and library objects — is generated in the library repository by `opo coverage` (`just check` writes `build/coverage.md`; CI publishes it as the `tables` artifact). The per-class table it is built from is the library's `templates/classes.yaml`.

Not covered: abstract classes (they cannot be instantiated), spatial elements (sites, buildings, storeys, spaces: project structure, not objects), annotations, grids and alignments, and type-only entities.

This note only points there (decision 0016: generated tables are not committed).
