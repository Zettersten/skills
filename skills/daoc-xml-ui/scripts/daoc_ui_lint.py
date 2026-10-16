#!/usr/bin/env python3
"""Lint a Dark Age of Camelot ``ui/custom`` folder.

The game client gives almost no feedback when a custom UI is wrong: a window
silently fails to appear, a control never shows, or a button does nothing.
The official doc says "most errors are naming errors". This script catches
those before you launch the game.

Usage:
    python daoc_ui_lint.py <custom-folder> [--base <ui/atlantis folder>] [--strict] [--json]

    --base    Path to the stock skin folder (usually ``<game>/ui/atlantis``).
              When given, the linter models the client's per-file fallback:
              a file missing from custom/ is taken from base/. Template and
              font/texture references are then resolved against the full
              effective set, which turns many "maybe" warnings into facts.
    --strict  Treat warnings as errors (exit code 1).
    --json    Emit machine-readable findings.

Exit code: 0 clean, 1 errors found (or warnings with --strict), 2 bad usage.

What it checks (E = error, W = warning, I = info):
    E xml        file does not parse (with line number)
    E include    <Include> target not found in custom/ (nor base/ when given)
    E template   referenced template/font/texture name is defined nowhere
                 (W when --base is not given, because it may live in atlantis)
    E adapter    case mismatch with a known adapter (adapter names ARE case sensitive)
    W adapter    adapter name not in the official or observed lists
    W event      event name not in the official or observed lists
    W name-len   name longer than 31 characters (the ToA doc's limit; modern
                 shipping UIs exceed it, so this is advisory)
    W dup-name   same name defined twice in one file (the later wins);
                 I when the duplicates are in different files (option variants)
    W draw-order a full-window background drawn after other controls (covers them)
    W bounds     control positioned outside a non-resizable window (cannot be clicked)
    W orphan     customN_window.xml exists but nothing <Include>s it
    W asset-file <File> referenced by a Font/Texture does not exist on disk
    I controlid  numeric ControlId used twice in one window (fine for tab grouping)
    I tab        TabControl references a ControlId that no control in the window has
    I unknown    element or field name not seen in the official doc or any
                 known working UI (not necessarily wrong, but double check it)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from xml.parsers import expat

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
NAME_MAX = 31
NULL_NAMES = {"", "none"}  # stock files use 'none' to mean "no template / font / texture here"

ADAPTER_FIELDS = {"adaptername", "adapter", "coloradapter", "textadaptername", "buffername",
                  "labeladaptername", "stateadaptername"}
TEMPLATE_REF_FIELDS = {
    "templatename", "backgroundtemplate", "scrollbartemplate", "icontemplate", "icontemplatename",
    "imageareatemplate", "imageareatemplatename", "hrbuttontemplatename", "labelbuttontemplate",
    "menutemplate", "downbuttontemplate", "upbuttontemplate", "thumbvresizetemplate",
    "guttervresizetemplate",
    "backgroundhresizetemplate", "foregroundhresizetemplate", "backgroundvresizetemplate",
    "headerhorizresizetemplate", "headerbackgroundtemplate", "controlareafullresizeimagetemplate",
    "tabbuttontemplate", "checkboxtemplate", "treecontroltemplate", "contexttemplatename",
    "backgroundimage", "foregroundimage",
}
FONT_REF_FIELDS = {"fontname"}
TEXTURE_REF_FIELDS = {"texturename"}
# Template fields that hold a texture/image name directly (no nested <Texture> block)
EVENT_FIELD_RE = re.compile(r"event$")
ASSET_TAGS = {"font", "ttffont", "texture", "canvas"}


# --------------------------------------------------------------------------- tree
@dataclass
class Node:
    tag: str
    line: int
    children: list["Node"] = field(default_factory=list)
    text: str = ""
    parent: "Node | None" = None

    @property
    def low(self) -> str:
        return self.tag.lower()

    def child(self, name: str) -> "Node | None":
        name = name.lower()
        for c in self.children:
            if c.low == name:
                return c
        return None

    def value(self, name: str) -> str:
        c = self.child(name)
        return c.text.strip() if c else ""


def parse(path: Path) -> tuple[Node | None, str | None]:
    raw = path.read_bytes().lstrip(b"\xef\xbb\xbf")
    text = raw.decode("latin-1")  # never fails; files declare ISO-8859-1
    text = re.sub(r"^\s*<\?xml[^>]*\?>", "", text, count=1)
    text = re.sub(r"&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", text)
    root: Node | None = None
    stack: list[Node] = []
    p = expat.ParserCreate()

    def start(tag, _attrs):
        nonlocal root
        n = Node(tag, p.CurrentLineNumber)
        if stack:
            n.parent = stack[-1]
            stack[-1].children.append(n)
        else:
            root = n
        stack.append(n)

    def end(_tag):
        stack.pop()

    def chars(data):
        if stack:
            stack[-1].text += data

    p.StartElementHandler = start
    p.EndElementHandler = end
    p.CharacterDataHandler = chars
    try:
        p.Parse(text, True)
    except expat.ExpatError as exc:
        return None, f"{exc}"
    return root, None


# --------------------------------------------------------------------------- knowledge
def expand(pattern: str) -> list[str]:
    """Expand 'name{0-7}' style patterns (possibly two ranges)."""
    m = re.search(r"\{(\d+)-(\d+)\}", pattern)
    if not m:
        return [pattern]
    out = []
    for i in range(int(m.group(1)), int(m.group(2)) + 1):
        out.extend(expand(pattern[: m.start()] + str(i) + pattern[m.end():]))
    return out


def load_knowledge() -> dict:
    k = {"adapters": set(), "events": set(), "templates": {}, "defs": {}, "window_fields": set(),
         "official_adapters": set(), "official_events": set()}
    off_path = DATA / "official.json"
    if off_path.exists():
        off = json.loads(off_path.read_text(encoding="utf-8"))
        for names in off["adapters"].values():
            for n in names:
                k["official_adapters"].update(expand(n))
        for group in off["events"].values():
            for n in group:
                k["official_events"].update(expand(n))
        for t, fields in off["templates"].items():
            k["templates"].setdefault(t.lower(), set()).update(f.split("{")[0].lower() for f in fields)
        common = [f.split("{")[0].lower() for f in off["defs"]["_common"]]
        for d, fields in off["defs"].items():
            if d.startswith("_"):
                continue
            k["defs"].setdefault(d.lower(), set()).update(common + [f.lower() for f in fields])
        k["window_fields"].update(f.lower() for f in off["window_fields"])
    k["adapters"] |= k["official_adapters"]
    k["events"] |= k["official_events"]
    # observed inventories: data/ (BobsUI 1.127 corpus) and data/stock/ (stock Atlantis skin, client 1.130)
    for folder in (DATA, DATA / "stock"):
        for fname, key in (("adapters.json", "adapters"), ("events.json", "events")):
            pth = folder / fname
            if pth.exists():
                k[key].update(json.loads(pth.read_text(encoding="utf-8")).keys())
        for fname, key in (("templates.json", "templates"), ("defs.json", "defs")):
            pth = folder / fname
            if pth.exists():
                for t, info in json.loads(pth.read_text(encoding="utf-8")).items():
                    if t.startswith("("):
                        continue
                    k[key].setdefault(t.lower(), set()).update(f.lower() for f in info["fields"])
        wf = folder / "window_fields.json"
        if wf.exists():
            k["window_fields"].update(f.lower() for f in json.loads(wf.read_text(encoding="utf-8")))
    k["events_lower"] = {e.lower(): e for e in k["events"]}
    k["adapters_lower"] = defaultdict(set)
    for a in k["adapters"]:
        k["adapters_lower"][a.lower()].add(a)
    return k


# --------------------------------------------------------------------------- linter
@dataclass
class Finding:
    level: str  # E W I
    code: str
    file: str
    line: int
    msg: str

    def __str__(self) -> str:
        return f"{self.level} {self.code:<10} {self.file}:{self.line}: {self.msg}"


class Linter:
    def __init__(self, custom: Path, base: Path | None, know: dict):
        self.custom = custom
        self.base = base
        self.k = know
        self.findings: list[Finding] = []
        self.defined: dict[str, list[tuple[str, str, int]]] = defaultdict(list)  # lower name -> [(kind, file, line)]
        self.defined_typed: dict[tuple[str, str], list[tuple[str, int, bool]]] = defaultdict(list)  # (kind, name) -> [(file, line, in_custom)]
        self.fonts: dict[str, list[tuple[str, int]]] = defaultdict(list)
        self.textures: dict[str, list[tuple[str, int]]] = defaultdict(list)
        self.windows: dict[str, list[tuple[str, int, bool]]] = defaultdict(list)
        self.refs: list[tuple[str, str, str, int]] = []  # (kind, name, file, line); custom files only
        self.includes: dict[str, list[tuple[str, int]]] = {}
        self.trees: dict[str, Node] = {}

    # -- helpers
    def add(self, level: str, code: str, file: str, line: int, msg: str) -> None:
        self.findings.append(Finding(level, code, file, line, msg))

    def effective_files(self) -> dict[str, Path]:
        """relative-path -> actual path, modelling custom-over-base fallback."""
        files: dict[str, Path] = {}
        if self.base:
            for p in self.base.rglob("*.xml"):
                files[p.relative_to(self.base).as_posix().lower()] = p
        for p in self.custom.rglob("*.xml"):
            rel = p.relative_to(self.custom).as_posix()
            if rel.split("/")[0].lower() == "options":  # BobsUI option variants, not loaded by the game
                continue
            files[rel.lower()] = p
        return files

    # -- passes
    def run(self) -> None:
        files = self.effective_files()
        for rel, path in sorted(files.items()):
            in_custom = self.custom in path.parents
            label = (path.relative_to(self.custom) if in_custom else Path("<base>") / path.relative_to(self.base)).as_posix()
            root, err = parse(path)
            if root is None:
                if in_custom:
                    self.add("E", "xml", label, 0, f"does not parse: {err}")
                continue
            self.trees[label] = root
            self.collect(root, label, rel, in_custom)
        self.resolve_includes(files)
        self.resolve_refs()
        self.check_orphans(files)

    def ref(self, kind: str, name: str, label: str, line: int, in_custom: bool) -> None:
        """Record a name reference to resolve later; only the user's files are checked."""
        if in_custom and name.strip().lower() not in NULL_NAMES:
            self.refs.append((kind, name.strip(), label, line))

    def collect(self, root: Node, label: str, rel: str, in_custom: bool) -> None:
        self.includes[rel] = []
        for top in root.children:
            t = top.low
            if t == "include":
                self.includes[rel].append((top.text.strip(), top.line))
            elif t in ASSET_TAGS:
                name = top.value("Name")
                if in_custom:
                    self.check_name_len(name, label, top.line, top.tag)
                    self.check_asset_file(top, label)
                store = self.fonts if t in ("font", "ttffont") else self.textures
                store[name.lower()].append((label, top.line))
                self.defined[name.lower()].append((top.tag, label, top.line))
                self.defined_typed[(t, name.lower())].append((label, top.line, in_custom))
            elif t == "windowtemplate":
                self.collect_window(top, label, in_custom)
            elif t.endswith("template"):
                name = top.value("Name")
                if in_custom:
                    self.check_name_len(name, label, top.line, top.tag)
                self.defined[name.lower()].append((top.tag, label, top.line))
                self.defined_typed[(t, name.lower())].append((label, top.line, in_custom))
                self.collect_template(top, label, in_custom)
            elif in_custom:
                self.add("I", "unknown", label, top.line, f"unexpected top-level element <{top.tag}>")

    def collect_template(self, tmpl: Node, label: str, in_custom: bool) -> None:
        known = self.k["templates"].get(tmpl.low)
        for f in tmpl.children:
            fl = f.low
            if known is not None and fl not in known and in_custom:
                self.add("I", "unknown", label, f.line, f"<{f.tag}> is not a known field of <{tmpl.tag}>")
            if fl in TEMPLATE_REF_FIELDS:
                self.ref("template", f.text, label, f.line, in_custom)
            elif fl in FONT_REF_FIELDS:
                self.ref("font", f.text, label, f.line, in_custom)
            elif fl in TEXTURE_REF_FIELDS:
                self.ref("texture", f.text, label, f.line, in_custom)
            elif fl == "texture":
                # nested <Texture> block or a bare texture name (CompassControlTemplate)
                if f.children:
                    self.ref("texture", f.value("TextureName") or f.value("Name"), label, f.line, in_custom)
                else:
                    self.ref("texture", f.text, label, f.line, in_custom)
            elif fl in ("font", "textfont") and f.children:
                self.ref("font", f.value("Name"), label, f.line, in_custom)
        if known is None and in_custom:
            self.add("I", "unknown", label, tmpl.line, f"<{tmpl.tag}> is not a known template type")

    def collect_window(self, win: Node, label: str, in_custom: bool) -> None:
        name = win.value("Name")
        if in_custom:
            self.check_name_len(name, label, win.line, "WindowTemplate")
        self.windows[name.lower()].append((label, win.line, in_custom))
        try:
            w, h = int(win.value("Width") or 0), int(win.value("Height") or 0)
        except ValueError:
            w = h = 0

        def flag(fname: str) -> bool:
            v = win.value(fname).lower()
            return v == "true" or (v.isdigit() and int(v) > 0)

        grows_x = flag("ResizeableWidth") or flag("BottomRightResizeButton") or flag("BottomLeftResizeButton") or flag("TopRightResizeButton")
        grows_y = flag("ResizeableHeight") or flag("BottomRightResizeButton") or flag("BottomLeftResizeButton") or flag("TopRightResizeButton")
        self.ref("window", win.value("ContextTemplateName"), label, win.line, in_custom)
        seen_ids: dict[str, int] = {}
        tab_refs: list[tuple[str, int]] = []
        saw_non_bg = False
        for i, c in enumerate(win.children):
            if not c.low.endswith("def"):
                if c.low not in self.k["window_fields"] and in_custom:
                    self.add("I", "unknown", label, c.line, f"<{c.tag}> is not a known WindowTemplate field")
                continue
            if not in_custom:
                continue
            known = self.k["defs"].get(c.low)
            if known is None:
                self.add("I", "unknown", label, c.line, f"<{c.tag}> is not a known control definition type")
            # fields
            cid = c.value("ControlId")
            if cid.isdigit():
                if cid in seen_ids:
                    self.add("I", "controlid", label, c.line,
                             f"ControlId {cid} already used at line {seen_ids[cid]} in window '{name}' (fine if both belong to the same tab)")
                seen_ids.setdefault(cid, c.line)
            for f in c.children:
                fl = f.low
                val = f.text.strip()
                if known is not None and fl not in known and fl not in ("tab", "tabcontrol"):
                    self.add("I", "unknown", label, f.line, f"<{f.tag}> is not a known field of <{c.tag}>")
                if fl in TEMPLATE_REF_FIELDS:
                    self.ref("template", val, label, f.line, in_custom)
                elif fl in FONT_REF_FIELDS:
                    self.ref("font", val, label, f.line, in_custom)
                elif fl in TEXTURE_REF_FIELDS:
                    self.ref("texture", val, label, f.line, in_custom)
                elif fl in ADAPTER_FIELDS and val:
                    self.check_adapter(val, label, f.line)
                elif EVENT_FIELD_RE.search(fl) and val:
                    self.check_event(val, label, f.line)
                elif fl == "tabcontrol":
                    tab_refs.append((f.value("ControlId"), f.line))
            # geometry
            pos = c.child("Position")
            if pos is not None and w and h:
                try:
                    x, y = int(pos.value("X") or 0), int(pos.value("Y") or 0)
                except ValueError:
                    x = y = 0
                align = c.child("Alignment")
                offs = {a.low for a in align.children} if align else set()
                out_x = x >= w and "offsetright" not in offs and not grows_x
                out_y = y >= h and "offsetbottom" not in offs and not grows_y
                if out_x or out_y:
                    self.add("W", "bounds", label, c.line,
                             f"<{c.tag}> at ({x},{y}) lies outside window '{name}' ({w}x{h}); it cannot be interacted with")
            # draw order heuristic: a full-size FullResizeImage after other controls hides them
            if c.low == "fullresizeimagedef":
                try:
                    cw, ch = int(c.value("Width") or 0), int(c.value("Height") or 0)
                except ValueError:
                    cw = ch = 0
                if saw_non_bg and w and h and cw >= w and ch >= h:
                    self.add("W", "draw-order", label, c.line,
                             f"full-window background drawn after other controls in '{name}'; controls draw in XML order, so earlier ones are covered")
            else:
                saw_non_bg = True
        for cid, line in tab_refs:
            if cid and cid not in seen_ids:
                self.add("I", "tab", label, line, f"TabControl references ControlId {cid}, but no control in '{name}' has it")

    def check_name_len(self, name: str, label: str, line: int, kind: str) -> None:
        if len(name) > NAME_MAX:
            self.add("W", "name-len", label, line,
                     f"{kind} name '{name}' is {len(name)} chars; the ToA doc limits names to {NAME_MAX} (modern clients accept longer, older ones may not)")

    def check_asset_file(self, node: Node, label: str) -> None:
        file_ = node.value("File")
        if not file_:
            return
        candidates = [self.custom.parent / file_, self.custom / file_]
        if not any(c.exists() for c in candidates):
            self.add("W", "asset-file", label, node.line,
                     f"'{file_}' not found (looked relative to ui/ and to custom/)")

    def check_adapter(self, name: str, label: str, line: int) -> None:
        if name in self.k["adapters"]:
            return
        same = self.k["adapters_lower"].get(name.lower())
        if same:
            self.add("E", "adapter", label, line,
                     f"adapter '{name}' differs only by case from known '{sorted(same)[0]}'; adapter names are case sensitive")
        else:
            self.add("W", "adapter", label, line, f"adapter '{name}' is not in the official or observed lists")

    def check_event(self, name: str, label: str, line: int) -> None:
        if name.lower() not in self.k["events_lower"]:
            self.add("W", "event", label, line, f"event '{name}' is not in the official or observed lists")

    def resolve_includes(self, files: dict[str, Path]) -> None:
        for rel, incs in self.includes.items():
            src = files.get(rel)
            if src is None:
                continue
            in_custom = self.custom in src.parents
            if not in_custom:
                continue
            label = src.relative_to(self.custom).as_posix()
            for target, line in incs:
                tl = target.replace("\\", "/").lower()
                if tl in files or (self.custom / target).exists() or (self.base and (self.base / target).exists()):
                    continue
                self.add("E" if self.base else "W", "include", label, line,
                         f"<Include>{target}</Include> not found in custom/" + ("" if self.base else " (ok only if it exists in ui/atlantis)"))

    def resolve_refs(self) -> None:
        # Duplicates are keyed by (type, name): stock legitimately reuses a name across types
        # (Font and ButtonTemplate 'button_small', Texture and CompassControlTemplate 'compass').
        for (kind, name), defs in self.defined_typed.items():
            if len(defs) > 1 and any(ic for _, _, ic in defs):
                first = defs[0]
                for label, line, in_custom in defs[1:]:
                    if not in_custom and not first[2]:
                        continue  # both copies are stock: not the user's problem
                    same_file = label == first[0]
                    self.add("W" if same_file else "I", "dup-name", label, line,
                             f"{kind} '{name}' already defined in {first[0]}:{first[1]}; the later definition wins"
                             + ("" if same_file else " (fine if you meant to override it, or if only one file is Included)"))
        for name, locs in self.windows.items():
            if len(locs) > 1 and any(ic for _, _, ic in locs):
                for label, line, in_custom in locs[1:]:
                    if not in_custom and not locs[0][2]:
                        continue
                    same_file = label == locs[0][0]
                    self.add("W" if same_file else "I", "dup-name", label, line,
                             f"window '{name}' already defined in {locs[0][0]}:{locs[0][1]}; windows cannot be duplicated"
                             + ("" if same_file else " (fine if you meant to override it, or if only one file is Included)"))
        level = "E" if self.base else "W"
        suffix = "" if self.base else " (may be defined in ui/atlantis; pass --base to be sure)"
        stock_fonts = {"arial9", "arial11", "arial14"}  # the client's resize fonts; the doc requires them to exist
        for kind, name, label, line in self.refs:
            nl = name.lower()
            if kind == "template" and nl not in self.defined:
                self.add(level, "template", label, line, f"template '{name}' is not defined anywhere{suffix}")
            elif kind == "font" and nl not in self.fonts and nl not in stock_fonts:
                self.add(level, "template", label, line, f"font '{name}' is not defined by any <Font>/<TTFFont>{suffix}")
            elif kind == "texture" and nl not in self.textures:
                self.add(level, "template", label, line, f"texture '{name}' is not defined by any <Texture>{suffix}")
            elif kind == "window" and nl not in self.windows:
                self.add(level, "template", label, line, f"context window '{name}' is not defined by any WindowTemplate{suffix}")

    def check_orphans(self, files: dict[str, Path]) -> None:
        included = {t.replace("\\", "/").lower() for incs in self.includes.values() for t, _ in incs}
        for rel, path in files.items():
            if self.custom not in path.parents:
                continue
            if re.fullmatch(r"custom\d+_window\.xml", rel) and rel not in included:
                self.add("W", "orphan", rel, 0, "custom window file is not <Include>d by any file, so the client will never load it")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("custom", type=Path)
    ap.add_argument("--base", type=Path, default=None, help="stock skin folder, usually <game>/ui/atlantis")
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--quiet-info", action="store_true", help="hide I-level findings")
    args = ap.parse_args()
    if not args.custom.is_dir():
        sys.stderr.write(f"not a directory: {args.custom}\n")
        return 2
    if args.base and not args.base.is_dir():
        sys.stderr.write(f"--base is not a directory: {args.base}\n")
        return 2
    if not args.base:
        # Prefer the sibling atlantis folder of the custom folder, then the default live install.
        for cand in (args.custom.resolve().parent / "atlantis",
                     Path(r"C:\Program Files (x86)\Electronic Arts\Dark Age of Camelot\ui\atlantis")):
            if (cand / "styles.xml").exists():
                args.base = cand
                if not args.json:
                    print(f"(using --base {cand} found automatically; pass --base to override)")
                break
    lint = Linter(args.custom.resolve(), args.base.resolve() if args.base else None, load_knowledge())
    lint.run()
    order = {"E": 0, "W": 1, "I": 2}
    findings = sorted(lint.findings, key=lambda f: (order[f.level], f.file, f.line))
    if args.quiet_info:
        findings = [f for f in findings if f.level != "I"]
    if args.json:
        print(json.dumps([f.__dict__ for f in findings], indent=1))
    else:
        for f in findings:
            print(f)
        counts = {lvl: sum(1 for f in lint.findings if f.level == lvl) for lvl in "EWI"}
        print(f"\n{len(lint.trees)} files checked: {counts['E']} errors, {counts['W']} warnings, {counts['I']} info")
    bad = any(f.level == "E" for f in lint.findings) or (args.strict and any(f.level == "W" for f in lint.findings))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
