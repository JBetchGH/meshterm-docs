#!/usr/bin/env python3
"""Content-preservation check for the Jekyll restyle.

For every page, compares the ORIGINAL page (from a git ref, default docs/v2.2)
with the BUILT page in _site/:

  original content region = <body> minus the old nav bar (.nav-links), the old
                            <footer>, and <script>/<style> elements
  built content region    = every element marked data-content, minus any
                            descendant marked data-chrome (the new sidebar
                            etc.), minus <script>/<style>

Checked, and required IDENTICAL:
  - visible text (whitespace-normalised)
  - every href, every id, every img src (in document order)
  - the full element/attribute sequence (stricter than the above)
  - the page footer text and links (old <footer> vs built [data-footer-content])
  - the <title>, meta description and hreflang alternates
Then: every href="#x" and "page.html#x" in the built site resolves.

Usage:  python3 scripts/check-content.py [--ref docs/v2.2] [--site _site]
Build first:  bundle exec jekyll build
"""
import argparse, difflib, os, re, subprocess, sys
from html.parser import HTMLParser

PAGES = ["index.html", "index.es.html", "meshterm.html",
         "meshterm-tailscale-integration.html", "privacy.html",
         "privacy.es.html", "eula.html", "eula.es.html"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


class Node:
    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.children = tag, attrs, parent, []


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", [], None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse(html):
    b = TreeBuilder()
    b.feed(html)
    b.close()
    return b.root


def walk(node):
    yield node
    for c in node.children:
        if isinstance(c, Node):
            yield from walk(c)


def attr(n, name):
    for k, v in n.attrs:
        if k == name:
            return v
    return None


def has_class(n, cls):
    return cls in (attr(n, "class") or "").split()


def find_all(root, pred):
    return [n for n in walk(root) if pred(n)]


def extract(nodes, skip):
    """Return dict of text / hrefs / ids / imgs / structure for a list of region roots."""
    text, hrefs, ids, imgs, struct = [], [], [], [], []

    def rec(n):
        if isinstance(n, str):
            text.append(n)
            return
        if n.tag in ("script", "style") or skip(n):
            return
        a = dict(n.attrs)
        struct.append((n.tag, tuple(sorted((k, v or "") for k, v in n.attrs))))
        if "href" in a:
            hrefs.append(a["href"])
        if "id" in a:
            ids.append(a["id"])
        if n.tag == "img":
            imgs.append(a.get("src"))
        for c in n.children:
            rec(c)

    for r in nodes:
        rec(r)
    return {"text": " ".join(" ".join(text).split()), "hrefs": hrefs, "ids": ids,
            "imgs": imgs, "structure": struct}


def head_meta(root):
    title = "".join(c for n in find_all(root, lambda n: n.tag == "title") for c in n.children if isinstance(c, str))
    desc = [attr(n, "content") for n in find_all(root, lambda n: n.tag == "meta" and attr(n, "name") == "description")]
    alts = [(attr(n, "hreflang"), attr(n, "href")) for n in find_all(root, lambda n: n.tag == "link" and attr(n, "rel") == "alternate")]
    return {"title": title.strip(), "description": desc, "alternates": alts}


def original_regions(root):
    body = find_all(root, lambda n: n.tag == "body")[0]
    skip_orig = lambda n: has_class(n, "nav-links") or n.tag == "footer"
    content = extract(body.children, skip_orig)
    footer = extract(find_all(body, lambda n: n.tag == "footer"), lambda n: False)
    return content, footer


def built_regions(root):
    regions = find_all(root, lambda n: attr(n, "data-content") is not None or ("data-content", None) in n.attrs)
    skip_built = lambda n: any(k == "data-chrome" for k, _ in n.attrs)
    content = extract(regions, skip_built)
    footer = extract(find_all(root, lambda n: any(k == "data-footer-content" for k, _ in n.attrs)), lambda n: False)
    # the region wrappers themselves are layout chrome: drop their own entry
    content["structure"] = [s for s in content["structure"] if not any(k == "data-content" for k, _ in s[1])]
    footer["structure"] = [s for s in footer["structure"] if not any(k == "data-footer-content" for k, _ in s[1])]
    return content, footer, len(regions)


def show_diff(a, b, label):
    if isinstance(a, str):
        a, b = re.split(r"(?<=[.!?:])\s+", a), re.split(r"(?<=[.!?:])\s+", b)
    else:
        a, b = [repr(x) for x in a], [repr(x) for x in b]
    for line in list(difflib.unified_diff(a, b, "original", "built", lineterm="", n=1))[:40]:
        print("      " + line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="docs/v2.2")
    ap.add_argument("--site", default="_site")
    args = ap.parse_args()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

    ok = True
    built_trees = {}
    print(f"Content check: original = git {args.ref}, built = {args.site}/\n")
    for page in PAGES:
        orig_html = subprocess.run(["git", "show", f"{args.ref}:{page}"], capture_output=True, text=True, check=True).stdout
        path = os.path.join(args.site, page)
        if not os.path.exists(path):
            print(f"FAIL  {page}: not built at /{page}")
            ok = False
            continue
        built_html = open(path, encoding="utf-8").read()
        o_root, b_root = parse(orig_html), parse(built_html)
        built_trees[page] = b_root
        o_c, o_f = original_regions(o_root)
        b_c, b_f, nreg = built_regions(b_root)
        failures = []
        if nreg == 0:
            failures.append(("data-content region", "", "missing"))
        for key in ("text", "hrefs", "ids", "imgs", "structure"):
            if o_c[key] != b_c[key]:
                failures.append(("content " + key, o_c[key], b_c[key]))
        for key in ("text", "hrefs"):
            if o_f[key] != b_f[key]:
                failures.append(("footer " + key, o_f[key], b_f[key]))
        o_m, b_m = head_meta(o_root), head_meta(b_root)
        for key in o_m:
            if o_m[key] != b_m[key]:
                failures.append(("head " + key, o_m[key], b_m[key]))
        status = "PASS" if not failures else "FAIL"
        ok &= not failures
        print(f"{status}  {page:38s} text {len(o_c['text']):6d} chars, {len(o_c['hrefs']):3d} hrefs, "
              f"{len(o_c['ids']):3d} ids, {len(o_c['imgs'])} imgs, {len(o_c['structure']):4d} elements")
        for label, a, b in failures:
            print(f"    mismatch in {label}:")
            show_diff(a, b, label)

    # Anchor check across the built site (content + chrome).
    print("\nAnchor check (every #x and page.html#x in the built pages):")
    ids_by_page = {p: {attr(n, "id") for n in walk(t) if attr(n, "id")} for p, t in built_trees.items()}
    bad = 0
    total = 0
    for p, t in built_trees.items():
        for n in walk(t):
            h = attr(n, "href")
            if not h or h.startswith(("http:", "https:", "mailto:", "//")):
                continue
            page, _, frag = h.partition("#")
            page = page.lstrip("/") or (p if h.startswith("#") else "index.html")
            if page.endswith("/"):
                page += "index.html"
            total += 1
            if page not in ids_by_page and not os.path.exists(os.path.join(args.site, page)):
                print(f"  BROKEN  {p}: {h} (no such page)")
                bad += 1
            elif frag and frag not in ids_by_page.get(page, set()):
                print(f"  BROKEN  {p}: {h} (no id '{frag}' on {page})")
                bad += 1
    print(f"  {total} internal links checked, {bad} broken" + ("  PASS" if not bad else "  FAIL"))
    ok &= not bad

    # Old ids present on the built pages.
    print("\nOriginal ids present on the built pages:")
    for page in PAGES:
        o_root = parse(subprocess.run(["git", "show", f"{args.ref}:{page}"], capture_output=True, text=True, check=True).stdout)
        old = [attr(n, "id") for n in walk(o_root) if attr(n, "id")]
        missing = [i for i in old if i not in ids_by_page.get(page, set())]
        print(f"  {page:38s} {len(old) - len(missing)}/{len(old)}" + (f"  MISSING {missing}" if missing else ""))
        ok &= not missing

    print("\nRESULT:", "ALL PASS" if ok else "FAILURES")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
