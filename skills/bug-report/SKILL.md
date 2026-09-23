---
name: bug-report
description: Report a bug in a Sugar theme file, or a mistake, gotcha or quirk you ran into while editing the user's Sugar theme or Shopify store, to the Sugar team without the user leaving the conversation. Use when a bug surfaces in an unedited Sugar file, when you or the user catch a mistake you made, or when you learn something every other agent working on Sugar should know. Check for updates first; the issue may already be fixed.
disable-model-invocation: false
---

# Overview

Send the Sugar theme team one of two kinds of report through the Sugar theme MCP:

- **A bug** in a shipped Sugar file, or an issue that affected you while working on the user's theme.
- **A learning:** a mistake you made while cloning or using existing Sugar files, a gotcha the docs didn't cover, or a quirk of Shopify or the CLI that cost you time. Learnings expose gaps in the docs, and once reviewed they reach every other agent working on Sugar so nobody hits the same thing twice.

The user never leaves the conversation and never fills in a form. The MCP knows who they are from their license, so you do not ask for their email, license key or store.

# Step 1: Check before you send

1. **Is it already fixed?** Search the updates index by symptom through the update-check skill. If a change matches, apply it instead of reporting it.
2. **Is it already known?** The report tool checks for duplicates itself and answers with the existing entry when it finds one. If it does, read the entry: it may carry a workaround, and you are done.
3. **Is it a bug at all?** A file you or another agent edited is not a Sugar bug; check the project's `custom-sections-blocks.md` before blaming the shipped file. A setting that does nothing is a bug, not a quirk.

# Step 2: Report

Send the report with the MCP's report tool, kind `bug` or `learning`, with:

- **Files affected**, by path, with the release stamp from each file's first line, and the theme's `theme_version`.
- **Description of the issue:** what you expected, what happened, on which page and device. For a bug, the steps to reproduce it. For a learning, the wrong way and the right way, so it can be turned into a docs line.
- **What you tried**, and the workaround if you found one.
- **Where to see it:** the storefront preview link to the page, if the user is fine sharing it.
- **Date** of the issue.

Say in one line what you sent and what the answer was: filed as new, or already known, and any workaround it came back with. Reports go into a review queue; only approved ones are distributed to other agents, so a report is never visible to anyone else the moment it is sent.
