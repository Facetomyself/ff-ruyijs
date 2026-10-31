# Bugbot rules — Facetomyself/ff-ruyijs (macOS maintainer line)

Review PRs with the macOS maintainer baseline in mind (`docs/macos-baseline.md`). Prefer real defects over style nits.

## Platform / Windows safety

- Flag any new or moved include of `CoreText`, `ImageIO`, `CoreGraphics`, `CoreFoundation`, or `Security/` that is **not** inside `#ifndef _WIN32` or the `#else` of `#ifdef _WIN32`.
- Flag Apple-only `.cpp` units under flat `src/<domain>/` that would compile on Windows without an empty-unit / guard pattern (see upstream `d49bfd3` / `font_face_mac.cpp`).
- Flag changes that would break the published Windows wheel path or assume a macOS-only runtime in shared Python code without a platform check.

## Necko / networking

- Flag setting `channel.redirectionLimit = 0` (causes immediate redirect-loop errors).
- Flag dropping or ignoring HTTP response headers when adapting Necko → requests-like responses (`Location`, `Set-Cookie`, `Content-Type`, etc.).
- Flag re-enabling the socket process, or product code that sets `MOZ_DISABLE_SOCKET_PROCESS_SANDBOX`. Prefs in `necko_fetch.js` that disable the socket process must stay off unless the PR is explicitly a sandbox diagnosis.
- Flag product code that reads `NECKO_EXTRA_CA`.
- Flag introducing a second QUIC/JA3 stack; keep `libnecko_quic` + Neqo 0.32.0 / NSS 3.131.

## macOS packaging / donors

- Flag commits that add Firefox source trees, objdirs, `dist/js`, helper venvs, macOS wheels/runtime zips, certs, cookies, tokens, proxy values, or fingerprint raw dumps.
- Flag `install_name_tool` usage or dropping `@loader_path` conventions.
- Flag changing Windows `runtime.json` url/sha256/size while updating macOS fields, unless the PR is explicitly a coordinated release.
- Flag uploading macOS artifacts to PyPI or to `cutetailbud/ff-ruyijs` releases.

## Process

- Prefer one concern per PR. Upstream sync should not mix feature work.
- If the PR needs a real macOS arm64 build/donor and has no hardware verification notes, call that out as a residual risk (do not block on style).
- Do not suggest Playwright/Puppeteer/Selenium or a visible browser as replacements for ruyijs.
