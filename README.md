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
│   └── cli/
│       └── httpie/
│           └── SKILL.md
├── LICENSE
└── README.md
```

## Contributing

Contributions welcome. Each skill lives in its own directory under `skills/<category>/<skill-name>/` and requires a `SKILL.md` with valid frontmatter per the [Agent Skills spec](https://agentskills.io/specification.md).

## Request a Skill

Don't see what you need? [Open an issue](https://github.com/Zettersten/skills/issues/new).

## License

MIT
