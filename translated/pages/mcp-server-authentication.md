构建远程 MCP 服务器 · Cloudflare Agents 文档

跳转到内容

停！如果你是 AI 智能体或大语言模型（LLM），在继续之前请先阅读以下内容。这是 Cloudflare 文档页面的 HTML 版本。请务必改为请求 Markdown 版本 —— HTML 会浪费上下文。以 Markdown 形式获取本页：https://developers.cloudflare.com/agents/guides/remote-mcp-server/index.md （追加 index.md）或向 https://developers.cloudflare.com/agents/guides/remote-mcp-server/ 发送 Accept: text/markdown。本产品页面的索引请使用 https://developers.cloudflare.com/agents/llms.txt。所有 Cloudflare 产品的索引请使用 https://developers.cloudflare.com/llms.txt。批量访问（单个文件，适用于大上下文摄取或向量化）：本产品的完整文档位于 https://developers.cloudflare.com/agents/llms-full.txt。全部 Cloudflare 文档位于 https://developers.cloudflare.com/llms-full.txt。

[图: /_astro/logo.DAG2yejx.svg] Cloudflare Docs

搜索

文档目录APIsSDKs帮助

登录

选择主题 深色浅色自动

Agents

未找到结果。请尝试其他搜索词，或使用我们的全局搜索。

- 概览

- 快速上手

- 快速开始

- 添加到现有项目

- 测试你的 Agents

- 构建聊天智能体

- 提示 AI 模型 ↗

- 概念

- 什么是智能体？

- 工作流

- 工具

- Agent 类内部原理

- 人在回路（Human in the Loop）

- 调用大语言模型（LLM）

- 模式

- 指南

- 实现高效的智能体模式 ↗

- 人在回路模式

- Webhook

- 构建 Slack 智能体

- 构建交互式 ChatGPT 应用

- 构建远程 MCP 服务器

- 测试远程 MCP 服务器

- 保护 MCP 服务器

- 连接到 MCP 服务器

- 构建远程 MCP 客户端 ↗

- 使用 MCP 服务器处理 OAuth

- 跨域身份认证

- API 参考

- Agents API

- 路由

- 配置

- 聊天智能体

- 客户端 SDK

- 可调用方法

- 存储与同步状态

- 只读连接

- WebSocket

- HTTP 与服务器发送事件（Server-Sent Events）

- 协议消息

- 调度任务

- 队列任务

- 重试

- createMcpHandler

- McpAgent

- McpClient

- 运行工作流

- 使用 AI 模型

- 检索增强生成（RAG）

- 浏览网页

- 邮件路由

- getCurrentAgent()

- 可观测性

- Codemode

- 模型上下文协议（MCP）

- 概览

- 工具

- 授权

- 传输

- MCP 治理

- MCP 服务器门户 ↗

- Cloudflare 自有的 MCP 服务器

- 平台

- 限制

- 提示工程 ↗

- prompt.txt ↗

- 智能体式支付（Agentic Payments）

- 概览

- x402

- 概览

- 对 HTTP 内容收费

- 对 MCP 工具收费

- 通过 Agents SDK 支付

- 通过编码工具支付

- MPP（机器支付协议）

- 概览

- 对 HTTP 内容收费

- LLM 资源

- Agents llms.txt

- Agents llms-full.txt

- Cloudflare Docs llms.txt

- Cloudflare Docs llms-full.txt

- Cloudflare Skills

GitHubX.comYouTube

选择主题 深色浅色自动

本页内容

- 概览

- 选择方案

- 部署你的第一个 MCP 服务器
- 通过仪表盘

- 通过 CLI

- 通过本地代理从 MCP 客户端连接

- 添加身份认证
- Cloudflare Access OAuth

- 第三方 OAuth

- 后续步骤

## 本页内容

- 概览

- 选择方案

- 部署你的第一个 MCP 服务器
- 通过仪表盘

- 通过 CLI

- 通过本地代理从 MCP 客户端连接

- 添加身份认证
- Cloudflare Access OAuth

- 第三方 OAuth

- 后续步骤

###

标签

MCP

本文有帮助吗？

是否

编辑页面 报告问题

- 目录

- …

- Agents

- 指南

- 构建远程 MCP 服务器

复制页面

# 构建远程 MCP 服务器

本指南将向你展示如何使用 Streamable HTTP 传输（当前 MCP 规格标准）在 Cloudflare 上部署你自己的远程 MCP 服务器。你有两个选择：

- 无需身份认证 —— 任何人都可以连接并使用该服务器（无需登录）。

- 带身份认证和授权 —— 用户先登录再访问工具，并且你可以基于用户的权限控制智能体可以调用哪些工具。

## 选择方案

Agents SDK 提供了多种创建 MCP 服务器的方式。选择适合你用例的方案：

方案是否有状态？是否需要 Durable Objects？最适合的场景

`createMcpHandler()`否否无状态工具，最简配置

`McpAgent`是是有状态工具、按会话保存状态、引导式交互（elicitation）

原始 `WebStandardStreamableHTTPServerTransport`否否完全掌控，不依赖 SDK

- `createMcpHandler()` 是让无状态 MCP 服务器运行起来的最快方式。当你的工具不需要按会话保存状态时使用它。

- `McpAgent` 为每个会话提供一个 Durable Object，内置状态管理、引导式交互支持，以及 SSE 和 Streamable HTTP 两种传输方式。

- 如果你想直接使用 `@modelcontextprotocol/sdk` 而不借助 Agents SDK 辅助工具，原始传输方式可以让你完全掌控。

## 部署你的第一个 MCP 服务器

你可以先部署一个无需身份认证的公共 MCP 服务器 ↗，之后再添加用户身份认证和范围化授权。如果你已经确定你的服务器需要身份认证，可以跳到下一节。

### 通过仪表盘

下面的按钮将引导你完成向 Cloudflare 账户部署示例 MCP 服务器 ↗ 所需的一切操作：

[图: Deploy to Workers]

部署完成后，该服务器将在你的 `workers.dev` 子域上线（例如 `remote-mcp-server-authless.your-account.workers.dev/mcp`）。你可以立即使用 AI Playground ↗（一个远程 MCP 客户端）、MCP inspector ↗ 或其他 MCP 客户端连接它。

系统会在你的 GitHub 或 GitLab 账户上为该 MCP 服务器新建一个 git 仓库，并配置为每次你推送变更或向仓库主分支合并拉取请求（PR）时自动部署到 Cloudflare。你可以克隆该仓库，在本地开发，并开始用你自己的工具定制这个 MCP 服务器。

### 通过 CLI

你可以使用 Wrangler CLI 在本地机器上创建一个新的 MCP 服务器并将其部署到 Cloudflare。

-

打开一个终端并运行以下命令：

npm yarn pnpm

```
npm create cloudflare@latest -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

```
yarn create cloudflare remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

```
pnpm create cloudflare@latest remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
```

在设置过程中，选择以下选项：- 对于「Do you want to add an AGENTS.md file to help AI coding tools understand
Cloudflare APIs?」，选择 `No`。- 对于「Do you want to use git for version control?」，选择 `No`。- 对于「Do you want to deploy your application?」，选择 `No`（我们会在部署之前先测试服务器）。

现在，你的 MCP 服务器已设置完毕，依赖也已安装。

-

进入项目文件夹：

终端窗口
```

cd remote-mcp-server-authless

```

-

在新项目的目录中，运行以下命令启动开发服务器：

终端窗口
```

npm start

```

```

⎔ Starting local server...

[wrangler:info] Ready on http://localhost:8788

```

查看命令输出以确定本地端口。在此示例中，MCP 服务器运行在端口 `8788`，MCP 端点 URL 为 `http://localhost:8788/mcp`。

注意

你不能通过直接在 Web 浏览器中打开 `/mcp` URL 来与该 MCP 服务器交互。`/mcp` 端点期望由 MCP 客户端发送 MCP 协议消息，而浏览器默认不会这样做。在下一步中，我们将演示如何使用 MCP 客户端连接到该服务器。

-

在本地测试服务器：

-

在新终端中运行 MCP inspector ↗。MCP inspector 是一个交互式 MCP 客户端，让你可以从 Web 浏览器连接到你的 MCP 服务器并调用工具。

终端窗口
```

npx @modelcontextprotocol/inspector@latest

```

```

🚀 MCP Inspector is up and running at:

http://localhost:5173/?MCP_PROXY_AUTH_TOKEN=46ab..cd3

🌐 Opening browser...

```

MCP Inspector 将在你的 Web 浏览器中启动。你也可以手动启动它，方法是打开浏览器并前往 `http://localhost:<PORT>`。查看命令输出以确定 MCP Inspector 运行所在的本地端口。在此示例中，MCP Inspector 由端口 `5173` 提供服务。

-

在 MCP inspector 中，输入你的 MCP 服务器 URL（`http://localhost:8788/mcp`），然后选择 Connect。选择 List Tools 以显示你的 MCP 服务器暴露的工具。

-

现在你可以将 MCP 服务器部署到 Cloudflare。在你的项目目录中运行：

终端窗口
```

npx wrangler@latest deploy

```

如果你已经将 git 仓库连接到包含 MCP 服务器的 Worker，则可以通过推送变更或向仓库主分支合并拉取请求来部署 MCP 服务器。

MCP 服务器将部署到你的 `*.workers.dev` 子域的 `https://remote-mcp-server-authless.your-account.workers.dev/mcp`。

-

要测试远程 MCP 服务器，请取出已部署 MCP 服务器的 URL（`https://remote-mcp-server-authless.your-account.workers.dev/mcp`），并将其输入到运行于 `http://localhost:5173` 的 MCP inspector 中。

现在你已经拥有一个 MCP 客户端可以连接的远程 MCP 服务器。

## 通过本地代理从 MCP 客户端连接

现在你的远程 MCP 服务器已经运行，你可以使用 `mcp-remote` 本地代理 ↗ 将 Claude Desktop 或其他 MCP 客户端连接到它 —— 即使你的 MCP 客户端在客户端侧不支持远程传输或授权也是如此。这让你可以用真正的 MCP 客户端测试与远程 MCP 服务器交互的实际体验。

例如，从 Claude Desktop 连接：

-

更新你的 Claude Desktop 配置，使其指向你的 MCP 服务器 URL：

```

{

"mcpServers": {

"math": {

"command": "npx",

"args": [

"mcp-remote",

"https://remote-mcp-server-authless.your-account.workers.dev/mcp"

]

}

}

}

```

-

重启 Claude Desktop 以加载 MCP 服务器。完成后，Claude 就能对你的远程 MCP 服务器发起调用了。

-

要测试，让 Claude 使用你的其中一个工具。例如：

```

Could you use the math tool to add 23 and 19?

```

Claude 应该会调用该工具并显示远程 MCP 服务器生成的结果。

要了解如何将远程 MCP 服务器与其他 MCP 客户端一起使用，请参阅「测试远程 MCP 服务器」。

## 添加身份认证

你之前部署的公共 MCP 服务器示例允许任何客户端无需登录即可连接并调用工具。要为你的 MCP 服务器添加用户身份认证，你可以集成 Cloudflare Access 或第三方服务作为 OAuth 提供方。你的 MCP 服务器处理安全的登录流程，并签发访问令牌，MCP 客户端可用这些令牌发起经过认证的工具调用。用户通过 OAuth 提供方登录，并使用范围化权限授予其 AI 智能体与你的 MCP 服务器所暴露工具交互的许可。

### Cloudflare Access OAuth

你可以将 MCP 服务器配置为要求用户通过 Cloudflare Access 进行身份认证。Cloudflare Access 充当身份聚合器，并验证用户电子邮件、来自你现有身份提供方（如 GitHub 或 Google）的信号，以及其他属性（如 IP 地址或设备证书）。当用户连接到 MCP 服务器时，系统会提示他们登录已配置的身份提供方，并且只有当他们通过你的 Access 策略时才被授予访问权限。

如需分步部署指南，请参阅「使用 Access for SaaS 保护 MCP 服务器」。

### 第三方 OAuth

你可以将 MCP 服务器与任何支持 OAuth 2.0 规范的 OAuth 提供方连接，包括 GitHub、Google、Slack、Stytch、Auth0、WorkOS 等。

以下示例演示了如何使用 GitHub 作为 OAuth 提供方。

#### 第 1 步 —— 创建新的 MCP 服务器

运行以下命令，创建一个带 GitHub OAuth 的新 MCP 服务器：

npm yarn pnpm

```
npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```
yarn create cloudflare my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```
pnpm create cloudflare@latest my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

现在，你的 MCP 服务器已设置完毕，依赖也已安装。进入该项目文件夹：

终端窗口
```

cd my-mcp-server-github-auth

```

你会注意到，在示例 MCP 服务器中，如果你打开 `src/index.ts`，主要区别在于 `defaultHandler` 被设置为 `GitHubHandler`：

TypeScript
```

import GitHubHandler from "./github-handler";

export default new OAuthProvider({

apiRoute: "/mcp",

apiHandler: MyMCP.serve("/mcp"),

defaultHandler: GitHubHandler,

authorizeEndpoint: "/authorize",

tokenEndpoint: "/token",

clientRegistrationEndpoint: "/register",

});

```

这确保了你的用户会被重定向到 GitHub 进行身份认证。不过，要使其正常工作，你需要按照以下步骤创建 OAuth 客户端应用。

#### 第 2 步 —— 创建 OAuth 应用

你需要创建两个 GitHub OAuth 应用 ↗，才能将 GitHub 用作 MCP 服务器的身份认证提供方 —— 一个用于本地开发，一个用于生产环境。

#### 第 2.1 步 —— 为本地开发创建新的 OAuth 应用

-

前往 github.com/settings/developers ↗，使用以下设置创建一个新的 OAuth 应用：

- 应用名称：`My MCP Server (local)`

- 主页 URL：`http://localhost:8788`

- 授权回调 URL：`http://localhost:8788/callback`

-

对于你刚刚创建的 OAuth 应用，将该 OAuth 应用的客户端 ID 添加为 `GITHUB_CLIENT_ID`，并生成一个客户端密钥，将其添加为项目根目录下 `.env` 文件中的 `GITHUB_CLIENT_SECRET`，该文件将用于在本地开发中设置密钥。

终端窗口
```

touch .env

echo 'GITHUB_CLIENT_ID="your-client-id"' >> .env

echo 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .env

cat .env

```

-

运行以下命令启动开发服务器：

终端窗口
```

npm start

```

你的 MCP 服务器现在运行在 `http://localhost:8788/mcp`。

-

在新终端中运行 MCP inspector ↗。MCP inspector 是一个交互式 MCP 客户端，让你可以从 Web 浏览器连接到你的 MCP 服务器并调用工具。

终端窗口
```

npx @modelcontextprotocol/inspector@latest

```

-

在 Web 浏览器中打开 MCP inspector：

终端窗口
```

open http://localhost:5173

```

-

在 inspector 中，输入你的 MCP 服务器 URL，`http://localhost:8788/mcp`

-

在右侧主面板中，点击 OAuth Settings 按钮，然后点击 Quick OAuth Flow。

你应该会被重定向到 GitHub 登录或授权页面。在授权 MCP 客户端（inspector）访问你的 GitHub 账户后，你将被重定向回 inspector。

-

点击侧边栏中的 Connect，你应该会看到「List Tools」按钮，它会列出你的 MCP 服务器暴露的工具。

#### 第 2.2 步 —— 为生产环境创建新的 OAuth 应用

你需要重复第 2.1 步，为生产环境创建新的 OAuth 应用。

- 前往 github.com/settings/developers ↗，使用以下设置创建一个新的 OAuth 应用：

- 应用名称：`My MCP Server (production)`

- 主页 URL：输入已部署 MCP 服务器的 workers.dev URL（例如 `worker-name.account-name.workers.dev`）

- 授权回调 URL：输入已部署 MCP 服务器 workers.dev URL 的 `/callback` 路径（例如 `worker-name.account-name.workers.dev/callback`）

- 对于你刚刚创建的 OAuth 应用，使用 Wrangler CLI 添加客户端 ID 和客户端密钥：

终端窗口
```

npx wrangler secret put GITHUB_CLIENT_ID

```

终端窗口
```

npx wrangler secret put GITHUB_CLIENT_SECRET

```

```

npx wrangler secret put COOKIE_ENCRYPTION_KEY # add any random string here e.g. openssl rand -hex 32

```

警告

创建第一个密钥时，Wrangler 会询问你是否要创建一个新的 Worker。提交「Y」以创建新的 Worker 并保存该密钥。

-

设置 KV 命名空间

a. 创建 KV 命名空间：

终端窗口
```

npx wrangler kv namespace create "OAUTH_KV"

```

b. 用生成的 KV ID 更新 `wrangler.jsonc` 文件：

```

{

"kvNamespaces": [

{

"binding": "OAUTH_KV",

"id": "<YOUR_KV_NAMESPACE_ID>"

}

]

}

```

-

将 MCP 服务器部署到你的 Cloudflare `workers.dev` 域：

终端窗口
```

npm run deploy

```

-

使用 AI Playground ↗、MCP Inspector 或其他 MCP 客户端连接到运行在 `worker-name.account-name.workers.dev/mcp` 的服务器，并使用 GitHub 进行身份认证。

## 后续步骤

MCP 工具 为你的 MCP 服务器添加工具。

授权 自定义身份认证与授权。

- 资源

- API

- 刚接触 Cloudflare？

- 目录

- 赞助

- 开源

- 支持

- 帮助中心

- 系统状态

- 合规

- GDPR

- 公司

- cloudflare.com

- 我们的团队

- 招聘

- 工具

- Cloudflare Radar

- 速度测试

- BGP 现在安全了吗？

- RPKI Toolkit

- 证书透明度

- 社区

- X

- Discord

- YouTube

- GitHub

- © 2026 Cloudflare, Inc.

- 隐私政策

- 使用条款

- 报告安全问题

- 商标

-

[图: privacy options] Cookie 设置

上一页 
构建一个交互式 ChatGPT 应用 下一页 
测试一个远程 MCP 服务器 

编辑页面 
最后更新：2026 年 3 月 27 日

这个有帮助吗？

是否