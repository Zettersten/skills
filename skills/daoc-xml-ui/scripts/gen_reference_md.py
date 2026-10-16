#!/usr/bin/env python3
"""Render references/adapters.md, references/events.md and references/windows.md
from the JSON inventories in scripts/data (official.json + observed *.json).

Re-run after `build_reference_data.py` whenever the corpus changes:
    python gen_reference_md.py [--out ../references]
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
STOCK = DATA / "stock"  # inventory of a real ui/atlantis folder (client 1.130), authoritative where present


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def load_stock(name: str) -> dict:
    p = STOCK / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def expand(pattern: str) -> list[str]:
    m = re.search(r"\{(\d+)-(\d+)\}", pattern)
    if not m:
        return [pattern]
    out = []
    for i in range(int(m.group(1)), int(m.group(2)) + 1):
        out.extend(expand(pattern[: m.start()] + str(i) + pattern[m.end():]))
    return out


def collapse(names: list[str]) -> list[tuple[str, list[str]]]:
    """Group names that differ only in digit runs: returns [(pattern, members)]."""
    groups: dict[str, list[str]] = defaultdict(list)
    for n in names:
        key = re.sub(r"\d+", "#", n)
        groups[key].append(n)
    out = []
    for key, members in groups.items():
        if len(members) < 3 or "#" not in key:
            for m in members:
                out.append((m, [m]))
            continue
        slots = key.count("#")
        mins = [10**9] * slots
        maxs = [-1] * slots
        for m in members:
            nums = [int(x) for x in re.findall(r"\d+", m)]
            for i, v in enumerate(nums[:slots]):
                mins[i] = min(mins[i], v)
                maxs[i] = max(maxs[i], v)
        pat = key
        for i in range(slots):
            pat = pat.replace("#", f"{{{mins[i]}-{maxs[i]}}}", 1)
        out.append((pat, sorted(members)))
    return sorted(out, key=lambda t: t[0])


# ----------------------------------------------------------------------------- adapters
# (def type, field) -> adapter kind. '*' matches any def type. Keys are lower-case.
TYPE_BY_BINDING = {
    ("chatcontroldef", "buffername"): "chat buffer",
    ("*", "coloradapter"): "color",
    ("scalarlabeldef", "adapter"): "scalar",
    ("statusbardef", "adaptername"): "scalar 0-100",
    ("verticalstatusbardef", "adaptername"): "scalar 0-100",
    ("statusicondef", "adaptername"): "scalar 0-100",
    ("horizontalsliderdef", "adaptername"): "scalar",
    ("verticalsliderdef", "adaptername"): "scalar",
    ("checkboxdef", "adaptername"): "scalar 0/1",
    ("checkboxdef", "textadaptername"): "text",
    ("icondef", "adaptername"): "scalar (icon id)",
    ("icondef", "stateadaptername"): "scalar (icon state)",
    ("icondef", "labeladaptername"): "text",
    ("labeldef", "adapter"): "text",
    ("textareadef", "adaptername"): "text (multi-line)",
    ("editboxdef", "adaptername"): "text",
    ("listboxdef", "adaptername"): "list",
    ("treecontroldef", "adaptername"): "list (tree)",
    ("comboboxdef", "adaptername"): "list",
    ("buttondef", "adapter"): "text",
    ("compasscontroldef", "adaptername"): "scalar (heading)",
}


def infer_type(bound_by: dict[str, int]) -> str:
    kinds: list[str] = []
    for key in sorted(bound_by, key=lambda k: -bound_by[k]):
        d, _, f = key.partition(".")
        kind = TYPE_BY_BINDING.get((d.lower(), f.lower())) or TYPE_BY_BINDING.get(("*", f.lower()))
        if kind and kind not in kinds:
            kinds.append(kind)
    return " / ".join(kinds) if kinds else "?"


def prefix_of(name: str) -> str:
    base = re.sub(r"\d+", "", name)
    first = base.split("_")[0]
    return first or name


def gen_adapters(out_dir: Path) -> None:
    off = load("official.json")
    obs = load("adapters.json")
    stock = load_stock("adapters.json")
    # merge stock bindings into the observed map so types/bindings/files come from both
    for n, info in stock.items():
        tgt = obs.setdefault(n, {"count": 0, "windows": [], "bound_by": {}})
        tgt["count"] += info["count"]
        tgt["windows"] = sorted(set(tgt["windows"]) | {"atlantis/" + w for w in info["windows"]})
        for b, c in info["bound_by"].items():
            tgt["bound_by"][b] = tgt["bound_by"].get(b, 0) + c
    official_type: dict[str, str] = {}
    for typ, names in off["adapters"].items():
        for pat in names:
            for n in expand(pat):
                official_type.setdefault(n, typ)
    all_names = set(official_type) | set(obs)
    by_prefix: dict[str, list[str]] = defaultdict(list)
    for n in all_names:
        by_prefix[prefix_of(n)].append(n)

    lines = [
        "# Adapter reference",
        "",
        "Adapters are the named live-data slots the client exposes to the UI. A control binds to one by name",
        "(`<Adapter>`, `<AdapterName>`, `<ColorAdapter>`, `<TextAdapterName>`, `<BufferName>`, `<LabelAdapterName>`,",
        "`<StateAdapterName>`). **Adapter names are case sensitive** (everything else in the XML is not).",
        "",
        "Three sources are merged here:",
        "",
        "- **official** = listed in the Trials of Atlantis XML UI document (types are authoritative).",
        "- **stock** = bound by a control in the stock Atlantis skin of the live 1.130 client (`ui/atlantis`). Authoritative",
        "  for what the current client exposes; files are shown with an `atlantis/` prefix.",
        "- **observed** = bound by a control in a complete, working 1.127-era custom UI",
        "  (CynicalJedi/DAOC-UI-Chooser). The type is inferred from the control that binds it, so treat it as a strong hint.",
        "",
        "Numbered series are collapsed: `group_name{0-7}` means `group_name0` .. `group_name7`.",
        "The bind column tells you which control types a working UI uses for it, which is the practical answer to",
        "\"what do I put this in?\". Status bars and status icons need a scalar that ranges 0-100.",
        "",
        f"Totals: {len(official_type)} official names, {len(obs)} observed names, {len(all_names)} distinct.",
        "",
        "## Contents",
        "",
    ]
    prefixes = sorted(by_prefix, key=lambda p: (-len(by_prefix[p]), p))
    prefixes = sorted(by_prefix)
    for p in prefixes:
        lines.append(f"- [{p}](#{p.lower()}) ({len(by_prefix[p])})")
    lines.append("")
    for p in prefixes:
        lines.append(f"## {p}")
        lines.append("")
        lines.append("| adapter | type | source | bound by (observed) | seen in |")
        lines.append("|---|---|---|---|---|")
        for pat, members in collapse(sorted(by_prefix[p])):
            srcs = set()
            types = set()
            bound = defaultdict(int)
            files = set()
            for m in members:
                if m in official_type:
                    srcs.add("official")
                    types.add(official_type[m])
                if m in stock:
                    srcs.add("stock")
                if m in obs:
                    if m not in stock or obs[m]["count"] > stock[m]["count"]:
                        srcs.add("observed")
                    for b, c in obs[m]["bound_by"].items():
                        bound[b.split(".")[0]] += c
                    files.update(obs[m]["windows"])
            if not types:
                merged = defaultdict(int)
                for m in members:
                    if m in obs:
                        for b, c in obs[m]["bound_by"].items():
                            merged[b] += c
                types.add(infer_type(merged))
            seen = ", ".join(sorted(files)[:3]) + (" ..." if len(files) > 3 else "")
            bound_s = ", ".join(f"{k}" for k, _ in sorted(bound.items(), key=lambda kv: -kv[1])[:4])
            lines.append(f"| `{pat}` | {' / '.join(sorted(types))} | {'+'.join(sorted(srcs))} | {bound_s or '-'} | {seen or '-'} |")
        lines.append("")
    notes = off.get("adapter_notes", {})
    if notes:
        lines.append("## Notes from the official document")
        lines.append("")
        for k, v in notes.items():
            lines.append(f"- `{k}`: {v}")
        lines.append("")
    (out_dir / "adapters.md").write_text("\n".join(lines), encoding="utf-8")


# ----------------------------------------------------------------------------- events
def gen_events(out_dir: Path) -> None:
    off = load("official.json")
    obs = load("events.json")
    stock = load_stock("events.json")
    for n, info in stock.items():
        tgt = obs.setdefault(n, {"count": 0, "windows": [], "fired_by": {}})
        tgt["count"] += info["count"]
        tgt["windows"] = sorted(set(tgt["windows"]) | {"atlantis/" + w for w in info["windows"]})
    official: dict[str, tuple[str, str]] = {}
    for group, items in off["events"].items():
        for pat, desc in items.items():
            for n in expand(pat):
                official[n] = (group, desc)
    obs_lower = {k.lower(): k for k in obs}
    lines = [
        "# Event reference",
        "",
        "Events are what buttons fire: `<OnClickEvent>Name</OnClickEvent>` on a `ButtonDef`, `InvisibleButtonDef`,",
        "`HorizontalResizeButtonDef`, `HorizontalResizeImageButtonDef`, `CheckBoxDef`, `IconDef`, slider or `ListBoxDef`",
        "(`OnClickEvent`, `OnHeaderClickEvent`), and `ComboBoxDef` (`OnChangeEvent`). Event names are not case sensitive.",
        "",
        "The XML cannot define new behaviour: an event only works if the client implements it. Some events need",
        "state the window owns (a selected list row, a chosen pet mode) and only make sense inside that window.",
        "",
        "- **official** = in the Trials of Atlantis document, with its description.",
        "- **observed** = wired to a control in the stock Atlantis skin of the live 1.130 client (files prefixed `atlantis/`)",
        "  or in a complete, working 1.127-era custom UI (CynicalJedi/DAOC-UI-Chooser).",
        "  No official description exists; the name and the window it is used in are the documentation.",
        "",
        f"Totals: {len(official)} official, {len(obs)} observed, "
        f"{len(set(official) | set(obs))} distinct.",
        "",
        "## Contents",
        "",
        "- [Window toggles (observed)](#window-toggles-observed)",
        "- [Custom windows](#custom-windows)",
    ]
    for group in off["events"]:
        anchor = re.sub(r"[^a-z0-9]+", "-", group.lower()).strip("-")
        lines.append(f"- [{group} (official)](#{anchor}-official)")
    lines.append("- [Other observed events](#other-observed-events)")
    lines.append("")

    toggles = sorted(n for n in obs if n.lower().startswith("toggle") and not re.match(r"togglecustom\d+", n.lower()))
    lines += ["## Window toggles (observed)", "",
              "`Toggle*` events open/close a specific window. Put one on a button anywhere (command window, your own",
              "menu window) to get a launcher. Names are what the client ships; the table shows where a working UI wires them.", "",
              "| event | fired from |", "|---|---|"]
    for n in toggles:
        if n in official:
            continue
        files = ", ".join(sorted(obs[n]["windows"])[:3])
        lines.append(f"| `{n}` | {files} |")
    lines += ["", "## Custom windows", "",
              "`ToggleCustom0` .. `ToggleCustom19` open the user window templates named `custom0_window` .. `custom19_window`",
              "(by convention in `custom0_window.xml` .. `custom19_window.xml`, `<Include>`d from `assets.xml`).",
              "This is the only mechanism for adding a brand-new window; see SKILL.md recipe \"add a custom window\".", ""]
    for group, items in off["events"].items():
        anchor_title = f"{group} (official)"
        lines += [f"## {anchor_title}", "", "| event | what it does | also observed |", "|---|---|---|"]
        for pat, desc in items.items():
            seen = any(n.lower() in obs_lower for n in expand(pat))
            lines.append(f"| `{pat}` | {desc} | {'yes' if seen else '-'} |")
        lines.append("")
    other = sorted(n for n in obs if n not in official and n.lower() not in {o.lower() for o in official}
                   and not n.lower().startswith("toggle"))
    lines += ["## Other observed events", "",
              "Grouped by prefix. `fired from` lists up to three files from the reference UI.", ""]
    by_prefix: dict[str, list[str]] = defaultdict(list)
    for n in other:
        m = re.match(r"([A-Z][a-z]+)", n)
        by_prefix[m.group(1) if m else n].append(n)
    for p in sorted(by_prefix):
        lines += [f"### {p}", "", "| event | fired from |", "|---|---|"]
        for pat, members in collapse(sorted(by_prefix[p])):
            files = set()
            for m in members:
                files.update(obs[m]["windows"])
            lines.append(f"| `{pat}` | {', '.join(sorted(files)[:3])} |")
        lines.append("")
    (out_dir / "events.md").write_text("\n".join(lines), encoding="utf-8")


# ----------------------------------------------------------------------------- windows
def window_rows(w: dict) -> list[str]:
    rows = []
    for name, info in sorted(w.items()):
        ids = info["numeric_control_ids"]
        if not ids:
            ids_s = "-"
        elif len(ids) <= 6:
            ids_s = ", ".join(map(str, ids))
        else:
            ids_s = f"{ids[0]}..{ids[-1]} ({len(ids)} ids)"
        defs = ", ".join(f"{k}x{v}" for k, v in sorted(info["defs"].items(), key=lambda kv: -kv[1])[:5])
        rows.append(f"| `{name}` | {info['WindowId'] or '-'} | `{info['file']}` | {info['Width']}x{info['Height']} | {ids_s} | {defs} |")
    return rows


def gen_windows(out_dir: Path) -> None:
    w = load("windows.json")
    inc = load("includes.json")
    sw = load_stock("windows.json")
    sinc = load_stock("includes.json")
    lines = [
        "# Window reference",
        "",
        "Two tables. The **stock** table is the Atlantis skin of the live 1.130 client (`ui/atlantis`, 83 files) and is",
        "authoritative: the sizes are what the game ships, and the numeric `ControlId`s are the ones client code binds",
        "(do not reuse them when adding controls to that window). The **BobsUI** table is a complete 1.127-era custom UI",
        "(CynicalJedi/DAOC-UI-Chooser); its sizes and ids are that UI's own choices and it adds 20 custom windows.",
        "Use both to answer: what is the file for window X, what is its template `Name`, what size does it have, and",
        "which ids are taken.",
        "",
        "Rules that matter here:",
        "",
        "- The template `Name` is how the client finds a window. Keep the stock name when you restyle a stock window.",
        "- `WindowId` is mostly a label (the doc says it is used for debugging). Custom windows use anything.",
        "- Numeric `ControlId`s inside stock windows may be bound by client code (the doc warns not to reuse them).",
        "  Inside custom windows they are yours; `TabsDef` uses them to assign controls to tabs.",
        "- Files that are not in your `custom/` folder are loaded from `ui/atlantis/`, so you only ship what you change.",
        "- `custom0_window` .. `custom19_window` are the user slots (see events.md, `ToggleCustomN`). In BobsUI they are",
        "  used for its main menu, floating bars, command bar, tabbed XP, atlas, etc.; a fresh skin can use them freely.",
        "",
        "## Contents",
        "",
        "- [Stock windows (Atlantis, client 1.130)](#stock-windows-atlantis-client-1130)",
        "- [Stock load order (uimain.xml)](#stock-load-order-uimainxml)",
        "- [BobsUI windows (1.127 custom UI)](#bobsui-windows-1127-custom-ui)",
        "- [Files that are not windows](#files-that-are-not-windows)",
        "- [Include graph](#include-graph)",
        "",
    ]
    if sw:
        lines += ["## Stock windows (Atlantis, client 1.130)", "",
                  "| template Name | WindowId | file | WxH | numeric ControlIds (code-bound) | control defs |",
                  "|---|---|---|---|---|---|"]
        lines += window_rows(sw)
        lines.append("")
        uimain = HERE.parent / "references" / "_uimain_order.txt"
        lines += ["## Stock load order (uimain.xml)", "",
                  "`ui/uimain.xml` (never edit) includes these files in this order; `styles.xml` first, `assets.xml` near the end.",
                  "Each is resolved in `ui/custom/` first, then `ui/atlantis/`. Custom windows are not in this list, which is",
                  "why they need an `<Include>` from one of these files.", ""]
        if uimain.exists():
            lines.append(", ".join(f"`{x}`" for x in uimain.read_text(encoding="utf-8").split()))
        else:
            lines.append("(uimain order not captured; read the file in the game folder)")
        lines.append("")
    lines += ["## BobsUI windows (1.127 custom UI)", "",
              "| template Name | WindowId | file | WxH | numeric ControlIds used | control defs |",
              "|---|---|---|---|---|---|"]
    lines += window_rows(w)
    lines.append("")
    window_files = {info["file"] for info in w.values()}
    others = sorted(f for f in inc if f not in window_files)
    lines += ["## Files that are not windows", "",
              "Template/asset collections. `styles.xml` and `assets.xml` are the two the client always loads;",
              "everything else is pulled in by an `<Include>`.", ""]
    for f in others:
        lines.append(f"- `{f}`" + (f" includes {len(inc[f])} files" if inc[f] else ""))
    lines += ["", "## Include graph", "", "Files that include other files (reference UI):", ""]
    for f, targets in sorted(inc.items()):
        if targets:
            lines.append(f"- `{f}` -> " + ", ".join(f"`{t}`" for t in targets))
    lines.append("")
    (out_dir / "windows.md").write_text("\n".join(lines), encoding="utf-8")


def gen_stock_templates(out_dir: Path) -> None:
    st = load_stock("templates.json")
    sa = load_stock("assets.json")
    if not st:
        return
    lines = [
        "# Stock template, font and texture names (Atlantis skin, client 1.130)",
        "",
        "When a mod builds on the stock skin, these are the names it can reference without defining anything. They come",
        "from the shipped `ui/atlantis` files (mostly `styles.xml` and `assets.xml`). Names are not case sensitive.",
        "Templates defined inside a window file (e.g. `generic_editbox` in `bazaar_query.xml`) only exist while that",
        "file is loaded, which it always is on stock, but a custom override of that file must re-define them.",
        "",
        "Quick picks: status bars `red_status` / `green_status` / `blue_status` / `yellow_status` (plus `_small`/`_thick`",
        "variants, `exp_bubbles`); window backgrounds `dlg_sm_title`, `dlg_sm_notitle`, `dlg_background_resize`,",
        "`dlg_background_noresize`, insets `dlg_interior_small` / `dlg_interior_large`; buttons `button_small` (60x16),",
        "`button_large`, `button_wide`, `button_narrow`, `button_nobg`, resizable `generic_hr_button`; fonts `arial9`,",
        "`arial11`, `arial14`, `button_small`, `button_large`, `brit9`, `title`, `barb10`, TrueType `chat_small`,",
        "`chat_large`, `minion`, `myriadbold`.",
        "",
        "## Contents",
        "",
        "- [Fonts and textures](#fonts-and-textures)",
        "- [Templates by type](#templates-by-type)",
        "",
        "## Fonts and textures",
        "",
    ]
    for kind, info in sa.items():
        lines.append(f"- **{kind}** ({info['count']}, {', '.join(f'{k} x{v}' for k, v in info['extensions'].items())}): "
                     + ", ".join(f"`{n}`" for n in sorted(info["names"])))
    lines += ["", "Icon sheets are `<Canvas>` assets named `<sheet>_b` (32px) and `<sheet>_s` (16px): `spl1..`, `itm1..`,",
              "`combat1..`, `skill1`. Font files live in `ui/fonts/`; texture sheets `page1..page4b` are the Atlantis frame art.", "",
              "## Templates by type", ""]
    for t, info in sorted(st.items()):
        names = sorted(info["names"])
        lines.append(f"### {t} ({len(names)})")
        lines.append("")
        lines.append(", ".join(f"`{n}`" for n in names))
        lines.append("")
    (out_dir / "stock-templates.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE.parent / "references")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    gen_adapters(args.out)
    gen_events(args.out)
    gen_windows(args.out)
    gen_stock_templates(args.out)
    for n in ("adapters.md", "events.md", "windows.md", "stock-templates.md"):
        if (args.out / n).exists():
            print(n, len((args.out / n).read_text(encoding="utf-8").splitlines()), "lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
