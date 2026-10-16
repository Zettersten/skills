# Skills

A curated collection of AI agent skills following the [Agent Skills](https://agentskills.io/) format.

---

Skills follow the [Agent Skills](https://agentskills.io/) format and work across Warp, Claude Code, Codex, Cursor, Gemini CLI, and other compatible agents.

## Browse Skills

View all skills with documentation and examples at [skills.sh](https://skills.sh/Zettersten/skills).

## Install

### Agent Skills (npx)

```bash
npx skills add Zettersten/skills
```

### Codex

```bash
codex plugin marketplace add Zettersten/skills
```

After adding the marketplace, restart Codex, open `/plugins`, select the skill collection, install and enable it, then start a new thread.

### Manual (Claude Code)

```bash
git clone https://github.com/Zettersten/skills ~/.claude/skills/zettersten
```

### Manual (Warp)

```bash
git clone https://github.com/Zettersten/skills ~/.agents/skills/zettersten
```

## Skills

### CLI Tools

| Skill | Tool | What It Does |
|-------|------|--------------|
| `httpie` | HTTPie CLI | Make HTTP requests with expressive, human-friendly syntax |

### Automation & APIs

| Skill | Tool | What It Does |
|-------|------|--------------|
| `sharepoint-api` | agent-browser + SharePoint REST API | Automate SharePoint/OneDrive operations — list files, download/upload documents, filter with CAML queries, discover APIs via HAR capture |

### Marketing & Strategy

| Skill | Focus | What It Does |
|-------|-------|--------------|
| `positioning-messaging-grill` | Customer research and messaging | Grills users to build a differentiated positioning and messaging framework with evidence, outcomes, benefits, and proof points |

### Reporting & Communication

| Skill | Focus | What It Does |
|-------|-------|--------------|
| `weekly-report-writer` | Weekly updates and status reports | Structures friendly, concise, privacy-safe weekly reports with clear guidance for tone, length, verbosity, risks, and next steps |

### UI & Visual Effects

| Skill | Tool | What It Does |
|-------|------|--------------|
| `liquid-glass` | CSS / SVG | Implement Apple's Liquid Glass UI effect (iOS 26 / macOS 26) using SVG displacement filters and backdrop-filter |

### Games & Modding

| Skill | Tool | What It Does |
|-------|------|--------------|
| `daoc-xml-ui` | Dark Age of Camelot XML UI | Author, modify, debug and restyle DAoC custom UIs (ui\custom, WindowTemplates, adapters, events, custom windows) with verified syntax, references rebuilt from the stock 1.130 skin and working custom UIs (1000+ adapters, 280+ events, every stock template name), a linter that checks against the real ui\atlantis, and a self-contained example mod |

## Repository Structure

```
skills/
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .codex-plugin/
│   └── plugin.json
├── .claude-plugin/
│   └── marketplace.json
├── skills/
│   ├── daoc-xml-ui/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── scripts/
│   │   ├── examples/
│   │   └── evals/
│   ├── httpie/
│   │   └── SKILL.md
│   ├── liquid-glass/
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   ├── references/
│   │   └── scripts/
│   ├── positioning-messaging-grill/
│   │   └── SKILL.md
│   ├── weekly-report-writer/
│   │   └── SKILL.md
│   └── sharepoint-api/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
├── LICENSE
└── README.md
```

## Contributing

Contributions welcome. Each skill lives in its own directory under `skills/<skill-name>/` and requires a `SKILL.md` with valid frontmatter per the [Agent Skills spec](https://agentskills.io/specification.md).

## Request a Skill

Don't see what you need? [Open an issue](https://github.com/Zettersten/skills/issues/new).

## License

MIT
