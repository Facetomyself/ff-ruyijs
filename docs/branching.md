# Branching

How this fork (`Facetomyself/ff-ruyijs`) relates to upstream (`cutetailbud/ff-ruyijs`). The Chinese copy is [branching.zh-CN.md](branching.zh-CN.md). Both say the same rules.

`main` is the trunk for Linux, macOS, and Windows together. A change lands on `main` only after the platforms it can affect have been checked, using the commands below. Platform branches are not a second product line.

The old SHA ledger is [BRANCHES.md](BRANCHES.md). It now points here. Do not copy a tip SHA into every branch. Run `git fetch origin` and `git fetch upstream`, then `git rev-parse origin/<branch>`.

## Long-lived branches

| Branch | Role | When it moves |
| --- | --- | --- |
| `main` | Fork trunk. Three platforms. Pull requests land here. | Merge a reviewed PR. Never force-push. |
| `sync/<upstream-sha>` | Temporary. Cut from `main`, then merge `upstream/main`. No rebase. | Deleted after that merge is on `main`. |
| `release/macos` | Pointer at the same commit as `main`, so older Mac checkouts have a name. Not a place to commit. | Fast-forward to `main` after `main` moves. Plain push only (`git push origin origin/main:refs/heads/release/macos`). |
| `tls/necko-core-arm64` | Same kind of pointer. The TLS work already sits on `main`. No separate tip. | Same fast-forward as `release/macos`. |

`upstream/main` is the canonical project. Fetch it. Do not push it. A change meant for the published project is prepared on `upstream/<feature>` (below) and opened by a person against `cutetailbud/ff-ruyijs` `main`. This fork does not merge those pull requests.

## Short-lived names

Cut from `main` unless the row says otherwise.

| Prefix | Use |
| --- | --- |
| `sync/<upstream-sha>` | One merge of `upstream/main` into a branch off `main`. |
| `feat/<topic>` | New behavior. |
| `fix/<topic>` | A bugfix. |
| `perf/<topic>` | A speed or memory change, with before/after numbers. |
| `docs/<topic>` | Documentation only. |
| `chore/<topic>` | Maintainer tooling, CI, prompts. |
| `upstream/<feature>` | Cut from **`upstream/main`**, not from this fork's `main`. Only changes that belong in the published project. No fork release URLs, branch maps, or maintainer-bot files. Push to this fork. A person opens the upstream pull request. |

`cursor/<topic>` is an agent session branch. After its pull request merges, it is stale.

## Pulling upstream

1. `git fetch upstream main`.
2. From `main`, create `sync/<upstream-sha>` and merge `upstream/main`. Do not rebase. Do not force-push.
3. Verify each platform that the merge can affect (next section).
4. Open a pull request into `main`. The description lists conflicts and how they were resolved.
5. After it merges, fast-forward `release/macos` and `tls/necko-core-arm64` to `main` if they are ancestors. If a push is rejected, stop. Do not force it.

Feature work done while a sync is open is cut from that sync branch, and its pull request targets the sync branch or `main` after the sync merges. It does not commit on `release/macos`.

## Verification

Say in the pull request which of these ran, and which did not.

**Linux.** A cloud agent or any Ubuntu 24.04 machine, from a checkout that has the `firefox/` submodule. Steps and the extra packages some images need are in [linux.md](linux.md).

```sh
ci/linux/build.sh deps
ci/linux/build.sh donor
ci/linux/build.sh shell
ci/linux/build.sh necko    # needs Python 3.14 as python3, or PYTHON=python3.14
ci/linux/build.sh wheel
ci/linux/build.sh test     # smoke, helper, layout, atob, network, proxy, ClientHello, engine
```

A performance change also runs `ci/linux_baseline.py --network` from outside the checkout, with the wheel's interpreter, and reports before and after. See [linux-baseline.md](linux-baseline.md).

**macOS.** The maintainer's macos-maint Mac mini (arm64), not a Linux cloud agent. Donor build, from [macos.md](macos.md):

```sh
python3.12 -B tools/bootstrap_macos_helper.py
python3.12 -B tools/build.py --donor-obj ../firefox-159/obj-js-standalone
```

`MACOSX_DEPLOYMENT_TARGET=26.0`. The donor tree stays outside the repository. Say what was actually run (import, `dist/js` eval, a page load). Apple headers stay inside `#ifndef _WIN32` or the `#else` of `#ifdef _WIN32`. Details that are still the macOS floor, not the branch procedure, stay in [macos-baseline.md](macos-baseline.md).

**Windows.** This fork has no Windows machine and no one runs a from-source Windows check before merge. A push to `main` starts [`.github/workflows/wheels.yml`](../.github/workflows/wheels.yml), which builds Windows, macOS, and Linux wheels on GitHub-hosted runners. [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) smokes the published wheel on `windows-latest`. That is the only Windows signal. It is not a local verification step.

## Contributing upstream

Branch `upstream/<feature>` from `upstream/main`. Cherry-pick or re-apply only that feature. Keep the original author. One concern per branch. Fork-only files stay out: `docs/BRANCHES.md`, `docs/branching.md`, `docs/macos-baseline.md`, `docs/macos-gaps.md`, maintainer prompts, Mac PR guards, and any sentence that points `runtime.json` `macos.url` at this fork's release. Push the branch to `origin` only. Do not open or merge the upstream pull request from an unattended agent unless asked. The description ends with `Please review. I will not merge.`

## Stale branches

Delete a short-lived branch after its pull request is merged and nothing else points at it. Do not delete a branch that still has an open pull request. Do not delete `main`, `release/macos`, or `tls/necko-core-arm64`. Historical branches with no unique commits (`macos-core-proxy`, `macos-necko-adapter`) can be deleted once no one needs the old name; until then leave them. Deleting is a separate, explicit step. This document does not do it.

## Current branches

Read on 2026-11-03. `git rev-parse` wins over this table.

| Branch | Purpose | Status |
| --- | --- | --- |
| `sync/v0.3.4` | Merge of upstream v0.3.4 (`6b6e0b9`, including `fae5b82`) | Merged into `main` at `04426f6` (PR #23). The branch can be deleted once nothing else points at it. This change does not delete it. |
| `main` | Three-platform trunk | `04426f6`, merge of the v0.3.4 sync |
| `release/macos` | Fast-forward pointer of `main` | Same commit as `main` |
| `tls/necko-core-arm64` | Fast-forward pointer of `main` | Same commit as `main`. No unique TLS commits |
| `macos-core-proxy` | Old proxy experiment | Tip `302565c`. Already in upstream. No unique commits |
| `macos-necko-adapter` | Old Darwin Necko adapter | Tip `00b31c5`. Already in upstream as PR #9 |
| `chore/mac-maint-bot-ci` | Duty prompt, Bugbot rules, Mac PR guard | Open PR #3. Based on an older tip. Not on `main` |
| `cursor/cloud-agent-wine-e182` | Wine note for Cloud Agents | Open PR #1. The note is not on `main` |
| `cursor/sync-upstream-0.3.3-711e` | The 0.3.3 sync that landed through PR #4 | Merged. Stale |
| `cursor/*-711e`, `cursor/*-d26f` | Session branches for the sync, baseline, and performance PRs | Merged into `main`. Stale |
| `upstream/*` | Patches prepared for upstream, each off `d41f247` | On the fork only. No upstream pull request yet |

## What changed in the rules

Older notes said a fix lands on `release/macos` first and `main` only fast-forwards, that every shared branch including a short-lived agent branch must have its SHA written into `docs/BRANCHES.md`, and that the map commit is then pushed onto every `origin` branch. That made the map stale on the day it was written (`2e11166`, upstream still `d41f247`) and it required rewriting every branch for a documentation typo. The trunk is `main`. The map is this file. Update it when a role changes, not when a pointer moves.
