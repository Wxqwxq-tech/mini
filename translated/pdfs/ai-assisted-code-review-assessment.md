<!-- page 1 -->
现代代码评审中编码实践的 AI 辅助评估
Manushree Vijayvergiya
manushree@google.com
Google
瑞士苏黎世
Małgorzata Salawa
magorzata@google.com
Google
瑞士苏黎世
Ivan Budiselić
ibudiselic@google.com
Google
瑞士苏黎世
Dan Zheng
danielzheng@google.com
Google
美国山景城
Pascal Lamblin
lamblinp@google.com
Google
加拿大蒙特利尔
Marko Ivanković
markoi@google.com
Google
瑞士苏黎世
Juanjo Carin
juanjocarin@google.com
Google
美国森尼韦尔
Mateusz Lewko
mlewko@google.com
Google
瑞士苏黎世
Jovan Andonov
jandonov@google.com
Google
瑞士苏黎世
Goran Petrović
goranpetrovic@google.com
Google
瑞士苏黎世
Daniel Tarlow
dtarlow@google.com
Google
加拿大蒙特利尔
Petros Maniatis
maniatis@google.com
Google
美国山景城
René Just∗
rjust@cs.washington.edu
华盛顿大学
美国西雅图
摘要
现代代码评审是一个流程：代码作者所做的增量代码贡献在提交到版本控制系统之前，由一个或多个同行进行评审。现代代码评审的一个重要环节是验证代码贡献是否符合最佳实践。虽然其中一些最佳实践可以自动验证，但另一些通常仍交由人工评审者来验证。本文报告了 AutoCommenter 的开发、部署与评估情况。AutoCommenter 是一个由大语言模型支撑的系统，能够自动学习并执行编码最佳实践。我们为四种编程语言（C++、Java、Python 和 Go）实现了 AutoCommenter，并在一个大型工业环境中评估了其性能与采用情况。我们的评估表明，一个用于学习并执行编码最佳实践的端到端系统是可行的，并且对开发者工作流具有积极影响。此外，本文还报告了将这样一个系统部署到数万名开发者所面临的挑战以及相应的经验教训。
CCS 概念
• 软件及其工程 →软件验证与确认。
∗本文工作完成于 Google。
允许个人或课堂使用免费制作本作品全部或部分的数字或纸质副本，前提是此类副本不得用于牟利或商业目的进行制作或分发，且副本需在首页保留本声明及完整引用信息。本作品中第三方组件的版权应得到尊重。如需其他用途，请联系版权所有者/作者。
AIware '24，2024 年 7 月 15–16 日，巴西加利尼亚斯港
© 2024 版权归所有者/作者所有。
ACM ISBN 979-8-4007-0685-1/24/07
https://doi.org/10.1145/3664646.3665664
关键词
人工智能、代码评审、编码最佳实践
ACM 引用格式：
Manushree Vijayvergiya, Małgorzata Salawa, Ivan Budiselić, Dan Zheng,
Pascal Lamblin, Marko Ivanković, Juanjo Carin, Mateusz Lewko, Jovan An-
donov, Goran Petrović, Daniel Tarlow, Petros Maniatis, and René Just. 2024.
现代代码评审中编码实践的 AI 辅助评估. In
Proceedings of the 1st ACM International Conference on AI-Powered Software
(AIware '24), July 15–16, 2024, Porto de Galinhas, Brazil. ACM, New York,
NY, USA, 9 pages. https://doi.org/10.1145/3664646.3665664
1
引言
现代代码评审 [21, 23]（相较于整体式代码评审 [8]）多年来在开源和工业环境中自然发展壮大。一套通用的同行评审标准已经形成 [5, 20, 21]，其中包括编码最佳实践。许多公司、项目乃至编程语言都以“风格指南”[1–4] 的形式对其做了正式定义，这些指南通常涵盖以下几个方面：
• 格式化：行宽限制、空格与缩进的使用、圆括号与方括号的位置等；
• 命名：大小写、简洁性、描述性等；
• 文档：文件级、函数级及其他注释的预期位置与内容；
• 语言特性：在不同（代码）上下文中对特定语言特性的使用；
• 代码惯用法：运用代码惯用法以提升代码的清晰度、模块化与可维护性。
开发者普遍对现代代码评审流程表示高度满意 [23, 28]。其主要好处之一在于，为不熟悉代码库、特定语言特性或常见代码惯用法的代码作者提供了学习体验。在评审过程中，除了评审（并了解）代码贡献及其影响之外，专家级开发者还会就最佳实践对代码作者进行指导。
arXiv:2405.13565v1  [cs.SE]  22 May 2024

<!-- page 2 -->
AIware '24，2024 年 7 月 15–16 日，巴西加利尼亚斯港
Manushree Vijayvergiya et al.
诸如 Linter 之类的静态分析工具 [15] 能够自动验证代码是否遵循某些最佳实践（例如格式化规则），有些工具甚至能自动修复违规之处。然而，那些细致入微或存在例外情况的准则难以被完整地自动验证（例如命名约定以及遗留代码中合理的偏离），而有些准则根本无法用精确的规则来刻画（例如代码注释的清晰性与明确性），只能依赖人的判断和开发者群体的集体知识。因此，通常期望由人工评审者来检查代码变更是否存在违反最佳实践的情况。
代码评审流程最大的成本在于所需的时间，尤其是专家级开发者的时间。即便已有显著的自动化，且尽力让流程保持轻量，一名开发者每天仍可能轻松地在这项任务上投入数小时 [23]。机器学习的最新进展，尤其是大语言模型（LLM）的能力，表明 LLM 适合用于代码评审自动化（例如 [11, 16, 17, 24–26]）。然而，围绕在大规模下部署端到端系统所面临的软件工程挑战仍未被探索。同样，对此类系统在整体效能与用户接受度方面的外部评估也尚付阙如。
本文探讨能否对代码评审流程进行部分自动化，特别是对违反最佳实践情况的检测，从而为代码作者提供及时反馈，并让评审者专注于整体功能。具体而言，本文报告了我们在 Google 的工业环境中开发、部署并评估 AutoCommenter——一个自动化代码评审助手——的经验；目前它每天被数万名开发者使用。
总而言之，本文的贡献如下：
• 一个基于 LLM 的代码评审助手系统的通用架构（第 3 节）。
• 对工具校准及其向数万名开发者部署的描述（第 4 节）。
• 对该系统的评估（第 5 节）。
• 对经验教训的总结与讨论（第 6 节）。
2
背景
AutoCommenter 是在 Google 的大型工业环境中开发的。Google 的现代代码评审实践与其他工业项目及开源项目类似 [23]。
2.1
代码评审流程
Google 的代码评审流程非常成熟，以变更为基础，并有工具辅助。Ivanković 等人 [12] 和 Petrović 等人 [18] 对该流程做了详细总结。对代码库的每一次变更都必须经过至少一名其他开发者的评审。每天，代码库中都有数万处变更经过评审流程，数万名开发者以代码作者和评审者的双重身份参与其中。
作者与评审者通过代码评审系统交换评论，一次评审随着受变更影响文件的快照逐轮推进。每条评审者评论都附加在特定文件快照中的特定行列区间上。为了解决一条评论，作者通常会在其本地副本中修改文件，并导出一个新快照以供下一轮代码评审使用。
图 1：人工评审者发布的一条示例评论。
当作者和所有评审者都满意、且没有任何自动化分析阻塞合并时，代码即被合并到代码库中。
代码评审流程中成本最高的部分是代码作者与评审者“护送”一次变更所花费的时间（从最初的编码，到处理评审者评论、确保所有自动化分析通过，直至最终将变更合并到代码库中）。尽管该流程已通过自动化系统在评审前对代码进行分析而得到优化（尤其是不需人工干预的自动代码格式化），代码评审每年仍要耗费数千个开发者·年。因此，即便只是个位百分比的节省，也能转化为显著的商业影响。
2.2
最佳实践
最佳实践是指被认为更优的编程语言的某种特定用法；最佳实践文档则描述了应当如何应用它以及它能带来哪些好处。最佳实践 URL 指的是最佳实践文档或其中的某个具体章节；最佳实践违规指的是一段不符合某条最佳实践、但可以修改为符合的代码。在上下文清楚的情况下，我们分别用 URL 和违规来指代最佳实践 URL 与最佳实践违规。
Google 的中央代码仓库包含多种语言的代码，其中 C++、Java、Python 和 Go 每种都超过 1 亿行 [19]。对于 15 种不同的语言，都有所有开发者可随时查阅的正式风格指南。其中许多语言还有额外的语言入门读物、核心库文档，以及“每周小贴士”式的通讯。尽管这些材料的执行不像风格指南那样严格，但它们在代码评审中经常被引用。有些语言拥有数百页此类文档。代码作者和评审者都应验证代码是否遵循了所有最佳实践。
一个名为“readability（可读性）”的正式机制于十多年前引入，用以确保最佳实践得到一贯遵循。针对特定语言的专业风格专家，被称为“readability mentor（可读性导师）”，指导经验不足的开发者熟练掌握该语言 [23]。可读性导师通常会先用几句话总结一条最佳实践，并在评论末尾附上一个 URL，供变更作者参考。图 1 展示了一条由可读性导师发布的评论的示例。

<!-- page 3 -->
现代代码评审中编码实践的 AI 辅助评估
AIware '24，2024 年 7 月 15–16 日，巴西加利尼亚斯港
训练与微调（按需）
工作节点
工作节点
工作节点
源代码
仓库
评论
存储
调度器
相关
代码
评论
工作节点
工作节点
工作节点
示例
（时间
划分）
工作节点
工作节点
TPU pod
Tensorboard
模型
检查点
输入/目标
格式
大规模预处理（周期性）
数据集整理（按需）
图 2：模型训练流水线的架构。
可读性流程也存在一些弊端。对作者而言，它会因额外的评审轮次而增加开发时间。对可读性导师而言，它可能变成一项单调而耗时的任务。这要求掌握数百条不断演进的最佳实践，包括识别并弃用过时的规则，并在代码评审系统中（附上相关链接）加以记录。此外，它还要求进行跟踪，有时需要经历多轮迭代，以确保所有违规都已被纠正。
3
方法
为应对第 2.1 节和第 2.2 节所述的挑战，我们开发了 AutoCommenter——一个能够自动检测最佳实践违规的代码分析工具。它旨在为代码作者提供及时反馈，并减轻人工最佳实践评审的负担，从而使评审者能够专注于代码功能。
3.1
模型与任务定义
自动进行最佳实践分析，需要一个能够表示源代码、精确定位违规位置并识别被违反的最佳实践的模型。我们以文本到文本的转换为目标，采用基于 T5 的传统 Transformer 方法，并使用 T5X [22]。
最佳实践分析是一个多任务大型序列模型中的一项任务。除了 T5 的标准预训练任务——跨度去噪（预测被遮蔽的 Token（令牌））之外，用于训练该模型的其他任务还包括代码评审评论消解、下一处编辑预测、变量重命名以及构建错误修复 [9]。训练语料包含超过 30 亿条示例，其中最佳实践分析数据集贡献了约 80 万条示例。该模型使用此类模型典型的标准交叉熵损失进行训练，并经过调优以最大化序列准确率指标，即为每条示例预测出精确的目标文本。
对于最佳实践分析，模型的输入是一个任务提示和源代码，目标则是源代码位置以及违反最佳实践所对应的 URL。任务提示以固定文本的代码注释形式格式化，采用相应编程语言合适的注释风格。它用自然语言描述任务，并置于源代码之前；源代码是单个文件的直接文本表示。如果输入超出模型的上下文窗口，则会被截断。位置是源代码中的字节偏移量，URL 则指向被违反的最佳实践。一种领域特定语言定义了目标格式；如果没有违规，则目标为“空”这一特殊情况。除了目标之外，模型还会输出一个介于 0 到 1 之间的置信度分数。
以下面这个 Go 语言的输入/目标示例为例。
输入
/ /
[ ∗]
Task :
Check
language
b e s t
p r a c t i c e s .
/ /
Package
a d d i t i o n
p r o v i d e s
Add
package
a d d i t i o n
/ /
Return a sum
func Add ( value1 ,
value2
int )
int
{
return
value1 + value2
}
目标
INSERT 153 COMMENT h t t p s : / / go . dev / doc / comment # func
输入的第一行是固定文本的任务提示，其余部分则是源代码。目标给出了位置（字节偏移量 153 对应于 Add 函数的起始位置）以及一个 go.dev 的 URL，指向该函数注释所违反的 Go 语言风格指南中的确切部分（在本例中，即通常应以函数名开头的注释写法）。请注意，根据源代码中违规的数量，目标可能包含零个、一个或多个（连接在一起的）位置-URL 对。
3.2
模型训练
图 2 展示了模型训练流水线的架构，它由三部分组成。我们将数据集创建拆分为两个步骤（预处理和整理），因为第一步操作的数据量大得多，成本也显著更高。预处理步骤的输出与模型的输入/目标表示方式无关。这种分离通过支持对示例表示及其他示例级调整的快速迭代，提升了特性开发速度。预处理步骤使用一个容错的调度系统，并周期性地提取相关代码评论，以确保新数据能够随时可用。
3.2.1
大规模预处理。训练示例来源于真实的代码评审数据，但并非所有代码评论都适合用于模型训练。因此，预处理步骤会识别相关代码评论——即那些包含指向最佳实践文档的 URL 的人工撰写的评论。对于每条评论，预处理步骤随后收集相应的源代码和相关元数据，包括该评论在源代码中的位置及其创建时间。该步骤的输出是一组相关代码评论，每条都带有为模型训练整理示例所需的全部数据。

<!-- page 4 -->
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil
Manushree Vijayvergiya et al.
3.2.2
数据集整理（Dataset curation）。数据集整理是一个一次性的、按需执行的处理步骤，以 Beam1 流水线（pipeline）实现。它根据第 3.1 节描述的输入/目标格式，将每条相关的代码注释（code comment）转换为标准的 TensorFlow Example 数据结构。
3.2.3
训练与微调（fine-tuning）。整理好的示例直接用于模型训练与评估。我们在一个 TPU 机群上使用 T5X 框架 [22]，每 1000 步保存一次模型检查点（checkpoint），并使用 Tensorboard 监控训练过程。
3.3
模型选择（Model Selection）
对历史数据的两项内在评估（intrinsic evaluation）为我们在模型检查点、置信度阈值（confidence threshold）与解码策略（decoding strategy）上的选择提供了依据。第一，在验证集与测试集上的评估提供了按文件粒度估算的精确率（precision）与召回率（recall）。第二，对完整历史代码评审（code review）的评估提供了每次代码评审中注释总数的估算，从而表明开发人员与 AutoCommenter 交互的频率。
3.3.1
验证集与测试集上的评估。我们按时间切分数据集，以确保模型没有在验证集与测试集代码注释的未来代码评审快照（code-review snapshot）上训练过。在我们的数据集中，85% 的文件恰好含有一条相关代码注释，11% 含两条，4% 含三条或更多。若预测出的代码位置与 URL 与期望值相匹配（不论顺序），我们即判定该预测正确。
回想一下，模型会为每个预测给出一个置信度分数（confidence score），这就引入了另一个参数：当某个预测的置信度分数低于某个阈值 𝑡 时，该预测可被抑制（suppress）。我们将 𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛𝑡定义为置信度分数大于 𝑡 的正确预测数，除以所有置信度分数大于 𝑡 的预测数；类似地定义 𝑅𝑒𝑐𝑎𝑙𝑙𝑡。这些定义使我们能够估计，作为 𝑡 的函数，会有多少（不）正确的结果被展示给用户。在训练过程中，𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛𝑡与 𝑅𝑒𝑐𝑎𝑙𝑙𝑡用于模型检查点之间的比较。
尽管这种评估避免了数据泄漏（data leakage），并使我们能够自动评估模型性能，但它有一个局限：虽然可以合理地假设给定代码评审快照中的人工注释是正确的，但它们并非详尽无遗。换句话说，某个给定代码评审快照中的代码，可能本可以依据多条最佳实践（best practice）加以改进，但人工评审者（reviewer）并未针对所有这些实践都发布注释（含 URL）。这可能由以下几种原因造成：
• 缺失引用（reference）：评审者可能针对某个问题发布了注释，但未附上 URL 作为引用。
• 选择性评论（selective commenting）：评审者可能只针对某个问题评论一次，期望作者（author）在整个代码中一并修正。
• 专业度或关注点各异：评审者可能并不熟悉所有最佳实践，或者只是在某次代码评审的语境下选择不对某个问题发表评论（例如只关注发生变更的代码）。
虽然我们数据集中的大多数文件只有一条相关注释，但通过人工检查“不正确”预测所得的轶事性证据（anecdotal evidence）表明，由于上述原因，通常可能存在多条最佳实践注释。鉴于我们的基准真值（ground truth）数据不完整，我们的精确率与召回率度量是带噪的（noisy）。
1https://beam.apache.org/
因此，我们采用了下一节所述的一项补充性评估，以提升对整体模型性能的信心。
3.3.2
完整历史代码评审上的评估。为准确衡量线上环境（live setting）中潜在的注释量，我们使用特定的模型检查点与阈值，在一组历史代码评审上评估 AutoCommenter。预测出的注释不会追溯性地发布到代码评审系统中，而是记录在数据库里以供分析。这使我们能够估算预期的发布频率——既包括按文件粒度，也包括按代码评审粒度。
由于开发人员在受到代码评审的整套代码变更（code change）上都会与 AutoCommenter 交互，这一评估是生产部署（production deployment）前的重要一步。作为额外收益，这一步还能针对不同用户群体、编程语言等进一步优化并评估发布频率。
3.4
推理基础设施（Inference Infrastructure）
AutoCommenter 的核心是一个中央最佳实践分析服务。该服务以一个或多个待分析的源文件作为输入。对每个文件，它构造一个模型输入（第 3.1 节），将其编码为标准 TensorFlow Example 数据结构，并查询模型。模型本身由一个模型服务提供，该服务使用 TensorFlow 的 Example 数据结构作为领域无关（domain agnostic）的输入输出格式。最后，最佳实践分析服务执行一系列过滤步骤（第 4 节），抑制低质量的预测，并返回剩余的预测结果。
3.5
IDE 与代码评审集成（Integration）
开发人员通过两种方式与 AutoCommenter 的分析服务交互——直接通过 IDE 插件，或间接通过代码评审系统。代码评审系统被 Google 的所有开发人员使用，IDE 也几乎被所有人使用。
AutoCommenter 的注释在 IDE 中以诊断信息（diagnostic）的形式呈现，标记为蓝色波浪下划线，覆盖相关的代码片段（code snippet）。将鼠标悬停在下划线代码上会显示完整注释，并附有最佳实践的简明摘要，包括一个指向相关最佳实践文档的可点击链接。这种内嵌信息消除了开发人员在 IDE 与网页浏览器之间切换以查询陌生最佳实践的需要，从而简化了工作流（workflow）。由于 IDE 中的注释需要实时生成，我们力求以亚秒级延迟（sub-second latency）生成注释。
在代码评审系统中，AutoCommenter 在每次更新之后（即在每个新的代码评审快照上）运行，若检测到任何违规（violation）就自动发布注释。自动化工具生成的注释在视觉上与人工生成的注释相似，但背景颜色不同。
图 3 展示了 AutoCommenter 在代码评审系统中生成并发布的一条示例注释。请注意右侧的“赞”和“踩”按钮，作者与评审者如果觉得某条注释特别有用或无用，可点击这些按钮。另请注意左侧的“Please fix”按钮，该按钮对评审者可见。若被点击，会生成一条新注释，表明该评审者认为此注释意义重大，必须在代码合并（merge）进代码库（codebase）之前加以处理。这些反馈按钮是代码评审系统中的标准组件，出现在所有自动化工具生成的注释上（例如 [7, 13]），并为工具的用户接受度（user acceptance）提供信号。IDE 也提供了类似的反馈机制。

<!-- page 5 -->
AI-Assisted Assessment of Coding Practices in Modern Code Review
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil
图 3：AutoCommenter 发布的示例注释。
4
部署（DEPLOYMENT）
我们在 2022 年 7 月至 2023 年 10 月期间，将 AutoCommenter 逐步部署给了 Google 的所有开发人员：
• 直至 2022 年 7 月——内部试用（teamfooding）：即本文作者。
• 2022 年 7 月——早期采用者（early adopters）：约 3 千名志愿者。
• 2023 年 7 月——A/B 实验：约占全体开发人员的一半。
• 自 2023 年 10 月起——全面可用（general availability）：所有开发人员。
请注意，出于行业保密（industrial confidentiality）原因，我们无法披露代码评审、开发人员、文件、注释的绝对数量，或代码评审时长的分布。我们在适当之处报告相对度量（relative measure）以及相关趋势。
我们采用迭代式精化（iterative refinement）的方法，持续评估并改进 AutoCommenter 的性能：
• 对历史数据的评估（第 3.3 节），以获得模型在该任务上表现如何的方向性洞察（directional insight），并据此定义阈值、选择解码策略。
• 通过反馈按钮与议题报告（issue report），监控并分析用户交互与直接反馈。
• 基于其他评估步骤中观察到的模式，进行有针对性的（targeted）人工评估。
图 4 展示了开发人员对已发布代码评审注释与 IDE 诊断信息的正负面反馈比例随时间的变化。虚线表示开发人员每月提供的反馈点击总数。如预期那样，在早期采用者阶段，这一计数要低得多。此外，由于我们在此期间积极改进 AutoCommenter，该阶段的波动性（volatility）也更高。
回想一下代码评审系统内的三个反馈按钮（图 3），它们允许开发人员对已发布的注释表达正面或负面情绪（sentiment）。我们将收到“赞”或“Please fix”的注释视为正面，收到“踩”的注释视为负面；我们将有用比率（useful ratio）定义为正面注释与所有收到反馈的注释之比。
本节其余部分描述我们在部署期间所做的具体观察与相应改进。
4.1
选择阈值与解码策略
4.1.1
阈值（Threshold）。在初期部署期间，我们希望谨慎管理开发人员对 AutoCommenter 的信任，因此从一个较高的置信度阈值 𝑡= 0.98 起步。我们人工抽样
图 4：部署过程中的开发人员反馈。
了数百条结果，观察到阈值以下的预测中约 80% 仍然是正确的——也就是说，在 𝑡= 0.98 时，假阴性率（false-negative rate）非常高。此外，我们观察到 Python 中预测的置信度分数分布显著不同，这些预测受到阈值化（thresholding）的不成比例的影响。我们推测，训练数据集的构成（不同 URL 的数量及 URL 频率）以及最佳实践文档的具体程度（specificity）是原因所在，但更深入的调查留待未来工作。尝试按语言部署阈值被证明无效，因为每种语言一个单一阈值仍然无法充分捕捉模型正确预测数百种多样最佳实践的能力。这导致预测 URL 缺乏多样性，因为无论正确与否，模型都倾向于对某些 URL 给出比另一些更高的分数。这些观察促成了 AutoCommenter 的第一次重大变更：基于验证集上的内在评估，计算按 URL 区分的阈值（per-URL threshold）。
4.1.2
解码（Decoding）。使用按 URL 阈值与贪心解码（greedy decoding）在完整历史代码评审上进行的一项评估显示，AutoCommenter 在全部变更文件中的 6% 上检测到违规。然而，80% 的注释本会被发布在作者未修改的代码行上。开发人员通常不会对未变更的代码采取行动。因此，AutoCommenter 过滤掉生成于未变更代码行上的注释，将变更文件中的注释比例降至 1.3%。为提高这一比例，我们实验了不同的解码策略：贪心（默认）、束搜索（beam search）、top-k 以及 top-p 采样（sampling）。我们最终选定束搜索（生成 𝑛= 4 个候选响应），它使发布频率提高两倍，达到 3.9%。它还带来了显著更高的 URL 多样性：最常发布的 10 个 URL 占全部注释的 41%，而贪心搜索则为 80%。
延迟（latency）是选择部署解码策略时的另一个重要方面。虽然束搜索提高了发布频率与多样性，但推理（inference）明显变慢（中位延迟为 2 秒）。鉴于这一延迟对 IDE 中的交互式使用而言不可接受，我们最终决定在代码评审系统中使用束搜索，而在 IDE 中使用贪心搜索。

<!-- page 6 -->
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil
Manushree Vijayvergiya et al.
4.2
抑制过时的最佳实践
在向约三千名自愿的首批试用者推出 AutoCommenter 之后，我们注意到在几天之内用户提交了大量议题（issues）。其中许多议题都对应同一个 URL2，该 URL 描述了与 Python 导入（imports）相关的最佳实践。然而，某些类型名称的权威来源在 Python 3.9 中已经发生了变化，而且该最佳实践也在 2022 年初发生了变更。由于我们的训练数据延伸到了 2022 年之前，其中包含了大量已不再适用的最佳实践注释。我们意识到这是一种反复出现的模式：随着语言的演进，或者新库的引入，最佳实践也在随之演变。缓解这一问题的一种方式是（每当规则发生变化时）过滤掉这类数据，并重新训练模型。然而，这样做既耗时又耗资源：它需要完整的数据再生成、模型训练、评估和上线发布。在此期间，这台“过时”的模型要么需要被关闭，从而造成系统停机，要么需要抑制其受影响的预测。否则，系统可能会迅速失去开发者的信任。我们选择抑制特定的最佳实践预测，使用条件过滤（在源代码上匹配正则表达式）来实现，原因有二。第一，它可以动态部署并立即生效。第二，它允许对预测进行细粒度的过滤。
4.3
对选定注释进行独立评分
在经历了数月的早期使用之后，我们观察到有用率（useful ratio）在 54% 左右趋于平稳。为了理解原因、识别改进方向，并为更大范围的部署做准备，我们在 2023 年 4 月进行了一项独立的人工评分研究，分析了在我们首批试用者部署期间收到开发者反馈的约 370 条已发布注释的样本。
为了收集关于注释有用性的多样化观点，我们招募了 15 名评分者——来自合作团队的开发者。我们请他们为收到明确用户反馈的 AutoCommenter 注释进行评分。我们没有向评分者展示原始的用户反馈，以避免对其评估产生偏差。评分者根据所关联的最佳实践以及周围的代码来评估每条注释的有用性。我们指导他们把重点放在注释的正确性上，同时也要考虑该注释对于作为作者（提交者）的他们来说是否具有可操作性（例如，他们是否会去解决一条技术上正确、但在特定场景下似乎不值得解决的注释）。我们鼓励他们对每条注释提供自由形式的反馈。
评分者评估得出的有用率为 60%，略高于同一批注释上开发者反馈的 54%，但远低于我们为更大范围部署所设定的 80% 的目标。这项研究中最有趣的发现是，无用注释存在着清晰的模式。以下是一些示例：
多个主题或复杂主题：例如，某个 URL 指向一个章节，该章节描述了与 Python Linter 交互的多条准则，包括它经常触发的情形以及抑制它的方法。作者可能难以理解一条已发布注释究竟指的是哪条具体准则，以及该如何解决它。类似地，关于在 C++ 中编写良好函数文档的指导是一整页密集的文本。评分者经常指出，即使代码中确实包含相关违规，最佳实践（以及 AutoCommenter 的简洁摘要）与实际代码之间仍存在脱节。
2https://github.com/google/styleguide/blob/gh-pages/pyguide.md#22-imports
高质量摘要的重要性：评分者经常发现，AutoCommenter 的摘要——它通过抓取文档源生成，有时还会缺失——未能充分说明被引用的准则与注释/代码之间的相关性。
主观且可能引发争议的主题：一个例子是避免在库代码中使用标志（flags）。标志在库中使用时可能会引发问题，但有些库是专门设计为通过标志来配置大量功能的。此外，遗留代码可能并不遵循这一准则，评审者也不会强制执行它。模型没有学到这些细微差别，有时会在作者向现有库添加一个新标志时预测出违规。
某些准则的系统性模型错误：一个有趣的例子是，有一条准则提倡对 C++ 的 vector 使用成员函数 push_back 而不是 emplace_back，前提是这两个函数可以用相同的参数达到相同的效果。模型已经学会了预测这一点，但它也会在应当使用 emplace_back 的情况下进行预测，以及在不相关类型拥有一个名为 push_back 的成员函数时进行预测。
正确但价值低的注释：代码注释中一句话末尾缺少句号，人类评审者通常是可以接受的。虽然在技术上正确，但要求作者回到他们的 IDE 中去修复这个问题，可能会带来净负价值。
评分研究的洞见促成了对 AutoCommenter 的两项改动。第一，评分研究识别出 17 个不可操作的 URL，对它们的抑制使历史有用率在开发者反馈上从 54% 提升到 66%，在评分者反馈上从 60% 提升到 74%。我们进一步分析了链接到类似、未经评分的 URL 的注释，并额外抑制了 5 个。第二，我们审查并手动更新了所有频繁发布 URL 的摘要。综合起来，这些改动足以让我们在下一阶段的部署中达到 80% 的目标有用率。
4.4
A/B 实验
2023 年 7 月，我们在一项 A/B 实验的背景下，将 AutoCommenter 部署给了大约一半的开发者。我们将开发者随机分配到实验组（启用 AutoCommenter）和对照组（禁用 AutoCommenter）。我们基于开发者电子邮件地址 SHA256 哈希值的最后几位数字进行随机化，并验证了两组在规模和构成上没有差异，包括任期、资历、编程语言和业务单元的分布。我们还确认，在实验开始之前，实验期间测量的任何变量在对照组和实验组之间都不存在差异。实验期间的注释发布频率与预期相符（第 4.1 节）。
我们没有在以下任何指标中检测到具有统计显著性的变化：代码评审的总时长、开发者实际花在代码评审上的时间、作者与评审者之间往返回应注释的轮数。然而，我们确实检测到编码速度略有提升。我们推测，向文档进行上下文切换的减少带来了这一积极效果。我们把更深入的调查留给未来工作。基于这些结果，我们得出结论：不存在负面影响，并于 2023 年 10 月将 AutoCommenter 部署给了所有开发者。

<!-- page 7 -->
AI-Assisted Assessment of Coding Practices in Modern Code Review
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil
Figure 5: Cumulative distribution of comments per URL for
the automated comments generated by AutoCommenter in
production and human comments in the training data.
5
评估
基于自 2023 年 3 月以来收集的有用率和用户反馈，我们得出结论：开发者总体上对 AutoCommenter 生成的注释感到满意。我们通过分析用户反馈，持续改进我们的数据集准备、阈值、URL 抑制和摘要生成，以确保 AutoCommenter 为开发者工作流带来高度的积极影响。
除了开发者满意度之外，在对 Google 全体开发者进行了数月的广泛发布之后，我们还评估了 AutoCommenter 表现的另外三个方面：
(1) 注释解决（Comment resolution）：开发者多久会修改他们的代码来解决 AutoCommenter 发布的注释？
(2) AutoCommenter 与人工注释：AutoCommenter 的注释在多大程度上覆盖了人类评审者在注释中引用的最佳实践文档？
(3) AutoCommenter 与 Linter：AutoCommenter 的输出在多大程度上超越了传统静态分析工具的能力？
5.1
注释解决
开发者很少通过点击代码评审系统和 IDE 中的“点赞/点踩”按钮，以及代码评审系统中的“请修复”（Please fix）按钮，来对 AutoCommenter 的注释给出明确反馈（图 3）：代码评审系统中约 10% 的自动化注释、以及 IDE 中 2% 的诊断信息收到了明确反馈，这与 Google 中其他自动化分析的情况相当。与此同时，开发者会悬停查看大约 50% 的 AutoCommenter IDE 诊断信息，而且此前的研究表明，开发者经常在没有明确反馈的情况下解决自动化注释 [18]。为了评估开发者解决 AutoCommenter 注释的频率，我们进行了一项离线分析，估计由后续代码变更所解决的注释的比例。
为了分析注释解决情况，我们提取了针对带有 AutoCommenter 自动化注释的文件的历史变更。对于每一处变更，我们提取了注释发布时的初始快照，以及开发者最终合并进代码库的快照。每条注释都跨越一段特定的行范围。我们使用一种基于 AST 的自动化行映射方法 [18] 来对齐这些快照，以识别模型在第一个快照上做出过预测、但在合并后的快照上不再做出预测的注释。
Code idioms
Documentation
Formatting
Language
Naming
0
5
10
Number of distinct URLs
Linter
Yes
No/Partially
Figure 6: The top-50 most frequently predicted URLs catego-
rized into types. Linter indicates whether a linter that detects
a violation exists or can easily be built.
此类快照对表明某条注释可能已经被解决，但也有可能是无关的代码变更导致某条特定注释不再被预测出来。
对 6000 个快照对进行的自动化分析显示，在 50% 的情况下，注释在其最初发布的那些行上不再出现于提交的快照中。我们人工抽查了其中 40 个随机样本对。我们发现，在 80% 的情况下，作者所做的某处变更直接解决了已发布注释所描述的问题。因此，我们估计注释解决率约为 40%，这显著高于获得明确正面反馈的注释占全部注释的比例。
5.2
AutoCommenter 与人工注释
图 5 比较了 AutoCommenter 在生产环境中生成的自动化注释与训练数据中人工注释的（每个指向最佳实践文档的唯一 URL 的）注释累积分布。x 轴是当所有曾在自动化注释中使用过的 URL 按频率排序时，该 URL 的排名。例如，最常用的 URL 排名为 1，它占全部自动化注释的 9.9%。这同一个 URL 出现在训练数据中人工创建注释的 4.3% 里。总体而言，AutoCommenter 已为 330 个不同的 URL 创建过注释。AutoCommenter 使用的 URL 集合覆盖了历史上带有最佳实践 URL 的人工注释的 68%。这是一个不错的结果：它表明 AutoCommenter 并没有聚焦于那些评审者很少引用的冷门最佳实践。
另一方面，尽管使用了束搜索（beam search），URL 的多样性仍然相对较低。排名前 85 的 URL 占 AutoCommenter 所创建注释的 90%。这同一组 URL 覆盖了带有最佳实践 URL 的人工注释的 35%。在保持准确性和低延迟的同时，提升自动化注释中 URL 的多样性和最佳实践的覆盖率，是我们的首要任务之一。
5.3
AutoCommenter 与 Linter
为了理解 AutoCommenter 在多大程度上提供了超越 Linter 的价值——Linter 能够高效且精确地检查某些最佳实践——我们抽取了预测频率最高的前 50 种违规，也就是图 5 中的前 50 个 URL。对于每个被抽取的

<!-- page 8 -->
AIware '24, July 15–16, 2024, Porto de Galinhas, Brazil
Manushree Vijayvergiya et al.
URL，我们检查了其最佳实践文档，并判定（1）最佳实践的类型（第 1 节），以及（2）是否存在能够检测相应违规的 Linter，或是否可以轻松构建一个。具体而言，三位作者——每人都有超过 10 年构建静态分析工具的经验——阅读了文档，并独立地对这些 URL 进行分类。在最佳实践类型上没有分歧，但在约 15% 的 URL 上，对于能否轻松构建一个 Linter 存在分歧。三位作者通过多数表决和讨论解决了这些分歧。分歧源于模糊的最佳实践，以及那些包含多条准则的实践。例如，检查是否存在代码文档相对直接，而就合理的例外情况和内容的清晰程度进行推理则不然。
图 6 展示了 50 个抽样 URL 的分布，按类型以及违规能否被 Linter 检测到进行拆分。在这些最佳实践中，有 33/50（66%）的违规检测超出了传统静态分析的范畴。
6
经验教训
基于我们在开发与部署 AutoCommenter 过程中积累的经验，我们总结了若干关键的经验教训：
• 补充传统分析：AutoCommenter 基于 LLM 的方法能够为人类评审者频繁引用的 68% 的最佳实践生成评论。其中许多都超出了传统静态分析的范畴。
• 内在评估与真实世界表现：内在评估和真实世界表现可能存在显著差异：我们的内在评估——使用真实世界人类评论的数据集，加上最先进的模型架构和训练流程——表明该模型很有前景，但我们的外在评估和系统改进对于成功部署至关重要。
• 监控用户接受度至关重要：即便是少数负面的用户体验，也可能侵蚀对自动化系统的信任。持续监控和分析真实世界的反馈，对于发现此类情况并确定补救措施至关重要。就 AutoCommenter 而言，一个简单的抑制机制就足以将用户接受度大幅提升至 80% 以上，而不会在有效性上造成重大损失。
7
相关工作
Johnson [15] 在近 50 年前的 1977 年引入了 C Linter。在这 50 年间，产生了大量关于自动化静态分析的研究：Heckman 和 Williams [10] 最近的一项文献综述识别出 17,571 篇论文。许多研究探讨了开发者如何与静态分析交互。Johnson 等人 [14] 探讨了开发者在使用静态分析时所面临的挑战。他们研究的结果凸显了将工具良好地集成到现有开发者工作流中的重要性，以及在工具中建立并维持信任的重要性。Vassallo 等人 [27] 探讨了开发者如何在不同情境下（包括编码和代码评审）与静态分析交互。他们也发现，集成到现有工作流中对开发者使用这些工具的意愿起着重要作用，而且结果的高质量极其重要。Beller 等人 [6] 研究了大量开源项目中静态代码分析的使用情况。在其他发现之外，他们强调自动化分析如何被使用以及应当如何使用，会因编程语言的不同而有所差异。
相比之下，使用机器学习进行代码分析是一个相对较新且了解较少的领域。许多近期发表的文章（例如 Hong 等人 [11]、Li 等人 [16]、Li 等人 [17]、Thongtanunam 等人 [24]、Tufano 等人 [25] 和 Tufano 等人 [26]）报告了模型评估，并提出了用于自动化代码评审的工具。虽然这些模型以及评审评论生成任务与本文所介绍的模型非常相似，但评估主要集中在历史数据集上。正如第 3.3.1 节所讨论的，仅基于历史评论进行的内在评估在某种程度上是有局限的，有时无法预测真实世界的表现。Frömmgen 等人 [9] 的另一篇近期文章展示了对一个在线系统的评估，但针对的是相反的任务：从评论生成代码，而非从代码生成评论。
8
结论
验证代码是否遵循最佳实践，是现代代码评审流程中的一项常见任务。虽然某些最佳实践可以通过 Linter 等传统工具自动验证，但许多最佳实践需要经验丰富的开发者的知识和判断力，而这需要时间和精力。
本文报告了我们在开发、部署和评估 AutoCommenter——一个基于 LLM 的代码评审辅助系统——方面的经验。具体而言，本文阐述了从任务和模型设计，经过内在评估和系统校准，到分阶段推出和最终用户评估的完整过程。
评估结果表明，开发一个端到端系统是可行的，该系统具备远超传统工具的能力，同时还能实现高度的最终用户接受度。这些结果是朝着部署复杂代码评审辅助工具和自动化代码评审迈出的、充满希望的第一步。
我们的首要任务是确保积极的开发者体验，为此将 AutoCommenter 设计为具有非常高的精确率（precision）。虽然召回率（recall）不是主要关注点，但我们认识到其重要性，并计划探索模型和系统架构中的哪些变化能够提升召回率。例如，我们在 2022 年使用的模型在当时是最先进的。然而，它的上下文窗口仅为 2048 个 Token，仅能容纳约 200 行代码。当前最先进的模型在训练时拥有数万个 Token 的上下文窗口，在推理时拥有超过一百万个 Token 的上下文窗口。这一飞跃为新增功能以及现有功能的显著改进打开了机遇。
9
致谢
这项工作是 Google Core Systems 与 Google DeepMind 团队多年合作的成果。我们感谢所有团队成员和领导层的支持与建议，包括 Alberto Elizondo、Alexander Frömmgen、Ballie Sandhu、Chandu Thekkath、Chris Gorgolewski、David Tattersall、Ilya Cherny、Jacob Austin、Katja Grünwedel、Kristóf Molnár、Lera Kharatyan、Luka Rimanić、Madhura Dudhgaonkar、Marc Brockschmidt、Marcus Revaj、Maxim Tabachnyk、Nina Chen、Niranjan Tulpule、Nitya Ramani、Paige Bailey、Pavel Sychev、Pierre-Antoine Manzagol、Quinn Madison、Roger Fleig、Satish Chandra、Savinee Dancs、Stoyan Nikolov、Subhodeep Moitra 和 Vaibhav Tulsyan。

<!-- page 9 -->
AI-Assisted Assessment of Coding Practices in Modern Code Review
AIware '24, July 15–16, 2024, Porto de Galinhas, Brazil
参考文献
[1] 2024. Google Style Guides. https://google.github.io/styleguide/.
Accessed:
2024-03-15.
[2] 2024. Linux kernel coding style. https://www.kernel.org/doc/html/v4.10/process/
coding-style.html. Accessed: 2024-03-15.
[3] 2024. PEP 8 – Style Guide for Python Code. https://peps.python.org/pep-0008/.
Accessed: 2024-03-15.
[4] 2024. Rust Style Guide. https://doc.rust-lang.org/nightly/style-guide/. Accessed:
2024-03-15.
[5] Alberto Bacchelli and Christian Bird. 2013. Expectations, outcomes, and chal-
lenges of modern code review. In 2013 35th International Conference on Software
Engineering (ICSE). 712–721. https://doi.org/10.1109/ICSE.2013.6606617
[6] Moritz Beller, Radjino Bholanath, Shane McIntosh, and Andy Zaidman. 2016.
Analyzing the state of static analysis: A large-scale evaluation in open source soft-
ware. In 2016 IEEE 23rd International Conference on Software Analysis, Evolution,
and Reengineering (SANER), Vol. 1. IEEE, 470–481.
[7] Zimin Chen, Małgorzata Salawa, Manushree Vijayvergiya, Goran Petrović, Marko
Ivanković, and René Just. 2023. MuRS: Mutant Ranking and Suppression using
Identifier Templates. In Proceedings of the Symposium on the Foundations of
Software Engineering (FSE). 1798–1808.
[8] M. E. Fagan. 1976. Design and code inspections to reduce errors in program
development. IBM Systems Journal 15, 3 (1976), 182–211. https://doi.org/10.1147/
sj.153.0182
[9] Alexander Frömmgen, Jacob Austin, Peter Choy, Nimesh Ghelani, Lera Kharatyan,
Gabriela Surita, Elena Khrapko, Pascal Lamblin, Pierre-Antoine Manzagol, Marcus
Revaj, Maxim Tabachnyk, Daniel Tarlow, Kevin Villela, Daniel Zheng, Satish
Chandra, and Petros Maniatis. 2024. Resolving Code Review Comments with
Machine Learning. In International Conference on Software Engineering: Software
Engineering in Practice (ICSE-SEIP).
[10] Sarah Heckman and Laurie Williams. 2011. A systematic literature review of
actionable alert identification techniques for automated static code analysis.
Information and Software Technology 53, 4 (2011), 363–387. https://doi.org/10.
1016/j.infsof.2010.12.007 Special section: Software Engineering track of the 24th
Annual Symposium on Applied Computing.
[11] Yang Hong, Chakkrit Tantithamthavorn, Patanamon Thongtanunam, and Aldeida
Aleti. 2022. Commentfinder: a simpler, faster, more accurate code review com-
ments recommendation. In Proceedings of the Joint Meeting of the European Soft-
ware Engineering Conference and the Symposium on the Foundations of Software
Engineering (ESEC/FSE). 507–519.
[12] Marko Ivanković, Goran Petrović, René Just, and Gordon Fraser. 2019. Code
Coverage at Google. In Proceedings of the Joint Meeting of the European Soft-
ware Engineering Conference and the Symposium on the Foundations of Software
Engineering (ESEC/FSE). 955–963.
[13] Marko Ivanković, Goran Petrović, Yana Kulizhskaya, Mateusz Lewko, Luka Kali-
novčić, René Just, and Gordon Fraser. 2024. Productive Coverage: Improving
the Actionability of Code Coverage. In International Conference on Software
Engineering: Software Engineering in Practice (ICSE-SEIP).
[14] Brittany Johnson, Yoonki Song, Emerson Murphy-Hill, and Robert Bowdidge.
2013. Why don't software developers use static analysis tools to find bugs?. In
2013 35th International Conference on Software Engineering (ICSE). IEEE, 672–681.
[15] Stephen C Johnson. 1977. Lint, a C program checker. Bell Telephone Laboratories
Murray Hill.
[16] Lingwei Li, Li Yang, Huaxi Jiang, Jun Yan, Tiejian Luo, Zihan Hua, Geng Liang,
and Chun Zuo. 2022. Auger: Automatically generating review comments with
pre-training models. In Proceedings of the Joint Meeting of the European Soft-
ware Engineering Conference and the Symposium on the Foundations of Software
Engineering (ESEC/FSE). 1009–1021.
[17] Zhiyu Li, Shuai Lu, Daya Guo, Nan Duan, Shailesh Jannu, Grant Jenks, Deep
Majumder, Jared Green, Alexey Svyatkovskiy, Shengyu Fu, and Neel Sundaresan.
2022. Automating code review activities by large-scale pre-training. In Proceedings
of the 30th ACM Joint European Software Engineering Conference and Symposium
on the Foundations of Software Engineering (<conf-loc>, <city>Singapore</city>,
<country>Singapore</country>, </conf-loc>) (ESEC/FSE 2022). Association for
Computing Machinery, New York, NY, USA, 1035–1047. https://doi.org/10.1145/
3540250.3549081
[18] Goran Petrović, Marko Ivanković, Gordon Fraser, and René Just. 2023. Please fix
this mutant: How do developers resolve mutants surfaced during code review?. In
International Conference on Software Engineering: Software Engineering in Practice
(ICSE-SEIP). 150–161.
[19] Rachel Potvin and Josh Levenberg. 2016. Why Google Stores Billions of Lines
of Code in a Single Repository. Communications of the ACM (CACM) 59 (2016),
78–87. http://dl.acm.org/citation.cfm?id=2854146
[20] Peter Rigby, Brendan Cleary, Frederic Painchaud, Margaret-Anne Storey, and
Daniel German. 2012. Contemporary Peer Review in Action: Lessons from Open
Source Development. IEEE Software 29, 6 (2012), 56–61. https://doi.org/10.1109/
MS.2012.24
[21] Peter C. Rigby and Christian Bird. 2013. Convergent contemporary software peer
review practices. In Proceedings of the 2013 9th Joint Meeting on Foundations of
Software Engineering (Saint Petersburg, Russia) (ESEC/FSE 2013). Association for
Computing Machinery, New York, NY, USA, 202–212. https://doi.org/10.1145/
2491411.2491444
[22] Adam Roberts, Hyung Won Chung, Gaurav Mishra, Anselm Levskaya, James
Bradbury, Daniel Andor, Sharan Narang, Brian Lester, Colin Gaffney, Afroz
Mohiuddin, et al. 2023. Scaling up models and data with t5x and seqio. Journal
of Machine Learning Research 24, 377 (2023), 1–8.
[23] Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko, and Alberto
Bacchelli. 2018. Modern Code Review: A Case Study at Google. In International
Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP).
181–190.
[24] Patanamon Thongtanunam, Chanathip Pornprasit, and Chakkrit Tantithamtha-
vorn. 2022. Autotransform: Automated code transformation to support modern
code review process. In Proceedings of the International Conference on Software
Engineering (ICSE). 237–248.
[25] Rosalia Tufano, Ozren Dabić, Antonio Mastropaolo, Matteo Ciniselli, and Gabriele
Bavota. 2024. Code Review Automation: Strengths and Weaknesses of the State
of the Art. IEEE Transactions on Software Engineering (TSE) (2024).
[26] Rosalia Tufano, Simone Masiero, Antonio Mastropaolo, Luca Pascarella, Denys
Poshyvanyk, and Gabriele Bavota. 2022. Using pre-trained models to boost code
review automation. In Proceedings of the International Conference on Software
Engineering (ICSE). 2291–2302.
[27] Carmine Vassallo, Sebastiano Panichella, Fabio Palomba, Sebastian Proksch, Har-
ald C Gall, and Andy Zaidman. 2020. How developers engage with static analysis
tools in different contexts. Empirical Software Engineering 25 (2020), 1419–1457.
[28] T. Winters, T. Manshreck, and H. Wright. 2020. Software Engineering at Google:
Lessons Learned from Programming Over Time. O'Reilly Media. https://books.
google.ch/books?id=TyIrywEACAAJ
Received 2024-04-05; accepted 2024-05-04