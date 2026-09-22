# Third-party components / 第三方组件

## v1.8.0 research and numerical references / 本轮参考资料

The four bundled toolsets and seven runtime packages below are unchanged. Newly reviewed `specs-to-pcb`, `circuit-synth` and `atopile` supplied workflow/diagnostic ideas only; no source code or runtime from those projects is included. Pinned commits and inspected files are recorded in [external-method review](references/32-adversarial-improvement.md). JITX Skills was excluded from derivative reuse after its inspected license reserved rights.

`assets/microstrip-reference.json` contains numerical results generated with scikit-rf 1.8.0 as an independent cross-check of the project-authored Hammerstad–Jensen implementation. scikit-rf and its dependencies are not shipped or required at runtime. Agreement tests validate implementation against that reference model, not a fabricator's impedance tolerance.

新增参考项目没有作为依赖打包。微带线参考数据用于交叉核对计算结果，不代表实板测量或生产公差承诺。

This inventory describes files actually shipped in this repository. Versions are
pinned source snapshots, not claims about the latest upstream release. Original
workflow, templates and integration scripts use the root [MIT License](LICENSE).
Bundled components retain the notices and licenses listed below.

以下清单按仓库实际文件核对。随包提供 4 套工具或方法库及 7 个 JavaScript
运行依赖；外部后端和需要另行安装的程序单独列出。固定版本、原始许可和
本地修改分别记录，仓库根目录的 MIT 许可不替代第三方许可。

## Bundled tools / 随包工具

| Source | Version and commit | Location | License evidence |
|---|---|---|---|
| [easyeda/easyeda-api-skill](https://github.com/easyeda/easyeda-api-skill) | 1.1.36 · `ccfaf28a577b61a09ebc907f0a943d1e6c782def` | [vendor/easyeda-api](vendor/easyeda-api/) | MIT declared in upstream SKILL.md; no standalone LICENSE supplied |
| [easyeda/easyeda-enhanced-schematic-skill](https://github.com/easyeda/easyeda-enhanced-schematic-skill) | 1.2.0 · `0c4b9a0ad94d532923dee5c828a6efa7444f4506` | [vendor/easyeda-schematic-net-fanout](vendor/easyeda-schematic-net-fanout/) | MIT declared in upstream SKILL.md; no standalone LICENSE supplied |
| [easyeda/easyeda-pro-format-skill](https://github.com/easyeda/easyeda-pro-format-skill) | 1.0.0 · `bee647fbe5e649ab9b4d8ebe3a201a1eee68ff03` | [vendor/easyeda-pro-format-skill](vendor/easyeda-pro-format-skill/) | Original [MIT LICENSE](vendor/easyeda-pro-format-skill/LICENSE) retained |
| Adapted subset of [daishuge/pcb-skill](https://github.com/daishuge/pcb-skill) | `6e939b64907e3c63236c7522c511af5d7d1afaad` | [vendor/pcb-skill-toolkit](vendor/pcb-skill-toolkit/) | Original [MIT LICENSE](vendor/pcb-skill-toolkit/LICENSE) retained |

The first three sources belong to the EasyEDA organization. The PCB inspection
toolkit is a community project. Bundled copies include local adaptations and are
not pristine upstream distributions. No missing copyright statements, dates or
license texts have been invented.

前三项取自 EasyEDA 官方仓库；PCB 检查工具来自社区项目。原理图增强仓库的
Skill 名称为 `easyeda-schematic-net-fanout`，因此本地目录使用该名称。

### API and bridge

The API documentation was refreshed to 1.1.36 on 2026-09-21. Earlier package history
used a user-supplied 1.1.28 distribution; it is not the currently bundled API version.
The bridge retains the runtime reviewed in this project's v1.4.0, including the
`activeEdaWindowId` response correction and `integrationRevision` health field.
The entrypoint retains the `openProject(projectUuid)` signature correction.
These changes do not establish that every documented API works on every client.
See [the source record](vendor/easyeda-api/UPSTREAM.md).

### Schematic methods

The upstream README, skill entrypoint and ESP32-S3 example are retained. The
compatibility field was moved under metadata; the source recipe and its dependency
semantics remain intact. Apply the project-authored
[methods adapter](references/15-easyeda-schematic-methods.md) before those recipes.
It preserves staged placement/wiring, supported schematic styles, pin review and
native readback. The example is not an electrically approved reference design.
See [the source record](vendor/easyeda-schematic-net-fanout/UPSTREAM.md).

### Native-format validation

Local changes move invocation metadata, expose schema maps to the strict file-input
adapter and use registry.npmjs.org for locked tarballs while retaining integrity
pins. Six runtime dependencies were installed with lifecycle scripts disabled and
are shipped with their original license files. Schema validity alone does not
establish native import or electrical correctness. See
[the source record](vendor/easyeda-pro-format-skill/UPSTREAM.md).

### PCB inspection toolkit

The included subset contains placement, routing, verify and notify scripts with
their documentation. Local fixes cover native-data coverage, repeated physical
lands, plating and via spans, geometric routing protection, outline topology and
edge margins, actual mask-opening unions, assertion validation and process/output
monitoring. [UPSTREAM.md](vendor/pcb-skill-toolkit/UPSTREAM.md) records adaptations;
[reference 18](references/18-pcb-inspection-toolkit.md) defines supported scope.

The upstream skill entrypoint, purchase workflow, approval automation and
case-specific board are not bundled. Optional notification code is not configured
or activated by this package. No external autorouter is included. This toolkit is
an inspection component under the parent design workflow.

## Bundled runtime packages / 运行依赖

| Package | Version | License | Retained license file |
|---|---|---|---|
| ws | 8.21.3 | MIT | [LICENSE](vendor/easyeda-api/node_modules/ws/LICENSE) |
| ajv | 8.20.0 | MIT | [LICENSE](vendor/easyeda-pro-format-skill/node_modules/ajv/LICENSE) |
| ajv-formats | 2.1.1 | MIT | [LICENSE](vendor/easyeda-pro-format-skill/node_modules/ajv-formats/LICENSE) |
| fast-deep-equal | 3.1.3 | MIT | [LICENSE](vendor/easyeda-pro-format-skill/node_modules/fast-deep-equal/LICENSE) |
| fast-uri | 3.1.7 | BSD-3-Clause | [LICENSE](vendor/easyeda-pro-format-skill/node_modules/fast-uri/LICENSE) |
| json-schema-traverse | 1.0.0 | MIT | [LICENSE](vendor/easyeda-pro-format-skill/node_modules/json-schema-traverse/LICENSE) |
| require-from-string | 2.0.2 | MIT | [license](vendor/easyeda-pro-format-skill/node_modules/require-from-string/license) |

These packages supply the bridge transport and native-format validator. The
shipped paths require no npm install. Optional ws native acceleration packages
and development-only dependencies are not included. Lockfiles and package metadata
retain the version information; MANIFEST.sha256.json fingerprints the shipped files.

这些依赖已经随包附带，原始许可文件保留在对应目录。用户仍需准备 Node.js；
本包没有附带 Node.js 安装程序。

## External-only integrations / 仅外部接入

| Project | Reviewed snapshot | Integration boundary |
|---|---|---|
| [zhoushoujianwork/easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) | `d090a4665c62c005623f2144f7024f6bf1f13016`; additional layout review `caf102b3ea12a667c963b9d29484f5887751b97b` | Optional typed CLI/daemon/Connector; no source, skill or binary bundled. Reviewed notices include MIT and an Apache-2.0 exception |
| [oaslananka/easyeda-mcp-pro](https://github.com/oaslananka/easyeda-mcp-pro) | `dcfd4a7a73ff9e02d114ecb4492ab248711615c6` | Optional MCP backend; no source or service bundled. Reviewed snapshot uses PolyForm Noncommercial 1.0.0 |

These are community projects. They are not installed automatically; their license
notices describe reviewed snapshots and must be checked against any separately
selected distribution. The root MIT license grants no additional rights to them.
See [backend selection](references/16-easyeda-operation-backends.md).

这两个项目均未收录源码、Connector 或运行服务；当前只有操作后端接入说明。
不因它们能调用官方 API 就将其称为官方工具。

## Separately supplied software / 另行准备的软件

Node.js, Python, the EasyEDA desktop application and Run API Gateway are not
redistributed here. NumPy is optional for raster/copper-clearance inspection and
is not bundled. External autorouters and JVMs are not bundled. Install only the
software needed by the selected workflow, using its own license and setup instructions.

## User-supplied visual reference / 用户提供的排版参考

[assets/schematic-style-reference.png](assets/schematic-style-reference.png) was
provided by the user on 2026-09-06 and retained at their request. Its original
author and license have not been independently established. It illustrates page
organization and is not an electrically validated circuit. The root MIT grant
does not extend to this image.

该图用于说明原理图页面组织，按用户要求收录；原作者和原始许可尚未独立确认，
不纳入本仓库自有内容的 MIT 授权范围。
