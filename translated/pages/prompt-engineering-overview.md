AI 提示工程指南 | Google Cloud

页面目录

- 主题

- 

- 提示工程

# 提示工程：概述与指南

最后更新：2026/01/14

大语言模型（LLM）的兴起为人机交互带来了令人兴奋的可能性。然而，要充分释放这些强大 AI 模型的潜力，需要一项关键技能：提示工程。这一新兴领域专注于设计能够解锁 LLM 能力的有效提示词，使其能够理解意图、遵循指令并生成期望的输出。随着我们在各种应用中越来越多地与 AI 交互，提示工程在确保交互准确、相关且安全方面发挥着至关重要的作用。

免费开始使用

试用聊天提示词

[图：提示工程师]
1:53

成为世界级提示工程师的技巧

## 什么是提示工程？

提示工程是设计与优化提示词以引导 AI 模型（尤其是 LLM）生成期望响应的艺术与科学。通过精心设计提示词，你可以为模型提供上下文、指令和示例，帮助它理解你的意图并以有意义的方式作出回应。可以把它想象成为 AI 提供一份路线图，引导它朝着你心中期望的特定输出前进。

要更深入地了解提示设计的世界及其应用，请查看 Google Cloud 上的《提示设计简介》。

准备好亲身体验 LLM 和提示工程了吗？试用 Vertex AI 免费试用版，感受这项技术的强大之处。

## 什么是 AI 提示词？

在 AI 的语境中，提示词是你提供给模型以引出特定响应的输入。它可以有多种形式，从简单的问题或关键词，到复杂的指令、代码片段，甚至是创意写作示例。提示词的有效性会直接影响 AI 输出的质量与相关性。

## 进行提示工程需要什么？

几个关键要素有助于实现有效的提示工程。掌握这些要素，你就能与 AI 模型有效沟通并充分释放其潜力。

### 提示词格式

提示词的结构和风格在引导 AI 响应方面起着重要作用。不同的模型可能对特定格式响应更好，例如：

提示词的格式在 AI 如何理解你的请求方面起着重要作用。不同的模型可能对特定格式响应更好，例如自然语言问题、直接命令，或带有特定字段的结构化输入。了解模型的能力和偏好的格式，对于设计有效的提示词至关重要。

### 上下文与示例

在提示词中提供上下文和相关示例，有助于 AI 理解期望的任务并生成更准确、更相关的输出。例如，如果你想要一个创意故事，加入几句描述期望语气或主题的句子，就能显著改善结果。

### 微调与适配

使用量身定制的提示词在特定任务或领域上微调 AI 模型，可以提升其性能。此外，根据用户反馈或模型输出调整提示词，可以随着时间推移进一步改善模型的响应。

### 多轮对话

为多轮对话设计提示词，可以让用户与 AI 模型进行连续且具有上下文感知的交互，从而提升整体用户体验。

## 提示词的类型

AI 中使用了多种类型的提示词，各有其特定用途：

### 直接提示词（零样本）

零样本提示是指向模型提供直接的指令或问题，而不附带任何额外的上下文或示例。

这方面的例子之一是创意生成，即提示模型生成创意点子或头脑风暴解决方案。另一个例子是摘要生成或翻译，即要求模型对某段内容进行总结或翻译。

### 单样本、少样本与多样本提示词

这种方法是在给出实际提示词之前，向模型提供一个或多个期望的输入-输出对示例。这有助于模型更好地理解任务并生成更准确的响应。

### 思维链提示词

思维链（CoT）提示鼓励模型将复杂的推理分解为一系列中间步骤，从而产生更全面、结构更清晰的最终输出。

### 零样本思维链提示词

将思维链提示与零样本提示相结合，要求模型执行推理步骤，通常能产生更好的输出。

## 提示工程的用例与示例

以下是一些具体的示例和用例，展示了提示工程如何帮助生成定制化且相关的输出。

### 语言与文本生成

场景

说明

示例提示词

创意写作

设计指定体裁、语气、风格和情节要点的提示词，引导 AI 生成引人入胜的叙事。

“写一篇关于一位年轻女性在阁楼里发现一扇魔法之门的小故事。”

摘要生成

向 AI 提供文本并指示它生成能够抓住关键信息的简洁摘要。

“总结以下关于气候变化的新闻文章的主要观点。”

翻译

指定源语言和目标语言，使 AI 能够在保留含义和上下文的同时准确地翻译文本。

“将以下文本从英语翻译为西班牙语：'The quick brown fox jumps over the lazy dog.'”

对话

设计模拟对话的提示词，让 AI 生成模仿人类互动并保持上下文的响应。

“你是一个友善的聊天机器人，帮助用户排查他们的电脑问题。请回应用户的提问：'我的电脑无法开机。'”

场景

说明

示例提示词

创意写作

设计指定体裁、语气、风格和情节要点的提示词，引导 AI 生成引人入胜的叙事。

“写一篇关于一位年轻女性在阁楼里发现一扇魔法之门的小故事。”

摘要生成

向 AI 提供文本并指示它生成能够抓住关键信息的简洁摘要。

“总结以下关于气候变化的新闻文章的主要观点。”

翻译

指定源语言和目标语言，使 AI 能够在保留含义和上下文的同时准确地翻译文本。

“将以下文本从英语翻译为西班牙语：'The quick brown fox jumps over the lazy dog.'”

对话

设计模拟对话的提示词，让 AI 生成模仿人类互动并保持上下文的响应。

“你是一个友善的聊天机器人，帮助用户排查他们的电脑问题。请回应用户的提问：'我的电脑无法开机。'”

### 问答

场景

说明

示例提示词

开放式问题

设计鼓励 AI 基于其知识库提供全面且信息丰富的回答的提示词。

“解释量子计算的概念及其对未来技术发展的潜在影响。”

具体问题

设计针对特定信息的提示词，使 AI 能够从所提供的上下文或其内部知识库中检索精确的答案。

“法国的首都是什么？”或“根据所提供的文本，森林砍伐的主要原因是什么？”

选择题

提供带选项的提示词，促使 AI 根据对上下文的理解分析并选择最合适的答案。

“《哈利·波特》系列是谁写的？A) J.R.R. Tolkien，B) J.K. Rowling，C) Stephen King”

假设性问题

设计探索假设情境的提示词，让 AI 能够推理、推测并提供可能的结果或解决方案。

“如果人类能够以光速旅行，会发生什么？”

观点类问题

设计引出 AI 对特定主题的看法或观点的提示词，鼓励它为其立场提供推理和理由。

“你认为人工智能最终会超越人类智能吗？为什么？”

场景

说明

示例提示词

开放式问题

设计鼓励 AI 基于其知识库提供全面且信息丰富的回答的提示词。

“解释量子计算的概念及其对未来技术发展的潜在影响。”

具体问题

设计针对特定信息的提示词，使 AI 能够从所提供的上下文或其内部知识库中检索精确的答案。

“法国的首都是什么？”或“根据所提供的文本，森林砍伐的主要原因是什么？”

选择题

提供带选项的提示词，促使 AI 根据对上下文的理解分析并选择最合适的答案。

“《哈利·波特》系列是谁写的？A) J.R.R. Tolkien，B) J.K. Rowling，C) Stephen King”

假设性问题

设计探索假设情境的提示词，让 AI 能够推理、推测并提供可能的结果或解决方案。

“如果人类能够以光速旅行，会发生什么？”

观点类问题

设计引出 AI 对特定主题的看法或观点的提示词，鼓励它为其立场提供推理和理由。

“你认为人工智能最终会超越人类智能吗？为什么？”

### 代码生成

场景

说明

示例提示词

代码补全

向 AI 提供一段不完整的代码片段，并提示它根据上下文和编程语言建议或补全剩余代码。

“编写一个 Python 函数来计算给定数字的阶乘。”

代码翻译

指定源编程语言和目标编程语言，使 AI 能够在保留功能和语法的同时翻译代码。

“将以下 Python 代码翻译为 JavaScript：def greet(name): print('Hello,', name)”

代码优化

提示 AI 分析现有代码，并就效率、可读性或性能提出改进建议。

“优化以下 Python 代码以缩短其执行时间。”

代码调试

向 AI 提供包含错误的代码，并提示它识别问题并针对所发现的问题提出可能的解决方案。

“调试以下 Java 代码，并解释它为什么会抛出 NullPointerException。”

场景

说明

示例提示词

代码补全

向 AI 提供一段不完整的代码片段，并提示它根据上下文和编程语言建议或补全剩余代码。

“编写一个 Python 函数来计算给定数字的阶乘。”

代码翻译

指定源编程语言和目标编程语言，使 AI 能够在保留功能和语法的同时翻译代码。

“将以下 Python 代码翻译为 JavaScript：def greet(name): print('Hello,', name)”

代码优化

提示 AI 分析现有代码，并就效率、可读性或性能提出改进建议。

“优化以下 Python 代码以缩短其执行时间。”

代码调试

向 AI 提供包含错误的代码，并提示它识别问题并针对所发现的问题提出可能的解决方案。

“调试以下 Java 代码，并解释它为什么会抛出 NullPointerException。”

### 图像生成

场景

说明

示例提示词

写实图像

设计详细描述期望图像的提示词，包括物体、场景、光线和风格，以生成逼真且高质量的图像。

“一张日落时分海洋上空的写实图像，棕榈树的剪影映衬在天空背景下。”

艺术图像

设计指定艺术风格、技法和主题的提示词，引导 AI 创作模仿特定艺术流派或唤起某种情感的图像。

“一幅印象派画作，描绘繁忙的城市街道上人们在雨中撑着伞行走。”

抽象图像

设计鼓励 AI 生成具有开放解读空间的图像的提示词，利用形状、色彩和纹理来唤起感受或概念。

“一幅代表希望这一概念的抽象图像，使用明亮的色彩和流动的形状。”

图像编辑

向 AI 提供一张现有图像并指定期望的修改，使其能够根据给定指令编辑和增强图像。

“将这张照片的背景改为繁星点点的夜空，并加上一轮满月。”或“将这张图像中的人物移除，并用一只猫替换。”

场景

说明

示例提示词

写实图像

设计详细描述期望图像的提示词，包括物体、场景、光线和风格，以生成逼真且高质量的图像。

“一张日落时分海洋上空的写实图像，棕榈树的剪影映衬在天空背景下。”

艺术图像

设计指定艺术风格、技法和主题的提示词，引导 AI 创作模仿特定艺术流派或唤起某种情感的图像。

“一幅印象派画作，描绘繁忙的城市街道上人们在雨中撑着伞行走。”

抽象图像

设计鼓励 AI 生成具有开放解读空间的图像的提示词，利用形状、色彩和纹理来唤起感受或概念。

“一幅代表希望这一概念的抽象图像，使用明亮的色彩和流动的形状。”

图像编辑

向 AI 提供一张现有图像并指定期望的修改，使其能够根据给定指令编辑和增强图像。

“将这张照片的背景改为繁星点点的夜空，并加上一轮满月。”或“将这张图像中的人物移除，并用一只猫替换。”

## 编写更优提示词的策略

编写有效的提示词需要策略性的方法。考虑以下策略来提升你的提示工程技能：

### 1. 设定清晰的目标与目的：

策略

提示词示例

使用动作动词来指定期望的动作

“编写一个要点列表，总结所附研究论文的关键发现”

定义期望的输出长度与格式

“撰写一篇 500 字的文章，讨论气候变化对沿海社区的影响。”

指定目标受众

“为一款面向关注可持续发展的年轻成年人的新有机护肤产品线撰写产品描述。”

策略

提示词示例

使用动作动词来指定期望的动作

“编写一个要点列表，总结所附研究论文的关键发现”

定义期望的输出长度与格式

“撰写一篇 500 字的文章，讨论气候变化对沿海社区的影响。”

指定目标受众

“为一款面向关注可持续发展的年轻成年人的新有机护肤产品线撰写产品描述。”

### 2. 提供上下文与背景信息：

策略

提示词示例

包含相关事实与数据

“鉴于自工业化前时代以来全球气温已上升 1 摄氏度，讨论其对海平面上升可能带来的后果。”

引用具体的来源或文档

“基于所附的财务报告，分析该公司过去五年的盈利能力。”

定义关键术语与概念

“用通俗易懂的语言解释量子计算的概念，适合非技术背景的受众。”

策略

提示词示例

包含相关事实与数据

“鉴于自工业化前时代以来全球气温已上升 1 摄氏度，讨论其对海平面上升可能带来的后果。”

引用具体的来源或文档

“基于所附的财务报告，分析该公司过去五年的盈利能力。”

定义关键术语与概念

“用通俗易懂的语言解释量子计算的概念，适合非技术背景的受众。”

### 3. 使用少样本提示：

策略

提示词示例

提供若干期望的输入-输出对示例

输入：“猫” 输出：“一种有胡须的小型毛茸哺乳动物。” 输入：“狗” 输出：“一种以忠诚著称的家养犬科动物。” 提示词：“大象”

展示期望的风格或语气

示例 1（幽默）：“这位政治家的演讲如此乏味，足以治愈失眠。” 示例 2（正式）：“这位政要发表了一场既富有信息量又引人入胜的演讲。” 提示词：“写一句话描述这位喜剧演员的单口相声表演。”

展示期望的详细程度

示例 1（简短）：“这部电影讲述了一个小男孩与外星人交朋友的故事。” 示例 2（详细）：“这部科幻电影讲述了埃利奥特（Elliot）的故事：一个孤独的男孩发现并与一名滞留在地球的外星生物建立了独特的联系。” 提示词：“总结你刚读完的那本小说的情节。”

策略

提示词示例

提供若干期望的输入-输出对示例

输入：“猫” 输出：“一种有胡须的小型毛茸哺乳动物。” 输入：“狗” 输出：“一种以忠诚著称的家养犬科动物。” 提示词：“大象”

展示期望的风格或语气

示例 1（幽默）：「这位政客的演讲枯燥乏味，堪称治疗失眠的良药。」示例 2（正式）：「这位贵宾发表了一场既富有信息量又引人入胜的演讲。」提示词：「写一句话描述这位喜剧演员的单口喜剧表演。」

展示期望的详细程度

示例 1（简短）：「这部电影讲述了一个小男孩与外星人交朋友的故事。」示例 2（详细）：「这部科幻电影讲述了埃利奥特的故事，他是一个孤独的男孩，发现并与一名滞留在地球上的外星生命建立了独特的纽带。」提示词：「总结你刚读完的那部小说的情节。」

### 4. 具体明确：

策略

提示词示例

使用精确的语言，避免歧义

不要用：「写点关于气候变化的内容」，而要用：「写一篇有说服力的文章，论证应实施更严格的碳排放法规。」

尽可能量化你的要求

不要用：「写一首长诗」，而要用：「写一首 14 行的十四行诗，探讨爱与失去的主题。」

将复杂任务分解为更小的步骤

不要用：「制定一个营销计划」，而要用：「1. 确定目标受众。2. 制定关键营销信息。3. 选择适当的营销渠道。」

策略

提示词示例

使用精确的语言，避免歧义

不要用：「写点关于气候变化的内容」，而要用：「写一篇有说服力的文章，论证应实施更严格的碳排放法规。」

尽可能量化你的要求

不要用：「写一首长诗」，而要用：「写一首 14 行的十四行诗，探讨爱与失去的主题。」

将复杂任务分解为更小的步骤

不要用：「制定一个营销计划」，而要用：「1. 确定目标受众。2. 制定关键营销信息。3. 选择适当的营销渠道。」

### 5. 迭代与实验：

策略

行动

尝试不同的措辞和关键词

使用同义词或替代句式重新表述你的提示词。

调整详细程度和具体程度

添加或删除信息以微调输出。

测试不同的提示词长度

尝试较短和较长的提示词，以找到最佳平衡。

策略

行动

尝试不同的措辞和关键词

使用同义词或替代句式重新表述你的提示词。

调整详细程度和具体程度

添加或删除信息以微调输出。

测试不同的提示词长度

尝试较短和较长的提示词，以找到最佳平衡。

### 6. 利用思维链提示：

策略

提示词示例

鼓励逐步推理

「逐步解决这个问题：约翰有 5 个苹果，他吃了 2 个。他还剩多少个苹果？第 1 步：约翰一开始有 5 个苹果。第 2 步：他吃了 2 个苹果，所以我们需要用 5 减去 2。第 3 步：5 - 2 = 3。答案：约翰还剩下 3 个苹果。」

要求模型解释其推理过程

「解释你判断这则电影评论情感倾向的思考过程：'表演非常出色，但情节可以预料。'」

引导模型经历逻辑性的思考序列

「要将这封电子邮件分类为垃圾邮件或非垃圾邮件，请考虑以下几点：1. 发件人是否已知？2. 主题行是否包含可疑关键词？3. 这封邮件是否提供了好得令人难以置信的东西？」

策略

提示词示例

鼓励逐步推理

「逐步解决这个问题：约翰有 5 个苹果，他吃了 2 个。他还剩多少个苹果？第 1 步：约翰一开始有 5 个苹果。第 2 步：他吃了 2 个苹果，所以我们需要用 5 减去 2。第 3 步：5 - 2 = 3。答案：约翰还剩下 3 个苹果。」

要求模型解释其推理过程

「解释你判断这则电影评论情感倾向的思考过程：'表演非常出色，但情节可以预料。'」

引导模型经历逻辑性的思考序列

「要将这封电子邮件分类为垃圾邮件或非垃圾邮件，请考虑以下几点：1. 发件人是否已知？2. 主题行是否包含可疑关键词？3. 这封邮件是否提供了好得令人难以置信的东西？」

如需有关提示工程最佳实践的进一步指导，请参阅 Google Cloud 上的《提示工程五大最佳实践》。

## 提示工程的益处

有效的提示工程带来诸多益处，能增强 AI 模型的能力和可用性：

### 提升模型性能

精心设计的提示词能让 AI 模型产生更准确、更相关、信息量更丰富的输出，因为它们提供了清晰的指令和上下文。

### 减少偏见和有害回复

通过谨慎控制输入并引导 AI 的关注点，提示工程有助于减轻偏见，并最大限度降低生成不当或冒犯性内容的风险。

### 提升可控性和可预测性

提示工程使你能够影响 AI 的行为，并确保回复一致、可预测，与你期望的结果保持一致。

### 改善用户体验

清晰简洁的提示词让用户更容易与 AI 模型有效互动，从而带来更直观、更令人满意的体验。

### 
用 Google Cloud 开启你的 AI 之旅

新客户可获得 300 美元的免费赠额，用于 Google Cloud。

立即开始

与 Google Cloud 销售专家交谈，更详细地讨论你的独特挑战。

联系我们

## 
相关 Google Cloud 产品和服务

查看所有 AI 产品和解决方案

- 

[图: Vertex AI 图标]

Vertex AI Platform

一个面向数据科学家和工程师的统一平台，用于创建、训练、测试、监控、调优和部署机器学习与 AI 模型。

- 

[图: Vertex AI 图标]

Generative AI on Vertex AI

快速构建生成式 AI 模型的原型并进行测试。测试示例提示词、设计你自己的提示词，并定制基础模型和 LLM。

- 

[图: 示例：BigQuery 图标]

AI APIs

借助 Google Cloud 的 AI 和机器学习 API，将 AI 轻松集成到你的应用中。

- 

解决方案

Model Garden on Vertex AI

通过一个集中的地方发现、定制和部署来自 Google 及 Google 合作伙伴的各种模型，快速启动你的机器学习项目。

#### 帮助你入门的更多学习资源

刚接触 Google Cloud 或生成式 AI？新客户可获得 300 美元的免费赠额，用于运行、测试和部署工作负载。

- 培训：免费的生成式 AI 基础课程

- 文档：提示设计入门

- 文档：通用提示设计策略

- 文档：生成式 AI 提示词示例

#### 迈出下一步

用 300 美元免费赠额和 20 多个始终免费的产品，在 Google Cloud 上开始构建。

免费开始使用

- 
##### 需要帮助开始使用吗？
联系销售

- 
##### 与值得信赖的合作伙伴协作
查找合作伙伴

- 
##### 继续浏览
查看所有产品

菜单
[图: Google Cloud]

概览解决方案产品定价资源文档支持联系我们

搜索发送

文档支持
控制台

登录

免费开始

免费开始

联系我们

关闭

- 加速你的数字化转型

- 无论你的业务正处于数字化转型的起步阶段，还是已经稳步推进，Google Cloud 都能帮助你解决最棘手的挑战。

- 

了解更多

- 关键优势

- 

为什么选择 Google Cloud

企业选择我们的首要原因。

- 

AI 和机器学习

获得企业级就绪的 AI。

- 

多云

在任何需要的地方运行你的应用。

- 

全球基础设施

在 Google 同款基础设施上构建。

- 

Data Cloud

用统一的数据做出更明智的决策。

- 

Modern Infrastructure Cloud

新一代云基础设施。

- 

安全

保护你的用户、数据和应用。

- 

生产力和协作

用 AI 驱动的应用连接你的团队。

- 报告与洞察

- 

高管洞察

精选的高管层视角。

- 

分析师报告

了解行业分析师对我们的评价。

- 

白皮书

浏览并下载热门白皮书。

- 

客户案例

浏览案例研究和视频。

关闭

- 行业解决方案

- 应用现代化

- 人工智能

- API 与应用

- 数据分析

- 数据库

- 基础设施现代化

- 生产力与协作

- 安全

- 初创企业与中小企业

查看所有解决方案

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

行业解决方案

降低成本、提升运营敏捷性，并抓住新的市场机遇。

- 
[图: https://www.gstatic.com/cloud/images/navigation/retail.svg]

零售

面向零售价值链的分析和协作工具。

- 
[图: https://www.gstatic.com/cloud/images/navigation/cpg.svg]

快速消费品

面向快消品数字化转型和品牌增长的解决方案。

- 
[图: https://www.gstatic.com/cloud/images/navigation/finance.svg]

金融服务

面向金融服务的计算、数据管理和分析工具。

- 
[图: https://www.gstatic.com/cloud/images/navigation/hcls.svg]

医疗保健与生命科学

大规模推进研究，为医疗保健创新赋能。

- 
[图: https://www.gstatic.com/cloud/images/navigation/media.svg]

媒体与娱乐

面向内容生产和分发运营的解决方案。

- 
[图: https://www.gstatic.com/cloud/images/navigation/telecommunications.svg]

电信

用于部署 5G 并实现其商业化的混合云和多云服务。

- 
[图: https://www.gstatic.com/cloud/images/navigation/gaming.svg]

游戏

由 AI 驱动的解决方案，可更快地构建和扩展游戏。

- 
[图: https://www.gstatic.com/cloud/images/navigation/manufacturing.svg]

制造业

用于优化制造业价值链的迁移和 AI 工具。

- 
[图: https://www.gstatic.com/cloud/images/navigation/supply-chain.svg]

供应链与物流

在供应链和物流运营中实现可持续、高效且具有韧性的数据驱动运营。

- 
[图: https://www.gstatic.com/cloud/images/navigation/government.svg]

政府

面向政府机构的数据存储、AI 和分析解决方案。

- 
[图: https://www.gstatic.com/cloud/images/navigation/icon-sprite.svg#education]

教育

提供更具吸引力学习体验的教学工具。

- 没找到你要找的内容？

- 

查看所有行业解决方案

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

应用现代化

评估、规划、实施和衡量软件实践与能力，以现代化并简化贵组织的业务应用组合。

- 
CAMP

利用 DORA 改进软件交付能力的计划。

- 
传统应用现代化

分析、分类传统工作负载，并着手进行云迁移。

- 
从 PaaS 迁移：Cloud Foundry、OpenShift

将现有容器迁移到 Google 托管容器服务的工具。

- 
从大型机迁移

用于将大型机应用迁移到云端的自动化工具和规范指导。

- 
软件交付现代化

软件供应链最佳实践——内环生产力、CI/CD 和 S3C。

- 
DevOps 最佳实践

在贵组织内实施 DevOps 的流程和资源。

- 
SRE 原则

在贵组织内采用 SRE 的工具和资源。

- 
平台工程

一套全面的托管服务和黄金路径，用于构建、管理和扩展 IDP。

- 
在边缘运行应用

在 Google 的硬件无关边缘解决方案上运行本地化和低延迟应用的指导。

- 
多云架构

用一致的平台管理跨多个云的工作负载。

- 
走向无服务器

用于开发、部署和扩展应用的完全托管环境。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

人工智能

用 AI 和机器学习为你的业务增添智能和效率。

- 
Customer Engagement Suite with Google AI

结合我们最先进的对话式 AI 的端到端应用。

- 
Document AI

大规模自动化的文档处理和数据采集。

- 
Vertex AI Search for commerce

面向零售商的 Google 级搜索和商品推荐。

- 
Google Cloud with Gemini

用于应用开发、编码等的 AI 助手。

- 
Generative AI on Google Cloud

借助生成式 AI 的力量，变革内容创作与发现、研究、客户服务和开发人员效率。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

API 与应用

借助 API、应用和自动化，无需编码即可加快创新步伐。

- 
使用 API 开辟新业务渠道

吸引并赋能开发者和合作伙伴生态。

- 
使用 API 释放遗留应用的价值

用于扩展和现代化遗留应用的云服务。

- 
Open Banking APIx

简化和加速安全交付符合开放银行标准的 API。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

数据分析

借助无服务器、完全托管的分析平台，从任意规模的数据中即时生成洞察，显著简化分析工作。

- 
数据迁移

借助 AI 驱动的迁移服务，迁移并现代化你的数据仓库和数据湖。

- 
数据湖仓

用高性能、开放的数据湖仓统一治理你的多模态数据。

- 
实时分析

从摄取、处理和分析事件流中获得洞察。

- 
营销分析

用于收集、分析和激活客户数据的解决方案。

- 
数据集

来自 Google、公共和商业提供商的数据，用于丰富你的分析和 AI 项目。

- 
商业智能

用于现代化你的 BI 技术栈并创建丰富数据体验的解决方案。

- 
AI for Data Analytics

借助面向数据分析的 AI，编写 SQL、构建预测模型并可视化数据。

- 
地理空间分析

一个可大规模解决地理空间用例的综合平台。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

数据库

借助安全、可靠、高可用且完全托管的数据服务，迁移和管理企业数据。

- 
数据库迁移

用于简化数据库迁移生命周期的指南和工具。

- 
数据库现代化

用于现代化你的运营数据库基础设施的升级。

- 
游戏数据库

用 Google Cloud 数据库构建全球性实时游戏。

- 
Google Cloud 数据库

用于迁移、管理和现代化数据的数据库服务。

- 
将 Oracle 工作负载迁移到 Google Cloud

对你的 Oracle 工作负载进行重新托管、重新平台化或重写。

- 
开源数据库

具备企业级支持的完全托管开源数据库。

- 
SQL Server on Google Cloud

在 Google Cloud 上运行 SQL Server 虚拟机的选项。

- 
Gemini for Databases

用 AI 极大增强数据库开发和管理。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

基础设施现代化

借助面向 SAP、VMware、Windows、Oracle 及其他工作负载的解决方案快速迁移。

- 
应用迁移

用于迁移到云端的发现和分析工具。

- 
SAP on Google Cloud

运行 SAP 应用和 SAP HANA 的认证。

- 
高性能计算

支持任意工作负载的计算、存储和网络选项。

- 
Windows on Google Cloud

用于运行 Windows 工作负载的工具和合作伙伴。

- 
数据中心迁移

面向虚拟机、应用、数据库等的迁移解决方案。

- 
Active Assist

自动优化云资源并提升安全性。

- 
虚拟桌面

面向桌面和应用的远程办公解决方案（VDI 与 DaaS）。

- 
快速迁移与现代化计划

简化上云之路的端到端迁移计划。

- 
备份与灾难恢复

确保满足你的业务连续性需求。

- 
Red Hat on Google Cloud

Google 与 Red Hat 为传统本地部署和定制应用提供企业级平台。

- 
跨云网络

简化混合云和多云网络，并保护你的工作负载、数据和用户。

- 
可观测性

借助端到端的可见性监控、排查问题并改善应用性能。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

生产力与协作

用为人设计、为影响力而构建的解决方案改变团队的工作方式。

- 
Google Workspace

面向企业的协作和生产力工具。

- 
Google Workspace Essentials

面向团队的安全视频会议和现代化协作。

- 
Cloud Identity

供 IT 管理员管理用户设备和应用的统一平台。

- 
Chrome Enterprise

为企业打造的 ChromeOS、Chrome 浏览器和 Chrome 设备。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

安全

检测、调查并应对在线威胁，帮助保护你的业务。

- 
Agentic SOC

借助 AI 智能体交付更出色的安全成果。

- 
Web 应用与 API 防护

面向你的 Web 应用和 API 的威胁与欺诈防护。

- 
安全与韧性框架

面向安全与韧性生命周期各阶段的解决方案。

- 
风险与合规即代码（RCaC）

借助自动化现代化你的治理、风险与合规职能的解决方案。

- 
软件供应链安全

用于提升端到端软件供应链安全的解决方案。

- 
Security Foundation

帮助实现强大安全态势的推荐产品。

- 
Google Cloud Cybershield™

强化全国范围的网络防御。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

初创企业与中小企业

用量身定制的解决方案和计划加速初创企业和中小企业成长。

- 
初创企业计划

获得资金、业务和技术支持，推动你的初创企业更上一层楼。

- 
中小企业

探索面向网站托管、应用开发、AI 和分析的解决方案。

- 
软件即服务

构建更出色的 SaaS 产品，高效扩展并推动业务增长。

关闭

- 精选产品

- AI 与机器学习

- 商业智能

- 计算

- 容器

- 数据分析

- 数据库

- 开发工具

- 分布式云

- 混合云与多云

- 行业专用

- 集成服务

- 管理工具

- 地图与地理空间

- 媒体服务

- 迁移

- 混合现实

- 网络

- 运营

- 生产力与协作

- 安全与身份

- 无服务器

- 存储

- Web3

查看所有产品（100 多个）

- 精选产品

- 
[图: https://www.gstatic.com/cloud/images/navigation/compute-engine.png]

Compute Engine

在 Google 数据中心中运行的虚拟机。

- 
[图: https://www.gstatic.com/cloud/images/navigation/cloud-storage.png]

Cloud Storage

安全、持久且可扩展的对象存储。

- 
[图: https://www.gstatic.com/cloud/images/navigation/bigquery.png]

BigQuery

面向分析和数据科学的自主数据到 AI 平台。

- 
[图: https://www.gstatic.com/cloud/images/navigation/cloud-run.png]

Cloud Run

用于运行容器化应用的完全托管环境。

- 
[图: https://www.gstatic.com/cloud/images/navigation/kubernetes-engine.png]

Google Kubernetes Engine

用于运行容器化应用的托管环境。

- 
[图: https://www.gstatic.com/cloud/images/navigation/vertex-ai.png]

Vertex AI

面向机器学习模型和生成式 AI 的统一平台。

- 
[图: https://www.gstatic.com/cloud/images/navigation/looker.png]

Looker

用于商业智能、数据应用和嵌入式分析的平台。

- 
[图: https://www.gstatic.com/cloud/images/navigation/apigee.png]

Apigee API Management

以可见性和可控性在任何地方管理 API 的全生命周期。

- 
[图: https://www.gstatic.com/cloud/images/navigation/cloud-sql.png]

Cloud SQL

面向 MySQL、PostgreSQL 和 SQL Server 的关系型数据库服务。

- 
[图: https://www.gstatic.com/images/branding/productlogos/gemini_2025/v1/web-24dp/logo_gemini_2025_color_2x_web_24dp.png]

Gemini Enterprise

用于发现、创建、运行和治理 AI 智能体的安全平台。

- 
[图: https://www.gstatic.com/cloud/images/navigation/networking.png]

Cloud CDN

用于分发网页和视频的内容分发网络。

- 没有找到你要的内容？

- 
查看全部产品（100+）

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

AI 和机器学习

- 
Vertex AI Platform

面向机器学习模型和生成式 AI 的统一平台。

- 
Vertex AI Studio

在 Vertex AI 上构建、调优和部署基础模型。

- 
Vertex AI Agent Builder

构建和部署生成式 AI 体验。

- 
Conversational Agents

构建兼具确定性和生成式 AI 功能的对话式 AI。

- 
Vertex AI Search

为你的企业应用和体验构建 Google 品质的搜索。

- 
Speech-to-Text

支持 125 种语言的语音识别和转录。

- 
Text-to-Speech

支持 220 多种音色和 40 多种语言的语音合成。

- 
Translation AI

语言检测、翻译和术语表支持。

- 
Gemini Enterprise

用于发现、创建、运行和治理 AI 智能体的安全平台。

- 
Vision AI

用于检测情绪、文本等内容的定制和预训练模型。

- 
Contact Center as a Service

云原生的一体化联络中心解决方案。

- 没有找到你要的内容？

- 
查看全部 AI 和机器学习产品

- Business Intelligence

- 
Looker

用于商业智能、数据应用和嵌入式分析的平台。

- 
Looker Studio

用于仪表盘、报告和分析的交互式数据套件。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Compute

- 
Compute Engine

运行在 Google 数据中心中的虚拟机。

- 
App Engine

面向应用和后端的无服务器应用平台。

- 
Cloud GPUs

用于机器学习、科学计算和 3D 可视化的 GPU。

- 
Migrate to Virtual Machines

将服务器和虚拟机迁移到 Compute Engine。

- 
Spot VMs

用于批处理作业和容错型工作负载的计算实例。

- 
Batch

用于调度批处理作业的完全托管服务。

- 
Sole-Tenant Nodes

用于合规、授权和管理的专用硬件。

- 
Bare Metal

用于在 Google Cloud 上运行专用工作负载的基础设施。

- 
Recommender

面向 Google Cloud 产品和服务的用量建议。

- 
VMware Engine

完全托管、原生的 VMware Cloud Foundation 软件栈。

- 
Cloud Run

用于运行容器化应用的完全托管环境。

- 没有找到你要的内容？

- 
查看全部计算产品

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Containers

- 
Google Kubernetes Engine

用于运行容器化应用的托管环境。

- 
Cloud Run

用于运行容器化应用的完全托管环境。

- 
Cloud Build

用于在 Docker 容器中运行构建步骤的解决方案。

- 
Artifact Registry

用于构建产物和依赖项的包管理器。

- 
Cloud Code

用于编写、运行和调试 Kubernetes 应用的 IDE 支持。

- 
Cloud Deploy

面向 GKE 和 Cloud Run 的完全托管持续交付。

- 
Migrate to Containers

用于将虚拟机迁移到 GKE 上系统容器的组件。

- 
Deep Learning Containers

包含数据科学框架、库和工具的容器。

- 
Knative

用于创建 Kubernetes 原生云软件的组件。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Data Analytics

- 
BigQuery

面向分析和数据科学的自主数据到 AI 平台。

- 
Looker

用于商业智能、数据应用和嵌入式分析的平台。

- 
Dataflow

用于流式处理和批处理的实时分析。

- 
Pub/Sub

用于事件摄取和投递的消息服务。

- 
Dataproc

用于运行 Apache Spark 和 Apache Hadoop 集群的托管服务。

- 
Google Cloud Serverless for Apache Spark

面向 Spark 工作负载的快速虚拟机启动和动态自动扩缩。

- 
Cloud Composer

构建在 Apache Airflow 之上的工作流编排服务。

- 
BigLake

使用 Apache Iceberg 构建数据湖仓的存储引擎。

- 
Dataplex Universal Catalog

面向所有 Google Cloud 服务的统一数据到 AI 治理框架。

- 
BigQuery Migration Services

免费使用、云原生且由 AI 驱动的数据迁移服务。

- 
Managed Service for Apache Kafka

用于运行高可用 Apache Kafka 集群的托管 Kafka 服务。

- 没有找到你要的内容？

- 
查看全部数据分析产品

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Databases

- 
AlloyDB for PostgreSQL

面向企业工作负载的完全托管、兼容 PostgreSQL 的数据库。

- 
Cloud SQL

面向 MySQL、PostgreSQL 和 SQL Server 的完全托管数据库。

- 
Firestore

具有 MongoDB 兼容性、高可扩展的无服务器 NoSQL 文档数据库。

- 
Spanner

具有无限扩展能力和 99.999% 可用性的云原生关系型数据库。

- 
Bigtable

面向大规模、低延迟工作负载的云原生宽列数据库。

- 
Datastream

无服务器变更数据捕获和复制服务。

- 
Database Migration Service

面向 Cloud SQL 的无服务器、停机时间极短的迁移服务。

- 
Bare Metal Solution

面向 Oracle 工作负载的完全托管基础设施。

- 
Memorystore

用于亚毫秒级数据访问的完全托管 Redis 和 Memcached。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Developer Tools

- 
Artifact Registry

用于构建产物和依赖项的通用包管理器。

- 
Cloud Code

用于编写、运行和调试 Kubernetes 应用的 IDE 支持。

- 
Cloud Build

持续集成和持续交付平台。

- 
Cloud Deploy

面向 GKE 和 Cloud Run 的完全托管持续交付。

- 
Cloud Deployment Manager

用于创建和管理 Google Cloud 资源的服务。

- 
Cloud SDK

面向 Google Cloud 的命令行工具和库。

- 
Cloud Scheduler

用于任务自动化和管理的 Cron 作业调度器。

- 
Cloud Source Repositories

用于存储、管理和跟踪代码的私有 Git 仓库。

- 
Infrastructure Manager

使用 Terraform 实现基础设施管理自动化。

- 
Cloud Workstations

云端托管且安全的开发环境。

- 
Gemini Code Assist

在 Google Cloud 和你的 IDE 中均可使用的 AI 驱动助手。

- 没有找到你要的内容？

- 
查看全部开发者工具

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Distributed Cloud

- 
Google Distributed Cloud Connected

面向边缘工作负载的分布式云服务。

- 
Google Distributed Cloud Air-gapped

面向隔离环境工作负载的分布式云。

- Hybrid and Multicloud

- 
Google Kubernetes Engine

用于运行容器化应用的托管环境。

- 
Apigee API Management

API 管理、开发和安全平台。

- 
Migrate to Containers

用于将工作负载和现有应用迁移到 GKE 的工具。

- 
Cloud Build

用于在 Google Cloud 基础设施上执行构建的服务。

- 
Observability

监控、日志记录和应用性能套件。

- 
Cloud Service Mesh

基于 Envoy 和 Istio 的完全托管服务网格。

- 
Google Distributed Cloud

面向边缘和数据中心的完全托管解决方案。

- Industry Specific

- 
Anti Money Laundering AI

使用 AI 检测可疑的潜在洗钱活动。

- 
Cloud Healthcare API

用于在 Google Cloud 上桥接现有医疗系统和应用的解决方案。

- 
Device Connect for Fitbit

通过 Google Cloud 上的 Fitbit 连接数据获得 360 度患者视图。

- 
Telecom Network Automation

面向电信网络的开箱即用云原生自动化。

- 
Telecom Data Fabric

以自动化方式实现的电信数据管理和分析。

- 
Telecom Subscriber Insights

摄取数据以改进用户获取和留存。

- 
Spectrum Access System (SAS)

控制公民宽带无线电服务（CBRS）的基础接入。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Integration Services

- 
Application Integration

无需代码即可连接第三方应用并实现数据一致性。

- 
Workflows

面向无服务器产品和 API 服务的工作流编排。

- 
Apigee API Management

以可见性和可控性在任何地方管理 API 的全生命周期。

- 
Cloud Tasks

用于异步任务执行的任务管理服务。

- 
Cloud Scheduler

用于任务自动化和管理的 Cron 作业调度器。

- 
Dataproc

用于运行 Apache Spark 和 Apache Hadoop 集群的服务。

- 
Cloud Data Fusion

用于构建和管理数据流水线的数据集成。

- 
Cloud Composer

构建在 Apache Airflow 之上的工作流编排服务。

- 
Pub/Sub

用于事件摄取和投递的消息服务。

- 
Eventarc

构建可连接任何服务的事件驱动架构。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Management Tools

- 
Cloud Shell

内置命令行的交互式 Shell 环境。

- 
Cloud console

用于管理和监控云应用的基于 Web 的界面。

- 
Cloud Endpoints

用于 Google Cloud 上 API 的部署和开发管理。

- 
Cloud IAM

面向 Google Cloud 资源的权限管理系统。

- 
Cloud APIs

面向 Google Cloud 服务的编程接口。

- 
Service Catalog

供管理员管理企业内部解决方案的服务目录。

- 
Cost Management

用于监控、控制和优化成本的工具。

- 
Observability

监控、日志记录和应用性能套件。

- 
Carbon Footprint

用于查看和导出 Google Cloud 碳排放报告的仪表盘。

- 
Config Connector

用于管理 Google Cloud 资源的 Kubernetes 附加组件。

- 
Active Assist

用于轻松管理性能、安全和成本的工具。

- 没有找到你要的内容？

- 
查看全部管理工具

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Maps and Geospatial

- 
Earth Engine

面向地球观测数据和分析的地理空间平台。

- 
Google Maps Platform

创建沉浸式位置体验并改进业务运营。

- Media Services

- 
Cloud CDN

用于分发网页和视频内容的内容分发网络。

- 
Live Stream API

用于转换直播视频并打包进行流式分发的服务。

- 
OpenCue

面向视觉效果和动画的开源渲染管理器。

- 
Transcoder API

转换视频文件并将其打包以实现优化分发。

- 
Video Stitcher API

用于动态或服务端广告插入的服务。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Migration

- 
Migration Center

使用 Google Cloud 进行迁移和现代化的统一平台。

- 
Application Migration

以低成本刷新周期将应用迁移到云端。

- 
Migrate to Virtual Machines

用于将虚拟机和物理服务器迁移到 Compute Engine 的组件。

- 
Cloud Foundation Toolkit

面向 Deployment Manager 和 Terraform 的参考模板。

- 
Database Migration Service

面向 Cloud SQL 的无服务器、停机时间极短的迁移服务。

- 
Migrate to Containers

用于将虚拟机迁移到 GKE 上系统容器的组件。

- 
BigQuery Migration Services

简化的数据仓库和数据湖迁移工具及激励措施。

- 
Rapid Migration and Modernization Program

简化上云路径的端到端迁移计划。

- 
Transfer Appliance

用于将大量数据迁移到 Google Cloud 的存储服务器。

- 
Storage Transfer Service

从在线和本地来源向 Cloud Storage 传输数据。

- 
VMware Engine

在 Google Cloud 上原生迁移和运行 VMware 工作负载。

- Mixed Reality

- 
Immersive Stream for XR

托管、渲染和流式分发 3D 与 XR 体验。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Networking

- 
Cloud Armor

针对 Web 和 DDoS 攻击的安全策略和防御。

- 
Cloud CDN and Media CDN

用于分发网页和视频内容的内容分发网络。

- 
Cloud DNS

用于可靠、低延迟名称解析的域名系统。

- 
Cloud Load Balancing

用于在应用和区域之间分发流量的服务。

- 
Cloud NAT

用于为私有实例提供互联网访问的 NAT 服务。

- 
Cloud Connectivity

面向 VPN、对等互联和企业需求的连接选项。

- 
Network Connectivity Center

用于简化和扩展网络的连接管理。

- 
Network Intelligence Center

网络监控、验证和优化平台。

- 
Network Service Tiers

基于性能、可用性和成本的云网络选项。

- 
Virtual Private Cloud

适用于整个组织、在项目内隔离的单一 VPC。

- 
Private Service Connect

你的 VPC 与服务之间的安全连接。

- 没有找到你要的内容？

- 
查看全部网络产品

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Operations

- 
Cloud Logging

Google Cloud 审计、平台和应用日志管理。

- 
Cloud Monitoring

以丰富指标呈现基础设施和应用健康状况。

- 
Error Reporting

应用错误识别和分析。

- 
Managed Service for Prometheus

Google Cloud 上完全托管的 Prometheus。

- 
Cloud Trace

从应用采集延迟数据的追踪系统。

- 
Cloud Profiler

用于分析应用性能的 CPU 和堆分析器。

- 
Cloud Quotas

管理所有 Google Cloud 服务的配额。

- Productivity and Collaboration

- 
AppSheet

用于构建和扩展应用的无代码开发平台。

- 
Gemini Enterprise

用于发现、创建、运行和治理 AI 智能体的安全平台。

- 
Google Workspace

面向个人和组织的协作与生产力工具。

- 
Google Workspace Essentials

面向团队的安全视频会议和现代协作。

- 
Cloud Identity

供 IT 管理员管理用户设备和应用的统一平台。

- 
Chrome Enterprise

面向企业打造的 ChromeOS、Chrome 浏览器和 Chrome 设备。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Security and Identity

- 
Cloud IAM

面向 Google Cloud 资源的权限管理系统。

- 
Sensitive Data Protection

发现、分类和保护你的宝贵数据资产。

- 
Mandiant Managed Defense

全天候 24x7 自信地发现并消除威胁。

- 
Google Threat Intelligence

了解是谁在攻击你。

- 
Security Command Center

用于防御针对 Google Cloud 资产威胁的平台。

- 
Cloud Key Management

在 Google Cloud 上管理加密密钥。

- 
Mandiant Incident Response

将入侵事件的影响降到最低。

- 
Chrome Enterprise Premium

以广泛的端点可见性获得安全的企业浏览体验。

- 
Assured Workloads

面向敏感工作负载的合规性和安全控制。

- 
Google Security Operations

检测、调查并响应网络威胁。

- 
Mandiant Consulting

在事件发生前、发生期间和发生后获取专家指导。

- 没有找到你要的内容？

- 
查看全部安全和身份产品

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Serverless

- 
Cloud Run

用于运行容器化应用的完全托管环境。

- 
Cloud Functions

用于创建响应云事件的函数的平台。

- 
App Engine

面向应用和后端的无服务器应用平台。

- 
Workflows

面向无服务器产品和 API 服务的工作流编排。

- 
API Gateway

使用完全托管的网关开发、部署、保护和管理 API。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Storage

- 
Cloud Storage

安全、持久且可扩展的对象存储。

- 
Block Storage

面向 AI、分析、数据库和企业应用的高性能存储。

- 
Filestore

高度可扩展且安全的文件存储。

- 
Persistent Disk

面向在 Google Cloud 上运行的虚拟机实例的块存储。

- 
Cloud Storage for Firebase

用于存储和提供用户生成内容的对象存储。

- 
Local SSD

本地挂载、满足高性能需求的块存储。

- 
Storage Transfer Service

从在线和本地来源向 Cloud Storage 传输数据。

- 
Google Cloud Managed Lustre

高性能托管并行文件服务。

- 
Google Cloud NetApp Volumes

面向 NFS、SMB 和多协议环境的文件存储服务。

- 
Backup and DR Service

用于集中式、应用一致的数据保护的服务。

- 
[图: https://www.gstatic.com/cloud/images/navigation/forward.svg]

Web3

- 
Blockchain Node Engine

用于在区块链上进行开发的完全托管节点托管。

- 
Blockchain RPC

用于在区块链上进行构建的企业级 RPC。

close

- 通过我们透明的定价方式省钱

- Google Cloud 的按需付费定价会根据每月用量自动节省费用，并为预付费资源提供折扣费率。立即联系我们获取报价。

- 


Request a quote

- Pricing overview and tools

- 


Google Cloud pricing

只需为你的实际用量付费，无锁定。

- 


Pricing calculator

计算你的云成本节省。

- 


Google Cloud free tier

探索每月免费用量的产品。

- 


Cost optimization framework

获取优化工作负载成本的最佳实践。

- 


Cost management tools

用于监控和控制成本的工具。

- Product-specific Pricing

- 


Compute Engine

- 


Cloud SQL

- 


Google Kubernetes Engine

- 


Cloud Storage

- 


BigQuery

- 


查看包含 100 多种产品的完整价格表

close

- 学习和构建

- 


Google Cloud Free Program

300 美元免费赠金和 20 多种免费产品。

- 


Solution Generator

获取由 AI 生成的解决方案建议。

- 


Quickstarts

获取教程和分步指南。

- 


Blog

阅读我们最新的产品新闻和故事。

- 


Learning Hub

通过基于角色的培训促进你的职业发展。

- 


Google Cloud certification

准备并报名参加认证。

- 


Cloud computing basics

进一步了解云计算基础知识。

- 


Cloud Architecture Center

获取参考架构和最佳实践。

- Connect

- 


Innovators

加入 Google Cloud 的开发者计划。

- 


Developer Center

保持了解并保持连接。

- 


Events and webinars

浏览即将举行和点播的活动。

- 


Google Cloud Community

提问、找答案并建立连接。

- Consulting and Partners

- 


Google Cloud Consulting

在云项目上与我们的专家合作。

- 


Google Cloud Marketplace

只需几次点击即可部署开箱即用的解决方案。

- 


Find a partner

探索与合作伙伴合作的好处。

- 


Google Cloud partners

了解生态系统和资源。

close
[图: Google Cloud]

- Overview
- arrow_forward

- Solutions
- arrow_forward

- Products
- arrow_forward

- Pricing
- arrow_forward

- Resources
- arrow_forward

- Docs

- Support

- Console

- 加速你的数字化转型

- Learn more

- Key benefits

- Why Google Cloud

- AI and ML

- 多云

- 全球基础设施

- 数据云（Data Cloud）

- 现代基础设施云

- 安全性

- 生产力与协作

- 报告与洞察

- 高管洞察

- 分析师报告

- 白皮书

- 客户案例

- 行业解决方案

- 零售

- 快速消费品（Consumer Packaged Goods）

- 金融服务

- 医疗健康与生命科学

- 媒体与娱乐

- 电信

- 游戏

- 制造业

- 供应链与物流

- 政府

- 教育

- 查看所有行业解决方案

- 查看所有解决方案

- 应用现代化

- CAMP

- 传统应用现代化

- 从 PaaS 迁移：Cloud Foundry、Openshift

- 从大型机迁移

- 软件交付现代化

- DevOps 最佳实践

- SRE 原则

- 平台工程

- 在边缘运行应用

- 面向多云的架构设计

- 走向无服务器

- 人工智能

- 基于 Google AI 的客户互动套件

- Document AI

- 面向商业的 Vertex AI Search

- 搭载 Gemini 的 Google Cloud

- Google Cloud 上的生成式 AI

- 接口与应用（API 与应用）

- 利用 API 开辟新业务渠道

- 利用 API 释放遗留应用

- Open Banking APIx

- 数据分析

- 数据迁移

- 数据湖仓（Data Lakehouse）

- 实时分析

- 营销分析

- 数据集

- 商业智能

- 用于数据分析的 AI

- 地理空间分析

- 数据库

- 数据库迁移

- 数据库现代化

- 游戏数据库

- Google Cloud 数据库

- 将 Oracle 工作负载迁移到 Google Cloud

- 开源数据库

- Google Cloud 上的 SQL Server

- 面向数据库的 Gemini

- 基础设施现代化

- 应用迁移

- Google Cloud 上的 SAP

- 高性能计算

- Google Cloud 上的 Windows

- 数据中心迁移

- Active Assist

- 虚拟桌面

- 快速迁移与现代化计划

- 备份与灾难恢复

- Google Cloud 上的 Red Hat

- 跨云网络

- 可观测性

- 生产力与协作

- Google Workspace

- Google Workspace Essentials

- Cloud Identity

- Chrome Enterprise

- 安全性

- 智能体式 SOC

- Web 应用与 API 保护

- 安全与韧性框架

- 风险与合规即代码（RCaC）

- 软件供应链安全

- 安全基础

- Google Cloud Cybershield™

- 初创企业与中小型企业

- 初创企业计划

- 中小企业

- 软件即服务

- 精选产品

- Compute Engine

- Cloud Storage

- BigQuery

- Cloud Run

- Google Kubernetes Engine

- Vertex AI

- Looker

- Apigee API 管理

- Cloud SQL

- Gemini Enterprise

- Cloud CDN

- 查看所有产品（100+）

- AI 与机器学习

- Vertex AI 平台

- Vertex AI Studio

- Vertex AI Agent Builder

- 对话式智能体

- Vertex AI Search

- 语音转文字

- 文字转语音

- 翻译 AI

- Gemini Enterprise

- 视觉 AI

- 联络中心即服务

- 查看所有 AI 与机器学习产品

- 商业智能

- Looker

- Looker Studio

- 计算

- Compute Engine

- App Engine

- Cloud GPU

- 迁移到虚拟机

- Spot VM

- Batch

- 独占租户节点

- 裸金属

- Recommender

- VMware Engine

- Cloud Run

- 查看所有计算产品

- 容器

- Google Kubernetes Engine

- Cloud Run

- Cloud Build

- Artifact Registry

- Cloud Code

- Cloud Deploy

- 迁移到容器

- 深度学习容器

- Knative

- 数据分析

- BigQuery

- Looker

- Dataflow

- Pub/Sub

- Dataproc

- 面向 Apache Spark 的 Google Cloud 无服务器

- Cloud Composer

- BigLake

- Dataplex 通用目录

- BigQuery 迁移服务

- Apache Kafka 托管服务

- 查看所有数据分析产品

- 数据库

- 面向 PostgreSQL 的 AlloyDB

- Cloud SQL

- Firestore

- Spanner

- Bigtable

- Datastream

- 数据库迁移服务

- 裸金属解决方案

- Memorystore

- 开发者工具

- Artifact Registry

- Cloud Code

- Cloud Build

- Cloud Deploy

- Cloud Deployment Manager

- Cloud SDK

- Cloud Scheduler

- Cloud Source Repositories

- 基础设施管理器

- Cloud Workstations

- Gemini Code Assist

- 查看所有开发者工具

- 分布式云

- Google Distributed Cloud Connected

- Google Distributed Cloud Air-gapped

- 混合与多云

- Google Kubernetes Engine

- Apigee API 管理

- 迁移到容器

- Cloud Build

- 可观测性

- Cloud Service Mesh

- Google Distributed Cloud

- 行业专属

- 反洗钱 AI

- Cloud Healthcare API

- 面向 Fitbit 的设备连接

- 电信网络自动化

- 电信数据编织

- 电信用户洞察

- 频谱接入系统（SAS）

- 集成服务

- 应用集成

- 工作流

- Apigee API 管理

- Cloud Tasks

- Cloud Scheduler

- Dataproc

- Cloud Data Fusion

- Cloud Composer

- Pub/Sub

- Eventarc

- 管理工具

- Cloud Shell

- Cloud 控制台

- Cloud Endpoints

- Cloud IAM

- Cloud API

- 服务目录

- 成本管理

- 可观测性

- 碳足迹

- Config Connector

- Active Assist

- 查看所有管理工具

- 地图与地理空间

- Earth Engine

- Google Maps Platform

- 媒体服务

- Cloud CDN

- Live Stream API

- OpenCue

- Transcoder API

- Video Stitcher API

- 迁移

- Migration Center

- 应用迁移

- 迁移到虚拟机

- Cloud Foundation Toolkit

- 数据库迁移服务

- 迁移到容器

- BigQuery 迁移服务

- 快速迁移与现代化计划

- Transfer Appliance

- Storage Transfer Service

- VMware Engine

- 混合现实

- 面向 XR 的沉浸式流式传输

- 网络

- Cloud Armor

- Cloud CDN 与 Media CDN

- Cloud DNS

- Cloud 负载均衡

- Cloud NAT

- Cloud Connectivity

- Network Connectivity Center

- Network Intelligence Center

- 网络服务层级

- 虚拟私有云

- Private Service Connect

- 查看所有网络产品

- 运维

- Cloud Logging

- Cloud Monitoring

- 错误报告

- Prometheus 托管服务

- Cloud Trace

- Cloud Profiler

- Cloud 配额

- 生产力与协作

- AppSheet

- Gemini Enterprise

- Google Workspace

- Google Workspace Essentials

- Cloud Identity

- Chrome Enterprise

- 安全与身份

- Cloud IAM

- 敏感数据保护

- Mandiant 托管防御

- Google 威胁情报

- Security Command Center

- Cloud Key Management

- Mandiant 事件响应

- Chrome Enterprise Premium

- Assured Workloads

- Google Security Operations

- Mandiant 咨询

- 查看所有安全与身份产品

- 无服务器

- Cloud Run

- Cloud Functions

- App Engine

- 工作流

- API 网关

- 存储

- Cloud Storage

- 块存储

- Filestore

- 持久化磁盘

- 面向 Firebase 的 Cloud Storage

- 本地 SSD

- Storage Transfer Service

- Google Cloud 托管 Lustre

- Google Cloud NetApp Volumes

- 备份与灾难恢复服务

- Web3

- Blockchain Node Engine

- Blockchain RPC

- 通过我们透明的定价方式节省成本

- 申请报价

- 定价概览与工具

- Google Cloud 定价

- 定价计算器

- Google Cloud 免费套餐

- 成本优化框架

- 成本管理工具

- 产品专属定价

- Compute Engine

- Cloud SQL

- Google Kubernetes Engine

- Cloud Storage

- BigQuery

- 查看 100+ 产品的完整价格列表

- 学习与构建

- Google Cloud 免费计划

- 解决方案生成器

- 快速入门

- 博客

- 学习中心

- Google Cloud 认证

- 云计算基础

- 云架构中心

- 连接

- 创新者

- 开发者中心

- 活动与网络研讨会

- Google Cloud 社区

- 咨询与合作伙伴

- Google Cloud 咨询

- Google Cloud Marketplace

- 寻找合作伙伴

- Google Cloud 合作伙伴

- 
### 为什么选择 Google

- 选择 Google Cloud

- 信任与安全

- 现代基础设施云

- 多云

- 全球基础设施

- 区域

- 客户与案例研究

- 分析师报告

- 白皮书

- 博客

- 
### 产品与定价

- Google Cloud 定价

- Google Workspace 定价

- 查看所有产品

- 
### 解决方案

- 基础设施现代化

- 数据库

- 应用现代化

- 智能分析

- 人工智能

- 安全性

- 生产力与工作转型

- 行业解决方案

- DevOps 解决方案

- 小企业解决方案

- 查看所有解决方案

- 
### 资源

- Google Cloud 联盟计划

- Google Cloud 文档

- Google Cloud 快速入门

- Google Cloud Marketplace

- 了解云计算

- 支持

- 代码示例

- 云架构中心

- 培训

- 认证

- Google for Developers

- 面向初创企业的 Google Cloud

- 系统状态

- 发行说明

- 
### 互动

- 联系销售

- 寻找合作伙伴

- 成为合作伙伴

- 活动

- 播客

- 开发者中心

- 新闻中心

- YouTube 上的 Google Cloud

- YouTube 上的 Google Cloud Tech

- 在 X 上关注

- 参与用户研究

- 我们正在招聘，加入 Google Cloud！

- 社区论坛

- 关于 Google

- 隐私

- 网站条款

- Google Cloud 条款

- Cookie 管理控制

- 我们气候行动的第三个十年：加入我们

- 订阅 Google Cloud 时事通讯

Subscribe

语言 English

- English

- Deutsch

- Español

- Español (Latinoamérica)

- Français

- Indonesia

- Italiano

- Português (Brasil)

- 简体中文

- 繁體中文

- 日本語

- 한국어