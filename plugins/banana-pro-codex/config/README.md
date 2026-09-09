# Environment package configuration

The source plugin keeps `.mcp.json` pointed at production:
`https://bb.1nutnhan.com/mcp`.

Build a disposable local-dev package with a loopback port:

```bash
python3 plugins/banana-pro-codex/scripts/build_plugin.py \
  --environment dev --port 8000 --output dist/dev
```

Build the Codex Desktop release package explicitly as production:

```bash
python3 plugins/banana-pro-codex/scripts/build_plugin.py \
  --environment production --output dist/production
```

The build script refuses an existing output directory and never copies secrets.
