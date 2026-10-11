代码评审：放手去做吧

[图: Coding Horror]

- Archive

- Discourse

- Stack

- RGMII

- Reading

- About

- Shop

# 代码评审：放手去做吧

[图: Jeff Atwood]

#### Jeff Atwood

21 Jan 2006
— 2 min read
— Comments

在《人性化的同行评审》（Humanizing Peer Reviews）中，Karl Wiegers 以一个强有力的论断开篇：

> 同行评审（peer review）——一种由软件交付物作者以外的人员对其进行检查、以发现缺陷和改进机会的活动——是可用的最强大的软件质量工具之一。同行评审的方法包括审查（inspection）、走查（walkthrough）、同行桌面检查（peer desk check）以及其他类似活动。在亲身体验了同行评审将近十五年的种种好处之后，我绝不会加入一个不做同行评审的团队。

在 Vertigo 参与了一段时间的代码评审之后，我深信，**同行代码评审是你能够用来改进自己代码的最重要的一件事。** 如果你现在还没有和另一位开发者一起做代码评审，那么你正在遗漏自己代码中大量的 bug，也在白白错失一些关键的职业成长机会。就我而言，我的代码在与另一位开发者一起过一遍之前，都不算完成。

不过别只听我的一面之词。McConnell 在《代码大全》（Code Complete）中为代码评审的有效性提供了大量证据：

> 

……仅靠软件测试，其有效性是有限的——单元测试的平均缺陷发现率只有 25%，功能测试为 35%，集成测试为 45%。相比之下，设计评审与代码审查的平均有效性分别为 55% 和 60%。有关评审结果的案例研究令人印象深刻：

- 在一家软件维护组织中，在引入代码评审之前，单行维护变更中有 55% 存在错误。引入评审之后，只有 2% 的变更存在错误。当把所有变更都纳入考量时，引入评审后，95% 的变更一次即正确；而引入评审之前，一次即正确的不到 20%。

- 在由同一批人开发的 11 个程序中，前 5 个是在没有评审的情况下开发的，其余 6 个则是在有评审的情况下开发的。所有这些程序发布到生产环境之后，前 5 个程序平均每 100 行代码有 4.5 个错误，而经过审查的 6 个程序平均每 100 行代码仅有 0.82 个错误。评审将错误减少了 80% 以上。

- Aetna 保险公司通过使用审查，发现了一个程序中 82% 的错误，并得以将其开发资源削减了 20%。

- IBM 的 50 万行 Orbit 项目采用了 11 个层级的审查。该项目提前交付，且出现的错误仅为通常预期水平的约 1%。

- 一项针对 AT&T 某组织（超过 200 人）的研究报告显示，在引入评审之后，其生产率提高了 14%，缺陷减少了 90%。

- 喷气推进实验室（Jet Propulsion Laboratories）估计，通过在早期阶段发现并修复缺陷，每次审查可节省约 25,000 美元。

代码评审唯一的障碍，就是找到一位你尊重的开发者来做这件事，并腾出时间来完成评审。一旦开始，我想你很快就会意识到，你在代码评审上花费的每一分钟，都会获得十倍的回报。

如果你的组织刚开始接触代码评审，我强烈推荐 Karl 的书《软件中的同行评审：实用指南》（Peer Reviews in Software: A Practical Guide）。Karl 在其网站上提供的示例章节也是极佳的入门读物。

software development
code reviews
peer reviews
code quality
professional development

[图: Jeff Atwood]

#### Written by Jeff Atwood

Indoor enthusiast. Co-founder of Stack Overflow, Discourse, and RGMII. Disclaimer: I have no idea what I'm talking about. Let's be kind to each other. Find me https://infosec.exchange/@codinghorror

✉️ Subscribe

⏲️ Busy signing you up.

❗ Something's gone wrong. Please try again.

✅ Success! Check your inbox (and your spam folder, just in case).

← Previous Post

## 3D positional audio and HRTFs

Next Post →

## ... and a Pony!

## Related posts

[图: Civilized Discourse Construction Kit]

### 

Civilized Discourse Construction Kit

Occasionally, startups will ask me for advice. That's a shame, because I am a terrible person to ask for advice. The conversation usually goes something like this:

We'd love to get your expert advice on our thing.

I probably don't use your thing. Even if I tried

By Jeff Atwood
·
05 Feb 2013

Comments

[图: How to Stop Sucking and Be Awesome Instead]

### 

How to Stop Sucking and Be Awesome Instead

I've been fortunate to have some measure of success in my life, primarily through this very blog over the last eight years, and in creating Stack Overflow and Stack Exchange over the last four years. With the birth of our twin girls, I've had a few months to

By Jeff Atwood
·
31 May 2012

Comments

[图: Books: Bits vs. Atoms]

### 

Books: Bits vs. Atoms

I adore words, but let's face it: books suck.

More specifically, so many beautiful ideas have been helplessly trapped in physical made-of-atoms books for the last few centuries. How do books suck? Let me count the ways:

* They are heavy.
* They take up too much space.
* They have to

By Jeff Atwood
·
10 Apr 2012

Comments

[图: The Vast and Endless Sea]

### 

The Vast and Endless Sea

After we created Stack Overflow, some people were convinced we had built a marginally better mousetrap for asking and answering questions. The inevitable speculation began: can we use your engine to build a Q&A site about {topic}? Our answer was Stack Exchange. Pay us $129 a month (and

By Jeff Atwood
·
31 May 2010

Comments

## Recent Posts

[图: map of the United States via rgmii.org showing all 3,143 counties by rural (gold) / metro (grey) and population]

### 

Launching The Rural Guaranteed Minimum Income Initiative

It's been a year since I invited Americans to join us in a pledge to Share the American Dream:

1. Support organizations you feel are effectively helping those most in need across America right now.

2. Within the next five years, also contribute public dedications of time or

By Jeff Atwood
·
03 Feb 2026

Comments

[图: The Road Not Taken is Guaranteed Minimum Income]

### 

The Road Not Taken is Guaranteed Minimum Income

The dream is incomplete until we share it with our fellow Americans.

By Jeff Atwood
·
20 Mar 2025

Comments

[图: Let's Talk About The American Dream]

### 

Let's Talk About The American Dream

A few months ago I wrote about what it means to stay gold — to hold on to the best parts of ourselves, our communities, and the American Dream itself. But staying gold isn't passive. It takes work. It takes action. It takes hard conversations that ask us to confront

By Jeff Atwood
·
05 Mar 2025

Comments

[图: Stay Gold, America]

### 

Stay Gold, America

We are at an unprecedented point in American history, and I'm concerned we may lose sight of the American Dream.

By Jeff Atwood
·
06 Jan 2025

Comments

I'm feeling unlucky... 🎲

See All Posts

[图: Coding Horror]

- Archive

- Reading

- About

- Shop

Powered by Ghost · Themed by Obox