# Contributing

## Release process

`.codex-plugin/plugin.json` is the single source of truth for the release version. While the project is pre-1.0, use PATCH for compatible fixes and documentation, and MINOR for new behavior or contract changes.

For each release:

1. Run `make release VERSION=X.Y.Z`. This updates the manifest and creates
   `dist/prudent-ponytail-skill-X.Y.Z.zip` for ChatGPT upload.
2. Validate the plugin, bundled skill, and generated ZIP.
3. Tag the release commit with the matching `vX.Y.Z`.
4. Create a GitHub Release from that tag and attach the ZIP.

Run `make package` to rebuild the ZIP for the current manifest version without
changing the version. Generated archives stay under the ignored `dist/`
directory and are not committed.
