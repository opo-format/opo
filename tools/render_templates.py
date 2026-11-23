"""Preview images for class templates: 3D view and plan with hatches drawn from the objects' own
opo::materials / opo::hatches. Usage: python3 tools/render_templates.py [repo root] → library/templates/previews/
"""
import json, math, sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from shapely.geometry import LineString, Polygon
from shapely.affinity import rotate as srotate

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
sys.path.insert(0, str(ROOT / "tools"))
import recipe as RX  # noqa: E402
from check_opo import resolver  # noqa: E402

LIB = ROOT / "library/templates"
OUT = LIB / "previews"
STYLE = {"cut": dict(color="k", lw=0.9), "projected": dict(color="k", lw=0.5), "overhead": dict(color="k", lw=0.5, ls=(0, (4, 2))),
         "hidden": dict(color="k", lw=0.5, ls=(0, (2, 2))), "annotation": dict(color="#555", lw=0.4)}

def hatch_lines(poly, hatch, scale):
    """Clip a hatch definition (line families) to a polygon. Paper lengths are multiplied by the drawing scale."""
    if hatch.get("kind") != "lines": return []
    k = scale if hatch.get("scale_mode", "paper") == "paper" else 1.0
    minx, miny, maxx, maxy = poly.bounds
    R = math.hypot(maxx - minx, maxy - miny) + 1
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    segs = []
    for f in hatch["lines"]:
        a = math.radians(f["angle"])
        d = np.array([math.cos(a), math.sin(a)]); n = np.array([-math.sin(a), math.cos(a)])
        o = np.array(f.get("origin", [0, 0])) * k
        along, across = f["offset"][0] * k, f["offset"][1] * k
        if abs(across) < 1e-12: continue
        # index range of lines that can cross the polygon
        c_rel = np.array([cx, cy]) - o
        i0 = int(math.floor((np.dot(c_rel, n) - R) / across)); i1 = int(math.ceil((np.dot(c_rel, n) + R) / across))
        if i0 > i1: i0, i1 = i1, i0
        dashes = [x * k for x in f.get("dashes", [])]
        period = sum(abs(x) for x in dashes) if dashes else 0
        for i in range(i0, i1 + 1):
            base = o + i * (along * d + across * n)
            t_c = np.dot(np.array([cx, cy]) - base, d)
            t0, t1 = t_c - R, t_c + R
            if not dashes:
                pieces = [(t0, t1)]
            else:
                pieces = []
                start = math.floor(t0 / period) * period
                t = start
                while t < t1:
                    for x in dashes:
                        L = abs(x) if x != 0 else 0
                        if x > 0: pieces.append((t, t + L))
                        elif x == 0: pieces.append((t, t + 0.0004 * k))
                        t += L
            for a0, a1 in pieces:
                ls = LineString([tuple(base + a0 * d), tuple(base + a1 * d)])
                inter = ls.intersection(poly)
                for g in getattr(inter, "geoms", [inter]):
                    if g.geom_type == "LineString" and not g.is_empty: segs.append(np.array(g.coords))
    return segs

def draw_region(ax, shape, hatch, scale, line_style=None):
    for p in RX.polys(shape):
        if hatch and hatch.get("kind") == "solid":
            ax.fill(*p.exterior.xy, color=hatch.get("colour", "#333"), lw=0)
            for r in p.interiors: ax.fill(*r.xy, color="white", lw=0)
        elif hatch and hatch.get("kind") == "lines":
            for s in hatch_lines(p, hatch, scale): ax.plot(s[:, 0], s[:, 1], color=hatch.get("colour", "#222"), lw=0.35)
        if line_style:
            ax.plot(*p.exterior.xy, **line_style)
            for r in p.interiors: ax.plot(*r.xy, **line_style)

def plan(ax, T, env, geo, rep_id="plan.medium", scale=50):
    rep = next(r for r in T["opo::representations"] if r["id"] == rep_id)
    mats, hatches = T["opo::materials"], T["opo::hatches"]
    for it in rep.get("items", []):
        st = STYLE.get(it.get("class", "projected"), STYLE["projected"])
        if it.get("role") == "clearance": st = dict(color="#777", lw=0.4, ls=(0, (1, 2)))
        for g in RX.flat(geo.get(it["geometry"])):
            if g["kind"] == "region":
                h = None
                if it.get("hatch"):
                    m = RX.resolve_material({"material": it["hatch"]}, env, g)
                    h = hatches.get(mats.get(m, {}).get("cut", {}).get("hatch"))
                lw = dict(st); lw["lw"] = st["lw"] * (1.8 if it.get("role") == "outline" else 1)
                draw_region(ax, g["shape"], h, scale, lw)
            elif g["kind"] == "curve":
                p = np.array(g["points"]); ax.plot(p[:, 0], p[:, 1], **st)
            elif g["kind"] == "text":
                ax.text(g["at"][0], g["at"][1], g["value"], ha="center", va="center", fontsize=7)
    ax.set_aspect("equal"); ax.axis("off")

def model(ax, T, env, geo):
    rep = next(r for r in T["opo::representations"] if r["id"] == "model.medium")
    mats = T["opo::materials"]
    allp = []
    for it in rep["items"]:
        for g in RX.flat(geo.get(it["geometry"])):
            if g["kind"] != "solid": continue
            m = RX.resolve_material(it, env, g)
            col = mats.get(m, {}).get("colour", "#bbbbbb")
            P = np.asarray(g["points"]); F = np.asarray(g["faces"])
            ax.add_collection3d(Poly3DCollection(P[F], facecolor=col, edgecolor=(0, 0, 0, 0.15), lw=0.2))
            allp.append(P)
    if allp:
        P = np.vstack(allp); c = (P.max(0) + P.min(0)) / 2; r = (P.max(0) - P.min(0)).max() / 2 or 1
        ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(24, -58); ax.set_axis_off()

def template_previews():
    OUT.mkdir(parents=True, exist_ok=True)
    folders = sorted(p for p in LIB.iterdir() if (p / "object.ifcx").exists())
    fig = plt.figure(figsize=(12, 4.2 * math.ceil(len(folders) / 3)))
    for i, f in enumerate(folders):
        doc = json.loads((f / "object.ifcx").read_text())
        vals, ins = {}, {}
        if f.name == "IfcOpeningElement": vals = {"host_kind": "slab"}
        env, geo, T = RX.run(doc, values=vals, inputs=ins, base_dir=LIB, resolver=resolver)
        ax = fig.add_subplot(math.ceil(len(folders) / 3) * 2, 3, (i // 3) * 6 + i % 3 + 1, projection="3d")
        model(ax, T, env, geo)
        if f.name == "IfcOpeningElement":
            P = np.asarray(RX.flat(geo["void"])[0]["points"]); ax.add_collection3d(Poly3DCollection(P[np.asarray(RX.flat(geo["void"])[0]["faces"])], facecolor=(0.8, 0.2, 0.2, 0.25), edgecolor=(0.6, 0, 0, 0.4), lw=0.3))
            c = (P.max(0) + P.min(0)) / 2; r = (P.max(0) - P.min(0)).max() / 2
            ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
        ax.set_title(f"{f.name}  ·  {T['opo::object']['archetype']}", fontsize=9)
        ax2 = fig.add_subplot(math.ceil(len(folders) / 3) * 2, 3, (i // 3) * 6 + i % 3 + 4)
        plan(ax2, T, env, geo, "plan.medium", 50)
    fig.tight_layout()
    fig.savefig(OUT / "class-templates.png", dpi=110); plt.close(fig)

def wall_types_sheet():
    """Every example wall type in plan at 1:20 and 1:50, hatched only from the definitions inside the wall file."""
    f = LIB / "IfcWall"
    doc = json.loads((f / "object.ifcx").read_text())
    layer = json.loads((f / "layers/types-examples.ifcx").read_text())
    variants = [(n["attributes"]["bsi::ifc::prop::TypeName"], n["attributes"]["opo::values"]) for n in layer["data"] if "bsi::ifc::prop::TypeName" in n["attributes"]]
    variants = [("Template default", {})] + variants
    fig, axes = plt.subplots(len(variants), 1, figsize=(7.5, 1.45 * len(variants)))
    for ax, (name, vals) in zip(axes, variants):
        env, geo, T = RX.run(doc, values=vals, inputs={"path": [[0, 0], [1.2, 0]]})
        plan(ax, T, env, geo, "plan.medium", 20)
        mats = [l["material"] for l in env["layers"]]
        ax.set_title(f"{name}  —  {env['total_thickness'] * 1000:.0f} mm\n" + " | ".join(T["opo::materials"][m]["label"] for m in mats),
                     fontsize=6.5, loc="left")
    fig.tight_layout(); fig.savefig(OUT / "wall-types-hatches.png", dpi=150); plt.close(fig)

if __name__ == "__main__":
    template_previews(); wall_types_sheet()
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))
