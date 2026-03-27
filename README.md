[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-2ea44f?logo=github)](https://zettersten.github.io/skills/)
[![skills.sh](https://img.shields.io/badge/skills.sh-liquid--glass-blue)](https://skills.sh/zettersten)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

# Skills

A collection of AI agent skills focused on modern CSS/SVG visual effects and web UI techniques.

## Overview

This repository contains focused, self-contained skills that teach AI agents how to implement advanced visual effects — starting with Apple's Liquid Glass refraction system introduced in iOS 26 / macOS 26.

Install via the skills CLI:

```bash
npx skills add Zettersten/skills@liquid-glass
```

Or browse at: **[zettersten.github.io/skills](https://zettersten.github.io/skills/)**

## Skills

This repo currently includes 1 skill:

| Skill | Folder | Description |
| --- | --- | --- |
| Liquid Glass | `liquid-glass` | Implements Apple's iOS 26 / macOS 26 Liquid Glass UI effect using CSS `backdrop-filter` and SVG `feDisplacementMap`. Covers the full technique from physics (Snell's law, SDF) to copy-paste HTML/React templates with a zero-dependency displacement map generator. |

## Usage

Each skill is self-contained. Refer to the `SKILL.md` file in each skill directory for triggers, workflow guidance, examples, and supporting references.

```bash
# Install liquid-glass skill
npx skills add Zettersten/skills@liquid-glass

# Or generate a custom displacement map directly
python liquid-glass/scripts/generate-displacement-map.py \
  --width 300 --height 56 --radius 28 --mode sdf --datauri
```

## What's inside `liquid-glass`

```
liquid-glass/
├── SKILL.md                           # Triggers + 4-layer composition guide
├── scripts/
│   └── generate-displacement-map.py  # Zero-dep Python: SDF + Snell's law modes
├── references/
│   ├── physics.md                    # Snell's law, surface functions, SDF math
│   └── filter-pipeline.md            # SVG filter primitives, browser compat, perf
└── assets/templates/
    ├── glass-button.html             # Standalone pill button demo (Chrome)
    ├── glass-card.html               # Card with chromatic aberration
    ├── glass-pill-navbar.html        # Apple-style tab bar with nested active state
    └── LiquidGlass.tsx               # React 18+ component, browser fallback
```

## Browser Compatibility

The full refraction effect requires **Chrome / Chromium** (`backdrop-filter: url(#svg-filter)`).
Firefox and Safari gracefully degrade to frosted blur (`backdrop-filter: blur()`).

## Contributing

Skills are designed to be focused and reusable. When adding new skills, ensure they:
- Have a clear, single purpose
- Include comprehensive documentation
- Follow consistent patterns with existing skills
- Include reference materials when applicable

## License

MIT
