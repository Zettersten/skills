---
name: daoc-xml-ui
description: Author, modify, debug and restyle Dark Age of Camelot (DAoC) user interfaces: the XML "custom UI" system (ui/custom, WindowTemplate, control templates, adapters, events, custom0..19 windows, textures, fonts) used by live DAoC and freeshards (Eden, Phoenix, Uthgard) and by UIs such as BobsUI/UI Chooser, Bysan UI and Lym. Use this skill whenever the user mentions DAoC, Camelot, Broadsword/Mythic, Eden-DAoC, a daoc "custom UI", "UI mod", "skin", "interface", a file under ui\custom or ui\atlantis, chat_window.xml / minigroup_window.xml / command_window.xml / styles.xml / assets.xml, adapters like summary_target_hits, events like ToggleCustom1, moving or adding a health bar, group window, compass, clock, chat font, target window, floating bars, or asks why a window/button/control does not show up in game. Also use it to tell XML work apart from client add-ons (daochook Lua/ImGui) and to lint a custom folder before launching the game.
license: MIT
metadata:
  version: "1.0"
  sources: official XML UI doc (ToA era) + inventories from working 1.127 UIs; see references/ecosystem.md
---

# Dark Age of Camelot XML UI

DAoC's interface is data-driven XML: windows are `WindowTemplate`s made of control definitions, controls are
drawn from control templates (texture cut-outs + fonts), live values arrive through named **adapters**, and buttons
fire named **events**. The official document is from 2003 and omits most of what the current client accepts; the
bundled references were rebuilt from complete working UIs, so trust them over memory.

## Triage first

1. **Cosmetic, layout, readouts of existing values, launcher buttons, new arrangement of windows** -> XML, this skill.
2. **Logic** (calculators, countdown timers, flashing/animation, parsing chat, damage meters, anything computed) ->
   XML cannot do it. Say so plainly and point at daochook (`references/ecosystem.md`, last section). Do not fake it.
   One exception worth offering: "different look below X%" is approximable without logic, because a
   `StatusIconDef` picks a texture frame from the 0-100 value (recipe below). Flashing and timers are not.
3. **Positions of windows / quickbar contents / macros** -> not XML; per-character `.ini` files
   (`references/assets-fonts-textures.md`, last section).
4. Ask which client (live 1.129, Eden 1.127, older freeshard) and which base UI (stock Atlantis, BobsUI, Bysan)
   only if the answer changes the file you touch. Default to live/Eden and a stock Atlantis base.

## Rules that are not negotiable

- Work only in `<game>\ui\custom\` with the **Custom** skin selected at character select. Never edit `ui\uimain.xml`.
- A file in `custom\` **replaces** its stock twin from `ui\atlantis\` entirely; a file you do not ship is loaded
  from stock. So copy the stock file, then edit; never write a stock-named file from scratch.
- New files load only when something `<Include>`s them. New windows live only in slots `custom0_window` ..
  `custom19_window` (file `customN_window.xml`, event `ToggleCustomN`).
- Controls draw and receive clicks in XML order. Background first, invisible click areas last.
- Adapter names are case sensitive. Everything else (elements, template names, events) is not.
- Status bars and status icons need a 0-100 scalar adapter. Labels show text adapters; `ScalarLabelDef` shows numbers.
- There is no reload command. Edit, run the linter, log to character select and back in (full relaunch after
  texture or font changes).

## Setup checklist

```text
<game>\ui\custom\            <- your files (create it)
<game>\ui\custom\oldstyle\   <- only for repainting non-XML panels (inventory, quickbars...)
<game>\ui\atlantis\          <- stock skin: the source of truth for the player's client version; read, never edit
%APPDATA%\Electronic Arts\Dark Age of Camelot\<server>\Name-<id>.ini   <- window positions, per character
```

Before editing anything, open the stock copy of the target file in `ui\atlantis\` (or the user's current UI if they
run BobsUI/Bysan) and `styles.xml`/`assets.xml` to learn the template and font names that skin actually defines.
Names differ between skins; `references/windows.md` tells you which file holds which window. The sizes and
ControlIds listed there are BobsUI's, so quote them as "in BobsUI", never as stock dimensions; the stock numbers
are whatever the player's `ui\atlantis` file says. When you cannot read that file, say so and give positions as
estimates relative to the window's own `Width`/`Height`.

## The model in one screen

```text
assets.xml        <Texture>/<Font>/<TTFFont>  name -> file            (sheets, fonts)
styles.xml        <*Template>                  name -> how to draw     (ButtonTemplate, FullResizeImageTemplate, StatusBarTemplate...)
<win>_window.xml  <WindowTemplate>             Name, size, flags, then <*Def> children in draw order
                    <*Def>                     Position/Alignment + TemplateName + Adapter/AdapterName + OnClickEvent
client            adapters (live data, read-only to you)   events (commands the client implements)
```

Full skeletons with every field: `references/xml-syntax.md`. Field tables: `references/control-templates.md`,
`references/control-defs.md`. Names: `references/adapters.md`, `references/events.md`, `references/windows.md`.

## Workflow for any change

1. Identify the window file (`references/windows.md`) and whether the control exists already.
2. Copy the stock file into `custom\` if it is not there yet. Keep the stock `Name`, `WindowId` and every numeric
   `ControlId` the stock file uses.
3. Make the edit (recipes below). Keep every window attribute present, even zeros; shipping UIs do.
4. Run `python scripts/daoc_ui_lint.py <game>\ui\custom --base <game>\ui\atlantis` and fix errors; read warnings.
5. Relog. If nothing changed, you edited a file nothing includes, or the skin is not set to Custom.
6. Hand over in this order: a five-line summary (what, which files, where they go, how to open it), the install
   steps, then the files. Name the adapters/events/fonts you relied on and what was not verified in a live client.
   Save files to disk when you can; do not paste a 500-line file inline unless the user asked for inline.

## Recipes

### Move, resize, recolour, refont a control
Edit `Position`, `Width`/`Height`, `Color`, `FontName` on the def. Fonts must be declared names (`arial9/11/14`
exist everywhere; others depend on the skin). Keep text within `Width` or it is clipped at `MaxCharacters`.

### Add a digital readout next to a bar
```xml
<ScalarLabelDef>
  <ControlId></ControlId>
  <Position><X>128</X><Y>20</Y></Position>
  <Alignment></Alignment>
  <FontName>arial11</FontName>
  <Adapter>summary_player_hits</Adapter>        <!-- same scalar the bar uses -->
  <ColorAdapter></ColorAdapter>
  <Width>26</Width><Height>14</Height>
  <MaxCharacters>4</MaxCharacters>
  <Color><R>255</R><G>255</G><B>255</B><A>255</A></Color>
  <Data></Data>
  <EndAligned>true</EndAligned>
  <TextCentered>false</TextCentered>
  <DontDrawWhenZero>false</DontDrawWhenZero>
  <DontDrawWhenNegOne>true</DontDrawWhenNegOne>
</ScalarLabelDef>
```
Percent adapters: `summary_player_hits/end/power`, `summary_target_hits`, `group_health0-7`, `group_power0-7`,
`group_endurance0-7`, `mini_pet_life`, `summary_exp_fine/coarse`, `realm_exp_fine/coarse`. Full list in
`references/adapters.md` (grouped by prefix, type and the control that binds it).

### Add a button that does something
`ButtonDef` (fixed size, needs a `ButtonTemplate`) or `HorizontalResizeButtonDef` (variable width) with
`<OnClickEvent>`. Common events: `Stick`, `Follow`, `Face`, `AssistTarget`, `ToggleAttackMode`, `Sprint`,
`Release`, `Quit`, `GroupInvite`, `GroupDisband`, `SelectGroupMember0-7`, `Repair`/`Craft`/`Salvage`,
`ToggleMap`, `ToggleJournal`, `ToggleMiniGroup`, `ToggleClock`, `ToggleCustomN`. Full list in `references/events.md`.
An `InvisibleButtonDef` makes any region clickable (a name label that faces the target). Place it after the
controls it overlays or they steal the click.

### Add a brand-new window
1. Pick a free slot N (check which `customN_window.xml` the user's UI already ships; BobsUI uses all 20, stock none).
2. Write `custom\customN_window.xml` with `<Name>customN_window</Name>` (exact) and your controls.
3. `<Include>customN_window.xml</Include>` from a file you already override (`assets.xml` in BobsUI-style UIs,
   or your copy of `command_window.xml` for a minimal mod). Do **not** create a fresh `assets.xml` for this: it
   would replace the stock one and drop every stock font and texture.
4. Add a button with `<OnClickEvent>ToggleCustomN</OnClickEvent>` somewhere (command window, main menu).
5. Lint, relog, press the button. The complete worked example is `examples/` (target bar, self-contained textures).

### Low-touch alternative: repurpose a stock window you never use
If the user does not want to touch `command_window.xml`/`assets.xml`, a stock window they never open (clock,
performance meter, mini friends) can be rewritten in place: copy its file, keep its template `Name` and numeric
ControlIds, replace the controls. It loads without any `<Include>` and keeps its stock toggle (Interface Elements /
main menu entry; the clock also has `ToggleClock`). Cost: that stock window is gone until the file is removed.
Say that trade-off out loud.

### Restyle (new look, same layout)
Copy the stock texture sheets from `ui\atlantis\`, repaint pixels in place keeping every coordinate, save as 32-bit
TGA with alpha under the same asset `Name` (declare in your copy of `assets.xml`). No template edits needed.
For a different geometry, write your own templates with new names (`references/control-templates.md`) and point
the defs at them. Old-style panels (inventory, quickbars, spell sheets) are bitmaps in `custom\oldstyle\`.

### Change the chat font or size
Copy `chat_window.xml` and the font declarations. Bitmap `<Font>` = fixed size per TGA. On modern clients add a
`<TTFFont>` (`Height`, `Antialiased`, `Hint`) and set it as the `ChatControlTemplate` font. Details in
`references/assets-fonts-textures.md`.

### Change the compass
Strip compass: `compass.xml` + `CompassControlTemplate` whose `Texture` is a standalone file (`compass.bmp`), adapter
`compass_heading`. Round compass (BobsUI): `StatusIconDef`s bound to `compass_heading` and `combat_mode`.

### "Make the bar look different below X%" without logic
A `StatusIconTemplate` with `MaxLevels` frames shows frame `round(value / 100 * (MaxLevels-1))` for a 0-100 scalar.
Paint a strip where the low frames are red bars and the high frames are green bars (e.g. 20 frames: frames 0-4 red),
bind a `StatusIconDef` to `group_health0` (or any percent adapter). You get threshold colouring and even a crude
fill level, with no conditions in the XML. It cannot flash or count down; say so.

### Clone a layout to another character
Copy `Name-<id>.ini` to `Other-<id>.ini` in the `%APPDATA%` folder while logged out. Not an XML task.

## Gotchas (check these before blaming the XML)

- Skin not set to Custom; file saved outside `ui\custom`; file not included by anything.
- Typo in a `TemplateName`/`FontName`/`TextureName`: the control simply does not render. The linter catches it.
- Adapter case: `Summary_Target` is not `summary_target`.
- Draw order: background listed after other controls hides them; invisible button listed before a button eats clicks.
- A control positioned past `Width`/`Height` of a non-resizable window cannot be clicked.
- `MinWidth`/`MinHeight` below the background's cap sizes corrupts the image.
- Resizable window but background without `GrowWidth`/`GrowHeight`: the frame stops growing.
- Reused a numeric `ControlId` that the stock window binds in code, or dropped one when rewriting the file.
- After a game patch, stock windows gain controls; your old copy silently lacks them. Diff against `ui\atlantis`.
- Fonts: `arial9/11/14` must remain defined if you override `assets.xml`; custom TGA fonts need the alpha markers.
- Shipping a `custom\assets.xml` that does not re-declare the stock assets.

## Debugging

1. `python scripts/daoc_ui_lint.py <custom> --base <atlantis>`; errors first, then `template`/`adapter` warnings.
2. `<game>\ui.log` lists files the client could not find (wrong `<File>` path or include name).
3. Bisect: move half of your custom files out, relog, repeat. The stock versions load in their place, so the game
   stays usable while you narrow it down.
4. For "the window does not open": confirm the template `Name` is exactly `customN_window`, the file is included,
   and the button's event is `ToggleCustomN` with the same N.
5. For "it is there but blank": the background template name or its texture name is wrong, or the sheet lacks alpha.

## Bundled resources

- `references/xml-syntax.md` - the file shapes with every field, read first when writing XML.
- `references/control-templates.md`, `references/control-defs.md` - field tables, official and observed.
- `references/adapters.md` (999 names), `references/events.md` (280), `references/windows.md` (107 windows,
  files, sizes, used ControlIds) - look names up here rather than guessing.
- `references/assets-fonts-textures.md` - TGA/DDS, icon sheets, bitmap font format, TTFFont, oldstyle, `.ini`.
- `references/ecosystem.md` - sources, real UIs to read, tools, communities, client versions, daochook.
- `examples/` - complete self-contained custom window + install notes.
- `scripts/daoc_ui_lint.py` - run before every launch. `scripts/build_reference_data.py` + `gen_reference_md.py`
  rebuild the inventories from any `custom/` or `atlantis/` folder (do this on the player's own stock skin when
  their client is newer than the data).

## Honesty notes

Nothing in this skill was executed in a live client from the authoring machine. Syntax and names come from the
official document and from complete UIs that ship and work; pixel positions in examples are estimates. Say so
when handing over files, and ask the user to report `ui.log` and a screenshot if something does not appear.
