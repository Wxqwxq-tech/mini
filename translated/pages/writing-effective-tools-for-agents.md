跳到主内容跳到页脚

- 研究

- 经济未来

- 承诺

- 学习

- 新闻

试用 Claude

Anthropic 工程团队

[图: This is an abstract illustration for the Eng Blog article, Writing effective tools for agents -- with agents.]

# 为智能体编写高效工具 —— 与智能体一起

发布于 2025 年 9 月 11 日

智能体的能力上限，取决于我们交给它们的工具。本文将分享如何编写高质量的工具与评测，以及如何借助 Claude 优化其自身工具来提升性能。

模型上下文协议（MCP）可以让 LLM 智能体拥有数百个工具，去解决真实世界中的任务。但我们要怎样才能让这些工具发挥最大效能？

在这篇文章中，我们将介绍在一系列智能体式 AI 系统中提升性能最有效的技巧1。

我们先从以下几个方面讲起：

- 构建并测试你的工具原型

- 借助智能体为你的工具创建并运行全面的评测

- 与 Claude Code 等智能体协作，自动提升工具的性能

最后，我们总结一路走来总结出的编写高质量工具的关键原则：

- 选择要实现的工具（以及不要实现的工具）

- 为工具命名空间化，以界定清晰的功能边界

- 向智能体返回有意义的上下文

- 为 Token 效率优化工具响应

- 对工具描述与规格进行提示工程

[图: This is an image depicting how an engineer might use Claude Code to evaluate the efficacy of agentic tools.]构建评测可以让你系统性地衡量工具的性能。你可以借助 Claude Code，针对这项评测自动优化你的工具。

## 什么是工具？

在计算领域，确定性系统在给定相同输入时每次都产生相同输出，而非确定性系统——比如智能体——即使在相同起始条件下也可能生成各不相同的响应。

当我们以传统方式编写软件时，我们是在确定性系统之间建立一种契约。例如，像 `getWeather(“NYC”)` 这样的函数调用，每次被调用时都会以完全相同的方式获取纽约市的天气。

工具是一种新的软件形态，它体现的是确定性系统与非确定性智能体之间的契约。当用户问“我今天要不要带伞？”时，智能体可能会调用天气工具，可能根据通用知识来回答，甚至可能先追问一个关于位置的问题。偶尔，智能体也可能产生幻觉，甚至根本没弄明白该如何使用某个工具。

这意味着在面向智能体编写软件时，我们要从根本上重新思考我们的方法：与其像为其他开发者或系统编写函数和接口（API）那样去编写工具和 MCP 服务器，我们更应该为智能体来设计它们。

我们的目标是扩大智能体能够有效解决各类任务的“覆盖范围”，让它们通过工具去尝试多种成功的策略。幸运的是，根据我们的经验，对智能体来说最“顺手”的工具，往往对人类而言也出奇地直观易用。

## 如何编写工具

在本节中，我们将介绍如何与智能体协作，编写并改进你交给它们的工具。首先，快速搭建一个工具原型并在本地进行测试。接着，运行一次全面的评测来衡量后续的改动。与智能体并肩协作，你可以反复进行“评测—改进”的循环，直到你的智能体在真实任务上取得强劲的性能。

### 搭建原型

如果不亲自上手，很难预判哪些工具对智能体来说是顺手的、哪些不是。先快速搭建一个工具原型。如果你用 Claude Code 来编写工具（可能是一次性完成），最好为 Claude 提供你的工具所依赖的任何软件库、接口（API）或软件开发工具包（SDK）（可能包括 MCP SDK）的文档。对 LLM 友好的文档通常可以在官方文档站点上扁平的 `llms.txt` 文件中找到（这是我们 API 的对应文件）。

把工具封装进一个本地 MCP 服务器或桌面扩展（DXT），就可以让你在 Claude Code 或 Claude Desktop 应用中连接并测试这些工具。

要将本地 MCP 服务器连接到 Claude Code，运行 `claude mcp add <name> <command> [args...]`。

要将本地 MCP 服务器或 DXT 连接到 Claude Desktop 应用，请分别前往 `Settings > Developer` 或 `Settings > Extensions`。

工具也可以直接传入 Anthropic API 调用，用于程序化测试。

亲自测试工具，找出任何毛糙之处。收集用户的反馈，围绕你期望这些工具所支撑的用例与提示词建立直觉。

### 运行评测

接下来，你需要通过运行评测来衡量 Claude 使用你工具的效果。首先，生成大量以真实使用场景为基础的评测任务。我们建议与智能体协作，帮助分析结果并确定如何改进工具。请在我们的工具评测 cookbook 中查看这一流程的完整过程。

[图: This graph measures the test set accuracy of human-written vs. Claude-optimized Slack MCP servers.]我们内部 Slack 工具在留出测试集上的表现

生成评测任务

借助早期原型，Claude Code 可以快速探索你的工具，并生成数十对提示词与响应。提示词应当以真实使用场景为灵感，并基于真实的数据源和服务（例如内部知识库和微服务）。我们建议避免过于简单或流于表面的“沙盒”环境，它们无法用足够的复杂度对工具进行压力测试。强评测任务可能需要多次工具调用——甚至多达几十次。

以下是一些较强任务的例子：

- 下周与 Jane 安排一次会议，讨论我们最新的 Acme Corp 项目。附上我们上次项目规划会议的笔记，并预订一间会议室。

- 客户 ID 9182 反馈称，一次购买尝试被扣了三次款。找出所有相关日志条目，并判断是否有其他客户受到同一问题影响。

- 客户 Sarah Chen 刚刚提交了取消请求。准备一份挽留方案。判断：(1) 他们为什么离开，(2) 什么样的挽留方案最有吸引力，以及 (3) 在给出方案前我们应留意哪些风险因素。

以下是一些较弱的任务：

- 下周与 jane@acme.corp 安排一次会议。

- 在支付日志中搜索 `purchase_complete` 和 `customer_id=9182`。

- 通过客户 ID 45892 查找取消请求。

每个评测提示词都应当配对一个可验证的响应或结果。你的验证器既可以简单到在基准真值与采样响应之间做精确的字符串比较，也可以先进到让 Claude 来评判响应。要避免过于严格的验证器——它们会因为格式、标点或合理的替代表述等无关紧要的差异而拒绝正确的响应。

对于每对提示词—响应，你还可以选择性地指定你期望智能体在解决该任务时调用的工具，以衡量智能体在评测过程中是否成功把握了每个工具的用途。不过，由于解决任务可能存在多条正确路径，请尽量避免过度指定或过度拟合某一种策略。

运行评测

我们建议通过直接调用 LLM API 以程序化方式运行评测。使用简单的智能体循环（`while`-循环，交替包裹 LLM API 调用与工具调用）：每个评测任务对应一个循环。每个评测智能体都应被赋予一个单一的任务提示词和你的工具。

在评测智能体的系统提示词中，我们建议指示智能体不仅输出结构化的响应块（用于验证），还要输出推理和反馈块。指示智能体在工具调用和响应块之前先输出这些内容，可能会触发思维链（CoT）行为，从而提升 LLM 的有效智能。

如果你用 Claude 来运行评测，可以开启交替思考，开箱即用地获得类似功能。这将帮助你探究智能体为何调用或不调用某些工具，并凸显工具描述和规格中具体的改进之处。

除了顶层准确率之外，我们还建议收集其他指标，比如单个工具调用和任务的总体运行时长、工具调用的总次数、Token 消耗总量以及工具错误。追踪工具调用有助于揭示智能体所采用的常见工作流，并为工具的整合提供一些机会。

[图: This graph measures the test set accuracy of human-written vs. Claude-optimized Asana MCP servers.]我们内部 Asana 工具在留出测试集上的表现

分析结果

智能体是你发现问题、给出反馈的得力伙伴，从自相矛盾的工具描述，到低效的工具实现，再到令人困惑的工具 schema，它们都能给出反馈。不过要记住：智能体在反馈和响应中遗漏的内容，往往比它们包含的内容更重要。LLM 并不总是说出它们真正的意思。

观察你的智能体在哪里卡壳或感到困惑。通读评测智能体的推理和反馈（或 CoT），找出毛糙之处。审阅原始对话记录（包括工具调用和工具响应），捕捉智能体 CoT 中没有明确描述的行为。读懂言外之意；记住你的评测智能体未必知道正确的答案和策略。

分析你的工具调用指标。大量冗余的工具调用可能意味着需要适当调整分页或 Token 上限参数；大量因无效参数导致的工具错误可能意味着工具需要更清晰的描述或更好的示例。当我们上线 Claude 的网页搜索工具时，我们发现 Claude 会不必要地给工具的 `query` 参数追加 `2025`，从而让搜索结果产生偏差并降低了性能（我们通过改进工具描述把 Claude 引向了正确方向）。

### 与智能体协作

你甚至可以让智能体帮你分析结果并改进工具。只需把你评测智能体的对话记录拼接起来，粘贴到 Claude Code 中。Claude 擅长分析对话记录，并一次性重构大量工具——例如，确保在做出新改动时，工具实现与描述保持一致。

事实上，本文中的大部分建议都来自我们反复用 Claude Code 优化内部工具实现的过程。我们的评测是建立在我们内部工作区之上的，镜像了我们内部工作流的复杂度，包括真实的项目、文档和消息。

我们依赖留出测试集来确保我们没有过度拟合“训练”评测。这些测试集表明，即便超过了我们用“专家级”工具实现所取得的性能——无论这些工具是由我们的研究人员手写，还是由 Claude 自身生成——我们仍能从中榨取额外的性能提升。

在下一节中，我们将分享从这一过程中收获的一些经验。

## 编写高效工具的原则

在本节中，我们将把所学提炼成几条编写高效工具的指导原则。

### 为智能体选择合适的工具

工具越多，并不总能带来更好的结果。我们观察到的一个常见错误是：工具只是简单包装了现有的软件功能或 API 端点——无论这些工具是否适合智能体。这是因为智能体相较于传统软件拥有不同的“可供性（affordance）”——也就是说，它们感知自身借助这些工具所能采取潜在行动的方式是不同的。

LLM 智能体的“上下文”是有限的（也就是说，它们一次性能够处理的信息量是有上限的），而计算机内存则廉价且充裕。以在通讯录中搜索联系人为例。传统软件程序可以高效地逐个存储和处理联系人列表，在转向下一个之前逐一检查。

然而，如果一个 LLM 智能体使用的工具返回了全部联系人，然后它不得不逐 Token 地读取每一个联系人，那它就是把有限的上下文空间浪费在了无关信息上（想象一下，为了在通讯录中找一个人，却从上到下逐页翻找——也就是暴力搜索）。更好、更自然的做法（对智能体和人类都如此）是先跳到相关的页面（也许按字母顺序就能找到）。

我们建议先构建少数几个经过深思熟虑的工具，瞄准特定的高影响工作流，使其与你的评测任务相匹配，然后再从那里扩展。在通讯录的例子中，你可能会选择实现 `search_contacts` 或 `message_contact` 工具，而不是 `list_contacts` 工具。

工具可以整合功能，在幕后处理多个可能离散的操作（或 API 调用）。例如，工具可以用相关元数据来充实工具响应，或在一次工具调用中处理频繁链式的多步骤任务。

下面是一些例子：

- 与其实现 `list_users`、`list_events` 和 `create_event` 工具，不如考虑实现一个 `schedule_event` 工具，它能查找空闲时间并安排事件。

- 与其实现 `read_logs` 工具，不如考虑实现一个 `search_logs` 工具，它只返回相关的日志行以及一些上下文。

- 与其实现 `get_customer_by_id`、`list_transactions` 和 `list_notes` 工具，不如实现一个 `get_customer_context` 工具，它能一次性汇总某个客户最近所有相关的信息。

确保你构建的每个工具都有清晰、独特的用途。工具应当让智能体能够像人类一样——在获得相同底层资源的前提下——对任务进行拆解和解决，同时减少那些原本会被中间输出消耗的上下文。

工具过多或功能重叠也会让智能体偏离高效策略。对你构建（或不构建）的工具进行审慎、有选择的规划，能带来实实在在的回报。

### 为工具命名空间化

你的 AI 智能体可能会访问几十个 MCP 服务器和数百个不同的工具——包括其他开发者提供的工具。当工具功能重叠或用途含糊时，智能体可能会困惑于该用哪一个。

命名空间化（用共同前缀将相关工具分组）有助于在众多工具之间划清边界；MCP 客户端有时默认就会这么做。例如，按服务命名空间化（如 `asana_search`、`jira_search`）以及按资源命名空间化（如 `asana_projects_search`、`asana_users_search`），可以帮助智能体在合适的时机选择正确的工具。

我们发现，在前缀式和后缀式命名空间化之间做选择，对我们的工具使用评测产生了不可忽视的影响。这种影响因 LLM 而异，我们鼓励你根据自己的评测来选择命名方案。

智能体可能会调用错误的工具、用错误的参数调用正确的工具、调用过少的工具，或者错误地处理工具响应。通过有选择地实现那些名称能反映任务自然划分的工具，你同时减少了加载到智能体上下文中的工具和工具描述的数量，并把智能体式计算从智能体的上下文卸载回工具调用本身。这降低了智能体整体犯错的风险。

### 从工具中返回有意义的上下文

同理，工具实现应当注意只向智能体返回高信号的信息。它们应当优先考虑上下文相关性而非灵活性，并摒弃底层技术标识符（例如：`uuid`、`256px_image_url`、`mime_type`）。像 `name`、`image_url` 和 `file_type` 这样的字段，更有可能直接为智能体后续的动作和响应提供指引。

智能体处理自然语言的名称、术语或标识符，往往比处理晦涩的标识符要成功得多。我们发现，仅仅是把任意的字母数字 UUID 解析为语义上更有意义、更可解释的语言（甚至是 0 起索引的 ID 方案），就能通过减少幻觉显著提升 Claude 在检索任务中的精确度。

在某些情况下，智能体可能需要同时与自然语言和技术标识符输出进行交互的灵活性，哪怕只是为了触发下游的工具调用（例如，`search_user(name=’jane’)` → `send_message(id=12345)`）。你可以通过在工具中暴露一个简单的 `response_format` 枚举参数来同时启用两者，让你的智能体控制工具返回 `“concise”`（简洁）还是 `“detailed”`（详细）响应（见下图）。

你可以添加更多格式以获得更大的灵活性，类似于 GraphQL，你可以精确选择想要接收哪些信息。下面是一个用于控制工具响应详略程度的 ResponseFormat 枚举示例：

```
enum ResponseFormat {
DETAILED = "detailed",
CONCISE = "concise"
}
```

Copy

以下是一个详细工具响应的示例（206 个 Token（令牌））：

[图: This code snippet depicts an example of a detailed tool response.]

以下是一个简洁工具响应的示例（72 个 Token（令牌））：

[图: This code snippet depicts a concise tool response.]Slack 线程及线程回复由唯一的 `thread_ts` 标识，获取线程回复需要用到它。`thread_ts` 及其他 ID（`channel_id`、`user_id`）可以从 `“detailed”` 工具响应中获取，从而支持需要这些 ID 的进一步工具调用。`“concise”` 工具响应则只返回线程内容并排除 ID。在此示例中，使用 `“concise”` 工具响应时我们仅消耗了约 ⅓ 的 Token（令牌）。

即便是工具响应的结构——例如 XML、JSON 或 Markdown——也会对评估性能产生影响：并不存在放之四海而皆准的解决方案。这是因为 LLM 基于下一个 Token（令牌）预测进行训练，对于与其训练数据匹配的格式往往表现更好。最佳响应结构会因任务和智能体的不同而有很大差异。我们鼓励你根据自己的评估来选择最佳响应结构。

### 优化工具响应以提升 Token（令牌）效率

优化上下文的质量固然重要，但优化工具响应返回给智能体的上下文数量同样重要。

对于任何可能消耗大量上下文的工具响应，我们建议结合实施分页、范围选择、过滤和/或截断，并为其设置合理的默认参数值。对于 Claude Code，我们默认将工具响应限制为 25,000 个 Token（令牌）。我们预期智能体的有效上下文长度会随时间增长，但对上下文高效工具的需求仍将持续存在。

如果你选择截断响应，务必用有帮助的说明来引导智能体。你可以直接鼓励智能体采用更高 Token（令牌）效率的策略，例如在进行知识检索（Retrieval）任务时执行多次小型而有针对性的搜索，而非一次宽泛的搜索。同样地，如果某次工具调用报错（例如在输入校验期间），你可以对错误响应进行提示工程（Prompt Engineering），清晰地传达具体且可操作的改进建议，而非晦涩的错误代码或回溯信息（traceback）。

以下是一个截断工具响应的示例：

[图: This image depicts an example of a truncated tool response.]

以下是一个无益错误响应的示例：

[图: This image depicts an example of an unhelpful tool response. ]

以下是一个有益错误响应的示例：

[图: This image depicts an example of a helpful error response.]工具截断和错误响应可以引导智能体采取更高 Token（令牌）效率的工具使用行为（使用过滤或分页），或者给出格式正确的工具输入示例。

### 对工具描述进行提示工程（Prompt Engineering）

现在我们来讨论改进工具最有效的方法之一：对工具描述和规格（Spec）进行提示工程（Prompt Engineering）。由于这些内容会加载到智能体的上下文中，它们能够共同引导智能体走向高效的工具调用行为。

在编写工具描述和规格时，想一想你会如何向团队中的新员工描述这个工具。考虑你可能会隐含带入的上下文——专用的查询格式、生僻术语的定义、底层资源之间的关系——并将其显式化。通过清晰描述（并用严格的数据模型加以约束）预期的输入和输出来避免歧义。尤其是，输入参数应当以无歧义的方式命名：不要使用名为 `user` 的参数，而是尝试使用名为 `user_id` 的参数。

借助你的评估，你可以更有信心地衡量提示工程（Prompt Engineering）带来的影响。即便是对工具描述的微小改进，也能带来显著的提升。Claude Sonnet 3.5 在我们对工具描述做出精确改进后，在 SWE-bench Verified 评估上达到了最先进的性能水平，大幅降低了错误率并提升了任务完成度。

你可以在我们的开发者指南（Developer Guide）中找到其他关于工具定义的最佳实践（Best Practice）。如果你正在为 Claude 构建工具，我们还推荐阅读关于工具是如何被动态加载到 Claude 系统提示（system prompt）中的内容。最后，如果你正在为 MCP 服务器编写工具，工具注解（tool annotations）有助于披露哪些工具需要开放世界（open-world）访问，或会做出破坏性更改。

## 展望

要为智能体构建有效的工具，我们需要将软件开发实践从可预测的、确定性的模式重新导向非确定性的模式。

通过本文所描述的迭代式、评估驱动（evaluation-driven）的过程，我们识别出了工具之所以成功的一致模式：有效的工具被有意地、清晰地定义，审慎地使用智能体上下文，能够在多样化的流程中相互组合，并使智能体能够直观地解决现实世界中的任务。

展望未来，我们预期智能体与世界交互的具体机制会不断演进——从 MCP 协议的更新，到底层 LLM 本身的升级。凭借系统化、评估驱动（evaluation-driven）的方法来改进智能体的工具，我们可以确保随着智能体能力的增强，它们所使用的工具也将随之共同演进。

## 致谢

本文由 Ken Aizawa 撰写，并得到了来自以下同事的宝贵贡献：Research（Barry Zhang、Zachary Witten、Daniel Jiang、Sami Al-Sheikh、Matt Bell、Maggie Vo）、MCP（Theodora Chu、John Welsh、David Soria Parra、Adam Jones）、Product Engineering（Santiago Seira）、Marketing（Molly Vorwerck）、Design（Drew Roper）以及 Applied AI（Christian Ryan、Alexander Bricken）。

1 除了训练底层 LLM 本身之外。

[图: Interlocking puzzle piece with complex geometric shape and detailed surface texture]

### 想了解更多？

浏览课程

## 获取开发者通讯

产品更新、操作指南、社区焦点等内容，每月发送至你的收件箱。

如果你希望接收我们每月的开发者通讯，请提供你的邮箱地址。你可以随时退订。

### 产品

- Claude

- Claude Code

- Claude Code Enterprise

- Claude Cowork

- Claude for Chrome

- Claude for Excel

- Claude for PowerPoint

- Claude for Slack

- Skills

- Max plan

- Team plan

- Enterprise plan

- Download app

- Pricing

- Log in to Claude

### 模型

- Opus

- Sonnet

- Haiku

### 解决方案

- AI agents

- Claude Code Security

- Code modernization

- Coding

- Customer support

- Education

- Financial services

- Government

- Healthcare

- Life sciences

- Nonprofits

### Claude Platform

- Overview

- Developer docs

- Pricing

- Marketplace

- Regional compliance

- Amazon Bedrock

- Google Cloud’s Vertex AI

- Microsoft Foundry

- Console login

### 资源

- Blog

- Claude partner network

- Community

- Connectors

- Courses

- Customer stories

- Engineering at Anthropic

- Events

- Inside Claude Code

- Inside Cowork

- Plugins

- Powered by Claude

- Service partners

- Startups program

- Tutorials

- Use cases

### 公司

- Anthropic

- Careers

- Economic Futures

- Research

- News

- Claude’s Constitution

- Responsible Scaling Policy

- Security and compliance

- Transparency

### 帮助与安全

- Availability

- Status

- Support center

### 条款与政策

- Privacy policy

- Consumer health data privacy policy

- Responsible disclosure policy

- Terms of service: Commercial

- Terms of service: Consumer

- Usage policy

© 2026 Anthropic PBC
- 

- 

- 

Writing effective tools for AI agents—using AI agents \ Anthropic