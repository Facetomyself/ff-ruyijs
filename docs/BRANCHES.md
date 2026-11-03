# Branches

This is the map of the macOS maintainer fork and the upstream project. The Chinese copy is [BRANCHES.zh-CN.md](BRANCHES.zh-CN.md). Both files state the same facts.

`AGENTS.md`, `CONTRIBUTING.md`, and `.github/copilot-instructions.md` require every shared-branch change to update both files before the work is finished. A shared branch is any branch on `origin` or `upstream`, including a short-lived agent branch. A branch that exists only on one machine and was never pushed stays out of this map.

The SHAs below were read on 2026-11-03 after `git fetch origin` and `git fetch upstream`. They are the work tips. Commits whose subject starts with `docs: map the fork` or `docs: keep the branch map` sit on top of those tips and are this map; they do not replace the work tip. Run `git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short) %(objectname:short) %(subject)' refs/heads refs/remotes` before treating any other SHA as current. This checkout was on `macos-necko-adapter` when the map was written.

This map is kept on every branch of `origin`. After it changes, those documentation commits are applied to each `origin` branch and pushed. A branch that can take them by fast-forward does. A diverged branch receives them by cherry-pick, and its other changes stay. This checkout does not push `upstream`.

## Remotes

| Remote | Repository | Use |
| --- | --- | --- |
| `origin` | https://github.com/Facetomyself/ff-ruyijs | This fork. Push here. |
| `upstream` | https://github.com/cutetailbud/ff-ruyijs | Canonical project. The push URL in this checkout is `DISABLED`. Fetch it, and open a pull request against it from a fork branch. |

Some clones still have `refs/remotes/upstream-check/main` at `fd094ed`. No `upstream-check` remote is configured. Leave that ref alone.

## How a change moves

Upstream `main` is the release line of cutetailbud/ff-ruyijs. On this fork the macOS maintenance line is `release/macos`. A fix lands there first. The fork's `main` then fast-forwards to the same commit.

An upstream update is brought across on a branch cut from `release/macos`: merge upstream there, review that branch, merge it back into `release/macos`, then fast-forward the fork's `main`. The fork's `main` receives the result by that fast-forward.

`main`, `release/macos`, and `tls/necko-core-arm64` currently share `2e11166` ("Record 0.3.0 as the macOS maintenance baseline.", 2026-11-01). Upstream `main` is `d41f247` ("release: pin the 0.3.3 runtime", 2026-11-02). Tags `v0.3.1`, `v0.3.2`, and `v0.3.3` point at that upstream history. The fork's `main` is 9 commits ahead of upstream `main` (its own maintenance records) and 53 commits behind. The branch that already contains both tips is `cursor/sync-upstream-0.3.3-711e`.

## Which branch to check out

| Task | Branch |
| --- | --- |
| Patch the published 0.3.3 tree | `upstream/main` |
| macOS maintenance that should become the fork default | `release/macos`, then fast-forward `main` |
| Review the 0.3.3 sync onto the fork baseline | `cursor/sync-upstream-0.3.3-711e` |
| Read the Darwin Necko adapter trial | `macos-necko-adapter` |
| Read the two HTTP-proxy commits | `macos-core-proxy` |
| Edit the project web site | `upstream/gh-pages` |

## Fork branches

`origin` is https://github.com/Facetomyself/ff-ruyijs.

### `main`

Default branch of the fork. `origin/main` is `2e11166` (2026-11-01). It matches `release/macos` and `tls/necko-core-arm64`.

The nine commits upstream `main` lacks are maintenance records: the baseline note, the gaps notes, and the merges that brought upstream's 0.3.0 / Firefox 159 wheel floor onto the fork. After `release/macos` moves, fast-forward `main` to that same commit. New product work starts on a branch cut from `release/macos`, or from `upstream/main` when the change is for the published project.

### `release/macos`

Same tip as the fork's `main` (`2e11166`). This is the branch a macOS fix merges into. Earlier release work — the Firefox donor shell, the adapters, the helper, and the 0.2.1 upstream merge — landed here before `main` fast-forwarded. Cut the next maintenance branch from this tip.

### `tls/necko-core-arm64`

Same tip as the fork's `main` (`2e11166`). The branch began at `d170a06` for direct macOS HTTPS through arm64 `libnecko_core` and the Firefox 100–159 TLS profile. The measurement notes are [tls-profile.md](tls-profile.md) and [tls-profile.zh-CN.md](tls-profile.zh-CN.md). Those notes still describe HTTP/2 and page measurements taken on this branch before the pointer joined the 0.3.0 baseline. There is no separate TLS tip to check out. A new TLS change starts from `release/macos` or from `upstream/main`, on the line that should carry it.

### `macos-necko-adapter`

Darwin Necko adapter. Local `macos-necko-adapter` and `origin/macos-necko-adapter` are `00b31c5` ("Merge upstream main into the Darwin Necko adapter.", 2026-11-01).

It contains `macos-core-proxy`. On top of that it runs the Windows `necko` / `ruyijs_necko` packages on macOS, records the recovered ClientHello, adds the HTTP/3 bridge, stages the adapter as the runtime, covers CONNECT-proxy page loads in CI, falls back to HTTP/1.1 when a TLS peer omits ALPN, and snapshots WebTransport state before a session closes. The trial write-up is [macos-necko-adapter-spike.md](macos-necko-adapter-spike.md).

Upstream `main` contains this tip (pull request #9). `cursor/sync-upstream-0.3.3-711e` contains it too. The fork's `main` is still the 0.3.0 baseline: this branch is 14 commits ahead of `origin/main` and 9 behind it. Upstream `main` is 39 commits past this tip, through 0.3.3. Adapter work that should ship with the published project continues from `upstream/main`, or from the sync branch once that branch is the fork line under review. This tip stays the fork's record of the adapter as proposed.

### `macos-core-proxy`

`302565c` ("Say when a proxy stays on xpcshell and when it uses CONNECT.", 2026-11-01), on `origin` and locally. Two commits sit on `6d45317` ("release: pin the 0.3.0 runtime"). They let a macOS wheel without xpcshell use an HTTP proxy, and they say when a proxy stays on xpcshell and when it uses CONNECT.

Pull request #7 merged this branch. `macos-necko-adapter` and upstream `main` both contain the tip. The fork's `main` is still the baseline: the branch is 2 commits ahead of `origin/main` and 9 behind it, and 51 behind upstream `main`. The local branch tracks `upstream/main`, so status can report it behind upstream while its own work remains those two commits. Leave the branch as history. Later proxy work lives on the adapter line and on upstream `main`.

### `cursor/sync-upstream-0.3.3-711e`

On `origin` only. Tip `a11cfd4` (2026-11-03) merges `upstream/main` (`d41f247`, 0.3.3) into the fork baseline (`2e11166`).

The branch contains the fork's `main` (54 commits ahead, 0 behind) and upstream `main` (10 commits ahead, 0 behind). Those 10 commits are the fork's nine maintenance records plus this merge. The diff against upstream `main` is the fork's macOS maintenance set: `docs/macos-baseline.md`, `docs/macos-gaps.md`, their Chinese copies, and small edits to `CHANGELOG.md`, `CONTRIBUTING.md`, `docs/macos.md`, and `docs/macos.zh-CN.md`. It contains the Darwin adapter because upstream `main` already does.

This is the review branch for bringing 0.3.3 onto the fork. It becomes `release/macos` when that review merges it back, and the fork's `main` fast-forwards afterwards. It was not the checkout used to write this map.

### `chore/mac-maint-bot-ci`

On `origin` only. `0ca5f5d` (2026-10-31) is one commit on `c69875b`: a Grok Bot duty prompt, Bugbot rules, and a Mac pull-request guard (`.cursor/BUGBOT.md`, `.cursor/config/bugbot.yaml`, `.github/workflows/mac-pr.yml`, `ci/mac_pr_guard.py`, `docs/maintainers/grok-bot-duty.md`). It is 1 commit ahead of `origin/main` and 16 behind, and it is not merged. It is maintainer automation. A new product change starts from `release/macos` or `upstream/main`. Continue this automation from this branch, then merge the result through `release/macos`.

### `cursor/cloud-agent-wine-e182`

On `origin` only. `8ef9157` (2026-10-30) is one documentation commit. It explains that Cloud Agents run ruyijs under Wine because the host Python cannot import the Windows engine, and it edits `AGENTS.md`. It is 1 commit ahead of `origin/main` and 48 behind, and it is not merged. The Wine note is still only on this branch.

## Upstream branches

`upstream` is https://github.com/cutetailbud/ff-ruyijs. This checkout fetches it and does not push it.

### `main`

`d41f247` (2026-11-02), tag `v0.3.3`. This is the canonical line. Past the 0.3.0 pin it contains the Darwin adapter (pull request #9), the Core Text and DOMException port (pull request #8, merge `163621e` from `isesword/upstream-mac`), the ClientHello fixes (pull request #10), and the 0.3.1–0.3.3 releases: `Engine` sessions in one process, Necko helpers started from bytecode, and geometry that restyles only what a style change reaches. Published wheels and version tags come from this branch. The fork still calls it the Windows release line because macOS maintenance on the fork lands on `release/macos` first.

### `ci/macos`

`ed189ef` (2026-11-01). macOS arm64 source-build and wheel CI. It repeatedly merges `ci/source-build`. Sixteen of its commits are absent from upstream `main`. Later wheel CI on `main` took its own path. Read this branch for that CI experiment. Build the product from `main`.

### `ci/source-build`

`89e260b` (2026-11-01). Shared CI fixes: strip CR from the browser build steps, parse every object-list style, link libraries in order, and resolve `build.py` paths. Nine commits are absent from upstream `main`. `ci/macos` contains this tip.

### `gh-pages`

`4394b97` (2026-10-30). The GitHub Pages site: `llms.txt`, `robots.txt`, the sitemap, and the sponsor and branding updates. It is the site branch, separate from the engine tree.

### `review/pr8`

`48f20d2` (2026-11-01), "Merge pull request #8 (review build)". A review snapshot of the Core Text shaping port, the DOMException surface, `matchMedia`, and a configurable NSS directory for `libnecko_core`. This ref is not an ancestor of upstream `main` (upstream `main` has 22 commits that this ref lacks, and the histories differ). The port that landed is pull request #8, merge `163621e`, which upstream `main` contains and which sits on the history of `v0.3.3`. New work on that port starts from upstream `main`.

## Updating this map

Update this file and [BRANCHES.zh-CN.md](BRANCHES.zh-CN.md) in the same change when any of the following happens:

- A branch is created, renamed, deleted, or pushed on `origin` or `upstream`.
- A shared branch moves to a new tip, or a pull request merges it.
- The role of a branch changes: where a fix lands, or which branch a new person should check out.
- A SHA, date, or "contains / is contained in" sentence here no longer matches `git`.

Record the remote, the tip SHA, the subject, the date, what the branch is for, and which branch now holds that work. Run `git fetch origin` and `git fetch upstream` first when the network is available. When a fetch did not run, write that the snapshot is from local refs and give the date. Ahead and behind counts are part of the snapshot; recompute them with `git rev-list --count` instead of copying an old number.

The English file and the Chinese file name the same branches, tips, and roles. A change to one is unfinished until the other matches. It is also unfinished until every `origin` branch contains that change and the commits are pushed.
