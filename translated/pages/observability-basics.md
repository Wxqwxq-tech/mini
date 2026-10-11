Traces & Spans：你应该了解的可观测性基础 | Last9 

[图: Cookie] 

我们使用 Cookie 来定制你的 Last9 使用体验。
你的偏好是？

仅必需项

全部接受

Last9 

预约演示
打开菜单 

Last9 

预约演示
关闭菜单 

产品 
发现 
探索
日志 追踪 指标 控制平面 AI RUM 告警 

资源 
指南 博客 活动 更新日志 

更多 
客户 文档 定价 

Last9 

- 

产品 

发现 
自动发现你运行的一切，并把问题追踪到根因——速度快 

服务 Kubernetes 任务 主机 

[图: Discover] 

探索

每秒流式处理并分析数百万个事件，全部关联在一起 

日志 追踪 指标 

[图: Explore] 

控制平面 
用于实时管理传入遥测数据的一流开发者体验 

摄取 存储 查询 分析 

[图: Control Plane] 

AI 
在你的 IDE 中使用自然语言获得洞察与调试 

RUM 
带业务上下文的监控 

告警 
面向高基数（high-cardinality）环境 

- 

资源 

指南 
面向构建大规模应用的工程师的全面文档 

OpenTelemetry 高基数 Prometheus LogQL 

[图: Guides] 

博客 
来自可观测性领域的故事、指南与经验 

活动 
SRE 与 DevOps 分享聚会 

更新日志 
更新与改进 

- 

客户 

- 

文档 

- 

定价 

- 

预约演示 

资源 博客 2025 年 4 月 23 日 

# Traces & Spans：你应该了解的可观测性基础 

了解追踪与跨度如何帮助你看清分布式系统内部——从而更快地排查故障并构建更可靠的软件。

[图: Anjali Udasi] Anjali Udasi 

[图: Traces & Spans: Observability Basics You Should Know] 

#### 
目录

在现代软件架构中，应用不仅变得越来越大——它们也变得越来越分布式。微服务、无服务器函数和运行在多个环境中的容器，使得理解系统内部正在发生什么这件事，感觉就像试图在暴风雨中追踪某一滴雨水。

这正是追踪与跨度登场的地方。这些可观测性工具并非只是流行词——它们是你理解复杂分布式系统的秘密武器。让我们来拆解追踪与跨度是什么、它们为什么重要，以及你如何用它们更快地排查故障、构建更可靠的系统。

## 理解追踪与跨度：核心概念

追踪记录了请求在你的分布式系统中流动的整个旅程。可以把一条追踪想象成一个请求从开始到结束的完整故事——从用户点击一个按钮，到他们看到结果为止。

跨度是追踪的构建块。每个跨度代表这段旅程中的一个工作单元——比如一次数据库查询、一次 API 调用，或一次函数执行。跨度彼此嵌套，以展示操作之间的父子关系。

用简单的话来说，它们的关系如下：

- 一条追踪包含多个跨度

- 每个跨度代表一个操作

- 跨度带有计时数据和元数据

- 跨度可以嵌套，以展示操作之间如何相互关联

```
Trace
├── Span (API Gateway)
│ ├── Span (Auth Service)
│ └── Span (User Service)
│ └── Span (Database Query)
└── Span (Response Formatting)
```

💡

如果你好奇追踪与跨度如何同指标、日志和事件配合，这篇文章拆解了这四者。

## 追踪与跨度给 DevOps 专业人员带来的好处

你正在运行一个由几十个微服务组成的复杂系统。突然之间，用户反馈结账流程变慢了。如果没有追踪，你就不得不逐个检查每个服务，白白浪费时间。

有了追踪与跨度，你可以：

- 即时定位瓶颈：准确看到是哪个服务或函数耗时过长

- 跨服务边界调试：跟随请求在服务之间跳转

- 理解依赖关系：可视化你的服务如何连接并相互依赖

- 提升性能：精准地识别并修复缓慢的操作

- 缩短平均恢复时间（MTTR）：问题出现时更快找到根因

## 追踪与跨度的技术实现

让我们深入了解追踪在分布式系统中是如何工作的细节。

### 追踪上下文与传播

要让追踪跨服务边界生效，每个服务都需要知道它正在处理同一个请求的一部分。这是通过上下文传播实现的——在服务之间传递追踪 ID 和跨度 ID。

当请求首次进入你的系统时，它会被分配一个唯一的追踪 ID。当请求在服务之间移动时，这个 ID 会随之传递（通常以 HTTP 头的形式）。每个服务随后创建自己的跨度，但将它们关联到同一条追踪上。

### 跨度属性与事件

跨度不仅仅是时间戳——它们包含丰富的数据：

- 名称：这个跨度代表什么操作

- 计时：开始与结束时间

- 状态：成功、错误等

- 属性：自定义的键值对（如 `user_id` 或 `cart_size`）

- 事件：跨度内值得注意的偶发事项

- 链接：与其他跨度的连接

### 采样策略

追踪所有内容会产生海量数据。这就是为什么大多数系统会使用采样——只采集一定百分比的追踪。明智的采样策略包括：

- 头部采样（head-based sampling）：在请求开始时决定是否采样

- 尾部采样（tail-based sampling）：在请求完成后决定（更适合捕获错误）

- 优先级采样（priority sampling）：始终追踪重要操作，但对常规操作进行采样

💡

如果你想理解可观测性、遥测与监控之间的区别，请查看这篇有用的文章：Observability vs Telemetry vs Monitoring。

## 追踪实现指南：工具与框架

准备好为你的系统添加追踪了吗？以下是你需要的内容：

### OpenTelemetry：行业标准

OpenTelemetry 已成为实现追踪与跨度的首选框架。它提供：

- 面向所有主流编程语言的库

- 厂商中立（vendor-neutral）的 API 和 SDK

- 面向流行框架的自动插桩

- 一致的数据采集与导出方式

### 追踪工具箱

以下若干工具可以帮助你采集、存储和可视化你的追踪数据：

工具
类型
最适合场景

Last9
一体化可观测性
高性价比、高基数（high-cardinality）的可观测性，且定价可预测

Jaeger
开源追踪
自托管（self-hosted）的追踪可视化

Zipkin
开源追踪
简单的分布式追踪

Grafana Tempo
追踪后端
与 Grafana 仪表盘集成

OpenTelemetry Collector
数据采集流水线
处理与路由遥测数据

如果你正在寻找一款符合预算的可观测性解决方案，Last9 值得一看。它按摄取的事件数量定价，让成本保持可预测。此外，我们的平台能够大规模处理高基数数据，并与 OpenTelemetry 和 Prometheus 集成，将你的指标、日志和追踪汇聚到一处。

### 在你的代码中实现追踪

下面是一个使用 OpenTelemetry 在 Node.js 应用中创建跨度的简化示例：

```
// Initialize the OpenTelemetry SDK (once in your app)
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const provider = new NodeTracerProvider();
const exporter = new OTLPTraceExporter({
url: 'http://localhost:4318/v1/traces',
});
provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
provider.register();

// Get a tracer
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('my-service');

// Create spans in your code
async function processOrder(orderId) {
const span = tracer.startSpan('process-order');

// Add attributes to the span
span.setAttribute('order.id', orderId);
span.setAttribute('customer.type', 'premium');

try {
// Do work...

// Create a child span
const dbSpan = tracer.startSpan('database-query', {
parent: span,
});

try {
// Run database query...
dbSpan.end();
} catch (error) {
dbSpan.setStatus({ code: SpanStatusCode.ERROR });
dbSpan.recordException(error);
dbSpan.end();
throw error;
}

span.end();
} catch (error) {
span.setStatus({ code: SpanStatusCode.ERROR });
span.recordException(error);
span.end();
throw error;
}
}
```

💡

想知道 OpenTelemetry 与传统 APM 工具相比如何？这篇文章拆解了关键差异：OpenTelemetry vs Traditional APM Tools。

## 高级追踪技术

一旦你搭建好了基础追踪，以下这些高级技术可以把你的可观测性提升到新的高度。

### 分布式上下文管理

在复杂系统中，你需要管理的上下文远不止追踪 ID。W3C Trace Context 规范为以下内容提供了标准：

- traceparent：包含追踪 ID 与父跨度 ID

- tracestate：允许厂商添加自定义上下文数据

使用这些头可以确保你的追踪能够跨不同的服务和厂商正常工作。

### 追踪、指标与日志之间的关联

可观测性真正的威力来自连接不同的信号：

- 示例追踪（exemplar traces）：将指标与其所生成的追踪关联起来

- 日志中的追踪 ID：将追踪 ID 加入日志消息，以便交叉引用

- 自定义属性：在所有遥测类型中保持一致地使用属性

### 错误处理与异常追踪

当异常发生时，跨度可以提供关键的上下文：

- 为跨度标记错误状态

- 用堆栈追踪记录异常

- 向跨度添加事件，展示错误的演进过程

- 创建携带错误上下文、跨服务边界传递的 baggage 项

💡

要更深入地了解如何领先于问题并提升系统可靠性，请查看这篇关于主动监控的文章：Proactive Monitoring。

## 现实世界中的追踪模式与反模式

### 有效的追踪模式

有意义的跨度命名：使用一致的命名约定，如 `service_name/operation`
正确的粒度：只为重要操作创建跨度，而不是每个函数调用都创建
正确的上下文传播：确保追踪上下文流经所有通信渠道
有用的属性：添加有助于排查故障的属性，如用户 ID 或功能开关（feature flags）
性能意识：留意过度创建跨度带来的开销

### 需要避免的追踪反模式

过度插桩（over-instrumentation）：创建过多跨度会导致性能问题
缺失上下文：未能传播上下文会破坏跨服务边界的追踪
命名不一致：使用不同的命名标准会让追踪更难以解读
数据过多：在跨度中放入过大的负载会让你的追踪后端不堪重负
忽略第三方服务：外部调用缺少跨度会产生盲区

💡

探索可观测性如何在 LLM 的性能与可靠性中发挥关键作用：LLM Observability。

## 追踪与跨度的业务价值：超越技术收益

追踪不仅仅用于排查故障——它们也能提供业务洞察：

- 端到端地追踪关键用户旅程

- 衡量关键业务操作的性能

- 基于追踪数据设定 SLO（服务级别目标，Service Level Objectives）

- 以真实用户视角量化性能问题的成本

- 通过为跨度添加相关属性来创建业务上下文

当你能展示技术改进如何影响用户体验和业务指标时，你就弥合了 DevOps 与业务利益相关者之间的鸿沟。

## 结语

追踪与跨度让你获得观察分布式系统的 X 光般的透视能力。它们揭示服务之间隐藏的连接、精准定位性能瓶颈，并大幅加速调试。

随着系统变得越来越复杂，这种可观测性不再是奢侈品——而是必需品。

💡

如果你想继续围绕分布式追踪与可观测性展开交流，欢迎加入我们的 Discord 社区，在那里 DevOps 专业人员会分享他们的经验与最佳实践！

## 常见问题

### 追踪与日志记录有什么区别？

日志记录采集的是离散的事件，而追踪展示的是跨服务的操作之间的关系。日志告诉你发生了什么；追踪展示给你它是如何发生的。

### 添加追踪会拖慢我的应用吗？

现代追踪库带来的开销极小——在正确配置的情况下，性能影响通常低于 3%。借助采样，你还可以进一步降低这种影响。

### 我需要修改所有代码才能添加追踪吗？

不一定。许多框架提供自动插桩，只需极少的代码改动就能添加追踪。OpenTelemetry 为大多数语言中的流行框架提供了自动插桩。

### 分布式追踪会生成多少数据？

这取决于流量、采样率和跨度详细程度，差异很大。对于繁忙的系统，要按每天从千兆字节到太字节（gigabytes to terabytes）的规模来做规划。这就是为什么选择合适的可观测性平台对成本控制至关重要。

### 追踪能帮助满足安全与合规要求吗？

能！追踪会创建一份请求流经系统的审计轨迹。借助合适的属性，你可以追踪哪些用户或服务在何时访问了哪些数据。

### 追踪与跨度如何同其他可观测性信号配合？

追踪与指标、日志互为补充。指标在高层面上展示系统健康状况，日志提供详细的事件，而追踪则把各个点连起来，展示跨服务的请求流程。

## 

主题

可观测性 监控 

关于作者

[图: Anjali Udasi]

Anjali Udasi 

致力于让技术不那么令人望而生畏。我

#### 
目录

[图: Last9 keyboard illustration] 

## 
免费开始观测。无锁定。

预约演示

OPENTELEMETRY • PROMETHEUS 
只需更新你的配置，几秒内即可在 Last9 上看到数据。

DATADOG • NEW RELIC • 其他 
我们已经为你准备好了。一键迁移你的仪表盘与告警。

基于开放标准构建 
100+ 集成。OTel 原生，可与你的现有技术栈协同工作。

4.8/5 

G2 评价

[图: Gartner Cool Vendor 2025] Gartner Cool Vendor 2025 

[图: High Performer] High Performer 

[图: Best Usability] Best Usability 

[图: Highest User Adoption] Highest User Adoption 

面向 AI 原生团队的可观测性

© 2026 Last9, Inc. 保留所有权利

资源

- 客户 

- 博客 

- 活动 

- 更新日志 

- 指南 

- 文档 

- llms.txt 

平台

- 控制平面 

- 日志 

- 追踪 

- 指标 

- 告警 

- Last9 MCP 

公司

- 关于我们 

- 预约演示 

- 隐私 

- 条款 

[图: SOC 2 Certified] SOC 2 Certified 

[图: PCI DSS Compliant] PCI DSS Compliant 

[图: HIPAA Compliant] HIPAA Compliant 

[图: ISO 27001 Compliant] ISO 27001 Compliant