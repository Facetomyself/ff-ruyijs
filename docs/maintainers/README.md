# Maintainer automation

Ops notes for the macOS maintainer line on `Facetomyself/ff-ruyijs`. These files do not change product behavior.

| File | Purpose |
| --- | --- |
| [grok-bot-duty.md](grok-bot-duty.md) | Paste-ready Grok Bot duty prompt for weekly sync / triage / Cloud Agent dispatch |
| [../../.cursor/BUGBOT.md](../../.cursor/BUGBOT.md) | Bugbot review rules for Mac PRs |
| [../../.cursor/config/bugbot.yaml](../../.cursor/config/bugbot.yaml) | Repo Bugbot triggers (read from the PR **base** branch) |
| [../../.github/workflows/mac-pr.yml](../../.github/workflows/mac-pr.yml) | Minimal CI for PRs into `release/macos` |
| [../../ci/mac_pr_guard.py](../../ci/mac_pr_guard.py) | Required-docs + Apple-header guard scan |

Standing macOS rules stay in [../macos-baseline.md](../macos-baseline.md).
