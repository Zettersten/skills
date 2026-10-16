# Control definition and window attribute reference

A control definition (`*Def`) places one control in one window: position, size, template, adapter bindings and
events. Defs are only valid as children of a `<WindowTemplate>`. They are drawn, and receive clicks, in XML order.

Tags: **official** = in the ToA document. **observed** = used by working 1.127-era UIs (CynicalJedi/DAOC-UI-Chooser,
Lymhit/UI). Field names are case-insensitive; the canonical spelling is shown.

## Contents

- [Common head](#common-head)
- [ControlId rules](#controlid-rules)
- [Text](#text): LabelDef, ScalarLabelDef, TextAreaDef, EditBoxDef, ClickableEditBoxDef, ChatControlDef
- [Images](#images): FullResizeImageDef, HorizontalResizeImageDef, VerticalResizeImageDef, ImageAreaDef, DynamicImageDef, StaticFileImageDef
- [Indicators](#indicators): StatusBarDef, VerticalStatusBarDef, StatusIconDef, IconDef, DockableIconDef, CompassControlDef
- [Buttons and inputs](#buttons-and-inputs): ButtonDef, InvisibleButtonDef, HorizontalResizeButtonDef, HorizontalResizeImageButtonDef, CheckBoxDef, HorizontalSliderDef, VerticalSliderDef, ComboBoxDef
- [Lists and containers](#lists-and-containers): ListBoxDef, TreeControlDef, TabsDef
- [Window template attributes](#window-template-attributes)
- [Which def for which adapter type](#which-def-for-which-adapter-type)

## Common head

Every def starts with the same three elements (official):

| field | type | meaning |
|---|---|---|
| ControlId | id | empty, a number, or (rarely) a word; see below |
| Position | point | pixels from the window's top-left; negative allowed |
| Alignment | flags | `TopLeft`, `CenterHorizontally`, `CenterVertically`, `OffsetBottom`, `OffsetRight`, `GrowWidth`, `GrowHeight`; an empty `<Alignment></Alignment>` means top-left |

`ToolTipID` (number, observed) appears on many defs in stock windows; it selects a client-side tooltip string.
Leave it out of your own controls.

## ControlId rules

- Empty is normal for decorative controls.
- Stock windows use numeric ids (1000+) for controls the client code reads or writes (list boxes, edit boxes,
  the chat control, group member buttons...). Keep those exactly as they are when you restyle a stock window,
  and do not give a new control an id that the window already uses.
- `TabsDef` groups controls by `ControlId`: every control listed under a tab via `<TabControl>` needs that id, so
  custom windows with tabs use numeric ids freely (BobsUI uses 1100-1199 for tab 1, 1200-1299 for tab 2, ...).
- A few stock windows use word ids (`Background`, `Title`, `Health`, `SelectGroupMember0`); treat them as reserved too.

## Text

### LabelDef (official)
Single-line text. Shows a text adapter, or the literal `Data` when no adapter is set. Cannot show scalars.

| field | type | source | meaning |
|---|---|---|---|
| FontName | name | official | a `<Font>`/`<TTFFont>` |
| Adapter | name | official | text adapter |
| ColorAdapter | name | official | color adapter; overrides `Color` |
| Width / Height | number | official | |
| MaxCharacters | number | official | storage; longer text is cut |
| Color | color | official | used when ColorAdapter is empty |
| Data | string | official | literal text when Adapter is empty |
| EndAligned | bool | official | right-align |
| TextCentered | bool | observed | centre within Width |

### ScalarLabelDef (official)
Single number from a scalar adapter (hit points, percentages, levels, timers).

| field | type | source | meaning |
|---|---|---|---|
| FontName, Adapter, ColorAdapter, Width, Height, MaxCharacters, Color, Data, EndAligned | | official | as LabelDef; `Adapter` is a scalar |
| TextCentered | bool | observed | |
| DontDrawWhenZero | bool | observed | hide when the value is 0 (no target, empty slot) |
| DontDrawWhenNegOne | bool | observed | hide when the value is -1 (unavailable) |

### TextAreaDef (official)
Multi-line scrollable text; supports hotspots (the clickable `[keywords]` in NPC dialogue).

| field | type | source | meaning |
|---|---|---|---|
| TemplateName | name | official | TextAreaTemplate |
| AdapterName | name | official | multi-line text adapter |
| HasHotspots | bool | official | light up bracketed text |
| HotspotDelineator | string | observed | the opening bracket character, e.g. `[` |
| MaxCharacters | number | official | buffer size (32768 is common) |
| Width / Height | number | official | |

### EditBoxDef (observed)
Single-line text input bound to a text adapter (chat rename, bazaar query).

| field | type |
|---|---|
| TemplateName | name (EditBoxTemplate) |
| AdapterName | name |
| Width / Height | number |
| MaxCharacters | number |

### ClickableEditBoxDef (observed)
Edit box without an adapter (key-config capture). Fields: TemplateName, Width, Height, MaxCharacters.

### ChatControlDef (official)
The chat log. Binds one of the two special chat buffers.

| field | type | meaning |
|---|---|---|
| TemplateName | name | ChatControlTemplate |
| LinePadding | number | blank rows between lines |
| BufferName | name | `chat` or `system` |
| TextOffset | point | where text starts |
| Width / Height | number | |

## Images

### FullResizeImageDef (official)
Nine-slice image; window backgrounds and inset panels. Give the window background `GrowWidth`/`GrowHeight`
alignment if the window is resizable.

| field | type |
|---|---|
| TemplateName | name (FullResizeImageTemplate) |
| Width / Height | number |

### HorizontalResizeImageDef (official)
Three-slice horizontal strip (row backgrounds, separators). Fields: TemplateName, Width.

### VerticalResizeImageDef (observed)
Three-slice vertical strip. Fields: TemplateName, Height.

### ImageAreaDef (official)
A decal. Size comes from the template. Field: TemplateName.

### DynamicImageDef (observed; added with the 1.71 map system)
Image whose texture the client swaps at runtime (zone maps, atlas pages).

| field | type | meaning |
|---|---|---|
| TextureName | name | initial texture (e.g. `no_map`) |
| Dimensions | size | displayed size (256x256, 512x512) |
| TextureCoords | texcoord | top-left in the texture |

### StaticFileImageDef (official, deprecated)
Whole image file of any size, via a `<Canvas>` asset. Field: CanvasName. Not used by stock windows.

## Indicators

### StatusBarDef (official)
Horizontal bar. The adapter must be a 0-100 scalar.

| field | type |
|---|---|
| TemplateName | name (StatusBarTemplate) |
| AdapterName | name |
| Width | number |

### VerticalStatusBarDef (official)
Vertical bar, 0-100 scalar. Fields: TemplateName, AdapterName, Height.

### StatusIconDef (official)
Multi-frame image driven by a 0-100 scalar (compass face, meters, state frames). Fields: TemplateName, AdapterName.

### IconDef (official + observed)
Game icon by id. Either a fixed `IconId` or a scalar adapter supplying the id.

| field | type | source | meaning |
|---|---|---|---|
| TemplateName | name | official | IconTemplate |
| AdapterName | name | official | scalar giving the icon id |
| IconId | number | official | fixed icon when no adapter |
| Data | string | official | overlay text |
| LabelAdapterName | name | observed | text adapter for the overlay |
| StateAdapterName | name | observed | scalar selecting an icon state (greyed/active) |
| HideLabel | bool | observed | |
| Width / Height | number | observed | |
| OnClickEvent | event | observed | icons can fire events |

### DockableIconDef (observed)
Icon slot that accepts drag-and-drop (mount saddlebags). Field: IconTemplateName.

### CompassControlDef (official)
Strip compass bound to `compass_heading`. Fields: TemplateName, AdapterName, Width, Height.

## Buttons and inputs

### ButtonDef (official + observed)
Fixed-size button from a ButtonTemplate.

| field | type | source |
|---|---|---|
| TemplateName | name | official |
| Label | string | official |
| OnClickEvent | event | official |
| LabelAlignment | alignment | observed |
| Adapter / ColorAdapter | name | observed (label text/colour from adapters) |

### InvisibleButtonDef (official)
Click area with no visuals. Used to make whole regions clickable (click the target name to face it) and to
overlay actions on decorations. Because it has no template it needs its own size. Put it after the controls it
covers; it will intercept their clicks.

| field | type |
|---|---|
| OnClickEvent | event |
| Width / Height | number |
| Label | string (unused, keep empty) |

### HorizontalResizeButtonDef (observed)
Variable-width text button (the standard button in modern UIs).

| field | type |
|---|---|
| TemplateName | name (HorizontalResizeButtonTemplate) |
| Label | string |
| Width | number |
| OnClickEvent | event |
| LabelAlignment / LabelIndent | alignment / number |

### HorizontalResizeImageButtonDef (observed)
Resizable button with a decal on it (chat emoticon button, icon buttons).

| field | type |
|---|---|
| HRButtonTemplateName | name (HorizontalResizeButtonTemplate) |
| ImageAreaTemplateName | name (ImageAreaTemplate) |
| ImageOffset | point |
| Width | number |
| Label, OnClickEvent, LabelAlignment, LabelIndent | |

### CheckBoxDef (official + observed)

| field | type | source | meaning |
|---|---|---|---|
| TemplateName | name | official | |
| AdapterName | name | official | scalar 0/1 for the state |
| TextAdapterName | name | official | text adapter for the label |
| Data | string | official | label when no text adapter |
| LabelWidth | number | official | label storage |
| OnClickEvent | event | observed | |
| Font | block | observed | per-control font override |

### HorizontalSliderDef / VerticalSliderDef (observed)
Slider over a scalar (realm-ability levels in the training window).

| field | type |
|---|---|
| TemplateName | name |
| AdapterName | name |
| Width (horizontal) / Height (vertical) | number |
| Numticks | number |
| OnClickEvent | event |

### ComboBoxDef (official + observed)
Drop-down. The ToA doc lists `OnChangeEvent` and `AdapterName`; modern stock windows set only TemplateName and a
numeric ControlId (the client fills the list by id).

## Lists and containers

### ListBoxDef (official + observed)

| field | type | source | meaning |
|---|---|---|---|
| TemplateName | name | official | |
| AdapterName | name | official | list adapter |
| Sorting | bool | official | "not used" per doc |
| Columns | number | official | |
| Width / Height | number | official | |
| IconTemplate | name | observed | icon style |
| ShowIndicator | bool | observed | selection indicator |
| ShowDefaultToolTips | bool | observed | |
| OnClickEvent / OnHeaderClickEvent | event | observed | row click / header click |

### TreeControlDef (observed)
Quest journal tree.

| field | type |
|---|---|
| TemplateName, AdapterName, Width, Height | |
| Column1Width / Column1Offset / Column2Width / Column2Offset | number |

### TabsDef (observed)
Tab strip that shows/hides other controls in the same window by ControlId.

```xml
<TabsDef>
  <TemplateName>tabs_generic</TemplateName>
  <ControlId></ControlId>
  <Position><X>5</X><Y>5</Y></Position>
  <Alignment></Alignment>
  <Width>190</Width><Height>51</Height>
  <OnClickEvent></OnClickEvent>
  <Tab><Id>1</Id><Name>Exp</Name></Tab>
  <Tab><Id>2</Id><Name>Rxp</Name></Tab>
  <TabControl><TabId>1</TabId><ControlId>1200</ControlId></TabControl>
  <TabControl><TabId>2</TabId><ControlId>1100</ControlId></TabControl>
</TabsDef>
```

Controls not listed under any tab are always visible. Several controls may share an id to be toggled together.

## Window template attributes

All official unless noted. Shipping files always write every one.

| field | type | meaning |
|---|---|---|
| Name | name | lookup key; `custom0_window`..`custom19_window` for user windows |
| WindowId | id | label; the doc says debugging only |
| CloseButton / MoveButton | bool | stock close X (top right) / move grip (top left) |
| TopRightResizeButton | bool | cannot coexist with CloseButton |
| BottomRightResizeButton / BottomLeftResizeButton | bool | corner resize grips; supersede ResizeableTwoWay* |
| ResizeButtonOffsetX / ResizeButtonOffsetY | number | nudge the bottom grips (X from the respective side, Y from the bottom) |
| Width / Height | number | initial size |
| TitleWidth / TitleHeight | number | drag area from the top-left; 0 in either disables title dragging |
| ResizeableWidth / ResizeableHeight | number | size of the edge zones that allow one-axis resizing; the background needs GrowWidth/GrowHeight |
| ResizeableTwoWayWidth / ResizeableTwoWayHeight | number | legacy corner zones |
| MinWidth / MinHeight | number | computed lower bound is the innermost resizable control's minimum plus margins; going below it corrupts the image |
| ContextTemplateName | name | observed: window template used as the right-click context menu (alpha chooser, chat menus) |
| TabName | string | observed on a few tabbed stats windows |

## Which def for which adapter type

| adapter type | defs that display it |
|---|---|
| text | LabelDef (`Adapter`), CheckBoxDef (`TextAdapterName`), IconDef (`LabelAdapterName`), ButtonDef (`Adapter`) |
| multi-line text | TextAreaDef, EditBoxDef |
| scalar | ScalarLabelDef (`Adapter`), sliders |
| scalar 0-100 | StatusBarDef, VerticalStatusBarDef, StatusIconDef |
| scalar icon id | IconDef (`AdapterName`) |
| scalar 0/1 | CheckBoxDef (`AdapterName`) |
| color | any label/button via `ColorAdapter` |
| list | ListBoxDef, TreeControlDef, ComboBoxDef |
| chat buffer | ChatControlDef (`BufferName`: `chat` or `system`) |
| heading | CompassControlDef, StatusIconDef (`compass_heading`) |
