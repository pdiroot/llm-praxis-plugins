---
name: install
description: Install the llm-praxis status line in this project. Use when the user runs /statusline:install.
disable-model-invocation: true
---

Install the status line in this project.

1. Copy `${CLAUDE_PLUGIN_ROOT}/statusline.py` to `.claude/statusline.py`.
   Replace the file if it exists: this is how the status line is updated.
2. Read `.claude/settings.json` and `.claude/settings.local.json`. If either
   has a `statusLine` that runs a different command, stop and tell the user.
   Do not replace it.
3. Otherwise, set this `statusLine` in `.claude/settings.json` and keep every
   other setting. Create the file if it does not exist:

   ```json
   "statusLine": {
     "type": "command",
     "command": "uv run --quiet --script \"$CLAUDE_PROJECT_DIR/.claude/statusline.py\"",
     "refreshInterval": 30
   }
   ```

4. Tell the user that the status line shows now, that `.claude/settings.json`
   is shared with everyone who works in this project, and that they can
   change the status line in the settings at the top of
   `.claude/statusline.py`.
