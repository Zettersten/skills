# Stock template, font and texture names (Atlantis skin, client 1.130)

When a mod builds on the stock skin, these are the names it can reference without defining anything. They come
from the shipped `ui/atlantis` files (mostly `styles.xml` and `assets.xml`). Names are not case sensitive.
Templates defined inside a window file (e.g. `generic_editbox` in `bazaar_query.xml`) only exist while that
file is loaded, which it always is on stock, but a custom override of that file must re-define them.

Quick picks: status bars `red_status` / `green_status` / `blue_status` / `yellow_status` (plus `_small`/`_thick`
variants, `exp_bubbles`); window backgrounds `dlg_sm_title`, `dlg_sm_notitle`, `dlg_background_resize`,
`dlg_background_noresize`, insets `dlg_interior_small` / `dlg_interior_large`; buttons `button_small` (60x16),
`button_large`, `button_wide`, `button_narrow`, `button_nobg`, resizable `generic_hr_button`; fonts `arial9`,
`arial11`, `arial14`, `button_small`, `button_large`, `brit9`, `title`, `barb10`, TrueType `chat_small`,
`chat_large`, `minion`, `myriadbold`.

## Contents

- [Fonts and textures](#fonts-and-textures)
- [Templates by type](#templates-by-type)

## Fonts and textures

- **Canvas** (55, .bmp x55): `combat1_b`, `combat1_s`, `combat2_b`, `combat2_s`, `combat3_b`, `combat3_s`, `combat4_b`, `combat4_s`, `combat5_b`, `combat5_s`, `itm1_b`, `itm1_s`, `itm2_b`, `itm2_s`, `itm3_b`, `itm3_s`, `skill1_b`, `skill1_s`, `spl10_b`, `spl10_s`, `spl11_b`, `spl11_s`, `spl12_b`, `spl12_s`, `spl13_b`, `spl13_s`, `spl14_b`, `spl14_s`, `spl15_b`, `spl15_s`, `spl1_b`, `spl1_s`, `spl2_b`, `spl2_s`, `spl3_b`, `spl3_s`, `spl4_b`, `spl4_s`, `spl5_b`, `spl5_s`, `spl6_b`, `spl6_s`, `spl7_b`, `spl7_s`, `spl8_b`, `spl8_s`, `spl9_b`, `spl9_s`, `wpns1_b`, `wpns1_s`, `wpns2_b`, `wpns2_s`, `wpns3_b`, `wpns3_s`
- **Font** (9, .tga x9): `arial11`, `arial14`, `arial9`, `barb10`, `brit9`, `brit9s`, `button_large`, `button_small`, `title`
- **TTFFont** (4, .ttf x4): `chat_large`, `chat_small`, `minion`, `myriadbold`
- **Texture** (20, .tga x16, .dds x3, .bmp x1): `compass`, `emoticons`, `frames_win`, `map_icons`, `navigation`, `no_map`, `page1`, `page2`, `page3`, `page4`, `page4b`, `realm_symbols`, `selected_icon`, `slider`, `small_arrows`, `warmap_agramon`, `warmap_alb`, `warmap_hib`, `warmap_mid`

Icon sheets are `<Canvas>` assets named `<sheet>_b` (32px) and `<sheet>_s` (16px): `spl1..`, `itm1..`,
`combat1..`, `skill1`. Font files live in `ui/fonts/`; texture sheets `page1..page4b` are the Atlantis frame art.

## Templates by type

### ButtonTemplate (33)

`button_bag`, `button_barb10`, `button_checkbox`, `button_down`, `button_large`, `button_large_new`, `button_large_tab`, `button_left`, `button_money`, `button_narrow`, `button_nobg`, `button_right`, `button_small`, `button_tab`, `button_up`, `button_wide`, `button_wide_barb10`, `chat_scale`, `chat_vscroll_down`, `chat_vscroll_up`, `color_button`, `color_highlight_button`, `combo_label`, `resize_bottom_left`, `resize_bottom_right`, `resize_top_right`, `scroll_down`, `scroll_down_no_gutter`, `scroll_up`, `scroll_up_no_gutter`, `window_close`, `window_minimize`, `window_move`

### ChatControlTemplate (1)

`chat`

### CheckBoxTemplate (15)

`abilities_tab`, `chat_config_check`, `chat_config_checkbox`, `chat_tab`, `generic_check`, `group_tab`, `inventory_tab`, `narrow_font_check`, `realmwar_tab`, `simple_check`, `small_font_check`, `spells_tab`, `stats_tab`, `styles_tab`, `tree_check`

### ComboBoxTemplate (3)

`combobox_thin`, `generic_combobox`, `generic_combobox_scroll`

### CompassControlTemplate (1)

`compass`

### EditBoxTemplate (1)

`generic_editbox`

### FullResizeImageTemplate (17)

`chat_entry`, `chat_int`, `dlg_background_noresize`, `dlg_background_resize`, `dlg_interior_large`, `dlg_interior_small`, `dlg_lg_notitle_noresize`, `dlg_lg_title_noresize`, `dlg_sm_notitle`, `dlg_sm_title`, `dlg_sm_title_noresize`, `inner_frame`, `listbox_header_background`, `menu_background_noresize`, `normal_bg`, `selection_box`, `tool_tip_background`

### HorizontalResizeButtonTemplate (12)

`context_hr_button`, `context_hr_button_wtext`, `context_hr_button_wtext_barb10`, `generic_hr_button`, `generic_hr_button_arial9`, `generic_hr_button_barb10`, `generic_hr_button_small`, `generic_hr_button_title`, `hr_button`, `listbox_hrbutton`, `simple_hr_button`, `tab_button`

### HorizontalResizeImageTemplate (34)

`Hslider`, `blue_back`, `blue_full`, `context_hr_image_divider`, `context_hr_image_highlit`, `dialog_inset`, `exp_high`, `exp_low`, `generic_hr_image_disabled`, `generic_hr_image_normal`, `generic_hr_image_normalhighlight`, `generic_hr_image_pressed`, `green_back`, `green_back_small`, `green_full`, `green_full_small`, `hr_image_highlit`, `hr_image_normal`, `hr_image_pressed`, `listbox_header`, `listbox_row_bg`, `listbox_selected_bg`, `paperdoll_back`, `red_back`, `red_back_thick`, `red_full`, `red_full_thick`, `simple_hr_image_highlit`, `tab_button_highlit`, `tab_button_normal`, `yellow_back`, `yellow_back_small`, `yellow_full`, `yellow_full_small`

### HorizontalSliderTemplate (1)

`generic_horizontal_slider`

### IconSetTemplate (1)

`group_buffs_iconset`

### IconTemplate (2)

`plain_icon_large`, `plain_icon_small`

### ImageAreaTemplate (140)

`Hslider_indicator`, `Vslider_indicator`, `alb_symbol`, `angry`, `arrow`, `bang`, `battle_symbol`, `beckon`, `beg`, `blush`, `bottom_endcap`, `bow`, `brandish`, `bridge_symbol`, `channel_button`, `charge`, `check_mark`, `cheer`, `clap`, `confuse`, `copper_decal`, `courbette`, `cower`, `cry`, `curtsey`, `dance`, `destination_symbol`, `diabolical`, `dismiss`, `dock_symbol`, `doh`, `drink`, `dungeon_symbol`, `emote_button`, `endcap_thick_left`, `endcap_thick_right`, `flex`, `gold_decal`, `graze`, `green1_back_stat`, `green2_back_stat`, `group_location`, `halt`, `hib_symbol`, `horse_nod`, `horse_rear`, `howl`, `hug`, `icon_socket_large`, `icon_socket_large_active`, `icon_socket_small`, `icon_socket_small_active`, `impasse_symbol`, `induct`, `keep_symbol`, `kiss`, `knock`, `laugh`, `loco`, `lookfar`, `master_title`, `mememe`, `mgclosed_symbol`, `mgopen_symbol`, `mid_symbol`, `military_salute`, `mino_relic_1`, `mino_relic_2`, `mino_relic_3`, `mithril_decal`, `monty`, `no`, `pet`, `platinum_decal`, `player_location`, `point`, `ponder`, `present`, `quest_completer`, `quest_giver`, `quest_title`, `quest_title_left`, `quest_title_right`, `quest_waypoint`, `raise`, `realmwar_destination`, `realmwar_selection`, `realmwar_siege`, `red_back_left`, `red_back_right`, `red_back_stat`, `relic_symbol`, `reward_frame_template`, `rofl`, `rude`, `salute`, `selection_symbol`, `shiver`, `shrug`, `siege_symbol`, `silver_decal`, `slap`, `slit`, `sm_horiz_endcap_left`, `sm_horiz_endcap_left_thin`, `sm_horiz_endcap_right`, `sm_horiz_endcap_right_thin`, `smile`, `stagger`, `startle`, `startled`, `stats_index_background`, `stench`, `surrender`, `sweat`, `talk`, `taunt`, `tiny_horiz_endcap_left`, `tiny_horiz_endcap_right`, `top_endcap`, `tower_symbol`, `tricks`, `victory`, `warmap_agramon`, `warmap_breifine`, `warmap_collory`, `warmap_cruachon`, `warmap_emain`, `warmap_hadrians`, `warmap_jamtland`, `warmap_odins`, `warmap_pennine`, `warmap_sauvage`, `warmap_snowdonia`, `warmap_uppland`, `warmap_yggdra`, `wave`, `worship`, `yawn`, `yes`

### ListBoxHeaderTemplate (8)

`listboxheader_banner`, `listboxheader_class`, `listboxheader_group`, `listboxheader_level`, `listboxheader_name`, `listboxheader_note`, `listboxheader_rank`, `listboxheader_zone`

### ListBoxTemplate (20)

`keyconfig_listbox`, `listbox_alliance`, `listbox_bg`, `listbox_bg_icons`, `listbox_bg_nw_font`, `listbox_bg_nw_white_font`, `listbox_bg_sm_bright`, `listbox_bg_sm_font`, `listbox_combat_bg`, `listbox_friends_lfguild`, `listbox_gr`, `listbox_green_bg`, `listbox_guild`, `listbox_nobg`, `listbox_nobg_nw_font`, `listbox_nobg_nw_white_font`, `listbox_nobg_sm_bright`, `listbox_nobg_sm_grey`, `listbox_skill_bg`, `listbox_small_bg`

### MenuTemplate (3)

`generic_menu`, `generic_menu_scroll`, `menu_thin`

### StatusBarTemplate (8)

`blue_status`, `exp_bubbles`, `green_status`, `green_status_small`, `red_status`, `red_status_thick`, `yellow_status`, `yellow_status_small`

### StatusIconTemplate (17)

`framerate_icon_large`, `lag_icon_large`, `mini_group_endurance`, `mini_group_power`, `performance_icon_large`, `performance_icon_small`, `realmwar_battle_large`, `realmwar_battle_medium`, `realmwar_battle_small`, `realmwar_keep`, `realmwar_milegate`, `realmwar_ruined_keep`, `realmwar_ruined_tower`, `realmwar_scouting_large`, `realmwar_scouting_medium`, `realmwar_scouting_small`, `realmwar_tower`

### TabsTemplate (2)

`generic_tabs`, `large_tabs`

### TextAreaTemplate (6)

`generic_textarea`, `generic_textarea_nobg`, `generic_textarea_sm`, `generic_textarea_sm_nobg`, `map_textarea`, `nobg_textarea`

### TreeControlTemplate (4)

`combat_tree_control`, `generic_tree_control`, `quest_tree_control`, `spell_tree_control`

### VerticalResizeImageTemplate (13)

`Vslider`, `bag_bg`, `blue_back`, `blue_full`, `chat_vscroll_gutter`, `chat_vscroll_thumb`, `red_back`, `red_full`, `scroll_gutter`, `scroll_gutter_no_gutter`, `scroll_thumb`, `scroll_thumb_no_gutter`, `vault_blank`

### VerticalScrollbarTemplate (3)

`chat_vscroll`, `generic_vscroll`, `vscroll_no_gutter`

### VerticalSliderTemplate (1)

`generic_vertical_slider`

### VerticalStatusBarTemplate (2)

`vstatus_blue`, `vstatus_red`
