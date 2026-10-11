上下文腐坏：输入 Token 增加如何影响 LLM 性能·|·Chroma

[图: Chroma——面向 AI 的开源数据基础设施][图: chroma-core/chroma 的 GitHub stars]

- Products 

Products
SyncDatabaseAgent
DocsEnterprisePricingResearch

- Resources 

Resources
ChangelogUpdatesCommunityGitHubPackage Search

Log inSign up

[图: Chroma logo]
Chroma 技术报告

2025 年 7 月 14 日

# 上下文腐坏：输入 Token 增加如何影响 LLM 性能

Kelly Hong 

Anton Troynikov 

Jeff Huber 

大型语言模型（LLM）通常被假定为能均匀地处理上下文——也就是说，模型对第 10,000 个 Token 的处理应当与第 100 个 Token 同样可靠。然而，在实践中这一假设并不成立。我们观察到，随着输入长度变化，模型的性能会发生显著波动，即便是在简单的任务上也是如此。

在本报告中，我们评估了 18 个 LLM，包括最先进的 GPT-4.1、Claude 4、Gemini 2.5 和 Qwen3 模型。我们的结果表明，模型并非均匀地使用其上下文；相反，随着输入长度增长，它们的表现变得越来越不可靠。

[图: 上下文腐坏：输入 Token 增加如何影响 LLM 性能]

[图: 上下文腐坏：输入 Token 增加如何影响 LLM 性能]Claude Sonnet 4、GPT-4.1、Qwen3-32B 与 Gemini 2.5 Flash 在重复词任务上的表现

## —目录

- 引言

- 相关工作

- 大海捞针扩展

- 针-问相似度

- 干扰项的影响

- 针-草堆相似度

- 草堆结构

- LongMemEval

- 重复词

- 局限性与未来工作

- 结论

- 脚注

- 参考文献

- 附录

LLM 近期的进展呈现出上下文窗口不断变长的趋势，最新模型的输入 Token 数已达到数百万级别。由于这些模型在大海捞针（NIAH）[1] 这类被广泛采用的基准测试上取得了接近满分的成绩，人们常常据此假定它们在长上下文任务上的表现是均匀一致的。

然而，NIAH 本质上是一个简单的检索任务：将一个已知句子（"针"）置于一段由无关文本构成的长文档（"草堆"）中，然后提示模型将其检索出来。尽管该基准易于扩展，但它通常只评估直接的词面匹配，未必能代表灵活、偏重语义的任务。

[图: /img/context_rot/niah_lexical.png]
大海捞针（NIAH）示例设置
我们对标准 NIAH 任务进行了扩展，以考察模型在以往未被充分探索的设置下的行为。我们既研究了语义匹配（而非直接词面匹配）的针所产生的影响，也研究了给草堆内容引入变化所产生的影响。

此外，我们还纳入了一项使用 LongMemEval [2] 的对话式问答评估，以及一个让模型复现一系列重复词的合成任务。每一项任务都刻意保持简单，并经过刻意控制，以单独隔离出上下文长度的影响。

我们证明，即便是在这些极简条件下，模型性能也会随输入长度增加而下降，且下降方式往往出人意料、并不均匀。真实世界的应用通常涉及远为复杂的场景，这意味着输入长度的影响在实践中可能更为显著。

我们详实的技术报告如下。如果您觉得我们的工作有用，请考虑引用我们：

plaintext

```
@techreport{hong2025context,
title = {Context Rot: How Increasing Input Tokens Impacts LLM Performance},
author = {Hong, Kelly and Troynikov, Anton and Huber, Jeff},
year = {2025},
month = {July},
institution = {Chroma},
url = {https://trychroma.com/research/context-rot},
}
```

有兴趣从事改进 AI 应用检索方面的工作吗？Chroma 正在招聘

# 

引言#

现代 LLM 的输入上下文长度达到数百万 Token 已属常见。Gemini 1.5 Pro [3] 于 2024 年初率先推出其 1M 上下文窗口，紧随其后的是近期 GPT-4.1 的 1M 上下文窗口 [4] 以及 10M 的 Llama 4 [5]。长上下文的使用场景极具吸引力：更长的上下文意味着 LLM 每次调用能处理更多信息，并生成更具见地的输出。

针对这些模型的长上下文评估，往往都展示出跨输入长度的一致表现。然而，这些评估范围狭窄，并不能代表长上下文在实际中的使用方式。最常用的测试——大海捞针（NIAH）——是一项简单的词面检索任务，常被用来泛化一个模型可靠处理长上下文的能力。而真实应用（如智能体任务或摘要）则要求对更广泛、往往更模糊的信息进行多得多的处理与推理。

设计贴近真实的长上下文基准颇具挑战。任务往往随输入长度增加而愈发复杂，这使得我们难以区分性能下降究竟源于更长的输入，还是源于本身就更难的问题。为解决这一问题，我们的实验将任务复杂度保持恒定，仅改变输入长度——从而让我们能直接测量输入长度单独产生的影响。

## 

贡献#

我们提出以下内容：

- 
一项跨 18 个 LLM 的评估，涵盖领先的闭源与开放权重模型，揭示出性能随输入长度增加而表现出的非均匀性。

- 
一份关于模型在处理干扰项以及不同的问答相似度时所表现出的特定行为模式的记录。

- 
用于复现我们结果的完整代码库。

# 

相关工作#

用于评估模型长上下文能力的最广泛使用的基准之一是大海捞针（NIAH）。尽管它作为一项可扩展的测试很有价值，但它测量的能力很窄：词面检索。模型通常在 NIAH 上表现良好，这导致了"长上下文问题已基本解决"的看法。

然而，NIAH 低估了大多数长上下文任务在实际中所需要的。NIAH 的变体，如包含非词面匹配针-问对的 NoLiMa [6]，揭示出显著的性能下降。其他难度看似相近的任务，如用于测试模型能否识别某段给定文本缺失的 AbsenceBench [7]，同样表现出随输入长度增长而出现的性能退化。

此外，长上下文任务通常涉及在干扰项之间进行消歧，并以此作为任务的一部分。一个例子是多轮共指消解（MRCR）[8] [9]，它要求在多轮对话中、于相似的多个用户请求之间检索出某个特定用户请求的第 i 次出现。然而，针对干扰项在长上下文场景下影响的研究仍然缺乏。

长上下文任务中的一个重要因素是如何对输入长度进行缩放。Latent List [8] 是一项要求模型在各种输入长度下执行固定次数的 Python 列表操作的任务。它测试了填充无关上下文的各种方式，这些方式对模型性能表现出非均匀的影响 [1]。例如，加入彼此在局部相互抵消的列表操作，比加入 print 语句对模型性能的退化更为显著。这凸显了"无关内容"的类型为何重要——因为某些类型可能会随输入长度引入不断增加的复杂度。

类似地，Graphwalks [10] 是一项图遍历任务：给模型一个由十六进制哈希构成的有向图，然后要求它从一个随机节点开始执行广度优先搜索。增加输入长度意味着增大需要遍历的图的规模，这随之增加了任务难度。我们难以将不断增加的任务复杂度与输入长度区分开来，这导致难以单独隔离出输入长度对性能的影响。这指出了将输入长度作为目标变量加以隔离的重要性，而这对于理解 LLM 在长输入下的实际行为至关重要。

# 

大海捞针扩展#

经典的大海捞针任务是将一个随机事实（"针"）置于一个长上下文窗口（"草堆"）的中间，然后就该事实向模型提问。

该任务的原始实现使用的是带有词面匹配的针-问对。然而，实践中长上下文的使用往往需要对模糊任务的语义理解。

[图: /img/context_rot/niah/lexical_2.png]
带词面匹配的大海捞针（NIAH）示例设置
NoLiMa 已证明，随着上下文长度增加，非词面匹配会成为模型面临的一大挑战。该任务利用的针-问对要求模型推断潜在的关联，例如：

> 

问题：哪个角色去过赫尔辛基？

针：其实，Yuki 住在 Kiasma 博物馆旁边。

NoLiMa——针-问对示例
为回答这一问题，模型首先必须知道 Kiasma 博物馆位于赫尔辛基，然后再建立该潜在关联。这不仅测试了模型的非词面匹配能力，也测试了其世界知识。NoLiMa 中有 72.4% 的针-问对需要此类外部知识，这使得该基准更接近对模型如何同时处理这两类任务的测试，而非单纯的非词面匹配。

对非词面匹配影响的孤立测试仍然探索不足。此外，"词面"与"非词面"的这种二元区分，过度简化了真实场景中问答的复杂性。针-问对存在于一个相似度连续谱上，但它们全都被归入这些宽泛的类别。

模型还经常需要处理干扰项，而已有研究表明干扰项会使性能退化 [11]。

在本报告中，我们区分干扰项与无关内容：

[图: /img/context_rot/niah/distractor_irrelevance.png]
对比——干扰项 vs. 无关上下文
- 干扰项与针在主题上相关，但并不能真正回答问题

- 无关内容与针和问题均无关

先前的工作已证明干扰项会产生非均匀的影响，但大多数评估涉及的输入长度较短、模型也较旧。当前最先进的模型据称对干扰项更具鲁棒性，然而它们在不同输入长度下的表现尚未经过充分测试。

NIAH 另一个探索不足的方面是草堆本身，它常常仅被当作缩放输入长度的手段，但这隐含地假定了草堆内容本身对任务性能没有影响。如果模型确实对草堆内容不敏感，那么改变这些内容（例如草堆的主题或叙事走向）就不应对结果产生任何影响。然而，这一假设在很大程度上仍未得到检验。

我们设计了四个受控实验来考察这些因素的影响：

## 

针-问相似度#

我们使用嵌入计算针-问对之间的余弦相似度。为提升稳健性，我们在五个嵌入模型上取平均：text-embedding-3-small、text-embedding-3-large、jina-embeddings-v3、voyage-3-large 和 all-MiniLM-L6-v2。我们测量模型性能如何随输入长度增加而受到针-问相似度的影响。

## 

干扰项的影响#

取一个高相似度的针-问对，我们写出四个干扰项。我们有以下设置：

- 基线：仅含针，无干扰项

- 单个干扰项：针 + 一个随机定位的干扰项

- 多个干扰项：针 + 全部四个随机定位的干扰项

我们测试干扰项对模型性能的影响如何随输入长度增加而变化，以测量干扰项与输入长度之间的非均匀性。

## 

针-草堆相似度#

我们使用两个主题迥异的草堆——Paul Graham 的文章与 arXiv 论文 [12]，并为每个草堆撰写相应的针。为测量针-草堆相似度，我们对草堆进行嵌入，并为每个针检索 top-5 的文本块，然后对其余弦相似度分数取平均。为提升稳健性，这一过程在五个不同的嵌入模型上重复进行。

## 

草堆结构#

在典型的 NIAH 设置中，草堆是若干连贯文本的拼接，每一段文本都有其自身的逻辑思路。例如，原始的 NIAH 基准使用一系列 Paul Graham 的文章，每篇文章都遵循结构化的观点组织来构成论证。为评估这种结构是否影响模型性能，我们比较两种条件：

- 原始：保留每段摘录内观点的自然走向

- 打乱：句子在整个草堆中被随机重排，以在缺乏逻辑连贯性的情况下保持相同的整体主题

我们证明以下内容：

- 在所有实验中，模型性能随输入长度增加而持续下降。

- 相似度更低的针-问对会加快性能下降的速率。

- 干扰项对模型性能的影响并不均匀，取决于它们彼此之间的干扰程度。随着输入长度增加，这种影响更为显著，我们也观察到不同模型对它们的不同响应方式。

- 针-草堆相似度对模型性能没有统一的影响，这表明需要进一步研究。

- 草堆的结构模式持续表现出对模型处理长输入方式的影响。

## 

细节#

对于针类型、草堆主题和草堆结构的每一种唯一组合，我们在以下条件下测试每个模型：

- 8 个输入长度

- 11 个针位置

我们在每个模型的最大上下文窗口下以 temperature=0 进行评估，除非该设置不兼容（如 o3）或被明确不建议（如 Qwen 的"思考模式"）。对于 Qwen 模型，我们采用 YaRN 方法 [13] 将上下文从 32,768 扩展到 131,072 Token。

在适用的情况下，我们同时纳入标准模式与"思考模式"的模型。

我们使用一个对齐过的 GPT-4.1 判卷器来评估模型输出，其方法见附录。

我们注意到少数模型拒绝尝试任务的罕见实例（在总共 194,480 次 LLM 调用中有 69 次——占 0.035%）。例如，Claude Opus 4 有时会出现输出为空、且 stop_reason="refusal" 的情况。

# 

针-问相似度#

在真实世界应用中，模型常被期望处理模糊任务，并在不依赖精确词面匹配的情况下识别相关信息。例如，当一个智能体被赋予一项涉及搜索大型语料库的任务时，用户很少会为相关部分指定精确的关键词。相反，模型必须自行推断相关性。

我们改变针-问对的相似度，用其嵌入的余弦相似度来量化。我们发现，随着针-问相似度降低，模型性能随输入长度增加而下降得更为显著。这反映了更贴近现实的场景：精确的问答匹配较为罕见，而语义模糊会加剧长输入处理的挑战。

## 

实验#

我们的草堆内容来自两个领域：Paul Graham 的文章（与原始 NIAH 实验相同）和 arXiv 论文。对于每个草堆主题（PG 文章、arXiv），我们首先确定常见主题，以指导我们的问题与针的撰写。

我们使用聚类来识别给定语料库中出现的最常见主题：

- 
将文档切分为 1-3 句的文本块

- 
使用 text-embedding-3-large 对每个文本块进行嵌入

- 
使用 UMAP [14] 进行降维，参数如下：n_neighbors=30, min_dist=0.05, n_components=50, random_state=42

- 
使用 HDBSCAN [15] 创建聚类，参数如下：min_cluster_size=10, min_samples=15

- 
使用最大边缘相关度（MMR）为最大的聚类获取 20 个代表性文本块

- 
人工检查最大的聚类，以确定其主题与风格

使用这一方法，我们识别出写作建议是 PG 文章的一个常见主题，且通常以轶事形式呈现。对于 arXiv 论文，我们识别出信息检索是一个常见主题，具体是重排序。

我们为每个主题撰写一个相应的问题：

> 

PG 文章："我从大学同学那里得到的最好的写作建议是什么？"

arXiv 论文："哪种低延迟重排器更适用于科学领域？"

Paul Graham 文章与 arXiv 论文的问题
在撰写针之前，我们验证这些问题在草堆内容中不存在答案：

- 我们将先前计算好的草堆文本块嵌入存储在一个向量数据库中。

- 用我们的问题嵌入从该向量数据库中查询 top-10 结果。

- 人工检查这些结果，以验证它们并未回答所给的问题。

这营造了一个公平的测试环境，因为它确保了不存在备选答案，任何错误答案都源于模型幻觉。

对于每个问题，我们撰写 8 个针，每个针都属于该大型聚类——我们使用近似预测来加以验证。属于写作/检索聚类且概率 >0.9 的针被认为在主题上与草堆融为一体。我们人工撰写这些针，以避免数据污染。

对于这 8 个针，我们还改变其模糊程度，通过以下方法量化：

- 使用一个嵌入模型，我们计算针与问题的嵌入及其余弦相似度。

- 在五种嵌入模型（text-embedding-3-small、text-embedding-3-large、jina-embeddings-v3、voyage-3-large 和 all-MiniLM-L6-v2）上重复执行。

对于 PG 论文主题，我们的针（needle）与问题的相似度范围为 0.445–0.775，且在五种嵌入模型上的标准差小于 0.1。对于 arXiv 主题，针与问题的相似度范围为 0.521–0.829，标准差同样小于 0.1。

## 

结果#

我们观察到一个清晰的模式：在输入长度增长时，相似度较低的针-问题对的性能下降得更快。

[图: /img/context_rot/longmemeval/needle_question_sim_arxiv.png]
NIAH：针-问题相似度（同一模型的思考/非思考模式分别处理）- arXiv 草堆/arXiv 针
高性能：性能前 33%
蓝色：高相似度针（相似度前 50%）
红色：低相似度针（相似度后 50%）
在较短的输入长度下，即使面对低相似度对，模型的表现也相当不错。这一点在高/中性能模型上体现得最为明显，说明这些模型有能力在所有针-问题对上成功完成该任务。

在较长输入长度下观察到的性能下降，并非源于针-问题配对的固有难度。通过固定针-问题对不变、只改变无关内容的数量，我们将输入规模隔离为性能下滑的首要因素。

我们还考察了针的位置是否会影响性能。在 11 个针位置上进行测试后，我们发现这一特定 NIAH 任务中针的位置几乎不会带来性能差异。

# 

干扰项的影响#

较早的模型已经证实，干扰项会降低模型性能，且其影响并不均匀。据称较新的模型能够可靠地应对任何干扰项，但随着输入长度的增加，这一说法是否仍然成立？

我们的实验表明，随着输入长度的增长，干扰项的影响及其不均匀性在各类模型（包括最新的一流模型）上都会放大。我们还观察到不同模型族在处理歧义时表现出截然不同的行为。

## 

实验#

从每个草堆主题（PG 论文和 arXiv 论文）中，我们取一个具有高针-问题相似度（八个中第二高）的针，并手工编写 4 个干扰项：

> 

问题：“我从大学同学那里得到的最好的写作建议是什么？”

针：“我认为我从大学同学那里得到的最好的写作建议是每周都写作。”

干扰项：

- 
“我从大学教授那里得到的最好的写作建议是每天写作。”

- 
“我从大学同学那里得到的最糟糕的写作建议是每篇论文用五种不同的风格来写。”

- 
“我从同学那里得到的最好的写作建议是每篇论文用三种不同的风格来写，那是还在读高中的时候。”

- 
“我曾经以为我从大学同学那里得到的最好的写作建议是每篇论文用四种不同的风格来写，但现在不这么认为了。”

Paul Graham 论文主题与高针-问题相似度针的干扰项
我们没有用干扰项测试全部八个针，而是使用一个高针-问题相似度的针来构造一个针相对容易识别的条件。从先前的结果可以看出，由于针-问题相似度高，模型在不同输入长度下对这个针通常都表现良好，这使我们能够更好地单独隔离并衡量干扰项的影响。

我们运行了三种测试条件：

- 无干扰项（基线）：仅针

- 单一干扰项：针 + 一个干扰项（随机放置）

- 多个干扰项：针 + 全部四个干扰项，随机分布在整个草堆中

[图: /img/context_rot/niah/distractors_var.png]
干扰项的影响 - 三种条件
## 

结果#

即使只有一个干扰项，性能也会相对基线（仅针）下降，而加入四个干扰项会进一步加剧这种退化。

[图: /img/context_rot/niah/distractors_num.png]
干扰项的影响：按干扰项数量划分的性能 - arXiv 草堆/PG 论文针
我们还能看到干扰项的影响并不均匀。例如，在 arXiv 草堆与 PG 论文针的组合中，我们可以看到干扰项 3（红色）相对其他干扰项导致了更大的性能下降。

[图: /img/context_rot/niah/distractors_ind.png]
干扰项的影响：按单个干扰项划分的性能 - arXiv 草堆/PG 论文针
为了进一步研究这种不均匀的影响，我们分析了各模型在 4 干扰项条件下的失败尝试。对于 arXiv 草堆和 PG 论文针的组合，我们看到干扰项 2 和 3 在各模型的幻觉回答中出现得最为频繁。

[图: /img/context_rot/niah/hallucinations.png]
干扰项的影响：失败分析 - arXiv 草堆/PG 论文针
这些失败还揭示了模型在应对歧义时的模型特定差异。Claude 模型始终表现出最低的幻觉率。具体而言，Claude Sonnet 4 和 Opus 4 尤其保守，在不确定时倾向于弃权（abstain），并明确声明无法找到答案。相比之下，GPT 模型表现出最高的幻觉率，在存在干扰项时经常生成看似自信但错误的回答。

# 

针-草堆相似度#

在长上下文任务中，无关上下文常被当作一个中性的占位符来放大输入长度。通常假设这些无关上下文的内容无关紧要，只要它不直接干扰任务即可。

然而，一个自然而然的问题随之而来：针-草堆相似度究竟会不会影响任务难度？直觉上，如果针与草堆内容融为一体，模型提取针的难度可能会更大。

我们的发现表明，针-草堆相似度对模型性能具有不均匀的影响。

## 

实验#

利用针-问题相似度实验中的针，我们设置了实验来测试针-草堆相似度的影响。

我们通过对草堆做嵌入、为每个针检索相似度最高的前五个块（chunk），然后对其余弦相似度分数取平均，来衡量针-草堆相似度。为稳健起见，这一过程在五种不同的嵌入模型上重复执行。

在 PG 论文草堆中，PG 论文针的平均针-草堆相似度分数为 0.529，变异为 0.101，而 arXiv 针的平均针-草堆相似度为 0.368，变异为 0.111。相反，在 arXiv 草堆中，arXiv 针的平均针-草堆相似度为 0.654，变异为 0.0858，而 PG 论文针得分较低，为 0.394，变异为 0.105。

在每个草堆上，我们将语义相似的针与不相关的针进行对比测试。例如，我们将 PG 论文针和 arXiv 针都放入一个 Paul Graham 论文草堆中，以比较两种条件：

[图: /img/context_rot/niah/needle_haystack.png]
针-草堆相似度：实验设置
## 

结果#

我们在两种草堆类型（Paul Graham 论文和 arXiv 论文）中测试了 PG 论文针和 arXiv 针。在 Paul Graham 论文草堆中，arXiv 针的表现显著优于 PG 论文针；换言之，当针不与草堆在语义上融为一体时，模型表现更好。然而，在 arXiv 草堆中，我们观察到 arXiv 针和 PG 论文针之间只有极小的性能差异。

[图: /img/context_rot/niah/needle_haystack_2.png]
针-草堆相似度结果
仅跨两个主题进行测试，不足以得出“更高的针-草堆相似度会降低模型在该任务上的性能”这一可推广的结论。不过这确实凸显了长上下文处理的非均匀特性。即使在任务结构和针-问题相似度都保持不变的情况下，改变针与草堆之间的语义相似度也会影响结果。这指向了长上下文基准中一个尚未充分探索的领域，也是未来研究的一个有意义方向。

# 

草堆结构#

除了针-草堆相似度，我们还考虑了草堆的结构模式。

如果草堆由连贯的论文组成，随机插入的针可能会破坏思路的逻辑流，使其更加显眼。相反，在由随机排序句子组成的打乱草堆中，由于整体上下文缺乏结构，针可能更容易融入其中。这符合如下假设：模型对上下文的逻辑流是敏感的——会以结构化、对顺序敏感的方式处理它。

令人惊讶的是，我们发现结构连贯性始终损害模型性能。

虽然这看似违反直觉，但当草堆保留思路的逻辑流时，模型表现得更差。打乱草堆并移除局部连贯性反而始终能提升性能。

## 

实验#

为了评估草堆结构的影响，我们创建了两个变体：

- 原始（Original）：保留每段摘录内自然的思路流

- 打乱（Shuffled）：在整个草堆中随机重排句子，保持相同的整体主题但没有逻辑连续性

[图: /img/context_rot/niah/nh2.png]
草堆结构：实验设置示例
## 

结果#

在所有 18 个模型和针-草堆配置中，我们观察到一个一致的模式：模型在打乱的草堆上比在逻辑结构的草堆上表现更好。

[图: /img/context_rot/niah/structure_2.png]
草堆结构：18 个模型在原始与打乱草堆上的平均性能
这些结果可能对模型的内部处理具有一定启示：输入的结构模式可能影响注意力机制的运用方式，尤其是在输入长度增加时。

尽管超出了本报告的范围，但这为可解释性研究指出了一个潜在方向，即注意力如何受输入结构的影响。理解这些随输入长度增加而产生的结构影响，或许有助于解释这些长上下文失败模式。

# 

LongMemEval#

为了在更贴近真实的环境中评估这些模型，我们使用 LongMemEval，一个用于对话式问答的长上下文基准。

对于聊天助手而言，使用长输入是维持后续对话相关历史的一种常见做法。要把“记忆”纳入聊天助手，一种朴素的做法是将完整的聊天历史包含到后续对话的提示中。这要求模型在一次调用中通常完成两项任务：找到对话历史中相关的部分（检索），然后以对传入查询有用的方式综合它们（推理）。

在理想情况下，模型只会被给予相关部分，从而可以专注于推理。加入无关上下文会增加“识别何为相关”这一额外步骤，迫使模型同时执行两项任务。

我们通过两种条件系统地测试了随输入长度增加而加入这一额外步骤的效果：

- 
聚焦输入，仅包含相关部分，因此模型只需进行简单推理。

- 
完整输入，利用包含无关上下文的完整 113k token 的 LongMemEval 输入。在这种情况下，模型除了推理之外，还必须在长上下文中执行检索。

我们验证了这些模型在聚焦输入上具有很强成功能力，随后观察到它们在完整输入上性能持续下降。这种性能下滑表明，加入无关上下文从而加入额外的检索步骤，会显著影响模型维持可靠性能的能力。

## 

实验#

给定一段用户与助手之间的聊天历史，模型的任务是回答与聊天历史某一部分相关的问题。

[图: /img/context_rot/longmemeval/ex.png]
LongMemEval - 按问题类型划分的示例 [[2](#longmemeval-source)]
我们使用 LongMemEval_s，并筛选出属于知识更新、时序推理和多会话类别的任务。随后我们手工清洗这一数据集，因为有些问题过于含糊和/或无法回答，最终筛除 38 个提示，得到 306 个提示。这些提示平均约 113k token。

这些长提示大多由与问题无关的内容组成，有时还包含看似与问题相关的干扰项。我们将模型在这些长提示上的性能与聚焦版本进行比较，聚焦版本仅包含回答问题所需的相关部分。

聚焦提示平均约 300 token，源自原始标注数据集和手工调整。

模型输出使用一个对齐的 LLM 裁判（GPT-4.1，与人类判断的对齐度超过 99%）进行评判。

## 

结果#

在所有模型中，我们看到聚焦提示上的性能显著高于完整提示。

[图: /img/context_rot/longmemeval/claude.png]
LongMemEval 结果 - Claude 家族
Claude 模型在聚焦与完整提示性能之间表现出最明显的差距。这一差距主要由歧义引发的弃权导致，进而造成模型不确定性，类似于该模型族在 NIAH 中面对干扰项时的行为。这一行为在 Claude Opus 4 和 Sonnet 4 上最为明显，它们在歧义下似乎特别保守，导致在完整提示上的性能相对较老的 Claude 模型更低。

> 

问题：从我参加园艺工作坊那天到我种下番茄苗那天，中间隔了多少天？

正确答案：6 天。7 天（含最后一天）也可接受。

模型输出：我无法确定园艺工作坊与种植番茄苗之间相隔的天数，因为聊天历史中并未提供这些事件的具体日期。

LongMemEval - Claude Sonnet 4（非思考模式）在包含日期的完整提示上的表现
聚焦提示上更强性能的趋势同样适用于 GPT、Gemini 和 Qwen 模型族。对于支持思考模式的模型，我们看到启用后其在聚焦和完整提示上都有显著提升。然而，即使在最新模型上拥有完整的推理能力，两种输入长度之间仍然存在性能差距。

[图: /img/context_rot/longmemeval/gpt.png]
LongMemEval 结果 - GPT 家族
[图: /img/context_rot/longmemeval/gemini.png]
LongMemEval 结果 - Gemini 家族
[图: /img/context_rot/longmemeval/qwen.png]
LongMemEval 结果 - Qwen 家族
我们还观察到特定问题类型之间的模式。在非思考模式下，模型通常在知识更新上表现最好，其次是多会话，再次是时序推理——无论是聚焦还是完整提示均如此。然而，当启用思考模式时，这一排序变为：知识更新、时序推理，然后是多会话。

[图: /img/context_rot/longmemeval/claude_comparison.png]
按问题类型划分的 LongMemEval 结果 - Claude Opus 4
# 

重复词#

我们此前的实验探讨了输入长度本身如何影响模型性能。但当输出长度随输入一起扩展时又会怎样？由于这些模型是自回归的，模型的输出也属于其输入的一部分；每个 token 都是基于输入以及到该点为止已生成的 token 有条件地生成的。

考虑一个将字符串重复 n 次的基本程序——它每次都产生相同的输出。对于这样一个简单的任务，我们会期望这些模型同样可靠，并愿意将它们视作计算系统。

然而，我们的发现表明，即使对于这些简单的任务，随着上下文长度（包含输入和输出长度）的增长，模型性能也会变得不均匀。

## 

实验#

我们设计了一个受控任务，要求模型复现一段重复词的序列，其中在特定位置插入了一个唯一词。提示明确指示模型逐字复现输入文本。

一个示例提示是：

> 

只需复现以下文本，输出完全相同的文本：apple apple apple apple apples apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple

重复词 - 以 'apple' 作为重复词、'apples' 作为唯一词的示例提示
对于给定的词组合，我们创建了 1090 个上下文长度和唯一词索引的变体：

- 词数：25、50、75、100、250、500、750、1000、2500、5000、7500、10000

- 索引：
- 当 num_words <= 100 时：每个可能的位置

- 否则：以 num_words // 100 为步长递增

我们对以下词组合执行该任务：

- 常见词：“apple” | 唯一词：“apples”

- 常见词：“apples” | 唯一词：“apple”

- 常见词：“golden” | 唯一词：“Golden”

- 常见词：“orange” | 唯一词：“run”

- 常见词：“orange” | 唯一词：“San Francisco”

- 常见词：“San Francisco” | 唯一词：“sf”

- 常见词："Golden Gate Bridge" | 唯一词："Golden Gate Park"

注意："San Francisco" = 1 个词，"Golden Gate Bridge/Park" = 1 个词

模型配置：

- max_output_tokens = input_tokens *2（最高不超过模型的最大输出 Token 上限，旧模型通常更低）

- temperature = 0

- thinking = max(0, minimum_thinking_budget)

对于推理模型，我们将其思考预算设为 0 或最小值（例如 Gemini 2.5 Pro 设为 128 个 Token）。我们排除了 OpenAI 的 o3，因为它不支持基于 Token 的思考预算，也无法配置固定的输出长度，而这对于保持各次评测之间的一致性至关重要。

分数通过归一化 Levenshtein 距离计算。

我们遇到了模型未尝试执行任务的情况，判定依据如下：

- 
空输出但带有停止原因（即 GPT-3.5 turbo 的 finish_reason='content_filter'）

- 
输出非空，但输出无效：

- 
仅作观察而毫无尝试：

> 

我注意到文本中有一处不一致。原文中出现了一次 "apples"（而非 "apple"），位置大约在文本块的第 89 或 90 行左右。由于你要求我逐字复现相同的文本，我应当指出这一差异。你希望我：

- 完全按所示原样复现（保留这一处 "apples"）

- 将其更正为 "apple" 以与模式一致

- 直接按原样复现。请告诉我你希望我如何处理。

重复词——Claude Opus 4 输出
- 拒绝回答：

> 

抱歉，我无法提供这方面的帮助。

重复词——GPT-4.1 输出
- 随机输出：

> 

-\n-\n--\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-...

重复词——Gemini 2.5 Pro 输出
我们排除此类情况，并在结果中单独记录拒绝回答的百分比和常见模式。我们只纳入已尝试执行任务的情况，包括以如下开头短语开头的情况：

> 

我注意到文本中有一处不一致。在某一处，"apple" 变成了 "apples"（多了一个 's'）。我将按提供的文本逐字复现：

apple apple apple apple apple apple apple apple apple...

重复词——Claude Opus 4 输出
对于这些情况，我们采用相同的评分流程，对未严格遵循指令的模型进行轻微扣分。

我们完全排除了 GPT-3.5 turbo，因为该模型由于 finish_reason='content_filter' 在 60.29% 的任务中拒绝生成输出。

我们从以下几个维度分析输出：

- 
归一化 Levenshtein 距离

- 
唯一词的存在与位置

- 正确：唯一词存在且出现在正确的索引位置

- 位置错误：唯一词出现，但索引位置错误

- 
词数差异（输入词数 − 生成词数）

## 

结果#

随着上下文长度增加，所有模型的性能均一致地下降。在本实验中，输入长度与输出长度成正比，这不同于我们此前的测试——在那些测试中输出长度保持在相对固定的较短长度。这一设定使我们能够评估模型可靠复现长序列的能力。

我们还观察到模型不尝试执行任务的模式，这一现象在所有模型家族中都存在。

[图: /img/context_rot/repeated_words/claude_line_plot.png]
重复词——Claude 家族
我们观察到 Sonnet 3.5（红色）在其最大输出 Token 数 8192 以内优于较新的 Claude 模型。Opus 4（蓝色）虽然退化速度最慢，但也是该家族中唯一拒绝执行任务的模型（占尝试次数的 2.89%）。

Opus 4 的一个常见模式是：模型会先作出观察，再决定是否继续，随后进行尝试或不尝试。这种行为通常从 2500 个词开始出现。

也有 Opus 4 因以下原因直接拒绝尝试执行任务的情况：

- 生成受版权保护材料的风险

> 

我无法按请求逐字复现该文本。尽管它看起来只是 "San Francisco" 的重复，但当被要求逐字复现文本时，我应当避免这样做，因为这可能被用来测试我在其他场景下是否会复现受版权保护的材料。

不过，我可以告诉你，该文本包含 "sf"，后面跟着重复 24 次的短语 "San Francisco"。

重复词——Claude Opus 4 输出
- 重复序列中的不一致

> 

我注意到你提供的文本中有一处错误。有一处 "San Francisco" 显示为 "San Francisco sf San Francisco"（中间多了一个 "sf"）。由于你要求我逐字复现该文本，而源文本包含这一不一致之处，我无法提供完美的复现。

该文本由重复多次的 "San Francisco" 组成，但其中嵌入了这一处错误。

重复词——Claude Opus 4 输出
我们还测量了位置准确率：即唯一词是否出现在正确的位置。当唯一词被放置在序列开头附近时，准确率最高，尤其是随着输入长度增加时更是如此。

[图: /img/context_rot/repeated_words/claude_position_accuracy.png]
重复词：位置准确率——Claude 家族
此外，随着上下文长度增加，模型往往会一直生成重复词，直到达到输出 Token 上限。我们通过计算输入与输出词数之差来量化这一现象：

- 正值 = 模型生成不足

- 负值 = 模型生成过度

[图: /img/context_rot/repeated_words/claude_num_words.png]
重复词：词数差异——Claude 家族
在 GPT 模型家族中，我们观察到 GPT-4.1 的拒绝率为 2.55%。这些拒绝通常从约 2500 个词开始出现，回复如 "抱歉，我无法提供这方面的帮助。"

[图: /img/context_rot/repeated_words/gpt_line_plot.png]
重复词——GPT 家族
我们还观察到 GPT-4 turbo 在约 500 个词处出现一个局部性能峰值。在 50 到 250 个词之间，该模型倾向于过度生成（将常见词重复到输出上限），但在 500 个词时，其词数变得更准确。然而，超过这一点之后，它开始生成不足，这体现在输入与输出词数差为正值。

[图: /img/context_rot/repeated_words/gpt_4_turbo.png]
重复词：词数差异——GPT-4 Turbo
位置准确率呈现相似趋势，因为当唯一词在输入中较早出现时，GPT 模型也更可能将其放置在正确位置。

我们还注意到该家族中更多针对具体模型的行为。

GPT-4.1 mini 会尝试所有任务，但有时会为 "Golden Gate Bridge"/"Golden Gate Park" 组合生成随机词。随机输出被定义为输入中不存在的词或词序列。

该模型会输出重复词，例如 "Golden Golden" 和 "Gate Gate"，这些词在输入中并不存在（输入只包含 "Golden Gate Bridge" 和 "Golden Gate Park"）。

这些重复词并非出现在唯一词的位置，而是出现在文本中更靠后的位置。

GPT-4.1 nano 在 "San Francisco" / "sf" 组合上表现出类似行为，偶尔会输出小写的 "san"。

> 

模型输出片段：

San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco san Francisco san Francisco san Francisco san Francisco

金标准参考中对应部分：

San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco

重复词——GPT-4.1 nano
在这些随机词中，我们注意到与位置相关的一些结构迹象。我们观察到唯一词的位置与随机词开始出现的位置之间存在相关性，这或许是未来研究的一个方向。

GPT-4 Turbo 在该家族中输出最为多变，这意味着该模型更倾向于生成随机输出，且输出的多样性更高。

[图: /img/context_rot/repeated_words/gemini_line_plot.png]
重复词——Gemini 家族
总体而言，随着上下文长度增加，我们看到各模型性能均出现退化。对于 Gemini 2.5 Pro（蓝色），我们观察到其起点较低，因为在 50 个词时，该模型生成的词少于应有数量。

在该家族的所有词组合与模型中——除了 Gemini 2.5 Flash 在 "apples" / "apple" 上的表现——我们都观察到生成了输入中不存在的随机词。这通常从约 500–750 个词开始出现，其中 Gemini 2.5 Pro 的变异性最大，其次是 2.0 Flash，再次是 2.5 Flash。

> 

"golden" | "Golden"（2,500 个词）：

- - "I'-a-le-le-le-le-le-le-'a-le-le-le-le-le-le-le--le-le-le-le-le-le-le...

"orange" | "run"（10,000 个词）：

orange orange orange--g.-g/2021/01/20/orange-county-california-sheriff-deputies-wore...

重复词——Gemini 2.5 Pro 输出样例
[图: /img/context_rot/repeated_words/qwen_line_plot.png]
重复词——Qwen 家族
我们仅在 Qwen3-8B 上观察到未尝试的情况，占任务的 4.21%。对于该模型，我们观察到随机输出从约 5000 个词开始出现：

> 

好的，我要休息一下。告诉我，我现在没心情。我需要放松一下。我要去某个地方透透气。也许去海滩，或者随便找个地方放松。我不知道，但我需要休息一下。告诉我，我现在没心情。我需要放松一下。我要去某个地方透透气。也许去海滩，或者随便找个地方放松。我不知道，但我需要休息一下。告诉我，我现在没心情。我需要放松一下。我要去某个地方透透气。也许去海滩，或者随便找个地方放松。我不知道，但我需要休息一下。告诉我，我现在没心情。我需要放松一下。我要去某个地方透透气。也许去海滩，或者随便找个地方放松。我不知道，但我需要休息一下。告诉我，我现在没心情。我需要放松一下。我要去某个地方...

重复词——Qwen3-8B 在 'golden' | 'Golden' 上的输出（5,000 个词）
# 

局限与未来工作#

我们的实验表明，即使对于简单任务，LLM 在不同上下文长度下的性能也不一致。然而，这一评测并未穷尽现实世界中的使用场景。在实践中，长上下文应用往往复杂得多，需要综合归纳或多步推理。根据我们的发现，我们预计在这些条件下性能退化会更加严重。

我们的结果对未来的长上下文评测工作也有启示。一个常见的局限——此前关于长上下文基准的工作也曾指出——是将输入长度与任务难度混为一谈的倾向，因为更长的输入往往会引入更复杂的推理。我们的实验聚焦于将输入长度作为独立因素加以隔离，同时保持任务难度恒定。未来工作的一个重要方向是厘清模型的性能退化有多少源于任务本身的固有难度，又有多少源于其有效处理长上下文的能力。

我们也未解释这种性能退化背后的机制。我们的观察表明，上下文的结构特性——例如相关信息的放置位置或重复——会影响模型行为，然而我们对其发生原因尚无定论。研究这些效应需要更深入地探究机制可解释性，而这超出了本报告的范围。

更广泛地看，我们的发现指向了上下文工程的重要性：即对模型上下文窗口的精心构建与管理。信息在模型上下文中的呈现位置与方式会强烈影响任务性能，这使其成为优化模型性能的一个有意义的未来工作方向。

# 

结论#

通过我们的实验，我们证明了 LLM 在不同输入长度下无法保持一致的性能。即使在非词汇检索或文本复现这样简单的任务上，随着输入长度增长，我们也看到性能的不均匀性不断增加。

我们的结果凸显了在现有基准之外进行更严格的长上下文评测的必要性，以及上下文工程的重要性。相关信息是否存在于模型上下文中并非唯一关键；更重要的是这些信息如何呈现。我们证明了即使是最强大的模型对此也十分敏感，这使得有效的上下文工程对于可靠性能至关重要。

# 

脚注#

[1]（2025 年 7 月 16 日）由 Kiran Vodrahalli（Google Deepmind）补充 Latent List 洞察并作出澄清

[2] 示例的原始来源：https://arxiv.org/pdf/2410.10813

# 

参考文献#

[1] Kamradt, G. (2023). Needle In A Haystack - Pressure Testing LLMs [GitHub 仓库]. 链接

[2] Wu, D., Wang, H., Yu, W., Zhang, Y., Chang, K.-W., and Yu, D. (2025). LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. arXiv preprint arXiv:2410.10813. 链接

[3] Gemini Team, Georgiev, P., Lei, V. I., Burnell, R., Bai, L., Gulati, A., Tanzer, G., Vincent, D., Pan, Z., Wang, S., et al. (2024). Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. arXiv preprint arXiv:2403.05530. 链接

[4] OpenAI, Kumar, A., Yu, J., Hallman, J., Pokrass, M., Goucher, A., Ganesh, A., Cheng, B., McKinzie, B., Zhang, B., Koch, C., et al. (2025). Introducing GPT-4.1 in the API. 链接

[5] Meta AI, (2025). The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation. 链接

[6] Modarressi, A., Deilamsalehy, H., Dernoncourt, F., Bui, T., Rossi, R. A., Yoon, S., and Schütze, H. (2025). NoLiMa: Long-Context Evaluation Beyond Literal Matching. arXiv preprint arXiv:2502.05167. 链接

[7] Fu, H. Y., Shrivastava, A., Moore, J., West, P., Tan, C., and Holtzman, A. (2025). AbsenceBench: Language Models Can't Tell What's Missing. arXiv preprint arXiv:2506.11440. 链接

[8] Vodrahalli, K., Ontanon, S., Tripuraneni, N., Xu, K., Jain, S., Shivanna, R., Hui, J., Dikkala, N., Kazemi, M., Fatemi, B., et al. (2024). Michelangelo: Long Context Evaluations Beyond Haystacks via Latent Structure Queries. arXiv preprint arXiv:2409.12640. 链接

[9] openai. (2025). mrcr [数据集]. Hugging Face. 链接

[10] openai. (2025). graphwalks [数据集]. Hugging Face. 链接

[11] Shi, F., Chen, X., Misra, K., Scales, N., Dohan, D., Chi, E., Schärli, N., and Zhou, D. (2023). Large Language Models Can Be Easily Distracted by Irrelevant Context. arXiv preprint arXiv:2302.00093. 链接

[12] jamescalam. (2024). ai-arxiv2 [数据集]. Hugging Face. 链接

[13] Peng, B., Quesnelle, J., Fan, H., and Shippole, E. (2023). YaRN: Efficient Context Window Extension of Large Language Models. arXiv preprint arXiv:2309.00071. 链接

[14] McInnes, L., Healy, J., and Melville, J. (2020). UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction. arXiv preprint arXiv:1802.03426. 链接

[15] Campello, R. J. G. B., Moulavi, D., and Sander, J. (2013). Density-Based Clustering Based on Hierarchical Density Estimates. In Pei, J., Tseng, V. S., Cao, L., Motoda, H., and Xu, G. (Eds.), Advances in Knowledge Discovery and Data Mining (PAKDD 2013), Lecture Notes in Computer Science, vol 7819. Springer, Berlin, Heidelberg. 链接

# 

附录#

清理后的 LongMemEval 数据集以及所用针/干扰项可在此处下载。

## 

LLM 评判器校准：#

我们使用 LLM 评判器来评测 NIAH 和 LongMemEval 实验的输出。这些评判器通过以下流程校准到人工判断：

- 
对模型输出子集进行人工标注为错误/正确（NIAH 约 500 个输出，LongMemEval 约 600 个输出）

- 
使用 GPT-4.1 对同一子集的模型输出进行「正确/错误」标注。

- 
通过衡量人类与模型判断一致的比例来计算对齐分数（alignment score）。

- 
根据对不一致情况的（misalignments）人工检查来迭代提示（prompt）。

- 
重复步骤 2-4，直到对齐分数达到 > 0.99。

## 

已测试的模型（Models Tested）#

由于上下文窗口（context window）或 thinking_budget 的限制，并非全部 18 个模型都包含在每个实验中。

### 

Anthropic#

- Claude Opus 4

- Claude Sonnet 4

- Claude Sonnet 3.7

- Claude Sonnet 3.5

- Claude Haiku 3.5

### 

OpenAI#

- o3

- GPT-4.1

- GPT-4.1 mini

- GPT-4.1 nano

- GPT-4o

- GPT-4 Turbo

- GPT-3.5 Turbo

### 

Google#

- Gemini 2.5 Pro

- Gemini 2.5 Flash

- Gemini 2.0 Flash

### 

Alibaba#

- Qwen3-235B-A22B

- Qwen3-32B

- Qwen3-8B

## 

使用的嵌入模型（Embedding Models Used）#

- text-embedding-3-small

- text-embedding-3-large

- jina-embeddings-v3 (input_type='text-matching')

- voyage-3-large (input_type=None)

- all-MiniLM-L6-v2

## 

针问题相似度（Needle-Question Similarity）#

注：同一模型的思考（thinking）/非思考（non-thinking）模式被分别处理

[图: /img/context_rot/appendix/arxiv_pg_nq_sim.png]
针问题相似度 —— arXiv 干草堆/PG 文章针
[图: /img/context_rot/appendix/pg_pg_nq_sim.png]
针问题相似度 —— PG 文章干草堆/PG 文章针
[图: /img/context_rot/appendix/pg_arxiv_nq_sim.png]
针问题相似度 —— PG 文章干草堆/arXiv 针
正如我们在「针-干草堆相似度」结果中所提到的，我们注意到这一处情况：与其他针-干草堆组合相比，模型表现异常出色。单独来看，高表现模型似乎表现一致。然而，对于这些模型而言，这种一致性在其余实验中并不成立。

## 

干扰项的影响（Impact of Distractors）#

[图: /img/context_rot/appendix/distractors_num_arxiv.png]
干扰项的影响：按干扰项数量衡量的表现 —— arXiv 干草堆/arXiv 针
[图: /img/context_rot/appendix/distractors_ind_arxiv.png]
干扰项的影响：按单个干扰项衡量的表现 —— arXiv 干草堆/arXiv 针
[图: /img/context_rot/appendix/distractors_num_pg.png]
干扰项的影响：按干扰项数量衡量的表现 —— PG 文章干草堆/PG 文章针
[图: /img/context_rot/appendix/distractors_ind_pg.png]
干扰项的影响：按单个干扰项衡量的表现 —— PG 文章干草堆/PG 文章针
[图: /img/context_rot/appendix/distractors_num_pg_arxiv.png]
干扰项的影响：按干扰项数量衡量的表现 —— PG 文章干草堆/arXiv 针
[图: /img/context_rot/appendix/distractors_ind_pg_arxiv.png]
干扰项的影响：按单个干扰项衡量的表现 —— PG 文章干草堆/arXiv 针
[图: /img/context_rot/appendix/failures_arxiv.png]
干扰项的影响：失败分析 —— arXiv 干草堆/arXiv 针
[图: /img/context_rot/appendix/failures_writing.png]
干扰项的影响：失败分析 —— PG 文章干草堆/PG 文章针
[图: /img/context_rot/appendix/failures_writing_arxiv.png]
干扰项的影响：失败分析 —— PG 文章干草堆/arXiv 针
## 

重复词（Repeated Words）#

[图: /img/context_rot/appendix/gpt_position_accuracy.png]
重复词：位置准确度 —— GPT 系列
[图: /img/context_rot/appendix/gemini_position_accuracy.png]
重复词：位置准确度 —— Gemini 系列
[图: /img/context_rot/appendix/qwen_position_accuracy.png]
重复词：位置准确度 —— Qwen 系列
[图: /img/context_rot/appendix/wc_gpt.png]
重复词：词数差异 —— GPT 系列
[图: /img/context_rot/appendix/wc_gemini.png]
重复词：词数差异 —— Gemini 系列
[图: /img/context_rot/appendix/wc_qwen.png]
重复词：词数差异 —— Qwen 系列
[图: Watch video]观看视频
### ─目录（Contents）

- ○引言（Introduction）

- ○相关工作（Related Work）

- ○干草堆中的针扩展（Needle in a Haystack Extension）

- ○针问题相似度

- ○干扰项的影响

- ○针-干草堆相似度

- ○干草堆结构（Haystack Structure）

- ○LongMemEval

- ○重复词

- ○局限性与未来工作（Limitations & Future Work）

- ○结论（Conclusion）

- ○脚注（Footnotes）

- ○参考文献（References）

- ○附录（Appendix）

[图: Chroma logo]
© 2026

### 产品（Product）
DatabaseSyncEnterprisePackage Search MCPDocsStatusContact

### 关注（Follow）
GitHubXYouTube

### 公司（Company）
AboutChangelogCareers

### 法律（Legal）
PrivacyTermsSecurity