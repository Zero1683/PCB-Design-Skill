# PCB Design to Bring-up

**从需求到实板验证的 AI PCB 工程 Skill · An AI skill for PCB design, manufacturing handoff, and board bring-up**

[中文](#中文) · [English](#english)

## 中文

把选型、原理图、封装、布局布线、制造交付和首板调试整理成一套可执行、可交接的流程。让没有项目历史的 AI 能从工程记录继续工作，并区分“设计检查通过”和“实板已经验证”。

本仓库提供的是 **AI 工作流程、文档和工具**，不是自动布线器，也不保证未经实测的设计一次打板成功。

### 包含什么

- **完整 PCB 工作流程**：需求与基线 → 架构与选型 → 原理图与封装 → 布局 → 布线与地铜 → 制造发布 → 装配 → 上电与下载 → 功能验证 → 交接。
- **内置 EasyEDA API Skill 1.1.28**：API、枚举、接口、源文件格式与扩展开发文档，以及本地桥接服务。
- **离线运行依赖**：附带桥接所需的 `ws`，无需另装 easyeda-api 或运行 `npm install`。
- **启动和诊断入口**：检查端口、复用已有服务、报告 EDA 连接与窗口状态。
- **项目模板与发布校验**：需求记录、检查表、交接文档，以及文件 SHA-256 清单工具。

### 环境要求

| 用途 | 要求 |
|---|---|
| 阅读与使用工程流程 | 能读取 `SKILL.md` 的 AI 工具 |
| 在线操作嘉立创EDA | Node.js 18+、支持扩展的桌面客户端、已安装并启用 Run API Gateway |
| 初始化记录、校验发布文件、运行辅助测试 | Python 3.10+ |
| 其他 EDA | 使用其原生接口和检查工具；本包只内置 EasyEDA 适配 |

Node.js、EDA 客户端和 Gateway 扩展不包含在下载包中。可在客户端扩展市场搜索 **Run API Gateway**；参见 [首次使用说明](START_HERE.md)。桥接依赖已内置不代表 EDA 扩展已安装。

### 快速开始

1. 从 [Releases](https://github.com/Zero1683/pcb-design-to-bringup/releases) 下载发布 ZIP，解压并保留目录结构。也可克隆整个仓库。
2. 将文件夹注册到 AI 工具的 Skill 目录，或直接让 AI 读取根目录 `SKILL.md`。只需注册本 Skill，无需再安装同名 EasyEDA 工具包。
3. 打开嘉立创EDA并启用 Gateway。在本目录执行：

```sh
node scripts/easyeda_bridge.mjs start
```

Windows 也可双击 `start-easyeda.cmd`。只读查询状态：

```sh
node scripts/easyeda_bridge.mjs status
node scripts/easyeda_bridge.mjs doctor
```

| 状态 | 含义与下一步 |
|---|---|
| `BRIDGE_NOT_FOUND` | 未找到桥接；执行 `start`，启动失败时查看日志与端口占用 |
| `WAITING_FOR_EDA` | 桥接已启动；打开客户端并启用 Gateway |
| `EDA_CONNECTED` | 客户端已连接；执行操作前仍需核对目标窗口、工程和文档 |

桥接绑定 `127.0.0.1`，在 `49620–49629` 中选可用端口。不要把它暴露到公网。默认日志写入 `.runtime/`；可通过 `PCB_SKILL_STATE_DIR` 指定包外工作目录。启动器不会自动选择工程或修改 PCB。

### 如何交给 AI

```text
使用 $pcb-design-to-bringup。
根据我的功能需求与制造条件完成 PCB 设计。
先读取已有工程和交接记录，核对器件手册与封装，
对布局、布线、制造文件和实板测试分别保留证据。
未经验证的项目标为未验证，不要仅凭 DRC 就宣布整板可用。
```

已有板子也可以只要求审查，例如：“只读检查 USB 与电源区域，不改动工程，列出证据和待核实项。”适用阶段由任务决定，不必从头重复所有流程。

### 工程约束

- 用确切型号的数据手册核对引脚与封装；库名、推荐标签和 3D 外观不能替代尺寸证据。
- 用旋转后的真实器件、焊盘和插拔空间检查布局，不能只看元件中心或 DRC 数量。
- 阻抗对应实际叠层和几何；不把变化的铜间距取平均后当作全线验证。
- API 返回成功后仍需重读结果；必要时重新铺铜、检查连通性并查看实际画面。
- 隐藏焊点需要可接触的等效测试点；记录供电、复位、启动、下载和功能测试条件。
- 项目尺寸、层数、铜厚、接口和装配方式由需求决定，案例参数不是默认设计规则。

### 目录与验证

```text
SKILL.md                  AI 入口与阶段判据
START_HERE.md             首次安装与启动
references/              分阶段工程流程、排故与经验
assets/                  PROJECT / CHECKS / HANDOFF 模板
scripts/                 桥接启动、记录初始化、发布校验
vendor/easyeda-api/       内置上游文档、桥接与 ws
agents/openai.yaml       Skill 显示信息
THIRD_PARTY_NOTICES.md    第三方来源与许可说明
```

初始化一个**尚不存在**的项目目录：

```sh
python scripts/init_project.py --output /path/to/new-project --name MyPCB
```

运行辅助脚本测试，`--workdir` 指定已有、可写的临时工作目录：

```sh
python -X utf8 scripts/test_helpers.py --workdir /path/to/workdir
```

校验 **Release ZIP 全新解压目录**中的文件清单：

```sh
python -X utf8 scripts/release_manifest.py verify --root /path/to/pcb-design-to-bringup
```

清单检查文件完整性，不检查电气正确性。它采用严格清单，Git 克隆产生的 `.git/`、启动后产生的 `.runtime/` 等额外文件不属于发布包；请使用全新解压副本进行发布校验。

已验证独立解压、中文及空格路径、内置依赖加载、桥接启动与重复启动复用，并通过 11 项辅助脚本测试。桥接测试到 `WAITING_FOR_EDA`；**本包尚未以连接中的 EDA 工程验证完整设计流程**。实际工程和实板仍需逐阶段验证。

### 许可与反馈

本项目自有流程、模板和脚本采用 [MIT](LICENSE)。第三方内容保留原作者声明及许可，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。问题和改进建议可提交到 [Issues](https://github.com/Zero1683/pcb-design-to-bringup/issues)，请附复现步骤、工具版本及去除敏感信息后的错误输出。

## English

A reusable workflow for component selection, schematics, footprints, placement, routing, manufacturing handoff, assembly, and first-board debugging. It helps an AI without project history resume from explicit records and distinguish **design review** from **verified hardware behavior**.

This repository contains **AI instructions, documentation, and helper tools**. It is not an autorouter and does not guarantee a successful first fabrication without hardware testing.

### Included

- **End-to-end workflow:** requirements and baseline → architecture and parts → schematics and footprints → placement → routing and ground → manufacturing release → assembly → power-up and programming → functional verification → handoff.
- **Bundled EasyEDA API Skill 1.1.28:** API, enum, interface, source-format, and extension-development references, plus the local bridge server.
- **Offline bridge dependency:** `ws` is included. No separate easyeda-api installation or `npm install` is needed.
- **Startup and diagnostics:** discover ports, reuse an existing bridge, and report desktop/window connectivity.
- **Project templates and release checks:** requirements, check records, handoff notes, and SHA-256 file manifests.

### Requirements

| Use | Requirement |
|---|---|
| Engineering workflow | An AI tool that can read `SKILL.md` |
| Live EasyEDA operations | Node.js 18+, an extension-capable desktop client, and Run API Gateway installed and enabled |
| Record initialization, manifest checks, helper tests | Python 3.10+ |
| Other EDA tools | Their native interfaces and checks; only the EasyEDA adapter is bundled |

Node.js, the desktop client, and the Gateway extension are **not bundled**. Search the client's extension marketplace for **Run API Gateway**. Bundled bridge dependencies do not install the desktop extension.

### Quick start

1. Download and extract the ZIP from [Releases](https://github.com/Zero1683/pcb-design-to-bringup/releases), preserving the folder structure, or clone this repository.
2. Register the folder in your AI tool's skill directory, or ask the AI to read the root `SKILL.md`. There is no separate EasyEDA skill to install.
3. Open EasyEDA, enable the Gateway extension, and run this from the skill folder:

```sh
node scripts/easyeda_bridge.mjs start
```

On Windows, double-click `start-easyeda.cmd`. Read-only diagnostics:

```sh
node scripts/easyeda_bridge.mjs status
node scripts/easyeda_bridge.mjs doctor
```

| Status | Meaning and next step |
|---|---|
| `BRIDGE_NOT_FOUND` | No bridge found; run `start`, then inspect logs and occupied ports if startup fails |
| `WAITING_FOR_EDA` | Bridge running; open the desktop client and enable Gateway |
| `EDA_CONNECTED` | Client connected; still verify the target window, project, and document before any operation |

The bridge binds to `127.0.0.1` and selects an available port in `49620–49629`. Do not expose it to the public Internet. Logs default to `.runtime/`; set `PCB_SKILL_STATE_DIR` to use a writable directory outside the package. The launcher does not select a project or modify a PCB.

### Example prompt

```text
Use $pcb-design-to-bringup to design a PCB from my functional and manufacturing requirements.
Read the existing project and handoff records first. Verify datasheets and footprints,
and keep separate evidence for placement, routing, manufacturing files, and hardware tests.
Mark untested items as unverified; do not declare the board functional solely from DRC.
```

For an existing board, you can request a narrower task: “Review the USB and power sections without modifying the project. List evidence and unresolved checks.” Start at the relevant stage instead of repeating completed work.

### Engineering principles

- Match pinouts and footprints to the exact manufacturer part; library labels and 3D appearance do not replace dimensional evidence.
- Check rotated component outlines, pads, and connector clearance, not just centers or DRC counts.
- Evaluate impedance against the real stackup and geometry; averaging varying copper clearances does not validate the entire route.
- Re-read edits after API success; rebuild copper, check connectivity, and inspect the actual view as needed.
- Provide accessible test points for hidden joints and record power, reset, boot, programming, and functional test conditions.
- Derive dimensions, layers, copper weight, interfaces, and assembly constraints from requirements; example values are not universal rules.

### Files and verification

`SKILL.md` is the AI entry point. `references/` contains stage-specific procedures; `assets/` contains project/check/handoff templates; `scripts/` contains the launcher and helpers; `vendor/easyeda-api/` contains the upstream tool package and its runtime dependency. Detailed engineering instructions are primarily Chinese; this README is bilingual and upstream API references retain their original language.

Initialize a project in a directory that **does not yet exist**:

```sh
python scripts/init_project.py --output /path/to/new-project --name MyPCB
```

Run helper tests using an existing writable scratch directory:

```sh
python -X utf8 scripts/test_helpers.py --workdir /path/to/workdir
```

Verify a **freshly extracted Release ZIP**:

```sh
python -X utf8 scripts/release_manifest.py verify --root /path/to/pcb-design-to-bringup
```

The strict manifest checks file integrity, not electrical correctness. Extra files such as a clone's `.git/` directory or startup logs in `.runtime/` are outside the release manifest; use a fresh archive extraction for this check.

Independent extraction, paths containing Chinese characters/spaces, bundled dependency loading, bridge startup, and repeated-start reuse have been tested. All 11 helper tests passed. Bridge verification reached `WAITING_FOR_EDA`; **the complete workflow has not been validated against a connected EDA project in this package's release test**. Each actual design and assembled board still needs its own staged verification.

### License and feedback

Original workflow content, templates, and scripts use the [MIT License](LICENSE). Bundled third-party material retains its original notices and licenses; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Report problems or suggestions through [Issues](https://github.com/Zero1683/pcb-design-to-bringup/issues), with reproduction steps, tool versions, and sanitized error output.
