# Upstream snapshot

Repository: https://github.com/easyeda/easyeda-pro-format-skill
Commit: bee647fbe5e649ab9b4d8ebe3a201a1eee68ff03
Declared version: 1.0.0
Retrieved: 2026-09-21
License: MIT; original LICENSE retained.

Integration changes:
- Move when_to_use and argument-hint under metadata for the local skill validator.
- Export DOC_TYPES and DOC_TYPE_MAP from validate.js for the strict file-input
  adapter; upstream validation and schemas are unchanged.
- Resolve locked dependency tarballs from registry.npmjs.org instead of
  registry.npmmirror.com, retaining exact versions and integrity hashes.
- Bundle the six locked runtime dependencies with their original license files;
  installation used npm ci --omit=dev --ignore-scripts. No install is required
  to use the shipped validator.

Use ../../references/17-easyeda-native-format.md before the upstream recipes.
Write generated files in the task workspace, not inside this vendor directory.
Schema acceptance is not native import, connectivity or electrical acceptance.
