# Skills

A curated collection of AI agent skills following the [Agent Skills](https://agentskills.io/) format.

---

Skills follow the [Agent Skills](https://agentskills.io/) format and work across Warp, Claude Code, Codex, Cursor, Gemini CLI, and other compatible agents.

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

### UI & Visual Effects

| Skill | Tool | What It Does |
|-------|------|--------------|
| `liquid-glass` | CSS / SVG | Implement Apple's Liquid Glass UI effect (iOS 26 / macOS 26) using SVG displacement filters and backdrop-filter |

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
│   ├── httpie/
│   │   └── SKILL.md
│   ├── liquid-glass/
│   │   ├── SKILL.md
│   │   ├── assets/
│   │   ├── references/
│   │   └── scripts/
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
