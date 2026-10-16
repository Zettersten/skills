# Adapter reference

Adapters are the named live-data slots the client exposes to the UI. A control binds to one by name
(`<Adapter>`, `<AdapterName>`, `<ColorAdapter>`, `<TextAdapterName>`, `<BufferName>`, `<LabelAdapterName>`,
`<StateAdapterName>`). **Adapter names are case sensitive** (everything else in the XML is not).

Three sources are merged here:

- **official** = listed in the Trials of Atlantis XML UI document (types are authoritative).
- **stock** = bound by a control in the stock Atlantis skin of the live 1.130 client (`ui/atlantis`). Authoritative
  for what the current client exposes; files are shown with an `atlantis/` prefix.
- **observed** = bound by a control in a complete, working 1.127-era custom UI
  (CynicalJedi/DAOC-UI-Chooser). The type is inferred from the control that binds it, so treat it as a strong hint.

Numbered series are collapsed: `group_name{0-7}` means `group_name0` .. `group_name7`.
The bind column tells you which control types a working UI uses for it, which is the practical answer to
"what do I put this in?". Status bars and status icons need a scalar that ranges 0-100.

Totals: 388 official names, 820 observed names, 1000 distinct.

## Contents

- [RenameChatText](#renamechattext) (1)
- [alb](#alb) (1)
- [alliance](#alliance) (6)
- [bounty](#bounty) (1)
- [chat](#chat) (90)
- [combat](#combat) (1)
- [compass](#compass) (1)
- [conc](#conc) (1)
- [concentration](#concentration) (1)
- [craft](#craft) (1)
- [cur](#cur) (1)
- [font](#font) (1)
- [framerate](#framerate) (1)
- [friends](#friends) (1)
- [game](#game) (1)
- [group](#group) (267)
- [guild](#guild) (16)
- [help](#help) (1)
- [hib](#hib) (1)
- [hookpoint](#hookpoint) (2)
- [house](#house) (1)
- [index](#index) (26)
- [info](#info) (2)
- [interact](#interact) (2)
- [keep](#keep) (8)
- [key](#key) (1)
- [lag](#lag) (1)
- [lfg](#lfg) (3)
- [lfguild](#lfguild) (1)
- [map](#map) (3)
- [master](#master) (6)
- [max](#max) (1)
- [merchant](#merchant) (14)
- [mid](#mid) (1)
- [mini](#mini) (28)
- [mino](#mino) (1)
- [mount](#mount) (6)
- [new](#new) (50)
- [news](#news) (3)
- [none](#none) (1)
- [performance](#performance) (1)
- [quest](#quest) (1)
- [quiver](#quiver) (8)
- [realm](#realm) (88)
- [realmwar](#realmwar) (28)
- [release](#release) (2)
- [siege](#siege) (5)
- [siegetower](#siegetower) (1)
- [spec](#spec) (64)
- [stats](#stats) (52)
- [summary](#summary) (106)
- [system](#system) (65)
- [time](#time) (1)
- [timer](#timer) (2)
- [titles](#titles) (2)
- [train](#train) (6)
- [training](#training) (8)
- [value](#value) (2)
- [vault](#vault) (2)
- [window](#window) (1)

## RenameChatText

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `RenameChatText` | text | observed+stock | EditBoxDef | atlantis/chatrename.xml, chatrename.xml |

## alb

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `alb_low_pop_rp_bonus` | text | observed+official+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |

## alliance

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `alliance_member_count` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |
| `alliance_members` | list | observed+stock | ListBoxDef | atlantis/community_window.xml, community_window.xml |
| `alliance_members_current_page` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |
| `alliance_members_total_pages` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |
| `alliance_motd` | text (multi-line) | observed+stock | TextAreaDef | atlantis/community_window.xml, community_window.xml |
| `alliance_name` | text | observed+stock | LabelDef | atlantis/community_window.xml, community_window.xml |

## bounty

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `bounty_points` | scalar | observed+official+stock | ScalarLabelDef | atlantis/hookpoint_merchant_window.xml, custom17_window.xml, hookpoint_merchant_window.xml |

## chat

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `chat` | chat_buffer | observed+official+stock | ChatControlDef | atlantis/chat_window.xml, chat_window.xml |
| `chat_config_channel{0-15}` | text | official | - | - |
| `chat_config_current_output` | text | official | - | - |
| `chat_config_output_label` | text | official | - | - |
| `chat_config_title` | text | official | - | - |
| `chat_entry` | text | observed+official+stock | LabelDef | atlantis/chat_window.xml, chat_window.xml |
| `chat_tab{0-4}` | text | official | - | - |
| `chat{0-63}_color` | color | official | - | - |

## combat

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `combat_mode` | scalar 0-100 | observed | StatusIconDef | compass.xml, summary.xml |

## compass

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `compass_heading` | scalar | observed+official+stock | CompassControlDef, StatusIconDef | atlantis/compass.xml, compass.xml |

## conc

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `conc_list` | list | observed+official+stock | ListBoxDef | atlantis/concentration_window.xml, concentration_window.xml, custom12_window.xml |

## concentration

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `concentration` | scalar | observed+official+stock | StatusBarDef, ScalarLabelDef | atlantis/concentration_window.xml, concentration_window.xml |

## craft

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `craft_title` | text | observed+official | LabelDef | stats_spec_abil_window.xml |

## cur

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `cur_encumberance` | scalar | official | - | - |

## font

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `font_alpha_value` | text | observed+stock | LabelDef | atlantis/context_window.xml, context_font_alpha.xml |

## framerate

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `framerate_meter` | scalar | observed+official+stock | StatusIconDef | atlantis/menu_bar_window.xml, atlantis/performance_window.xml, menu_bar_window.xml ... |

## friends

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `friends_members` | list | observed+stock | ListBoxDef | atlantis/community_window.xml, community_window.xml |

## game

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `game_time` | text | observed | LabelDef | custom0_window.xml, interface_elements_window.xml |

## group

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `group_class{0-7}` | text | observed+official+stock | LabelDef | HHelperCubeWindow1.xml, HHelperHorizWindow1.xml, HHelperHorizWindow2.xml ... |
| `group_color{0-7}` | color | observed+official+stock | LabelDef, ScalarLabelDef | HHelperCubeWindow1.xml, HHelperHorizWindow1.xml, HHelperHorizWindow2.xml ... |
| `group_endurance{0-7}` | scalar / scalar 0-100 | observed+stock | ScalarLabelDef, StatusBarDef, StatusIconDef | HHelperCubeWindow1.xml, HHelperHorizWindow1.xml, HHelperHorizWindow2.xml ... |
| `group_health{0-7}` | scalar | observed+official+stock | StatusIconDef, ScalarLabelDef, StatusBarDef | HHelperCubeWindow1.xml, HHelperHorizWindow1.xml, HHelperHorizWindow2.xml ... |
| `group_level{0-7}` | scalar | observed+official+stock | ScalarLabelDef | atlantis/group_buffs.xml, atlantis/new_group_window.xml, atlantis/stats_group_window.xml ... |
| `group_mode` | scalar | official | - | - |
| `group_name{0-7}` | text | observed+official+stock | LabelDef | HHelperCubeWindow1.xml, HHelperHorizWindow1.xml, HHelperHorizWindow2.xml ... |
| `group_number` | scalar | official | - | - |
| `group_power{0-7}` | scalar | observed+official+stock | ScalarLabelDef, StatusBarDef, StatusIconDef | HHelperCubeWindow1.xml, HHelperHorizWindow1.xml, HHelperHorizWindow2.xml ... |
| `group_results` | list | observed+stock | ListBoxDef | atlantis/group_results_window.xml, group_results_window.xml |
| `group_status{0-7}` | scalar | official | - | - |
| `group_{0-7}icon{0-24}` | scalar | observed+official+stock | IconDef | atlantis/stats_group_window.xml, group_buffs.xml, stats_group_window.xml |

## guild

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `guild_banner_status` | text | observed+stock | LabelDef | atlantis/community_window.xml, community_window.xml |
| `guild_bounty_points` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml, hookpoint_merchant_window.xml |
| `guild_bp` | scalar | stock | ScalarLabelDef | atlantis/hookpoint_merchant_window.xml |
| `guild_dues` | text | observed+stock | LabelDef | atlantis/community_window.xml, community_window.xml |
| `guild_house_lot` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |
| `guild_level` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |
| `guild_member_count` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |
| `guild_members` | list | observed+stock | ListBoxDef | atlantis/community_window.xml, community_window.xml |
| `guild_members_current_page` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |
| `guild_members_total_pages` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |
| `guild_merit_points` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |
| `guild_money` | text | observed+stock | ButtonDef | atlantis/community_window.xml, community_window.xml |
| `guild_motd` | text (multi-line) | observed+stock | TextAreaDef | atlantis/community_window.xml, community_window.xml |
| `guild_name` | text | observed+official+stock | LabelDef | atlantis/community_window.xml, community_window.xml |
| `guild_rank` | text | official | - | - |
| `guild_realm_points` | scalar | observed+stock | ScalarLabelDef | atlantis/community_window.xml, community_window.xml |

## help

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `help_text` | text (multi-line) | observed+stock | TextAreaDef | atlantis/help_window.xml, help_window.xml |

## hib

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `hib_low_pop_rp_bonus` | text | observed+official+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |

## hookpoint

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `hookpoint_store_list` | list | observed+stock | ListBoxDef | atlantis/hookpoint_merchant_window.xml, hookpoint_merchant_window.xml |
| `hookpoint_store_title` | text | observed+stock | LabelDef | atlantis/hookpoint_merchant_window.xml, hookpoint_merchant_window.xml |

## house

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `house_lot` | scalar | official | - | - |

## index

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `index_color_{0-25}` | color | observed+stock | ButtonDef | atlantis/chat_config_window.xml, chat_config_window.xml |

## info

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `info_text` | text | observed+official+stock | TextAreaDef | atlantis/info_window.xml, info_window.xml |
| `info_title` | text | observed+official+stock | LabelDef | atlantis/info_window.xml, info_window.xml |

## interact

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `interact_text` | text | observed+official+stock | TextAreaDef | atlantis/interact_window.xml, interact_window.xml |
| `interact_title` | text | observed+official+stock | LabelDef | atlantis/interact_window.xml, interact_window.xml |

## keep

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `keep_status_claimed` | text | observed+stock | LabelDef | atlantis/keep_status_window.xml, keep_status_window.xml |
| `keep_status_level` | text | observed+stock | LabelDef | atlantis/keep_status_window.xml, keep_status_window.xml |
| `keep_status_target` | text | observed+stock | LabelDef | atlantis/keep_status_window.xml, keep_status_window.xml |
| `keep_status_title` | text | observed+stock | LabelDef | atlantis/keep_status_window.xml, keep_status_window.xml |
| `keep_status_type` | text | observed+stock | LabelDef | atlantis/keep_status_window.xml, keep_status_window.xml |
| `keep_upgrade_level` | scalar | observed+stock | ScalarLabelDef | atlantis/keep_upgrade_window.xml, keep_upgrade_window.xml |
| `keep_upgrade_target` | scalar | observed+stock | ScalarLabelDef | atlantis/keep_upgrade_window.xml, keep_upgrade_window.xml |
| `keep_upgrade_title` | text | observed+stock | LabelDef | atlantis/keep_upgrade_window.xml, keep_upgrade_window.xml |

## key

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `key_config` | list | observed+stock | ListBoxDef | atlantis/key_config.xml, key_config.xml |

## lag

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `lag_meter` | scalar | observed+official+stock | StatusIconDef | atlantis/menu_bar_window.xml, atlantis/performance_window.xml, menu_bar_window.xml ... |

## lfg

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `lfg_max_level` | scalar | observed+stock | ScalarLabelDef | atlantis/lfg_window.xml, lfg_window.xml |
| `lfg_min_level` | scalar | observed+stock | ScalarLabelDef | atlantis/lfg_window.xml, lfg_window.xml |
| `lfg_title` | text | observed+stock | LabelDef | atlantis/lfg_window.xml, lfg_window.xml |

## lfguild

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `lfguild_members` | list | observed+stock | ListBoxDef | atlantis/community_window.xml, community_window.xml |

## map

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `map_info` | text (multi-line) | observed+stock | TextAreaDef | atlantis/map_window.xml, map_window.xml |
| `map_info0` | text | observed+stock | LabelDef | atlantis/map_window.xml, map_window.xml |
| `map_title` | text | observed+stock | LabelDef | atlantis/map_window.xml, map_window.xml |

## master

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `master_exp` | scalar | observed+official+stock | StatusIconDef, ScalarLabelDef, VerticalStatusBarDef | atlantis/master_level_window.xml, custom11_window.xml |
| `master_list` | text | observed+official+stock | TextAreaDef | atlantis/master_level_window.xml, master_level_window.xml |
| `master_rank` | scalar | observed+official+stock | ScalarLabelDef | atlantis/master_level_window.xml, atlantis/new_summary_window.xml, master_level_window.xml ... |
| `master_rp` | scalar | official+stock | VerticalStatusBarDef | atlantis/master_level_window.xml |
| `master_title` | text | observed+official+stock | LabelDef | atlantis/master_level_window.xml, master_level_window.xml |
| `master_window_title` | text | observed+stock | LabelDef | atlantis/master_level_window.xml, master_level_window.xml |

## max

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `max_encumberance` | scalar | official | - | - |

## merchant

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `merchant_copper` | text | observed+official+stock | LabelDef | atlantis/hookpoint_merchant_window.xml, atlantis/menu_bar_window.xml, atlantis/merchant_window.xml ... |
| `merchant_gold` | text | observed+official+stock | LabelDef | atlantis/hookpoint_merchant_window.xml, atlantis/menu_bar_window.xml, atlantis/merchant_window.xml ... |
| `merchant_max_pages` | scalar | official | - | - |
| `merchant_mithril` | text | official+stock | LabelDef | atlantis/hookpoint_merchant_window.xml, atlantis/merchant_window.xml |
| `merchant_page_display` | text | observed+official+stock | LabelDef | atlantis/merchant_window.xml, merchant_window.xml |
| `merchant_page{0-4}` | list | observed+official+stock | ListBoxDef | atlantis/merchant_window.xml, merchant_window.xml |
| `merchant_platinum` | text | observed+official+stock | LabelDef | atlantis/hookpoint_merchant_window.xml, atlantis/menu_bar_window.xml, atlantis/merchant_window.xml ... |
| `merchant_quantity` | text | observed+official+stock | LabelDef | atlantis/merchant_window.xml, merchant_window.xml |
| `merchant_silver` | text | observed+official+stock | LabelDef | atlantis/hookpoint_merchant_window.xml, atlantis/menu_bar_window.xml, atlantis/merchant_window.xml ... |
| `merchant_title` | text | observed+official+stock | LabelDef | atlantis/merchant_window.xml, merchant_window.xml |

## mid

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `mid_low_pop_rp_bonus` | text | observed+official+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |

## mini

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `mini_craft_title` | text | observed+official+stock | LabelDef | atlantis/minicraft_window.xml, minicraft_window.xml |
| `mini_friends_text` | text | observed+official+stock | TextAreaDef | atlantis/minifriends_window.xml, minifriends_window.xml |
| `mini_info_icon` | scalar | official | - | - |
| `mini_info_string{0-7}` | text | observed+official+stock | LabelDef | atlantis/miniinfo_window.xml, miniinfo_window.xml |
| `mini_info_title_color` | scalar | official | - | - |
| `mini_info_use_list` | list | observed+stock | ListBoxDef | atlantis/miniinfo_window.xml, miniinfo_window.xml |
| `mini_pet_combat{0-2}` | scalar | observed+official+stock | CheckBoxDef | atlantis/minipet_window.xml, minipet_window.xml |
| `mini_pet_effect{0-5}` | scalar | observed+official+stock | IconDef | atlantis/minipet_window.xml, minipet_window.xml |
| `mini_pet_life` | scalar | observed+official+stock | StatusBarDef | atlantis/minipet_window.xml, minipet_window.xml |
| `mini_pet_movement{0-3}` | scalar | observed+official+stock | CheckBoxDef | atlantis/minipet_window.xml, minipet_window.xml |
| `mini_pet_title` | text | observed+official+stock | LabelDef | atlantis/minipet_window.xml, minipet_window.xml |

## mino

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `mino_relic_time_percent` | scalar 0-100 / scalar | observed+stock | StatusIconDef, ScalarLabelDef, StatusBarDef | atlantis/mino_relic_window.xml, mino_relic_window.xml |

## mount

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `mount_encumbrance` | text | observed+stock | LabelDef | atlantis/mount_window.xml, mount_window.xml |
| `mount_name` | text | observed+stock | LabelDef | atlantis/mount_window.xml, mount_window.xml |
| `mount_saddlebag_slot_{1-4}` | text | observed+stock | LabelDef | atlantis/mount_window.xml, mount_window.xml |

## new

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `new_quest_copper` | text | observed+stock | LabelDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_exp_coarse` | scalar 0-100 | observed+stock | StatusBarDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_exp_fine` | scalar 0-100 | observed+stock | StatusBarDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_gold` | text | observed+stock | LabelDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_journal_entries` | list (tree) | observed+stock | TreeControlDef | atlantis/new_quest_journal_window.xml, new_quest_journal_window.xml |
| `new_quest_opt_reward_count` | text | observed+stock | LabelDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_opt_reward_desc{0-7}` | text | observed+stock | IconDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_opt_reward_state{0-7}` | scalar | observed+official+stock | IconDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_opt_reward{0-7}` | scalar (icon id) | observed+stock | IconDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_platinum` | text | observed+stock | LabelDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_reward_desc{0-7}` | text | observed+stock | IconDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_reward{0-7}` | scalar (icon id) | observed+stock | IconDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_silver` | text | observed+stock | LabelDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_text` | text (multi-line) | observed+stock | TextAreaDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |
| `new_quest_title` | text | observed+stock | LabelDef | atlantis/new_quest_finish_window.xml, atlantis/new_quest_window.xml, new_quest_finish_window.xml ... |

## news

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `news_pve_text` | text (multi-line) | observed+stock | TextAreaDef | atlantis/community_window.xml, community_window.xml |
| `news_rvr_global_text` | text (multi-line) | observed+stock | TextAreaDef | atlantis/community_window.xml, community_window.xml |
| `news_rvr_local_text` | text (multi-line) | observed+stock | TextAreaDef | atlantis/community_window.xml, community_window.xml |

## none

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `none` | text / scalar 0/1 | observed+stock | LabelDef, CheckBoxDef | atlantis/chat_config_window.xml, atlantis/minifriends_window.xml, atlantis/minigroup_window.xml ... |

## performance

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `performance_meter` | scalar | observed+official+stock | StatusIconDef | atlantis/menu_bar_window.xml, atlantis/performance_window.xml, menu_bar_window.xml ... |

## quest

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `quest_text` | text | observed+official+stock | TextAreaDef | atlantis/quest_window.xml, quest_window_orig.xml |

## quiver

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `quiver_count_string{0-3}` | text | observed+stock | LabelDef, IconDef | atlantis/quiver_window.xml, quiver_window.xml |
| `quiver_icon{0-3}` | scalar (icon id) | observed+stock | IconDef | atlantis/quiver_window.xml, quiver_window.xml |

## realm

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `realm_bonus_color{2-13}` | color | observed+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |
| `realm_color` | color | observed+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |
| `realm_cost{0-13}` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `realm_df_color` | color | observed+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |
| `realm_df_text` | text | observed+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |
| `realm_exp_coarse` | scalar | observed+official+stock | StatusIconDef, ScalarLabelDef, StatusBarDef | atlantis/float_realm_exp_window.xml, custom11_window.xml, float_realm_exp_window.xml |
| `realm_exp_fine` | scalar | observed+official+stock | StatusIconDef, ScalarLabelDef, StatusBarDef | atlantis/float_realm_exp_window.xml, custom11_window.xml, float_realm_exp_window.xml |
| `realm_info_alb` | color | observed | LabelDef | realmwar_agramon.xml |
| `realm_keep_text` | text | observed+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |
| `realm_level` | scalar | observed+official+stock | ScalarLabelDef | atlantis/new_summary_window.xml, new_summary_window.xml |
| `realm_level_color{0-13}` | color | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `realm_level{0-13}` | scalar | observed+stock | HorizontalSliderDef, ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `realm_name{0-13}` | text | observed+stock | LabelDef | atlantis/training_window.xml, training_window.xml |
| `realm_power_color{0-2}` | color | observed+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |
| `realm_power_text` | text | observed+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |
| `realm_rank` | text | observed+official+stock | LabelDef, ScalarLabelDef | atlantis/float_realm_exp_window.xml, atlantis/new_summary_window.xml, custom17_window.xml ... |
| `realm_skillpoints` | scalar | official | - | - |
| `realm_slider` | scalar | observed+stock | VerticalSliderDef | atlantis/training_window.xml, training_window.xml |
| `realm_strength_color{0-2}` | color | observed+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |
| `realm_strength_text` | text | observed+stock | LabelDef | atlantis/realm_bonuses.xml, realm_bonuses.xml |
| `realm_title` | text | observed+official | LabelDef | custom17_window.xml |

## realmwar

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `realmwar_info_agramon` | color | observed+stock | LabelDef | atlantis/realmwar_agramon.xml, realmwar_agramon.xml |
| `realmwar_info_agramon{0-5}` | text | observed+stock | LabelDef | atlantis/realmwar_agramon.xml, realmwar_agramon.xml |
| `realmwar_info_alb` | color | observed+stock | LabelDef | atlantis/realmwar_alb.xml, realmwar_alb.xml |
| `realmwar_info_alb{0-5}` | text | observed+stock | LabelDef | atlantis/realmwar_alb.xml, realmwar_alb.xml |
| `realmwar_info_hib` | color | observed+stock | LabelDef | atlantis/realmwar_hib.xml, realmwar_hib.xml |
| `realmwar_info_hib{0-5}` | text | observed+stock | LabelDef | atlantis/realmwar_hib.xml, realmwar_hib.xml |
| `realmwar_info_mid` | color | observed+stock | LabelDef | atlantis/realmwar_mid.xml, realmwar_mid.xml |
| `realmwar_info_mid{0-5}` | text | observed+stock | LabelDef | atlantis/realmwar_mid.xml, realmwar_mid.xml |

## release

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `release_timer_text` | text | observed+stock | LabelDef | atlantis/release_window.xml, release_window.xml |
| `release_timer_time` | scalar 0-100 / scalar | observed+stock | StatusIconDef, ScalarLabelDef, StatusBarDef | atlantis/release_window.xml, release_window.xml |

## siege

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `siege_ammo` | list | observed+official+stock | ListBoxDef | atlantis/siege_window.xml, siege_window.xml |
| `siege_hits` | scalar / scalar 0-100 | observed+stock | StatusBarDef, ScalarLabelDef | atlantis/siege_window.xml, siege_window.xml |
| `siege_timer` | scalar / scalar 0-100 | observed+stock | StatusBarDef, ScalarLabelDef | atlantis/siege_window.xml, siege_window.xml |
| `siege_timer_label` | text | observed+stock | LabelDef | atlantis/siege_window.xml, siege_window.xml |
| `siege_title` | text | observed+official+stock | LabelDef | atlantis/siege_window.xml, siege_window.xml |

## siegetower

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `siegetower_status_title` | text | observed+stock | LabelDef | atlantis/siegetower_status_window.xml, siegetower_status_window.xml |

## spec

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `spec_icon_desc{0-19}` | text | observed+stock | IconDef | atlantis/training_window.xml, training_window.xml |
| `spec_icon{0-19}` | scalar (icon id) | observed+stock | IconDef | atlantis/training_window.xml, training_window.xml |
| `spec_level_color{0-7}` | color | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `spec_level{0-7}` | scalar | observed+stock | HorizontalSliderDef, ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `spec_name{0-7}` | text | observed+stock | LabelDef | atlantis/training_window.xml, training_window.xml |

## stats

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `stats_abil` | list | observed+stock | ListBoxDef | atlantis/stats_spec_abil_window.xml, stats_spec_abil_window.xml |
| `stats_additional_info` | list | observed+official+stock | ListBoxDef | atlantis/stats_attributes_window.xml, stats_attributes_window.xml |
| `stats_armor_factor` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_base_class` | text | official | - | - |
| `stats_body` | text | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_body_color` | color | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_charisma` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_charisma_color` | color | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_cold` | text | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_cold_color` | color | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_combat` | list (tree) | observed+stock | TreeControlDef | atlantis/stats_combat_window.xml, stats_combat_window.xml |
| `stats_constitution` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_constitution_color` | color | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_crush` | text | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_crush_color` | color | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_dexterity` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_dexterity_color` | color | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_empathy` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_empathy_color` | color | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_energy` | text | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_energy_color` | color | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_heat` | text | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_heat_color` | color | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_hitpoints` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_intelligence` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_intelligence_color` | color | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_level` | scalar | observed+official+stock | ScalarLabelDef | atlantis/float_level_exp_window.xml, atlantis/new_summary_window.xml, atlantis/stats_attributes_window.xml ... |
| `stats_matter` | text | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_matter_color` | color | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_name` | text | observed+official+stock | LabelDef | atlantis/stats_attributes_window.xml, stats_attributes_window.xml |
| `stats_piety` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_piety_color` | color | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_profession` | text | official | - | - |
| `stats_quickness` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_quickness_color` | color | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_race` | text | official | - | - |
| `stats_realm_points` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom17_window.xml, stats_attributes_window.xml |
| `stats_slash` | text | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_slash_color` | color | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_spec_points` | text | observed+stock | LabelDef | atlantis/stats_spec_abil_window.xml, stats_spec_abil_window.xml |
| `stats_specs` | list | observed+stock | ListBoxDef | atlantis/stats_spec_abil_window.xml, stats_spec_abil_window.xml |
| `stats_spells` | list (tree) | observed+stock | TreeControlDef | atlantis/stats_spells_window.xml, stats_spells_window.xml |
| `stats_spirit` | text | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_spirit_color` | color | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_strength` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_strength_color` | color | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_thrust` | text | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_thrust_color` | color | observed+stock | LabelDef | atlantis/stats_attributes_window.xml, custom9_window.xml, stats_attributes_window.xml |
| `stats_title` | text | official | - | - |
| `stats_trades` | list | observed+stock | ListBoxDef | atlantis/stats_spec_abil_window.xml, stats_spec_abil_window.xml |
| `stats_weapon_damage` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |
| `stats_weapon_skill` | scalar | observed+official+stock | ScalarLabelDef | atlantis/stats_attributes_window.xml, custom8_window.xml, stats_attributes_window.xml |

## summary

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `summary_amount{0-3}` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `summary_champ_exp_coarse` | scalar 0-100 / scalar | observed+stock | StatusIconDef, ScalarLabelDef, StatusBarDef | atlantis/float_champ_exp_window.xml, custom11_window.xml, float_champ_exp_window.xml |
| `summary_champ_exp_fine` | scalar 0-100 / scalar | observed+stock | StatusIconDef, ScalarLabelDef, StatusBarDef | atlantis/float_champ_exp_window.xml, custom11_window.xml, float_champ_exp_window.xml |
| `summary_champ_level` | scalar | observed+stock | ScalarLabelDef | atlantis/float_champ_exp_window.xml, atlantis/new_summary_window.xml, float_champ_exp_window.xml ... |
| `summary_exp_coarse` | scalar | observed+official+stock | StatusBarDef, StatusIconDef, ScalarLabelDef | atlantis/float_level_exp_window.xml, atlantis/menu_bar_window.xml, atlantis/summary.xml ... |
| `summary_exp_fine` | scalar | observed+official+stock | StatusBarDef, StatusIconDef, ScalarLabelDef | atlantis/float_level_exp_window.xml, atlantis/menu_bar_window.xml, atlantis/summary.xml ... |
| `summary_hit_label` | text | official | - | - |
| `summary_icon_desc{0-38}` | text | observed+stock | IconDef | atlantis/training_window.xml, training_window.xml |
| `summary_icon{0-38}` | scalar (icon id) | observed+stock | IconDef | atlantis/training_window.xml, training_window.xml |
| `summary_label{0-3}` | text | observed+stock | LabelDef | atlantis/training_window.xml, training_window.xml |
| `summary_level{0-3}` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `summary_page{0-3}` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `summary_player_end` | scalar | observed+official+stock | ScalarLabelDef, StatusBarDef, StatusIconDef | atlantis/new_summary_window.xml, atlantis/summary.xml, custom2_window.xml ... |
| `summary_player_hits` | scalar | observed+official+stock | ScalarLabelDef, StatusBarDef, StatusIconDef | atlantis/new_summary_window.xml, atlantis/summary.xml, custom1_window.xml ... |
| `summary_player_power` | scalar | observed+official+stock | ScalarLabelDef, StatusIconDef, StatusBarDef | HHelperCubeWindow1.xml, atlantis/new_summary_window.xml, atlantis/summary.xml ... |
| `summary_skill_amount{0-3}` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `summary_slider` | scalar | observed+stock | VerticalSliderDef | atlantis/training_window.xml, training_window.xml |
| `summary_target` | text | observed+official+stock | LabelDef | atlantis/float_target_window.xml, atlantis/new_summary_window.xml, atlantis/summary.xml ... |
| `summary_target_color` | color | observed+official+stock | LabelDef, ScalarLabelDef | atlantis/float_target_window.xml, atlantis/new_summary_window.xml, atlantis/summary.xml ... |
| `summary_target_hits` | scalar | observed+official+stock | ScalarLabelDef, StatusBarDef, StatusIconDef | atlantis/float_target_window.xml, atlantis/new_summary_window.xml, atlantis/summary.xml ... |
| `summary_title` | text | observed+official+stock | LabelDef | atlantis/new_summary_window.xml, atlantis/summary.xml, custom1_window.xml ... |

## system

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `system` | chat_buffer | official | - | - |
| `system{0-63}_color` | color | official | - | - |

## time

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `time_of_day` | scalar | observed+official+stock | LabelDef | atlantis/clock_window.xml, clock_window.xml, custom0_window.xml ... |

## timer

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `timer_text` | text | observed+official+stock | LabelDef | atlantis/timer_window.xml, timer_window.xml |
| `timer_time` | scalar 0-100 / scalar | observed+stock | StatusIconDef, ScalarLabelDef, StatusBarDef | atlantis/timer_window.xml, timer_window.xml |

## titles

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `titles_available_titles` | list | observed+stock | ListBoxDef | atlantis/title_window.xml, title_window.xml |
| `titles_stats` | text (multi-line) | observed+stock | TextAreaDef | atlantis/title_window.xml, title_window.xml |

## train

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `train_min_level` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `train_min_level_color` | color | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `train_realm` | list | observed+official+stock | ListBoxDef | atlantis/train.xml, train.xml |
| `train_realm_skill_points` | text | observed+official+stock | LabelDef | atlantis/train.xml, train.xml |
| `train_skill_points` | text | observed+official+stock | LabelDef | atlantis/train.xml, train.xml |
| `train_skills` | list | observed+official+stock | ListBoxDef | atlantis/train.xml, train.xml |

## training

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `training_realm_avail` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `training_realm_color` | color | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `training_realm_needed` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `training_realm_remaining` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `training_spec_avail` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `training_spec_color` | color | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `training_spec_needed` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |
| `training_spec_remaining` | scalar | observed+stock | ScalarLabelDef | atlantis/training_window.xml, training_window.xml |

## value

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `value_chooser_qty` | scalar | observed+stock | ScalarLabelDef | atlantis/value_chooser.xml, value_chooser.xml |
| `value_item_title` | text | observed+stock | LabelDef | atlantis/value_chooser.xml, value_chooser.xml |

## vault

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `vault_items` | list | observed+stock | ListBoxDef | atlantis/vault_window.xml, vault_window.xml |
| `vault_page` | text | observed+stock | LabelDef | atlantis/vault_window.xml, vault_window.xml |

## window

| adapter | type | source | bound by (observed) | seen in |
|---|---|---|---|---|
| `window_alpha_value` | text | observed+stock | LabelDef | atlantis/context_window.xml, context_window_alpha.xml |

## Notes from the official document

- `realm_rank`: listed twice in the doc, as text and as scalar; bind with a LabelDef or ScalarLabelDef accordingly
- `mini_info_title_color`: listed as scalar in the doc although the name suggests a color adapter
- `time_of_day`: the special time-of-day scalar; a LabelDef bound to it renders the clock text (observed in clock_window.xml)
- `chat`: special chat buffer used by ChatControlDef <BufferName>
- `system`: special chat buffer used by ChatControlDef <BufferName>
- `conc_list`: icon list adapter
- `merchant_page{0-4}`: icon list adapter
- `siege_ammo`: icon list adapter
- `train_skills`: two-column list adapter
- `train_realm`: two-column list adapter
- `stats_additional_info`: two-column list adapter
- `status bars`: StatusBarDef, VerticalStatusBarDef and StatusIconDef require a scalar adapter in the range 0-100
