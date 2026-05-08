# RegenTribes ArchiMate Models

Enterprise architecture models for regenerative communities and Integral Collective nodes.

## What This Is

ArchiMate models expressing the system architecture for:
- **Regenerative Neighbourhood** — physical, social, knowledge, and infrastructure layers
- **Integral Collective Node** — five-subsystem architecture (OAD, ITC, CDS, COS, FRS)

## Repo Structure

```
genesis-zero-bot-archimate/
├── models/           ← .archimate XML files (coArchi format, git-mergeable)
├── exports/          ← rendered output (SVG, HTML, PNG)
├── scripts/          ← JArchi automation scripts
├── templates/        ← reusable model templates
├── assets/           ← CSS (aligned with wiki/ADR/spec — pure B/W minimal)
├── build.py          ← generates rendered output from models
├── _config.yml
└── .github/workflows/pages.yml
```

## Deployment

Push to main → GitHub Actions runs build.py → HTML/SVG/PNG to `_site/` → GitHub Pages at:
```
https://regentribes.github.io/genesis-zero-bot-archimate/
```

## Pipeline

Models are rendered via Docker (archimate-ci-image):
```bash
docker run --rm \
  -v $(pwd)/models:/archi/project \
  -v $(pwd)/exports:/archi/report \
  ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6
```

## Visual Style

Pure B/W minimal — same CSS tokens as wiki-zero-bot, adrs-zero-bot, spec-zero-bot.
Dark default, localStorage theme toggle, 860px max-width.

## ArchiMate Layers Covered

| Layer | Elements | Domain |
|-------|---------|--------|
| **Motivation** | Driver, Goal, Principle, Requirement | Why, governance |
| **Strategy** | Resource, Capability, ValueStream | Strategic positioning |
| **Business** | Actor, Role, Service, Process | Community structure |
| **Application** | Component, Service, DataObject | Software systems |
| **Technology** | Node, Device, Artifact, Path | Infrastructure |
| **Implementation** | WorkPackage, Plateau, Gap | Migration planning |

## Related Repos

- [genesis-zero-bot-wiki](https://github.com/regentribes/genesis-zero-bot-wiki) — knowledge graph
- [genesis-zero-bot-adrs](https://github.com/regentribes/genesis-zero-bot-adrs) — architecture decisions
- [genesis-zero-bot-spec](https://github.com/regentribes/genesis-zero-bot-spec) — Gherkin specifications