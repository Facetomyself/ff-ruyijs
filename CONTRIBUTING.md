# Contributing to ruyijs

Thanks for your interest! Bug reports, Firefox-parity findings, docs fixes and focused pull
requests are all welcome.

## Before you open a PR

ruyijs keeps a strict architecture. Please read [ARCHITECTURE.md](./ARCHITECTURE.md) and the
relevant [owner record](./docs/owners) first. The essentials:

- **One owner per API.** Every constructor, prototype, descriptor and global has exactly one
  production installer. Extend the existing owner. Do not add a second implementation or an
  `if (!window.X)` fallback.
- **No JavaScript overlays.** Browser APIs are native C++ in their bounded context
  (`src/<context>/`). Do not generate or inject JS shims, and do not hard-code site-specific values.
- **Dependency direction.** Domain code has no SpiderMonkey, Python or C ABI dependency.
  Adapters translate, and interfaces own only ABI and lifecycle. Python and the C ABI share one
  runtime assembly.
- **Realm-correct objects.** Realm objects are created by that realm's factory and never cloned
  from the main realm.
- **One browser API domain per change.** Any new single file over 200 lines needs a short
  responsibility and split rationale in the PR description.
- **Measure against Firefox.** Behaviour changes should cite real Firefox 159 output (for
  example via `tools/firefox_parity`) and update [docs/DEVIATIONS.md](./docs/DEVIATIONS.md) when
  a difference remains.

- **Cut from the recorded line.** Read [docs/BRANCHES.md](./docs/BRANCHES.md)
  ([中文](./docs/BRANCHES.zh-CN.md)) before choosing a base. On this fork, macOS fixes land on
  `release/macos` first and `main` fast-forwards to the same commit. An upstream update is merged
  on a branch cut from `release/macos`, reviewed, and merged back.

## Pull request checklist

- [ ] The owner record (bounded context, state source, factory, installer, tests) is updated for API changes
- [ ] When C++ changes, the shell is rebuilt (`js.exe` on Windows, `js` on macOS) together with the client library (`python -B tools/build.py ...`)
- [ ] Behaviour is checked through both Python and the C ABI
- [ ] Tests cover the owner, descriptors/prototypes, invalid receivers and realm behaviour, not just "it exists"
- [ ] The diff contains no build outputs, captures, logs, credentials or proxy details

- [ ] If this pull request creates, retargets, merges, or drops a shared branch, [docs/BRANCHES.md](./docs/BRANCHES.md) and [docs/BRANCHES.zh-CN.md](./docs/BRANCHES.zh-CN.md) match the new tips and roles, and that same update is pushed to every `origin` branch

## Reporting issues

Please include the ruyijs version or commit, your Windows version or your macOS version
and Xcode version, the Firefox tag, and which of the two donor objdirs the build used.
Also include a minimal script, the actual output and, where possible, what real Firefox
returns for the same code. macOS maintainers follow [docs/macos.md](./docs/macos.md), [docs/macos-baseline.md](./docs/macos-baseline.md), and [docs/macos-gaps.md](./docs/macos-gaps.md).

ff-ruyijs is dual-licensed under the [AGPL-3.0](./LICENSE) and a
[commercial license](./COMMERCIAL-LICENSE.md). By submitting a contribution you
agree that it is licensed under the AGPL-3.0, and you grant the project author a
perpetual, worldwide, non-exclusive, royalty-free, irrevocable license to use,
modify, sublicense and distribute your contribution under other license terms,
including commercial ones. You confirm that you have the right to grant this.
Changes to Mozilla-derived files remain under the MPL-2.0.
