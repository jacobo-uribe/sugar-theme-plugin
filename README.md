# Sugar Theme plugin

Skills and references that teach an AI agent to edit a Shopify store built on the [Sugar theme](https://sugarthe.me).

Install in Claude Code:

```
/plugin marketplace add jacobo-uribe/sugar-theme-plugin
/plugin install sugar-theme@sugar
```

Then, in a fresh project folder for your store, run `/sugar-theme:setup`.

Enable auto-update for the `sugar` marketplace (`/plugin` → Marketplaces) so the skills stay current.

## Other agents

Claude Code is the recommended and tested path. The skills use the open `SKILL.md` format, so agents that read it can use the same repo. For Codex, Cursor or Gemini CLI, install the skills with the community installer:

```
npx skills add jacobo-uribe/sugar-theme-plugin
```

Then connect the Sugar theme MCP by hand in your agent's MCP settings, and run the `setup` skill in a fresh project folder. The setup skill writes `AGENTS.md`, which those agents read natively. Marketplace auto-update is a Claude Code feature; other agents re-run the installer to update.

## Layout

- `skills/` — one folder per skill (`setup`, `clone`, `build`, `freestyle`, `ask`, `enhance`, `variations`, `speed-optimization`, `update-check`, `feedback`)
- `references/` — shared documents the skills read: `store-editing`, `creation-methods`, `new-file-creation`, `variations`, `custom-sections-blocks` (log template), `catalog-index` (generated)
- `docs/MCP.md` — the contract for the Sugar theme MCP the skills call

Only content a merchant can see in the theme editor lives here. Liquid internals and gated material are served by the MCP behind a license.
