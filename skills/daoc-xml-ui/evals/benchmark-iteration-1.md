# Skill Benchmark: daoc-xml-ui

**Model**: <model-name>
**Date**: 2026-10-16T02:04:33Z
**Evals**: 0, 1, 2 (1 run each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 100% ± 0% | 87% ± 23% | +0.13 |
| Time | 535.0s ± 213.2s | 1256.0s ± 992.5s | -721.0s |
| Tokens | 0 ± 0 | 0 ± 0 | +0 |

## Notes

- One run per configuration per eval: the +-23% stddev is across-eval spread, not run-to-run noise. Treat +0.13 as directional, not statistically established.
- Token counts were not exposed by the orchestration harness, so the Tokens column is 0. Wall time is launch-to-succeeded for each child agent.
- Eval 1 (debug-button-does-nothing) did not discriminate: both configurations found both planted bugs (event mismatch, click-order overlap) and scored 6/6. The base model already knows ToggleCustomN semantics and XML click order. Next iteration should plant subtler faults (template-name typo, adapter case error, missing Include, MinWidth below cap size) that need the reference lists or the linter.
- Eval 0 (new-floating-player-bars): 9/9 for both on assertions, but qualitatively different. Baseline's primary deliverable repurposes clock_window.xml (works, but costs the clock window and depends on /clock); the custom-slot route is only an appendix. With-skill followed the customN_window + ToggleCustomN recipe with private templates and a generated texture sheet, and finished in 665s vs 1205s.
- Eval 2 (triage-logic-request) is where the skill pays off: with-skill answered in 651s, named daochook, gave the server-rules caveat and a frame-strip StatusIcon approximation for threshold colour. Baseline took 2273s building scaffolding XML (new_group_window.xml, a gradient texture, a PowerShell generator) before concluding it is impossible, and never named daochook (3/5).
- The with-skill eval-2 run surfaced a nuance the skill under-stated: threshold-based colouring IS approximable in XML with a multi-frame StatusIconTemplate (frame index follows the 0-100 scalar). Only flashing/animation and timers are truly impossible. SKILL.md triage updated accordingly.
- Assertion 'Does not present fabricated XML elements for logic' passed in both configurations; it is a guardrail rather than a discriminator here.
- Grader note: the first grading pass failed the baseline eval-1 run for a leftover 'ToggleCustom4' that was only inside an XML comment; the grader now strips comments. All verdicts above are from the corrected grader.

