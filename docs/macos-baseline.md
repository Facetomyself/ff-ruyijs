# macOS maintenance baseline

Standing rules for later macOS work. The comparison table stays in [macos.md](macos.md). Current gaps and goals are in [macos-gaps.md](macos-gaps.md).

The same rules are written in [macos-baseline.zh-CN.md](macos-baseline.zh-CN.md).

## Integration base

Further macOS work is based on upstream `cutetailbud/ff-ruyijs` `main`.

Checked on 2026-11-01, that tip is `6d4531792b3f71379c9a53182930668f80bbdadf`, subject `release: pin the 0.3.0 runtime`. Read `main` again before the next sync. A new branch uses the tip read that day.

The maintainer fork is `Facetomyself/ff-ruyijs`. Before the fast-forward, its `main`, `release/macos`, and `tls/necko-core-arm64` were at `0a82adb4e9c3ed1a046dde5953676c00442da59c`. That commit is an ancestor of upstream `main` through merge `0d42c60`. It does not itself contain `d49bfd3`. The fast-forward to `da1df2c` is what brings the guard in. After that fast-forward, upstream advanced to `fd094ed`, then to `6d45317`. The fork line that already carried gaps docs on top of `da1df2c` merges `fd094ed`, then merges `6d45317` as `94f3540`, instead of resetting.

Commits that matter, newest first on upstream `main`:

| Commit | What it is |
| --- | --- |
| `6d45317` | `release: pin the 0.3.0 runtime`. |
| `d32dd74` | `release: 0.3.0 — wheels for Windows, macOS and Linux from the Firefox 159.0 source`. |
| `fd094ed` | CI builds Windows and macOS wheels from the Firefox 159.0 submodule. |
| `da1df2c` | Contributor avatars under the sponsor. Docs only. |
| `05b68fa` | Credits PR #6 next to PR #4. Docs only. |
| `0d42c60` | Merge of PR #6. Parents `48963a0` and `0a82adb`. |
| `0a82adb` | Fork tip before the fast-forward. QUIC ClientHello profiles and the published macOS wheel. |
| `48963a0` | Second merge of PR #4. WebTransport follow-up. |
| `9219fed` | First merge of PR #4. |
| `d49bfd3` | Windows guard around all of `src/web_geometry/font_face_mac.cpp`. |

The upstream author commented on PR #4 that the Windows build stopped at `<CoreText/CoreText.h>`, that the extra commit is `d49bfd3`, and that further macOS work should be based on `main`. The macOS half was not run there. The comment is on https://github.com/cutetailbud/ff-ruyijs/pull/4#issuecomment-6542165098. PR #6 is merged as `0d42c60`.

## Moving the fork

The next sync brings upstream `main` into the fork and contains no feature change.

`0a82adb` is an ancestor of the `main` checked above. The first sync fast-forwarded the fork branches through `da1df2c`, which brought in `d49bfd3`, `05b68fa`, and `da1df2c`. The second sync merges `fd094ed` into the gaps line that already sat on that tip. The third sync merges `6d45317` as `94f3540`.

Pushing `0a82adb` again as the current line leaves the guard and the later docs commits out. If the histories have diverged, merge upstream `main`. `reset --hard` and a force-push stay unused.

After the sync, the next feature branch is cut from that tip.

The maintainer does not push to `cutetailbud/ff-ruyijs` and does not merge its pull requests. A pull request targets that repository's `main`. The description ends with `Please review. I will not merge.`

Commits whose GitHub login is `charlesval` stay as they are. The author of a new commit is set only through the environment: `losenine <losenine@163.com>`. Git config stays unchanged.

The Mac clone receives a new commit as a bundle of `HEAD` excluding the parent full hash, fetched to `refs/incoming/macos`, then `git merge --ff-only`. A range `A..B` can produce an empty bundle. Git commands use `-C` on this checkout.

## Platform guard

`tools/product_sources.py` `sources()` compiles every flat `src/<domain>/*.cpp` on Windows and on macOS. A nested `.cpp` is an error. An Apple header in any of those units stops the Windows build.

Apple headers stay inside `#ifndef _WIN32`, or inside the `#else` of `#ifdef _WIN32`. `d49bfd3` uses that empty-unit pattern, the same one `svg_path.cpp` and `image_gif.cpp` already use, and wraps all of `font_face_mac.cpp`.

On a branch cut from `0a82adb`, `font_face_mac.cpp` includes `<CoreText/CoreText.h>` with no guard. Upstream `main` wraps the whole file. The Darwin statements inside that guard are the same text. This note does not record a new Mac run of that file.

Before a pull request, search the diff for `CoreText`, `ImageIO`, `CoreGraphics`, `CoreFoundation`, and `Security/` includes that sit outside those guards.

## Product floor

- The version string stays `neqo-0.32.0/nss-3.131`.
- `necko_quic_init` calls `nss::init()` first.
- The socket process stays off until a diagnosis with the sandbox launch enabled has passed. Preferences in `necko_fetch.js` stay false. Product code keeps `MOZ_DISABLE_SOCKET_PROCESS=1`.
- `MOZ_DISABLE_SOCKET_PROCESS_SANDBOX` stays out of product code. It is a one-off diagnosis.
- Ordinary HTTP/3 stays `webtransport=False`. `webtransport=true` belongs only to the long-lived WebTransport session.
- Certificate hashes stay ECDSA P-256, with validity of at most 14 days.
- Product code does not read `NECKO_EXTRA_CA`. A local HTTP/3 fixture may set it.
- One QUIC stack: `libnecko_quic` and Neqo 0.32.0. A second stack and a JA3 switch stay out.
- ClientHello follows the existing 100–159 fork points. Records are not required to be byte-identical.
- `@loader_path` stays. `install_name_tool` stays unused.
- `cargo update` stays unused.
- The library build is `python3 tools/build_necko_quic.py library`. The no-argument entry removes `/tmp/neqo-overlay` and also builds `neqo-server`, so that entry stays unused.
- The donor Firefox tree stays unmodified and uncommitted.

## What not to commit

Leave out the Firefox tree, either objdir, `dist/js`, the helper venv, the macOS wheel, the macOS runtime zip, `dist/necko_tls/libnecko_quic.dylib`, `neqo-server`, `native/necko_quic/Cargo.lock`, the echo binary, certificates, cookies, tokens, proxy values, fingerprint raw values, and response bodies.

New text files stay LF in git. `vendor/*` and `/dist/` stay gitignored.

## Release floor

Since 0.3.0, PyPI publishes a `macosx_26_0_arm64` wheel with no xpcshell. Proxies remain only in the donor build. The macOS zip and the wheel that includes xpcshell stay on `Facetomyself/ff-ruyijs` release `v0.2.1`. Those fork assets stay off `cutetailbud/ff-ruyijs` releases.

Write `runtime.json` `macos.url`, `sha256`, and `size` after that URL exists. The Windows `url`, `sha256`, and `size` stay as published in the current `runtime.json`.

An existing tag stays where it is. Fork tag `v0.2.1` was created before `0a82adb`. Its assets stay attached. A replacement archive uses a new tag or a new asset name.

Published macOS objects:

| File | Size | sha256 |
| --- | --- | --- |
| `ruyijs-runtime-macos-arm64.zip` | 109374640 | `f421e82e15b176af352345fee630175aa1df4fe13d1e4c3ebf21f36327011e56` |
| `ruyijs-0.2.1-py3-none-macosx_26_0_arm64.whl` | 109737476 | `1b70b21ca1e61762fe9eccd7321dfbfd40e57bbb2a37801240f8e9f994611727` |

The zip URL is `macos.url` in `runtime.json`: `https://github.com/Facetomyself/ff-ruyijs/releases/download/v0.2.1/ruyijs-runtime-macos-arm64.zip`.

The Windows archive is upstream `v0.3.0` `ruyijs-runtime-0.3.0-win-amd64.zip`, size 42977336, sha256 `d733f878ef5b4b7aacce715d0e7563e090b97198696ee2990ea07050680db2cc`, URL `https://github.com/cutetailbud/ff-ruyijs/releases/download/v0.3.0/ruyijs-runtime-0.3.0-win-amd64.zip`.

The Darwin wheel tag stays `macosx_26_0_arm64`.

## Pull request shape

One concern per pull request. The upstream sync is its own change.

The description says what ran on macOS, and it says when Windows was not rebuilt here. It carries no cookies, tokens, proxy values, certificate material, or fingerprint raw values.
