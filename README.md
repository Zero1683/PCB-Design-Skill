<p align="center">
  <img src="assets/logo.svg?v=2" width="156" height="156" alt="PCB Design to Bring-up logo">
</p>

<h1 align="center">PCB-Design-Skill</h1>

<p align="center"><strong>面向 AI Agent 的 PCB 工程 Skill</strong></p>
<p align="center">原理图设计 · PCB 布局布线 · 制造交付 · 实板调试</p>

<p align="center">
  <a href="https://github.com/Zero1683/PCB-Design-Skill/releases"><img src="https://img.shields.io/github/v/release/Zero1683/PCB-Design-Skill?style=flat-square&amp;label=release&amp;color=333333" alt="Latest release"></a>
  <a href="https://github.com/Zero1683/PCB-Design-Skill/stargazers"><img src="https://img.shields.io/github/stars/Zero1683/PCB-Design-Skill?style=flat-square&amp;color=333333" alt="GitHub stars"></a>
  <a href="https://github.com/Zero1683/PCB-Design-Skill/issues"><img src="https://img.shields.io/github/issues/Zero1683/PCB-Design-Skill?style=flat-square&amp;color=333333" alt="Open issues"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-333333?style=flat-square" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/EasyEDA-bundled-333333?style=flat-square" alt="EasyEDA tools bundled">
</p>

<p align="center"><a href="#近期更新">近期更新</a> · <a href="#内置第三方工具">第三方工具</a> · <a href="#安装">安装</a> · <a href="#核心能力">核心能力</a> · <a href="#使用示例">使用示例</a> · <a href="#文档索引">文档索引</a></p>
<p align="center"><strong>简体中文</strong> · <a href="README_EN.md">English</a></p>

---

将硬件需求转化为电路设计、PCB 工程与制造文件，提供封装核验、布局布线检查和首板调试流程。内置 EasyEDA API、原理图辅助方法库、本地桥接服务及运行依赖，支持在嘉立创EDA中执行工程操作。API 负责接口调用，辅助方法库提供功能分区、批量摆放、网络引出和修改清理流程。

## 近期更新

`main` 已包含 v1.6.0 之后的验收、几何检查和成本规划更新。**本轮软件回归 356 项通过，另完成 17 个工具自检。** 测试范围见[验证记录](VALIDATION.md)，逐版变化见[更新日志](CHANGELOG.md)。测试当前改进请下载 `main`；已发布的 Release 保留各自版本内容。

| 方向 | 当前能力 |
|---|---|
| 需求与元件预算 | 先梳理功能、接口和装配条件，再整理 BOM、查询立创商城报价；分别计算用量成本和计入起订量、包装倍数的实际采购金额 |
| 兼容替代料 | 按确认的需求逐项核对替代料，记录规格、数量、备料和报价变化；未经明确同意保留原有功能与性能 |
| 原理图绘制 | 限定自由分区、图框内分区两种格式；先检查无连线摆放，再连线；核对图纸边界、文字、引脚和功能分区 |
| 受控 EDA 操作 | 无连线原理图支持元件移动、写前拦截、逐步读回、保存重开和受控回滚；固定位置、允许区域、禁布区及限高可绑定到操作 |
| PCB 几何检查 | 检查板框闭合、凹口与槽孔边距、器件间距、同号多焊盘、镀孔属性和过孔层跨度；按修改前后的几何比较保护走线 |
| 制造文件检查 | 按支持的 Gerber 几何计算阻焊开窗并集，补查偏心开窗、组合开窗和宏定义；空数据及不支持的语义标为 `NOT_CHECKED` |
| 验收与证据 | 必检清单覆盖 G0–G9，检查项绑定需求、工程基线、实际输入与报告哈希；旧报告不能直接用于改动后的设计 |
| 数据读取与恢复 | 支持摘要、分页、差异和输出字节预算；保留完整源数据，阻止无变化的重复尝试，按已验证范围恢复检查点 |

项目报价属于只读查询。设计任务默认交付经过审查的 PCB 与制造文件，由用户自行下单。整板 G0–G5 流程、PCB 原生写入及布线回滚的验证范围见[新窗口实测指南](references/28-fresh-session-benchmark.md)。

## 内置第三方工具

完整目录随包提供以下 **4 套工具或方法库**。本项目负责设计流程和验收要求，工具负责相应的 EDA 操作、格式处理和独立检查。

| 项目 | 随包版本 / 快照 | 在本项目中的用途 |
|---|---|---|
| [easyeda-api-skill](https://github.com/easyeda/easyeda-api-skill) | 1.1.36 · `ccfaf28` | 官方 API 文档与经过本地修正的桥接运行时，默认通过 Run API Gateway 操作嘉立创EDA |
| [easyeda-enhanced-schematic-skill](https://github.com/easyeda/easyeda-enhanced-schematic-skill) | 1.2.0 · `0c4b9a0` | 官方原理图辅助方法：功能分区、批量摆放、选择性网络引出；目录名为 `easyeda-schematic-net-fanout` |
| [easyeda-pro-format-skill](https://github.com/easyeda/easyeda-pro-format-skill) | 1.0.0 · `bee647f` | 官方原生格式定义、示例及类型校验器；格式通过仍需核对原生导入和电气连接 |
| [pcb-skill](https://github.com/daishuge/pcb-skill) 的适配子集 | `6e939b6` | 社区 PCB 数据提取、布局和物理连接检查、制造文件检查及 DSN／SES 辅助；本地修复记录见 `vendor/pcb-skill-toolkit/UPSTREAM.md` |

桥接与格式校验所需的 **7 个运行依赖**也已附带：`ws 8.21.3`、`ajv 8.20.0`、`ajv-formats 2.1.1`、`fast-deep-equal 3.1.3`、`fast-uri 3.1.7`、`json-schema-traverse 1.0.0`、`require-from-string 2.0.2`。使用这些已打包的工具无需再执行 `npm install`。

**外部接入：** [easyeda-agent](https://github.com/zhoushoujianwork/easyeda-agent) 和 [easyeda-mcp-pro](https://github.com/oaslananka/easyeda-mcp-pro) 提供可选后端接入说明，源码、Connector 和服务未打包，也不会自动安装。它们属于社区项目。Node.js、Python、嘉立创EDA客户端、Run API Gateway、NumPy 和外部自动布线器均需按需另行准备。

版本、原始许可、实际文件位置及本地修改见[第三方组件清单](THIRD_PARTY_NOTICES.md)。表中列出的是本仓库保留的固定版本。

## 安装

测试当前改进可下载 [main 完整 ZIP](https://github.com/Zero1683/PCB-Design-Skill/archive/refs/heads/main.zip)，或克隆仓库：

```sh
git clone https://github.com/Zero1683/PCB-Design-Skill.git pcb-design-to-bringup
```

将完整目录放入客户端的 Skill 目录，或让 Agent 直接读取 [SKILL.md](SKILL.md)。目录中的 `references/`、`assets/` 和 `vendor/` 需一并保留。

**调用名称：** `$pcb-design-to-bringup`

已有 Git 副本可在保存本地改动后执行 `git pull --ff-only`。使用 ZIP 安装时，解压到新目录并将 Skill 指向完整新副本，再新开对话；不要只覆盖 `SKILL.md`。已发布版本可在 [Releases](https://github.com/Zero1683/PCB-Design-Skill/releases) 获取。正在运行的桥接进程按[更新指南](START_HERE.md#updating-an-existing-installation)处理。

### 连接嘉立创EDA

准备 Node.js 18+、支持扩展的嘉立创EDA桌面客户端，并在客户端安装、启用 **Run API Gateway**。进入本项目目录，启动桥接：

```sh
node scripts/easyeda_bridge.mjs start
```

Windows 可直接运行 `start-easyeda.cmd`。桥接所需的 `ws` 已内置，无需执行 `npm install`。完整配置见 [启动指南](START_HERE.md)。

| 状态 | 操作 |
|---|---|
| `BRIDGE_NOT_FOUND` | 启动桥接，检查日志和端口占用 |
| `WAITING_FOR_EDA` | 打开客户端，启用 Gateway 扩展 |
| `EDA_CONNECTED` | 核对目标窗口与工程，开始操作 |

Node.js、EDA 客户端和 Gateway 扩展需单独安装。Python 3.10+ 用于记录初始化、文件校验和辅助测试。

## 设计流程

设计任务默认交付完成布线、经过审查的 PCB 和制造文件，用户自行下单。选型可以查询手册、库存和价格；购买器件、加入购物车、提交订单和付款需要单独提出。

- **API 优先：** 内置 EasyEDA Skill 用于支持的工程创建和编辑操作。界面操作用于安装、视觉检查及明确的 API 缺口。
- **安装后验证：** 分别确认 Skill 已加载、Gateway 已连接、API 已响应。重启用于解决未刷新的技能列表等具体问题，不作为固定安装步骤。macOS 使用同一套 Node 启动器。
- **混合布线：** 先规划关键电源及敏感网络，合适的普通网络使用原生自动布线，保留已有走线并复查实际结果。
- **电气复核：** 计算功耗预算、损耗、直流通路压降和简化瞬态目标；受控阻抗使用实际叠层。需要用户操作计算器时，提供具体字段、数值、单位和返回要求。
- **电路复用与差异检查：** 记录模块接口和适用条件，用独立定义的引脚连接规则核对 EDA 实际导出数据，列出修改前后的器件及连接变化。
- **证据工具：** 校验检查记录、对照规范化原理图/PCB/BOM 数据、筛查器件外形重叠，配合原生 DRC 和视觉检查。

## EDA 操作基础

官方 API Skill 1.1.36、原理图辅助方法和官方格式 Skill 1.0.0 随包提供。在线操作优先使用 API；读取、生成或修复原生格式时使用文档类型明确的校验流程。设计顺序、电气复核、绘图规范与交付要求仍由本项目主流程决定。

社区 easyeda-agent 可作为结构化 CLI/Connector 后端；easyeda-mcp-pro 保留外部接入方式，当前审阅版本采用非商业许可，不并入本项目的 MIT 代码包。两者均不自动安装。详见 [操作后端与边界](references/16-easyeda-operation-backends.md) 和 [原生格式操作](references/17-easyeda-native-format.md)。

## 核心能力

| 模块 | 工作内容 |
|---|---|
| 电路设计 | 需求约束、供电预算、器件选型、引脚分配与原理图检查 |
| 封装核验 | 按完整型号核对数据手册、焊盘尺寸、脚号和装配方向 |
| 布局布线 | 器件间距、关键回路、差分信号、回流路径与地铜检查 |
| 制造交付 | Gerber、BOM、坐标和钢网文件的一致性检查与版本冻结 |
| 实板调试 | 断电测量、限流上电、复位与下载、接口及功能验证 |
| EDA 工具 | 内置 EasyEDA API Skill 1.1.36、原理图增强方法 1.2.0、格式 Skill 1.0.0 及桥接/校验运行依赖 |

工程流程也适用于其他 EDA；具体操作需使用对应软件的接口与检查工具。

## 独立 PCB 检查工具

内置经修正的社区 PCB 工具库，补充原生数据提取、器件实体与逃线空间筛查、
物理连接断言、Gerber／钻孔／阻焊检查，以及可选 DSN／SES 布线处理。
通过 `python scripts/pcb_toolkit.py --help` 查看入口。规则和层映射使用项目实际值，
不支持的文件语义会报错，缺失数据不能按检查通过处理。

工具不改变现有设计流程与通用性设置。详见[使用说明与覆盖范围](references/18-pcb-inspection-toolkit.md)。
多数工具仅需 Python 3.10+；栅格与铜间距检查还需 NumPy，未随包附带。

## 工程约束与计算

关键参数记录原厂依据、计算条件、EDA 规则和导出复核结果。补充密脚扇出、回流与热设计检查，提供阻焊开窗、阻焊桥、扇出通道和孔环余量计算。详见[工程约束](references/19-engineering-constraints.md)。

## 原理图布局规划

按实测元件与文字边界，将已安排好内部位置的功能块排列到指定页面。规划器保留区内相对位置和器件方向，输出固定的摆放坐标、分区框和标题范围。写入前核对源数据，写入及保存重载后分别对账，检测位置、参数、引脚和分区标注变化。支持两种原理图格式及 G2-A 无连线阶段；实际 EDA 操作由选定后端执行。见[布局执行指南](references/21-layout-execution.md)。

## 数据核对与操作恢复

提供两套 PCB 数据的器件与逐脚网络核对、摘要、分页查询和变更返回，完整原始数据保存在本地。完整文件工程可在隔离副本中执行分阶段操作；失败时核对版本、保留失败副本并恢复检查点。在线恢复已在 test1 的无连线原理图移动范围实测，其他操作需另行验证。见[使用说明](references/20-data-and-recovery.md)。

## 批次预检与修复反馈

在写入前检查完整的布局目标，并将读回差异整理为包含对象、预期值、实际值和候选动作的修复报告。重试账本阻止同计划与同适配器原样执行，识别重复失败，并限制连续无进展。引脚或属性异常先核对原因，保存重载失败先排查持久化。当前覆盖 G2-A 实测布局；工具不直接执行修复或拦截任意 EDA API。见[操作指南](references/22-batch-repair.md)。

## 使用示例

### 新建 PCB

```text
使用 $pcb-design-to-bringup 设计一块传感器板。
USB-C 供电，元件全部放在顶层，采用钢网和加热台装配。
先确定电源方案、器件选型和接口定义，再完成原理图与 PCB。
```

### 审查已有工程

```text
使用 $pcb-design-to-bringup 审查当前 PCB。
重点检查电源回路、USB 差分线、封装和装配间距。
保持工程只读，列出问题位置、判断依据和修改建议。
```

### 准备打板

```text
使用 $pcb-design-to-bringup 检查制造交付文件。
核对 Gerber、BOM、坐标文件与当前工程是否一致，
检查板框、钻孔、阻焊和钢网，并汇总尚未解决的问题。
```

## 工作流程

| 阶段 | 检查重点 |
|---|---|
| 需求与选型 | 供电、机械、接口、成本和装配条件 |
| 原理图与封装 | 先完成元件摆放和无连线检查，再连线；核验电气、排版、引脚和封装 |
| 布局与布线 | 实际器件外形、电源回路、信号完整性和连通性 |
| 制造与装配 | 文件版本、工艺参数、焊接方向与测试点 |
| 上电与验证 | 电压、电流、启动状态、通信和功能测试 |

各阶段记录检查条件、结果和待办项。封装以厂家尺寸图为依据，阻抗计算采用实际叠层与走线几何，API 修改后回读工程并复查。设计检查和实板测试分别记录。

## 文档索引

| 文档 | 内容 |
|---|---|
| [SKILL.md](SKILL.md) | Agent 入口、执行规则与阶段判据 |
| [启动指南](START_HERE.md) | 环境配置、桥接启动与连接诊断 |
| [电路与封装](references/02-circuit-and-library.md) | 器件选型、引脚和封装核验 |
| [原理图绘制规范](references/12-schematic-drafting.md) | 功能分区、两阶段绘制、连线和标注、示例图与验收证据 |
| [电路连接与复用](references/13-circuit-intent-and-reuse.md) | 引脚连接规则、模块复用条件、版本差异和原生工程回读 |
| [布局布线](references/03-layout-routing.md) | 布局、关键网络与地铜检查 |
| [制造与装配](references/04-release-assembly.md) | 制造发布、钢网与焊接 |
| [实板调试](references/05-bringup-debug.md) | 上电验证、测量与故障定位 |
| [EDA 操作](references/06-easyeda-execution.md) | API 调用、单位、状态与结果核对 |
| [原理图辅助方法](references/15-easyeda-schematic-methods.md) | 分区框、批量摆放、选择性网络引出、兼容探测和修改清理 |
| [记录模板](assets/) | PROJECT、CHECKS、HANDOFF |
| [电气计算](references/09-electrical-analysis.md) | 电源、压降、瞬态预算与阻抗复核 |
| [校验工具](references/10-validation-tools.md) | 证据与规范化导出数据格式 |
| [验证场景](references/11-validation-scenarios.md) | 行为评估与实际 EDA 操作验收 |
| [操作后端](references/16-easyeda-operation-backends.md) | 官方 API 与可选社区后端的选择和切换 |
| [原生格式](references/17-easyeda-native-format.md) | 原生格式输入、类型校验与导入边界 |
| [PCB 检查工具](references/18-pcb-inspection-toolkit.md) | 检查命令、覆盖范围与未支持的几何 |
| [工程约束](references/19-engineering-constraints.md) | 原厂依据、电气及工艺计算 |
| [数据与恢复](references/20-data-and-recovery.md) | 模型对账、分页读取与检查点恢复 |
| [布局执行](references/21-layout-execution.md) | 实测功能块规划与写入后核对 |
| [批次预检](references/22-batch-repair.md) | 批次预检、差异反馈与重试限制 |
| [实时写入](references/23-live-eda.md) | 原生移动、回读、保存重开和受控恢复 |
| [可执行约束](references/24-executable-constraints.md) | 位置、区域、禁布及高度约束 |
| [需求覆盖](references/25-requirement-coverage.md) | 需求与检查项、证据的对应关系 |
| [元件成本规划](references/26-component-cost-planning.md) | 元件报价、起订量及兼容替代料 |
| [当前设计证据](references/27-current-design-evidence.md) | 工程基线、源文件哈希与报告绑定 |
| [新窗口实测](references/28-fresh-session-benchmark.md) | 新任务整板实测与结果记录 |
| [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) | 来源、许可、版本与本地修改 |

核心 Skill 和工程参考采用英文，项目记录提供中英文模板；回复跟随用户语言。上游文档的集成勘误见第三方声明。

<details>
<summary><strong>辅助命令与运行配置</strong></summary>

查询连接状态：

```sh
node scripts/easyeda_bridge.mjs status
node scripts/easyeda_bridge.mjs doctor
```

桥接监听 `127.0.0.1`，使用 `49620` 至 `49629` 中的可用端口。日志默认保存在 `.runtime/`，可通过 `PCB_SKILL_STATE_DIR` 指定其他可写目录。桥接应保持本机访问。

初始化项目记录，输出目录需尚未创建：

```sh
python scripts/init_project.py --output /path/to/new-project --name MyPCB --lang zh
```

运行辅助测试，工作目录需存在且可写：

```sh
python -X utf8 scripts/test_helpers.py --workdir /path/to/workdir
```

校验全新解压的 Release ZIP：

```sh
python -X utf8 scripts/release_manifest.py verify --root /path/to/pcb-design-to-bringup
```

文件校验覆盖 SHA-256、缺失和新增文件。请使用独立解压副本，避免 `.git/` 和 `.runtime/` 被报告为新增内容。

</details>

## 验证状态

2026-09-22 的最新软件回归共 **356 项通过**，另有 **17 个工具自检通过，无跳过项**。其中包含 40 项路由物理测试、45 项阻焊几何测试、17 项连通性断言与入口测试；阻焊测试内部使用 1,000 组生成数据与独立数学结果对照。独立 CLI 审查发现的 4 个额外漏检已修复并复验关闭。

| 验证层级 | 当前证据 |
|---|---|
| 脚本与合成数据 | 几何、报告绑定、验收清单、成本、替代料和恢复回归通过；包含原生运行时模拟测试 |
| 原生 EDA 联调 | test1 已完成无连线原理图移动、碰撞及越界拦截、保存重开、定向修复与恢复验证 |
| 尚待实测 | 新窗口整板 G0–G5、macOS 全流程、外部布线器互操作及本轮改进后的实板制造验证 |

PCB 原生写入及布线回滚尚未实现。铺铜实体、钻孔空洞扣除、部分原生孔型编码和参数化 Gerber 宏等存在明确检查边界；详细限制见[检查工具说明](references/18-pcb-inspection-toolkit.md)。脚本通过只说明其已检查的范围，整板交付仍需原生检查与工程验收。

完整测试记录和历史版本结果见 [VALIDATION.md](VALIDATION.md)。

## 贡献

欢迎通过 [Issues](https://github.com/Zero1683/PCB-Design-Skill/issues) 提交问题，或通过 Pull Request 补充流程、文档和工具适配。问题报告请附软件版本、复现步骤及已去除敏感信息的日志；硬件相关问题请注明器件型号、板版本和测量条件。

## 许可

自有流程、模板和脚本采用 [MIT License](LICENSE)。内置组件保留原作者的许可与声明，详见 [第三方说明](THIRD_PARTY_NOTICES.md)。
