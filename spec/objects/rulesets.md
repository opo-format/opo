# Shared rule sets

Rule sets hold regulation values that several objects check against. They ship as layer files and are **off by default**; a project switches on the ones that apply. Values below are taken from the listed sources (Nov 2026). Where a source gives a value in only one unit system, the other is a conversion and is marked ≈.

**Markets.** Europe uses **EN and ISO norms only**; national norms (DIN, NF, UNE, NEN…) are left out. Where no EN/ISO norm sets a value, the EU column says so and the object falls back to project values. The UK (Approved Documents) and the US (IRC, IBC, ADA) are separate markets with their own columns.

Rule-set ids used by the object sheets: `stairs`, `guards`, `handrails`, `accessibility`, `escape_windows`, `kitchen`.

---

## stairs

| Value | EU — EN/ISO | UK — Approved Document K | US — IRC (dwellings) | US — IBC (other buildings) |
|---|---|---|---|---|
| Rise | no norm | private 150–220; utility 150–190; general access 150–170 mm | ≤ 7¾" (196 mm) | 4"–7" |
| Going / tread | no norm | private 220–300; utility 250–400; general access 250–400 mm | ≥ 10" with nosing (11" without) | ≥ 11" |
| Step rule | no norm | 550 ≤ 2R + G ≤ 700 mm | — | — |
| Pitch | no norm | private ≤ 42° | — | — |
| Clear width | no norm | ≥ 800 mm (loft conversion guidance) | ≥ 36" | ≥ 44" |
| Headroom | no norm | — | ≥ 6'8" | ≥ 6'8" |
| Uniformity | no norm | uniform rises in a flight | ≤ ⅜" variation | ≤ ⅜" variation |
| Nosing | no norm | — | ¾"–1¼" | — |
| Winders | no norm | — | ≥ 10" at 12" walkline, ≥ 6" at narrow end | — |
| Spiral | no norm | — | width ≥ 26", rise ≤ 9½", tread ≥ 7½" at 12" from narrow edge, headroom ≥ 6'6" | — |

There is no EN or ISO norm for stair geometry (EN 15644 covers prefabricated solid-wood stairs as products only). In the EU the `stairs` rule set is empty; projects add their national values as their own rule set layer. The generic metric preset is 175 / 280 mm (2R + G = 630 mm, the classic step formula), which is not a norm value.

## guards

| Value | EU — EN/ISO | US — IBC | US — IRC | UK |
|---|---|---|---|---|
| Where required | ISO 21542: along paths, ramps and stairs where the drop is > 600 mm | — | — | — |
| Height | no EN/ISO value *(ISO 21542 to verify)* | ≥ 42" (1067 mm) | ≥ 36" | (to add from AD K) |
| Guard on stair, top = handrail | — | 34"–38" in R-3 / dwelling units | 34"–38" | — |
| Openings | no EN/ISO value | 4" sphere up to 36", 4⅜" from 36"–42" | 4" sphere; stair sides 4⅜"; stair triangle 6" | 100 mm sphere where children under 5 may use the building |

Guard loads come from EN 1991-1-1 (structural, outside OPO's checks).

## handrails

| Value | EU — ISO 21542:2021 | UK — AD K | US — IRC / ADA |
|---|---|---|---|
| Height | top 850–1000 mm; second, lower rail 600–750 mm | 900–1000 mm above pitch line or floor | 34"–38" above nosing line |
| Sides | both sides on ramps and stairs *(to verify)* | both sides if stair ≥ 1000 mm wide | stairs with ≥ 4 risers: at least one side; ramps > 6" rise: both sides |
| Profile | *(to verify)* | — | round Ø 1¼"–2" |
| Projection | — | — | ≤ 4½" into the stair |

## accessibility

| Value | EU — ISO 21542:2021 | US — 2010 ADA Standards | UK — AD M |
|---|---|---|---|
| Door clear width | ≥ 800 mm clear opening (850 mm recommended), measured with the door open | ≥ 32" with door open 90° | (to add) |
| Door clear height | ≥ 2000 mm | — | — |
| Threshold | ≤ 20 mm | ≤ ½" | — |
| Door hardware height | 800–1000 mm | 34"–48" | (to add) |
| Controls and switches | 800–1100 mm | — | — |
| Ramp slope | *(to verify)* | ≤ 1:12 (8.3 %); 1:10 for ≤ 6" rise, 1:8 for ≤ 3" rise (existing sites) | 1:20 for a going up to 10 m (500 mm rise); steeper for shorter goings per AD M table |
| Ramp run | *(to verify)* | ≤ 30" rise per run, landings ≥ 60" long | — |
| Ramp width | ≥ 1000 mm clear between handrails | ≥ 36" between handrails | — |
| Turning space | *(to verify)* | 60" × 60" landing at turns | — |
| WC | *(to verify)* | seat 17"–19"; centreline 16"–18" from side wall; clearance 60" wide × 56" deep (wall-hung) | — |
| Washbasin | *(to verify)* | rim ≤ 34", knee clearance ≥ 27" high | — |
| Urinal | — | rim ≤ 17" | — |

EN 17210:2021 is the EU accessibility standard, but it states functional requirements only; its numeric guidance is in CEN/TR 17621 (a technical report, not requirements). A revision with requirements and recommendations (prEN 17210:2025) is in progress; when it is published the EU column moves to it. Until then OPO uses ISO 21542 for EU numbers.

## escape_windows

| Value | US — IRC R310 |
|---|---|
| Net clear opening | ≥ 5.7 ft² (0.53 m²); ≥ 5.0 ft² at grade floor |
| Net clear height | ≥ 24" |
| Net clear width | ≥ 20" |
| Sill height | ≤ 44" above floor |

Window objects compute their net clear opening from the open sash, so this check works for casement, hung and sliding windows alike.

## kitchen

| Value | EU — EN 1116:2018 | US — industry practice |
|---|---|---|
| Worktop height | 850, 900 or 950 mm (+0/+50) | 36" finished (34½" cabinet + 1½" top) |
| Worktop depth | ≥ 600 mm; front overhang ≤ 30 mm | 25"–26" over 24" cabinets |
| Base unit depth | ≥ 550 mm under a 600 mm worktop | 24" |
| Wall unit depth | 310–400 mm total | 12" (24" over fridges) |
| Worktop to wall unit | ≥ 450 mm | 18" |
| Plinth / toe kick | ≥ 80 mm | ~4"–4½" |
| Built-under recess height | ≥ 820, 870 or 920 mm | — |
| Unit widths | nominal 400, 500, 600, 900 mm for appliance housings (others in 100 / 150 mm steps by maker) | 9"–48" in 3" steps |
| Wall unit heights | by maker | 30", 36", 42" |
| Tall unit heights | by maker | 84", 90", 96" |

---

## Sources

- ISO 21542:2021 — accessibility summaries of the door, handrail, ramp-width, guarding and control criteria; EN 17210:2021, CEN/TR 17621, prEN 17210:2025 — CEN catalogue pages
- Approved Document K — designingbuildings.co.uk/wiki/Stair_design; buildingcontrol.bathnes.gov.uk/node/47
- IRC R311.7 / R312, IBC 1011 / 1015 — municipal IRC handouts (Boulder, Boise, Knox County, Timnath, Stillwater, Des Moines, Dublin CA, Alameda); iccsafe.org guard commentary; viewrail.com IBC vs IRC
- ADA — access-board.gov guides (ramps, toilet rooms, lavatories) and chapter 6
- AD M ramps — designingbuildings.co.uk/wiki/Ramps
- IRC R310 — municipal egress handouts (St Paul, Boise, Minnesota DLI, Lincoln NE)
- EN 1116 — catas.com UNI EN 1116 summary; standards.iteh.ai EN 1116:2018 abstract
- US kitchen cabinets — kraftmaid.com, angi.com, kitchencabinetkings.com, homedit.com
