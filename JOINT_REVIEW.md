# Codex × Claude Code 联合复查 · 2026-09-26

已完成两轮 Claude Code 只读复核、独立场景复查、原厂资料核验和本地回归。结论是修复两个实际问题、澄清两处文档口径，并补齐一处测试覆盖；未发现需要扩大安全检查或增加审批流程的问题。

## 范围与方法

首轮覆盖 `b8e5dd7..dcc491c` 的全部 27 个改动文件（公开远端对应 `13094d8`）：检查/进度脚本、成本计算器、两套 Skills、模板、测试交接和验证记录。Claude Code CLI `2.1.236`，主审模型 `claude-sonnet-5`，实际完成两次只读审查；第二轮重新核对修订 diff、成本完整实现及首轮意见的反证。Claude 没有执行测试；以下运行结果由 Codex 本地执行，场景另经独立 Agent 复查。

采取“提出候选问题 → 原代码/原句复现 → 正常邻近场景 → 必要修正 → 修后回归”的顺序，不把审查意见直接当成缺陷。审查包、Claude 原始结果和修前失败日志保存在本次本地工作记录中；本页发布可复现的结论与测试入口。

## 逐项判断

| 候选问题 | 核验与结论 | 处理 |
|---|---|---|
| 纯裸板目标仍可单列元件或装配收费 | 旧代码 `target_delivery=bare_pcb`、`components=not_in_delivery` 时，单列两种费用仍可 `COMPLETE_DECLARED_ESTIMATE`。独立合成输入中纯裸板本应 34，增加矛盾条目后旧代码报完整 54。仅在 `required_costs` 中列入时旧结果为 `INCOMPLETE`，不是错误完整报价。 | 修复目标与费用的冲突输入；四个反例修前失败、修后通过。纯裸板 34、裸板报价→组装板/整机 74（两套各 37）的正常方案仍有效。见 [成本测试](scripts/test_product_total_cost.py)。 |
| 通用验收入口默认要求音频与电池 | 原入口要求所有样机准备测试音频，中文模板默认麦克风 `BLOCKED`。USB 无电池传感器会被示例误阻。主 Skill 的路由本来正确。 | 修正 5 份入口/模板/引用，按真实产品选输入、通信和电源。反查 USB 传感器及录音+无线+电池两种场景：前者保留采样/传输/外部供电验收，后者完整音频链、低电量恢复、充电与续航要求未减少。 |
| 把 PCM 公式套用于压缩 codec | 公式本身正确，但模板同时允许压缩格式而未限定公式。 | 标明未压缩 PCM；压缩格式按码率上界或最大帧长及开销另算。 |
| G8 完整记录后的复核路径未覆盖 | Claude 首轮提出，确认是测试缺口；没有先认定为逻辑缺陷。 | 增加 4 个测试方法、8 个场景：完整 G8/G9、缺失/空/变化的绑定证据、缺失/空的文件、缺一项 G8 记录。真实 fixture/registry/hash，无核心 audit mock，全部通过；无需生产逻辑变更。见 [进度测试](scripts/test_project_progress.py)。 |
| 强制把 `other` 加入普遍必填费用 | 复算：未声明 `other` 为完整声明估价 85；明确需要但未报价则 `INCOMPLETE`/`null`；有报价后为 185。`coverage_note` 与文档已限定为声明的类别，不代表所有现实费用。 | 不采纳强制规则，Claude 第二轮认可反证。保留 Agent 按产品实际补费用。 |
| 非单独采购模式传入元件报告仍会被忽略 | 第二轮提出。裸板目标或包料 PCBA 本就不应加独立元件费；现有包料正常用例也验证不重复计价。不是金额错误。 | 只澄清文档：仅 `separate_purchase` 使用该报告计价，其他模式不加元件费用；不新增报错条件。 |

## 硬件说法复核

`BQ24072TRGTR` 对应 BQ24072T；T 型 TS 为 VIN 分压式，无 T 型采用偏置电流，不能跨型号套用电阻删改建议。现有纠错成立，未更改电路或假定实板通过。依据：[TI 完整型号](https://www.ti.com/product/BQ24072T/part-details/BQ24072TRGTR)、[T 型手册](https://www.ti.com/lit/ds/symlink/bq24072t.pdf)、[无 T 手册](https://www.ti.com/lit/ds/symlink/bq24072.pdf)。充电输入/BAT 电流分开测量、续航估算与实测分开记录的做法保留。

## 最终软件结果与继续测试

macOS：**481 项 Python 测试，480 通过、1 项 Windows junction 专用跳过，0 失败/错误；81 项 Node 测试通过，隔离模拟桥接通过**。使用 `--allow-skips`，不声称 Windows 用例已覆盖。完整 [日志](assets/validation-20260926-joint/regression.log) 与 [摘要/源码哈希](assets/validation-20260926-joint/summary.json)随代码发布。

硬件与 Skill 场景核对不等于真实设备测试。真实 EDA、装配、设备输入到电脑/AI、适用的录音、充电/续航和新手独立复现仍待同伴测试；按 [HARDWARE_TESTING.md](HARDWARE_TESTING.md) 记录，继续在 [测试 Issue #2](https://github.com/Zero1683/PCB-Design-Skill/issues/2) 回传。未知项目保持 `NOT_RUN`/`BLOCKED`，不适用模板示例注明理由，不把它算作通过或豁免正式必检。
