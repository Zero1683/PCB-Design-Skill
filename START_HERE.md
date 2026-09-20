# 开箱使用

本包包含 PCB 全流程 Skill、EasyEDA API Skill 1.1.28 的完整文档、桥接服务及 ws 运行依赖。不需要另装 easyeda-api Skill，也不需要 npm install 或重新生成文档。

## 首次使用

1. 将整个文件夹解压到工作盘，保留目录结构。Windows 建议放 D 盘；路径可以含中文和空格。
2. 电脑需已有 Node.js 18 或更高版本，以及支持扩展的嘉立创EDA桌面客户端。包内不含 Node.js 安装器或 EDA 客户端。
3. 在嘉立创EDA中安装并启用 **Run API Gateway** 扩展。原包未附带 `.eext`，本包也未伪造扩展；可在客户端扩展市场搜索该名称。上游提供的地址为 https://jlc-ext.com/item/oshwhub/run-api-gateway 。
4. Windows 双击 `start-easyeda.cmd`。其他系统或 AI 终端执行 `node scripts/easyeda_bridge.mjs start`，工作目录设为本文件夹。
5. `EDA_CONNECTED` 表示已连接；`WAITING_FOR_EDA` 表示桥接已启动，需打开客户端并启用扩展；`BRIDGE_NOT_FOUND` 表示未找到服务，检查输出中的日志路径和端口占用。
6. 在支持 Skill 的 AI 工具里注册本文件夹，使用 `$pcb-design-to-bringup` 开始任务。也可直接让 AI 读取本目录的 `SKILL.md`。不需要再加载一份外部 easyeda-api。

## 状态与文件

`node scripts/easyeda_bridge.mjs status` 只查询，不启动服务；`doctor` 同样输出 Node 版本、服务端口、连接与窗口状态。启动器只监听本机，复用已有桥接，不终止用户服务，不选择工程，不修改 PCB。

默认运行日志位于本包 `.runtime/`。可用 `PCB_SKILL_STATE_DIR` 指定有写权限的工作盘目录；文件夹只读时应设置它。校验发布包应在首次运行前进行，或将运行状态放到包外，避免生成日志被当成新增文件。

完整工具说明见 [EDA 执行](references/06-easyeda-execution.md)。第三方来源见 [第三方声明](THIRD_PARTY_NOTICES.md)。Python 仅供项目记录和发布校验脚本使用，不是桥接启动的必需依赖。
