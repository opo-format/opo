"""Reference evaluator for OPO recipes (spec §4.5). Prototype: runs a recipe for given values and returns geometry.

Geometry values:
  region  {"kind": "region", "plane", "shape": shapely geometry in plane coordinates}
  curve   {"kind": "curve", "plane", "points": [[u, v], ...]}   (2D)   or  {"kind": "curve3", "points": [[x, y, z], ...]}
  solid   {"kind": "solid", "points": [[x, y, z]...], "faces": [[i, j, k]...]}
  text    {"kind": "text", "plane", "at": [u, v], "value", "height"}
Lists of geometry are allowed anywhere; None means "nothing" (a step whose `when` is false).
Planes: xy (plan, extrusion along +z), xz (face, +y), yz (side, +x).
3D unions are mesh concatenations (no CSG); 2D unions/differences are exact (shapely).
"""
import json, math
from pathlib import Path
import numpy as np
import mapbox_earcut as earcut
from shapely.geometry import Polygon, MultiPolygon, LineString, Point
from shapely.ops import unary_union
from feel import feel, BUILTINS

# ------------------------------------------------------------------ helpers
def to3(plane, u, v, w):
    if plane == "xy": return [u, v, w]
    if plane == "xz": return [u, w, v]
    if plane == "yz": return [w, u, v]
    raise ValueError(plane)

def polys(shape):
    if shape is None or shape.is_empty: return []
    if isinstance(shape, Polygon): return [shape]
    if isinstance(shape, MultiPolygon): return list(shape.geoms)
    return [g for g in getattr(shape, "geoms", []) if isinstance(g, Polygon)]

def solid(points, faces):
    """Closed mesh with outward faces: a negative signed volume (mirrored mapping) flips every face."""
    P = np.asarray(points, float); F = np.asarray(faces, int)
    if len(F) and np.einsum("ij,ij->i", P[F[:, 0]], np.cross(P[F[:, 1]], P[F[:, 2]])).sum() < 0:
        F = F[:, [0, 2, 1]]
    return {"kind": "solid", "points": [[float(c) for c in p] for p in P], "faces": [list(map(int, f)) for f in F]}

def triangulate(poly):
    """Earcut triangles, all counter-clockwise, for a polygon oriented exterior CCW / holes CW."""
    from shapely.geometry.polygon import orient
    poly = orient(poly, 1.0)
    rings = [np.asarray(poly.exterior.coords[:-1], dtype=np.float64)] + [np.asarray(r.coords[:-1], dtype=np.float64) for r in poly.interiors]
    verts = np.vstack(rings)
    ends = np.cumsum([len(r) for r in rings]).astype(np.uint32)
    tri = earcut.triangulate_float64(verts, ends).reshape(-1, 3)
    a, b, c = verts[tri[:, 0]], verts[tri[:, 1]], verts[tri[:, 2]]
    cw = ((b[:, 0] - a[:, 0]) * (c[:, 1] - a[:, 1]) - (b[:, 1] - a[:, 1]) * (c[:, 0] - a[:, 0])) < 0
    tri[cw] = tri[cw][:, [0, 2, 1]]
    return verts, tri, rings

def flat(x):
    if x is None: return []
    if isinstance(x, list):
        out = []
        for y in x: out.extend(flat(y))
        return out
    return [x]

# ------------------------------------------------------------------ 2D operations
def op_rectangle(plane, min, max):
    (x0, y0), (x1, y1) = min, max
    return {"kind": "region", "plane": plane, "shape": Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])}

def op_polygon(plane, points):
    return {"kind": "region", "plane": plane, "shape": Polygon([tuple(p[:2]) for p in points]).buffer(0)}

def op_circle(plane, center, radius, segments=48):
    return {"kind": "region", "plane": plane, "shape": Point(center[0], center[1]).buffer(radius, quad_segs=max(4, segments // 4))}

def op_polyline(plane, points):
    return {"kind": "curve", "plane": plane, "points": [list(map(float, p[:2])) for p in points]}

def op_line(plane, start, end):
    return op_polyline(plane, [start, end])

def op_arc(plane, center, radius, start_angle, end_angle, segments=32):
    n = max(2, int(segments * abs(end_angle - start_angle) / 360) + 2)
    pts = [[center[0] + radius * math.cos(math.radians(a)), center[1] + radius * math.sin(math.radians(a))]
           for a in np.linspace(start_angle, end_angle, n)]
    return {"kind": "curve", "plane": plane, "points": pts}

def op_band(plane, path, left, right):
    """Region between two offsets of an open 2D path (positive = left of the direction of travel). Mitred joins."""
    pts = path["points"] if isinstance(path, dict) else path
    ls = LineString([tuple(p[:2]) for p in pts])
    def off(d):
        if abs(d) < 1e-12: return list(ls.coords)
        c = ls.offset_curve(d, join_style="mitre", mitre_limit=10.0)
        return list(c.coords)
    a, b = off(left), off(right)
    return {"kind": "region", "plane": plane, "shape": Polygon(a + b[::-1]).buffer(0)}

def op_difference(plane, a, b):
    sa = unary_union([g["shape"] for g in flat(a)])
    sb = unary_union([g["shape"] for g in flat(b)]) if flat(b) else None
    return {"kind": "region", "plane": flat(a)[0]["plane"], "shape": sa if sb is None else sa.difference(sb)}

def op_outline(plane, region):
    """Boundary curves of a region (for drawing)."""
    out = []
    for g in flat(region):
        for p in polys(g["shape"]):
            for r in [p.exterior] + list(p.interiors):
                out.append({"kind": "curve", "plane": g["plane"], "points": [list(c) for c in r.coords]})
    return out

def op_text(plane, at, value, height=0.0025):
    return {"kind": "text", "plane": plane, "at": list(at[:2]), "value": str(value), "height": height}

# ------------------------------------------------------------------ 3D operations
def op_extrude(plane, profile, **kw):
    lo, hi = kw["from"], kw["to"]
    out = []
    for g in flat(profile):
        for p in polys(g["shape"]):
            verts, tri, rings = triangulate(p)
            pts = [to3(g["plane"], u, v, lo) for u, v in verts] + [to3(g["plane"], u, v, hi) for u, v in verts]
            n = len(verts)
            faces = [[a, c, b] for a, b, c in tri] + [[a + n, b + n, c + n] for a, b, c in tri]
            start = 0
            for r in rings:
                m = len(r)
                for i in range(m):
                    a, b = start + i, start + (i + 1) % m
                    faces += [[a, b, b + n], [a, b + n, a + n]]
                start += m
            out.append(solid(pts, faces))
    return out

def frame(d):
    d = np.asarray(d, float); d /= np.linalg.norm(d)
    up = np.array([0, 0, 1.0]) if abs(d[2]) < 0.99 else np.array([1.0, 0, 0])
    across = np.cross(up, d); across /= np.linalg.norm(across)
    vert = np.cross(d, across)
    return d, across, vert

def op_sweep(plane, profile, path, roll=0):
    """Sweep a profile (drawn in its own u = across, v = up plane) along a straight-segment 3D path.
    Segments are extruded one by one (mitres are approximated)."""
    pts = [np.asarray(p, float) for p in (path["points"] if isinstance(path, dict) else path)]
    out = []
    for p0, p1 in zip(pts[:-1], pts[1:]):
        L = np.linalg.norm(p1 - p0)
        if L < 1e-9: continue
        d, across, vert = frame(p1 - p0)
        cr, sr = math.cos(math.radians(roll)), math.sin(math.radians(roll))
        a2, v2 = across * cr + vert * sr, -across * sr + vert * cr
        for g in flat(profile):
            for poly in polys(g["shape"]):
                verts, tri, rings = triangulate(poly)
                base = [p0 + a2 * u + v2 * v for u, v in verts]
                top = [b + d * L for b in base]
                n = len(verts)
                faces = [[a, c, b] for a, b, c in tri] + [[a + n, b + n, c + n] for a, b, c in tri]
                start = 0
                for r in rings:
                    m = len(r)
                    for i in range(m):
                        a, b = start + i, start + (i + 1) % m
                        faces += [[a, b, b + n], [a, b + n, a + n]]
                    start += m
                out.append(solid(base + top, faces))
    return out

def op_revolve(plane, profile, center, axis, angle, segments=24):
    """Revolve a profile region (in `plane`, local coordinates) about an axis through `center` (3D)."""
    c = np.asarray(center, float); k = np.asarray(axis, float); k /= np.linalg.norm(k)
    def rot(p, a):
        a = math.radians(a); p = np.asarray(p, float) - c
        return c + p * math.cos(a) + np.cross(k, p) * math.sin(a) + k * np.dot(k, p) * (1 - math.cos(a))
    n_steps = max(2, int(segments * abs(angle) / 360) + 1)
    out = []
    for g in flat(profile):
        for poly in polys(g["shape"]):
            from shapely.geometry.polygon import orient
            ring = list(orient(poly, 1.0).exterior.coords[:-1])
            m = len(ring)
            pts, faces = [], []
            for s in range(n_steps + 1):
                a = angle * s / n_steps
                pts += [rot(to3(g["plane"], u, v, 0.0), a) for u, v in ring]
            for s in range(n_steps):
                for i in range(m):
                    a0, b0 = s * m + i, s * m + (i + 1) % m
                    faces += [[a0, b0, b0 + m], [a0, b0 + m, a0 + m]]
            verts, tri, _ = triangulate(Polygon(ring))
            last = n_steps * m
            faces += [[a, c2, b] for a, b, c2 in tri] + [[a + last, b + last, c2 + last] for a, b, c2 in tri]
            out.append(solid(pts, faces))
    return out

def op_box(plane, min, max):
    return op_extrude("xy", op_rectangle("xy", min[:2], max[:2]), **{"from": min[2], "to": max[2]})

def op_cylinder(plane, start, end, radius, segments=24):
    return op_sweep("yz", op_circle("yz", [0, 0], radius, segments), [start, end])

def _xform(g, f):
    if g is None: return None
    if isinstance(g, list): return [_xform(x, f) for x in g]
    g = dict(g)
    if g["kind"] == "solid": g["points"] = [list(f(np.asarray(p, float))) for p in g["points"]]
    elif g["kind"] == "curve3": g["points"] = [list(f(np.asarray(p, float))) for p in g["points"]]
    else: raise ValueError("3D transform on 2D geometry")
    return g

def _xform2(g, f):
    if g is None: return None
    if isinstance(g, list): return [_xform2(x, f) for x in g]
    from shapely import affinity
    g = dict(g)
    if g["kind"] == "region": g["shape"] = f(g["shape"], affinity)
    elif g["kind"] == "curve":
        ls = f(LineString(g["points"]), affinity); g["points"] = [list(c) for c in ls.coords]
    elif g["kind"] == "text":
        p = f(Point(*g["at"]), affinity); g["at"] = [p.x, p.y]
    return g

def op_move(plane, geometry, by):
    if len(by) == 2: return _xform2(geometry, lambda s, A: A.translate(s, by[0], by[1]))
    return _xform(geometry, lambda p: p + np.asarray(by, float))

def op_rotate(plane, geometry, center, angle):
    if len(center) == 2: return _xform2(geometry, lambda s, A: A.rotate(s, angle, origin=tuple(center)))
    c = np.asarray(center, float); a = math.radians(angle)
    R = np.array([[math.cos(a), -math.sin(a), 0], [math.sin(a), math.cos(a), 0], [0, 0, 1]])
    return _xform(geometry, lambda p: c + R @ (p - c))

def op_mirror(plane, geometry, axis):
    sx, sy = (-1, 1) if axis == "x" else (1, -1)
    def f3(p): q = p.copy(); q[0 if axis == "x" else 1] *= -1; return q
    def flipfaces(g):
        if isinstance(g, list): return [flipfaces(x) for x in g]
        if g and g["kind"] == "solid": g["faces"] = [[a, c, b] for a, b, c in g["faces"]]
        return g
    if any(g["kind"] in ("region", "curve", "text") for g in flat(geometry)):
        return _xform2(geometry, lambda s, A: A.scale(s, sx, sy, origin=(0, 0)))
    return flipfaces(_xform(geometry, f3))

def op_union(plane, items):
    items = flat(items)
    if items and all(g["kind"] == "region" for g in items) and len({g["plane"] for g in items}) == 1:
        return {"kind": "region", "plane": items[0]["plane"], "shape": unary_union([g["shape"] for g in items])}
    return items

def op_path3(plane, points):
    return {"kind": "curve3", "points": [[float(c) for c in p] for p in points]}

OPS = {"rectangle": op_rectangle, "polygon": op_polygon, "circle": op_circle, "polyline": op_polyline, "line": op_line,
       "arc": op_arc, "band": op_band, "difference": op_difference, "boundary_curves": op_outline, "text": op_text,
       "extrude": op_extrude, "sweep": op_sweep, "revolve": op_revolve, "box": op_box, "cylinder": op_cylinder,
       "move": op_move, "rotate": op_rotate, "mirror": op_mirror, "union": op_union, "path3": op_path3}
SPECIAL = {"for_each", "instance"}  # arguments evaluated lazily

# ------------------------------------------------------------------ running an object
def type_node(doc):
    return next(n for n in doc["data"] if "opo::object" in n.get("attributes", {}))["attributes"]

def environment(T, values=None, inputs=None, context=None):
    env = {}
    for p in T["opo::parameters"]:
        env[p["name"]] = p.get("default")
    for s in T.get("opo::slots", []) or []:
        env[s["name"]] = s.get("default")
    env.update(values or {}); env.update(inputs or {})
    host_defaults = {k: v.get("default") for k, v in ((T.get("opo::host") or {}).get("inputs") or {}).items()}
    ctx = {"host": {"thickness": 0.2, "y_min": -0.1, "y_max": 0.1, "bottom": 0.0, "top": 3.0, **host_defaults}, "level": {"elevation": 0.0, "height": 3.0},
           "view": {"cut_height": 1.2}, "rules": {}}
    for k, v in (context or {}).items():
        ctx[k] = {**ctx.get(k, {}), **v} if isinstance(v, dict) else v
    env.update(ctx)
    for d in T["opo::rules"].get("derived", []):
        env[d["name"]] = feel(d["expr"], env)
    return env

def bind_ops(plane, env, base_dir):
    def mk(name, f):
        def call(*args, **kw):
            import inspect
            params = [p for p in inspect.signature(f).parameters if p not in ("plane", "kw")]
            kw2 = dict(zip(params, args)); kw2.update(kw)
            if name == "extrude" and len(args) >= 3: kw2 = {"profile": args[0], "from": args[1], "to": args[2]}
            return f(plane, **kw2)
        return call
    return {n: mk(n, f) for n, f in OPS.items()}

def run(doc, values=None, inputs=None, context=None, base_dir=None, resolver=None, depth=0):
    """Run an object's recipe. `resolver(object_id) -> folder` finds nested objects (spec §4.9)."""
    if depth > 8: raise RecursionError("nesting too deep")
    T = type_node(doc)
    env = environment(T, values, inputs, context)
    geo = {}

    def instance(object_id, vals=None, ins=None, representation="model.medium"):
        folder = resolver(object_id) if resolver else None
        if folder is None: raise FileNotFoundError(f"cannot resolve nested object {object_id}")
        sub = json.loads((Path(folder) / "object.ifcx").read_text())
        sub_env, sub_geo, subT = run(sub, vals or {}, ins or {}, context, folder, resolver, depth + 1)
        rep = next(r for r in subT["opo::representations"] if r["id"] == representation)
        parts = []
        for it in rep["items"]:
            for x in flat(sub_geo.get(it["geometry"])):
                x = dict(x); x["material_value"] = resolve_material(it, sub_env, x); x["nested"] = object_id; parts.append(x)
        return parts

    for step in T["opo::recipe"]:
        scope = bind_ops(step.get("plane", "xy"), env, base_dir); scope["instance"] = instance; scope.update(env); scope.update(geo)
        if "when" in step and feel(step["when"], scope) is not True:
            geo[step["id"]] = None; continue
        op, args, plane = step["op"], step["args"], step.get("plane", "xy")
        if op == "for_each":
            items = feel(args["items"], scope)
            res = []
            for i, it in enumerate(items or []):
                s2 = dict(scope); s2[args.get("as", "item")] = it; s2[args.get("index", "i")] = float(i + 1)
                g = feel(args["do"], s2)
                for x in flat(g):
                    x = dict(x)
                    x.setdefault("each", it if isinstance(it, dict) else x.get("each"))
                    if not isinstance(it, dict) and isinstance(it, list) is False and "each" not in x: x["each"] = {"value": it}
                    x["index"] = i + 1; res.append(x)
            geo[step["id"]] = res
        elif op == "instance":
            geo[step["id"]] = instance(feel(args["object"], scope), feel(args.get("values", "{}"), scope), feel(args.get("inputs", "{}"), scope),
                                       args.get("representation", "model.medium"))
        else:
            kw = {k: feel(v, scope) for k, v in args.items()}
            if op == "extrude": kw = {"profile": kw["profile"], "from": kw["from"], "to": kw["to"]}
            geo[step["id"]] = OPS[op](plane, **kw)
    return env, geo, T

def resolve_material(item, env, g=None):
    m = item.get("material")
    if m is None: return None
    if g is not None and "material_value" in g: return g["material_value"]
    if m.startswith("each."):
        return ((g or {}).get("each") or {}).get(m[5:])
    return feel(m, env)
