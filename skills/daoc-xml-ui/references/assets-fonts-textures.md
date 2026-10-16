# Assets: textures, icons, fonts, old-style panels

## Contents

- [Declaring assets](#declaring-assets)
- [Texture sheets](#texture-sheets)
- [Icon sheets](#icon-sheets)
- [Bitmap fonts (TGA)](#bitmap-fonts-tga)
- [TrueType fonts (TTFFont)](#truetype-fonts-ttffont)
- [Old-style panels and custom/oldstyle](#old-style-panels-and-customoldstyle)
- [Per-character layout files (.ini) and user.dat](#per-character-layout-files-ini-and-userdat)

## Declaring assets

```xml
<Texture><Name>mysheet_01</Name><File>custom/assets/textures/MySheet_01.tga</File></Texture>
<Font><Name>font_mine</Name><File>custom/assets/fonts/Mine_10.tga</File></Font>
<TTFFont><Name>chat_small</Name><File>custom/fonts/MyriadPro-Regular.ttf</File><Height>10</Height><Antialiased>true</Antialiased><Hint>2</Hint></TTFFont>
<Canvas><Name>...</Name><File>...</File></Canvas>   <!-- whole-file image for the deprecated StaticFileImageDef -->
```

- Declare them in `custom/assets.xml` (which replaces the stock `atlantis/assets.xml`, so copy the stock one and
  add to it, or `<Include>` your own `MyAssets.xml` from it). BobsUI splits them into `*Images.xml` files.
- `File` is relative to the `ui/` folder. Use forward or back slashes; keep file names free of spaces.
- Asset names are case-insensitive and share the namespace with templates; keep them distinct.

## Texture sheets

- Formats that work: `.tga` (32-bit with alpha for anything transparent), `.bmp` (no alpha), `.dds` (DXT1/3/5,
  used for maps and large sheets since ~1.71). The ToA doc predates DDS support.
- Coordinates are integer pixel offsets from the top-left of the sheet, mapped 1:1 on screen. There is no
  scaling, filtering or stretching: a 68x16 button cut-out is 68x16 on screen at every resolution.
- Coordinates off the edge of the sheet, or negative, are undefined (usually garbage pixels).
- Every piece of one template must come from one sheet. Sheets up to 512x512 are the norm; 1024 works on modern
  clients for maps.
- Sheet naming in shipping UIs: `buttons_01`, `dialogimages_02`, `statusbars_01`, `statusicons_03`... Pick a
  scheme and keep an index comment at the top of your assets file listing what lives where.
- Photoshop 7 (early versions) wrote broken TGA alpha; irrelevant now, but if an old mod's TGA looks wrong,
  re-save it with GIMP/Paint.NET.
- To restyle a stock skin, copy the stock sheet from `ui/atlantis/`, edit pixels in place, keep the same
  coordinates, and ship it under the same `Name` from your `assets.xml`. No template edits needed.

## Icon sheets

- Spell/style/ability/item icons are 10x10 sheets of 100 icons each, in two sizes: 16x16 per icon and 32x32 per
  icon. File names are hard-coded by the client (the stock skin declares them from `item_icons.xml`,
  `combat_icons.xml`, `skill_icons.xml`, `spell_icons.xml`, `weapon_icons.xml`); copy those files and the sheets
  to `custom/` and edit pixels only.
- Until every old panel is converted (still true), modified icons must also be copied into `custom/oldstyle/`
  so the old-style spell/style sheets pick them up.
- `IconTemplate.IconSize` is 0 for 16x16, anything else for 32x32; other sizes are not supported.
- Icon ids come from the server (via scalar adapters); you cannot renumber icons from XML.

## Bitmap fonts (TGA)

A `<Font>` is a TGA whose **alpha channel encodes the glyph grid**:

1. Each character sits on a row; directly under each character is a 1-pixel-tall run of pure white (255) in
   the alpha channel exactly as wide as the glyph. A gap in the run splits the glyph in two; a missing run drops
   the character.
2. The first (leftmost) pixel column holds one white pixel per row at the height of that row's underline. These
   mark the line heights; the tallest row becomes the font height.
3. Rows must be perfectly horizontal; keep the row pitch constant.
4. Characters must appear in the same order as the stock fonts (open `atlantis/fonts/arial11.tga` or any
   `custom/Assets/Fonts/*.tga` from BobsUI as the model). Wrong order = garbled text.
5. Put glyph pixels in the alpha channel too (white alpha, any RGB). RGB colour data distorts when the game
   recolours text, so keep RGB flat white.

Practical route: take an existing font TGA, overlay your glyphs row by row at the same positions, and keep the
markers. Fonts cannot be resized at runtime; make one file per size (`Calibri_08`, `Calibri_09`, `Calibri_10`).

Reserved names: `arial9`, `arial11`, `arial14` are the sizes selectable in the front-end; the doc says the game
may misbehave if they are missing. If you override `assets.xml`, keep them (pointing at stock files is fine).

## TrueType fonts (TTFFont)

Modern clients accept `<TTFFont>` with `Height` (pixel size), `Antialiased` (bool) and `Hint` (0-2 hinting level).
Declare one TTFFont per size you need, e.g. `chat_small` at 10 and `chat_large` at 13 from the same `.ttf`.
BobsUI exposes "new style" chat fonts with in-game variable sizes this way. Ship the `.ttf` under `custom/`.
Older/freeshard clients that predate the element ignore it; fall back to a bitmap font if text vanishes.

## Old-style panels and custom/oldstyle

Not everything is XML. Inventory, quickbars, spell/style/ability sheets, trade, options, housing dialogs, the
bank vault and the old scroll buttons are "panels" drawn from fixed bitmaps. You can recolour them, not rearrange
them. Drop same-named bitmaps into `custom/oldstyle/` (stock copies live under `<game>/data/` or
`Atlantis/data/` and `Atlantis/phousing/data/`, depending on client era):

| bitmap | panel(s) |
|---|---|
| `vault.bmp` | bank |
| `dialog_sm.bmp` | dialog |
| `emblempick.bmp` | emblem picker |
| `npctalk.bmp` | LFG group picker, help, housing big dialog |
| `leftbot.bmp` | alpha picker, value picker (coin, alpha), housing interior rotation |
| `options.bmp` | options, housing int/ext options, market query/results, friend permissions, housing friend list |
| `hbar_horz.bmp`, `hbar_min.bmp`, `hbar_vert.bmp` | quickbars |
| `pperdoll.bmp`, `hldbrite.bmp`, `sacks.bmp` | inventory (BobsUI ships 80+ `pperdoll.bmp` variants) |
| `magicsheet.bmp` | spells |
| `combstylesheet.bmp` | styles |
| `skillsheet.bmp` | abilities |
| `trade.bmp` | trade |
| `interact.bmp` | tradeskills |
| `edit_box.bmp` | housing market query |
| `garden.bmp` | housing garden placement |
| `consignment.bmp` | housing player merchant |
| `minipet.bmp` | housing money selector |
| `scrlbtns.bmp` | all old-style scroll buttons |
| `listicon1.bmp` | all old-style checkboxes |
| `buttons.bmp`, `buttons2.bmp`, `buttons3.bmp` | old-style buttons |

Patch notes occasionally convert a panel to an XML window; when that happens the bitmap stops mattering and a new
`*_window.xml` appears in `ui/atlantis/`.

## Per-character layout files (.ini) and user.dat

Window positions, sizes, visibility, quickbar contents, macros and `/qbind`s are **not** in the XML. The client
saves them per character:

- Live: `%APPDATA%\Electronic Arts\Dark Age of Camelot\<server folder>\<CharName>-<serverId>.ini`
  (older: `LotM`; server ids like `-41` for Ywain1).
- Freeshards: same root, folder chosen by `paths.dat` in the game directory (`eden`, `phoenix_`, `uth2`...).
- `default<width>.ini` in the game folder (e.g. `default1920.ini`) seeds new characters; some reports say recent
  clients ignore it, so copying `Name-41.ini` between characters is the reliable way to clone a layout.
- `user.dat` in the same folder holds account-level client settings (remembered accounts, resolution).
- Changing a window's XML `Width`/`Height` does not move it; players reposition in game and the `.ini` updates.
  When you ship a UI, ship an optional sample `.ini` for common resolutions rather than hard-coding positions.
