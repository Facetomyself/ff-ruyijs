# macOS 维护与提交底线

后续 macOS 工作的常驻规则。和 Windows 的比对表仍在 [macos.zh-CN.md](macos.zh-CN.md)。当前缺口和目标在 [macos-gaps.zh-CN.md](macos-gaps.zh-CN.md)。

同一份规则的英文版在 [macos-baseline.md](macos-baseline.md)。

## 集成底

后续 macOS 工作以上游 `cutetailbud/ff-ruyijs` 的 `main` 为底。

2026-10-31 核对时，这个尖端是 `da1df2ce375131eb37234dba4638a5ce0d96a532`，说明是 `docs: show contributors under the sponsor as round avatars`。下一次同步前再读一次 `main`。新分支用当天读到的尖端。

维护方 fork 是 `Facetomyself/ff-ruyijs`。它的 `main`、`release/macos` 和 `tls/necko-core-arm64` 停在 `0a82adb4e9c3ed1a046dde5953676c00442da59c`。该提交经合并 `0d42c60` 成为上游 `main` 的祖先，本身不包含其后的上游提交。

上游 `main` 上需要记住的提交，从新到旧：

| 提交 | 内容 |
| --- | --- |
| `da1df2c` | 赞助者下方的贡献者圆头像。只改文档。 |
| `05b68fa` | 在 PR #4 旁边补上 PR #6 的署名。只改文档。 |
| `0d42c60` | 合并 PR #6。父提交是 `48963a0` 和 `0a82adb`。 |
| `0a82adb` | fork 尖端。QUIC ClientHello 配置，以及已发布的 macOS wheel。 |
| `48963a0` | PR #4 的第二次合并。WebTransport 的后续提交。 |
| `9219fed` | PR #4 的第一次合并。 |
| `d49bfd3` | 用 Windows 守卫包住整个 `src/web_geometry/font_face_mac.cpp`。 |

上游作者在 PR #4 的评论里写明：Windows 构建停在 `<CoreText/CoreText.h>`，补上的提交是 `d49bfd3`，后续 macOS 工作应以 `main` 为底。那里没有跑 macOS 这一半。评论在 https://github.com/cutetailbud/ff-ruyijs/pull/4#issuecomment-6542165098 。PR #6 已作为 `0d42c60` 合并。

## 移动 fork

下一次同步把上游 `main` 带进 fork，这次同步本身不带功能改动。

上面核对的 `main` 仍以 `0a82adb` 为祖先，因此同步是把 fork 分支快进到那个 `main`。这次快进带入 `d49bfd3`、`05b68fa` 和 `da1df2c`。

再把 `0a82adb` 当成当前线推上去，守卫和后面的文档提交就会留在外面。历史若已经分叉，就合并上游 `main`。不使用 `reset --hard`，也不强推。

同步之后，下一个功能分支从那个尖端切出。

维护方不向上游 `cutetailbud/ff-ruyijs` 推送，也不合并那边的 pull request。pull request 的目标是该仓库的 `main`。说明末尾写 `Please review. I will not merge.`

GitHub 登录名为 `charlesval` 的提交保持原样。新提交的作者只通过环境变量设置为 `losenine <losenine@163.com>`。不改 git config。

Mac 克隆用 bundle 接收新提交：打包 `HEAD` 并排除父提交的完整哈希，取到 `refs/incoming/macos`，再 `git merge --ff-only`。范围 `A..B` 可能打出空 bundle。git 命令用 `-C` 指向本仓库。

## 平台守卫

`tools/product_sources.py` 的 `sources()` 在 Windows 和 macOS 上编译每一个平铺的 `src/<domain>/*.cpp`。嵌套的 `.cpp` 会报错。这些编译单元里只要出现 Apple 头文件，Windows 构建就会停。

Apple 头文件放在 `#ifndef _WIN32` 里面，或者放在 `#ifdef _WIN32` 的 `#else` 里面。`d49bfd3` 用的就是这种空编译单元，`svg_path.cpp` 和 `image_gif.cpp` 已经这么写，并包住整个 `font_face_mac.cpp`。

从 `0a82adb` 切出的分支上，`font_face_mac.cpp` 直接包含 `<CoreText/CoreText.h>`，没有守卫。上游 `main` 包住了整个文件。守卫里面的 Darwin 语句是同一段文本。本说明没有为这个字面再记一次新的 Mac 运行。

开 pull request 之前，在 diff 里查找落在这些守卫外面的 `CoreText`、`ImageIO`、`CoreGraphics`、`CoreFoundation` 和 `Security/` 包含。

## 产品底线

- 版本字符串保持 `neqo-0.32.0/nss-3.131`。
- `necko_quic_init` 先调用 `nss::init()`。
- 在 sandbox 启动开启的诊断通过之前，socket process 保持关闭。`necko_fetch.js` 里的偏好保持 false。产品代码保留 `MOZ_DISABLE_SOCKET_PROCESS=1`。
- `MOZ_DISABLE_SOCKET_PROCESS_SANDBOX` 不进入产品代码。它只用于一次诊断。
- 普通 HTTP/3 保持 `webtransport=False`。`webtransport=true` 只属于 WebTransport 那条长连接。
- 证书哈希保持 ECDSA P-256，有效期最多 14 天。
- 产品代码不读 `NECKO_EXTRA_CA`。本机 HTTP/3 夹具可以设置它。
- 只有一条 QUIC 栈：`libnecko_quic` 和 Neqo 0.32.0。不加第二条栈，也不加 JA3 开关。
- ClientHello 沿用已有的 100–159 分叉点。记录不要求逐字节相同。
- 保持 `@loader_path`。不使用 `install_name_tool`。
- 不运行 `cargo update`。
- 库的构建命令是 `python3 tools/build_necko_quic.py library`。不带参数的入口会删掉 `/tmp/neqo-overlay`，并且还会构建 `neqo-server`，因此不使用那个入口。
- donor Firefox 树不修改，也不提交。

## 不要提交的东西

不要提交 Firefox 树、两份 objdir、`dist/js`、helper venv、macOS wheel、macOS 运行时压缩包、`dist/necko_tls/libnecko_quic.dylib`、`neqo-server`、`native/necko_quic/Cargo.lock`、回声程序、证书、cookie、token、代理值、指纹原值或响应正文。

新的文本文件在 git 里保持 LF。`vendor/*` 和 `/dist/` 继续被 gitignore。

## 发布底线

macOS 产物只挂在 `Facetomyself/ff-ruyijs` 的 Release 上。不上传到 PyPI，也不挂到 `cutetailbud/ff-ruyijs` 的 Release。

`runtime.json` 的 `macos.url`、`sha256` 和 `size` 在该 URL 已经存在之后再写。Windows 的 `url`、`sha256` 和 `size` 保持已发布的值。

已有标签留在原地。fork 的标签 `v0.2.1` 创建于 `0a82adb` 之前。它的附件留在那里。替换用的压缩包用新标签或新的附件名。

已发布的 macOS 对象：

| 文件 | 大小 | sha256 |
| --- | --- | --- |
| `ruyijs-runtime-macos-arm64.zip` | 109374640 | `f421e82e15b176af352345fee630175aa1df4fe13d1e4c3ebf21f36327011e56` |
| `ruyijs-0.2.1-py3-none-macosx_26_0_arm64.whl` | 109737476 | `1b70b21ca1e61762fe9eccd7321dfbfd40e57bbb2a37801240f8e9f994611727` |

压缩包 URL 就是 `runtime.json` 里的 `macos.url`：`https://github.com/Facetomyself/ff-ruyijs/releases/download/v0.2.1/ruyijs-runtime-macos-arm64.zip`。

Windows 压缩包保持 `ruyijs-runtime-0.2.1-win-amd64.zip`，大小 42739018，sha256 `488f3b59dc2abb84d60c6dae6433fe711502b904e421bd8f939d85e088f95eca`，URL `https://github.com/cutetailbud/ff-ruyijs/releases/download/v0.2.1/ruyijs-runtime-0.2.1-win-amd64.zip`。

Darwin wheel 标签保持 `macosx_26_0_arm64`。

## Pull request 的形状

一个 pull request 只做一件事。上游同步单独成一次改动。

说明里写清 macOS 上跑了什么，以及这次有没有在这里重编 Windows。说明里不放 cookie、token、代理值、证书材料或指纹原值。
