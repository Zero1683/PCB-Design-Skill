# EasyEDA operation backends

Read this when choosing or changing the integration used for EDA operations.
The project workflow owns requirements, G0-G9 sequencing, the two allowed
schematic formats, electrical/geometry review and manufacturing handoff.
Operation tools implement those decisions. Their examples, scores, install
defaults and whole-project workflows do not override the user's scope or this
project's acceptance criteria.

## Reviewed sources

| Source | Provenance / reviewed snapshot | Integration role |
|---|---|---|
| [easyeda-api-skill](https://github.com/easyeda/easyeda-api-skill) | EasyEDA organization; 1.1.36, `ccfaf28a577b61a09ebc907f0a943d1e6c782def` | Bundled default API documentation, live bridge and source-format reference |
| [easyeda-pro-format-skill](https://github.com/easyeda/easyeda-pro-format-skill) | EasyEDA organization; 1.0.0, `bee647fbe5e649ab9b4d8ebe3a201a1eee68ff03` | Bundled native primitive schemas, examples and validator; use reference 17 |
| [easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) | Community project; reviewed main declares 1.5.3-dev.3, `d090a4665c62c005623f2144f7024f6bf1f13016` | Optional typed CLI, daemon and Connector backend; not bundled or installed |
| [easyeda-mcp-pro](https://github.com/oaslananka/easyeda-mcp-pro) | Community project; reviewed main declares 1.1.0-rc.1, `dcfd4a7a73ff9e02d114ecb4492ab248711615c6` | Optional external MCP inspection/export interface; not bundled or installed |

These are reviewed source snapshots, not claims about current release channels
or successful execution on the user's client. Only the repositories under the
EasyEDA organization are identified here as official sources. Community tools
may call the official eda API without being official EasyEDA products.

## Select by operation

- **Default live design/edit/export:** bundled official API via Run API Gateway,
  using reference 06's discovery and selected window/document checks.
- **Repeated structured operations:** an already installed, compatible
  easyeda-agent can provide typed input/output, dry-run plans, layout operations
  and readback. Verify each command/action first. Do not install it merely to
  execute an operation already handled reliably by the default API path.
- **Native source inspection/generation or a verified API gap:** official format
  documentation and validation, in a working copy; native import and save/reopen
  remain separate checks. It is a file layer, not another connection service.
- **Existing MCP environment:** easyeda-mcp-pro can expose inspection, BOM and
  export operations if separately installed and licensed for the intended use.
  Its tool profiles and advertised capabilities are not proof of actual support.

## One writer and explicit handoff

Record backend name/version, connector type, service endpoint, project/window/
document identity and baseline for the operation scope. Run the backend's health
and read-only capability checks. An occupied port or familiar service name alone
does not identify a compatible transport. The official bridge, EDA Agent Connector
and MCP Bridge use their own protocols; do not substitute one extension for another.
The MCP project also defaults to the 49620-49629 range used by the official bridge.
Do not stop the official bridge or repoint Gateway simply to resolve that collision.

Keep one writer per document operation scope. Other backends may be installed,
but never interleave mutation queues, autosave, reload or stale object handles.
Before switching: finish or reconcile pending work, save a checkpoint, stop the
old write queue, select the new target explicitly, reread native identities and
pin nets, then map stable identities to fresh runtime handles. Do not assume IDs,
units or state caches transfer between transports. After a partial failure,
read back before retrying or changing backend.

## easyeda-agent adapter

The reviewed project provides a Go CLI/daemon, an EDA Agent Connector extension
and a companion skill. Its MCP entrypoint is an alternative interface to that
tool stack. If selected, obtain a versioned distribution for the target OS and
check its published checksums, license/NOTICE and connector compatibility. The
reviewed main is a development version, not a recommendation to install latest.
Do not execute a remote install script blindly, upgrade unrelated clients or
change all global skill registrations as a side effect of drawing a board.

Use `easyeda health`, `easyeda actions` and the selected command's `--help` to
confirm capability. Use version-matched typed commands/actions and dry-run where
available. Preserve plans, returned object IDs, actual readback and save evidence.
Native operations such as layout, silk cleanup or library construction still
need the project-specific electrical, identity, geometry and manufacturing checks.

Apply these integration boundaries:
- Keep our G2-A unwired snapshot before G2-B; a compose/apply operation that
  combines placement and wiring must be split using supported operations. If
  that is unavailable, use the default API path for that scope.
- Check all visible values, part names and other attributes for collision and
  clipping. The reviewed community workflow excludes some non-designator text
  from its collision envelope; its clean result does not satisfy SCH-TEXT alone.
- Use layouts conforming to free-layout or framed-layout; an upstream layout
  score cannot waive this requirement or pad/silk clearance gates.
- Prefer its typed actions when that backend is selected. Do not inject arbitrary
  JavaScript to bypass a missing action inside that backend. For an unsupported
  operation, perform an explicit checkpoint/handoff to our official API path or
  the narrow UI fallback allowed by reference 06. Its blanket no-GUI workflow
  does not redefine this parent workflow's fallback policy.
- Reused circuits require exact-part and operating-condition review. Do not
  inherit development-board dimensions, pinouts, startup states or exam defaults.

The project's MIT license contains an Apache-2.0 exception for ported beautify
code; its compiled connector requires the corresponding notices. No community
source, connector binary or circuit library is copied into this package.

## easyeda-mcp-pro adapter

At the reviewed commit the project declares PolyForm Noncommercial 1.0.0;
commercial use requires separate terms according to its repository. Keep it an
optional external dependency. Do not copy its source or skills under this
project's MIT grant, and do not infer licensing from a historical MIT badge or
release. Evaluate any older release separately if it is ever selected.

The reviewed main requires Node 24.x and its own bridge extension. This does not
change our default Node 18+ requirement. Verify the selected release's actual
runtime and tool profile, set task-specific writable storage paths, and configure
only the intended client. Do not run setup-all, enable remote relay, supplier
credentials or experimental raw execution merely to inspect a local PCB.

Use read-only scope for review tasks. For authorized edits, confirm the specific
tool and readback support first, retain our snapshot/probe procedure, and report
unsupported operations. Sourcing tools may return candidate parts and prices;
they do not authorize purchases, cart operations, payments or vendor contact.

## Validation boundary

Installing a backend, listing tools or accepting a schema is not a live editing
test. Prove one scoped operation on a disposable design before broad mutations,
then verify native readback, save/reopen and affected checks. Record source-only,
offline-tested and live-tested results separately. See reference 11 for scenarios
and VALIDATION.md for actual execution evidence.
