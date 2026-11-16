# LLM Praxis Plugins

The `llm-praxis` marketplace of Claude Code plugins for the LLM Praxis
sessions.

## Plugins

| Plugin | What it does |
|--------|--------------|
| [`statusline`](plugins/statusline/README.md) | A status line that shows the model, effort, cost, prompt cache, context and usage windows |

## Install

In Claude Code, add the marketplace once:

```text
/plugin marketplace add pdiroot/llm-praxis-plugins
```

Use the path of a local clone in place of `pdiroot/llm-praxis-plugins` if
you have one. Then install a plugin by its name:

```text
/plugin install <plugin>@llm-praxis
```

Each plugin's README gives its requirements and how to use it.

To get new versions, run `/plugin marketplace update llm-praxis`.

## License

MIT. See [`LICENSE`](LICENSE).
