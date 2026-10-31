# macOS 当前缺口与目标

上游合并 PR #4 和 PR #6 之后的状态。下一次改动的规则在 [macos-baseline.zh-CN.md](macos-baseline.zh-CN.md)。比对表仍在 [macos.zh-CN.md](macos.zh-CN.md)。

同一份状态的英文版在 [macos-gaps.md](macos-gaps.md)。

核对日期是 2026-10-31。

## 眼前的缺口

fork 尖端没有 Windows 字体守卫，也没有 PR #6 之后的两次只改文档的提交。

| 线 | 尖端 | `font_face_mac.cpp` 里的守卫 |
| --- | --- | --- |
| 上游 `cutetailbud/ff-ruyijs` 的 `main` | `da1df2ce375131eb37234dba4638a5ce0d96a532` | 有，提交 `d49bfd3` |
| fork 的 `main`、`release/macos`、`tls/necko-core-arm64` | `0a82adb4e9c3ed1a046dde5953676c00442da59c` | 没有 |

上游 `main` 已经通过合并 `0d42c60` 包含 `0a82adb`。fork 不包含 `d49bfd3`、`05b68fa` 和 `da1df2c`。

`tools/product_sources.py` 的 `sources()` 编译每一个平铺的 `src/<domain>/*.cpp`。在 `0a82adb` 上，`font_face_mac.cpp` 直接包含 `<CoreText/CoreText.h>`，没有守卫。这个文件的 Windows 构建会停在这个包含上。上游 `main` 用 `#ifndef _WIN32` 包住了整个文件。

从 `0a82adb` 切出的 pull request 可能把这一点藏起来。分支没有改 `font_face_mac.cpp` 时，三点 diff 不会列出这个文件，分支内容仍然是那个会打断 Windows 构建的文件。

这棵树里的其他 Apple 包含已经在 `#ifndef _WIN32` 里面，或者在 `#ifdef _WIN32` 的 `#else` 里面。`system_font.cpp` 只在那个 `#else` 里包含 Core Text。`0a82adb` 没有新增 `.cpp`。这次核对的是当前树，不是第二次 Windows 构建。

上游作者没有跑 macOS 这一半。上游守卫里面的 Darwin 文本与未加守卫的文件正文一致。本说明不把守卫之后的字面说成又做了一次新的 Mac 运行。

这个检出没有在上游 `main` 上重编 Windows。作者的 Windows 结果仍以那条评论为准：加守卫后的树用同一套编译和链接命令构建，C ABI、已安装 wheel 的冒烟、CreepJS（96 个小节）和一套 64 探针的表现与之前一致。

## 文档已经对齐的两处

`docs/macos.md` 和 `docs/macos.zh-CN.md` 里有两段文字和这份状态矛盾，写本说明时已换掉。

维护方 fork 那一节原来写着：上游 `main` 仍是 Windows 发布线，上游更新不直接合并进该 fork 的 `main`。PR #4 和 PR #6 之后，那个 `main` 已经包含 macOS 外壳。那一节现在指向这里和底线文档。

比对引言原来写着：上一份本地 wheel 和运行时压缩包没有重打，那份压缩包也不是 0.2.1。安装那一行本来就是当前记录：两份文件都在 fork Release `v0.2.1` 上，`runtime.json` 的 `macos.url` 指向这份压缩包。引言现在改成这个事实。

## 目标

1. 只做同步。把 fork 移到上游 `main`，让 `d49bfd3`、`05b68fa` 和 `da1df2c` 进入 `main`、`release/macos` 和 `tls/necko-core-arm64`。这次同步不混入功能。不使用 `reset --hard`，也不强推。步骤在底线文档里。
2. 之后的每次提交都守住平台守卫。新的产品 `.cpp` 若包含 Apple 头文件，审查前先包上守卫。
3. socket process 保持关闭。偏好打开时，这只 xpcshell 在 `GeckoChildProcessHost::FillMacSandboxInfo` 里以信号 11 退出，调用来自 `SocketProcessHost::FillMacSandboxInfo`。`plugin-container.app` 只存在于 donor 的 objdir，来自 `mach build ipc/app --allow-subdirectory-build`。它不是产品文件。`MOZ_DISABLE_SOCKET_PROCESS_SANDBOX=1` 仍只是一次诊断。直连 HTTP/3 继续走 `libnecko_quic`。
4. macOS wheel 和压缩包继续放在 fork Release 上。只有新的压缩包 URL 已经存在时才改 `macos.url`。Windows 的 URL 保持不动。标签 `v0.2.1` 留在原地。

## 已在 `0a82adb` 关闭

这些不是还开着的缺口。

- QUIC ClientHello 的个数在现有 `libnecko_quic` 和 Neqo 0.32.0 里，于 16 个分叉点上对齐。CRYPTO 重组之后，16 个版本打印 ok，失败数为 0。后面的字节拆到多个包里时，单独的第一个 Initial 包不是一份完整的 ClientHello。记录不要求逐字节相同。没有 JA3 分数。
- 干净安装可以导入。直连 HTTPS 返回状态 200、版本码 20。本机 HTTP/3 的第一次响应是状态 200、版本码 11，第二次是状态 200、版本码 30。`libnecko_quic.dylib` 从打包后的 `dist/necko` 加载。
- wheel 和 `ruyijs-runtime-macos-arm64.zip` 在 fork Release `v0.2.1` 上。`runtime.json` 的 `macos.url` 指向这份压缩包。它们不在 PyPI。

## 仍在范围之外

COLRv1、Linux、Intel Mac、低于 macOS 26 的系统、GIF 像素对齐、额外字体别名、`wire_fields.py`、DNS / connect / TLS 计时槽（保持 0）、把全部 60 个配置当页面打开、把公网 HTTP/3 正文复测当成必做项、WebGPU、音频解码、WebCodecs、XML、自定义内置元素、表单目标、第二条 QUIC 栈，以及 JA3。

## 仍然成立的边界

不用 `--session` 时，页面外壳每个请求启动一次 oneshot，因此 `Alt-Svc` 缓存不会跨过这些进程。版本码 11 是 HTTP/1.1，20 是 HTTP/2，30 是 HTTP/3。

缺少 `d49bfd3` 的分支在 Windows 上重编时，会停在 `<CoreText/CoreText.h>`。

打开的 PR #5（`linux-native`）是另一条线。它不是这次 macOS 同步。

## 本说明不做什么

本说明不补上字体守卫，不合并 fork，也不发布新的 Release。这些留到下一次按底线文档进行的改动。
