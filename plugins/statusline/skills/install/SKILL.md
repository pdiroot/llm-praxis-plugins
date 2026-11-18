---
name: install
description: Install the llm-praxis status line in the user settings. Use when the user runs /statusline:install.
disable-model-invocation: true
---

Install the status line in the user settings, so that it shows in each
project and nothing goes into a repository.

1. Find the config folder of Claude Code: run
   `echo "${CLAUDE_CONFIG_DIR:-$HOME/.claude}"`. The next steps call it
   `{config}`.
2. Copy `${CLAUDE_PLUGIN_ROOT}/statusline.py` to `{config}/statusline.py`.
   Replace the file if it exists: this is how the status line is updated.
3. Read `{config}/settings.json`. If it has a `statusLine` that runs a
   different command, stop and tell the user. Do not replace it.
4. Otherwise, set this `statusLine` in `{config}/settings.json` and keep every
   other setting. Create the file if it does not exist:

   ```json
   "statusLine": {
     "type": "command",
     "command": "uv run --quiet --script \"${CLAUDE_CONFIG_DIR:-$HOME/.claude}/statusline.py\"",
     "refreshInterval": 30
   }
   ```

5. If `.claude/settings.json` or `.claude/settings.local.json` of the current
   project has a `statusLine`, tell the user that it hides the one in the user
   settings in this project.
6. Tell the user that the status line shows now in each project, and that
   they can change it in the settings at the top of `{config}/statusline.py`.
