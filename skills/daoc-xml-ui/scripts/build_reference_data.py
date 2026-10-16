#!/usr/bin/env python3
"""Build reference inventories from a real DAoC custom UI folder.

The official XML UI document is Trials-of-Atlantis era and omits most of
what the modern client accepts. The most reliable way to learn what the
client actually parses is to inventory a complete, working custom UI
(e.g. a clone of https://github.com/CynicalJedi/DAOC-UI-Chooser, folder
``custom/``). This script does that and writes JSON files that

* ``daoc_ui_lint.py`` uses as its "known identifiers" lists, and
* the ``references/*.md`` files were generated from.

Only identifiers (element names, adapter/event names, numeric ids) are
extracted. No textures, fonts, or file contents are copied.

Usage:
    python build_reference_data.py <path-to-custom-folder> [--out DIR]

Outputs (in --out, default ./data next to this script):
    templates.json   top-level *Template element types -> fields + counts
    defs.json        *Def element types found inside WindowTemplate -> fields
    window_fields.json  fields seen directly under WindowTemplate
    adapters.json    adapter name -> {count, windows, bound_by}
    events.json      event name  -> {count, windows, fired_by}
    windows.json     window template name -> file, WindowId, size, numeric ControlIds
    assets.json      Font/TTFFont/Texture asset names and file extensions
    summary.json     headline counts
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from xml.etree import ElementTree as ET

ADAPTER_FIELDS = {
    "adaptername", "adapter", "coloradapter", "textadaptername", "buffername",
    "labeladaptername", "stateadaptername",
}
EVENT_FIELD_RE = re.compile(r"event$", re.IGNORECASE)
ASSET_TAGS = {"font", "ttffont", "texture", "canvas"}


def parse_file(path: Path) -> ET.Element | None:
    """Parse leniently: the client is forgiving, hand-edited files often are not."""
    raw = path.read_bytes()
    for enc in ("iso-8859-1", "utf-8", "cp1252"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        return None
    # Strip BOM and any junk before the first '<'
    text = text.lstrip("\ufeff")
    first = text.find("<")
    if first > 0:
        text = text[first:]
    # Drop the encoding declaration; we already decoded to str.
    text = re.sub(r"^<\?xml[^>]*\?>", "", text.strip(), count=1)
    # Bare ampersands are common in labels and break strict parsers.
    text = re.sub(r"&(?!(amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)", "&amp;", text)
    try:
        return ET.fromstring(text)
    except ET.ParseError as exc:  # noqa: PERF203
        sys.stderr.write(f"WARN  unparseable {path.name}: {exc}\n")
        return None


def text_of(el: ET.Element) -> str:
    return (el.text or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("custom_dir", type=Path, help="path to a ui/custom folder")
    ap.add_argument("--out", type=Path, default=Path(__file__).parent / "data")
    ap.add_argument("--exclude", default="Options", help="comma-separated top-level subfolders to skip (default: Options)")
    args = ap.parse_args()

    root_dir: Path = args.custom_dir
    if not root_dir.is_dir():
        sys.stderr.write(f"not a directory: {root_dir}\n")
        return 2
    excluded = {e.strip().lower() for e in args.exclude.split(",") if e.strip()}

    templates: dict[str, dict] = defaultdict(lambda: {"count": 0, "fields": Counter(), "names": set()})
    defs: dict[str, dict] = defaultdict(lambda: {"count": 0, "fields": Counter()})
    window_fields: Counter = Counter()
    adapters: dict[str, dict] = defaultdict(lambda: {"count": 0, "windows": set(), "bound_by": Counter()})
    events: dict[str, dict] = defaultdict(lambda: {"count": 0, "windows": set(), "fired_by": Counter()})
    windows: dict[str, dict] = {}
    assets: dict[str, dict] = defaultdict(lambda: {"count": 0, "extensions": Counter(), "names": set()})
    includes: dict[str, list[str]] = {}
    files_total = files_parsed = 0

    for path in sorted(root_dir.rglob("*.xml")):
        rel = path.relative_to(root_dir)
        if rel.parts and rel.parts[0].lower() in excluded:
            continue
        files_total += 1
        root = parse_file(path)
        if root is None:
            continue
        files_parsed += 1
        includes[str(rel).replace("\\", "/")] = [text_of(e) for e in root if e.tag.lower() == "include"]

        for top in root:
            tag = top.tag
            low = tag.lower()
            if low == "include":
                continue
            if low in ASSET_TAGS:
                entry = assets[tag]
                entry["count"] += 1
                name = text_of(top.find("Name")) if top.find("Name") is not None else ""
                file_ = text_of(top.find("File")) if top.find("File") is not None else ""
                if name:
                    entry["names"].add(name)
                if file_:
                    entry["extensions"][Path(file_).suffix.lower()] += 1
                continue
            if low == "windowtemplate":
                wname = ""
                winfo = {"file": str(rel).replace("\\", "/"), "WindowId": "", "Width": "", "Height": "",
                         "numeric_control_ids": set(), "defs": Counter()}
                for child in top:
                    ctag = child.tag
                    if ctag.lower().endswith("def"):
                        d = defs[ctag]
                        d["count"] += 1
                        for f in child:
                            d["fields"][f.tag] += 1
                            fl = f.tag.lower()
                            val = text_of(f)
                            if fl in ADAPTER_FIELDS and val:
                                a = adapters[val]
                                a["count"] += 1
                                a["windows"].add(str(rel).replace("\\", "/"))
                                a["bound_by"][f"{ctag}.{f.tag}"] += 1
                            elif EVENT_FIELD_RE.search(fl) and val:
                                ev = events[val]
                                ev["count"] += 1
                                ev["windows"].add(str(rel).replace("\\", "/"))
                                ev["fired_by"][f"{ctag}.{f.tag}"] += 1
                            elif fl == "controlid" and val.isdigit():
                                winfo["numeric_control_ids"].add(int(val))
                        winfo["defs"][ctag] += 1
                    else:
                        window_fields[ctag] += 1
                        if ctag.lower() == "name":
                            wname = text_of(child)
                        elif ctag in ("WindowId", "Width", "Height"):
                            winfo[ctag] = text_of(child)
                if wname:
                    winfo["numeric_control_ids"] = sorted(winfo["numeric_control_ids"])
                    winfo["defs"] = dict(winfo["defs"])
                    windows[wname] = winfo
                continue
            if low.endswith("template"):
                t = templates[tag]
                t["count"] += 1
                for f in top:
                    t["fields"][f.tag] += 1
                    if f.tag.lower() == "name":
                        t["names"].add(text_of(f))
                continue
            # Anything else at top level is worth knowing about.
            templates[f"(unknown top-level) {tag}"]["count"] += 1

    def finalize(d: dict) -> dict:
        out = {}
        for k, v in sorted(d.items()):
            item = {}
            for kk, vv in v.items():
                if isinstance(vv, Counter):
                    item[kk] = dict(vv.most_common())
                elif isinstance(vv, set):
                    item[kk] = sorted(vv)
                else:
                    item[kk] = vv
            out[k] = item
        return out

    args.out.mkdir(parents=True, exist_ok=True)
    dump = {
        "templates.json": finalize(templates),
        "defs.json": finalize(defs),
        "window_fields.json": dict(window_fields.most_common()),
        "adapters.json": finalize(adapters),
        "events.json": finalize(events),
        "windows.json": dict(sorted(windows.items())),
        "assets.json": finalize(assets),
        "includes.json": includes,
    }
    for name, payload in dump.items():
        (args.out / name).write_text(json.dumps(payload, indent=1, sort_keys=False), encoding="utf-8")

    summary = {
        "source": str(root_dir),
        "files_scanned": files_total,
        "files_parsed": files_parsed,
        "template_types": len([k for k in templates if not k.startswith("(")]),
        "def_types": len(defs),
        "adapter_names": len(adapters),
        "event_names": len(events),
        "window_templates": len(windows),
    }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
