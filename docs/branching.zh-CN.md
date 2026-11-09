# 分支

本 fork（`Facetomyself/ff-ruyijs`）与上游（`cutetailbud/ff-ruyijs`）的关系。英文版是 [branching.md](branching.md)。两份说的是同一套规则。

`main` 是 Linux、macOS、Windows 三条平台共用的主干。改动先按下面的命令核过它会影响到的平台，再进入 `main`。平台分支不是第二条产品线。

旧的 SHA 台账是 [BRANCHES.md](BRANCHES.md)，现在改成指向这里。不要把顶端 SHA 抄进每一条分支。先 `git fetch origin` 和 `git fetch upstream`，再用 `git rev-parse origin/<分支>`。

## 长期分支

| 分支 | 角色 | 何时移动 |
| --- | --- | --- |
| `main` | fork 主干。三个平台。pull request 合到这里。 | 合并已审查的 PR。不用 force-push。 |
| `sync/<上游 SHA>` | 临时。从 `main` 拉出，再合并 `upstream/main`。不 rebase。 | 这次合并进入 `main` 之后删除。 |
| `release/macos` | 与 `main` 同一提交的指针，给还停在这个名字上的 Mac 检出用。不在上面写提交。 | `main` 前进之后快进。只用普通推送（`git push origin origin/main:refs/heads/release/macos`）。 |
| `tls/necko-core-arm64` | 同样的指针。TLS 工作已经在 `main` 上。没有单独的顶端。 | 与 `release/macos` 一起快进。 |

`upstream/main` 是规范项目。只拉取，不推送。要进已发布项目的改动放在 `upstream/<feature>`（见下），由人向上游 `main` 开 pull request。本 fork 不合并那些 pull request。

## 短分支的名字

除表中写明的以外，都从 `main` 拉出。

| 前缀 | 用途 |
| --- | --- |
| `sync/<上游 SHA>` | 把 `upstream/main` 合并进从 `main` 拉出的一条分支。 |
| `feat/<主题>` | 新行为。 |
| `fix/<主题>` | 缺陷修复。 |
| `perf/<主题>` | 速度或内存，附上前后数字。 |
| `docs/<主题>` | 只改文档。 |
| `chore/<主题>` | 维护工具、CI、提示词。 |
| `upstream/<feature>` | 从 **`upstream/main`** 拉出，不从本 fork 的 `main` 拉。只放适合进已发布项目的改动。不要带 fork 的 release URL、分支地图或维护机器人文件。只推到本 fork。上游 pull request 由人来开。 |

`cursor/<主题>` 是代理会话分支。对应 pull request 合并后即算过期。

## 接入上游

1. `git fetch upstream main`。
2. 从 `main` 建 `sync/<上游 SHA>`，合并 `upstream/main`。不 rebase，不 force-push。
3. 按下一节核过这次合并会影响到的每个平台。
4. 向 `main` 开 pull request。说明里写下冲突和解决办法。
5. 合并之后，若 `release/macos` 和 `tls/necko-core-arm64` 是 `main` 的祖先，就把它们快进到 `main`。推送被拒绝就停。不要 force。

同步还开着时做的功能，从那条同步分支拉出，pull request 指向同步分支，或等同步进 `main` 之后再指向 `main`。不要把提交写在 `release/macos` 上。

## 验收

pull request 里写明下面哪几项跑过，哪几项没跑。

**Linux。** 云代理，或任意一台 Ubuntu 24.04，检出里要有 `firefox/` 子模块。步骤和有些镜像还缺的包见 [linux.md](linux.md)。

```sh
ci/linux/build.sh deps
ci/linux/build.sh donor
ci/linux/build.sh shell
ci/linux/build.sh necko    # python3 需为 3.14，或 PYTHON=python3.14
ci/linux/build.sh wheel
ci/linux/build.sh test     # smoke、helper、layout、atob、network、proxy、ClientHello、engine
```

性能改动还要用 wheel 的解释器、在检出目录之外跑 `ci/linux_baseline.py --network`，并写下前后数字。见 [linux-baseline.md](linux-baseline.md)。

**macOS。** 维护者的 macos-maint Mac mini（arm64），不是 Linux 云代理。donor 构建见 [macos.md](macos.md)：

```sh
python3.12 -B tools/bootstrap_macos_helper.py
python3.12 -B tools/build.py --donor-obj ../firefox-159/obj-js-standalone
```

`MACOSX_DEPLOYMENT_TARGET=26.0`。donor 树放在仓库外面。写明实际跑了什么（导入、`dist/js` 求值、一次页面加载）。Apple 头文件留在 `#ifndef _WIN32` 里，或 `#ifdef _WIN32` 的 `#else` 里。仍属于 macOS 底线、而不属于分支流程的细节留在 [macos-baseline.md](macos-baseline.md)。

**Windows。** 本 fork 没有 Windows 机器，也没有人在本地做 Windows 验收。唯一的 Windows 信号来自 GitHub Actions，按需手动运行（见下一节）。[`.github/workflows/ci.yml`](../.github/workflows/ci.yml) 还会对每个 pull request 和推到 `main` 的提交，在 `windows-latest` 上对已发布的 wheel 做冒烟。

## GitHub Actions

fork 的 Actions 额度有限。macOS 和 Linux 在维护者自己的机器上验收，所以 Actions 不构建它们。

| 工作流 | 何时运行 | 用途 |
| --- | --- | --- |
| `ci.yml`、`mac-pr.yml` | 每个 pull request 和推到 `main` | 便宜的检查（Python lint、守卫、wheel 冒烟）。保持开启。 |
| `build-windows.yml` | 只能手动 | Windows 从源码构建及其测试。唯一的 Windows 验收。 |
| `wheels.yml` | 只能手动。Windows 默认勾选，macOS 和 Linux 默认不勾 | 发版打 wheel。只有发版才勾 macOS 和 Linux。 |
| `build-macos.yml`、`build-linux.yml` | 只能手动 | 不做日常使用。用上面的 macOS 和 Linux 步骤。 |

规则：

1. 推送不触发构建。表里没有任何工作流会因 pull request 或推送而启动平台构建。
2. 只有改动可能影响 Windows 时，才从 `main` 或 PR 分支手动运行 `build-windows.yml`：`src/`、`CMakeLists.txt`、`tools/`、Windows 工作流或其测试、上游同步、发版。只改文档或只改 macOS 的不需要。
3. 每个改动跑一次，不是每次推送跑一次。还在返工的改动等到定稿再跑。不再需要的运行要取消。
4. 把 Windows 运行的链接和结果写进 PR 描述；没跑就写明没跑。
5. 不要用 Actions 的 macOS 或 Linux 构建来验收改动。如果 Actions 和本地结果不一致，只跑一次对应构建来复现，并把两边结果都写出来。
6. 发版是唯一一次三个平台都在 Actions 上构建，通过 `wheels.yml` 勾选所有平台。

## 向上游贡献

`upstream/<feature>` 从 `upstream/main` 拉出。只拣或重放那一个功能。保留原作者。一条分支一件事。fork 专有文件留在 fork：`docs/BRANCHES.md`、`docs/branching.md`、`docs/macos-baseline.md`、`docs/macos-gaps.md`、维护提示词、Mac PR 守卫，以及任何把 `runtime.json` 的 `macos.url` 指到本 fork release 的句子。分支只推到 `origin`。未经要求，无人值守的代理不要替人开或合并上游 pull request。说明末尾写 `Please review. I will not merge.`

## 过期分支

短分支在 pull request 合并、且没有别的东西指着它之后可以删除。还有未合并 pull request 的分支不要删。不要删 `main`、`release/macos`、`tls/necko-core-arm64`。没有独有提交的历史分支（`macos-core-proxy`、`macos-necko-adapter`）可以在不再需要旧名字时删除；在那之前留着。删除是单独、明确的一步。这份文档本身不删除任何分支。

## 当前分支

2026-11-03 读取。以 `git rev-parse` 为准，不以本表为准。

| 分支 | 用途 | 状态 |
| --- | --- | --- |
| `sync/0ab7201` | 把上游合并进 fork `main`。从 v0.3.5（`0ab7201`）开始，现已包含 v0.3.6（`3c3771e`） | 临时。这次合并进入 `main` 后删除。 |
| `sync/v0.3.4` | 把上游 v0.3.4（`6b6e0b9`，含 `fae5b82`）合并进 fork `main` | 已合并，`main` 为 `04426f6`（PR #23）。没有别的东西指向它之后可以删除。这次修改不删除该分支。 |
| `main` | 三平台主干 | `6251601`，jemalloc 的 `MOZ_MEMORY` 保护 |
| `release/macos` | `main` 的快进指针 | 与 `main` 同一提交 |
| `tls/necko-core-arm64` | `main` 的快进指针 | 与 `main` 同一提交。没有独有的 TLS 提交 |
| `macos-core-proxy` | 旧的代理试验 | 顶端 `302565c`。已在上游。没有独有提交 |
| `macos-necko-adapter` | 旧的 Darwin Necko 适配器 | 顶端 `00b31c5`。已作为上游 PR #9 进入上游 |
| `chore/mac-maint-bot-ci` | 值班提示词、Bugbot 规则、Mac PR 守卫 | PR #3 仍开着。底是更早的顶端。不在 `main` 上 |
| `cursor/cloud-agent-wine-e182` | Cloud Agent 的 Wine 说明 | PR #1 仍开着。说明不在 `main` 上 |
| `cursor/sync-upstream-0.3.3-711e` | 经 PR #4 进入主干的 0.3.3 同步 | 已合并。过期 |
| `cursor/*-711e`、`cursor/*-d26f` | 同步、基线和性能 PR 的会话分支 | 已进入 `main`。过期 |
| `upstream/*` | 为上游准备的补丁，各自从 `d41f247` 拉出 | 只在本 fork。还没有上游 pull request |

## 规则改了什么

旧说明写的是：修正先进入 `release/macos`，`main` 只做快进；每一条共享分支，包括短命的代理分支，都要把 SHA 写进 `docs/BRANCHES.md`；然后把这份地图提交推到每一条 `origin` 分支上。那份地图在写下的当天就已经过时（仍写着 `2e11166`，上游仍是 `d41f247`），而且一个文档笔误就要改写每一条分支。主干是 `main`。地图是这一份。角色变了才改它，指针前进不用改。
