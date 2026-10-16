# Skill Benchmark: daoc-xml-ui

**Model**: <model-name>
**Date**: 2026-10-16T02:35:15Z
**Evals**: 3 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 83% ± 0% | +0.17 |
| Time | 584.0s ± 0.0s | 735.0s ± 0.0s | -151.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- Iteration 2 ran only the new eval 3 (planted: background drawn last, adapter case error, template-name typo, MinWidth below cap size). With skill 6/6 in 584s; baseline 5/6 in 735s (missed only 'uses/recommends the linter').
- Both agents discovered a real stock client at C:\Program Files (x86)\Electronic Arts\Dark Age of Camelot (1.130) and verified names against ui\atlantis, which is why the baseline also found the non-stock template names and the OffsetRight misplacement. On a machine without the client the baseline would have had to guess those.
- Baseline fault #1 ('WindowId must equal custom2_window, the client binds the slot by WindowId') contradicts shipping evidence: BobsUI's working custom1_window has WindowId 'Floating Player Health' and is opened by ToggleCustom1. The skill's references state WindowId is a label. No assertion scores this, so it is a qualitative mark against the baseline, not a counted failure. Consider an assertion 'does not report faults that are not faults' in a later iteration.
- The eval input used BobsUI template names (statusbar_red, fresizeimage_dlg_bg_small) while claiming a stock base; both agents correctly flagged them as non-stock, which was an unintended fifth fault. The eval file now uses stock names (red_status, dlg_sm_title) with the single typo blue_statu so future runs test exactly the intended faults.
- Skill changes driven by this iteration: stock 1.130 inventory added (scripts/data/stock, references/stock-templates.md, stock windows table + uimain load order), linter auto-detects ui\atlantis and now ignores 'none' references and type-distinct duplicate names, OffsetRight semantics documented, IconSetDef / OnShiftClickEvent / AdvancedStyle / Priority / Parent documented.
- Token counts not exposed by the harness; one run per configuration, so treat the comparison as directional.
