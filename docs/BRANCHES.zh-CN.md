# 分支

这是 macOS 维护方 fork 与上游仓库的分支地图。英文版是 [BRANCHES.md](BRANCHES.md)。两份文件记录同一组事实。

`AGENTS.md`、`CONTRIBUTING.md` 和 `.github/copilot-instructions.md` 要求：只要共享分支发生变动，就在同一项改动里更新这两份文件，然后再结束工作。共享分支指出现在 `origin` 或 `upstream` 上的分支，包括短命的代理分支。只存在于某台机器、从未推送的分支不写入这张地图。

下面的 SHA 在 2026-11-03 执行 `git fetch origin` 和 `git fetch upstream` 之后读取。它们是工作顶端。主题以 `docs: map the fork` 或 `docs: keep the branch map` 开头的提交叠在这些工作顶端之上，就是这张地图，不替换工作顶端。把其他 SHA 当作当前顶端之前，先运行：

```sh
git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short) %(objectname:short) %(subject)' refs/heads refs/remotes
```

写下这张地图时，本工作区在 `macos-necko-adapter`。

这张地图放在 `origin` 的每一条分支上。它改动之后，这些文档提交要应用到每一条 `origin` 分支并推送。能快进的分支用快进。已经分叉的分支用 cherry-pick，并保留该分支上的其他改动。本工作区不推送 `upstream`。

## 远程

| 远程 | 仓库 | 用途 |
| --- | --- | --- |
| `origin` | https://github.com/Facetomyself/ff-ruyijs | 本 fork。推送到这里。 |
| `upstream` | https://github.com/cutetailbud/ff-ruyijs | 规范仓库。本工作区把它的 push URL 设为 `DISABLED`。只拉取；要改上游时，从 fork 分支向上游开 pull request。 |

有的克隆里还留着 `refs/remotes/upstream-check/main`，指向 `fd094ed`。没有配置名为 `upstream-check` 的远程。不要使用这根 ref。

## 改动怎么走

上游 `main` 是 cutetailbud/ff-ruyijs 的发布线。本 fork 的 macOS 维护线是 `release/macos`。修正先合进 `release/macos`，fork 的 `main` 再快进到同一提交。

接上游更新时，从 `release/macos` 拉出分支，在那条分支上合并上游、审查，再合回 `release/macos`，然后把 fork 的 `main` 快进过去。fork 的 `main` 通过这次快进接到结果。

`main`、`release/macos` 和 `tls/necko-core-arm64` 目前同在 `2e11166`（「Record 0.3.0 as the macOS maintenance baseline.」，2026-11-01）。上游 `main` 是 `d41f247`（「release: pin the 0.3.3 runtime」，2026-11-02）。标签 `v0.3.1`、`v0.3.2`、`v0.3.3` 在这段上游历史上。fork 的 `main` 比上游 `main` 超前 9 个提交（fork 自己的维护记录），落后 53 个提交。已经同时包含两边顶端的分支是 `cursor/sync-upstream-0.3.3-711e`。

## 该检出哪条分支

| 要做的事 | 分支 |
| --- | --- |
| 修改已发布的 0.3.3 树 | `upstream/main` |
| 让 macOS 维护成为 fork 的默认线 | 先合入 `release/macos`，再快进 `main` |
| 审查把 0.3.3 同步到 fork 基线的结果 | `cursor/sync-upstream-0.3.3-711e` |
| 阅读 Darwin Necko 适配器试验 | `macos-necko-adapter` |
| 阅读那两个 HTTP 代理提交 | `macos-core-proxy` |
| 改项目网站 | `upstream/gh-pages` |

## Fork 上的分支

`origin` 是 https://github.com/Facetomyself/ff-ruyijs。

### `main`

fork 的默认分支。`origin/main` 为 `2e11166`（2026-11-01），与 `release/macos`、`tls/necko-core-arm64` 相同。

上游 `main` 里没有的那 9 个提交是维护记录：基线说明、缺口说明，以及把上游 0.3.0 / Firefox 159 wheel 底线合进 fork 的合并。`release/macos` 前进之后，把 `main` 快进到同一提交。新的产品工作从 `release/macos` 拉分支；改动要进已发布项目时，从 `upstream/main` 拉分支。

### `release/macos`

与 fork 的 `main` 同顶端（`2e11166`）。macOS 修正合到这里。更早的发布工作（Firefox donor 外壳、适配器、helper、以及 0.2.1 的上游合并）先落在这里，`main` 再快进。下一次维护从这根顶端拉分支。

### `tls/necko-core-arm64`

与 fork 的 `main` 同顶端（`2e11166`）。这条分支从 `d170a06` 拉出，用来做经 arm64 `libnecko_core` 的 macOS 直连 HTTPS，以及 Firefox 100–159 的 TLS 配置。测量记录在 [tls-profile.md](tls-profile.md) 和 [tls-profile.zh-CN.md](tls-profile.zh-CN.md)。那两份记录仍描述指针并入 0.3.0 基线之前、在这条分支上做的 HTTP/2 和页面测量。现在没有单独的 TLS 顶端可检出。新的 TLS 改动从 `release/macos` 或 `upstream/main` 开始，看它应该落在哪一条线上。

### `macos-necko-adapter`

Darwin Necko 适配器。本地 `macos-necko-adapter` 与 `origin/macos-necko-adapter` 都是 `00b31c5`（「Merge upstream main into the Darwin Necko adapter.」，2026-11-01）。

它包含 `macos-core-proxy`。在那之上，它在 macOS 上运行 Windows 的 `necko` / `ruyijs_necko` 包，记录恢复出的 ClientHello，加入 HTTP/3 桥，把适配器暂存为运行时，在 CI 里用 CONNECT 代理加载页面，在 TLS 对端省略 ALPN 时回退到 HTTP/1.1，并在关闭 WebTransport 会话前快照其状态。试验记录是 [macos-necko-adapter-spike.md](macos-necko-adapter-spike.md)。

上游 `main` 已包含这根顶端（pull request #9）。`cursor/sync-upstream-0.3.3-711e` 也包含它。fork 的 `main` 仍停在 0.3.0 基线：本分支比 `origin/main` 超前 14 个提交、落后 9 个。上游 `main` 又比这根顶端超前 39 个提交，一直到 0.3.3。要随已发布项目出货的适配器工作，从 `upstream/main` 继续；同步分支成为 fork 上待审查的线之后，从那条同步分支继续。这根顶端保留 fork 上当时提出的适配器记录。

### `macos-core-proxy`

`302565c`（「Say when a proxy stays on xpcshell and when it uses CONNECT.」，2026-11-01），`origin` 和本地都有。两个提交落在 `6d45317`（「release: pin the 0.3.0 runtime」）之上。它们让没有 xpcshell 的 macOS wheel 使用 HTTP 代理，并写明代理何时仍走 xpcshell、何时走 CONNECT。

pull request #7 合并了这条分支。`macos-necko-adapter` 和上游 `main` 都包含这根顶端。fork 的 `main` 仍是基线：本分支比 `origin/main` 超前 2 个提交、落后 9 个，比上游 `main` 落后 51 个。本地分支跟踪的是 `upstream/main`，因此 status 可能显示它落后于上游，而它自己的工作仍是那两个提交。把这条分支留作历史。之后的代理工作在适配器线和上游 `main` 上。

### `cursor/sync-upstream-0.3.3-711e`

只在 `origin`。顶端 `a11cfd4`（2026-11-03）把 `upstream/main`（`d41f247`，0.3.3）合并进 fork 基线（`2e11166`）。

它包含 fork 的 `main`（超前 54，落后 0）和上游 `main`（超前 10，落后 0）。这 10 个提交是 fork 的 9 条维护记录加上这次合并。相对上游 `main` 的差异是 fork 的 macOS 维护文档：`docs/macos-baseline.md`、`docs/macos-gaps.md`、两份中文，以及对 `CHANGELOG.md`、`CONTRIBUTING.md`、`docs/macos.md`、`docs/macos.zh-CN.md` 的小改动。Darwin 适配器也在其中，因为上游 `main` 已经包含它。

这是把 0.3.3 接到 fork 上的审查分支。审查合回之后，它才成为 `release/macos`，fork 的 `main` 再快进。写下这张地图时检出的是 `macos-necko-adapter`，不是这条同步分支。

### `chore/mac-maint-bot-ci`

只在 `origin`。`0ca5f5d`（2026-10-31）是 `c69875b` 上的一个提交：Grok Bot 值班提示、Bugbot 规则，以及 Mac pull request 守卫（`.cursor/BUGBOT.md`、`.cursor/config/bugbot.yaml`、`.github/workflows/mac-pr.yml`、`ci/mac_pr_guard.py`、`docs/maintainers/grok-bot-duty.md`）。它比 `origin/main` 超前 1 个提交、落后 16 个，尚未合并。这是维护自动化，不是产品线。新的产品改动从 `release/macos` 或 `upstream/main` 开始。要继续这套自动化，从这条分支接着做，再经 `release/macos` 合入。

### `cursor/cloud-agent-wine-e182`

只在 `origin`。`8ef9157`（2026-10-30）是一个文档提交。它说明 Cloud Agent 在 Wine 下运行 ruyijs，因为宿主 Python 无法导入 Windows 引擎，并修改了 `AGENTS.md`。它比 `origin/main` 超前 1 个提交、落后 48 个，尚未合并。这段 Wine 说明目前只在这条分支上。

## 上游分支

`upstream` 是 https://github.com/cutetailbud/ff-ruyijs。本工作区只拉取、不推送。

### `main`

`d41f247`（2026-11-02），标签 `v0.3.3`。这是规范线。过了 0.3.0 的钉住点之后，它包含 Darwin 适配器（pull request #9）、Core Text 与 DOMException 移植（pull request #8，合并提交 `163621e`，来自 `isesword/upstream-mac`）、ClientHello 修正（pull request #10），以及 0.3.1–0.3.3：同一进程里的多个 `Engine` 会话、从字节码启动的 Necko helper，以及样式变化后只重算触及范围的几何。发布的 wheel 和版本标签来自这条分支。fork 仍把它称为 Windows 发布线，因为 fork 上的 macOS 维护先落在 `release/macos`。

### `ci/macos`

`ed189ef`（2026-11-01）。macOS arm64 源码构建与 wheel 的 CI。它多次合并 `ci/source-build`。其中 16 个提交不在上游 `main` 里。后来 `main` 上的 wheel CI 走了自己的路径。读这条分支是为了看那次 CI 试验。产品构建用 `main`。

### `ci/source-build`

`89e260b`（2026-11-01）。共用的 CI 修正：去掉浏览器构建步骤里的 CR，解析各种目标文件列表，按链接顺序构建库，并解析 `build.py` 的路径。其中 9 个提交不在上游 `main` 里。`ci/macos` 包含这根顶端。

### `gh-pages`

`4394b97`（2026-10-30）。GitHub Pages 站点：`llms.txt`、`robots.txt`、站点地图，以及赞助方和品牌更新。这是站点分支，与引擎树分开。

### `review/pr8`

`48f20d2`（2026-11-01），「Merge pull request #8 (review build)」。Core Text 塑形移植、DOMException 表面、`matchMedia`，以及可配置 NSS 目录来链接 `libnecko_core` 的审查快照。这根 ref 不是上游 `main` 的祖先（上游 `main` 有 22 个提交不在这根 ref 里，两边历史也不相同）。已经落地的移植是 pull request #8，合并提交 `163621e`，上游 `main` 包含它，并处在通往 `v0.3.3` 的历史上。这项移植的新工作从上游 `main` 开始。

## 更新这张地图

发生下列任一情况时，在同一次改动中同时更新本文件和 [BRANCHES.md](BRANCHES.md)：

- 在 `origin` 或 `upstream` 上创建、重命名、删除或推送了分支。
- 共享分支移到新的顶端，或 pull request 合并了它。
- 分支的职责变了：修正落在哪里，或者新人应该检出哪一条。
- 这里的 SHA、日期，或「包含 / 被包含」与 `git` 不一致。

写下远程、顶端 SHA、说明、日期、这条分支做什么，以及这项工作现在在哪条分支上。网络可用时先运行 `git fetch origin` 和 `git fetch upstream`。没有拉取时，写明快照来自本地 ref，并写上日期。超前和落后的个数属于快照，用 `git rev-list --count` 重算，不要抄旧数字。

英文版和中文版列出相同的分支、顶端和职责。只改其中一份，这项更新就还没完成。每一条 `origin` 分支都包含这次改动并已推送之前，这项更新也还没完成。
