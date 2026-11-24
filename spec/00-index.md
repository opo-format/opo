# OPO — Open Parametric Object

**Draft specification · v0.1 · 23 Nov 2026**
Status: strategy draft, not yet a specification. Decisions recorded in §11; everything else may still change.

OPO is an open, vendor-neutral file format for parametric architectural objects: doors, windows, stairs, railings, furniture and more. One OPO file is a *generator*: it describes how to build an object from parameters, with 3D at several levels of detail and proper 2D plan, elevation and section symbols at several scales.

Curva is the first application to implement OPO, but the format belongs to no single application.

- Name: OPO — Open Parametric Object (pronounced "oh-poh")
- File extension: `.opo`
- Home: github.com/opo-format · opo-format.org
- Schema addresses: `https://opo-format.org/schema/<version>/...`

## Chapters

1. [Goals](01-goals.md)
2. [Non-goals](02-non-goals.md)
3. [Core concepts](03-core-concepts.md)
4. [Anatomy of an `.opo` file](04-anatomy.md)
5. [Encoding and packaging](05-encoding-and-packaging.md)
6. [Versioning and compatibility](06-versioning.md)
7. [IFC mapping](07-ifc-mapping.md)
8. [Libraries and licensing](08-libraries-and-licensing.md)
9. [Repositories](09-repositories.md)
10. [Reference test objects (drive the spec)](10-reference-test-objects.md)
11. [Decisions](11-decisions.md)
12. [Open questions](12-open-questions.md)

## Conventions

The key words "must", "must not", "required", "shall", "shall not", "should", "should not", "recommended", "may" and "optional" in this specification are to be interpreted as described in BCP 14 (RFC 2119 and RFC 8174) when, and only when, they appear in bold or are written as part of a normative rule. The spec is still a draft; most text describes the intended design and will be tightened into normative rules chapter by chapter.

Section references such as §4.2 refer to the chapter number and the section within it.

