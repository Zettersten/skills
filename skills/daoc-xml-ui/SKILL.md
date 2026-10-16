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
<game>\ui\uimain.xml         <- the load list (76 includes on 1.130); never edit
%APPDATA%\Electronic Arts\Dark Age of Camelot\<server>\Name-<id>.ini   <- window positions, per character
```

Default live install: `C:\Program Files (x86)\Electronic Arts\Dark Age of Camelot`. **Look for it first.** If a
client is installed on the machine you are working on, its `ui\atlantis` beats every reference in this skill:
read the target window file there, grep `styles.xml`/`assets.xml` for names, and pass it as `--base` to the
linter (it is picked up automatically when it sits next to the `custom` folder or at the default path).
Otherwise `references/stock-templates.md` and the stock table in `references/windows.md` are snapshots of the
1.130 skin; the BobsUI tables there are that UI's own layouts (its command window is 310x99, stock is 135x216),
so never quote BobsUI numbers as stock.

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
Edit `Position`, `Width`/`Height`, `Color`, `FontName` on the def. Fonts must be declared names: stock ships
`arial9`, `arial11`, `arial14`, `button_small`, `button_large`, `brit9`, `brit9s`, `title`, `barb10` and the
TrueType `chat_small`, `chat_large`, `minion`, `myriadbold`. Keep text within `Width` or it is clipped at
`MaxCharacters`. `OffsetRight`/`OffsetBottom` measure X/Y from the window's right/bottom edge to the control's
**far** edge (a button with `OffsetRight` and X=3 hugs the right border); `GrowWidth` on a bar stretches it.

### Stock names to reach for (Atlantis, 1.130; full list in `references/stock-templates.md`)
Bars `red_status`, `green_status`, `blue_status`, `yellow_status` (`*_small`, `red_status_thick`, `exp_bubbles`);
backgrounds `dlg_sm_title`, `dlg_sm_notitle`, `dlg_background_resize`, insets `dlg_interior_small`; buttons
`button_small` (60x16), `button_large`, `button_wide`, `button_narrow`, `generic_hr_button`; lists `listbox_bg`,
`generic_vscroll`; text `generic_textarea`; icons `plain_icon_small`/`plain_icon_large`. Names like
`statusbar_red` or `fresizeimage_dlg_bg_small` are BobsUI's, not stock.

### Add a digital readout next to a bar
(The stock `new_summary_window.xml` draws health as `<StatusBarDef>` with `red_status` + `summary_player_hits`;
this adds the number beside it.)
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
- Template names copied from another UI (BobsUI's `statusbar_red`, `fresizeimage_dlg_bg_small`...) do not exist
  on a stock base. Use the stock names or ship your own templates.
- Adapter case: `Summary_Target` is not `summary_target`.
- `OffsetRight` with a large X pushes the control off the left side: X counts from the right edge to the
  control's right edge, so a readout meant to sit at the right of a 160 px window wants X around 8, not 122.
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
- `references/stock-templates.md` - every template, font, texture and icon-sheet name the stock 1.130 skin
  defines; the names a stock-based mod may use without defining anything.
- `references/adapters.md` (1000+ names), `references/events.md` (280+), `references/windows.md` (stock 1.130
  table with code-bound ControlIds and the `uimain.xml` load order, plus BobsUI's 107 windows) - look names up
  here rather than guessing.
- `references/assets-fonts-textures.md` - TGA/DDS, icon sheets, bitmap font format, TTFFont, oldstyle, `.ini`.
- `references/ecosystem.md` - sources, real UIs to read, tools, communities, client versions, daochook.
- `examples/` - complete self-contained custom window + install notes.
- `scripts/daoc_ui_lint.py` - run before every launch; finds `ui\atlantis` on its own when present.
  `scripts/build_reference_data.py <atlantis> --out scripts/data/stock` + `gen_reference_md.py` rebuild the
  inventories from the player's own stock skin when their client is newer than 1.130.

## Honesty notes

Nothing in this skill was executed in a live client from the authoring machine. Syntax and names come from the
official document and from complete UIs that ship and work; pixel positions in examples are estimates. Say so
when handing over files, and ask the user to report `ui.log` and a screenshot if something does not appear.
