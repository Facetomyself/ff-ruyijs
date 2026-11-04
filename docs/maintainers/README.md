# Maintainer automation

Ops notes for `Facetomyself/ff-ruyijs`. These files do not change product behavior. Branch rules are in [../branching.md](../branching.md): `main` is the trunk, an upstream update is merged on `sync/<sha>`, and `release/macos` and `tls/necko-core-arm64` are fast-forward pointers of `main`.

| File | Purpose |
| --- | --- |
| [grok-bot-duty.md](grok-bot-duty.md) | Paste-ready Grok Bot duty prompt for sync / triage / Cloud Agent dispatch |
| [../../.cursor/BUGBOT.md](../../.cursor/BUGBOT.md) | Bugbot review rules |
| [../../.cursor/config/bugbot.yaml](../../.cursor/config/bugbot.yaml) | Repo Bugbot triggers (read from the PR **base** branch) |
| [../../.github/workflows/mac-pr.yml](../../.github/workflows/mac-pr.yml) | Minimal CI for pull requests into `main` |
| [../../ci/mac_pr_guard.py](../../ci/mac_pr_guard.py) | Required-docs + Apple-header guard scan |

Standing macOS rules stay in [../macos-baseline.md](../macos-baseline.md).
