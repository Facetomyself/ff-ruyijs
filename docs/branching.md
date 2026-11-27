# Branching

How this fork (`Facetomyself/ff-ruyijs`) relates to upstream (`cutetailbud/ff-ruyijs`). The Chinese copy is [branching.zh-CN.md](branching.zh-CN.md). Both say the same rules.

## Public fork maintenance scope

`Facetomyself/ff-ruyijs` tracks `cutetailbud/ff-ruyijs`. Fork-owned product work is limited to macOS/Linux compatibility and performance. `main` remains the shared Linux, macOS, and Windows trunk: preserve existing Windows behavior and packaging, and check Windows when shared changes can affect it. This is a maintenance scope, not a change to the supported-platform trunk or a separate product line. Send reusable fixes upstream as small, single-purpose PRs; keep sync and fork-only maintenance separate.

| Remote | GitHub repository | Use |
| --- | --- | --- |
| `origin` | `https://github.com/Facetomyself/ff-ruyijs.git` | Fork branches and fork PRs |
| `upstream` | `https://github.com/cutetailbud/ff-ruyijs.git` | Fetch only; never push to this remote |

Check `git remote -v` before branch work. Keep separate products' source, private repositories and original materials out of this public fork and its upstream PRs, even as fixtures or attachments. Use public or synthetic fixtures. Leave out raw captures, request/response bodies, credentials, private logs, donor trees, objdirs and build artifacts. The old SHA ledger [BRANCHES.md](BRANCHES.md) points here; live branch tips come from fetched refs (`git rev-parse origin/main`, `git rev-parse upstream/main`).

## Long-lived branches

| Branch | Role | When it moves |
| --- | --- | --- |
| `main` | Fork trunk. Three platforms. Pull requests land here. | Merge a reviewed PR. Never force-push. |
| `release/macos` | Pointer at the same commit as `main`, so older Mac checkouts have a name. Not a place to commit. | Fast-forward to `main` after `main` moves. Plain push only (`git push origin origin/main:refs/heads/release/macos`). |
| `tls/necko-core-arm64` | Same kind of pointer. The TLS work already sits on `main`. No separate tip. | Same fast-forward as `release/macos`. |

`upstream/main` is the canonical project. Prepare reusable changes as [upstream PRs](#contributing-upstream); fork PRs target `Facetomyself/ff-ruyijs:main`.

## Short-lived names

Cut from fetched `origin/main` unless the row says otherwise. Use a clean worktree (`git status --short` is empty).

| Prefix | Use |
| --- | --- |
| `sync/<sha>` | One pinned upstream merge and any necessary conflict resolutions; no feature changes. |
| `feat/<topic>` | Compatibility work in the fork's scope. |
| `fix/<topic>` | A compatibility or regression fix. |
| `perf/<topic>` | One speed or memory change, with [before/after evidence](#performance-evidence). |
| `docs/<topic>` | Documentation only. |
| `chore/<topic>` | Maintainer tooling, CI, prompts. |
| `upstream/<topic>` | Cut from fetched **`upstream/main`** for a clean, single-purpose patch. Push the head to `origin` only. |

`cursor/<topic>` is an agent session branch. After its pull request merges, it is stale.

## Pulling upstream

1. Run `git fetch origin main` and `git fetch upstream main`, then `sha=$(git rev-parse upstream/main)`. If `git merge-base --is-ancestor "$sha" origin/main` succeeds, the fork already includes that upstream tip.
2. Otherwise run `git switch -c "sync/$(git rev-parse --short=8 "$sha")" origin/main` and `git merge --no-ff "$sha"`. Keep only the merge and required conflict resolutions; no rebase or force-push. Use `git merge --abort` to abandon an in-progress merge.
3. Verify affected platforms and open a fork PR to `main`. Record both full source SHAs, conflicts and resolutions, and the checks run. Keep feature PRs separate; if a patch depends on the sync, cut it after the sync lands.
4. After merge, `git fetch origin` and check `git merge-base --is-ancestor origin/<pointer> origin/main` for `release/macos` and `tls/necko-core-arm64` before fast-forwarding them. If a ref has diverged or a push is rejected, stop for maintainer review; leave shared history intact.

## Verification

| Platform | Supported target | Evidence for an affected change |
| --- | --- | --- |
| macOS | Apple Silicon (`arm64`), macOS 26+, wheel `macosx_26_0_arm64` | Native Mac, Python 3.12 for the maintainer build, `MACOSX_DEPLOYMENT_TARGET=26.0`. For shell/client changes check import, eval, and page load; for packaging changes check the installed wheel, not just the donor build. See [macOS build](macos.md) and [maintainer baseline](macos-baseline.md). |
| Linux | `x86_64`, glibc 2.39+, wheel `manylinux_2_39_x86_64`; reference host Ubuntu 24.04 | Build against the pinned `firefox/` submodule; Python 3.14 for Necko, distro Python for donor configure and the installed-wheel tests. See [Linux build](linux.md) and [Linux baseline](linux-baseline.md). |
| Windows | Existing x64 support, preserved through upstream sync and shared changes | Use [Windows source build](../.github/workflows/build-windows.yml) on demand for an affected Windows path. The automatic [CI](../.github/workflows/ci.yml) uses the published wheel, so it does not verify the proposed native build. |

Use native platforms for native claims. Intel Macs, older macOS, Linux architectures other than x86_64, and older glibc are outside this matrix. List each affected check as `pass`, `fail`, or `not run` with a reason. Missing platform evidence stays pending; a doc-only PR can report native checks as `not run (docs only)`.

**Linux:** From the repo root after setting up the submodule and [prerequisites](linux.md#build), use [the installed-wheel flow](../ci/linux/build.sh):

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

**macOS:** From the repo root on native arm64, set `RUYIJS_DONOR_OBJ` and `RUYIJS_FIREFOX_GFX_OBJ` to the absolute paths of the external SpiderMonkey standalone objdir and browser/Skia objdir for this candidate. Use the matching Firefox source revision and record the revision actually used; see [donor layout](macos.md#what-lives-where) and [helper prerequisites](macos.md#build-the-shell-and-the-helper).

```sh
: "${RUYIJS_DONOR_OBJ:?set the standalone donor objdir}"
: "${RUYIJS_FIREFOX_GFX_OBJ:?set the browser/Skia donor objdir}"
export MACOSX_DEPLOYMENT_TARGET=26.0
python3.12 -B tools/bootstrap_macos_helper.py
python3.12 -B tools/build.py --donor-obj "$RUYIJS_DONOR_OBJ" \
  --firefox-gfx-obj "$RUYIJS_FIREFOX_GFX_OBJ"
PYTHONPATH="$PWD/python" RUYIJS_SHELL="$PWD/dist/js" python3.12 -B ci/smoke_test.py
```

For network changes also check the affected path (e.g., [online page smoke](../ci/network_smoke.py)). For wheel changes follow the installed-wheel steps in the [macOS build workflow](../.github/workflows/build-macos.yml) on the Mac: install the candidate in a fresh venv, test outside the checkout without source/runtime overrides, and record whether the tested path has xpcshell. Apple headers stay inside `#ifndef _WIN32` or the `#else` of `#ifdef _WIN32`.

### Platform pins and rollback

Record a full tested RuyiJS SHA per platform in the PR, plus the actual Firefox submodule/donor SHA (`git ls-tree <tested-sha> firefox` shows the recorded submodule), wheel tag and artifact SHA-256 or runtime ID where relevant, and prior known-good SHA. A platform pin records what is being tracked or what passed a named check; label an untested candidate `not run`. A pin is not a release, tag, publication, or instruction to move a branch. Keep release actions separate and maintainer-controlled.

For a local retest or fallback, use the known-good SHA in a separate clean worktree, e.g. `git worktree add --detach <new-path> <known-good-sha>`, with its own matching donor and build outputs. For a regression already on shared `main`, cut a clean revert PR from `origin/main`: `git revert <bad-sha>` for a single commit, or `git revert -m 1 <merge-sha>` only after confirming parent 1 is the fork trunk being retained. Re-run affected checks and record the reverted and replacement SHAs. Keep shared history, platform branch pointers and tags intact during rollback; only normal forward updates follow the revert.

### Performance evidence

1. Compare a baseline and candidate SHA on the same native host, with the same toolchain/build mode, runtime type, dependencies and relevant settings (fonts, power mode, network mode). Pin the harness and workload: commands, input/fixture hash or revision, data size/concurrency, and cold/warm conditions. Run the same harness on both revisions; keep build outputs separate.
2. Check correctness on both revisions before collecting timings. Use the affected regression check and compare expected outputs or assertions for the timed workload (e.g., [layout checks](../ci/layout_check.py) compare mutated geometry with a fresh layout). Failed or wrong-output runs are not evidence of a speedup.
3. Use the same warmup and sample counts per revision, with at least five independent runs each. Report `n`, p50, p95 for series with at least 20 comparable observations (range instead of p95 for smaller series), units (e.g., µs, ms, MiB) and before/after delta. Keep cold and warm samples separate. For memory, say whether RSS is for one process or a process tree and when it was sampled.
4. On Linux run [ci/linux_baseline.py](../ci/linux_baseline.py) from outside the checkout with the installed wheel's Python and `PYTHONPATH`, `RUYIJS_SHELL`, and `LD_LIBRARY_PATH` unset; see [the command](linux-baseline.md#speed-and-memory). It includes loopback HTTP; `--network` adds a separate public HTTPS sample, not the main performance comparison. The harness uses Linux `/proc`. On macOS reuse a fixed portable workload (e.g., the 1,500-div case in `ci/layout_check.py` for layout) with the native runtime and record the exact harness and method. State which checks or measurements were not run and why.

## GitHub Actions

Routine macOS and Linux verification is native on maintainer machines, not a build on every push or PR.

| Workflow | Runs when | Use |
| --- | --- | --- |
| [ci.yml](../.github/workflows/ci.yml), [mac-pr.yml](../.github/workflows/mac-pr.yml) | PRs (`mac-pr.yml` targets `main`), pushes to `main`, or manual | Cheap checks (Python lint, guards, published-wheel smoke). Leave them on. |
| [build-windows.yml](../.github/workflows/build-windows.yml) | Manual or called by `wheels.yml` | Windows from-source build and tests. |
| [wheels.yml](../.github/workflows/wheels.yml) | Manual; Windows defaults on, macOS/Linux off | Builds release candidates; a run does not publish them. |
| [build-macos.yml](../.github/workflows/build-macos.yml), [build-linux.yml](../.github/workflows/build-linux.yml) | Manual or called by `wheels.yml` | Use native checks above for routine maintenance. |

Rules:

1. A pull request or push runs only the lightweight checks, not a native build.
2. Run `build-windows.yml` by hand from `main` or the pull request branch only when the change can affect Windows: `src/`, `CMakeLists.txt`, `tools/`, the Windows workflow or its tests, a sync from upstream, or a release. Docs-only and macOS-only changes do not need it.
3. Run it once per change, not once per push. A change that is still being reworked waits until it is ready. Cancel a run that is no longer needed.
4. Put the Windows run link and result in the pull request description, or say it did not run.
5. Do not run macOS or Linux builds on Actions to check a change. If Actions disagrees with a local result, run that build once to reproduce it, and report both.
6. A release is the only time all three platforms build on Actions, through `wheels.yml` with every platform ticked.

## Contributing upstream

1. From a clean worktree, `git fetch upstream main` and `git switch -c upstream/<topic> upstream/main` (replace `<topic>`). Cherry-pick only the clean, relevant commit(s) with `git cherry-pick -x <clean-commit>` and preserve authorship. If a fork commit mixes concerns, extract only the public change into a clean commit first; never merge fork `main` or a sync branch into the upstream head. Use `git cherry-pick --abort` to abandon a conflicted pick.
2. Review `git log --oneline upstream/main..HEAD`, `git diff --check upstream/main...HEAD`, and `git diff upstream/main...HEAD`. Keep fork branch/maintenance docs, maintainer prompts, Mac PR guards, fork release URLs such as `runtime.json`'s `macos.url`, and the private materials listed above out of the patch.
3. Push the head branch to `origin` only. PR **head**: `Facetomyself/ff-ruyijs:upstream/<topic>`; PR **base**: `cutetailbud/ff-ruyijs:main`. A human opens it, or explicitly instructs an agent to open that PR. The upstream maintainers decide whether to merge. End the description with `Please review. I will not merge.`

### PR evidence template

```text
Scope / affected platform(s):
Base and candidate SHA(s); sync SHA/conflicts if applicable:
Per platform: tested SHA, Firefox/donor SHA, OS/arch and toolchain,
  wheel/runtime identity, prior known-good SHA, command/result or not run + reason:
Perf if applicable: fixed harness/fixture, correctness before/after, cold/warm,
  warmups and n, p50/p95 (or range for small n), units and delta:
Rollback: prior known-good SHA or exact commit/merge to revert:
```

## Stale branches

Delete a short-lived branch after its pull request is merged and nothing else points at it. Do not delete a branch that still has an open pull request. Do not delete `main`, `release/macos`, or `tls/necko-core-arm64`. Historical branches with no unique commits (`macos-core-proxy`, `macos-necko-adapter`) can be deleted once no one needs the old name; until then leave them. Deleting is a separate, explicit step. This document does not do it.

## Historical branch snapshot

Read on 2026-11-03; this is not a current pin ledger. Use fetched refs and `git rev-parse` for current tips.

| Branch | Purpose | Status |
| --- | --- | --- |
| `sync/0ab7201` | Open merge of upstream into fork `main`. Started at v0.3.5 (`0ab7201`); now also includes v0.3.6 (`3c3771e`) | Temporary. Deleted after that merge is on `main`. |
| `sync/v0.3.4` | Merge of upstream v0.3.4 (`6b6e0b9`, including `fae5b82`) | Merged into `main` at `04426f6` (PR #23). The branch can be deleted once nothing else points at it. This change does not delete it. |
| `main` | Three-platform trunk | `6251601`, the jemalloc `MOZ_MEMORY` guard |
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
