# Contributing to ruyijs

Thanks for your interest! Bug reports, Firefox-parity findings, docs fixes and focused pull
requests are all welcome.

## Before you open a PR

Start in the relevant bounded context under [src/](./src/) and check [owner records](./docs/owners/)
for the state source, factory and installer before making a change. The essentials:

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
- **Compare with Firefox.** For behaviour changes, run the same minimal synthetic fixture
  on the candidate and on the Firefox version matching its source/donor. Record the exact
  Firefox version, both outputs, and any remaining differences in the PR description.

- **Choose the right base.** Read the [public fork maintenance rules](./docs/branching.md#public-fork-maintenance-scope)
  ([中文](./docs/branching.zh-CN.md#公开-fork-维护范围)). Fork-owned product work is macOS/Linux compatibility and performance;
  `main` remains the shared three-platform trunk. Start fork work from `origin/main` and send a
  reusable patch upstream from a clean `upstream/<topic>` branch based on `upstream/main`.

## Pull request checklist

- [ ] The owner record (bounded context, state source, factory, installer, tests) is updated for API changes
- [ ] For C++ changes, rebuild the shell and client library for affected platforms using the [platform instructions](./docs/branching.md#verification)
- [ ] Behaviour is checked through both Python and the C ABI
- [ ] Tests cover the owner, descriptors/prototypes, invalid receivers and realm behaviour, not just "it exists"
- [ ] The diff and PR attachments contain no private/product source from outside this public project, original materials, build outputs, captures, logs, credentials or proxy details
- [ ] For platform or performance changes, use the [PR evidence template](./docs/branching.md#pr-evidence-template) ([中文](./docs/branching.zh-CN.md#pr-证据模板)) and record which checks ran, their results, and why any were skipped

- [ ] If this pull request changes the role of a long-lived branch, [docs/branching.md](./docs/branching.md) and [docs/branching.zh-CN.md](./docs/branching.zh-CN.md) match. A fast-forward of `release/macos` or `tls/necko-core-arm64` does not need a docs commit, and the change is not copied onto every other branch

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
