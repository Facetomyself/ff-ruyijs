# macOS gaps and goals

Status after upstream merged PR #4 and PR #6. Rules for the next change are in [macos-baseline.md](macos-baseline.md). The comparison table stays in [macos.md](macos.md).

The same status is written in [macos-gaps.zh-CN.md](macos-gaps.zh-CN.md).

Checked on 2026-11-01.

## Sync status

The Windows font guard was absent on `0a82adb`. The fast-forward to upstream `main` brought in `d49bfd3`, `05b68fa`, and `da1df2c`. Upstream then advanced to `fd094ed` (Firefox 159 CI wheels). This checkout merged that tip into the local gaps line as `3aad54a`; later gaps docs may sit on that merge. The fork tip still published on GitHub is `c69875b` on `main`, `release/macos`, and `tls/necko-core-arm64` until credentials allow a push. `font_face_mac.cpp` on every tip below is the guarded file.

| Line | Tip | Guard in `font_face_mac.cpp` |
| --- | --- | --- |
| Upstream `cutetailbud/ff-ruyijs` `main` | `fd094ed4d04f17a81c53e71c764b6788f3198183` | Yes, commit `d49bfd3` |
| Local maintainer line after the merge | `3aad54a` and later gaps docs on top | Yes |
| Maintainer fork branches on GitHub | `c69875b` (docs on top of `da1df2c`) | Yes |
| Historical tip before the fast-forward | `0a82adb4e9c3ed1a046dde5953676c00442da59c` | No |

Upstream `main` already contains `0a82adb` through merge `0d42c60`. A branch that is still at `0a82adb` does not contain `d49bfd3`, `05b68fa`, or `da1df2c`.

`tools/product_sources.py` `sources()` compiles every flat `src/<domain>/*.cpp`. On `0a82adb`, `font_face_mac.cpp` includes `<CoreText/CoreText.h>` with no guard. A Windows build of that file stops on that include. Upstream `main` wraps the whole file in `#ifndef _WIN32`.

A pull request cut from `0a82adb` can hide this. When the branch does not touch `font_face_mac.cpp`, a three-dot diff omits the file, and the branch content is still the file that breaks Windows.

Other Apple includes in this tree sit inside `#ifndef _WIN32`, or inside the `#else` of `#ifdef _WIN32`. `system_font.cpp` includes Core Text only in that `#else`. `0a82adb` added no new `.cpp`. This audit is the current tree. It is not a second Windows build.

The upstream author did not run the macOS half when merging. After the fast-forward, this checkout rebuilt with `MACOSX_DEPLOYMENT_TARGET=26.0` against the SpiderMonkey and browser donors, linked `web_geometry_font_face_mac`, and retested the product: `Context.eval('1+1')` returned 2, and `navigate('https://example.com/')` reached status 200 with title `Example Domain`. This checkout has not rebuilt Windows on upstream `main`. The author's Windows result stays that comment: the guarded tree built with the same compile and link commands, and the C ABI, installed-wheel smoke, CreepJS (96 sections), and a 64-probe suite behaved as before.

## Docs brought in line

Two passages in `docs/macos.md` and `docs/macos.zh-CN.md` contradicted the post-merge status and were replaced while writing the first gaps note.

The maintainer-fork section said upstream `main` stayed the Windows release line, and that an upstream update was not merged into the fork's `main`. After PR #4 and PR #6, that `main` contains the macOS shell. The section now points here and at the baseline.

The comparison introduction said the previous local wheel and runtime zip were not rebuilt, and that the zip was not a 0.2.1 archive. The install row was already the current record: both files are on fork release `v0.2.1`, and `runtime.json` `macos.url` points at the zip. The introduction now says that.

A later pass found the first gaps note still describing the GitHub branches as unpushed at `0a82adb`. That text is replaced by the sync status above.

## Goals

1. Sync only. Done locally: the fork fast-forwarded through `da1df2c`, then merged `fd094ed` into the gaps line as `3aad54a` with no feature mixed into either sync. `d49bfd3`, `05b68fa`, `da1df2c`, and `fd094ed` are ancestors. `reset --hard` and a force-push stay unused. GitHub still publishes `c69875b` until credentials allow a push of the merge and the later gaps commits.
2. Keep the platform guard on every later commit. Verified on this tip: every Apple `CoreText` / `ImageIO` / `CoreGraphics` / `CoreFoundation` / `Security` include under `src/**/*.cpp` sits in a Darwin-only region (`#ifndef _WIN32` or the `#else` of `#ifdef _WIN32`). Fifteen includes across twelve files. A new product `.cpp` that includes an Apple header is wrapped before review.
3. Leave the socket process off. Verified: `necko_fetch.js` keeps both socket-process prefs false, `necko_client.py` sets `MOZ_DISABLE_SOCKET_PROCESS=1`, and `MOZ_DISABLE_SOCKET_PROCESS_SANDBOX` is absent from `src/` and `python/`. With the preferences on, this xpcshell exits with signal 11 in `GeckoChildProcessHost::FillMacSandboxInfo`, reached from `SocketProcessHost::FillMacSandboxInfo`. `plugin-container.app` exists only in the donor objdir, after `mach build ipc/app --allow-subdirectory-build`. It is not a product file. Direct HTTP/3 stays on `libnecko_quic`.
4. Keep the macOS wheel and zip on the fork release. Verified: release `v0.2.1` on `Facetomyself/ff-ruyijs` still lists both assets; the zip size and sha256 match `runtime.json` `macos`; the Windows `url` still points at `cutetailbud`. Change `macos.url` only when a new zip URL exists. Leave the Windows URL unchanged. Leave tag `v0.2.1` where it is.

## Closed in `0a82adb`

These are not open gaps.

- QUIC ClientHello counts match at the 16 fork points inside the existing `libnecko_quic` and Neqo 0.32.0. After CRYPTO reassembly, 16 versions printed ok and the failed count was 0. The first Initial packet alone is not a complete ClientHello when later bytes are split across packets. Records are not byte-identical. There is no JA3 score.
- A clean install imported. Direct HTTPS returned status 200 and version 20. A local HTTP/3 first response was status 200 and version 11. The second response was status 200 and version 30. `libnecko_quic.dylib` loaded from the packaged `dist/necko` directory.
- The wheel and `ruyijs-runtime-macos-arm64.zip` are on the fork release `v0.2.1`. `runtime.json` `macos.url` points at that zip. They are not on PyPI.

## Stays out of scope

COLRv1, Linux, Intel Macs, macOS older than 26, GIF pixel parity, extra font aliases, `wire_fields.py`, the DNS, connect, and TLS timing slots (they stay 0), opening all 60 profiles as pages, a required public HTTP/3 body retest, WebGPU, audio decode, WebCodecs, XML, custom built-ins, form target, a second QUIC stack, and JA3.

## Boundaries that remain

Without `--session`, the page shell starts one oneshot per request, so the `Alt-Svc` cache does not cross those processes. Version 11 is HTTP/1.1, 20 is HTTP/2, and 30 is HTTP/3.

A Windows rebuild of a branch that lacks `d49bfd3` fails on `<CoreText/CoreText.h>`.

Open PR #5 (`linux-native`) is a separate line. It is not the macOS sync.

## What this note does not do

It does not retype the font guard. The guard arrived by the fast-forward. It does not publish a new release.
