# Upstream snapshot

Repository: https://github.com/easyeda/easyeda-api-skill
Commit: ccfaf28a577b61a09ebc907f0a943d1e6c782def
Declared version: 1.1.36
Retrieved: 2026-09-21

API, source-format and extension references refreshed from this commit.
The bridge remains byte-identical to this project's reviewed v1.4.0 runtime.
Compared with upstream it retains the activeEdaWindowId response fix and the
integrationRevision health field. The entrypoint retains the documented
openProject(projectUuid) correction. ws 8.21.3 remains bundled; development
dependencies are not installed. These patches do not certify all new API calls.
Upstream declares MIT in SKILL.md; it supplies no standalone LICENSE file.
