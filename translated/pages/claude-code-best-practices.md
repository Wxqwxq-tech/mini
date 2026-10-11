Claude Code 概览 - Claude Code 文档

跳转到主要内容

Claude Code Docs home page[图: light logo][图: dark logo]

[图: US]

英语

搜索...

⌘K向 AI 提问

- Claude Developer Platform

- Claude Code on the Web

- 
网页版 Claude Code

搜索...

导航

入门

Claude Code 概览

入门

使用 Claude Code 构建

部署

管理

配置

参考

资源

##### 入门

- 

概览

- 

快速开始

- 

更新日志

##### 核心概念

- 

Claude Code 的工作原理

- 

扩展 Claude Code

- 

探索 .claude 目录

- 

探索上下文窗口

##### 使用 Claude Code

- 

存储指令和记忆

- 

权限模式

- 

常见工作流

- 

最佳实践

##### 平台与集成

- 

概览

- 

远程控制

- 
网页版 Claude Code

- 
桌面版 Claude Code

- 

Chrome 扩展（测试版）

- 

计算机使用（预览版）

- 

Visual Studio Code

- 

JetBrains IDEs

- 
代码评审与 CI/CD

- 

Slack 中的 Claude Code

本页内容

- 快速开始

- 你能做什么

- 随处使用 Claude Code

- 后续步骤

快速开始

# Claude Code 概览

复制本页

Claude Code 是一款智能体式编程工具，能够读取你的代码库、编辑文件、运行命令，并与你的开发工具集成。可在终端、IDE、桌面应用和浏览器中使用。

复制本页

Claude Code 是一款由 AI 驱动的编程助手，可帮助你构建功能、修复缺陷并自动化开发任务。它理解你的整个代码库，并能跨多个文件和工具协同工作以完成任务。

## 
​

快速开始

选择你的环境开始使用。大多数界面都需要 Claude 订阅或 Anthropic Console 账户。终端 CLI 和 VS Code 也支持第三方提供商。

- 
终端

- 
VS Code

- 
桌面应用

- 
网页

- 
JetBrains

功能齐全的 CLI，可直接在终端中使用 Claude Code。编辑文件、运行命令，并从命令行管理整个项目。要安装 Claude Code，请使用以下方法之一：

- 
原生安装（推荐）

- 
Homebrew

- 
WinGet

macOS、Linux、WSL：

```
curl -fsSL https://claude.ai/install.sh | bash

```

Windows PowerShell：

```
irm https://claude.ai/install.ps1 | iex

```

Windows CMD：

```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd

```

如果你看到 `The token '&&' is not a valid statement separator`，说明你当前在 PowerShell 中，而不是 CMD。请改用上面的 PowerShell 命令。当你处于 PowerShell 中时，提示符会显示 `PS C:\`。Windows 需要 Git for Windows。如果尚未安装，请先安装。

原生安装会在后台自动更新，让你始终保持在最新版本。

```
brew install --cask claude-code

```

Homebrew 安装不会自动更新。请定期运行 `brew upgrade claude-code` 以获取最新功能和安全性修复。

```
winget install Anthropic.ClaudeCode

```

WinGet 安装不会自动更新。请定期运行 `winget upgrade Anthropic.ClaudeCode` 以获取最新功能和安全性修复。

然后在任意项目中启动 Claude Code：

```
cd your-project
claude

```

首次使用时系统会提示你登录。就这么简单！继续阅读 Quickstart →

有关安装选项、手动更新或卸载说明，请参阅高级设置。如遇到问题，请访问故障排查。

VS Code 扩展直接在编辑器中提供内联差异、@ 提及、计划评审和对话历史。

- 为 VS Code 安装

- 为 Cursor 安装

或者，在扩展视图（Mac 上为 `Cmd+Shift+X`，Windows/Linux 上为 `Ctrl+Shift+X`）中搜索“Claude Code”。安装后，打开命令面板（`Cmd+Shift+P` / `Ctrl+Shift+P`），输入“Claude Code”，然后选择“在新标签页中打开”。开始使用 VS Code →

一个独立应用，用于在 IDE 或终端之外运行 Claude Code。以可视化方式评审差异、并行运行多个会话、安排定期任务，并启动云端会话。下载并安装：

- macOS（Intel 和 Apple Silicon）

- Windows（x64）

- Windows ARM64（仅限远程会话）

安装后，启动 Claude，登录并点击 Code 标签页开始编程。需要使用付费订阅。了解桌面应用详情 →

无需本地设置，即可在浏览器中运行 Claude Code。启动长时间运行的任务并在完成后回来查看，处理你本地没有的仓库，或并行运行多个任务。支持桌面浏览器和 Claude iOS 应用。在 claude.ai/code 开始编程。开始在网页上使用 →

一款适用于 IntelliJ IDEA、PyCharm、WebStorm 及其他 JetBrains IDE 的插件，支持交互式差异查看和选择上下文共享。从 JetBrains Marketplace 安装 Claude Code 插件，然后重启 IDE。开始使用 JetBrains →

## 
​

你能做什么

以下是使用 Claude Code 的一些方式：

自动化你一直拖延的工作

Claude Code 可以处理那些耗费你时间的繁琐任务：为未经测试的代码编写测试、修复整个项目中的静态检查错误、解决合并冲突、更新依赖以及编写发布说明。

```
claude "write tests for the auth module, run them, and fix any failures"

```

构建功能并修复缺陷

用通俗的语言描述你想要什么。Claude Code 会规划方案、跨多个文件编写代码并验证其是否可用。对于缺陷，请粘贴错误信息或描述症状。Claude Code 会在你的代码库中追踪问题、定位根因并实施修复。更多示例请参阅常见工作流。

创建提交和拉取请求

Claude Code 直接与 git 协作。它可以暂存更改、编写提交信息、创建分支并打开拉取请求。

```
claude "commit my changes with a descriptive message"

```

在 CI 中，你可以使用 GitHub Actions 或 GitLab CI/CD 自动化代码评审和议题分诊。

通过 MCP 连接你的工具

模型上下文协议（MCP）是一种开放标准，用于将 AI 工具连接到外部数据源。借助 MCP，Claude Code 可以读取 Google Drive 中的设计文档、更新 Jira 中的工单、从 Slack 拉取数据，或使用你自己的自定义工具。

通过指令、技能和钩子进行自定义

`CLAUDE.md` 是一个 Markdown 文件，你将其添加到项目根目录，Claude Code 会在每次会话开始时读取它。你可以用它设置编码规范、架构决策、首选库和评审清单。Claude 在工作过程中还会构建自动记忆，跨会话保存构建命令、调试洞察等经验，无需你编写任何内容。创建自定义命令来打包团队可共享的可复用工作流，例如 `/review-pr` 或 `/deploy-staging`。钩子允许你在 Claude Code 操作之前或之后运行 shell 命令，例如在每次文件编辑后自动格式化，或在提交前运行静态检查。

运行智能体团队并构建自定义智能体

同时派生多个 Claude Code 智能体，分别处理任务的不同部分。一个主导智能体负责协调工作、分配子任务并合并结果。对于完全自定义的工作流，Agent SDK 允许你借助 Claude Code 的工具和能力构建自己的智能体，并完全掌控编排、工具访问和权限。

使用 CLI 进行管道、脚本化和自动化

Claude Code 具有可组合性，并遵循 Unix 哲学。你可以将日志管道传入它、在 CI 中运行它，或将它与其他工具串联：

```
# Analyze recent log output
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# Automate translations in CI
claude -p "translate new strings into French and raise a PR for review"

# Bulk operations across files
git diff main --name-only | claude -p "review these changed files for security issues"

```

有关完整的命令和标志集，请参阅 CLI 参考。

安排定期任务

按计划运行 Claude，以自动化重复性工作：早间 PR 评审、隔夜 CI 失败分析、每周依赖审计，或在 PR 合并后同步文档。

- 云端计划任务运行在 Anthropic 管理的基础设施上，因此即使你的计算机关机也能继续运行。可以从网页、桌面应用或通过在 CLI 中运行 `/schedule` 来创建它们。

- 桌面计划任务在你的机器上运行，可直接访问本地文件和工具

- `/loop` 在 CLI 会话内重复一个提示词以进行快速轮询

随时随地工作

会话不局限于单一界面。随着你的上下文变化，可在不同环境之间迁移工作：

- 离开办公桌，通过远程控制从手机或任意浏览器继续工作

- 通过 Message Dispatch 从手机派发任务，并打开它所创建的桌面会话

- 在网页或 iOS 应用上启动长时间运行的任务，然后用 `claude --teleport` 将其拉取到你的终端

- 使用 `/desktop` 将终端会话移交到桌面应用，以进行可视化差异评审

- 从团队聊天中转接任务：在 Slack 中提及 `@Claude` 并附上缺陷报告，即可获得拉取请求

## 
​

随处使用 Claude Code

每个界面都连接到同一个底层 Claude Code 引擎，因此你的 CLAUDE.md 文件、设置和 MCP 服务器可以在所有界面中正常工作。
除上述终端、VS Code、JetBrains、桌面和网页环境外，Claude Code 还可与 CI/CD、聊天和浏览器工作流集成：

我想要……最佳选择

从我的手机或其他设备继续本地会话 远程控制

将来自 Telegram、Discord、iMessage 或我自己 webhook 的事件推送到会话中 频道

在本地启动任务，在移动端继续 网页或 Claude iOS 应用

按定期计划运行 Claude 云端计划任务或桌面计划任务

自动化 PR 评审和议题分诊 GitHub Actions 或 GitLab CI/CD

在每个 PR 上自动进行代码评审 GitHub Code Review

将 Slack 中的缺陷报告转接为拉取请求 Slack

调试线上 Web 应用 Chrome

为你的工作流构建自定义智能体 Agent SDK

## 
​

后续步骤

安装 Claude Code 后，以下指南可帮助你深入了解。

- 快速开始：完成你的第一个真实任务，从探索代码库到提交修复

- 存储指令和记忆：通过 CLAUDE.md 文件和自动记忆为 Claude 提供持久化指令

- 常见工作流和最佳实践：充分利用 Claude Code 的模式

- 设置：针对你的工作流自定义 Claude Code

- 故障排查：常见问题的解决方案

- code.claude.com：演示、定价和产品详情

本页是否有帮助？

是否

快速开始

⌘I

Claude Code Docs home page[图: light logo][图: dark logo]

xlinkedin

公司
Anthropic招聘经济未来研究新闻信任中心透明度

帮助与安全
可用性状态支持中心

学习
课程MCP 连接器客户案例工程博客活动由 Claude 提供支持服务合作伙伴初创计划

条款与政策
隐私选项隐私政策披露政策使用政策商业条款消费者条款

助手

回复由 AI 生成，可能包含错误。