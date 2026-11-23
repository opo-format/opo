"""Reference interpreter for OPO's FEEL subset (spec §4.4). Prototype for tests; the Rust crate is canonical later.

Supported: numbers, strings, true/false/null, lists [a, b], ranges a..b (FEEL: descending when a > b),
names and paths (a.b; a path on a list maps over it), calls f(x), indexing x[i] (1-based, negative from the end),
+ - * / **, unary -, = != < <= > >=, and / or, if … then … else, for x in list return expr,
built-ins (see BUILTINS). Values: float, str, bool, None, list, dict (contexts).
"""
import math, re

TOKEN = re.compile(r"\s*(?:(\d+(?:\.\d+)?(?:[eE][-+]?\d+)?)|(\"(?:[^\"\\]|\\.)*\")|(\.\.|\*\*|<=|>=|!=|[-+*/(),\[\]<>=.{}:])|([A-Za-z_][A-Za-z_0-9]*))")
KEYWORDS = {"if", "then", "else", "for", "in", "return", "and", "or", "true", "false", "null"}


class FeelError(Exception):
    pass


def tokenize(src):
    out, i = [], 0
    while i < len(src):
        m = TOKEN.match(src, i)
        if not m or m.end() == i:
            if src[i:].strip() == "":
                break
            raise FeelError(f"bad token at {src[i:]!r} in {src!r}")
        num, s, op, name = m.groups()
        if num is not None: out.append(("num", float(num)))
        elif s is not None: out.append(("str", s[1:-1].replace('\\"', '"')))
        elif op is not None: out.append(("op", op))
        else: out.append(("kw" if name in KEYWORDS else "name", name))
        i = m.end()
    out.append(("end", None))
    return out


class Parser:
    def __init__(self, src):
        self.t, self.i, self.src = tokenize(src), 0, src

    def peek(self, k=0): return self.t[self.i + k]
    def next(self): tok = self.t[self.i]; self.i += 1; return tok
    def accept(self, kind, val=None):
        tk, tv = self.peek()
        if tk == kind and (val is None or tv == val): self.i += 1; return True
        return False
    def expect(self, kind, val=None):
        if not self.accept(kind, val): raise FeelError(f"expected {val or kind} at {self.peek()} in {self.src!r}")

    def parse(self):
        e = self.expr()
        if self.peek()[0] != "end": raise FeelError(f"trailing input {self.peek()} in {self.src!r}")
        return e

    def expr(self):
        if self.accept("kw", "if"):
            c = self.expr(); self.expect("kw", "then"); a = self.expr(); self.expect("kw", "else"); b = self.expr()
            return ("if", c, a, b)
        if self.accept("kw", "for"):
            binds = []
            while True:
                tk, name = self.next()
                if tk != "name": raise FeelError("for: name expected")
                self.expect("kw", "in"); binds.append((name, self.expr()))
                if not self.accept("op", ","): break
            self.expect("kw", "return")
            return ("for", binds, self.expr())
        return self.disj()

    def disj(self):
        e = self.conj()
        while self.accept("kw", "or"): e = ("or", e, self.conj())
        return e

    def conj(self):
        e = self.comp()
        while self.accept("kw", "and"): e = ("and", e, self.comp())
        return e

    def comp(self):
        e = self.rng()
        tk, tv = self.peek()
        if tk == "op" and tv in ("=", "!=", "<", "<=", ">", ">="):
            self.next(); e = ("cmp", tv, e, self.rng())
        return e

    def rng(self):
        e = self.add()
        if self.accept("op", ".."): e = ("range", e, self.add())
        return e

    def add(self):
        e = self.mul()
        while True:
            tk, tv = self.peek()
            if tk == "op" and tv in "+-" and tv != "": self.next(); e = ("bin", tv, e, self.mul())
            else: return e

    def mul(self):
        e = self.pow()
        while True:
            tk, tv = self.peek()
            if tk == "op" and tv in ("*", "/"): self.next(); e = ("bin", tv, e, self.pow())
            else: return e

    def pow(self):
        e = self.unary()
        if self.accept("op", "**"): e = ("bin", "**", e, self.pow())
        return e

    def unary(self):
        if self.accept("op", "-"): return ("neg", self.unary())
        return self.postfix()

    def postfix(self):
        e = self.atom()
        while True:
            if self.accept("op", "."):
                tk, name = self.next()
                if tk not in ("name", "kw"): raise FeelError("path: name expected")
                e = ("path", e, name)
            elif self.accept("op", "("):
                args = []
                if not self.accept("op", ")"):
                    while True:
                        args.append(self.expr())
                        if self.accept("op", ")"): break
                        self.expect("op", ",")
                e = ("call", e, args)
            elif self.accept("op", "["):
                idx = self.expr(); self.expect("op", "]"); e = ("index", e, idx)
            else:
                return e

    def atom(self):
        tk, tv = self.next()
        if tk == "num": return ("lit", tv)
        if tk == "str": return ("lit", tv)
        if tk == "kw" and tv in ("true", "false", "null"): return ("lit", {"true": True, "false": False, "null": None}[tv])
        if tk == "name": return ("name", tv)
        if tk == "op" and tv == "(":
            e = self.expr(); self.expect("op", ")"); return e
        if tk == "op" and tv == "{":
            entries = []
            if not self.accept("op", "}"):
                while True:
                    kt, kv = self.next()
                    if kt not in ("name", "str", "kw"): raise FeelError("context key expected")
                    self.expect("op", ":"); entries.append((kv, self.expr()))
                    if self.accept("op", "}"): break
                    self.expect("op", ",")
            return ("ctx", entries)
        if tk == "op" and tv == "[":
            items = []
            if not self.accept("op", "]"):
                while True:
                    items.append(self.expr())
                    if self.accept("op", "]"): break
                    self.expect("op", ",")
            return ("list", items)
        raise FeelError(f"unexpected {tv!r} in {self.src!r}")


def _num_list(args):
    return list(args[0]) if len(args) == 1 and isinstance(args[0], list) else list(args)

def _sum(*a):
    xs = _num_list(a)
    return None if not xs or any(x is None for x in xs) else float(sum(xs))

def _sublist(lst, start, length=None):
    start = int(start)
    s = start - 1 if start > 0 else len(lst) + start
    return lst[s:] if length is None else lst[s:s + int(length)]

def _flatten(lst):
    out = []
    for x in lst:
        out.extend(_flatten(x) if isinstance(x, list) else [x])
    return out

BUILTINS = {
    # unit helpers: canonical units are metres and degrees
    "mm": lambda v: v / 1000, "cm": lambda v: v / 100, "m": lambda v: v, "inch": lambda v: v * 0.0254,
    "ft": lambda v: v * 0.3048, "deg": lambda v: v,
    # numbers
    "min": lambda *a: min(_num_list(a)), "max": lambda *a: max(_num_list(a)), "abs": abs, "sqrt": math.sqrt,
    "ceiling": lambda v: float(math.ceil(v - 1e-9)), "floor": lambda v: float(math.floor(v + 1e-9)),
    "round": lambda v, d=0: float(round(v, int(d))), "modulo": lambda a, b: a - b * math.floor(a / b),
    "sin": lambda a: math.sin(math.radians(a)), "cos": lambda a: math.cos(math.radians(a)),
    "tan": lambda a: math.tan(math.radians(a)), "atan2": lambda y, x: math.degrees(math.atan2(y, x)),
    # lists
    "sum": _sum, "count": lambda l: float(len(l)), "sublist": _sublist, "flatten": _flatten,
    "append": lambda l, *x: list(l) + list(x), "concatenate": lambda *ls: [y for l in ls for y in l],
    "reverse": lambda l: list(reversed(l)), "index_of": lambda l, x: [float(i + 1) for i, y in enumerate(l) if y == x],
    "list_contains": lambda l, x: x in l,
    # logic
    "not": lambda b: None if b is None else (not b),
}


def evaluate(node, env):
    k = node[0]
    if k == "lit": return node[1]
    if k == "name":
        n = node[1]
        if n in env: return env[n]
        if n in BUILTINS: return BUILTINS[n]
        raise FeelError(f"unknown name {n!r}")
    if k == "list": return [evaluate(x, env) for x in node[1]]
    if k == "ctx": return {key: evaluate(v, env) for key, v in node[1]}
    if k == "path":
        base = evaluate(node[1], env)
        if isinstance(base, list): return [None if b is None else b.get(node[2]) for b in base]
        if base is None: return None
        if not isinstance(base, dict): raise FeelError(f"path .{node[2]} on {type(base).__name__}")
        return base.get(node[2])
    if k == "call":
        f = evaluate(node[1], env)
        return f(*[evaluate(a, env) for a in node[2]])
    if k == "index":
        lst, i = evaluate(node[1], env), evaluate(node[2], env)
        if lst is None or i is None: return None
        i = int(i)
        if i == 0 or abs(i) > len(lst): return None
        return lst[i - 1] if i > 0 else lst[i]
    if k == "neg":
        v = evaluate(node[1], env); return None if v is None else -v
    if k == "bin":
        a, b = evaluate(node[2], env), evaluate(node[3], env)
        if a is None or b is None: return None
        op = node[1]
        if op == "+": return a + b
        if op == "-": return a - b
        if op == "*": return a * b
        if op == "/": return None if b == 0 else a / b
        if op == "**": return a ** b
    if k == "cmp":
        a, b, op = evaluate(node[2], env), evaluate(node[3], env), node[1]
        if op == "=": return a == b if not (isinstance(a, float) and isinstance(b, float)) else abs(a - b) < 1e-9
        if op == "!=": return not (a == b if not (isinstance(a, float) and isinstance(b, float)) else abs(a - b) < 1e-9)
        if a is None or b is None: return None
        return {"<": a < b - 1e-12, "<=": a <= b + 1e-12, ">": a > b + 1e-12, ">=": a >= b - 1e-12}[op]
    if k == "and":
        a = evaluate(node[1], env)
        if a is False: return False
        b = evaluate(node[2], env)
        return False if b is False else (True if a is True and b is True else None)
    if k == "or":
        a = evaluate(node[1], env)
        if a is True: return True
        b = evaluate(node[2], env)
        return True if b is True else (False if a is False and b is False else None)
    if k == "if":
        return evaluate(node[2], env) if evaluate(node[1], env) is True else evaluate(node[3], env)
    if k == "range":
        a, b = int(evaluate(node[1], env)), int(evaluate(node[2], env))
        return [float(x) for x in (range(a, b + 1) if a <= b else range(a, b - 1, -1))]
    if k == "for":
        binds, body = node[1], node[2]
        def rec(i, scope):
            if i == len(binds): return [evaluate(body, scope)]
            name, src = binds[i]
            out = []
            for v in evaluate(src, scope):
                s2 = dict(scope); s2[name] = v; out.extend(rec(i + 1, s2))
            return out
        return rec(0, dict(env))
    raise FeelError(f"bad node {k}")


_CACHE = {}
def feel(src, env):
    """Evaluate a FEEL-subset expression string. Non-strings (numbers, lists already as data) pass through."""
    if not isinstance(src, str): return src
    ast = _CACHE.get(src)
    if ast is None: ast = _CACHE[src] = Parser(src).parse()
    return evaluate(ast, env)


def names(src):
    """Free names used by an expression (for reference checks); excludes built-ins and for-bound names."""
    ast = Parser(src).parse() if isinstance(src, str) else ("lit", src)
    used = set()
    def walk(n, bound):
        k = n[0]
        if k == "name":
            if n[1] not in bound and n[1] not in BUILTINS: used.add(n[1])
        elif k == "for":
            b2 = set(bound)
            for name, s in n[1]: walk(s, b2); b2.add(name)
            walk(n[2], b2)
        elif k == "ctx":
            for _, v in n[1]: walk(v, bound)
        elif k == "path":
            walk(n[1], bound)
        else:
            for x in n[1:]:
                if isinstance(x, tuple): walk(x, bound)
                elif isinstance(x, list):
                    for y in x:
                        if isinstance(y, tuple): walk(y, bound)
    walk(ast, set())
    return used


if __name__ == "__main__":
    # conformance smoke tests
    env = {"layers": [{"thickness": 0.015}, {"thickness": 0.2}, {"thickness": 0.015}], "w": 0.9}
    tests = [
        ("1 + 2 * 3", 7.0), ("mm(900)", 0.9), ("if w >= mm(900) then \"ok\" else \"no\"", "ok"),
        ("sum(layers.thickness)", 0.23), ("count(layers)", 3.0), ("[1, 2, 3][1]", 1.0), ("[1, 2, 3][-1]", 3.0),
        ("for i in 1..3 return i * 2", [2.0, 4.0, 6.0]), ("3..1", [3.0, 2.0, 1.0]),
        ("for i in 1..count(layers) return sum(sublist(layers.thickness, 1, i)) - layers[i].thickness", [0.0, 0.015, 0.215]),
        ("not(true) or null", None), ("false and null", False), ("ceiling(2.8 / 0.175)", 16.0), ("sum([])", None),
        ("flatten([[1, 2], [3]])", [1.0, 2.0, 3.0]), ("{a: 1, \"b c\": w}.a", 1.0), ("max([1, 5, 2])", 5.0), ("1 / 0", None),
    ]
    bad = 0
    for src, want in tests:
        got = feel(src, env)
        okv = (abs(got - want) < 1e-9) if isinstance(want, float) and isinstance(got, float) else (
            all(abs(a - b) < 1e-9 for a, b in zip(got, want)) and len(got) == len(want) if isinstance(want, list) and want and isinstance(want[0], float) else got == want)
        if not okv: bad += 1; print("FAIL", src, got, want)
    print(f"{len(tests) - bad}/{len(tests)} FEEL tests pass")
