# XML syntax: what the files actually look like

The official document describes the system but never shows a file. Everything below is the shape used by
the stock skins and by every working custom UI (BobsUI/UI Chooser, Bysan, Lym), confirmed across 200+ files.

## Contents

- [File skeleton](#file-skeleton)
- [Includes](#includes)
- [Assets: fonts and textures](#assets-fonts-and-textures)
- [Control templates](#control-templates)
- [Window templates](#window-templates)
- [Control definitions](#control-definitions)
- [Compound values](#compound-values)
- [Rules the parser enforces (and does not)](#rules-the-parser-enforces-and-does-not)
- [How loading works](#how-loading-works)

## File skeleton

```xml
<?xml version="1.0" encoding="ISO-8859-1"?>
<Root_Element ID="DAOCUi">

  <!-- any mix, in any order, of: -->
  <Include>other_file.xml</Include>
  <Font> ... </Font>            <TTFFont> ... </TTFFont>        <Texture> ... </Texture>
  <ButtonTemplate> ... </ButtonTemplate>   <!-- and every other *Template -->
  <WindowTemplate> ... </WindowTemplate>   <!-- control *Def elements live only inside this -->

</Root_Element>
```

- The root element name is not checked strictly (`<Root_Element ID="DAOCUi">` is what the UI Editor writes; an old
  stock `uimain.xml` uses `<XML ID="DAOCUi">`). Use `Root_Element`.
- Encoding is `ISO-8859-1`; keep it, because stock files contain Latin-1 characters in labels.
- Comments `<!-- -->` are fine anywhere. The UI Editor leaves a `<!-- @@ Edited with ... -->` banner; harmless.
- All values are element text, never attributes: `<Width>210</Width>`, not `<Window width="210">`.
- Element names are **not** case sensitive (`onClickEvent`, `OnClickEvent` and `Onclickevent` all appear in
  shipping UIs). Template, font, texture and window names are not case sensitive either.
  **Adapter names are case sensitive.**

## Includes

```xml
<Include>styles.xml</Include>
<Include>Styles/Button_Templates.xml</Include>   <!-- subfolders are fine; paths are relative to the skin folder -->
```

- `ui/uimain.xml` (never edit it) includes the top-level files. Each of those may include more.
- Each include is resolved against your `custom/` first, then `ui/atlantis/`. So a file you do not ship is the
  stock one, and a file you do ship replaces the stock one *entirely* (including every template it defined).
- Brand-new files (your `custom1_window.xml`, your `MyTemplates.xml`) are only loaded if something includes them.
  Convention: add the includes to your `custom/assets.xml` (BobsUI) or to `custom/styles.xml`.

## Assets: fonts and textures

```xml
<Texture>
  <Name>mytextures_01</Name>                     <!-- referenced by TextureName in templates -->
  <File>custom/assets/textures/MyTextures_01.tga</File>   <!-- relative to the ui/ folder -->
</Texture>

<Font>                                            <!-- bitmap font: TGA with the underline-marker alpha channel -->
  <Name>font_mybuttons</Name>
  <File>custom/assets/fonts/Calibri_10.tga</File>
</Font>

<TTFFont>                                         <!-- TrueType font, modern clients -->
  <Name>chat_small</Name>
  <File>custom/fonts/MyriadPro-Regular.ttf</File>
  <Height>10</Height>
  <Antialiased>true</Antialiased>
  <Hint>2</Hint>
</TTFFont>
```

- Texture formats seen working: `.tga` (most common, alpha supported), `.bmp`, `.dds` (DXT1/3/5; maps and large
  sheets). The ToA doc only lists BMP/TGA; DDS has worked since about 1.71.
- `File` paths in shipping UIs are written relative to `ui/` (`custom/...`, `atlantis/...`). Some older mods use
  paths relative to the skin folder (`fonts/x.tga`) and also work, because of the fallback lookup. Prefer `custom/...`.
- Texture coordinates used by templates are pixel offsets into these sheets, origin top-left, no scaling.
- Fonts/textures are usually declared in `assets.xml` (or files it includes), but any loaded file may declare them.
  The names `arial9`, `arial11`, `arial14` are the client's resize fonts; the doc says they must exist.

## Control templates

A template is "how to draw this kind of control" and never contains adapter bindings. Shape by family:

```xml
<ImageAreaTemplate>                 <!-- a decal cut from a texture sheet -->
  <Name>imagearea_mylogo</Name>
  <TextureName>mytextures_01</TextureName>
  <Size><X>64</X><Y>32</Y></Size>
  <TopLeft><X>0</X><Y>0</Y></TopLeft>
</ImageAreaTemplate>

<HorizontalResizeImageTemplate>     <!-- left cap + repeating middle + right cap; bars, rows, buttons -->
  <Name>hresizeimage_mybar_fg</Name>
  <Height>14</Height>
  <LeftWidth>2</LeftWidth><RepeatWidth>12</RepeatWidth><RightWidth>2</RightWidth>
  <Texture>
    <TextureName>mytextures_01</TextureName>
    <Left><X>0</X><Y>40</Y></Left>
    <Repeat><X>2</X><Y>40</Y></Repeat>
    <Right><X>14</X><Y>40</Y></Right>
  </Texture>
</HorizontalResizeImageTemplate>

<FullResizeImageTemplate>           <!-- 9-slice: corners fixed, edges/center tiled; window backgrounds -->
  <Name>fresizeimage_mydialog</Name>
  <TopHeight>8</TopHeight><MiddleHeight>20</MiddleHeight><BottomHeight>8</BottomHeight>
  <LeftWidth>8</LeftWidth><MiddleWidth>20</MiddleWidth><RightWidth>8</RightWidth>
  <Texture>
    <TextureName>mytextures_01</TextureName>
    <TopLeft><X>0</X><Y>0</Y></TopLeft>       <TopMiddle><X>8</X><Y>0</Y></TopMiddle>       <TopRight><X>28</X><Y>0</Y></TopRight>
    <MiddleLeft><X>0</X><Y>8</Y></MiddleLeft> <MiddleMiddle><X>8</X><Y>8</Y></MiddleMiddle> <MiddleRight><X>28</X><Y>8</Y></MiddleRight>
    <BottomLeft><X>0</X><Y>28</Y></BottomLeft><BottomMiddle><X>8</X><Y>28</Y></BottomMiddle><BottomRight><X>28</X><Y>28</Y></BottomRight>
  </Texture>
</FullResizeImageTemplate>

<StatusBarTemplate>                 <!-- composes two HResize templates: empty track + filled portion -->
  <Name>statusbar_mygreen</Name>
  <BackgroundHResizeTemplate>hresizeimage_mybar_bg</BackgroundHResizeTemplate>
  <ForegroundHResizeTemplate>hresizeimage_mybar_fg</ForegroundHResizeTemplate>
  <Height>14</Height>
  <ForegroundOffset><X>0</X><Y>0</Y></ForegroundOffset>
</StatusBarTemplate>

<ButtonTemplate>                    <!-- five texture states + font colours per state -->
  <Name>button_my68</Name>
  <Size><X>68</X><Y>16</Y></Size>
  <Font>
    <Name>font_buttons</Name>
    <ColorNormal><R>148</R><G>111</G><B>0</B><A>255</A></ColorNormal>
    <ColorPressed><R>255</R><G>192</G><B>0</B><A>255</A></ColorPressed>
    <ColorHighlit><R>192</R><G>192</G><B>192</B><A>255</A></ColorHighlit>
    <ColorDisabled><R>128</R><G>128</G><B>128</B><A>255</A></ColorDisabled>
  </Font>
  <Texture>
    <TextureName>buttons_01</TextureName>
    <Normal><X>1</X><Y>208</Y></Normal>
    <Pressed><X>1</X><Y>224</Y></Pressed>
    <NormalHighlit><X>1</X><Y>240</Y></NormalHighlit>
    <PressedHighlit><X>1</X><Y>224</Y></PressedHighlit>
    <Disabled><X>1</X><Y>208</Y></Disabled>
  </Texture>
</ButtonTemplate>

<StatusIconTemplate>                <!-- N frames side by side; frame chosen by a 0-100 scalar -->
  <Name>statusicon_mymeter</Name>
  <TextureName>mytextures_01</TextureName>
  <TextureStart><X>2</X><Y>2</Y></TextureStart>
  <Width>32</Width><Height>32</Height>
  <MaxLevels>8</MaxLevels>
  <Horizontal>true</Horizontal>
</StatusIconTemplate>
```

See `control-templates.md` for every type and field. Templates referenced by name must exist somewhere in the
loaded set; a typo gives you an invisible control and no error message.

## Window templates

```xml
<WindowTemplate>
  <Name>custom1_window</Name>            <!-- how the client finds it; custom slots are custom0_window..custom19_window -->
  <WindowId>My Target Bar</WindowId>     <!-- label only -->
  <CloseButton>true</CloseButton>        <!-- stock close X, top right -->
  <MoveButton>true</MoveButton>          <!-- stock move grip, top left -->
  <TopRightResizeButton>false</TopRightResizeButton>
  <BottomRightResizeButton>false</BottomRightResizeButton>
  <BottomLeftResizeButton>false</BottomLeftResizeButton>
  <ResizeButtonOffsetX>0</ResizeButtonOffsetX>
  <ResizeButtonOffsetY>0</ResizeButtonOffsetY>
  <TitleWidth>150</TitleWidth>           <!-- drag area; 0 disables dragging by title -->
  <TitleHeight>10</TitleHeight>
  <Width>150</Width>
  <Height>40</Height>
  <ResizeableWidth>0</ResizeableWidth>   <!-- >0 = user can resize horizontally; background needs GrowWidth -->
  <ResizeableHeight>0</ResizeableHeight>
  <ResizeableTwoWayWidth>0</ResizeableTwoWayWidth>
  <ResizeableTwoWayHeight>0</ResizeableTwoWayHeight>
  <MinWidth>150</MinWidth>
  <MinHeight>40</MinHeight>
  <ContextTemplateName></ContextTemplateName>   <!-- modern: name of a context-menu window (right click) -->

  <!-- control definitions, drawn in this order: background first -->
  <FullResizeImageDef> ... </FullResizeImageDef>
  <LabelDef> ... </LabelDef>
</WindowTemplate>
```

Shipping UIs always write every field, even when zero/false. Do the same; it avoids surprises on older clients.
`TabName` appears on a few windows (tabbed stats windows). `WindowId` values are free text in practice.

## Control definitions

Every def has the same head, then type-specific fields:

```xml
<LabelDef>
  <ControlId></ControlId>                <!-- empty, or a number (see ControlId notes) -->
  <Position><X>10</X><Y>5</Y></Position> <!-- pixels from the window's top-left -->
  <Alignment>                            <!-- zero or more flags; empty element is fine -->
    <CenterHorizontally>true</CenterHorizontally>
  </Alignment>
  <FontName>font_buttons</FontName>
  <Width>130</Width><Height>12</Height>
  <MaxCharacters>32</MaxCharacters>
  <Color><R>255</R><G>192</G><B>0</B><A>255</A></Color>   <!-- used when ColorAdapter is empty -->
  <ColorAdapter>summary_target_color</ColorAdapter>
  <Data>fallback text</Data>              <!-- shown when Adapter is empty -->
  <Adapter>summary_target</Adapter>       <!-- text adapter -->
  <EndAligned>false</EndAligned>
  <TextCentered>true</TextCentered>       <!-- modern -->
</LabelDef>

<ScalarLabelDef>                          <!-- numbers; LabelDef cannot show scalar adapters -->
  <ControlId></ControlId>
  <Position><X>2</X><Y>12</Y></Position>
  <Alignment></Alignment>
  <FontName>font_buttons_small</FontName>
  <Adapter>summary_target_hits</Adapter>
  <ColorAdapter>summary_target_color</ColorAdapter>
  <Width>25</Width><Height>16</Height>
  <MaxCharacters>4</MaxCharacters>
  <Color><R>255</R><G>255</G><B>255</B><A>255</A></Color>
  <Data></Data>
  <EndAligned>false</EndAligned>
  <TextCentered>true</TextCentered>
  <DontDrawWhenZero>true</DontDrawWhenZero>      <!-- modern -->
  <DontDrawWhenNegOne>true</DontDrawWhenNegOne>  <!-- modern -->
</ScalarLabelDef>

<StatusBarDef>
  <ControlId></ControlId>
  <Position><X>28</X><Y>17</Y></Position>
  <Alignment></Alignment>
  <TemplateName>statusbar_red</TemplateName>
  <AdapterName>summary_target_hits</AdapterName>  <!-- scalar 0-100 -->
  <Width>115</Width>
</StatusBarDef>

<ButtonDef>
  <ControlId></ControlId>
  <Position><X>16</X><Y>65</Y></Position>
  <Alignment></Alignment>
  <TemplateName>button_size_68</TemplateName>
  <Label>Health</Label>
  <OnClickEvent>ToggleCustom1</OnClickEvent>
</ButtonDef>

<InvisibleButtonDef>                      <!-- click area with no visuals; put it AFTER what it covers -->
  <ControlId></ControlId>
  <Position><X>0</X><Y>0</Y></Position>
  <Alignment></Alignment>
  <Label></Label>
  <OnClickEvent>Face</OnClickEvent>
  <Width>150</Width><Height>14</Height>
</InvisibleButtonDef>

<StatusIconDef>
  <ControlId></ControlId>
  <Position><X>0</X><Y>0</Y></Position>
  <Alignment><TopLeft>true</TopLeft></Alignment>
  <TemplateName>statusicon_compass_bg</TemplateName>
  <AdapterName>compass_heading</AdapterName>
</StatusIconDef>
```

See `control-defs.md` for every def type and field.

## Compound values

| type | shape | notes |
|---|---|---|
| Bool | `true` / `false` | anything else parses as false |
| Color | `<R/><G/><B/><A/>` 0-255 each | A=255 is opaque |
| Point / Size / TextureCoordinate | `<X/><Y/>` | Position may be negative; Size must be positive; texture coords are integer pixel offsets from the sheet's top-left |
| Alignment | child flags, each `true`/`false` | `TopLeft` (default), `CenterHorizontally`, `CenterVertically`, `OffsetBottom`, `OffsetRight`, `GrowWidth`, `GrowHeight`. `Offset*` make the position count from the right/bottom edge; `Grow*` resize the control with the window |

## Rules the parser enforces (and does not)

- **Draw order = XML order.** The first def is drawn first. A full-window background listed last hides everything.
  Click handling follows the same order: an `InvisibleButtonDef` over a button steals the click, which is why
  "my new button does nothing" is usually an overlap, not a wrong event name.
- **Naming.** Templates and assets are found by name; a misspelled `TemplateName` means the control silently does
  not render. The ToA doc says names are at most 31 characters; modern shipping UIs use longer names without issue.
- **Duplicates.** Defining a template name twice keeps the *later* definition. Windows cannot be duplicated.
- **Load order does not matter** for templates (all XML is read before any window is built), except for draw order.
- **Controls outside the window** render but cannot be interacted with.
- **Status bars/icons** need a scalar whose range is 0-100; a raw hitpoint count will not work, use the `*_hits`
  / `*_power` percentage adapters.
- **Nothing is validated.** Unknown elements are ignored, missing fields default, and errors go to `ui.log` only
  for missing files. Run `scripts/daoc_ui_lint.py` before launching the game.

## How loading works

1. Client reads `ui/uimain.xml` (patched by the game; never edit).
2. For each included file it looks in `ui/custom/` (when the Custom skin is selected), then `ui/atlantis/`.
3. All XML is parsed; templates and assets go into one flat namespace.
4. Windows are instantiated from `WindowTemplate`s. Positions come from the character's `.ini` file
   (`%APPDATA%\Electronic Arts\Dark Age of Camelot\<server>\CharName-<id>.ini`), not from the XML.
5. Old-style panels (inventory, quickbars, spell sheets, options...) are not XML; they use the bitmaps listed in
   `assets-fonts-textures.md`, overridden by dropping same-named files in `custom/oldstyle/`.
