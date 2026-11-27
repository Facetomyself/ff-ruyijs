# 分支

本 fork（`Facetomyself/ff-ruyijs`）与上游（`cutetailbud/ff-ruyijs`）的关系。英文版是 [branching.md](branching.md)。两份说的是同一套规则。

## 公开 fork 维护范围

`Facetomyself/ff-ruyijs` 持续接入 `cutetailbud/ff-ruyijs` 的更新。fork 自有产品改动限 macOS/Linux 兼容和性能优化。`main` 仍是 Linux、macOS、Windows 共用的主干：维持 Windows 既有行为和打包，共用改动影响 Windows 时也要验收。这是维护范围，三平台主干角色保持原样，平台分支并非独立产品线。可复用的小修复及时按单一事项向上游提 PR，同步和 fork 专有维护各自独立。

| Remote | GitHub 仓库 | 用途 |
| --- | --- | --- |
| `origin` | `https://github.com/Facetomyself/ff-ruyijs.git` | fork 分支与 fork PR |
| `upstream` | `https://github.com/cutetailbud/ff-ruyijs.git` | 只用于拉取，禁止推送 |

操作分支前先看 `git remote -v`。独立产品源码、私有仓库内容和原始材料留在公开 fork 和上游 PR 之外，测试夹具和附件也一样。用公开或合成夹具，排除原始抓包、请求与响应正文、凭据、私有日志、donor 树、objdir 和构建产物。旧 SHA 台账 [BRANCHES.zh-CN.md](BRANCHES.zh-CN.md) 指向本页；实时分支顶端以拉取后的引用为准（`git rev-parse origin/main`、`git rev-parse upstream/main`）。

## 长期分支

| 分支 | 角色 | 何时移动 |
| --- | --- | --- |
| `main` | fork 主干。三个平台。pull request 合到这里。 | 合并已审查的 PR。不用 force-push。 |
| `release/macos` | 与 `main` 同一提交的指针，给还停在这个名字上的 Mac 检出用。不在上面写提交。 | `main` 前进之后快进。只用普通推送（`git push origin origin/main:refs/heads/release/macos`）。 |
| `tls/necko-core-arm64` | 同样的指针。TLS 工作已经在 `main` 上。没有单独的顶端。 | 与 `release/macos` 一起快进。 |

`upstream/main` 是上游基准。可复用改动按[向上游贡献](#向上游贡献)准备；fork PR 的目标为 `Facetomyself/ff-ruyijs:main`。

## 短分支的名字

除表中写明的以外，都从拉取后的 `origin/main` 创建。使用干净工作树（`git status --short` 输出为空）。

| 前缀 | 用途 |
| --- | --- |
| `sync/<sha>` | 单次合并固定的上游 SHA，只带必要的冲突解决，功能改动另开。 |
| `feat/<topic>` | fork 范围内的兼容改动。 |
| `fix/<topic>` | 兼容或回归修复。 |
| `perf/<topic>` | 单项速度或内存优化，附[前后证据](#性能证据)。 |
| `docs/<topic>` | 只改文档。 |
| `chore/<topic>` | 维护工具、CI、提示词。 |
| `upstream/<topic>` | 从拉取后的 **`upstream/main`** 创建，只携带干净的单项补丁。head 只推 `origin`。 |

`cursor/<主题>` 是代理会话分支。对应 pull request 合并后即算过期。

## 接入上游

1. 执行 `git fetch origin main` 和 `git fetch upstream main`，再执行 `sha=$(git rev-parse upstream/main)`。若 `git merge-base --is-ancestor "$sha" origin/main` 成功，则 fork 已包含该上游顶端。
2. 否则执行 `git switch -c "sync/$(git rev-parse --short=8 "$sha")" origin/main` 和 `git merge --no-ff "$sha"`。只保留合并和必要的冲突解决，保留原有历史，禁止 rebase 或强推。要放弃正在进行的合并，执行 `git merge --abort`。
3. 核验受影响的平台，再向 fork 的 `main` 开 PR。记录两个完整的来源 SHA、冲突与解决方式、实际跑过的检查。功能 PR 单独提交；依赖这次同步的补丁，等同步合入后再开分支。
4. 合入后，执行 `git fetch origin`，用 `git merge-base --is-ancestor origin/<pointer> origin/main` 逐项检查 `release/macos` 和 `tls/necko-core-arm64` 后再快进。若引用已分叉或普通推送失败，停下来交维护者核对，保留共享历史。

## 验收

| 平台 | 支持目标 | 受影响改动的证据 |
| --- | --- | --- |
| macOS | Apple Silicon（`arm64`）、macOS 26+，wheel `macosx_26_0_arm64` | 原生 Mac，维护构建使用 Python 3.12 和 `MACOSX_DEPLOYMENT_TARGET=26.0`。外壳或客户端改动验收导入、求值、页面加载；打包改动验收已安装的 wheel，donor 构建并非 wheel 验收。见 [macOS 构建](macos.zh-CN.md)和[维护基线](macos-baseline.zh-CN.md)。 |
| Linux | `x86_64`、glibc 2.39+，wheel `manylinux_2_39_x86_64`；参考环境为 Ubuntu 24.04 | 使用固定的 `firefox/` 子模块构建；Necko 用 Python 3.14，donor 配置与安装后测试用发行版 Python。见 [Linux 构建](linux.zh-CN.md)和 [Linux 基线](linux-baseline.md)。 |
| Windows | 保持现有 x64 支持，上游同步和共用改动仍须兼容 | 影响 Windows 路径时按需使用 [Windows 源码构建](../.github/workflows/build-windows.yml)。自动 [CI](../.github/workflows/ci.yml) 使用已发布 wheel，无法验证 PR 提议的原生构建。 |

原生兼容结论使用原生平台验证。Intel Mac、低于 26 的 macOS、非 x86_64 Linux 和低于 2.39 的 glibc 均在矩阵之外。受影响检查逐项写 `通过`、`失败` 或 `未运行`，附原因。缺少平台证据时保持待验收；纯文档 PR 可标为 `未运行（仅文档）`。

**Linux：** 准备子模块和[构建依赖](linux.zh-CN.md#构建)后，在仓库根目录运行 [wheel 构建与安装后测试流程](../ci/linux/build.sh)：

```sh
export RUNNER_TEMP="$(mktemp -d)"
ci/linux/build.sh deps
export PATH="/usr/lib/llvm-21/bin:$PATH"
ci/linux/build.sh donor
ci/linux/build.sh shell
PYTHON=python3.14 ci/linux/build.sh necko
ci/linux/build.sh wheel
ci/linux/build.sh test
```

**macOS：** 在原生 arm64 Mac 的仓库根目录，把 `RUYIJS_DONOR_OBJ` 和 `RUYIJS_FIREFOX_GFX_OBJ` 分别设为本候选对应的外置 SpiderMonkey standalone objdir 和 browser/Skia objdir 的绝对路径。使用匹配的 Firefox 源码版本并记录实际采用的版本；见 [donor 目录](macos.zh-CN.md#各部分放在哪)和 [helper 依赖](macos.zh-CN.md#编译外壳和-helper)。

```sh
: "${RUYIJS_DONOR_OBJ:?set the standalone donor objdir}"
: "${RUYIJS_FIREFOX_GFX_OBJ:?set the browser/Skia donor objdir}"
export MACOSX_DEPLOYMENT_TARGET=26.0
python3.12 -B tools/bootstrap_macos_helper.py
python3.12 -B tools/build.py --donor-obj "$RUYIJS_DONOR_OBJ" \
  --firefox-gfx-obj "$RUYIJS_FIREFOX_GFX_OBJ"
PYTHONPATH="$PWD/python" RUYIJS_SHELL="$PWD/dist/js" python3.12 -B ci/smoke_test.py
```

网络改动另验受影响路径（如[联网加载冒烟](../ci/network_smoke.py)）。wheel 改动参考 [macOS 构建工作流](../.github/workflows/build-macos.yml)的安装后测试步骤，在 Mac 上用全新 venv 安装候选 wheel，在检出目录之外清除源码和运行时路径覆盖后验证，并记录被测路径是否带 xpcshell。Apple 头文件留在 `#ifndef _WIN32` 或 `#ifdef _WIN32` 的 `#else` 内。

### 平台固定 SHA 与回滚

PR 按平台记下被测 RuyiJS 完整 SHA、实际使用的 Firefox 子模块/donor SHA（`git ls-tree <tested-sha> firefox` 可看该提交记录的子模块）、相关 wheel 标签与产物 SHA-256 或 runtime 标识，以及上一已验证 SHA。固定 SHA 只记录纳管版本或具名检查的通过版本；尚未验证的候选标记 `未运行`。固定 SHA 与发行、打标签、发布产物或移动分支是两回事，发行由维护者单独处理。

本地重测或临时回退时，从上一已验证 SHA 建独立、干净的工作树，例如 `git worktree add --detach <new-path> <known-good-sha>`，配套匹配的 donor 和独立的构建输出。回归已进入共享 `main` 时，从 `origin/main` 开干净的回滚 PR：单提交用 `git revert <bad-sha>`；合并提交先确认第 1 父是要保留的 fork 主干，再用 `git revert -m 1 <merge-sha>`。复验受影响平台，记录被回滚和替代的 SHA。回滚时保留共享历史、平台分支指针和 tag，随后只做正常向前更新。

### 性能证据

1. 在同一台原生主机比较基准与候选 SHA，保持工具链、构建模式、运行时类型、依赖和相关设置（字体、电源、网络模式）一致。固定测试工具与工作负载：命令、输入或夹具的哈希/版本、数据规模与并发、冷暖条件。两个版本用同一测试工具，构建输出分开。
2. 先验证两个版本的正确性，再计时。运行相关回归检查，对照被测负载的预期输出或断言（例如 [布局检查](../ci/layout_check.py)比较变更后的几何结果与全新布局）。失败或输出错误的运行不能作为提速证据。
3. 两个版本使用相同的预热与采样次数，各至少独立运行五次。报告 `n`、p50、p95（单组可比观测达到 20 个时给出，否则用范围代替 p95）、单位（如 µs、ms、MiB）与前后差值。冷暖样本分开。测内存时写明 RSS 的采样时点，以及统计单进程还是进程树。
4. Linux 在检出目录外用已安装 wheel 的 Python 运行 [ci/linux_baseline.py](../ci/linux_baseline.py)，清除 `PYTHONPATH`、`RUYIJS_SHELL`、`LD_LIBRARY_PATH`，见[命令](linux-baseline.md#speed-and-memory)。脚本包含本机回环 HTTP，`--network` 只追加一条公网 HTTPS 样本，单列而非主性能对比。此脚本依赖 Linux `/proc`。macOS 用原生运行时复用固定的可移植工作负载（例如布局优化使用 `ci/layout_check.py` 的 1,500 个 div 场景），记录具体测试工具和测量方法。没跑的检查与测量写明原因。

## GitHub Actions

macOS 和 Linux 的日常验收在维护者的原生机器上进行，PR 或推送无需触发原生构建。

| 工作流 | 何时运行 | 用途 |
| --- | --- | --- |
| [ci.yml](../.github/workflows/ci.yml)、[mac-pr.yml](../.github/workflows/mac-pr.yml) | PR（`mac-pr.yml` 目标为 `main`）、推到 `main` 或手动 | 轻量检查（Python lint、守卫、已发布 wheel 冒烟）。保持开启。 |
| [build-windows.yml](../.github/workflows/build-windows.yml) | 手动或由 `wheels.yml` 调用 | Windows 源码构建及其测试。 |
| [wheels.yml](../.github/workflows/wheels.yml) | 手动；Windows 默认开启，macOS/Linux 默认关闭 | 构建候选发行产物；运行工作流本身与发布分开。 |
| [build-macos.yml](../.github/workflows/build-macos.yml)、[build-linux.yml](../.github/workflows/build-linux.yml) | 手动或由 `wheels.yml` 调用 | 日常维护使用上面的原生验收。 |

规则：

1. PR 或推送只运行轻量检查，原生构建单独触发。
2. 只有改动可能影响 Windows 时，才从 `main` 或 PR 分支手动运行 `build-windows.yml`：`src/`、`CMakeLists.txt`、`tools/`、Windows 工作流或其测试、上游同步、发版。只改文档或只改 macOS 的不需要。
3. 每个改动跑一次，不是每次推送跑一次。还在返工的改动等到定稿再跑。不再需要的运行要取消。
4. 把 Windows 运行的链接和结果写进 PR 描述；没跑就写明没跑。
5. 不要用 Actions 的 macOS 或 Linux 构建来验收改动。如果 Actions 和本地结果不一致，只跑一次对应构建来复现，并把两边结果都写出来。
6. 发版是唯一一次三个平台都在 Actions 上构建，通过 `wheels.yml` 勾选所有平台。

## 向上游贡献

1. 在干净工作树执行 `git fetch upstream main` 和 `git switch -c upstream/<topic> upstream/main`（替换 `<topic>`）。用 `git cherry-pick -x <clean-commit>` 拣选干净且相关的提交，保留原作者。若 fork 提交混合多个事项，先把公开部分拆成干净提交；上游 head 禁止合入 fork 的 `main` 或同步分支。要放弃冲突的拣选，执行 `git cherry-pick --abort`。
2. 审核 `git log --oneline upstream/main..HEAD`、`git diff --check upstream/main...HEAD` 和 `git diff upstream/main...HEAD`。补丁排除 fork 分支与维护文档、维护提示词、Mac PR 守卫、`runtime.json` 的 `macos.url` 等 fork Release URL，以及前述私有材料。
3. head 分支只推 `origin`。PR **head**：`Facetomyself/ff-ruyijs:upstream/<topic>`；PR **base**：`cutetailbud/ff-ruyijs:main`。由人创建，或由人明确指示代理创建这一条上游 PR。是否合并由上游维护者决定。说明末尾写 `Please review. I will not merge.`

### PR 证据模板

```text
范围 / 受影响平台：
基准与候选 SHA；若为同步，填上游 SHA 与冲突：
逐平台：被测 SHA、Firefox/donor SHA、OS/架构和工具链、
  wheel/runtime 标识、上一已验证 SHA、命令与结果，或未运行及原因：
如有性能改动：固定测试工具与夹具、前后正确性、冷暖条件、
  预热与采样数 n、p50/p95（样本少则给范围）、单位与差值：
回滚：上一已验证 SHA，或需 revert 的确切提交/合并 SHA：
```

## 过期分支

短分支在 pull request 合并、且没有别的东西指着它之后可以删除。还有未合并 pull request 的分支不要删。不要删 `main`、`release/macos`、`tls/necko-core-arm64`。没有独有提交的历史分支（`macos-core-proxy`、`macos-necko-adapter`）可以在不再需要旧名字时删除；在那之前留着。删除是单独、明确的一步。这份文档本身不删除任何分支。

## 历史分支快照

2026-11-03 读取，仅为历史记录。当前顶端以拉取后的引用及 `git rev-parse` 为准。

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
