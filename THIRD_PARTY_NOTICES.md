# 第三方组件

## EasyEDA API Skill

- 来源：用户提供的 easyeda-api 本地发行包，版本 1.1.28。
- 上游作者：JLCEDA；上游 `SKILL.md` 声明 `license: MIT`。
- 本包位置：`vendor/easyeda-api/`，文档、桥接源码、包元数据保持原样。
- 原包没有单独的 LICENSE 文件；保留原始许可元数据与作者信息，不另行编造版权年份或授权文本。
- 包内 README 描述了上游开发流程；本集成包的实际启动方式以 `START_HERE.md` 为准，无需执行上游 README 中的文档构建命令。

## ws

- 版本：8.21.3；MIT；源码及原始版权许可全文在 `vendor/easyeda-api/node_modules/ws/`，参见其中 `LICENSE`。
- 仅打包桥接运行所需的纯 JavaScript 文件；未附带可选原生加速包和开发类型依赖。

Node.js、嘉立创EDA客户端和 Run API Gateway 扩展不在此压缩包中，按各自的发行许可安装。本包启动器及集成说明未修改上游桥接协议。

## English

The bundled EasyEDA API Skill 1.1.28 was supplied as a local distribution. Its original `SKILL.md` identifies JLCEDA as the author and declares MIT licensing. Original documentation, bridge source, and package metadata are preserved under `vendor/easyeda-api/`. The supplied distribution contains no separate LICENSE file; no additional upstream copyright notice has been invented. Use this repository's startup instructions instead of the upstream README's development/build steps.

The bundled ws 8.21.3 runtime is MIT licensed. Its full original copyright and license notice is retained at `vendor/easyeda-api/node_modules/ws/LICENSE`. Optional native acceleration packages and development-only type definitions are not bundled.

The root MIT license covers this project's original workflow, templates, and integration scripts; third-party components retain their own notices. Node.js, the EasyEDA desktop application, and Run API Gateway are not distributed here and must be installed under their respective licenses.
