# Upstream snapshot

- Repository: https://github.com/easyeda/easyeda-enhanced-schematic-skill
- Commit: `0c4b9a0ad94d532923dee5c828a6efa7444f4506`
- Declared skill name/version: `easyeda-schematic-net-fanout`, `1.2.0`
- Retrieved: 2026-09-21
- Files retained: README.md, SKILL.md, references/esp32-s3-debugger-example.md.
- License declaration: upstream SKILL.md declares MIT. This revision has no separate LICENSE file or explicit copyright notice; none has been invented.

Local change: the top-level compatibility field is stored under metadata for
compatibility with the local skill validator. Its dependency requirement is
unchanged. The workflow and example text are retained as upstream references.

Within PCB-Design-Skill, read ../../references/15-easyeda-schematic-methods.md
before applying upstream recipes. It specifies the integrated loading order,
stage boundaries, version probes, geometry review and protected-edit rules.
The example is not an approved reference circuit or a pin-map authority.
No additional service, separate skill installation or npm dependency is needed.
