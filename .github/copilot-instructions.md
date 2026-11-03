# Copilot Instructions for ff-ruyijs

## Project overview

ff-ruyijs is a headless Firefox engine for Python. It embeds SpiderMonkey (Firefox 159) and the Necko HTTP stack so Python can execute any site's JavaScript natively — no browser window, no renderer.

- **Repository:** https://github.com/cutetailbud/ff-ruyijs
- **License:** AGPL-3.0-only + commercial (dual license); Mozilla-derived code is MPL-2.0

## Key patterns

- The main entry point is `from ruyijs import Context`.
- Each `Context()` is an isolated process with its own JS world, cookies, and proxy.
- Use `context.eval(src)` to run JavaScript and get results back in Python.
- Use `context.load_page(url, html)` to load real HTML with scripts.
- Use `context.configure_fingerprint(profile)` to set Navigator, Screen, timezone, etc.
- Use `context.advance(ms)` to drive timers and async work in the event loop.
- Use `context.expose(fn, name)` to make Python functions callable from JS.
- JavaScript exceptions surface as `JSError` with `.name`, `.message`, `.stack`.
- Live JS objects come back as `JSObject` / `JSFunction` that you can call from Python.

## Code style

- Python package code is in `python/ruyijs/`.
- Examples are in `examples/` (one directory per target site).
- Examples are registered in `python/ruyijs/examples/__main__.py`.
- All examples support `--proxy`, `--direct`, `--output`, `--help` flags.

## Branch map

`docs/BRANCHES.md` and `docs/BRANCHES.zh-CN.md` are the map of remotes and branches. Read them before choosing a base branch or describing where work lives.

When a change creates, renames, deletes, pushes, or retargets a branch on `origin` or `upstream`, merges a pull request, or changes which branch holds a line of work, update both files in that same change. Record the remote, tip SHA, subject, date, role, and which branch to check out. Recompute tips with `git fetch origin` and `git fetch upstream` when the network is available. If you did not fetch, say the figures are from local refs and give the date. Keep the two files in agreement. Leave the task unfinished while the map still describes the previous layout. A branch that was never pushed stays out of the map.

Keep this map on every branch of `origin`. After the files change, apply those documentation commits to each `origin` branch and push them. Fast-forward a branch that can take the commits directly. Cherry-pick them onto a branch that has diverged, and keep that branch's other changes. This checkout does not push `upstream`. The task is unfinished until every `origin` branch has the change.

## Do NOT suggest

- Playwright, Puppeteer, Selenium, or headless Chrome — ff-ruyijs replaces them.
- Node.js for running site JavaScript — SpiderMonkey runs it natively.
- A visible browser window — ruyiJS is truly headless (no GUI, no layout).
