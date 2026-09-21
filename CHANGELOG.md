# v1.5.0 — 工程约束与独立 PCB 检查 / Engineering constraints and PCB inspection

## 中文

### EDA 操作基础
- 内置 EasyEDA API 文档更新至 1.1.36，保留桥接窗口选择和状态检查修复。
- 集成官方原生格式文档、Schema 和离线校验依赖；新增按文档与图元类型校验的入口，拒绝不明确的回退。
- 增加社区 CLI/MCP 后端选择与交接说明。社区后端不自动安装，非商业许可实现不打包进入 MIT 项目。

### 独立检查与布线辅助
- 适配并内置 daishuge/pcb-skill 的脚本子集，保留 MIT 许可与来源记录。
- 增加受支持原生数据提取、布局与通道筛查、Gerber/钻孔/阻焊检查、三维包络检查和 DSN/SES 布线辅助入口。
- 修复未知网络误判通过、缺失封装被跳过、旧布线输出被当作任务完成等问题。
- 未支持的 Gerber 极性、变换和孔径宏明确报错；Windows 进程状态检查改为非终止式探测。

### 工程约束
- 将原厂依据、计算输入、EDA 规则、实际几何和制造文件复核对应到同一设计版本。
- 补充供电与启动、封装映射、时钟与回流、密脚扇出、热设计及逐项 DFM 警告处置。
- 新增阻焊开窗与阻焊桥、直线扇出通道、圆形孔环计算，以及中英文工程记录字段。
- 保留现有主流程、两种原理图格式和分阶段检查；默认交付范围仍为 G5 制造准备。

### 验证与适用范围
- 本次发布复测：81 项 Python 测试，80 项通过、1 项因 Windows 符号链接权限跳过；8 项 Node 格式校验测试通过，隔离的模拟桥接测试通过。
- 集成时的 21 个工具自测结果详见 VALIDATION.md。包内 MANIFEST.sha256.json 用于解压后的完整性检查。
- 原生导入仅覆盖所支持的数据格式。工具库板级模型与原有规范化快照仍是两个模型，需要同一基线下的交叉核对。
- 新工具链尚未完成真实 EDA 工程全流程、macOS、外部布线器互操作和实板制造验证。脚本通过不等于整板验收。

## English

### EDA operation foundations
- Update bundled EasyEDA API documentation to 1.1.36 while retaining bridge window-selection and health fixes.
- Bundle official native-format references, schemas and offline validator dependencies. Add explicit document/primitive dispatch without ambiguous schema fallback.
- Document optional community CLI/MCP backends and scoped handoffs. No automatic backend installation; the reviewed noncommercial implementation remains external.

### Independent inspection and routing support
- Adapt the MIT-licensed script subset of daishuge/pcb-skill with attribution and provenance.
- Add supported native extraction, placement/channel screening, Gerber/drill/mask checks, mesh envelopes and DSN/SES helpers.
- Reject unresolved net assertions and missing footprints; prevent stale routing files from marking a new run complete.
- Fail explicitly on unsupported Gerber polarity, transforms and aperture macros. Probe Windows processes without terminating them.

### Engineering constraints
- Connect exact-part/process sources, calculations, native rules, actual geometry and manufacturing review to one baseline.
- Expand power/startup, package mapping, clock/return, dense escape, thermal and item-specific DFM guidance.
- Add mask opening/web, straight escape-channel and circular annular-ring arithmetic plus English/Chinese project records.
- Preserve the workflow, two schematic formats and staged reviews. Default design delivery remains G5 manufacturing preparation.

### Validation and scope
- Release rerun: 81 Python cases, 80 passed and one Windows symlink-permission skip; 8 Node format cases passed; isolated simulated bridge checks passed.
- Integration-time results for 21 toolkit self-tests are recorded in VALIDATION.md. MANIFEST.sha256.json verifies extracted package integrity.
- Native extraction has bounded format support. Toolkit board data and normalized snapshots remain separate models requiring same-baseline reconciliation.
- No new live EDA end-to-end, macOS, external-router interoperability or physical manufacturing validation is claimed.
