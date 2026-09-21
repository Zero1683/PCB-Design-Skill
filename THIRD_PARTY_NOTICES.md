# 第三方组件

## EasyEDA API Skill

- 来源：用户提供的 easyeda-api 本地发行包，版本 1.1.28。
- 上游作者：JLCEDA；上游 `SKILL.md` 声明 `license: MIT`。
- 本包位置：`vendor/easyeda-api/`，保留上游文档和包元数据；桥接与入门文档的最小修正见下方补丁记录。
- 原包没有单独的 LICENSE 文件；保留原始许可元数据与作者信息，不另行编造版权年份或授权文本。
- 包内 README 描述了上游开发流程；本集成包的实际启动方式以 `START_HERE.md` 为准，无需执行上游 README 中的文档构建命令。

## ws

- 版本：8.21.3；MIT；源码及原始版权许可全文在 `vendor/easyeda-api/node_modules/ws/`，参见其中 `LICENSE`。
- 仅打包桥接运行所需的纯 JavaScript 文件；未附带可选原生加速包和开发类型依赖。

Node.js、嘉立创EDA客户端和 Run API Gateway 扩展不在此压缩包中，按各自的发行许可安装。本包保留桥接请求协议，并增加向后兼容的健康检查修订字段。

## English

The bundled EasyEDA API Skill 1.1.28 was supplied as a local distribution. Its original `SKILL.md` identifies JLCEDA as the author and declares MIT licensing. Upstream material is retained under `vendor/easyeda-api/`; minimal integration patches are documented below. The supplied distribution contains no separate LICENSE file; no additional upstream copyright notice has been invented. Use this repository's startup instructions instead of the upstream README's development/build steps.

The bundled ws 8.21.3 runtime is MIT licensed. Its full original copyright and license notice is retained at `vendor/easyeda-api/node_modules/ws/LICENSE`. Optional native acceleration packages and development-only type definitions are not bundled.

The root MIT license covers this project's original workflow, templates, and integration scripts; third-party components retain their own notices. Node.js, the EasyEDA desktop application, and Run API Gateway are not distributed here and must be installed under their respective licenses.

## Integration patches in 1.2.0 / 集成修正

- `vendor/easyeda-api/scripts/bridge-server.mjs`: fixes the successful window-selection response to return the defined `activeEdaWindowId`, preventing a misleading error after state changes. Adds `integrationRevision` to health responses so a running older bridge can be identified. Request formats are unchanged.
- `vendor/easyeda-api/SKILL.md`: corrects two `openProject(projectPath)` references to `openProject(projectUuid)`, matching the upstream method signature.
- 自动布线示例与接口字段不一致的部分未擅自修改上游 API 文档，使用说明记录在 `references/03-layout-routing.md`；运行时仍需核实客户端支持。
- 原作者与 MIT 许可信息保留。修正仅覆盖以上具体位置，不代表已验证全部上游 API。

## Schematic style reference / 原理图排版参考

`assets/schematic-style-reference.png` is the schematic example supplied by the user on 2026-09-06 and included at their request. Its original author and license have not been independently established. It is retained as a visual reference for page organization, not as an electrically validated circuit. The repository's MIT grant does not extend to this image.

该图片来自用户于 2026-09-06 提供的原理图示例，按用户要求收录。原作者及原始许可尚未独立确认；图片用于说明页面组织，不代表电路已通过验证，也不纳入本仓库自有内容的 MIT 授权范围。

## EasyEDA schematic enhancement / 原理图增强方法

- Source: https://github.com/easyeda/easyeda-enhanced-schematic-skill
- Snapshot: `0c4b9a0ad94d532923dee5c828a6efa7444f4506`; declared version 1.2.0.
- Bundled at `vendor/easyeda-schematic-net-fanout/`, retaining the README,
  skill entrypoint and ESP32-S3 example. The upstream SKILL.md declares MIT;
  this snapshot contains no separate LICENSE file or explicit copyright notice.
  No upstream copyright statement has been invented.
- Integration adjustment: the compatibility field is moved under metadata;
  dependency semantics and upstream workflow/example text are unchanged.
- The project-authored adapter is `references/15-easyeda-schematic-methods.md`.
  It identifies stage, geometry, pin-review and runtime rules that govern use of
  the upstream examples. The example is not an electrically approved circuit.

原理图增强资料取自上述固定版本，保留上游 MIT 声明。仅调整兼容性元数据位置；
本项目的辅助方法文档单独说明适用条件和集成规则。示例中的器件与脚号不能直接
作为其他设计的选型或连接依据。

## Operation foundations refresh, 2026-09-21

The API references are now sourced from easyeda/easyeda-api-skill 1.1.36,
commit ccfaf28a577b61a09ebc907f0a943d1e6c782def. The earlier 1.1.28 provenance
above describes the original bundle. Retained bridge fixes and the source pin
are recorded in vendor/easyeda-api/UPSTREAM.md; the runtime remains unchanged.

Official easyeda-pro-format-skill 1.0.0 is included from
https://github.com/easyeda/easyeda-pro-format-skill at
bee647fbe5e649ab9b4d8ebe3a201a1eee68ff03. Its original MIT LICENSE is retained.
The metadata adjustment, exported schema maps and locked registry URL change
are documented in vendor/easyeda-pro-format-skill/UPSTREAM.md. Six runtime
packages retain their own license files under that directory's node_modules:
ajv, ajv-formats, fast-deep-equal, fast-uri, json-schema-traverse and
require-from-string. Versions: ajv 8.20.0, ajv-formats 2.1.1, fast-deep-equal 3.1.3,
fast-uri 3.1.7, json-schema-traverse 1.0.0 and require-from-string 2.0.2.
fast-uri uses BSD-3-Clause; the other five use MIT. Refer to the lockfile for integrity pins.

easyeda-agent (zhoushoujianwork) and easyeda-mcp-pro (oaslananka) are community
projects, not claimed to be official EasyEDA products. They are referenced as
optional external backends; no source, skill or connector from either is bundled.
The former has MIT/Apache-2.0 notices; the reviewed latter uses PolyForm
Noncommercial 1.0.0. This project's MIT license does not grant rights to them.

官方 API 已更新至上述固定版本，保留已验证的桥接修正。官方格式 Skill 及运行依赖
随包提供并保留原始许可；社区 CLI 和 MCP 项目只提供外部接入说明，不混入本项目
的 MIT 代码包。具体运行条件与适用范围见 references/16 和 references/17。

## PCB inspection toolkit / PCB 检查工具库

- Source: https://github.com/daishuge/pcb-skill
- Commit: `6e939b64907e3c63236c7522c511af5d7d1afaad`.
- Included subset: placement/routing/verify/notify scripts and associated README files.
- Location: `vendor/pcb-skill-toolkit/`; original MIT copyright and license text
  retained in its LICENSE. Local modifications are listed in UPSTREAM.md.
- This is a community toolkit, not an official EasyEDA component. Its original
  skill entrypoint, procurement workflow and approval automation are not included.
- NumPy is an optional runtime dependency for two tools and is not redistributed.

保留上游署名与 MIT 许可；针对断言误判、Gerber 未支持语义、布线结果时效、
Windows 进程探测及不完整导入做了本地修正。主流程、通用性设置及 EDA 操作基础不变。
