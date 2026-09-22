# Unreleased (main) · 验收、几何与成本规划 / Acceptance, geometry and cost planning

Current changes are published on `main`; the latest tagged Release remains v1.6.0.
Documentation now consolidates the current capabilities, 356-case regression status,
upgrade path, four bundled third-party packages and seven runtime dependencies.
Optional external backends are listed separately. No dependency versions changed
in this documentation update.

- Add sourced, revisioned placement locks, allowed regions, keepouts and height checks; unknown height blocks applicable acceptance.
- Require constraint files for new guarded native schematic batches; verify source, target and intermediate states. Bind rule contents and local file hashes to journals.
- Add read-only resume with fresh native state inspection; changed rules or lost sessions require reconciliation.
- Bound summary/query/diff by actual UTF-8 output bytes. Preserve oversized records on disk and return explicit digest handles with correct pagination.
- Add offline PCB geometry checks and document routing capability review. No native PCB writer/rollback or complex-board qualification is claimed.

- Recheck actual final geometry and ordered intermediate clearance; detect stale operation replays before returning success.
- Support native empty rectangle interiors and explicitly scoped repair of invalid contract baselines; preserve final rules and expose restored baseline defects.
- Add requirement/check/evidence mapping with file hashes to G5 design gates; reject separator-only evidence paths.
- Record native test1 frame/move/repair/persistence/restoration evidence and an explicit capability matrix. Whole-board benchmarking and native PCB mutation remain pending.

- Add idea-to-function-to-BOM component costing with current 立创商城 quote sources, MOQ/order increments and separate consumption/purchase totals.
- Add decimal quote arithmetic with explicit missing-price/stock handling; preserve functional requirements during cost reduction and reconcile final BOM costs at G5.

- Enforce the independent G0-G9 minimum check registry, current saved-design hashes, explicit manual/composite gate decisions and mapped-check reconciliation.
- Add fixed read-only checker execution recording with input/tool drift detection; preserve raw failed/blocked observations without promoting them to PASS.
- Unify actual geometry validation for apply, replay, resume and save/reopen; derive bridge diagnostic version from the bundled package.
- Add requirement-by-requirement substitution review, complete quote observation coverage, explicit BOM quantity/spare changes and retained source captures.
- Document a fresh-session G0-G5 benchmark; software regressions do not replace native whole-board testing.

- Reconstruct one actual outline ring; reject gaps, branches, overlapping/self-intersecting and unsupported multi-ring outlines without bounding-box fallback.
- Enforce copper/drill edge clearances along full geometry, including concave notches and slot centrelines; distinguish omitted/empty coverage.
- Preserve per-element physical pad nets and reconcile every repeated-number land; reject ambiguous identities and conflicting net memberships.
- Bind imported and freshly executed reports to the same baseline and actual parsed input hashes; reject vacuous fitted-body checks and contradictory quote-row outcomes.

- Separate unplated layer copper from plated barrels, preserve explicit via spans and reject unsupported native hole/span encodings.
- Evaluate every physical land in logical-pin assertions; require actual plane reach for modeled plane assumptions.
- Compare protected route geometry to its baseline, preserving equivalent collinear segmentation and polygon ring ordering.
- Replace mask bounding-box/centre matching with supported opening-union coverage; expose partial-opening policy and reject empty/unsupported scopes.
- Reject misspelled, duplicate and invalid inspection options, weakened clearances and malformed physical geometry.

# v1.6.0 · 真实 EDA 受控写入 / Guarded live EDA writes

- 新增原生无连线原理图元件移动入口，支持写前碰撞、越界、源状态和字段检查。
- 正向写入与反向恢复保留完整可写属性；修复实测发现的仅传坐标导致扩展属性丢失问题。
- 新增逐步回读、保存重开验证、幂等操作 ID、日志锁和受控补偿；未知现场停止恢复。
- test1 实测通过合法移动、碰撞/越界拦截、保存重开及回滚后完整快照比对。
- 14 项新增自动化测试覆盖故障注入、自动补偿、并发改动阻断与重载差异；既有 52 项相邻测试复测。

Native movement now uses a typed Gateway entrypoint with preflight, full writable-property preservation, readback, save/reopen and guarded inverse operations. Native tests ran on test1; injected failure compensation was tested with mocks. Global interception of arbitrary calls, wired schematic edits and PCB routing rollback remain outside this release.

# v1.5.2 · 批次预检与修复反馈 / Batch preflight and repair feedback

## 中文

- 新增 G2-A 完整布局批次预检：读取新鲜源数据，计算所有目标对象和分区后的状态，检查几何及保护属性，再交给选定后端执行。
- 输出结构化修复报告：记录对象、预期值、实际值、失败检查及候选动作；身份、引脚、属性异常和重载失败不会直接生成移动指令。
- 新增持久化重试账本：阻止同计划与同适配器原样重试，识别重复失败，限制连续无进展，并支持幂等记录。
- 补充后端版本、原始观测和读回证据的对应要求；制造与供应信息保持可配置，不引入硬编码费用或库存门槛。
- 新增 11 项离线回归测试；复测相邻数据恢复和布局工具。更新中英文 README 与操作说明。

## English

- Add full-target G2-A layout batch preflight using fresh source data, geometry and protected properties before handoff to the selected backend.
- Emit structured repair evidence with expected/actual values, objects, failed checks and scoped proposals. Identity, pin/property and reload failures do not authorize movement.
- Add a persistent, idempotent attempt ledger that blocks unchanged retries, detects repeated failures and bounds unsuccessful attempts.
- Document adapter revisions, raw captures and native readback evidence. Keep manufacturing/supply policies configurable; add no hard-coded fees or stock threshold.
- Add 11 offline regression tests and rerun adjacent data/recovery and layout tests. Update both READMEs and the execution guide.

## 范围 / Scope

本版本支持已测量的无连线分区布局。它不拦截任意官方 API、不自动执行修复、不求解电气意图、不回滚实时 EDA；真实 EDA 采集、写入和保存重载仍需后端联调。测试使用合成数据，未验证实板或 Token 节省比例。

This release covers measured unwired block layouts. It does not intercept arbitrary official API calls, execute repairs, solve electrical intent or roll back live EDA. Native capture, application and save/reload still require backend integration. Tests use synthetic data; no hardware or token-saving benchmark is claimed.

# v1.5.1 · 数据核对、布局规划与操作恢复 / Data, layout and recovery

## 中文

- 增加两套 PCB 观测数据的器件与逐脚网络核对、摘要、分页查询和版本差异，保留完整原始输入。
- 增加完整关闭文件工程的隔离检查点与失败恢复，保留原工程和失败现场；验收后文件或证据变化时标记 STALE。
- 增加 G2-A 实测分区布局规划、写入前源数据核对、写入及重载后几何与属性对账。保留区内相对位置、两种原理图格式和无连线阶段。
- 补充官方 API 的布局执行流程、示例及中英文 README。
- 新增 27 项数据／恢复测试和 14 项布局测试通过；21 项既有 PCB 工具测试及导入器自检通过。

## English

- Reconcile components and pin nets across observed PCB models; query summaries, pages and revision deltas while retaining full inputs.
- Add isolated checkpoints and failure recovery for complete closed-file projects. Preserve the source and failed work; mark changed accepted files/evidence STALE.
- Add measured G2-A block planning, source preflight and post-apply/reload geometry and property comparison. Preserve local positions, both schematic formats and the unwired stage.
- Document native execution through the official API, with examples and updated English/Chinese READMEs.
- All 27 new data/recovery and 14 layout tests passed, along with 21 existing PCB toolkit tests and the importer self-test.

## 范围 / Scope

布局规划器处理已完成区内摆放的无连线功能块。EDA 写入和真实保存重载需通过选定后端执行与验证。未实现实时 EDA 自动回滚；本次未验证真实 EDA 全流程、macOS、实板或 Token 节省比例。

The planner packs locally arranged unwired blocks. Native application and actual save/reload require the selected backend and separate verification. Live EDA rollback is not implemented. No live EDA end-to-end, macOS, physical board or token-saving benchmark is claimed for this release.

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
