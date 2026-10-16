# Window reference

Two tables. The **stock** table is the Atlantis skin of the live 1.130 client (`ui/atlantis`, 83 files) and is
authoritative: the sizes are what the game ships, and the numeric `ControlId`s are the ones client code binds
(do not reuse them when adding controls to that window). The **BobsUI** table is a complete 1.127-era custom UI
(CynicalJedi/DAOC-UI-Chooser); its sizes and ids are that UI's own choices and it adds 20 custom windows.
Use both to answer: what is the file for window X, what is its template `Name`, what size does it have, and
which ids are taken.

Rules that matter here:

- The template `Name` is how the client finds a window. Keep the stock name when you restyle a stock window.
- `WindowId` is mostly a label (the doc says it is used for debugging). Custom windows use anything.
- Numeric `ControlId`s inside stock windows may be bound by client code (the doc warns not to reuse them).
  Inside custom windows they are yours; `TabsDef` uses them to assign controls to tabs.
- Files that are not in your `custom/` folder are loaded from `ui/atlantis/`, so you only ship what you change.
- `custom0_window` .. `custom19_window` are the user slots (see events.md, `ToggleCustomN`). In BobsUI they are
  used for its main menu, floating bars, command bar, tabbed XP, atlas, etc.; a fresh skin can use them freely.

## Contents

- [Stock windows (Atlantis, client 1.130)](#stock-windows-atlantis-client-1130)
- [Stock load order (uimain.xml)](#stock-load-order-uimainxml)
- [BobsUI windows (1.127 custom UI)](#bobsui-windows-1127-custom-ui)
- [Files that are not windows](#files-that-are-not-windows)
- [Include graph](#include-graph)

## Stock windows (Atlantis, client 1.130)

| template Name | WindowId | file | WxH | numeric ControlIds (code-bound) | control defs |
|---|---|---|---|---|---|
| `ChatRename` | chatRenameWindow | `chatrename.xml` | 300x80 | 1004 | ButtonDefx2, FullResizeImageDefx1, EditBoxDefx1 |
| `base` | c_windowInvalid | `base.xml` | 100x100 | - |  |
| `bazaar_query` | BazaarQuery | `bazaar_query.xml` | 390x420 | 1000..1041 (27 ids) | LabelDefx17, ComboBoxDefx10, ButtonDefx6, HorizontalResizeButtonDefx3, FullResizeImageDefx2 |
| `casual_group_finder_window` | - | `casual_group_finder_window.xml` | 200x200 | 1000..1007 (7 ids) | CheckBoxDefx5, LabelDefx2, ButtonDefx2, FullResizeImageDefx1 |
| `channel` | Channel | `channel_window.xml` | 86x212 | 1000..1010 (11 ids) | HorizontalResizeButtonDefx11, HorizontalResizeImageDefx10, FullResizeImageDefx1 |
| `chat` | Chat | `chat_window.xml` | 350x200 | 1000, 1001, 1002, 1003, 1004, 1005 | FullResizeImageDefx2, HorizontalResizeImageButtonDefx2, ChatControlDefx1, LabelDefx1, InvisibleButtonDefx1 |
| `chat_config` | ChatConfig | `chat_config_window.xml` | 333x436 | 1001..5031 (122 ids) | ButtonDefx54, LabelDefx34, HorizontalResizeButtonDefx31, CheckBoxDefx31, HorizontalResizeImageDefx29 |
| `chat_context` | ContextChat | `context_window.xml` | 121x155 | 1000..1007 (8 ids) | HorizontalResizeImageDefx7, HorizontalResizeButtonDefx4, HorizontalResizeImageButtonDefx4, FullResizeImageDefx1 |
| `chat_no_new_context` | ContextChat | `context_window.xml` | 121x136 | 1000..1007 (7 ids) | HorizontalResizeImageDefx6, HorizontalResizeImageButtonDefx4, HorizontalResizeButtonDefx3, FullResizeImageDefx1 |
| `clock` | Clock | `clock_window.xml` | 120x40 | - | FullResizeImageDefx1, LabelDefx1 |
| `command` | Command | `command_window.xml` | 135x216 | 0..21 (21 ids) | ButtonDefx22, FullResizeImageDefx1 |
| `community` | Community | `community_window.xml` | 605x410 | 1002..1503 (67 ids) | LabelDefx22, HorizontalResizeButtonDefx15, ScalarLabelDefx11, TextAreaDefx5, ButtonDefx5 |
| `compass` | Compass | `compass.xml` | 100x100 | 1000, 1001 | CompassControlDefx2 |
| `concentration` | Concentration | `concentration_window.xml` | 128x104 | 1000, 2000 | ImageAreaDefx2, FullResizeImageDefx1, LabelDefx1, StatusBarDefx1, ListBoxDefx1 |
| `context` | Context | `context_window.xml` | 121x25 | - |  |
| `context_default_channel` | ContextFontSize | `context_window.xml` | 110x148 | 2012..2019 (8 ids) | HorizontalResizeImageButtonDefx8, HorizontalResizeImageDefx7, FullResizeImageDefx1 |
| `context_font_alpha` | ContextFontAlpha | `context_window.xml` | 25x160 | 2001 | FullResizeImageDefx1, LabelDefx1, VerticalSliderDefx1 |
| `context_font_size` | ContextFontSize | `context_window.xml` | 44x184 | 2002..2011 (10 ids) | HorizontalResizeImageButtonDefx10, HorizontalResizeImageDefx9, FullResizeImageDefx1 |
| `context_sub` | ContextSub | `context_window.xml` | 121x25 | - |  |
| `context_window_alpha` | ContextWindowAlpha | `context_window.xml` | 25x160 | 2000 | FullResizeImageDefx1, LabelDefx1, VerticalSliderDefx1 |
| `daoc_subclass` | DAoC_Subclass | `daoc_subclass_window.xml` | 255x400 | 1000..2021 (8 ids) | ButtonDefx3, IconDefx3, FullResizeImageDefx2, LabelDefx2, HorizontalResizeImageDefx1 |
| `default_context` | - | `context_window.xml` | 121x41 | 1000, 1001 | HorizontalResizeImageButtonDefx2, FullResizeImageDefx1, HorizontalResizeImageDefx1 |
| `emblem_picker` | EmblemPicker | `emblem_picker.xml` | 230x300 | 1000..1009 (10 ids) | ButtonDefx10, LabelDefx5, FullResizeImageDefx1 |
| `emoticon` | Emoticon | `emoticon_window.xml` | 166x166 | 1000..1063 (64 ids) | HorizontalResizeImageButtonDefx64, FullResizeImageDefx1 |
| `emoticon_context` | ContextEmoticon | `context_window.xml` | 121x22 | 1000 | FullResizeImageDefx1, HorizontalResizeImageButtonDefx1 |
| `float_champ_exp_window` | float_champ_exp | `float_champ_exp_window.xml` | 108x40 | - | StatusBarDefx2, FullResizeImageDefx1, ScalarLabelDefx1, LabelDefx1 |
| `float_level_exp_window` | float_level_exp | `float_level_exp_window.xml` | 108x40 | - | StatusBarDefx2, FullResizeImageDefx1, ScalarLabelDefx1, LabelDefx1 |
| `float_realm_exp_window` | float_realm_exp | `float_realm_exp_window.xml` | 108x40 | - | StatusBarDefx2, FullResizeImageDefx1, LabelDefx1, ScalarLabelDefx1 |
| `float_target_window` | float_target | `float_target_window.xml` | 150x70 | - | HorizontalResizeButtonDefx6, FullResizeImageDefx1, StatusBarDefx1, ScalarLabelDefx1, LabelDefx1 |
| `group_buffs` | - | `group_buffs.xml` | 280x370 | - | LabelDefx17, ScalarLabelDefx8, IconSetDefx8, InvisibleButtonDefx8, FullResizeImageDefx1 |
| `group_options_window` | - | `group_options_window.xml` | 200x130 | 1000, 1001, 1002, 1003, 1004 | LabelDefx2, CheckBoxDefx2, ButtonDefx2, FullResizeImageDefx1 |
| `group_results` | - | `group_results_window.xml` | 484x448 | 1000..2006 (10 ids) | LabelDefx8, InvisibleButtonDefx7, FullResizeImageDefx1, ListBoxDefx1, ButtonDefx1 |
| `help` | Help | `help_window.xml` | 300x448 | 1000, 1001, 1002, 1003 | FullResizeImageDefx1, LabelDefx1, TextAreaDefx1, CheckBoxDefx1, ButtonDefx1 |
| `hookpoint_store` | Merchant | `hookpoint_merchant_window.xml` | 256x428 | 1000..1006 (7 ids) | LabelDefx13, HorizontalResizeImageDefx7, ButtonDefx5, ImageAreaDefx5, ScalarLabelDefx2 |
| `info` | Info | `info_window.xml` | 300x448 | 1001 | FullResizeImageDefx1, LabelDefx1, TextAreaDefx1 |
| `interact` | Interact | `interact_window.xml` | 384x320 | 1000 | FullResizeImageDefx1, TextAreaDefx1, LabelDefx1 |
| `interface_elements_window` | interface_elements | `interface_elements_window.xml` | 350x475 | - | HorizontalResizeButtonDefx29, LabelDefx6, FullResizeImageDefx1 |
| `keep_status` | - | `keep_status_window.xml` | 200x125 | - | LabelDefx5, ButtonDefx2, FullResizeImageDefx1 |
| `keep_upgrade` | - | `keep_upgrade_window.xml` | 256x128 | 1004, 1005 | LabelDefx4, ScalarLabelDefx2, ButtonDefx2, FullResizeImageDefx1 |
| `key_config` | KeyConfig | `key_config.xml` | 300x475 | 1000, 1010, 1011, 1012, 1013 | ButtonDefx7, LabelDefx6, CheckBoxDefx4, FullResizeImageDefx1, ListBoxDefx1 |
| `looking_for_group` | c_windowInvalid | `lfg_window.xml` | 440x330 | 1000..1263 (93 ids) | CheckBoxDefx78, ButtonDefx13, LabelDefx6, ScalarLabelDefx2, ComboBoxDefx2 |
| `main_chat_context` | ContextChat | `context_window.xml` | 121x116 | 1000, 1001, 1002, 1003, 1004, 1007 | HorizontalResizeImageDefx5, HorizontalResizeImageButtonDefx4, HorizontalResizeButtonDefx2, FullResizeImageDefx1 |
| `main_chat_no_new_context` | ContextChat | `context_window.xml` | 121x98 | 1000, 1001, 1002, 1003, 1007 | HorizontalResizeImageDefx4, HorizontalResizeImageButtonDefx4, FullResizeImageDefx1, HorizontalResizeButtonDefx1 |
| `main_menu_window` | main_menu | `main_menu_window.xml` | 225x250 | 20 | HorizontalResizeButtonDefx5, FullResizeImageDefx1, LabelDefx1 |
| `map_window` | - | `map_window.xml` | 270x498 | 1000..1107 (21 ids) | ImageAreaDefx12, LabelDefx7, ButtonDefx3, ComboBoxDefx2, FullResizeImageDefx1 |
| `master_level` | MasterLevel | `master_level_window.xml` | 200x200 | 1000, 1001, 2000 | ImageAreaDefx5, LabelDefx4, VerticalStatusBarDefx2, ButtonDefx2, FullResizeImageDefx1 |
| `menu_bar_window` | menu_bar | `menu_bar_window.xml` | 800x27 | 1001, 1002, 1003, 2000, 2001, 2002 | HorizontalResizeButtonDefx10, LabelDefx4, ImageAreaDefx4, StatusIconDefx3, StatusBarDefx2 |
| `merchant` | Merchant | `merchant_window.xml` | 350x458 | 1000..1009 (10 ids) | LabelDefx9, ButtonDefx7, HorizontalResizeImageDefx6, ImageAreaDefx5, FullResizeImageDefx1 |
| `mini_craft` | MiniCraft | `minicraft_window.xml` | 256x96 | 1000, 1001, 1002 | ButtonDefx3, FullResizeImageDefx1, LabelDefx1 |
| `mini_friends` | MiniFriends | `minifriends_window.xml` | 128x96 | 1009 | FullResizeImageDefx1, TextAreaDefx1, LabelDefx1 |
| `mini_group` | MiniGroup | `minigroup_window.xml` | 128x116 | 1000..1007 (8 ids) | StatusIconDefx16, LabelDefx9, StatusBarDefx8, InvisibleButtonDefx8, FullResizeImageDefx1 |
| `mini_info` | MiniInfo | `miniinfo_window.xml` | 144x114 | 1000..2000 (14 ids) | LabelDefx8, ButtonDefx4, FullResizeImageDefx1, IconDefx1, ListBoxDefx1 |
| `mini_pet` | MiniPet | `minipet_window.xml` | 135x125 | 1000..1009 (10 ids) | CheckBoxDefx7, IconDefx6, ImageAreaDefx4, ButtonDefx2, FullResizeImageDefx1 |
| `mino_relic` | MinoRelic | `mino_relic_window.xml` | 250x44 | 1000 | ImageAreaDefx2, FullResizeImageDefx1, HorizontalResizeImageDefx1, LabelDefx1, ButtonDefx1 |
| `mount` | Mount | `mount_window.xml` | 235x370 | 1001..1018 (18 ids) | LabelDefx10, ImageAreaDefx7, DockableIconDefx7, ButtonDefx4, FullResizeImageDefx3 |
| `new_group_window` | new_group | `new_group_window.xml` | 300x150 | 1000..2007 (9 ids) | ScalarLabelDefx32, LabelDefx16, StatusBarDefx8, InvisibleButtonDefx8, FullResizeImageDefx1 |
| `new_quest` | NewQuest | `new_quest_window.xml` | 300x400 | 1000..1025 (20 ids) | ImageAreaDefx21, IconDefx16, LabelDefx11, HorizontalResizeImageDefx3, StatusBarDefx2 |
| `new_quest_finish` | NewQuestFinish | `new_quest_finish_window.xml` | 300x400 | 1000..1025 (20 ids) | ImageAreaDefx21, IconDefx16, LabelDefx10, HorizontalResizeImageDefx3, StatusBarDefx2 |
| `new_quest_journal` | Quest | `new_quest_journal_window.xml` | 512x256 | 1000, 1001, 1002, 1003, 1004, 1005 | ImageAreaDefx3, FullResizeImageDefx2, HorizontalResizeImageDefx2, LabelDefx2, TreeControlDefx1 |
| `new_summary_window` | new_summary | `new_summary_window.xml` | 160x90 | - | ScalarLabelDefx11, LabelDefx7, StatusBarDefx4, FullResizeImageDefx1 |
| `options_window` | Options | `options_window.xml` | 390x600 | 1000..1031 (31 ids) | LabelDefx24, ComboBoxDefx13, CheckBoxDefx11, ButtonDefx5, FullResizeImageDefx1 |
| `performance` | PerformanceWindow | `performance_window.xml` | 96x32 | 1000, 1001, 1002, 2000, 2001, 2002 | StatusIconDefx6 |
| `quest` | Quest | `quest_window.xml` | 512x256 | 1000, 1001, 1002, 1003, 1004, 1005 | ImageAreaDefx3, FullResizeImageDefx1, TextAreaDefx1, ButtonDefx1, HorizontalResizeImageDefx1 |
| `quiver` | WindowQuiver | `quiver_window.xml` | 240x100 | 1000, 1001, 1002, 1003, 5000 | InvisibleButtonDefx8, LabelDefx5, IconDefx4, FullResizeImageDefx2 |
| `realm_bonuses` | - | `realm_bonuses.xml` | 300x500 | - | LabelDefx50, FullResizeImageDefx5 |
| `realmwar_agramon` | - | `realmwar_agramon.xml` | 394x288 | 1000..3405 (101 ids) | StatusIconDefx69, ImageAreaDefx16, InvisibleButtonDefx9, LabelDefx6, CheckBoxDefx4 |
| `realmwar_alb` | - | `realmwar_alb.xml` | 266x416 | 1000..3412 (205 ids) | StatusIconDefx101, ImageAreaDefx57, InvisibleButtonDefx41, LabelDefx6, CheckBoxDefx4 |
| `realmwar_hib` | - | `realmwar_hib.xml` | 266x416 | 1000..3412 (205 ids) | StatusIconDefx101, ImageAreaDefx57, InvisibleButtonDefx41, LabelDefx6, CheckBoxDefx4 |
| `realmwar_key` | - | `realmwar_key.xml` | 140x250 | - | LabelDefx15, ImageAreaDefx14, FullResizeImageDefx1 |
| `realmwar_mid` | - | `realmwar_mid.xml` | 394x288 | 1000..3412 (205 ids) | StatusIconDefx101, ImageAreaDefx57, InvisibleButtonDefx41, LabelDefx6, CheckBoxDefx4 |
| `release_window` | Release | `release_window.xml` | 285x96 | 1000 | HorizontalResizeButtonDefx4, ImageAreaDefx2, FullResizeImageDefx1, StatusBarDefx1, LabelDefx1 |
| `siege` | - | `siege_window.xml` | 240x210 | 1000..1107 (10 ids) | LabelDefx6, ButtonDefx6, ImageAreaDefx6, StatusBarDefx2, FullResizeImageDefx1 |
| `siegetower_status` | - | `siegetower_status_window.xml` | 200x57 | - | FullResizeImageDefx1, LabelDefx1, ButtonDefx1 |
| `stats_attributes` | StatsAttributes | `stats_attributes_window.xml` | 192x416 | 1000..1100 (30 ids) | LabelDefx34, HorizontalResizeImageDefx24, ScalarLabelDefx14, ButtonDefx6, FullResizeImageDefx3 |
| `stats_combat` | c_windowInvalid | `stats_combat_window.xml` | 192x416 | 1000 | FullResizeImageDefx2, HorizontalResizeImageDefx1, LabelDefx1, TreeControlDefx1, ButtonDefx1 |
| `stats_group` | StatsGroup | `stats_group_window.xml` | 192x416 | 1000..2007 (16 ids) | IconDefx48, StatusBarDefx24, LabelDefx16, ButtonDefx14, ImageAreaDefx8 |
| `stats_index` | StatsIndex | `stats_index_window.xml` | 192x32 | 1000..1006 (7 ids) | CheckBoxDefx6, ImageAreaDefx1, ButtonDefx1 |
| `stats_spec_abil` | Stats_Spec_Abil | `stats_spec_abil_window.xml` | 192x416 | 1000, 1001, 1002, 1003 | HorizontalResizeImageDefx4, LabelDefx4, ListBoxDefx3, FullResizeImageDefx1 |
| `stats_spells` | c_windowInvalid | `stats_spells_window.xml` | 192x416 | 1000, 1001, 1002 | FullResizeImageDefx2, ButtonDefx2, HorizontalResizeImageDefx1, TreeControlDefx1, LabelDefx1 |
| `summary` | c_windowInvalid | `summary.xml` | 128x100 | 1001, 1002, 1003 | ImageAreaDefx8, StatusBarDefx6, ScalarLabelDefx4, LabelDefx3, FullResizeImageDefx1 |
| `timer` | Timer | `timer_window.xml` | 300x96 | 1000 | FullResizeImageDefx2, ImageAreaDefx2, StatusBarDefx1, LabelDefx1 |
| `title` | Title | `title_window.xml` | 435x280 | 1001, 1002, 1003, 1004 | LabelDefx3, ButtonDefx2, FullResizeImageDefx1, ListBoxDefx1, TextAreaDefx1 |
| `train` | Train | `train.xml` | 300x450 | 1000, 1001, 1002, 1003 | LabelDefx5, HorizontalResizeImageDefx4, ButtonDefx2, ListBoxDefx2, FullResizeImageDefx1 |
| `training_window` | Training | `training_window.xml` | 390x536 | 1000..1902 (197 ids) | ScalarLabelDefx59, IconDefx56, LabelDefx37, InvisibleButtonDefx22, HorizontalSliderDefx22 |
| `value_chooser` | ValueChooser | `value_chooser.xml` | 128x96 | - | ButtonDefx4, LabelDefx2, FullResizeImageDefx1, ScalarLabelDefx1 |
| `vault_window` | Vault | `vault_window.xml` | 300x430 | 1000, 1001, 1002, 1003, 1004, 1005 | ButtonDefx3, FullResizeImageDefx2, LabelDefx2, VerticalResizeImageDefx1, ListBoxDefx1 |

## Stock load order (uimain.xml)

`ui/uimain.xml` (never edit) includes these files in this order; `styles.xml` first, `assets.xml` near the end.
Each is resolved in `ui/custom/` first, then `ui/atlantis/`. Custom windows are not in this list, which is
why they need an `<Include>` from one of these files.

`styles.xml`, `training_window.xml`, `command_window.xml`, `timer_window.xml`, `clock_window.xml`, `interact_window.xml`, `quest_window.xml`, `new_quest_journal_window.xml`, `info_window.xml`, `minifriends_window.xml`, `minigroup_window.xml`, `minicraft_window.xml`, `miniinfo_window.xml`, `concentration_window.xml`, `chat_window.xml`, `master_level_window.xml`, `chat_config_window.xml`, `train.xml`, `compass.xml`, `merchant_window.xml`, `summary.xml`, `stats_index_window.xml`, `stats_attributes_window.xml`, `stats_group_window.xml`, `siege_window.xml`, `performance_window.xml`, `minipet_window.xml`, `help_window.xml`, `options_window.xml`, `emblem_picker.xml`, `value_chooser.xml`, `stats_spells_window.xml`, `vault_window.xml`, `group_results_window.xml`, `lfg_window.xml`, `stats_spec_abil_window.xml`, `stats_combat_window.xml`, `quiver_window.xml`, `group_buffs.xml`, `keep_upgrade_window.xml`, `keep_status_window.xml`, `hookpoint_merchant_window.xml`, `realmwar_hib.xml`, `realmwar_mid.xml`, `realmwar_alb.xml`, `realmwar_agramon.xml`, `realmwar_key.xml`, `realm_bonuses.xml`, `map_window.xml`, `key_config.xml`, `title_window.xml`, `community_window.xml`, `mount_window.xml`, `daoc_subclass_window.xml`, `new_quest_window.xml`, `new_quest_finish_window.xml`, `mino_relic_window.xml`, `emoticon_window.xml`, `channel_window.xml`, `context_window.xml`, `ChatRename.xml`, `siegetower_status_window.xml`, `bazaar_query.xml`, `main_menu_window.xml`, `menu_bar_window.xml`, `interface_elements_window.xml`, `new_group_window.xml`, `new_summary_window.xml`, `float_target_window.xml`, `float_level_exp_window.xml`, `float_realm_exp_window.xml`, `float_champ_exp_window.xml`, `release_window.xml`, `assets.xml`, `casual_group_finder_window.xml`, `group_options_window.xml`

## BobsUI windows (1.127 custom UI)

| template Name | WindowId | file | WxH | numeric ControlIds used | control defs |
|---|---|---|---|---|---|
| `ChatRename` | chatRenameWindow | `chatrename.xml` | 250x86 | 1004 | FullResizeImageDefx2, LabelDefx2, ButtonDefx2, EditBoxDefx1 |
| `alpha_chooser` | AlphaChooser | `alpha_chooser.xml` | 0x0 | - |  |
| `base` | c_windowInvalid | `base.xml` | 0x0 | - |  |
| `bazaar_query` | BazaarQuery | `bazaar_query.xml` | 450x308 | 1000..1029 (29 ids) | LabelDefx22, ButtonDefx13, ComboBoxDefx9, FullResizeImageDefx3, HorizontalResizeImageDefx3 |
| `casual_group_finder_window` | - | `casual_group_finder_window.xml` | 210x193 | 1000..1007 (7 ids) | CheckBoxDefx5, LabelDefx4, FullResizeImageDefx3, HorizontalResizeImageDefx2, ButtonDefx2 |
| `channel` | Channel | `channel_window.xml` | 110x226 | 1000..1010 (11 ids) | HorizontalResizeButtonDefx11, FullResizeImageDefx2 |
| `chat` | - | `chat_window.xml` | 310x121 | 1000, 1001, 1002, 1003, 1004, 1005 | FullResizeImageDefx2, HorizontalResizeImageButtonDefx2, ChatControlDefx1, LabelDefx1, InvisibleButtonDefx1 |
| `chat_config` | ChatConfig | `chat_config_window.xml` | 310x430 | 1001..5031 (91 ids) | ButtonDefx54, LabelDefx35, CheckBoxDefx31, FullResizeImageDefx5, HorizontalResizeImageDefx3 |
| `chat_context` | ContextChat | `context_chat_sub.xml` | 130x172 | 1007 | ButtonDefx8, FullResizeImageDefx2 |
| `chat_no_new_context` | ContextChat | `context_chat_sub2.xml` | 130x172 | 1007 | ButtonDefx8, FullResizeImageDefx2 |
| `clock` | Clock | `clock_window.xml` | 210x25 | - | FullResizeImageDefx1, LabelDefx1, InvisibleButtonDefx1 |
| `command` | Command | `command_window.xml` | 310x99 | 1100..1620 (85 ids) | ButtonDefx72, FullResizeImageDefx13, TabsDefx1, LabelDefx1, ImageAreaDefx1 |
| `community` | Social | `community_window.xml` | 610x419 | 1002..1590 (67 ids) | ButtonDefx20, LabelDefx19, ScalarLabelDefx11, HorizontalResizeImageDefx7, TextAreaDefx5 |
| `compass` | Compass | `compass.xml` | 88x88 | - | StatusIconDefx3 |
| `concentration` | Concentration | `concentration_window.xml` | 210x210 | 2000 | LabelDefx3, FullResizeImageDefx1, InvisibleButtonDefx1, ListBoxDefx1, StatusBarDefx1 |
| `context` | Context | `context_base.xml` | 96x25 | - |  |
| `context_default_channel` | ContextFontSize | `context_default_chat_channel.xml` | 130x172 | 2012..2019 (8 ids) | HorizontalResizeImageButtonDefx8, FullResizeImageDefx2 |
| `context_font_alpha` | ContextFontAlpha | `context_font_alpha.xml` | 58x172 | 2001 | FullResizeImageDefx2, LabelDefx1, VerticalSliderDefx1 |
| `context_font_size` | ContextFontSize | `context_font_size.xml` | 70x208 | 2002..2011 (10 ids) | HorizontalResizeImageButtonDefx10, FullResizeImageDefx2 |
| `context_sub` | ContextSub | `context_base_sub.xml` | 96x25 | - |  |
| `context_window_alpha` | ContextWindowAlpha | `context_window_alpha.xml` | 58x172 | 2000 | FullResizeImageDefx2, LabelDefx1, VerticalSliderDefx1 |
| `custom0_window` | Main Menu | `custom0_window.xml` | 310x406 | - | ButtonDefx48, LabelDefx9, FullResizeImageDefx5, HorizontalResizeImageDefx4 |
| `custom10_window` | Command Bar | `custom10_window.xml` | 371x20 | - | ButtonDefx6, FullResizeImageDefx1 |
| `custom11_window` | Tabbed XP | `custom11_window.xml` | 210x71 | 1100..1407 (32 ids) | LabelDefx8, ScalarLabelDefx8, StatusIconDefx7, FullResizeImageDefx6, InvisibleButtonDefx4 |
| `custom12_window` | custom12_window | `custom12_window.xml` | 40x40 | - | FullResizeImageDefx1, ListBoxDefx1 |
| `custom13_window` | custom13_window | `custom13_window.xml` | 340x175 | 1100..1401 (19 ids) | HorizontalResizeImageDefx9, FullResizeImageDefx6, DynamicImageDefx4, LabelDefx2, TabsDefx1 |
| `custom14_window` | Artifacts | `custom14_window.xml` | 210x100 | - | LabelDefx5, FullResizeImageDefx2 |
| `custom15_window` | Atlas | `custom15_window.xml` | 210x100 | - | LabelDefx5, FullResizeImageDefx2 |
| `custom16_window` | Crafting | `custom16_window.xml` | 210x100 | - | LabelDefx5, FullResizeImageDefx2 |
| `custom17_window` | Realm Ranks | `custom17_window.xml` | 600x324 | 1100..1630 (74 ids) | HorizontalResizeImageDefx35, LabelDefx23, FullResizeImageDefx8, ScalarLabelDefx6, DynamicImageDefx6 |
| `custom18_window` | Video Screen | `custom18_window.xml` | 210x100 | - | LabelDefx5, FullResizeImageDefx2 |
| `custom19_window` | zExtra | `custom19_window.xml` | 210x100 | - | FullResizeImageDefx2, LabelDefx2 |
| `custom1_window` | Floating Player Health | `custom1_window.xml` | 125x35 | - | ImageAreaDefx2, InvisibleButtonDefx2, LabelDefx1, StatusIconDefx1, ScalarLabelDefx1 |
| `custom2_window` | Floating Player End | `custom2_window.xml` | 125x19 | - | ImageAreaDefx2, StatusIconDefx1, ScalarLabelDefx1 |
| `custom3_window` | Floating Player Pwr | `custom3_window.xml` | 125x19 | - | ImageAreaDefx2, StatusIconDefx1, ScalarLabelDefx1 |
| `custom4_window` | Floating Target Health | `custom4_window.xml` | 125x35 | - | ImageAreaDefx2, InvisibleButtonDefx2, LabelDefx1, StatusIconDefx1, ScalarLabelDefx1 |
| `custom5_window` | custom5_window | `HHelperCubeWindow1.xml` | 210x210 | - | StatusIconDefx26, ScalarLabelDefx25, LabelDefx24, ButtonDefx10, FullResizeImageDefx1 |
| `custom6_window` | custom6_window | `HHelperHorizWindow4.xml` | 191x121 | - | ScalarLabelDefx24, StatusIconDefx16, LabelDefx16, ButtonDefx8 |
| `custom7_window` | custom7_window | `HHelperVertWindow4.xml` | 101x227 | - | ScalarLabelDefx24, StatusIconDefx16, LabelDefx16, ButtonDefx8 |
| `custom8_window` | Mini Attributes | `custom8_window.xml` | 210x71 | - | LabelDefx12, ScalarLabelDefx12, FullResizeImageDefx2 |
| `custom9_window` | Mini Resists | `custom9_window.xml` | 210x71 | - | LabelDefx18, FullResizeImageDefx2 |
| `daoc_subclass` | Train Subclass | `daoc_subclass_window.xml` | 310x400 | 1000..2021 (8 ids) | IconDefx3, ButtonDefx3, FullResizeImageDefx2, LabelDefx2, HorizontalResizeImageDefx1 |
| `default_context` | Alpha Chooser | `context_default.xml` | 130x64 | - | FullResizeImageDefx2, ButtonDefx2 |
| `emblem_picker` | EmblemPicker | `emblem_picker.xml` | 360x196 | 1000, 1001 | ButtonDefx10, LabelDefx8, FullResizeImageDefx4, HorizontalResizeImageDefx3 |
| `emoticon` | Emoticon | `emoticon_window.xml` | 166x166 | 1000..1063 (64 ids) | HorizontalResizeImageButtonDefx64, FullResizeImageDefx1 |
| `emoticon_context` | contextemoticon | `context_emoticon.xml` | 130x64 | - | FullResizeImageDefx2, ButtonDefx2 |
| `float_champ_exp_window` | float_champ_exp | `float_champ_exp_window.xml` | 138x32 | - | StatusIconDefx2, FullResizeImageDefx1, LabelDefx1, ScalarLabelDefx1 |
| `float_level_exp_window` | float_level_exp | `float_level_exp_window.xml` | 138x32 | - | StatusIconDefx2, FullResizeImageDefx1, LabelDefx1, ScalarLabelDefx1 |
| `float_realm_exp_window` | float_realm_exp | `float_realm_exp_window.xml` | 138x32 | - | StatusIconDefx2, FullResizeImageDefx1, LabelDefx1, ScalarLabelDefx1 |
| `float_target_window` | float_target | `float_target_window.xml` | 150x70 | - | HorizontalResizeButtonDefx6, FullResizeImageDefx1, LabelDefx1, ScalarLabelDefx1, StatusBarDefx1 |
| `group_buffs` | - | `group_buffs.xml` | 350x338 | - | IconDefx200, LabelDefx17, InvisibleButtonDefx9, ScalarLabelDefx8, HorizontalResizeImageDefx8 |
| `group_options_window` | - | `group_options_window.xml` | 210x193 | 1000, 1001, 1002, 1003, 1004 | LabelDefx4, FullResizeImageDefx3, HorizontalResizeImageDefx2, CheckBoxDefx2, ButtonDefx2 |
| `group_results` | LFG Results | `group_results_window.xml` | 550x154 | 1000..2006 (10 ids) | LabelDefx9, InvisibleButtonDefx7, FullResizeImageDefx1, HorizontalResizeImageDefx1, ListBoxDefx1 |
| `help` | Help | `help_window.xml` | 310x310 | 1000, 1001, 1002, 1003 | FullResizeImageDefx1, LabelDefx1, TextAreaDefx1, CheckBoxDefx1, ButtonDefx1 |
| `hookpoint_store` | Merchant Hookpoint | `hookpoint_merchant_window.xml` | 310x350 | 1000..1006 (7 ids) | LabelDefx9, ButtonDefx5, HorizontalResizeImageDefx2, ScalarLabelDefx2, FullResizeImageDefx1 |
| `info` | Info | `info_window.xml` | 310x310 | 1001 | FullResizeImageDefx1, LabelDefx1, TextAreaDefx1 |
| `interact` | Interact | `interact_window.xml` | 310x310 | 1000 | LabelDefx3, FullResizeImageDefx1, TextAreaDefx1 |
| `interface_elements_window` | Interface Options | `interface_elements_window.xml` | 310x406 | 2001 | HorizontalResizeButtonDefx30, LabelDefx9, FullResizeImageDefx6, HorizontalResizeImageDefx5, ButtonDefx2 |
| `keep_status` | Keep Status | `keep_status_window.xml` | 210x124 | - | LabelDefx5, FullResizeImageDefx2, ButtonDefx2 |
| `keep_upgrade` | Keep Upgrade | `keep_upgrade_window.xml` | 210x98 | 1004 | LabelDefx3, FullResizeImageDefx2, ScalarLabelDefx2, ButtonDefx2 |
| `key_config` | KeyConfig | `key_config.xml` | 300x475 | 1000, 1010, 1011, 1012, 1013 | ButtonDefx7, LabelDefx6, CheckBoxDefx4, FullResizeImageDefx2, ListBoxDefx1 |
| `looking_for_group` | Looking for Group | `lfg_window.xml` | 450x388 | 1000..1263 (89 ids) | CheckBoxDefx78, ButtonDefx13, LabelDefx8, FullResizeImageDefx4, HorizontalResizeImageDefx3 |
| `main_chat_context` | ContextChat | `context_chat_main.xml` | 130x172 | 1007 | ButtonDefx8, FullResizeImageDefx2 |
| `main_chat_no_new_context` | ContextChat | `context_chat_main2.xml` | 130x172 | 1007 | ButtonDefx8, FullResizeImageDefx2 |
| `main_menu_window` | main_menu | `main_menu_window.xml` | 210x149 | - | HorizontalResizeButtonDefx6, FullResizeImageDefx2, LabelDefx1 |
| `map_window` | Map Window | `map_window.xml` | 278x412 | 1000..1107 (19 ids) | ImageAreaDefx12, ButtonDefx3, FullResizeImageDefx2, LabelDefx2, ComboBoxDefx2 |
| `master_level` | Master Level | `master_level_window.xml` | 310x200 | 2000 | LabelDefx5, ButtonDefx3, FullResizeImageDefx1, HorizontalResizeImageDefx1, ScalarLabelDefx1 |
| `menu_bar_window` | menu_bar | `menu_bar_window.xml` | 1000x26 | 1001, 1002, 1003, 2000, 2001, 2002 | HorizontalResizeButtonDefx10, LabelDefx4, ImageAreaDefx4, StatusIconDefx3, StatusBarDefx2 |
| `merchant` | Merchant | `merchant_window.xml` | 310x406 | 1002, 1003, 1004, 1005, 1006, 1009 | LabelDefx9, ButtonDefx7, FullResizeImageDefx1, HorizontalResizeImageDefx1, ListBoxDefx1 |
| `mini_craft` | Mini Craft | `minicraft_window.xml` | 310x100 | 1000, 1001, 1002 | ButtonDefx3, FullResizeImageDefx2, LabelDefx2 |
| `mini_friends` | Mini Friends | `minifriends_window.xml` | 100x100 | 1009 | FullResizeImageDefx1, LabelDefx1, TextAreaDefx1 |
| `mini_group` | MiniGroup | `minigroup_window.xml` | 400x53 | - | StatusIconDefx24, ScalarLabelDefx24, StatusBarDefx16, ButtonDefx9, LabelDefx8 |
| `mini_info` | Mini Info | `miniinfo_window.xml` | 310x146 | 1000..2000 (14 ids) | LabelDefx8, ButtonDefx4, FullResizeImageDefx2, IconDefx1, ListBoxDefx1 |
| `mini_pet` | Mini Pet | `minipet_window.xml` | 160x162 | 1000..1009 (10 ids) | CheckBoxDefx7, IconDefx6, FullResizeImageDefx2, ButtonDefx2, LabelDefx1 |
| `mino_relic` | Mino Relic | `mino_relic_window.xml` | 210x77 | 1000 | FullResizeImageDefx2, LabelDefx1, StatusIconDefx1, ScalarLabelDefx1, ButtonDefx1 |
| `mount` | Mount | `mount_window.xml` | 236x359 | 1001..1018 (18 ids) | LabelDefx10, ImageAreaDefx7, DockableIconDefx7, ButtonDefx4, FullResizeImageDefx3 |
| `new_group_window` | new_group | `new_group_window.xml` | 300x152 | 1000..2007 (9 ids) | ScalarLabelDefx32, LabelDefx16, StatusBarDefx8, ButtonDefx8, FullResizeImageDefx1 |
| `new_quest` | Quest Start | `new_quest_window.xml` | 310x400 | 1000..1025 (20 ids) | IconDefx16, LabelDefx12, HorizontalResizeImageDefx6, FullResizeImageDefx3, StatusBarDefx2 |
| `new_quest_finish` | Quest Finish | `new_quest_finish_window.xml` | 310x400 | 1000..1025 (20 ids) | IconDefx16, LabelDefx12, HorizontalResizeImageDefx6, FullResizeImageDefx3, StatusBarDefx2 |
| `new_quest_journal` | Quest Journal | `new_quest_journal_window.xml` | 512x200 | 1000, 1001, 1002, 1003, 1004, 1005 | ImageAreaDefx3, FullResizeImageDefx2, TreeControlDefx1, ButtonDefx1, HorizontalResizeImageDefx1 |
| `new_summary_window` | new_summary | `new_summary_window.xml` | 160x88 | - | ScalarLabelDefx9, LabelDefx7, StatusBarDefx4, FullResizeImageDefx1 |
| `options_window` | Options | `options_window.xml` | 340x315 | 1000..1408 (67 ids) | LabelDefx26, ComboBoxDefx13, CheckBoxDefx11, FullResizeImageDefx7, HorizontalResizeImageDefx7 |
| `performance` | Performance | `performance_window.xml` | 96x32 | 1000, 1001, 1002, 2000, 2001, 2002 | StatusIconDefx6 |
| `quest` | Quest | `quest_window_orig.xml` | 310x200 | 1000, 1001, 1002, 1003, 1004, 1005 | ImageAreaDefx3, FullResizeImageDefx1, TextAreaDefx1, ButtonDefx1, HorizontalResizeImageDefx1 |
| `quiver` | WindowQuiver | `quiver_window.xml` | 310x122 | 1000, 1001, 1002, 1003, 5000 | InvisibleButtonDefx9, LabelDefx5, ImageAreaDefx4, IconDefx4, FullResizeImageDefx3 |
| `realm_bonuses` | - | `realm_bonuses.xml` | 300x500 | - | LabelDefx50, FullResizeImageDefx5 |
| `realmwar_agramon` | - | `realmwar_agramon.xml` | 266x310 | 1000..3405 (101 ids) | StatusIconDefx69, ImageAreaDefx16, InvisibleButtonDefx9, LabelDefx6, ButtonDefx5 |
| `realmwar_alb` | - | `realmwar_alb.xml` | 266x416 | 1000..3412 (205 ids) | StatusIconDefx101, ImageAreaDefx57, InvisibleButtonDefx41, CheckBoxDefx7, LabelDefx6 |
| `realmwar_hib` | - | `realmwar_hib.xml` | 266x416 | 1000..3412 (205 ids) | StatusIconDefx101, ImageAreaDefx57, InvisibleButtonDefx41, CheckBoxDefx7, LabelDefx6 |
| `realmwar_key` | - | `realmwar_key.xml` | 140x250 | - | LabelDefx15, ImageAreaDefx14, FullResizeImageDefx1 |
| `realmwar_mid` | - | `realmwar_mid.xml` | 394x288 | 1000..3412 (205 ids) | StatusIconDefx101, ImageAreaDefx57, InvisibleButtonDefx41, CheckBoxDefx7, LabelDefx6 |
| `release_window` | Release | `release_window.xml` | 275x97 | - | HorizontalResizeButtonDefx4, FullResizeImageDefx2, LabelDefx1, StatusIconDefx1, ScalarLabelDefx1 |
| `siege` | Siege | `siege_window.xml` | 275x176 | 1000, 1001, 1105 | LabelDefx9, ButtonDefx6, ImageAreaDefx4, FullResizeImageDefx3, ScalarLabelDefx2 |
| `siegetower_status` | Siege Tower | `siegetower_status_window.xml` | 210x98 | - | FullResizeImageDefx2, LabelDefx2, ButtonDefx1 |
| `stats_attributes` | Stats Attributes | `stats_attributes_window.xml` | 210x423 | 1000..1100 (13 ids) | LabelDefx35, ScalarLabelDefx14, ButtonDefx6, FullResizeImageDefx4, InvisibleButtonDefx4 |
| `stats_combat` | Status Combat | `stats_combat_window.xml` | 210x423 | - | FullResizeImageDefx2, ButtonDefx2, HorizontalResizeImageDefx1, LabelDefx1, TreeControlDefx1 |
| `stats_group` | Status Group | `stats_group_window.xml` | 210x444 | 1002, 1003, 1004 | IconDefx48, StatusBarDefx24, LabelDefx17, ButtonDefx11, InvisibleButtonDefx9 |
| `stats_index` | Status Index | `stats_index_window.xml` | 210x32 | - | CheckBoxDefx6, ImageAreaDefx1, ButtonDefx1 |
| `stats_spec_abil` | Status Special Abilities | `stats_spec_abil_window.xml` | 210x423 | 1000, 1001, 1002, 1003 | LabelDefx5, HorizontalResizeImageDefx3, ListBoxDefx3, FullResizeImageDefx1 |
| `stats_spells` | Status Spells | `stats_spells_window.xml` | 210x423 | - | FullResizeImageDefx2, ButtonDefx2, HorizontalResizeImageDefx1, LabelDefx1, TreeControlDefx1 |
| `summary` | - | `summary.xml` | 210x88 | - | LabelDefx7, CheckBoxDefx5, StatusIconDefx4, ScalarLabelDefx3, FullResizeImageDefx2 |
| `timer` | Timer | `timer_window.xml` | 144x35 | - | ImageAreaDefx1, LabelDefx1, StatusIconDefx1, ScalarLabelDefx1, HorizontalResizeImageDefx1 |
| `title` | Title | `title_window.xml` | 420x250 | 1001, 1002, 1003, 1004 | LabelDefx4, HorizontalResizeImageDefx2, ButtonDefx2, FullResizeImageDefx1, ListBoxDefx1 |
| `train` | Train | `train.xml` | 310x400 | 1000, 1001, 1002, 1003 | LabelDefx5, HorizontalResizeImageDefx2, ListBoxDefx2, ButtonDefx2, FullResizeImageDefx1 |
| `training_window` | Training | `training_window.xml` | 385x582 | 1000..3405 (224 ids) | ScalarLabelDefx59, IconDefx56, LabelDefx47, InvisibleButtonDefx22, HorizontalSliderDefx22 |
| `value_chooser` | Value Chooser | `value_chooser.xml` | 185x105 | - | ButtonDefx6, FullResizeImageDefx2, LabelDefx2, ScalarLabelDefx1 |
| `vault_window` | Vault | `vault_window.xml` | 310x445 | - | ButtonDefx3, FullResizeImageDefx2, LabelDefx2, VerticalResizeImageDefx1, ListBoxDefx1 |

## Files that are not windows

Template/asset collections. `styles.xml` and `assets.xml` are the two the client always loads;
everything else is pulled in by an `<Include>`.

- `AtlasAlbionImages.xml`
- `AtlasHiberniaImages.xml`
- `AtlasMidgardImages.xml`
- `AtlasSharedImages.xml`
- `ButtonImages.xml`
- `ChantBackground.xml`
- `ChatFont.xml`
- `CommandBarBackground.xml`
- `CompassInnerImages.xml`
- `CompassOuterImages.xml`
- `DialogImages.xml` includes 2 files
- `DialogImagesBackground.xml` includes 1 files
- `DialogImagesBackgroundFrames.xml`
- `DialogImagesInterior.xml` includes 1 files
- `DialogImagesInteriorFrames.xml`
- `FrameImages.xml`
- `HHelperCenterImages.xml`
- `HHelperCubeWindow.xml` includes 1 files
- `HHelperExteriorImages.xml`
- `HHelperExteriorImages2.xml`
- `HHelperExteriorImages3.xml`
- `HHelperHorizWindow.xml` includes 1 files
- `HHelperHorizWindow1.xml`
- `HHelperHorizWindow2.xml`
- `HHelperHorizWindow3.xml`
- `HHelperInteriorImages.xml`
- `HHelperInteriorImages2.xml`
- `HHelperMiscImages.xml` includes 2 files
- `HHelperVertWindow.xml` includes 1 files
- `HHelperVertWindow1.xml`
- `HHelperVertWindow2.xml`
- `HHelperVertWindow3.xml`
- `MountImages.xml`
- `RCompassBGImages.xml`
- `RCompassInnerFrameImages.xml`
- `RCompassOuterFrameImages.xml`
- `RelicGateLinks.xml`
- `StatusIndexBackground.xml`
- `Styles/Button_Templates.xml`
- `Styles/ChatControl_Templates.xml`
- `Styles/CheckBox_Templates.xml`
- `Styles/ComboBox_Templates.xml`
- `Styles/CompassControl_Templates.xml`
- `Styles/FullResizeImage_Templates.xml`
- `Styles/HorizontalResizeButton_Templates.xml`
- `Styles/HorizontalResizeImage_Templates.xml`
- `Styles/IconSet_Templates.xml`
- `Styles/Icon_Templates.xml`
- `Styles/ImageArea_Templates.xml`
- `Styles/ListBox_Templates.xml`
- `Styles/ListboxHeader_Templates.xml`
- `Styles/Menu_Templates.xml`
- `Styles/OldStyle_Templates.xml`
- `Styles/StatusBar_Templates.xml`
- `Styles/StatusIcon_Templates.xml`
- `Styles/Tab_Templates.xml`
- `Styles/TextArea_Templates.xml`
- `Styles/TreeControl_Templates.xml`
- `Styles/VerticalResizeImage_Templates.xml`
- `Styles/VerticalScrollBar_Templates.xml`
- `Styles/VerticalStatusBar_Templates.xml`
- `SummaryCombatImages1.xml`
- `SummaryCombatImages1s.xml`
- `SummaryCombatImages2.xml`
- `SummaryCombatImages2s.xml`
- `SummaryCombatImages3.xml`
- `SummaryCombatImages3s.xml`
- `SummaryCombatImages4.xml`
- `SummaryCombatImages5.xml`
- `SummaryCombatImages5s.xml`
- `SummaryCombatImages6.xml`
- `SummaryCombatImages6s.xml`
- `SummaryCombatImages7.xml`
- `SummaryCombatImages7s.xml`
- `SummaryCombatImages8.xml`
- `SummaryCombatImages8s.xml`
- `SummaryCombatImages9.xml`
- `SummaryHUDFrame1.xml`
- `SummaryHUDFrame2.xml`
- `SummaryMoewenFrame1.xml`
- `SummaryMoewenFrame2.xml`
- `SummaryWoWFrame1.xml`
- `TargetImages.xml`
- `TargetImages2.xml`
- `TargetImages3.xml`
- `TargetImages4.xml`
- `TargetImages4L.xml`
- `ToolTips.xml`
- `VideoScreenImages.xml`
- `assets.xml` includes 26 files
- `context_window.xml` includes 12 files
- `custom5_window.xml` includes 1 files
- `custom6_window.xml` includes 1 files
- `custom7_window.xml` includes 1 files
- `guild_command_window.xml`
- `quest_window.xml`
- `styles.xml` includes 24 files

## Include graph

Files that include other files (reference UI):

- `DialogImages.xml` -> `DialogImagesBackground.xml`, `DialogImagesInterior.xml`
- `DialogImagesBackground.xml` -> `DialogImagesBackgroundFrames.xml`
- `DialogImagesInterior.xml` -> `DialogImagesInteriorFrames.xml`
- `HHelperCubeWindow.xml` -> `HHelperCubeWindow1.xml`
- `HHelperCubeWindow1.xml` -> `HHelperMiscImages.xml`, `HHelperCenterImages.xml`
- `HHelperHorizWindow.xml` -> `HHelperHorizWindow2.xml`
- `HHelperMiscImages.xml` -> `HHelperExteriorImages.xml`, `HHelperInteriorImages.xml`
- `HHelperVertWindow.xml` -> `HHelperVertWindow2.xml`
- `assets.xml` -> `ChatFont.xml`, `DialogImages.xml`, `FrameImages.xml`, `ButtonImages.xml`, `MountImages.xml`, `RelicGateLinks.xml`, `custom0_window.xml`, `custom1_window.xml`, `custom2_window.xml`, `custom3_window.xml`, `custom4_window.xml`, `custom5_window.xml`, `custom6_window.xml`, `custom7_window.xml`, `custom8_window.xml`, `custom9_window.xml`, `custom10_window.xml`, `custom11_window.xml`, `custom12_window.xml`, `custom13_window.xml`, `custom14_window.xml`, `custom15_window.xml`, `custom16_window.xml`, `custom17_window.xml`, `custom18_window.xml`, `custom19_window.xml`
- `compass.xml` -> `RCompassBGImages.xml`, `RCompassInnerFrameImages.xml`, `RCompassOuterFrameImages.xml`
- `context_window.xml` -> `context_base.xml`, `context_base_sub.xml`, `context_chat_main.xml`, `context_chat_main2.xml`, `context_chat_sub.xml`, `context_chat_sub2.xml`, `context_emoticon.xml`, `context_default.xml`, `context_font_size.xml`, `context_font_alpha.xml`, `context_window_alpha.xml`, `context_default_chat_channel.xml`
- `custom10_window.xml` -> `CommandBarBackground.xml`
- `custom12_window.xml` -> `ChantBackground.xml`
- `custom5_window.xml` -> `HHelperCubeWindow.xml`
- `custom6_window.xml` -> `HHelperHorizWindow.xml`
- `custom7_window.xml` -> `HHelperVertWindow.xml`
- `stats_index_window.xml` -> `StatusIndexBackground.xml`
- `styles.xml` -> `Styles/Button_Templates.xml`, `Styles/ChatControl_Templates.xml`, `Styles/CheckBox_Templates.xml`, `Styles/ComboBox_Templates.xml`, `Styles/CompassControl_Templates.xml`, `Styles/FullResizeImage_Templates.xml`, `Styles/HorizontalResizeButton_Templates.xml`, `Styles/HorizontalResizeImage_Templates.xml`, `Styles/Icon_Templates.xml`, `Styles/IconSet_Templates.xml`, `Styles/ImageArea_Templates.xml`, `Styles/ListBox_Templates.xml`, `Styles/ListBoxHeader_Templates.xml`, `Styles/Menu_Templates.xml`, `Styles/StatusBar_Templates.xml`, `Styles/StatusIcon_Templates.xml`, `Styles/Tab_Templates.xml`, `Styles/TextArea_Templates.xml`, `Styles/TreeControl_Templates.xml`, `Styles/VerticalResizeImage_Templates.xml`, `Styles/VerticalScrollBar_Templates.xml`, `Styles/VerticalStatusBar_Templates.xml`, `ToolTips.xml`, `TargetImages.xml`
- `summary.xml` -> `SummaryCombatImages1s.xml`
