# macOS gaps and goals

Status after upstream merged PR #4 and PR #6. Rules for the next change are in [macos-baseline.md](macos-baseline.md). The comparison table stays in [macos.md](macos.md).

The same status is written in [macos-gaps.zh-CN.md](macos-gaps.zh-CN.md).

Checked on 2026-10-31.

## Immediate gap

The Windows font guard was absent on `0a82adb`. The fast-forward to upstream `main` puts `d49bfd3`, `05b68fa`, and `da1df2c` under the fork tip. `font_face_mac.cpp` on this tip is the guarded file. Pushing that tip is a separate step. Until the push, GitHub's three branches stay at `0a82adb`.

| Line | Tip | Guard in `font_face_mac.cpp` |
| --- | --- | --- |
| Upstream `cutetailbud/ff-ruyijs` `main` | `da1df2ce375131eb37234dba4638a5ce0d96a532` | Yes, commit `d49bfd3` |
| Local fork branches after the fast-forward | parent `da1df2c`, plus this documentation | Yes |
| GitHub fork branches before the push | `0a82adb4e9c3ed1a046dde5953676c00442da59c` | No |

Upstream `main` already contains `0a82adb` through merge `0d42c60`. A branch that is still at `0a82adb` does not contain `d49bfd3`, `05b68fa`, or `da1df2c`.

`tools/product_sources.py` `sources()` compiles every flat `src/<domain>/*.cpp`. On `0a82adb`, `font_face_mac.cpp` includes `<CoreText/CoreText.h>` with no guard. A Windows build of that file stops on that include. Upstream `main` wraps the whole file in `#ifndef _WIN32`.

A pull request cut from `0a82adb` can hide this. When the branch does not touch `font_face_mac.cpp`, a three-dot diff omits the file, and the branch content is still the file that breaks Windows.

Other Apple includes in this tree sit inside `#ifndef _WIN32`, or inside the `#else` of `#ifdef _WIN32`. `system_font.cpp` includes Core Text only in that `#else`. `0a82adb` added no new `.cpp`. This audit is the current tree. It is not a second Windows build.

The upstream author did not run the macOS half. The Darwin text inside the upstream guard matches the body of the unguarded file. This note does not claim a new Mac run of that face after the guard.

This checkout has not rebuilt Windows on upstream `main`. The author's Windows result stays that comment: the guarded tree built with the same compile and link commands, and the C ABI, installed-wheel smoke, CreepJS (96 sections), and a 64-probe suite behaved as before.

## Docs brought in line

Two passages in `docs/macos.md` and `docs/macos.zh-CN.md` contradicted this status and were replaced while writing this note.

The maintainer-fork section said upstream `main` stayed the Windows release line, and that an upstream update was not merged into the fork's `main`. After PR #4 and PR #6, that `main` contains the macOS shell. The section now points here and at the baseline.

The comparison introduction said the previous local wheel and runtime zip were not rebuilt, and that the zip was not a 0.2.1 archive. The install row was already the current record: both files are on fork release `v0.2.1`, and `runtime.json` `macos.url` points at the zip. The introduction now says that.

## Goals

1. Sync only. The local fast-forward to upstream `main` is done, with no feature mixed in. `d49bfd3`, `05b68fa`, and `da1df2c` are ancestors of this tip. `reset --hard` and a force-push stay unused. The GitHub branches move when this tip is pushed.
2. Keep the platform guard on every later commit. A new product `.cpp` that includes an Apple header is wrapped before review.
3. Leave the socket process off. With the preferences on, this xpcshell exits with signal 11 in `GeckoChildProcessHost::FillMacSandboxInfo`, reached from `SocketProcessHost::FillMacSandboxInfo`. `plugin-container.app` exists only in the donor objdir, after `mach build ipc/app --allow-subdirectory-build`. It is not a product file. `MOZ_DISABLE_SOCKET_PROCESS_SANDBOX=1` stayed a one-off diagnosis. Direct HTTP/3 stays on `libnecko_quic`.
4. Keep the macOS wheel and zip on the fork release. Change `macos.url` only when a new zip URL exists. Leave the Windows URL unchanged. Leave tag `v0.2.1` where it is.

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

It does not retype the font guard. The guard arrives by the fast-forward. It does not publish a new release, and it does not push the fork.
