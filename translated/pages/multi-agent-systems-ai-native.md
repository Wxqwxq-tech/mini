多智能体系统（multi-agent systems）在让软件工程师变得 AI 原生（AI-native）过程中的作用

4 种工作流：在代码生成之外采用 AI 智能体（AI agents）

获取实践指南

[图: Resolve.ai]

- 
产品（Product）

- 

用例（Use cases）

- AI SRE

- 生产环境调试（Debugging prod）

- 
客户（Customers）

- 

资源（Resources）

- AI SRE 采购指南

- 评估用于生产的 AI

- AI ROI 操作手册（Playbook）

- 提示库（Prompt library）

- 集成（Integrations）

- 安全（Security）

- 文档（Docs）

- 
博客（Blog）

- 

公司（Company）

- 关于我们

- 招聘（Careers）

- 活动（Events）

联系我们

立即试用

立即试用

- 
首页（Home）

- 
产品（Product）

- 
用例（Use cases）

- 
客户（Customers）

- 
资源（Resources）

- 
博客（Blog）

- 
公司（Company）

#### 社交媒体（Social）

- Linkedin

- Youtube

- X

立即试用

隐私政策（Privacy Policy）服务条款（Terms of Service）
©Resolve.ai - 保留所有权利

[图: Resolve.ai logo]

### 为人类值班的机器

联系我们

产品（Product）

用例（Use cases）
AI SREDebugging prod

客户（Customers）

资源（Resources）
AI SRE 采购指南（buyers guide）评估用于生产的 AI（Evaluating AI for prod）AI ROI 操作手册（Playbook）提示库（Prompt library）术语表（Glossary）

博客（Blog）

公司（Company）
关于我们（About us）招聘（Careers）活动（Events）

产品（Product）客户（Customers）博客（Blog）

#### 加入对话

[图: LinkedIn][图: X/Twitter][图: YouTube]

©Resolve.ai - 保留所有权利
服务条款（Terms of Service）隐私政策（Privacy Policy）

返回博客

技术（Technology）

# 多智能体系统（multi-agent systems）在让软件工程师变得 AI 原生（AI-native）过程中的作用

2026/03/20

分享：

[图: The role of multi agent systems in making software engineers AI-native]

生成式 AI（Generative AI）已经如此深刻地改变了软件开发，以至于你可以在数小时内启动整套服务，然而要弄清楚这些服务出了什么问题，仍然需要在碎片化的工具之间进行艰苦的工作。从代码生成到代码评审（code review），编码智能体（coding agents）负责构建这一侧。但生产环境调试呢？这仍然要靠人工。看下面这个例子：

编码（Coding）生产（Production）

要编写一个服务：你打开一个 AI 原生的开发环境，让 AI「创建一个处理重试和超时的支付服务」。AI 借助你代码库的上下文生成带有错误处理（error handling）的实现当同一个服务出现高延迟（high latency）时：你从一个假设出发 → 查看 Datadog 获取指标 → 切换到 Loki 获取日志 → 交叉比对部署历史 → 关联时间戳 →……如此反复

问题不在于 AI 的能力，而在于我们如何架构 AI 系统。大多数工程团队仍然使用 AI 驱动的工具来更快地执行同样的工作流，而不是重新构想软件开发和生产运营应当如何端到端地运作。

在 Resolve AI，我们一直在为工程师构建用于在生产系统上工作的多智能体系统（multi-agent systems）。我们一直主张工程应当是 AI 原生的（即工程师主要通过与自主智能体（autonomous agents）交互来处理生产系统），而软件工程领域大多数生成式 AI 的讨论都集中在用 Copilot 和编码助手编写 AI 生成的代码上。

我们最近向斯坦福大学的研究生 AI 项目介绍了我们的方法，深入探讨了能够实现 AI 原生工程工作流的 AI 智能体及其架构模式。

### 什么是 AI 原生工程（AI-native engineering）？它为什么重要？

AI 原生工程是指工程师主要通过与 AI 交互来编排（orchestrate）他们的工作：无论是编写代码还是在生产系统上工作。AI 原生与仅仅「使用 AI」有着显著区别——后者中工程师仍然在与他们的系统和工具交互，只是用 AI 来加速流程中的单个步骤。

下面是一个示例工作流，用以展示这种区别。

AI 辅助（AI-Assisted）：你使用 AI 工具来更快地完成复杂任务。工作流仍然以人为中心：工程师 → 系统和工具 → 关联 → 行动。
工程师仍然与工具交互，只是用 AI 更快地执行单个任务

AI 原生（AI-Native）：AI 成为你生产工作的主要接口。工作流变为由 AI 主导：工程师 → 自然语言请求 → AI 系统 → 响应 / 行动。
工程师设定目标，让 AI 智能体处理运营工作

[图: Screenshot 2025-09-25 at 6.05.44 PM.png]

以事故响应（incident response）为例。在 AI 辅助的工作流中，你仍然在生成假设、决定哪些证据重要，并手动关联跨工具的各类信号。AI 帮助进行数据检索和分析，但调查中的繁重工作仍然由你承担。

AI 原生的事故响应则运作方式不同：AI 智能体对调查优先级进行实时分类（triage），并行生成相互竞争的假设，并基于跨系统证据通过连续的迭代来改进理论。你不再问「你能分析这些日志吗？」，而是说「解决这个结账故障」，智能体就会协调整个调查过程。

这不仅仅是更快。它改变了哪些问题值得工程师关注。当 AI 智能体处理日志分析、指标关联和部署时间线重建时，工程师在更高的层级上工作，专注于架构决策和系统设计，而非战术性的调查。

这种转变需要持久化的 AI 智能体，而不仅仅是 AI 工具。虽然像来自 OpenAI 或 Anthropic 的 AI 模型可以加速单个任务，但只有有状态（stateful）的智能体才能在整个事故生命周期中维护调查上下文、跨多个工具协调并自主执行复杂任务。

### 为什么多智能体系统（multi-agent systems）对于让工程变得 AI 原生至关重要？

现代生产系统呈现出学术界所称的「不可约的相互依赖」（irreducible interdependence）：理解它们需要跨领域的专业知识，而这些知识无法统一到一个单一的连贯模型之中。这是大多数构建者忽略的洞见：没有任何单一的 AI 工具或一组 AI 模型能够在协调实时调查的同时，在所有这些领域维持专家级的知识。

例如：在一次关键事故中，当 API 延迟激增 10 倍时，调查需要多个专业智能体同时进行实时分析：关联 50 多个微服务（microservices）之间的追踪（traces），分析缓慢的数据库查询和连接池（connection pool）耗尽，检查近期的部署和基础设施变更，扫描认证（auth）日志以发现安全异常，根据当前负载模式评估自动扩缩容（auto-scaling）函数，并结合 SLA 上下文分析支持工单以了解客户影响。这些职能中的每一项都需要领域特定的专业知识和上下文数据，而没有任何单一系统能够有效地维护这些。

在大规模场景下，随着系统复杂性的增加，单个 AI 工具缺乏适应性来应对上下文需求呈指数级的增长。这正是多智能体系统通过结合编排（orchestration）和单个领域专业化（specialization）来实现扩展的地方。下面的矩阵为工程领导者提供了一个概览。找到与你当前状态相匹配的那一行，以理解其局限性：

这个框架揭示了每个层级的技术局限性：

方法（Approach）它是什么在哪里失效局限性成因

LLM使用 LLM（如 ChatGPT）来完成解释、分析和文档等单个任务工程师仍然承担大部分运营工作量单遍（single-pass）生成容易产生幻觉（hallucinations），没有反馈回路，也没有与真实世界的集成

LLM + 工具AI 可以调用函数按指令从监控系统中获取数据关联的认知负担仍然落在人类身上有限的上下文窗口（context windows），跨工具交互没有持久化的状态管理

单个智能体AI 独立地遵循调查工作流顺序调查，在错误的假设上卡住而缺乏验证无法管理多样的推理策略或并行的调查路径

多智能体通过多智能体协作，专业化的 AI 智能体协调并行调查并将其输出合并为统一的诊断需要投入协调协议分布式智能需要正式的通信模式（schemas）和冲突解决机制

这种演进揭示了一个根本性的架构事实：每个层级都会撞上不同的可扩展性天花板。LLM 缺乏持久化状态。工具增强的 LLM 无法在多次聊天中维护调查上下文。即使采用精妙的提示工程（prompt engineering），随着系统复杂性的增长，单个智能体也会成为决策瓶颈。只有多智能体系统才能突破限制所有先前方法的顺序推理（sequential reasoning）约束。它们支持并行的假设检验，而单个智能体必须顺序调查，这使得它们在本质上不适合生产事故在时间上的要求。

### 构建多智能体系统（multi-agent systems）是一个艰难的工程问题

没有任何像 LangChain 这样的现成智能体框架能够单独解决这个问题。构建可用于生产的多智能体系统需要深度领域专业知识与 AI 工程能力的罕见结合。大多数尝试之所以失败，是因为团队只具备其中一方面的专长，而不同时具备两者。以下就是为什么需要这种双重专长的原因：

- 领域专长决定架构：如果不理解生产现实，你就无法设计智能体。只有那些曾在凌晨三点以 DevOps 或 SRE 角色调试过生产环境的人才知道，日志模式和指标异常需要根本不同的调查策略。当支付失败激增时，你需要数据库专长和基础设施专长来确定根因（root cause）。这样的决策不是 AI 问题，而是塑造你如何构建多智能体系统的生产决策。

- AI 专长让智能体协同工作：一旦你分解了问题，你就会碰到计算机科学中困难的部分。智能体之间的上下文传播（context propagation）不是靠直觉。它是在管理有向无环图（directed acyclic graphs）形式的信息流，其中每个智能体的输出馈入下一个智能体的输入。编排并行智能体需要正式的协调协议，以防止竞态条件（race conditions）和死锁（deadlocks）。系统需要从交互和转瞬即逝的故障模式中持续学习。在协调智能体时只要错一步，你的系统就会变得越来越糟，而不是越来越好。

- 二者的交集创造出突破性系统：没有 AI 架构的领域知识只是昂贵的咨询。没有领域知识的 AI 架构会产生调查错对象的结果。突破发生在将两者结合起来之时：既知道数据库连接池在负载下会如何表现（领域），又能构建可以协调池健康检查、部署时间线分析和上游服务验证的智能体：所有这些都在不互相干扰的情况下并行运行（AI 系统）。

在 Resolve AI，我们的团队既包括拥有超过二十年生产系统经验的工程师，也包括共同创建了 OpenTelemetry（生态系统中最具影响力的开源可观测性项目之一）的创始人，还有拥有深厚人工智能专业知识、作为 Google DeepResearch 和 Gemini Agents 背后智囊的研究人员。这种组合让我们能够构建出这样的系统：它们不只是理解「支付失败是坏事」，而是知道要去检查连接池指标，并将其与上游服务的退化相关联。与此同时，还能管理复杂的智能体编排，防止循环调查，并在并行的执行路径之间维持连贯的叙事主线。

### 关于 Resolve AI

Resolve AI 是你始终在线的 AI SRE，帮助你解决事故并运营生产环境。借助 Resolve AI，Salesforce、Zscaler 和 Coinbase 等客户通过让机器为人类值班、让工程师只需专注于写代码，提高了工程速度和系统可靠性。要了解更多关于 AI 原生工程工作流的信息，请访问 resolve.ai。

[图: AI SRE Buyer's Guide]

### AI SRE 采购指南

了解如何在生产环境中评估并采用 AI SRE。

下载

[图: /icons/arrow-right.svg]

[图: Spiros Xanthos's avatar]

Spiros Xanthos

创始人兼 CEO

Spiros 是 Resolve AI 的创始人兼 CEO。他热衷于向客户学习并做构建。他参与创建了 OpenTelemetry，并创办了 Log Insight（被 VMware 收购）和 Omnition（被 Splunk 收购），最近曾担任 Splunk 可观测性业务的高级副总裁（SVP）兼总经理（GM）。

[图: Gabor Angeli's avatar]

Gabor Angeli

研究工程师

Gabor Angeli 带来了丰富的 AI 专业知识，最近曾就职于 Google DeepMind 和 Square。他参与打造的 Gemini 和 Square Assistant 等产品每天触达数百万用户。他加入 Resolve AI 是为了构建智能体式 AI（Agentic AI）系统，帮助工程师理解和驾驭生产系统。

[图: Bharat Khandelwal's avatar]

Bharat Khandelwal

研究工程师

@ Resolve AI

Bharat 是 Resolve AI 的一名研究工程师，负责构建智能体式（agentic）系统，使大语言模型（large language models）能够调试和运营生产软件基础设施。在加入 Resolve 之前，他在 WorldQuant 领导机器学习项目，为宏观经济预测设计基于 Transformer 的架构，并从非结构化数据中融入由 LLM 驱动的情绪信号。他还曾在 Moveworks 从事企业级 NLP 系统的工作，并在 Tower Research Capital 为高频交易开发低延迟的机器学习策略。Bharat 拥有斯坦福大学计算机科学硕士学位（专攻人工智能），以及印度理工学院孟买分校（IIT Bombay）计算机科学工学学士（荣誉）学位。

[图: content title icon]内容（Content）

### AI for prod 电子书

了解顶尖工程团队如何使用 AI 运营生产环境。

下载

[图: /icons/arrow-right.svg]

[图: Spiros Xanthos's avatar]

Spiros Xanthos

创始人兼 CEO

Spiros 是 Resolve AI 的创始人兼 CEO。他热衷于向客户学习并做构建。他参与创建了 OpenTelemetry，并创办了 Log Insight（被 VMware 收购）和 Omnition（被 Splunk 收购），最近曾担任 Splunk 可观测性业务的高级副总裁（SVP）兼总经理（GM）。

[图: Gabor Angeli's avatar]

Gabor Angeli

研究工程师

Gabor Angeli 带来了丰富的 AI 专业知识，最近曾就职于 Google DeepMind 和 Square。他参与打造的 Gemini 和 Square Assistant 等产品每天触达数百万用户。他加入 Resolve AI 是为了构建智能体式 AI（Agentic AI）系统，帮助工程师理解和驾驭生产系统。

[图: Bharat Khandelwal's avatar]

Bharat Khandelwal

研究工程师

@ Resolve AI

Bharat 是 Resolve AI 的一名研究工程师，负责构建智能体式（agentic）系统，使大语言模型（large language models）能够调试和运营生产软件基础设施。在加入 Resolve 之前，他在 WorldQuant 领导机器学习项目，为宏观经济预测设计基于 Transformer 的架构，并从非结构化数据中融入由 LLM 驱动的情绪信号。他还曾在 Moveworks 从事企业级 NLP 系统的工作，并在 Tower Research Capital 为高频交易开发低延迟的机器学习策略。Bharat 拥有斯坦福大学计算机科学硕士学位（专攻人工智能），以及印度理工学院孟买分校（IIT Bombay）计算机科学工学学士（荣誉）学位。

[图: lead-title-icon]
### 相关文章

[图: Fireside Chat: How FinServ Companies Optimize Cost with AI for Prod]

### 炉边谈话：金融服务公司如何借助 AI 为生产环境优化成本

聆听包括 Affirm、MSCI 和 SoFi 在内的金融服务公司工程领导者分享 AI 战略与方法。

[图: How to Evaluate a Production Ready AI SRE ]

技术（Technology）

### 如何评估一个可用于生产的 AI SRE

了解如何评估 AI SRE，以确保它们能在你独特的生产环境中运行。本指南解释了五个智能体式支柱（agentic pillars）、六个关键评估维度以及企业就绪（enterprise readiness）标准，这些将可用于生产的 AI SRE 与实验区分开来。

[图: Beyond the Build: Accelerating Engineering Velocity with Agentic AI]

### 超越构建：用智能体式 AI 加速工程速度

100 位软件工程高管与 Resolve AI 及其他杰出领袖齐聚一堂，讨论了智能体式 AI（agentic AI）在软件工程中从编码到管理生产系统的加速演进。