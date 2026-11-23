# Shared rule sets

Rule sets hold regulation values that several objects check against. They ship as layer files and are **off by default**; a project switches on the ones that apply. Values below are taken from the listed sources (Nov 2026). Where a source gives a value in only one unit system, the other is a conversion and is marked ≈.

Rule-set ids used by the object sheets: `stairs`, `guards`, `handrails`, `accessibility`, `escape_windows`, `kitchen`.

---

## stairs

| Value | DE — DIN 18065 | UK — Approved Document K | US — IRC (dwellings) | US — IBC (other buildings) |
|---|---|---|---|---|
| Rise | 140–190 mm (necessary stair, multi-dwelling) | private 150–220; utility 150–190; general access 150–170 mm | ≤ 7¾" (196 mm) | 4"–7" |
| Going / tread | 260–370 mm (necessary stair, multi-dwelling) | private 220–300; utility 250–400; general access 250–400 mm | ≥ 10" with nosing (11" without) | ≥ 11" |
| Step rule | 2 s + a = 590–650 mm (required) | 550 ≤ 2R + G ≤ 700 mm | — | — |
| Pitch | — | private ≤ 42° | — | — |
| Clear width | ≥ 80 cm (dwellings ≤ 2 units), ≥ 100 cm other buildings | ≥ 800 mm (loft conversion guidance) | ≥ 36" | ≥ 44" |
| Headroom | — | — | ≥ 6'8" | ≥ 6'8" |
| Uniformity | — | uniform rises in a flight | ≤ ⅜" variation | ≤ ⅜" variation |
| Nosing | — | — | ¾"–1¼" | — |
| Winders | ≥ 50 mm going at the narrow end (dwellings ≤ 2 units) | — | ≥ 10" at 12" walkline, ≥ 6" at narrow end | — |
| Landing depth | ≥ 2.5 × going (dwellings), ≥ 3 × going (others) | — | — | — |
| Spiral | — | — | width ≥ 26", rise ≤ 9½", tread ≥ 7½" at 12" from narrow edge, headroom ≥ 6'6" | — |

Rule of thumb used as a default target: 17 / 29 cm satisfies all three German stair rules (step, comfort, safety).

## guards

| Value | DE — Landesbauordnungen | US — IBC | US — IRC | UK |
|---|---|---|---|---|
| Height | ≥ 90 cm up to 12 m fall height; ≥ 110 cm above 12 m (1000 mm in workplaces) | ≥ 42" (1067 mm) | ≥ 36" | (to add from AD K) |
| Guard on stair, top = handrail | — | 34"–38" in R-3 / dwelling units | 34"–38" | — |
| Openings | generally ≤ 12 cm between members | 4" sphere up to 36", 4⅜" from 36"–42" | 4" sphere; stair sides 4⅜"; stair triangle 6" | 100 mm sphere where children under 5 may use the building |

## handrails

| Value | DE (DIN 18040, ramps) | UK — AD K | US — IRC / ADA |
|---|---|---|---|
| Height | 85–90 cm | 900–1000 mm above pitch line or floor | 34"–38" above nosing line |
| Sides | both sides on ramps | both sides if stair ≥ 1000 mm wide | stairs with ≥ 4 risers: at least one side; ramps > 6" rise: both sides |
| Profile | Ø 30–45 mm | — | round Ø 1¼"–2" |
| Projection | — | — | ≤ 4½" into the stair |

## accessibility

| Value | DE — DIN 18040 | US — 2010 ADA Standards | UK — AD M |
|---|---|---|---|
| Door clear width | ≥ 900 mm clear passage | ≥ 32" with door open 90° | (to add) |
| Door hardware height | 85–105 cm | 34"–48" | (to add) |
| Ramp slope | ≤ 6 % | ≤ 1:12 (8.3 %); 1:10 for ≤ 6" rise, 1:8 for ≤ 3" rise (existing sites) | 1:20 for a going up to 10 m (500 mm rise); steeper for shorter goings per AD M table |
| Ramp run | ≤ 6 m, then landing ≥ 150 cm | ≤ 30" rise per run, landings ≥ 60" long | — |
| Ramp width | ≥ 120 cm | ≥ 36" between handrails | — |
| Ramp edge | wheel guards ≥ 10 cm | edge protection | — |
| Turning space | 150 × 150 cm before and after ramps, in front of WC | 60" × 60" landing at turns | — |
| WC | free space beside WC 90 × 70 cm | seat 17"–19"; centreline 16"–18" from side wall; clearance 60" wide × 56" deep (wall-hung) | — |
| Washbasin | height 80 cm, knee space 90 × 55 cm | rim ≤ 34", knee clearance ≥ 27" high | — |
| Urinal | — | rim ≤ 17" | — |

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

- DIN 18065 — weka.de/architekten-ingenieure/din-18065; tuvsud.com (Treppen/DIN 18065, Geländer, Brüstungen); baunetzwissen.de (Steigungsverhältnis, Auftritt, Stufen); heinze.de stair rules PDF
- Approved Document K — designingbuildings.co.uk/wiki/Stair_design; buildingcontrol.bathnes.gov.uk/node/47
- IRC R311.7 / R312, IBC 1011 / 1015 — municipal IRC handouts (Boulder, Boise, Knox County, Timnath, Stillwater, Des Moines, Dublin CA, Alameda); iccsafe.org guard commentary; viewrail.com IBC vs IRC
- Guards DE — tuvsud.com Geländer; baunetzwissen.de Absturzsicherung / Geländer
- DIN 18040 ramps — dguv.de / sifa.dguv.de Rampen; baunetzwissen.de Rampen; landtag.ltsh.de Maßstab table
- ADA — access-board.gov guides (ramps, toilet rooms, lavatories) and chapter 6
- AD M ramps — designingbuildings.co.uk/wiki/Ramps
- IRC R310 — municipal egress handouts (St Paul, Boise, Minnesota DLI, Lincoln NE)
- EN 1116 — catas.com UNI EN 1116 summary; standards.iteh.ai EN 1116:2018 abstract
- US kitchen cabinets — kraftmaid.com, angi.com, kitchencabinetkings.com, homedit.com
