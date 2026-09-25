---
name: weekly-report-writer
description: Create clear, friendly, privacy-safe weekly reports and status updates from notes, tickets, meetings, or work logs. Use when someone asks for a weekly report, weekly update, team summary, progress report, project status update, or a rewrite that should match a supplied reporting example and tone.
license: MIT
metadata:
  author: Zettersten
  version: "1.0"
---

# Weekly Report Writer

Use this skill to turn scattered weekly notes into a readable, useful, and friendly report. The report should help the reader understand what happened, what matters, what is next, and where help or a decision is needed.

The goal is not to make the report sound impressive. The goal is to make the state of the work easy to understand without exposing personal information or burying important details.

## Core Principles

- Be friendly, calm, and direct.
- Lead with progress and outcomes, not a raw activity log.
- Use plain language and short sentences.
- Preserve the user's meaning, but remove repetition and internal clutter.
- Separate completed work, current work, upcoming work, risks, and asks.
- State uncertainty clearly rather than making the week sound more certain than it was.
- Keep each item proportional to its importance.
- Use an example as a reference for tone, format, level of detail, and rhythm, never as a source of facts.
- Remove or generalize personally identifiable information before it appears in the report.

## When To Use This Skill

Use this skill for:

- Weekly team updates.
- Project or program reports.
- Individual work summaries.
- Leadership status reports.
- Client-safe weekly updates.
- Product, engineering, operations, marketing, or research updates.
- A recurring weekly report that needs a consistent structure.
- Rewriting rough notes into a friendly report.
- Matching a supplied example without copying its private details.

Do not use it to fabricate progress, convert speculation into a commitment, or produce a performance evaluation about a named individual.

## First Step: Understand The Request

Before drafting, identify:

1. The reporting period, if it can be stated safely.
2. The intended audience.
3. Whether the report covers a person, team, project, product area, or portfolio.
4. Whether the reader needs a quick scan or a detailed record.
5. The source material: notes, tickets, meeting summaries, metrics, milestones, or a previous report.
6. Whether the user supplied an example to imitate.
7. Whether there are required headings, word limits, or formatting constraints.

If the user does not specify an audience, assume a busy stakeholder who wants the essential status in two to four minutes.

If the user does not specify a period, use a neutral placeholder such as `[Reporting period]`. Do not guess dates.

If the user does not specify a tone, use the default tone below.

## Tone Reference

### Default tone

The default tone is:

- Warm without being chatty.
- Professional without being stiff.
- Honest without being alarmist.
- Positive without pretending everything went perfectly.
- Specific without overexplaining.
- Helpful without sounding like a sales pitch.

### Reference tone from the supplied guidance

The reference guidance uses a friendly leadership voice: direct, appreciative, practical, and comfortable asking for better discipline without sounding punitive. It explains why the format matters, gives concrete expectations, and leaves room for follow-up discussion. It is conversational enough for email but focused enough for executive reporting.

Match these qualities when using that reference:

- Start with a brief human explanation of the purpose and audience.
- Use plain language such as `less is more`, `what matters most`, and `happy to discuss` when appropriate.
- Connect updates to business impact, especially cost, schedule, delivery, customers, and organizational priorities.
- Encourage people to surface risks without making the report feel like a fault-finding exercise.
- Recognize good work and recovery from setbacks.
- Give clear process guidance without overformalizing it.
- End with a short, appreciative close rather than a long motivational statement.

Do not copy the reference's people, organization names, sign-off, or private reporting chain. Reproduce the tone and operating principles only.

Prefer:

- "This week, the team completed..."
- "The main change was..."
- "The work is on track, with one open dependency..."
- "Next week, we plan to..."
- "A decision is needed on..."

Avoid:

- "We crushed it."
- "Huge wins everywhere."
- "Obviously..."
- "As everyone knows..."
- "No blockers" when risks or dependencies are present.
- Inflated claims such as `transformational`, `revolutionary`, or `world-class`.
- Defensive language that assigns blame.

### How to use a supplied example

If the user provides an example report, analyze it before writing. Extract:

- Tone: warm, formal, upbeat, matter-of-fact, reflective, or urgent.
- Point of view: first person singular, first person plural, or neutral team voice.
- Typical sentence length.
- Heading style.
- Whether bullets are fragments or full sentences.
- How much context appears before a result.
- How risks and setbacks are phrased.
- Whether the report ends with asks, next steps, or a short reflection.
- Approximate length of each section.
- The amount of detail expected in a single item.

State the interpretation briefly before drafting, for example:

> I will use a warm, concise team voice with short outcome-led bullets, brief context for risks, and a focused next-steps section.

Do not copy names, email addresses, customer details, personal circumstances, ticket IDs, internal links, exact private metrics, or distinctive anecdotes from the example. The example controls style, not facts.

If the example and the user's explicit instruction conflict, follow the explicit instruction and note the adjustment.

If the example is long, do not automatically make the new report long. Match the example's information density and section proportions, then remove material that is not useful for this reporting period.

## Privacy And PII Rules

The final report must not include unnecessary personally identifiable information. Treat privacy as a drafting requirement, not a final cleanup step.

### Remove or generalize

Remove or generalize:

- Full names and personal usernames.
- Personal email addresses, phone numbers, home addresses, and private contact details.
- Government, employee, customer, patient, student, account, ticket, or device identifiers.
- Personal URLs, profile links, calendar links, and direct message links.
- Exact private locations when a broader region or team description is enough.
- Personal schedules, travel details, family details, health information, or other sensitive circumstances.
- Private customer information unless the user explicitly confirms it is approved for the audience.
- Screenshots or copied text that contain private information.
- Unique combinations of role, date, location, and event that could identify someone unnecessarily.

Use safe substitutions such as:

- `[team member]`
- `[project lead]`
- `[customer]`
- `[partner team]`
- `[vendor]`
- `[internal system]`
- `[region]`
- `a mid-sized customer`
- `a recent release`
- `the first half of the week`

### Preserve useful context without identity

Keep the role, responsibility, and work context when it helps the report:

- `The design lead reviewed the flow.`
- `The partner team confirmed the dependency.`
- `A pilot customer completed onboarding.`

Do not write:

- `[person], [email address], reviewed the flow.`
- `The customer at [street address] completed onboarding.`

### Metrics and dates

Metrics are not automatically PII, but a very small sample, a named person, a precise timestamp, or a unique customer result can make them identifying. When needed:

- Round or aggregate numbers.
- Use ranges instead of exact values.
- Report team or project totals instead of individual activity.
- Use the reporting week rather than precise event timestamps.
- Omit the metric if it does not help the reader make a decision.

Do not claim that content is anonymous unless the user has actually checked that it cannot identify someone.

### What to do when source material contains PII

1. Do not repeat the PII in the response.
2. Replace it with a role, team, category, or placeholder.
3. Preserve only the non-identifying context needed for the report.
4. Tell the user briefly that identifying details were generalized, without quoting them.
5. If removing the detail changes the meaning, ask whether a privacy-safe category is acceptable.

Never infer, reconstruct, or look up missing personal details.

## Recommended Report Shape

For the supplied reporting style, use this structure by default:

1. `Weekly Status Report: [Group or Area]`
2. `Submitted by: [role or team]`
3. `Reporting period: [period]`
4. `Priorities`
5. `Highlights`
6. `Lowlights`
7. `Help Needed`
8. `Travel / PTO`

The report should focus on the four or five topics that account for most of the material cost, schedule, customer, delivery, or operational movement. Do not turn the report into a complete activity log.

For each major section, use no more than four or five bullets. Keep each topic to two or three sentences maximum. Omit an empty section when appropriate, except where the audience explicitly needs a confirmation that there are no material issues.

### Submission cadence and medium

When following the supplied guidance, treat Thursday close of business (COB) as the normal submission deadline. Use email as the current submission medium unless the user provides a different process. A future move to a dedicated team channel can be treated as a process note, not as report content.

Do not invent a deadline when none was provided. If the user asks for a reusable template, include the deadline as an optional process note rather than embedding it as a fact about every organization.

### Acronyms and visuals

Spell out every acronym the first time it appears, followed by the acronym in parentheses. Use the shortened form afterward only when it improves readability. Do not assume the reader knows internal or industry-specific abbreviations.

Photos, diagrams, and screenshots may be suggested when they explain a change better than prose, but use them sparingly. They should support the report, not dominate it. Never reproduce an image or screenshot that contains unredacted personal information, private links, names, contact details, or identifiers.

Do not include every section when it would be empty. Use `No material blockers this week` only when the source supports that statement. Otherwise omit the section or write `No blockers were noted in the source material` if that distinction matters.

## Length And Verbosity Guide

Use the smallest amount of detail that lets the reader understand the status. The ranges below are defaults, not rigid rules.

| Item | Target length | Verbosity | What it should contain |
|---|---:|---|---|
| Title | 3 to 10 words | Minimal | Topic and period, without private identifiers |
| Overall summary | 25 to 50 words | Low | Main progress, current state, and notable concern |
| Priority item | 20 to 45 words | Low to medium | Focus area, business alignment, and target date when useful |
| Highlight item | 20 to 60 words | Low to medium | Accomplishment, milestone, business impact, and recognition when appropriate |
| Lowlight item | 30 to 75 words | Medium | Risk or challenge, discovery, impact, mitigation, and next step |
| Help-needed item | 25 to 60 words | Medium | Support requested, requested role, first-ask date, impact, and urgency |
| Travel or PTO item | 10 to 25 words | Low | Approximate timing, coverage role, and relevant impact |
| Next-week item | 15 to 40 words | Low | Planned action and intended outcome |
| Closing note | 20 to 50 words | Low | Appreciation, confidence level, or transition to next week |
| Full report | 250 to 500 words | Medium | Enough detail to inform without becoming a work log |

For an executive scan, aim for 150 to 300 words. For this team-to-leadership format, aim for 250 to 500 words. Exceed 500 words only when the audience needs an operational record or the reporting period contains significant decisions and risks.

### Verbosity levels

#### Brief

Use one sentence or one bullet per item. State the change and outcome. Use this for routine work and familiar audiences.

Example pattern:

`Completed [work], which enables [outcome].`

#### Standard

Use two sentences or one substantial bullet. Add the most useful context, dependency, or result. This is the default.

Example pattern:

`Completed [work]. This matters because [outcome or implication].`

#### Detailed

Use two to four sentences. Add context, evidence, tradeoffs, and the next step. Reserve this for major decisions, material risks, meaningful changes, or work that a reader cannot understand from the headline alone.

Example pattern:

`Completed [work]. The change addresses [problem] and resulted in [evidence or observed effect]. The remaining consideration is [risk or dependency], with [next step] planned.`

Do not give every bullet the detailed treatment. Uneven detail is useful when it reflects uneven importance.

## Drafting Workflow

### Step 1: Gather and classify the source material

Sort source notes into:

- Completed.
- In progress.
- Planned.
- Outcome or evidence.
- Risk or blocker.
- Decision or ask.
- Context only.
- Unclear or contradictory.

Do not assume that the order of notes reflects importance.

### Step 2: Identify the reporting period

Use the user's stated period. If it is missing, insert `[Reporting period]` rather than guessing. If exact dates are unnecessary, use a week label such as `Week of [date]` only when supplied.

### Step 3: Find the three to five most important messages

Prioritize:

1. Outcomes that changed the state of the work.
2. Decisions that affect scope, schedule, quality, cost, or risk.
3. Blockers or dependencies that require attention.
4. Commitments for the next period.
5. Evidence that helps the reader assess progress.

Deprioritize routine activity unless it explains an outcome or a risk.

### Step 4: Build a factual outline

Before writing polished prose, create a short internal outline:

| Item | Status | Why it matters | Evidence | Confidence | PII check |
|---|---|---|---|---|---|
| Example item | Complete | Enables next phase | Source note | Reported | Generalized |

Mark statements as:

- **Observed:** directly present in the source material.
- **Reported:** supplied by the user but not independently checked.
- **Inferred:** a reasonable interpretation.
- **Planned:** intended work, not completed work.
- **Unclear:** needs clarification.

Do not turn an inference into a fact in the final report.

### Step 5: Match the reference tone

Compare the outline with the supplied example, if any:

- Is the example first person or third person?
- Does it use bullets, short paragraphs, or both?
- Does it lead with results or activities?
- Does it use casual contractions?
- How does it describe setbacks?
- How much detail does one bullet receive?
- Does it include a closing reflection?

Apply the style while keeping the content original and privacy-safe.

### Step 6: Draft the summary first

Write the one-sentence or short-paragraph summary after selecting the important messages. It should answer:

- What changed this week?
- What is the current state?
- What deserves attention?

Do not write a vague summary such as `It was a productive week.`

### Step 7: Draft each item at the right size

Use the length table. Expand only when the item has meaningful context, evidence, risk, or a decision. Compress routine work into a single bullet.

### Step 8: Add next steps and asks

Make planned work distinct from completed work. Every ask should say what is needed and why. Do not hide an ask in a long paragraph.

### Step 9: Run the privacy pass

Search the draft for:

- Names.
- Email-like strings.
- Phone-like strings.
- Addresses.
- Usernames and handles.
- Direct links.
- IDs and ticket numbers.
- Customer or partner details not approved for the audience.
- Precise personal circumstances.

Generalize or remove them before presenting the report.

### Step 10: Run the usefulness pass

Confirm that a reader can answer:

- What happened?
- Why does it matter?
- What is still underway?
- What might change the plan?
- What happens next?
- Is a decision or action needed from me?

## Section Instructions

### Title

Length: 3 to 10 words.

Verbosity: minimal.

Format options:

- `Weekly Status Report: [Group or Area]`
- `Weekly Status Report: [Project or Area]`

Do not include a person's full name, private customer name, or an internal identifier in the title.

### Submitted by and reporting period

Length: one short line each.

Verbosity: minimal.

Use privacy-safe role or team labels rather than personal names when the report is intended to remain free of PII:

```text
Submitted by: [role or team]
Reporting period: [period]
```

Do not copy a real submitter name from a reference example. If the user explicitly wants a named submission field in their own report, use `[submitter]` until they provide an approved value for the intended audience.

### Priorities

Length: 20 to 45 words per bullet; no more than four or five bullets.

Verbosity: low to medium.

Use this section for near-term efforts and focus areas tied to broader business goals. Include a target completion or review date when it is known. Keep an item here from week to week until it is completed, deprioritized, or intentionally moved elsewhere.

Each item should answer:

- What is the priority?
- Why does it matter to the business?
- What is the current state?
- When is the target closure or review date, if known?

Template:

> **[Priority]:** [Near-term focus] supports [business goal or impact]. Target [date or timeframe] is [date, status, or not yet set].

### Highlights

Length: 20 to 60 words per bullet; no more than four or five bullets.

Verbosity: low to medium.

Use this section for recent accomplishments, internal or external milestones, and meaningful progress. Lead with the outcome and connect it to business impact where possible.

This is also the right place to recognize team effort without naming individuals. Use a role or team label, such as `[delivery team]` or `[operations lead]`, when recognition is useful but the report must remain PII-free.

If a previous lowlight was resolved or materially improved, include it as a highlight and label the recovery clearly, for example `Recovery from prior risk:`.

Good pattern:

`Completed [specific work], enabling [specific outcome or business impact].`

If there is no outcome yet, say what the work makes possible and label the result as expected rather than achieved.

### Lowlights

Length: 30 to 75 words per bullet; no more than four or five bullets.

Verbosity: medium.

Use this section for risks, blockers, emerging technical or operational challenges, and important changes to the plan. It is acceptable not to have a complete resolution path yet, but include how and when the issue was discovered, its business impact, and what is being done to understand or mitigate it.

Each item should include:

- What happened or changed?
- When or how was it discovered?
- What business impact could result?
- What mitigation, investigation, or next step is underway?

Template:

> **[Risk or challenge]:** [What happened and when it was identified]. This may affect [cost, schedule, quality, customer, or operations]. [Mitigation or next step] is underway; the next update is expected [timeframe].

Do not name or blame an individual. Refer to the role, team, dependency, or process.

### Help Needed

Length: 25 to 60 words per bullet; no more than four or five bullets.

Verbosity: medium.

Use this section for requests for personnel, customer support, equipment, decisions, cross-functional help, or escalation. State who or what role is being asked, even when the request is initially directed to the report recipient.

Keep an item here from week to week until it is resolved, no longer needed, or superseded. Include the date of the first ask using a period or generalized date when possible; do not expose private correspondence.

Each item should answer:

- What support is needed?
- Who or what team is being asked?
- Why is it needed?
- What is the business impact if it remains open?
- When was it first raised, if known?

Template:

> **[Support needed]:** Requesting [role or team] support with [specific need]. First raised [period or date]. This affects [business impact]; the next action is [action or decision].

If the request belongs outside the reporting team's area, identify the function rather than a person, such as `[Finance]`, `[Business Development]`, `[Legal]`, or `[customer support]`.

### Travel / PTO

Length: 10 to 25 words per bullet; one to three bullets.

Verbosity: low.

Include a high-level view of planned travel or time off for the next 30 to 60 days only when the audience needs it for coverage or scheduling. Include approximate timing and the delegate role. Do not include personal reasons, private itineraries, home locations, or other identifying details.

Template:

> **[Approximate period]:** [Team or role] coverage will be handled by [delegate role or team].

If no coverage information is provided, write `No coverage changes were noted in the source material` rather than asking people to disclose private details in the report.

### Optional next steps

Length: 15 to 40 words per bullet; no more than four or five bullets.

Verbosity: low.

Use this only when the supplied format or audience needs a separate next-week section. In the reference format, near-term work belongs in `Priorities`, so do not add this section by default.

State planned actions and intended outcomes. Use `plan to`, `expect to`, or `will evaluate` when the item is not a firm commitment.

Good pattern:

`[Work] is underway. Next, [action] will address [purpose or outcome].`

### Closing note

Length: 20 to 50 words.

Verbosity: low.

Use only when it fits the tone reference or audience. It may express appreciation, confidence with a caveat, or a transition to the next reporting period.

Example:

> Thanks to everyone who helped move this forward. The next focus is [priority], with [known consideration] still being monitored.

Do not add a generic motivational paragraph just to make the report feel finished.

## Writing Patterns

### Outcome-led bullets

Prefer:

`Validated the new workflow with representative users, giving the team a clearer basis for the next design iteration.`

Over:

`Had several meetings about the new workflow.`

### Honest uncertainty

Prefer:

`Early feedback is encouraging, but the sample is small. The next step is to test the workflow with a broader group.`

Over:

`The workflow is proven.`

### Friendly risks

Prefer:

`The integration remains the main schedule risk. The team is confirming the dependency this week and will adjust the plan if access is delayed.`

Over:

`The integration team is holding us up.`

### Useful metrics

Include a metric only when it answers one of these questions:

- Did progress occur?
- Did quality improve?
- Did usage or adoption change?
- Is the plan at risk?
- Does the reader need to make a decision?

Pair a metric with interpretation:

`Completion increased from the previous period, which suggests the revised workflow is reducing rework.`

Do not list metrics without explaining what they mean.

## Handling Missing Or Conflicting Information

If a note is incomplete:

- Use `[detail needed]` in a draft intended for review.
- Omit the detail in a final reader-facing report if it is not essential.
- Ask one focused question when the missing fact changes the meaning.

If notes conflict:

1. Do not silently choose the more favorable version.
2. State the conflict briefly.
3. Ask which version is authoritative, or report the uncertainty.
4. Keep the final wording neutral until resolved.

If there are no measurable outcomes:

- Report meaningful progress, decisions, completed milestones, or reduced uncertainty.
- Do not invent metrics.
- Explain what evidence will be available next.

If the week was quiet:

- Say what was maintained, reviewed, or intentionally deferred.
- Mention only material changes.
- Avoid padding the report with low-value activity.

## Final Review Checklist

### Tone

- Is the report friendly and professional?
- Does it match the supplied example's tone and structure when one was provided?
- Is it honest about setbacks and uncertainty?
- Is it free of hype, blame, and defensive language?

### Content

- Is the reporting period clear or safely marked as a placeholder?
- Does the summary explain what changed and why it matters?
- Are completed, in-progress, and planned work clearly separated?
- Are risks and asks visible?
- Are routine activities compressed?
- Are outcomes distinguished from intentions?

### Length and verbosity

- Is the full report within the audience-appropriate range?
- Are routine bullets brief?
- Do only important items receive detailed context?
- Are long paragraphs split into readable bullets or short paragraphs?
- Does each section follow its target length?

### Privacy

- Are names, emails, phone numbers, addresses, handles, IDs, and private links removed or generalized?
- Are customer and partner details appropriate for the audience?
- Could a combination of details identify someone unnecessarily?
- Did the report avoid quoting private source material?

### Accuracy

- Did every completed item actually happen in the reporting period?
- Are plans clearly labeled as plans?
- Are metrics and claims supported by the source?
- Are unresolved questions visible?

## Output Format

When no structure is provided, use:

```markdown
# Weekly Status Report: [Group or Area]
**Submitted by:** [Role or team]
**Reporting period:** [Reporting period]

## Priorities
- [20 to 45 words; no more than four or five bullets]
- [20 to 45 words]

## Highlights
- [20 to 60 words; no more than four or five bullets]
- [20 to 60 words]

## Lowlights
- [30 to 75 words; include discovery, impact, and mitigation]

## Help Needed
- [25 to 60 words; include requested role and first-ask period]

## Travel / PTO
- [10 to 25 words; use approximate timing and coverage role]
```

If the user requests a more conversational style, keep the same information architecture but use short paragraphs instead of headings and bullets only where they improve scanning.

If the user supplies a recurring report format, preserve its headings and order unless they ask for a redesign. Apply the length and privacy rules inside that format.

## Response Behavior

When producing the report:

1. Briefly state the tone and level of detail you are using, especially when following an example.
2. Present the privacy-safe report first.
3. After the report, include a short `Notes` section only if needed.
4. Mention generalized or omitted identifying details without reproducing them.
5. List unresolved factual questions separately from the report.
6. Do not add a lengthy explanation of the writing process unless the user asks for one.

When the input is too thin to draft responsibly, ask for the smallest missing set of details:

- Reporting period.
- Audience.
- Three to five important events or outcomes.
- Current risks or dependencies.
- Planned next steps.
- A tone or format example, if they want close matching.

## Example Interpretation Template

Use this before drafting from an example:

> **Reference read:** The example uses a `[warm/formal/matter-of-fact]` tone, `[first-person/team/neutral]` voice, and `[short bullets/brief paragraphs]`. Items are generally `[brief/standard/detailed]`, with extra context reserved for `[risks, decisions, major outcomes]`. I will keep that style while generalizing identifying details.

Do not claim that the example has a tone or format that it does not have. If no example was provided, say:

> **Default style:** Friendly, concise, outcome-led, and transparent about risks. Routine items will be brief; important decisions and blockers will receive more context.
