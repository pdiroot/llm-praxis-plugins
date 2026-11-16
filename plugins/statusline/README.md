# Status Line

A Claude Code plugin of the [`llm-praxis` marketplace](../../README.md). It
adds a status line to a project:

```text
shop │ Opus │ high │ $12.47 │ ◷ cache 41m │ ▰▰▰▱▱▱▱▱ 34% │ 5h 42% │ 7d 61% ↻ 3d 4h13m
```

This is the real output for a session in the directory `shop` with Opus at
high effort. It has cost $12.47 so far, its one-hour prompt cache has 41
minutes left, and it uses 34% of the context window. 42% of the 5-hour
limit is used. 61% of the 7-day limit is used, and it resets in 3 days 4
hours 13 minutes. The 5-hour limit shows no reset time, because it is below
50%.

| Segment | Color |
|---------|-------|
| Directory where Claude Code started | Cyan |
| Cost | Default; yellow over $20, red over $50 |
| Prompt cache, minutes left | Default; yellow when half of its lifetime is gone, red at 80% |
| Context window | Default; yellow from 50%, red from 80% |
| 5-hour and 7-day limits: percent used, then the time to reset from 50% used | Default; yellow from 50%, red from 80% |

Everything else, the model and effort included, has the default color. A
segment with no data is left out.

## Requirements

- Claude Code 2.1.251 or later
- `uv`, which runs the script. It uses the Python standard library only.

## Install

```text
/plugin marketplace add pdiroot/llm-praxis-plugins
/plugin install statusline@llm-praxis
```

Then run `/statusline:install` in the project. It copies the script to
`.claude/statusline.py` and adds `statusLine` to `.claude/settings.json`. It
never replaces a status line that you set yourself. Run it again to update
the script.

To show the reset time of a limit from a different percent, set
`STATUSLINE_RESET_FROM` in the `env` of `.claude/settings.json`. Use `0` to
always show it:

```json
"env": {
  "STATUSLINE_RESET_FROM": "0"
}
```

To change the colors or the other thresholds, edit the settings at the top
of `.claude/statusline.py`: `CYAN`, `YELLOW` and `RED` for the colors,
`WARN`, `DANGER`, `COST_WARN`, `COST_DANGER` and `RESET_FROM` for the
thresholds. To remove it, delete `statusLine` from `.claude/settings.json`,
then delete `.claude/statusline.py`.

## License

MIT. See [`LICENSE`](../../LICENSE).
