# easyeda-enhanced-schematic-skill

这是一个原理图增强Skill，依赖于[easyeda-api-skill](https://github.com/easyeda/easyeda-api-skill)使用。

## 功能演示

<img width="640" height="360" alt="Image" src="https://github.com/user-attachments/assets/34e1d764-5601-4f6c-b6db-317775c9b86c" />

[【立创开源硬件平台】EDA课程案例团队-AI远程调试器](https://oshwhub.com/course-examples/project_ddnrazxm)

## 前置要求

- 支持 SKILL 的 AI Agent工具
- [嘉立创EDA](https://lceda.cn/)
- 安装[run-api-gateway](https://jlc-ext.com/item/oshwhub/run-api-gateway)插件并开启外部交互全选
- 安装 [easyeda-api-skill](https://github.com/easyeda/easyeda-api-skill) 并与 [run-api-gateway](https://jlc-ext.com/item/oshwhub/run-api-gateway) 连接
- AI Agent先使用Plan模式构建完整项目计划后通过本SKILL完成原理图辅助绘制

## Skill 功能

1. **批量获取器件信息** — 通过 LCSC ID 调用 `lib_Device.getByLcscIds()`
2. **绘制模块框** — 彩色矩形框分组功能分区（USB、MCU、显示屏等）
3. **放置元件** — 在模块框内按可配置间距放置
4. **读取所有引脚位置** — 调用 `getAllPinsByPrimitiveId()`
5. **创建网络标记**（电源/地）和**网络端口**（信号）— 距每个引脚 10 单位
6. **连接** — 每个引脚到网络标签用短线连接

## 已测试的平台
  
| 平台 | 模型 |
|------|------|
| CodeX | gpt-5.6 |
| Hermes | glm-5.2 |
| Claude | opus-4.7 |
| OpenCode | mimo-v2.5-pro |
