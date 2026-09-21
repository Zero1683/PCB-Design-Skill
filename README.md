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

<p align="center"><a href="#近期更新">近期更新</a> · <a href="#安装">安装</a> · <a href="#核心能力">核心能力</a> · <a href="#使用示例">使用示例</a> · <a href="#文档索引">文档索引</a></p>
<p align="center"><strong>简体中文</strong> · <a href="README_EN.md">English</a></p>

---

将硬件需求转化为电路设计、PCB 工程与制造文件，提供封装核验、布局布线检查和首板调试流程。内置 EasyEDA API、原理图辅助方法库、本地桥接服务及运行依赖，支持在嘉立创EDA中执行工程操作。API 负责接口调用，辅助方法库提供功能分区、批量摆放、网络引出和修改清理流程。

## 近期更新

最近几轮更新覆盖绘图规范、EDA 操作、独立检查和失败恢复。**当前 `main` 已包含数据核对与操作恢复；最新 Release 仍为 v1.5.0。** 使用这些新增能力，请克隆或更新 `main`。

| 方向 | 已加入的内容 |
|---|---|
| 原理图绘制 | 限定自由分区和图框内分区两种格式；先检查无连线的元件摆放，再完成连线。补充边界、文字间距和常见排版问题的处理方法 |
| EDA 操作 | 内置官方 API、原理图辅助方法、原生格式文档与校验依赖；支持批量摆放、网络引出和明确的操作后端选择 |
| PCB 与制造检查 | 增加受支持原生数据提取、器件间距与逃线空间筛查、Gerber／钻孔／阻焊检查，以及 DSN／SES 布线辅助 |
| 电气与工艺计算 | 将原厂依据、计算条件、EDA 规则和导出复核绑定到同一版本；补充供电、回流、热设计、扇出通道、阻焊桥与孔环余量检查 |
| 数据读取 | 核对两套 PCB 数据中的器件与逐脚网络；提供摘要、分页查询和版本差异，保留完整原始输入，拒绝缺失或冲突记录 |
| 操作恢复 | 为关闭后的完整文件工程创建隔离副本和检查点；失败时保留现场并恢复候选副本。验收后文件或证据发生变化，状态标记为 `STALE` |

数据与恢复工具的入口、示例和适用范围见[操作指南](references/20-data-and-recovery.md)。完整变更见[更新记录](CHANGELOG.md)，测试结果见[验证记录](VALIDATION.md)。实时 EDA 自动回滚尚未实现，Token 节省比例尚未实测。

## 安装

下载 [最新发布包](https://github.com/Zero1683/PCB-Design-Skill/releases)，或克隆仓库：

```sh
git clone https://github.com/Zero1683/PCB-Design-Skill.git pcb-design-to-bringup
```

将完整目录放入客户端的 Skill 目录，或让 Agent 直接读取 [SKILL.md](SKILL.md)。目录中的 `references/`、`assets/` 和 `vendor/` 需一并保留。

**调用名称：** `$pcb-design-to-bringup`

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

## 数据核对与操作恢复

提供两套 PCB 数据的器件与逐脚网络核对、摘要、分页查询和变更返回，完整原始数据保存在本地。完整文件工程可在隔离副本中执行分阶段操作；失败时核对版本、保留失败副本并恢复检查点。在线 EDA 自动回滚仍需单独联调。见[使用说明](references/20-data-and-recovery.md)。

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

v1.5.0 发布前复测 81 项 Python 测试：80 项通过，1 项因 Windows 符号链接权限跳过。8 项 Node 格式校验测试及隔离的模拟桥接测试通过。集成时完成的 21 个工具自测另见[验证记录](VALIDATION.md)。

测试覆盖脚本和合成数据。新工具链的真实 EDA 工程全流程、macOS、外部布线器互操作及实板制造尚未验证。原生数据提取有格式边界；工具库板级模型与规范化快照可通过新适配器进行同一基线下的器件与逐脚核对；该适配器仍需真实工程验证。辅助检查不替代阻抗求解或实板验收。

当前 `main` 新增的 27 项数据与恢复测试全部通过；复测 21 项 PCB 工具测试及导入器自检通过。这些结果不计入上述 v1.5.0 测试数量。

完整更新内容见[更新记录](CHANGELOG.md)。

## 贡献

欢迎通过 [Issues](https://github.com/Zero1683/PCB-Design-Skill/issues) 提交问题，或通过 Pull Request 补充流程、文档和工具适配。问题报告请附软件版本、复现步骤及已去除敏感信息的日志；硬件相关问题请注明器件型号、板版本和测量条件。

## 许可

自有流程、模板和脚本采用 [MIT License](LICENSE)。内置组件保留原作者的许可与声明，详见 [第三方说明](THIRD_PARTY_NOTICES.md)。
