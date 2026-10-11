GitHub Copilot: Remote Code Execution via Prompt Injection (CVE-2025-53773) · Embrace The Red

# Embrace The Red

wunderwuzzi's blog

learn the hacks, stop the attacks.

 Home

 RSS

 Subscribe

# GitHub Copilot: Remote Code Execution via Prompt Injection (CVE-2025-53773)

Posted on

Aug 12, 2025

#llm

#agents

#month of ai bugs

本文介绍的是一个重要但同时令人心惊的提示注入（Prompt Injection）发现，它可导致 GitHub Copilot 和 VS Code 中开发者机器遭到完全的系统入侵（system compromise）。

其实现方式是通过修改项目的 `settings.json` 文件，将 Copilot 置于 YOLO 模式（YOLO mode）。

[图: vscode episode 18]

正如几天前用 Amp 所描述的那样，智能体（Agent）中一种可能被忽视的漏洞模式是：如果某个智能体能够写入文件并修改其自身的配置，或更新与安全相关的设置，那么就可能引发远程代码执行（Remote Code Execution，RCE）。这种情况并不罕见，也是在进行安全评审（security review）时始终值得关注的一个方向。

## Background Research

在查看 VS Code 和 GitHub Copilot Agent Mode 时，我注意到了一个奇怪的行为……它可以在未经用户批准的情况下在工作区（workspace）中创建文件并写入文件。

这些编辑会立即持久化，而不是作为可审阅的差异（diff）暂存在内存中。修改会立刻写入磁盘。

[图: vscode agents that can modify their own settings]

作为一名红队（red teamer）成员，你凭直觉就知道这类事情大概不是什么好事……所以我一直在研究能否利用它来提升权限（escalate privileges）并执行代码。

### YOLO Mode

于是，接下来我研究了 VS Code 中那些依赖于项目/工作区文件夹内设置的特性，很快就发现了一个有趣的地方。

[图: vscode-exp-yolo-mode]

事实证明，在 `.vscode/settings.json` 文件中可以添加如下一行：

`"chat.tools.autoApprove": true`

这会让 GitHub Copilot 进入 YOLO 模式。

并且它会禁用所有用户确认，我们可以运行 shell 命令、浏览网页，还能做更多的事！

有意思的是，这是一个实验性特性，但它默认仍然存在。我并没有下载任何特殊版本，也没有把整个 VS Code 设为实验模式。

此外，它在 Windows、macOS 以及 Linux 上都有效。

## Exploit Chain Explained

劫持 Copilot 并提升权限的概念验证（proof-of-concept）漏洞利用（exploit）链如下：

- 攻击始于植入到源代码文件、网页、GitHub issue、工具调用响应或其他内容中的提示注入……载荷（payload）还可以使用不可见文本作为指令。

- 提示注入首先将 `"chat.tools.autoApprove": true` 这一行添加到 `~/.vscode/settings.json` 文件中。如果文件夹和文件尚不存在，则会创建它们。

- GitHub Copilot 立即进入 YOLO 模式！

- 攻击者运行一条终端（Terminal）命令。利用条件提示注入（conditional prompt injection），我们实际上可以根据操作系统来选择要运行的内容。

- 我们实现了由提示注入驱动的远程代码执行（Remote Code Execution）。

下面这张截图展示了带有提示注入的演示文件、开发者在右侧聊天框中与该文件的交互，以及弹出的计算器！

[图: vscode-e2e-calc]

当然，任何其他提示注入的投递手段，例如来自网页或从 MCP 服务器返回的数据，也都是一种攻击角度（attack angle）。我只是把它放在源代码文件里，因为这样最容易测试。

## Video Walkthrough

### Short Demos

这里是一段演示视频，展示了在 Windows 上的代码执行。

而这一段是在 macOS 上：

### Walkthrough

这里是一段更长的视频，详细解释了这一发现和漏洞利用：

AI 能够自行设置自己的权限和配置设置，这实在太疯狂了！

## Joining the Workstation to a Botnet - ZombAIs

当然，这意味着我们可以把开发者的机器加入僵尸网络（botnet），使其成为 ZombAI。

此外，为了好玩，我们还可以修改 `settings.json` 文件，把 VS Code 切换成 `Red` 配色方案之类的。

但这还没完！这也意味着我们可以构建一种真正的 AI 病毒（AI virus），它会附着在文件上，并在开发者下载并交互受感染文件时传播开来。

最后但同样重要的是，为了证明我们对开发者主机拥有完全控制，我们展示了 Copilot 可以被劫持去下载恶意软件（malware），并加入一个远程命令与控制（command and control）服务器。

[图: vscode-zombai-deployment]

这意味着恶意软件、勒索软件（ransomware）、信息窃取器（info stealer）等的大门已经敞开。

真是可怕。

## Building an AI Virus

看到这一点时，人们会意识到这基本上允许创建一种病毒。攻击者可以嵌入指令，一旦获得代码执行能力，额外的恶意软件就可以侵入其他 Git 项目（以及 RAG 来源），植入恶意指令，并提交这些更改，甚至将其强制推送（force push）到上游。

随着其他开发者在不知情的情况下传播受感染的代码，这可能导致进一步扩散。

最后，我们还需要谈谈不可见指令（invisible instructions）！

## Using Invisible Instructions

有人可能会说，如果指令是以注释的形式嵌入的，那很快就会被发现。所以为了让事情更有趣一点，我动手创建了一个不可见的载荷，它能够实现这条攻击链，但对用户不可见。这种方式不那么可靠，但仍然有效：

注意：尽管这里使用不可见指令的演示对我而言多次成功，但使用不可见指令往往会导致该漏洞利用非常不可靠，也常常会被模型拒绝，而且 VS Code 通常还会针对 Unicode 字符显示一个视觉提示。然而，攻击（以及模型）会随着时间不断改进。同样值得强调的是，并非所有模型都容易受到这类不可见提示注入攻击。

## Recommendations and Fix

实际上，除了我分享的 YOLO 模式示例之外，还有更多的攻击角度。当 Microsoft 问我是否还有其他信息时，我多看了看，注意到还有其他有问题的位置，例如 AI 可以写入的 `.vscode/tasks.json`，或者添加伪造的恶意 MCP 服务器等等，这些都可能引发代码执行。而且 AI 还可以重新配置项目的用户界面和配置设置。

最近我注意到开发者常常会同时使用多个智能体，因此还存在覆盖其他智能体配置文件（允许列表中的 bash 命令、添加 MCP 服务器……）的威胁，因为这些文件通常也位于项目文件夹中。

理想情况下，AI 在没有人类先行批准的情况下不应能够修改文件。许多其他编辑器确实会显示差异，然后由开发者批准。

## Responsible Disclosure

在 2025 年 6 月 29 日报告该漏洞后，Microsoft 确认了复现（repro）过程并问了几个后续问题。几周后，MSRC 指出这是他们已经在跟踪的问题，并将在 8 月前完成修补。随着 8 月的 Patch Tuesday 发布，该问题现已修复。

向 Persistent Security 的 Markus Vervier 致谢，他也发现并向 Microsoft 报告了这一漏洞。你可以在这里找到他们的报告。同时也要向 Ari Marzuk 致谢，他似乎也同时发现了这一问题。

感谢 MSRC 成员和产品团队在协助缓解该问题方面提供的帮助。

## Conclusion

这是又一个展示 AI 智能体可能不会安分守己的例子！通过修改自身环境，GitHub Copilot 可以提升权限并执行代码，从而入侵开发者的机器。正如我所发现的，这是智能体式系统（agentic systems）中一种并不罕见的设计缺陷。

请继续留意这类设计缺陷，它们在威胁建模（threat modeling）过程中应当很容易被捕捉到。

Cheers.

## References

- Month of AI Bugs 2025

- Amp Code: Arbitrary Command Execution via Prompt Injection Fixed

- Copilot Settings

- CVE-2025-53773: GitHub Copilot and Visual Studio Remote Code Execution Vulnerability

- Persistent Security Write-Up

- Persistent Security 

- Newer →

- 

 Contact me

- ← Older

(c) WUNDERWUZZI 2018-2026

Disclaimer: Penetration testing requires authorization from proper stakeholders. Information on this blog is provided for research and educational purposes to advance understanding of attacks and countermeasures to help secure the Internet. | Privacy