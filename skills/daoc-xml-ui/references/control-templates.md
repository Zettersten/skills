# Control template reference

A template describes how one flavour of a control is drawn: texture cut-outs, fonts, colours, offsets.
Templates never bind adapters. Most live in `styles.xml` (or files it includes); any loaded file may define one.
Names are looked up case-insensitively. If two share a name, the later one wins.

Tags: **official** = fully described in the ToA document. **observed** = used by working 1.127-era UIs
(fields are what shipping files contain; semantics are inferred from names and usage).

Types in the official list that modern UIs also use: Button, VerticalResizeImage, HorizontalResizeImage,
FullResizeImage, VerticalScrollbar, ListBox, TextArea, StatusBar, ImageArea, StatusIcon, Icon, ChatControl,
CheckBox, VerticalStatusBar, CompassControl, Menu, ComboBox. Added since: HorizontalResizeButton, EditBox,
HorizontalSlider, VerticalSlider, IconSet, ListBoxHeader, Tabs, TreeControl.

## Contents

- [Image pieces](#image-pieces): ImageArea, HorizontalResizeImage, VerticalResizeImage, FullResizeImage
- [Indicators](#indicators): StatusBar, VerticalStatusBar, StatusIcon, Icon, IconSet, CompassControl
- [Buttons and inputs](#buttons-and-inputs): Button, HorizontalResizeButton, CheckBox, EditBox, HorizontalSlider, VerticalSlider
- [Lists and text](#lists-and-text): ListBox, ListBoxHeader, TextArea, ChatControl, TreeControl, Menu, ComboBox, Tabs
- [Scrollbars](#scrollbars): VerticalScrollbar
- [Shared sub-blocks](#shared-sub-blocks): Font, TextFont, Texture, Color, Size/Point

## Image pieces

### ImageAreaTemplate (official)
A decal: a fixed rectangle copied from a texture sheet. Used for logos, icons, masks, slider thumbs.

| field | type | meaning |
|---|---|---|
| Name | name | template name |
| TextureName | name | a `<Texture>` asset |
| Size | size | pixel size of the decal |
| TopLeft | texcoord | where the decal starts in the sheet |

### HorizontalResizeImageTemplate (official)
Left cap, repeated middle, right cap. Used by status bars, list rows, resize buttons. Caps are never tiled or cut.

| field | type | meaning |
|---|---|---|
| Name | name | |
| Height | number | pixel height of the strip |
| LeftWidth / RepeatWidth / RightWidth | number | widths of the three pieces |
| Texture.TextureName | name | sheet |
| Texture.Left / Repeat / Right | texcoord | top-left of each piece in the sheet |

Minimum drawable width is LeftWidth + RightWidth.

### VerticalResizeImageTemplate (official)
Same idea vertically: top cap, repeating middle, bottom cap. Used by scrollbar gutters/thumbs and vertical bars.

| field | type | meaning |
|---|---|---|
| Name | name | |
| Width | number | pixel width |
| TopHeight / RepeatHeight / BottomHeight | number | heights of the pieces |
| Texture.TextureName | name | |
| Texture.Top / Repeat / Bottom | texcoord | |

### FullResizeImageTemplate (official)
Nine-slice image: four fixed corners, tiled edges, tiled centre. The backbone of every window background,
inset panel and tooltip. Minimum size is (LeftWidth+RightWidth) x (TopHeight+BottomHeight); a window whose
`MinWidth`/`MinHeight` go below that shows visual garbage.

| field | type | meaning |
|---|---|---|
| Name | name | |
| TopHeight / MiddleHeight / BottomHeight | number | row heights |
| LeftWidth / MiddleWidth / RightWidth | number | column widths |
| Texture.TextureName | name | |
| Texture.TopLeft, TopMiddle, TopRight, MiddleLeft, MiddleMiddle, MiddleRight, BottomLeft, BottomMiddle, BottomRight | texcoord | the nine pieces |

All nine coordinates must come from the same sheet.

## Indicators

### StatusBarTemplate (official)
Horizontal bar for 0-100 scalars (health, power, endurance, XP). Composed of two HResize templates.

| field | type | meaning |
|---|---|---|
| Name | name | |
| BackgroundHResizeTemplate | name | the empty track |
| ForegroundHResizeTemplate | name | the filled part, clipped to the percentage |
| Height | number | |
| ForegroundOffset | size | offset of the fill inside the track |

### VerticalStatusBarTemplate (official)
Vertical bar. Not seen in the modern reference UI but documented.

| field | type | meaning |
|---|---|---|
| Name | name | |
| BackgroundImage / ForegroundImage | name | VResize templates for track and fill |
| Width | number | |
| ForegroundOffset | size | |

### StatusIconTemplate (official)
A fixed-size image with N frames laid out in a row or column; the frame shown is picked by a 0-100 scalar.
Used for the compass face (frame = heading), meters, combat-mode frames, multi-state glyphs.

| field | type | meaning |
|---|---|---|
| Name | name | |
| TextureName | name | |
| TextureStart | texcoord | first frame |
| Width / Height | number | one frame |
| MaxLevels | number | number of frames, lowest to highest |
| Horizontal | bool | frames side by side (true) or stacked (false) |

### IconTemplate (official)
A 16x16 or 32x32 game icon (spell, style, ability, item) with an optional overlay label.

| field | type | meaning |
|---|---|---|
| Name | name | |
| Size | size | control size |
| FontName | name | font for the overlay text |
| FontColor | color | |
| IconSize | number | 0 for 16x16, anything else for 32x32 |

### IconSetTemplate (observed)
Grid layout for several icons (group buffs). Referenced by `IconTemplate`-based controls in group windows.

| field | type |
|---|---|
| Name | name |
| CellPadding / LinePadding | number |
| IconTemplate | name |

### CompassControlTemplate (official)
Drives the strip compass. The texture must be a standalone file with no padding.

| field | type |
|---|---|
| Name | name |
| Texture | name (a `<Texture>` asset) |

## Buttons and inputs

### ButtonTemplate (official)
Five visual states: normal, highlit, pressed, pressed+highlit, disabled.

| field | type | meaning |
|---|---|---|
| Name | name | |
| Size | size | button size |
| Font.Name | name | |
| Font.ColorNormal / ColorPressed / ColorHighlit / ColorDisabled | color | label colours per state |
| Texture.TextureName | name | |
| Texture.Normal / Pressed / NormalHighlit / PressedHighlit / Disabled | texcoord | per-state cut-outs (same sheet) |

### HorizontalResizeButtonTemplate (observed)
A button of variable width: each state is an HResize image template instead of a fixed cut-out. The width is set
on the `HorizontalResizeButtonDef`. Used for most text buttons in modern UIs and for chat tabs.

| field | type | meaning |
|---|---|---|
| Name | name | |
| Height | number | |
| Font.Name, Font.ColorNormal/ColorPressed/ColorHighlit/ColorDisabled | | as ButtonTemplate |
| Normal / Pressed / NormalHighlit / PressedHighlit / Disabled | name | HorizontalResizeImageTemplate per state (may be empty) |

### CheckBoxTemplate (official)
On/off button with a text label beside it.

| field | type | meaning |
|---|---|---|
| Name | name | |
| Size | size | size of the box part |
| Font.Name, Font.ColorNormal/ColorPressed/ColorHighlit/ColorDisabled | | |
| TextOffset | size | label offset to the right of the box |
| TextAlignment | alignment | |
| ChangeFontColor | bool | label colour follows state |
| Texture.TextureName, Normal/Pressed/NormalHighlit/PressedHighlit/Disabled | texcoord | |

### EditBoxTemplate (observed)
Single-line text input (chat rename, market search).

| field | type |
|---|---|
| Name | name |
| LinePadding | number |
| BackgroundTemplate | name (FullResizeImage) |
| TextOffset | point |
| Font.Name, Font.ColorNormal, Font.ColorActive | |
| ScrollbarOffset / ScrollbarSizeOffset | point |

### HorizontalSliderTemplate / VerticalSliderTemplate (observed)
Slider with a thumb decal over a resizable gutter. Bound to a scalar by the def; `Numticks` lives on the def.

| field | type |
|---|---|
| Name | name |
| ImageAreaTemplate | name (thumb) |
| BackgroundHResizeTemplate (horizontal) / BackgroundVResizeTemplate (vertical) | name (gutter) |
| Height (horizontal) / Width (vertical) | number |

## Lists and text

### ListBoxTemplate (official + observed extensions)
Multi-column, multi-row list with optional icons, header row, alternate-row shading and selection highlight.
Backs merchant wares, concentration list, stats additional info, chant list, vault, community lists.

| field | type | source | meaning |
|---|---|---|---|
| Name | name | official | |
| LinePadding / CellPadding | number | official | blank pixels between rows / columns (negative values are used to tighten) |
| LabelLength | number | official | characters per label |
| ScrollbarTemplate | name | official | |
| ScrollbarTopOffset / ScrollbarBottomOffset / ScrollbarRightOffset | number | official | |
| BackgroundTemplate | name | official | FullResizeImage |
| TextFont.Name, ColorNormal, ColorHighlit, ColorGreyed | | official | |
| TextFont.TextLeftOffset / TextTopOffset / TextBottomOffset / TextRightOffset / LineOffset | number | official (Right: observed) | text placement inside cells |
| DrawScroll | bool | observed | hide the scrollbar when false |
| Sorting | bool | observed | |
| IconTemplate | name | observed | icon style for icon lists |
| IconSize | size | observed | |
| HeaderControl | bool | observed | show a header row |
| HeaderHorizResizeTemplate / HeaderBackgroundTemplate | name | observed | header visuals |
| HeaderLeftOffset / HeaderRightOffset / HeaderTopOffset / HeaderHeight | number | observed | |
| AlternateRowName / DisplayAlternateRow / AlternateRowOffset | name / bool / number | observed | zebra striping (an HResize image) |
| SelectedRowName / SelectedRowOffset | name / number | observed | selection highlight (an HResize image) |

### ListBoxHeaderTemplate (observed)
Clickable column header (sortable lists in the community window).

| field | type |
|---|---|
| Name | name |
| Texture.Name, Texture.Size, Texture.Normal / Pressed / Highlit | name, size, texcoord |
| TextFont.Name, ColorNormal / ColorPressed / ColorHighlit / ColorGreyed | |

### TextAreaTemplate (official)
Multi-line, scrollable text. Supports bracketed hotspots (NPC interact, help).

| field | type | meaning |
|---|---|---|
| Name | name | |
| ScrollbarTemplate | name | |
| LinePadding | number | |
| BackgroundTemplate | name | FullResizeImage |
| Font.Name, Font.ColorNormal, Font.ColorActive | | active = hotspot colour |
| TextOffset | size | top and bottom inset |
| ScrollbarOffset | point | from the top-left of the scrollbar |
| ScrollbarSizeOffset | point | added to the scrollbar size on resize |

### ChatControlTemplate (official)
The chat log itself.

| field | type |
|---|---|
| Name | name |
| FontName | name |
| BackgroundTemplate | name (FullResizeImage) |
| ScrollbarTemplate | name |

### TreeControlTemplate (observed)
Collapsible tree with checkboxes and icons (quest journal).

| field | type |
|---|---|
| Name | name |
| BackgroundTemplate / ScrollbarTemplate / CheckBoxTemplate / IconTemplate | name |
| FontName | name |
| FontColor | color |
| LinePadding / OffsetX / OffsetY / TextOffset | number |

### MenuTemplate (listed, undocumented; fields observed)
Drop-down list used by combo boxes and context menus.

| field | type |
|---|---|
| Name | name |
| Width / Height | number (one row) |
| LabelLength | number |
| Font.Name, Font.ColorNormal, Font.ColorHighlit | |
| Texture.TextureName, Texture.Normal, Texture.Highlit | texcoord |
| ScrollbarTemplate | name |
| MaxVisibleItems | number |

### ComboBoxTemplate (listed, undocumented; fields observed)

| field | type |
|---|---|
| Name | name |
| Menuoffset | point |
| DownButtonTemplate | name (ButtonTemplate) |
| LabelButtonTemplate | name (ButtonTemplate showing the current value) |
| MenuTemplate | name |

### TabsTemplate (observed)
Tab strip plus content panel; tabs show/hide controls by `ControlId` (see `TabsDef`).

| field | type |
|---|---|
| Name | name |
| ControlAreaFullResizeImageTemplate | name (panel background) |
| TabButtonTemplate | name (ButtonTemplate for each tab) |
| TabXOffset / TabYOffset | number |

## Scrollbars

### VerticalScrollbarTemplate (official)
Sub-component of list boxes, text areas, chat, menus. The active zone is how far outside the bar a drag keeps working.

| field | type |
|---|---|
| Name | name |
| ThumbVResizeTemplate / GutterVResizeTemplate | name (VerticalResizeImage) |
| UpButtonTemplate / DownButtonTemplate | name (Button) |
| Width | number |
| UpButtonOffset / DownButtonOffset / ThumbOffset / ActiveZoneOffset | size |

## Shared sub-blocks

```xml
<Font>                       <!-- inside Button/CheckBox/HResizeButton/Menu/EditBox/TextArea templates -->
  <Name>font_buttons</Name>
  <ColorNormal><R/><G/><B/><A/></ColorNormal>
  <ColorPressed>...</ColorPressed> <ColorHighlit>...</ColorHighlit> <ColorDisabled>...</ColorDisabled>
  <ColorActive>...</ColorActive>   <!-- TextArea/EditBox -->
</Font>
<TextFont>                   <!-- inside ListBox / ListBoxHeader templates -->
  <Name>...</Name> <ColorNormal/> <ColorHighlit/> <ColorGreyed/> <ColorPressed/>
  <TextLeftOffset/> <TextTopOffset/> <TextBottomOffset/> <TextRightOffset/> <LineOffset/>
</TextFont>
<Texture>                    <!-- inside image/button templates -->
  <TextureName>sheet</TextureName>
  <!-- then one <X/><Y/> block per piece or state -->
</Texture>
```

Colours are 0-255 RGBA. Sizes and points are `<X/><Y/>`. Every texture coordinate in one template must come from
the same sheet.
