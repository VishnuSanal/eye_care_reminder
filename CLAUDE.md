# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Run locally (uses the checked-in `.venv`):
```
.venv/bin/python main.py
```

Build a single-file binary with PyInstaller (matches what CI produces):
```
.venv/bin/pyinstaller --clean -y --onefile main.py
```
Output goes to `dist/main`. `main.spec` is the saved spec from a prior build; `--onefile` regenerates it.

There are no tests or linters configured.

## Architecture

Single-file PyQt6 app (`main.py`). The whole program is a 20/20/20 break reminder: every `DELAY_SECS` (1200s) it pops up a modal `QDialog` for `DURATION_SECS` (20s), then sleeps and repeats.

Two non-obvious design points worth preserving:

- **The reminder loop in `start_app()` is a plain `while True: show_popup(); time.sleep(...)`**, not a `QTimer` on the `QApplication` event loop. Each popup runs its own nested event loop via `popup.exec()` (modal), which is what makes the blocking `time.sleep` between popups acceptable. `QApplication` is created in `__main__` but its `app.exec()` is unreachable — the while-loop never exits. Don't "fix" this by moving to a top-level QTimer without verifying the popup-close semantics still work.
- **The popup cannot be dismissed early.** `PopupWindow.closeEvent` ignores the event while its internal `QTimer` is still running; only when the 20s progress bar completes does `update_progress` stop the timer and call `self.close()`. The window also uses `FramelessWindowHint | WindowStaysOnTopHint` so there's no titlebar X. This is intentional (see commit `d14eb17 disable closing`) — preserve this behavior.

Also note: `__main__` does `time.sleep(DELAY_SECS)` *before* the first popup, so the app is silent for 20 minutes after launch. This matters when testing — temporarily lower `DELAY_SECS`/`DURATION_SECS` (commented constants are at the top of `main.py`) rather than waiting.

## Distribution

Users don't run from source. CI (`.github/workflows/build_release.yml`) builds onefile binaries for Linux/Windows/macOS on every push to `main` and uploads them as workflow artifacts. `install.sh` expects the Linux binary at `~/bin/eye_care_reminder` and registers it as a systemd user service running under `graphical.target` with `DISPLAY=:0`.
