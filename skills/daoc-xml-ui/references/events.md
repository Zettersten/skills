# Event reference

Events are what buttons fire: `<OnClickEvent>Name</OnClickEvent>` on a `ButtonDef`, `InvisibleButtonDef`,
`HorizontalResizeButtonDef`, `HorizontalResizeImageButtonDef`, `CheckBoxDef`, `IconDef`, slider or `ListBoxDef`
(`OnClickEvent`, `OnHeaderClickEvent`), and `ComboBoxDef` (`OnChangeEvent`). Event names are not case sensitive.

The XML cannot define new behaviour: an event only works if the client implements it. Some events need
state the window owns (a selected list row, a chosen pet mode) and only make sense inside that window.

- **official** = in the Trials of Atlantis document, with its description.
- **observed** = wired to a control in the stock Atlantis skin of the live 1.130 client (files prefixed `atlantis/`)
  or in a complete, working 1.127-era custom UI (CynicalJedi/DAOC-UI-Chooser).
  No official description exists; the name and the window it is used in are the documentation.

Totals: 66 official, 257 observed, 282 distinct.

## Contents

- [Window toggles (observed)](#window-toggles-observed)
- [Custom windows](#custom-windows)
- [Command Window (official)](#command-window-official)
- [Interact Window (official)](#interact-window-official)
- [Group and Mini-Group Window (official)](#group-and-mini-group-window-official)
- [Mini-Craft Window (official)](#mini-craft-window-official)
- [Concentration Window (official)](#concentration-window-official)
- [Train Window (official)](#train-window-official)
- [Merchant Window (official)](#merchant-window-official)
- [Chat Window (official)](#chat-window-official)
- [Siege Window (official)](#siege-window-official)
- [Pet Window (official)](#pet-window-official)
- [Random (official)](#random-official)
- [Other observed events](#other-observed-events)

## Window toggles (observed)

`Toggle*` events open/close a specific window. Put one on a button anywhere (command window, your own
menu window) to get a launcher. Names are what the client ships; the table shows where a working UI wires them.

| event | fired from |
|---|---|
| `ToggleCasualGroupFinder` | atlantis/stats_group_window.xml, stats_group_window.xml |
| `ToggleClock` | atlantis/command_window.xml, atlantis/interface_elements_window.xml, command_window.xml |
| `ToggleCommandWindow` | atlantis/interface_elements_window.xml, custom0_window.xml, interface_elements_window.xml |
| `ToggleCompassWindow` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleConcentration` | atlantis/interface_elements_window.xml, atlantis/stats_spells_window.xml, command_window.xml |
| `ToggleFloatChampXP` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleFloatLevelXP` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleFloatRealmXP` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleFloatTarget` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleGroupBuffs` | atlantis/interface_elements_window.xml, command_window.xml, custom0_window.xml |
| `ToggleGroupOptions` | atlantis/stats_group_window.xml, stats_group_window.xml |
| `ToggleHelp` | atlantis/main_menu_window.xml, command_window.xml, custom0_window.xml |
| `ToggleInterfaceElements` | atlantis/main_menu_window.xml, interface_elements_window.xml, main_menu_window.xml |
| `ToggleJournal` | atlantis/interface_elements_window.xml, atlantis/menu_bar_window.xml, command_window.xml |
| `ToggleMainMenu` | atlantis/menu_bar_window.xml, menu_bar_window.xml |
| `ToggleMap` | atlantis/command_window.xml, atlantis/interface_elements_window.xml, atlantis/menu_bar_window.xml |
| `ToggleMasterLevel` | atlantis/interface_elements_window.xml, command_window.xml, custom0_window.xml |
| `ToggleMenuBar` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleMiniFriends` | atlantis/interface_elements_window.xml, custom0_window.xml, interface_elements_window.xml |
| `ToggleMiniGroup` | atlantis/interface_elements_window.xml, command_window.xml, custom0_window.xml |
| `ToggleMiniPet` | atlantis/interface_elements_window.xml, atlantis/stats_spells_window.xml, command_window.xml |
| `ToggleMount` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleNewGroup` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleNewSummary` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleOptions` | atlantis/main_menu_window.xml, command_window.xml, custom0_window.xml |
| `TogglePerformanceMeter` | atlantis/interface_elements_window.xml, command_window.xml, custom0_window.xml |
| `ToggleQuiver` | atlantis/interface_elements_window.xml, atlantis/stats_combat_window.xml, command_window.xml |
| `ToggleStatsAttributes` | atlantis/menu_bar_window.xml, menu_bar_window.xml |
| `ToggleStatsGroup` | atlantis/menu_bar_window.xml, menu_bar_window.xml |
| `ToggleStatsInventory` | atlantis/menu_bar_window.xml, menu_bar_window.xml |
| `ToggleStatsSkills` | atlantis/menu_bar_window.xml, menu_bar_window.xml |
| `ToggleStatsSpells` | atlantis/menu_bar_window.xml, menu_bar_window.xml |
| `ToggleStatsStyles` | atlantis/menu_bar_window.xml, menu_bar_window.xml |
| `ToggleSummary` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleTitle` | atlantis/interface_elements_window.xml, interface_elements_window.xml |
| `ToggleWarmapKey` | atlantis/realmwar_agramon.xml, atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml |

## Custom windows

`ToggleCustom0` .. `ToggleCustom19` open the user window templates named `custom0_window` .. `custom19_window`
(by convention in `custom0_window.xml` .. `custom19_window.xml`, `<Include>`d from `assets.xml`).
This is the only mechanism for adding a brand-new window; see SKILL.md recipe "add a custom window".

## Command Window (official)

| event | what it does | also observed |
|---|---|---|
| `ToggleAttackMode` | Toggles player attack mode | yes |
| `Realm` | Shows the /realm display | yes |
| `Sprint` | Toggles sprint mode | yes |
| `ToggleSitting` | Toggles sitting mode | yes |
| `Task` | Toggles task display | yes |
| `Follow` | Toggles auto-follow mode | yes |
| `Stick` | Toggles auto-stick mode | yes |
| `Afk` | Toggles AFK mode | yes |
| `Face` | Toggles auto-face mode | yes |
| `Anon` | Toggles anon mode | yes |
| `Pray` | Issues the /pray command | yes |
| `Help` | Shows the Help Window | yes |
| `Release` | Issues the /release command | yes |
| `Relic` | Shows the /relic display | yes |
| `Bonuses` | Shows the /bonus display (resists) | yes |
| `ShowKeyboardConfig` | Shows the keyboard configuration display | yes |
| `Journal` | Shows the Quest Journal Window | yes |
| `Friends` | Shows the Mini-Friends Window | yes |
| `Bind` | Issues the /bind command | yes |
| `ToggleCompass` | Toggles compass mode between off, small, and large | yes |
| `Quit` | Issues the /quit command | yes |

## Interact Window (official)

| event | what it does | also observed |
|---|---|---|
| `Interact` | Issues an interact event for the clicked hotspot; requires extra data | - |

## Group and Mini-Group Window (official)

| event | what it does | also observed |
|---|---|---|
| `SelectGroupMember{0-7}` | Selects group member N (0 = leader) | yes |
| `GroupQuerySolo` | Sends a looking-for-group query as a solo player | - |
| `GroupQueryGroup` | Sends a looking-for-group query as a group leader | - |
| `GroupSoloSeeking` | Sets a solo player's looking-for-group flag | - |
| `GroupSoloNotSeeking` | Removes a solo player's looking-for-group flag | - |
| `GroupSeekingNone` | Sets a group's seeking-members flag to none | - |
| `GroupSeekingAll` | Sets a group's seeking-members flag to all | - |
| `GroupSeekingFighter` | Sets seeking flag to fighter | - |
| `GroupSeekingMage` | Sets seeking flag to mage | - |
| `GroupSeekingHealer` | Sets seeking flag to healer | - |
| `GroupSeekingRogue` | Sets seeking flag to rogue | - |
| `GroupInvite` | Issues the /invite command | yes |
| `GroupDisband` | Issues the /disband command | yes |

## Mini-Craft Window (official)

| event | what it does | also observed |
|---|---|---|
| `Repair` | Issues the /repair command | yes |
| `Craft` | Issues the /craft command | yes |
| `Salvage` | Issues the /salvage command | yes |

## Concentration Window (official)

| event | what it does | also observed |
|---|---|---|
| `RemoveConc` | Removes the selected concentration buff (needs the window's selection) | - |
| `ConcQuickDesc` | Shows the Mini-Info Window for the selected concentration buff | - |

## Train Window (official)

| event | what it does | also observed |
|---|---|---|
| `Train` | Trains the selected skill or realm ability (needs the window's selection) | yes |
| `TrainInfo` | Gets info on the selected skill or realm ability | yes |

## Merchant Window (official)

| event | what it does | also observed |
|---|---|---|
| `MerchantBuy` | Buys the selected item (needs the window's selection) | - |
| `MerchantSell` | Sells the selected inventory object | - |
| `MerchantAppraise` | Appraises the selected inventory object | - |
| `MerchantQuickDesc` | Shows the Mini-Info Window for the selected merchant item | - |

## Chat Window (official)

| event | what it does | also observed |
|---|---|---|
| `ChatChannelsChanged` | Tells the server to filter chat channels | - |

## Siege Window (official)

| event | what it does | also observed |
|---|---|---|
| `SiegeArm` | Issues a siege arm command | - |
| `SiegeLoad` | Issues a siege load command using the selected (or first) ammo | - |
| `SiegeAim` | Issues a siege aim command | yes |
| `SiegeFire` | Issues a siege fire command | yes |

## Pet Window (official)

| event | what it does | also observed |
|---|---|---|
| `PetSetMoveState` | Sets pet move state to the current state (needs the window's state) | - |
| `PetSetCombatState` | Sets pet combat state to the current state (needs the window's state) | - |
| `PetAttack` | Pet attack command | yes |
| `PetRelease` | Release pet command | yes |
| `PetTarget` | Target pet command | yes |

## Random (official)

| event | what it does | also observed |
|---|---|---|
| `ShowWindow` | Shows a window (extra data needed) | - |
| `HideWindow` | Hides a window (extra data needed) | - |
| `ToggleWindow` | Toggles a window (extra data needed) | - |

## Other observed events

Grouped by prefix. `fired from` lists up to three files from the reference UI.

### Assist

| event | fired from |
|---|---|
| `AssistTarget` | atlantis/float_target_window.xml, atlantis/stats_group_window.xml, float_target_window.xml |

### Chat

| event | fired from |
|---|---|
| `ChatRenameCancel` | atlantis/chatrename.xml, chatrename.xml |
| `ChatRenameOK` | atlantis/chatrename.xml, chatrename.xml |

### Com

| event | fired from |
|---|---|
| `ComAllianceMemberSelected` | atlantis/community_window.xml, community_window.xml |
| `ComAllianceMembersNext` | atlantis/community_window.xml, community_window.xml |
| `ComAllianceMembersPrev` | atlantis/community_window.xml, community_window.xml |
| `ComAllianceMembersShowOffline` | atlantis/community_window.xml, community_window.xml |
| `ComAllianceMembersSort` | atlantis/community_window.xml, community_window.xml |
| `ComAllianceSend` | atlantis/community_window.xml, community_window.xml |
| `ComFriendsMemberSelected` | atlantis/community_window.xml, community_window.xml |
| `ComFriendsMembersSort` | atlantis/community_window.xml, community_window.xml |
| `ComFriendsSend` | atlantis/community_window.xml, community_window.xml |
| `ComGuildBannerDeploy` | atlantis/community_window.xml, community_window.xml |
| `ComGuildCommands` | atlantis/community_window.xml, community_window.xml |
| `ComGuildDemote` | atlantis/community_window.xml, community_window.xml |
| `ComGuildMemberSelected` | atlantis/community_window.xml, community_window.xml |
| `ComGuildMembersNext` | atlantis/community_window.xml, community_window.xml |
| `ComGuildMembersPrev` | atlantis/community_window.xml, community_window.xml |
| `ComGuildMembersShowOffline` | atlantis/community_window.xml, community_window.xml |
| `ComGuildMembersSort` | atlantis/community_window.xml, community_window.xml |
| `ComGuildNote` | atlantis/community_window.xml, community_window.xml |
| `ComGuildPromote` | atlantis/community_window.xml, community_window.xml |
| `ComGuildSend` | atlantis/community_window.xml, community_window.xml |
| `ComGuildWithdraw` | atlantis/community_window.xml, community_window.xml |
| `ComLFGuildInvite` | atlantis/community_window.xml, community_window.xml |
| `ComLFGuildMemberSelected` | atlantis/community_window.xml, community_window.xml |
| `ComLFGuildMembersSort` | atlantis/community_window.xml, community_window.xml |
| `ComLFGuildSend` | atlantis/community_window.xml, community_window.xml |
| `ComTabChanged` | atlantis/community_window.xml, community_window.xml, custom13_window.xml |
| `ComTabRefresh` | atlantis/community_window.xml, community_window.xml |

### Community

| event | fired from |
|---|---|
| `Community` | atlantis/interface_elements_window.xml, atlantis/stats_attributes_window.xml, command_window.xml |

### Context

| event | fired from |
|---|---|
| `ContextOnAddChatWindow` | atlantis/context_window.xml, context_chat_main.xml, context_chat_sub.xml |
| `ContextOnDefaultChannel` | atlantis/context_window.xml, context_chat_main.xml, context_chat_main2.xml |
| `ContextOnDeleteChatWindow` | atlantis/context_window.xml, context_chat_sub.xml, context_chat_sub2.xml |
| `ContextOnFontAlpha` | atlantis/context_window.xml, context_chat_main.xml, context_chat_main2.xml |
| `ContextOnFontSize` | atlantis/context_window.xml |
| `ContextOnMessageAndChannel` | atlantis/context_window.xml, context_chat_main.xml, context_chat_main2.xml |
| `ContextOnRenameChatWindow` | atlantis/context_window.xml, context_chat_sub.xml, context_chat_sub2.xml |
| `ContextOnWindowAlpha` | atlantis/context_window.xml, context_chat_main.xml, context_chat_main2.xml |
| `ContextSetDefaultChannel` | atlantis/context_window.xml, context_default_chat_channel.xml |
| `ContextSetFontAlpha` | atlantis/context_window.xml, context_font_alpha.xml |
| `ContextSetFontSize` | atlantis/context_window.xml, context_font_size.xml |
| `ContextSetWindowAlpha` | atlantis/context_window.xml, context_window_alpha.xml |

### Delve

| event | fired from |
|---|---|
| `Delve` | atlantis/miniinfo_window.xml, miniinfo_window.xml |

### Group

| event | fired from |
|---|---|
| `GroupFind` | atlantis/stats_group_window.xml, stats_group_window.xml |

### Hookpoint

| event | fired from |
|---|---|
| `HookpointStoreBP` | atlantis/hookpoint_merchant_window.xml, hookpoint_merchant_window.xml |
| `HookpointStoreBuy` | atlantis/hookpoint_merchant_window.xml, hookpoint_merchant_window.xml |
| `HookpointStoreCoin` | atlantis/hookpoint_merchant_window.xml, hookpoint_merchant_window.xml |
| `HookpointStoreContract` | atlantis/hookpoint_merchant_window.xml, hookpoint_merchant_window.xml |
| `HookpointStoreGBP` | atlantis/hookpoint_merchant_window.xml, hookpoint_merchant_window.xml |

### In

| event | fired from |
|---|---|
| `InGameKeyConfigAccept` | atlantis/key_config.xml, key_config.xml |
| `InGameKeyConfigCancel` | atlantis/key_config.xml, key_config.xml |
| `InGameKeyConfigClearKey` | atlantis/key_config.xml, key_config.xml |
| `InGameKeyConfigResetFPS` | atlantis/key_config.xml, key_config.xml |
| `InGameKeyConfigResetMMO` | atlantis/key_config.xml, key_config.xml |
| `InGameKeyConfigResetRPG` | atlantis/key_config.xml, key_config.xml |

### Keep

| event | fired from |
|---|---|
| `KeepStatusHookpoints` | atlantis/keep_status_window.xml, keep_status_window.xml |
| `KeepStatusRepair` | atlantis/keep_status_window.xml, atlantis/siegetower_status_window.xml, keep_status_window.xml |
| `KeepUpgradeCancel` | atlantis/keep_upgrade_window.xml, keep_upgrade_window.xml |
| `KeepUpgradeRelease` | atlantis/keep_upgrade_window.xml, keep_upgrade_window.xml |

### Master

| event | fired from |
|---|---|
| `MasterLevelPageNext` | atlantis/master_level_window.xml, master_level_window.xml |
| `MasterLevelPagePrevious` | atlantis/master_level_window.xml, master_level_window.xml |

### Menu

| event | fired from |
|---|---|
| `MenuBarToggleExp` | atlantis/menu_bar_window.xml, menu_bar_window.xml |

### Mino

| event | fired from |
|---|---|
| `MinoRelicDrop` | atlantis/mino_relic_window.xml, mino_relic_window.xml |

### Mount

| event | fired from |
|---|---|
| `Mount` | atlantis/stats_attributes_window.xml, stats_attributes_window.xml |

### New

| event | fired from |
|---|---|
| `NewQuestAccept` | atlantis/new_quest_window.xml, new_quest_window.xml |
| `NewQuestContinue` | atlantis/new_quest_finish_window.xml, new_quest_finish_window.xml |
| `NewQuestDecline` | atlantis/new_quest_window.xml, new_quest_window.xml |
| `NewQuestFinish` | atlantis/new_quest_finish_window.xml, new_quest_finish_window.xml |
| `NewQuestSelectOptReward{0-7}` | atlantis/new_quest_finish_window.xml, new_quest_finish_window.xml |
| `NewTrain` | atlantis/training_window.xml, training_window.xml |
| `NewTrainInfo` | atlantis/training_window.xml, training_window.xml |
| `NewTrainRealmInfo` | atlantis/training_window.xml, training_window.xml |

### Quick

| event | fired from |
|---|---|
| `QuickBind` | atlantis/key_config.xml, key_config.xml |

### Quiver

| event | fired from |
|---|---|
| `QuiverAdd{0-3}` | atlantis/quiver_window.xml, quiver_window.xml |
| `QuiverSelect{0-3}` | atlantis/quiver_window.xml, quiver_window.xml |

### Release

| event | fired from |
|---|---|
| `ReleaseToBind` | atlantis/release_window.xml, release_window.xml |
| `ReleaseToCity` | atlantis/release_window.xml, release_window.xml |
| `ReleaseToHouse` | atlantis/release_window.xml, release_window.xml |

### Remove

| event | fired from |
|---|---|
| `RemoveQuest` | atlantis/new_quest_journal_window.xml, atlantis/quest_window.xml, new_quest_journal_window.xml |

### Respec

| event | fired from |
|---|---|
| `RespecAll` | atlantis/training_window.xml, training_window.xml |
| `RespecBuy` | atlantis/training_window.xml, training_window.xml |
| `RespecRealm` | atlantis/training_window.xml, training_window.xml |

### Show

| event | fired from |
|---|---|
| `ShowWarMap` | atlantis/menu_bar_window.xml, command_window.xml, custom0_window.xml |
| `ShowWarmap` | atlantis/interface_elements_window.xml, atlantis/stats_group_window.xml, interface_elements_window.xml |

### Siege

| event | fired from |
|---|---|
| `SiegeMove` | atlantis/siege_window.xml, siege_window.xml |
| `SiegeRelease` | atlantis/siege_window.xml, siege_window.xml |
| `SiegeRepair` | atlantis/siege_window.xml, siege_window.xml |
| `SiegeSalvage` | atlantis/siege_window.xml, siege_window.xml |

### Subclass

| event | fired from |
|---|---|
| `SubclassDelve` | atlantis/daoc_subclass_window.xml, daoc_subclass_window.xml |

### Summary

| event | fired from |
|---|---|
| `SummaryToggleExp` | atlantis/summary.xml |

### Value

| event | fired from |
|---|---|
| `ValueChooserAccept` | atlantis/value_chooser.xml, value_chooser.xml |
| `ValueChooserCancel` | atlantis/value_chooser.xml, value_chooser.xml |
| `ValueChooserDecrease` | atlantis/value_chooser.xml, value_chooser.xml |
| `ValueChooserIncrease` | atlantis/value_chooser.xml, value_chooser.xml |
| `ValueChooserShiftDecrease` | atlantis/value_chooser.xml, value_chooser.xml |
| `ValueChooserShiftIncrease` | atlantis/value_chooser.xml, value_chooser.xml |

### Warmap

| event | fired from |
|---|---|
| `WarmapKeepSelect{0-6}` | atlantis/realmwar_agramon.xml, atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml |
| `WarmapPowerBorderSelect` | atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml, atlantis/realmwar_mid.xml |
| `WarmapPowerRelicSelect` | atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml, atlantis/realmwar_mid.xml |
| `WarmapPowerRelicTownSelect` | atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml, atlantis/realmwar_mid.xml |
| `WarmapStrengthBorderSelect` | atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml, atlantis/realmwar_mid.xml |
| `WarmapStrengthRelicSelect` | atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml, atlantis/realmwar_mid.xml |
| `WarmapStrengthRelicTownSelect` | atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml, atlantis/realmwar_mid.xml |
| `WarmapTeleportRequest` | atlantis/realmwar_agramon.xml, atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml |
| `WarmapTowerSelect{0-27}` | atlantis/realmwar_agramon.xml, atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml |
| `WarmapUpdateBattles` | atlantis/realmwar_agramon.xml, atlantis/realmwar_alb.xml, atlantis/realmwar_hib.xml |
| `WarmapUpdateBonuses` | atlantis/interface_elements_window.xml, atlantis/realmwar_agramon.xml, atlantis/realmwar_alb.xml |
