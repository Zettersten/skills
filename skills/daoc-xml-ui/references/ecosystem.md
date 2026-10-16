# Ecosystem: sources, tools, communities, and the limits of XML

## Contents

- [Primary sources, ranked by usefulness](#primary-sources-ranked-by-usefulness)
- [Complete UIs worth reading](#complete-uis-worth-reading)
- [Tools](#tools)
- [Communities](#communities)
- [Clients and versions](#clients-and-versions)
- [What breaks when the game patches](#what-breaks-when-the-game-patches)
- [When XML is the wrong tool: daochook](#when-xml-is-the-wrong-tool-daochook)
- [Support reality](#support-reality)

## Primary sources, ranked by usefulness

1. **The stock skin on disk**: `<game>\ui\atlantis\` (also `isles\`, `classic\`, `transparent\`). The authoritative
   current syntax for the client the player actually runs. Always diff against it; it changes with patches.
2. **A complete working custom UI** (next section). Shows every modern element the official doc omits.
3. **Official XML User Interface document**: https://www.darkageofcamelot.com/xml-user-interface/ (ToA era, 2003-04).
   Still correct on the model (templates, windows, defs, adapters, events, loading, fonts); incomplete on
   inventories; silent on custom windows, DDS, TTF, tabs, tooltips, context menus. Transcribed in
   `scripts/data/official.json` and folded into these references.
4. **Patch notes**: https://www.darkageofcamelot.com/patch-notes/ ("UI" sections). 1.110 added many windows;
   a March 2017 client hotfix required custom UIs to update `key_config.xml`; 1.127 changed market explorer.
5. **Camelot Herald wiki** ("How do I make my own custom UI/skins?"): only points at the doc and the UI Editor.

## Complete UIs worth reading

| UI | where | client | why read it |
|---|---|---|---|
| BobsUI / DAOC UI Chooser (Ewer's update) | https://github.com/CynicalJedi/DAOC-UI-Chooser (`custom/`) | 1.127B | The largest open corpus: 180 top-level XML files, `Styles/` split by template type, 20 custom windows in use, OptionsChooser variants under `Options/`. The inventories in `scripts/data/` were built from it. |
| Lym UI 2 | https://github.com/Lymhit/UI | 1.80 to 1.123 history | Git history shows how files changed across patches; uses `<TTFFont>`, DDS maps, `custom/fonts/*.ttf`. |
| Bysan UI | Discord only: https://discord.gg/TqX3b3G (`#releases`), ships `bysanUI.exe` style chooser | live + Eden | Most popular current UI; no public source, but the zip's `custom/` folder is readable XML. |
| nathrach mods | https://nathrach.republicofnewhome.org/uimods.html | 1.69 | Tiny single-window mods (chat clock, digital group HP, compass frames). Good minimal examples of the ToA-era shape. |
| KotRT UI | https://kotrt.eu5.org/DAoC_UI.html | ToA/Catacombs | Example of shipping per-resolution `default<width>.ini` layouts with a skin. |

Pattern shared by all of them: a `custom/` folder dropped into `<game>\ui\`, the "Custom" skin selected in the
character-select Options, and an `assets.xml` that includes everything new.

## Tools

- **`scripts/daoc_ui_lint.py`** (this skill): parse, include, template/font/texture resolution, duplicate names,
  adapter/event spelling, draw order, bounds, orphan custom windows. Pass `--base <game>\ui\atlantis` for exact
  resolution. Run it before every game launch.
- **`scripts/build_reference_data.py`** + **`gen_reference_md.py`**: rebuild the inventories from any `custom/`
  folder (for example the player's own stock `ui/atlantis`, which is the most accurate source for their client).
- **DAoC User Interface Editor** (Brad Townsend, Java): http://www.bradtownsend.com/daoced/ , v1.75 public
  (2005), v1.80 beta referenced by file banners. Visual editor for coordinates and defs, DDS preview. Legacy:
  needs an old JRE, does not know post-1.80 elements. Useful for reading texture coordinates, not required.
- **OptionsChooser.exe** (BobsUI) / **bysanUI.exe** (Bysan): copy pre-made variant files into place. If a
  player uses one, edit the variant source under `Options/`, not the live file, or the chooser overwrites it.
- **Image editors**: anything that writes 32-bit TGA with alpha (GIMP, Paint.NET, Photoshop). For DDS, a DXT
  plugin or `texconv`.
- **An XML-aware editor** with folding; files run to thousands of lines.

## Communities

- Eden freeshard forum, "User Interface" board: https://eden-daoc.net/ (install threads for BobsUI and Bysan).
- Phoenix / Uthgard forums (archived threads on `.ini` locations, `paths.dat`).
- r/daoc for current recommendations.
- The VN "ToA UI Mods" board and DAOCmods are gone; their mods survive in the repos above.

## Clients and versions

- **Live (Broadsword/EA)**: 1.129b (Sept 2025), 1.130 on Pendragon. All modern elements available.
- **Eden**: 1.127-based client; BobsUI 1.127B and Bysan both work.
- **Phoenix, Uthgard, other freeshards**: older clients (1.124 era or earlier). Elements added later may not
  exist; keep to the official set plus custom windows and test in that client.
- The same `custom/` folder generally works across these, except for files that were added or renamed by a
  patch (the client then loads the stock version of a window you did not ship, which is fine, or an old copy
  you did ship, which is the usual breakage).

## What breaks when the game patches

- A stock window gains controls (new options in `key_config.xml`, new tabs in the training window). Your copy
  of that file silently lacks them. Fix: diff your file against the new `ui/atlantis/` copy and merge.
- A stock template is renamed or moved between files. Your windows reference a name that no longer exists
  in the effective set. Fix: lint with `--base` after every patch.
- A panel becomes an XML window. Your `custom/oldstyle/` bitmap stops being used; restyle the new window instead.
- `uimain.xml` gains an include for a new file you do not ship. Nothing breaks; the stock file loads.

## When XML is the wrong tool: daochook

The XML system can only **place existing data** (adapters) and **fire existing commands** (events). It cannot do
arithmetic, timers, conditions, text parsing, or anything the client does not already expose. Requests like a
spellcraft calculator, a buff-timer overlay with countdowns, a damage meter, or "colour the bar red under 30%"
need code, and the community's answer is **daochook**:

- https://github.com/daochook/daochook and https://daochook.github.io/ (atom0s, AGPL v3).
- Injects into `game.dll`, hooks the command, chat and packet handlers plus Direct3D, exposes **Lua (LuaJIT)**
  addons and **ImGui** for custom in-game UI. Needs the 32-bit MSVC 2022 redist. Supports client `1.127e [1409]`.
- Developed against private servers; it is a client modification, so check the rules of the server you play on
  before recommending it for live.
- It does not touch `ui/custom`; an XML skin and daochook addons coexist.

If the ask is cosmetic, layout, readouts of existing values, or launcher buttons: stay in XML. If it needs logic:
point at daochook and stop.

## Support reality

Broadsword CSRs do not help with custom UIs; `/appeal` only for bugs. The doc itself tells players not to attempt
skins without the skills. Set expectations: every change is a text edit plus a relog (logging out to character
select and back in reloads the XML; BobsUI's notes say re-zoning is enough after swapping option files; new
textures and fonts want a full client restart). The only diagnostics are `ui.log` (missing files) and your own eyes.
