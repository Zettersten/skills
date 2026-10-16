# Event reference

Events are what buttons fire: `<OnClickEvent>Name</OnClickEvent>` on a `ButtonDef`, `InvisibleButtonDef`,
`HorizontalResizeButtonDef`, `HorizontalResizeImageButtonDef`, `CheckBoxDef`, `IconDef`, slider or `ListBoxDef`
(`OnClickEvent`, `OnHeaderClickEvent`), and `ComboBoxDef` (`OnChangeEvent`). Event names are not case sensitive.

The XML cannot define new behaviour: an event only works if the client implements it. Some events need
state the window owns (a selected list row, a chosen pet mode) and only make sense inside that window.

- **official** = in the Trials of Atlantis document, with its description.
- **observed** = wired to a control in a complete, working 1.127-era custom UI (CynicalJedi/DAOC-UI-Chooser).
  No official description exists; the name and the window it is used in are the documentation.

Totals: 66 official, 253 observed, 280 distinct.

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
| `ToggleCasualGroupFinder` | stats_group_window.xml |
| `ToggleClock` | command_window.xml, custom0_window.xml, interface_elements_window.xml |
| `ToggleCommandWindow` | custom0_window.xml, interface_elements_window.xml |
| `ToggleCompassWindow` | interface_elements_window.xml |
| `ToggleConcentration` | command_window.xml, custom0_window.xml, interface_elements_window.xml |
| `ToggleFloatChampXP` | interface_elements_window.xml |
| `ToggleFloatLevelXP` | interface_elements_window.xml |
| `ToggleFloatRealmXP` | interface_elements_window.xml |
| `ToggleFloatTarget` | interface_elements_window.xml |
| `ToggleGroupBuffs` | command_window.xml, custom0_window.xml, interface_elements_window.xml |
| `ToggleGroupOptions` | stats_group_window.xml |
| `ToggleHelp` | command_window.xml, custom0_window.xml, main_menu_window.xml |
| `ToggleInterfaceElements` | interface_elements_window.xml, main_menu_window.xml |
| `ToggleJournal` | command_window.xml, custom0_window.xml, custom11_window.xml |
| `ToggleMainMenu` | menu_bar_window.xml |
| `ToggleMap` | clock_window.xml, command_window.xml, custom0_window.xml |
| `ToggleMasterLevel` | command_window.xml, custom0_window.xml, custom11_window.xml |
| `ToggleMenuBar` | interface_elements_window.xml |
| `ToggleMiniFriends` | custom0_window.xml, interface_elements_window.xml |
| `ToggleMiniGroup` | command_window.xml, custom0_window.xml, interface_elements_window.xml |
| `ToggleMiniPet` | command_window.xml, custom0_window.xml, interface_elements_window.xml |
| `ToggleMount` | interface_elements_window.xml |
| `ToggleNewGroup` | interface_elements_window.xml |
| `ToggleNewSummary` | interface_elements_window.xml |
| `ToggleOptions` | command_window.xml, custom0_window.xml, main_menu_window.xml |
| `TogglePerformanceMeter` | command_window.xml, custom0_window.xml, interface_elements_window.xml |
| `ToggleQuiver` | command_window.xml, custom0_window.xml, interface_elements_window.xml |
| `ToggleStatsAttributes` | menu_bar_window.xml |
| `ToggleStatsGroup` | menu_bar_window.xml |
| `ToggleStatsInventory` | menu_bar_window.xml |
| `ToggleStatsSkills` | menu_bar_window.xml |
| `ToggleStatsSpells` | menu_bar_window.xml |
| `ToggleStatsStyles` | menu_bar_window.xml |
| `ToggleSummary` | interface_elements_window.xml |
| `ToggleTitle` | interface_elements_window.xml |
| `ToggleWarmapKey` | custom0_window.xml, realmwar_agramon.xml, realmwar_alb.xml |

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
| `Help` | Shows the Help Window | - |
| `Release` | Issues the /release command | yes |
| `Relic` | Shows the /relic display | yes |
| `Bonuses` | Shows the /bonus display (resists) | yes |
| `ShowKeyboardConfig` | Shows the keyboard configuration display | yes |
| `Journal` | Shows the Quest Journal Window | - |
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
| `AssistTarget` | float_target_window.xml |

### Chat

| event | fired from |
|---|---|
| `ChatRenameCancel` | chatrename.xml |
| `ChatRenameOK` | chatrename.xml |

### Com

| event | fired from |
|---|---|
| `ComAllianceMemberSelected` | community_window.xml |
| `ComAllianceMembersNext` | community_window.xml |
| `ComAllianceMembersPrev` | community_window.xml |
| `ComAllianceMembersShowOffline` | community_window.xml |
| `ComAllianceMembersSort` | community_window.xml |
| `ComAllianceSend` | community_window.xml |
| `ComFriendsMemberSelected` | community_window.xml |
| `ComFriendsMembersSort` | community_window.xml |
| `ComFriendsSend` | community_window.xml |
| `ComGuildBannerDeploy` | community_window.xml |
| `ComGuildCommands` | community_window.xml |
| `ComGuildDemote` | community_window.xml |
| `ComGuildMemberSelected` | community_window.xml |
| `ComGuildMembersNext` | community_window.xml |
| `ComGuildMembersPrev` | community_window.xml |
| `ComGuildMembersShowOffline` | community_window.xml |
| `ComGuildMembersSort` | community_window.xml |
| `ComGuildNote` | community_window.xml |
| `ComGuildPromote` | community_window.xml |
| `ComGuildSend` | community_window.xml |
| `ComGuildWithdraw` | community_window.xml |
| `ComLFGuildInvite` | community_window.xml |
| `ComLFGuildMemberSelected` | community_window.xml |
| `ComLFGuildMembersSort` | community_window.xml |
| `ComLFGuildSend` | community_window.xml |
| `ComTabChanged` | community_window.xml, custom13_window.xml, custom17_window.xml |
| `ComTabRefresh` | community_window.xml |

### Community

| event | fired from |
|---|---|
| `Community` | command_window.xml, custom0_window.xml, interface_elements_window.xml |

### Context

| event | fired from |
|---|---|
| `ContextOnAddChatWindow` | context_chat_main.xml, context_chat_sub.xml |
| `ContextOnDefaultChannel` | context_chat_main.xml, context_chat_main2.xml, context_chat_sub.xml |
| `ContextOnDeleteChatWindow` | context_chat_sub.xml, context_chat_sub2.xml |
| `ContextOnFontAlpha` | context_chat_main.xml, context_chat_main2.xml, context_chat_sub.xml |
| `ContextOnMessageAndChannel` | context_chat_main.xml, context_chat_main2.xml, context_chat_sub.xml |
| `ContextOnRenameChatWindow` | context_chat_sub.xml, context_chat_sub2.xml |
| `ContextOnWindowAlpha` | context_chat_main.xml, context_chat_main2.xml, context_chat_sub.xml |
| `ContextSetDefaultChannel` | context_default_chat_channel.xml |
| `ContextSetFontAlpha` | context_font_alpha.xml |
| `ContextSetFontSize` | context_font_size.xml |
| `ContextSetWindowAlpha` | context_window_alpha.xml |

### Delve

| event | fired from |
|---|---|
| `Delve` | miniinfo_window.xml |

### Group

| event | fired from |
|---|---|
| `GroupFind` | stats_group_window.xml |

### Hookpoint

| event | fired from |
|---|---|
| `HookpointStoreBP` | hookpoint_merchant_window.xml |
| `HookpointStoreBuy` | hookpoint_merchant_window.xml |
| `HookpointStoreCoin` | hookpoint_merchant_window.xml |
| `HookpointStoreContract` | hookpoint_merchant_window.xml |
| `HookpointStoreGBP` | hookpoint_merchant_window.xml |

### In

| event | fired from |
|---|---|
| `InGameKeyConfigAccept` | key_config.xml |
| `InGameKeyConfigCancel` | key_config.xml |
| `InGameKeyConfigClearKey` | key_config.xml |
| `InGameKeyConfigResetFPS` | key_config.xml |
| `InGameKeyConfigResetMMO` | key_config.xml |
| `InGameKeyConfigResetRPG` | key_config.xml |

### Keep

| event | fired from |
|---|---|
| `KeepStatusHookpoints` | keep_status_window.xml |
| `KeepStatusRepair` | keep_status_window.xml, siegetower_status_window.xml |
| `KeepUpgradeCancel` | keep_upgrade_window.xml |
| `KeepUpgradeRelease` | keep_upgrade_window.xml |

### Master

| event | fired from |
|---|---|
| `MasterLevelPageNext` | master_level_window.xml |
| `MasterLevelPagePrevious` | master_level_window.xml |

### Menu

| event | fired from |
|---|---|
| `MenuBarToggleExp` | menu_bar_window.xml |

### Mino

| event | fired from |
|---|---|
| `MinoRelicDrop` | mino_relic_window.xml |

### Mount

| event | fired from |
|---|---|
| `Mount` | stats_attributes_window.xml |

### New

| event | fired from |
|---|---|
| `NewQuestAccept` | new_quest_window.xml |
| `NewQuestContinue` | new_quest_finish_window.xml |
| `NewQuestDecline` | new_quest_window.xml |
| `NewQuestFinish` | new_quest_finish_window.xml |
| `NewQuestSelectOptReward{0-7}` | new_quest_finish_window.xml |
| `NewTrain` | training_window.xml |
| `NewTrainInfo` | training_window.xml |
| `NewTrainRealmInfo` | training_window.xml |

### Quick

| event | fired from |
|---|---|
| `QuickBind` | key_config.xml |

### Quiver

| event | fired from |
|---|---|
| `QuiverAdd{0-3}` | quiver_window.xml |
| `QuiverSelect{0-3}` | quiver_window.xml |

### Release

| event | fired from |
|---|---|
| `ReleaseToBind` | release_window.xml |
| `ReleaseToCity` | release_window.xml |
| `ReleaseToHouse` | release_window.xml |

### Remove

| event | fired from |
|---|---|
| `RemoveQuest` | new_quest_journal_window.xml, quest_window_orig.xml |

### Respec

| event | fired from |
|---|---|
| `RespecAll` | training_window.xml |
| `RespecBuy` | training_window.xml |
| `RespecRealm` | training_window.xml |

### Show

| event | fired from |
|---|---|
| `ShowWarMap` | command_window.xml, custom0_window.xml, menu_bar_window.xml |
| `ShowWarmap` | interface_elements_window.xml |

### Siege

| event | fired from |
|---|---|
| `SiegeMove` | siege_window.xml |
| `SiegeRelease` | siege_window.xml |
| `SiegeRepair` | siege_window.xml |
| `SiegeSalvage` | siege_window.xml |

### Subclass

| event | fired from |
|---|---|
| `SubclassDelve` | daoc_subclass_window.xml |

### Value

| event | fired from |
|---|---|
| `ValueChooserAccept` | value_chooser.xml |
| `ValueChooserCancel` | value_chooser.xml |
| `ValueChooserDecrease` | value_chooser.xml |
| `ValueChooserIncrease` | value_chooser.xml |
| `ValueChooserShiftDecrease` | value_chooser.xml |
| `ValueChooserShiftIncrease` | value_chooser.xml |

### Warmap

| event | fired from |
|---|---|
| `WarmapKeepSelect{0-6}` | realmwar_agramon.xml, realmwar_alb.xml, realmwar_hib.xml |
| `WarmapPowerBorderSelect` | realmwar_alb.xml, realmwar_hib.xml, realmwar_mid.xml |
| `WarmapPowerRelicSelect` | realmwar_alb.xml, realmwar_hib.xml, realmwar_mid.xml |
| `WarmapPowerRelicTownSelect` | realmwar_alb.xml, realmwar_hib.xml, realmwar_mid.xml |
| `WarmapStrengthBorderSelect` | realmwar_alb.xml, realmwar_hib.xml, realmwar_mid.xml |
| `WarmapStrengthRelicSelect` | realmwar_alb.xml, realmwar_hib.xml, realmwar_mid.xml |
| `WarmapStrengthRelicTownSelect` | realmwar_alb.xml, realmwar_hib.xml, realmwar_mid.xml |
| `WarmapTeleportRequest` | realmwar_agramon.xml, realmwar_alb.xml, realmwar_hib.xml |
| `WarmapTowerSelect{0-27}` | realmwar_agramon.xml, realmwar_alb.xml, realmwar_hib.xml |
| `WarmapUpdateBattles` | realmwar_agramon.xml, realmwar_alb.xml, realmwar_hib.xml |
| `WarmapUpdateBonuses` | command_window.xml, custom0_window.xml, interface_elements_window.xml |
