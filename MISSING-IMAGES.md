# Missing / pending screenshots — meshTerm docs (v2.0)

Status as of the v2.0 docs rewrite. "Missing" = referenced by the HTML but
the file is not in `images/`. These render as a graceful placeholder box
(the `onerror` handler hides the broken `<img>`), so the pages don't break —
but the screenshot is absent.

All capture screenshots at **iPhone 16 Pro native, 1179×2556 portrait** so
the framing script (`~/scripts/iphone-frame-v2.py`) aligns. Drop the raw
screenshot into `images/<name>` and re-run the framer (see README/workflow),
or hand me the raw shots and I'll frame + commit them.

## 1. Genuinely missing (referenced, file absent)

| File | Used in | What to capture |
|------|---------|-----------------|
| `images/v2-predictions.png` | §11 Predictions & history | Active Roam session to `demo` at a shell prompt. Type just `git st`; the chip strip above the keyboard should show history matches (`git status`, `git stash`, …). Seed `~/.bash_history` on the host with a few git commands first. |
| `images/v2-tailscale-settings.png` | §9 Tailscale → Tailscale SSH | The **Settings → Connections → Tailscale** screen: the profiles list with one connected (green status / tailnet IP visible), so the embedded-Tailscale + profiles story is shown. |

## 2. Present but worth revisiting

| File | Note |
|------|------|
| `images/v2-keyboard-modes.png` | Exists, but it's a **3577×2556 side-by-side composite** of three modes — the framing script can't frame it (it expects a single 1179×2556 shot). Two single-mode portrait shots are already in `images/` but **unreferenced**: `v2-keyboard-second.PNG` and `v2-keyboard-minimal.PNG`. Option: replace the wide composite in §10 with these (framed) individual shots, or leave the composite as-is. |

## 3. New v2.0 sections with no screenshot (optional)

The two sections added in this pass are text-only. Optional shots if you want them:

| Suggested file | Section | What to capture |
|----------------|---------|-----------------|
| `images/v2-roam-transport.png` | §6 Roam → "Choosing a transport" | **Edit Host → Transport Details** with the **mtRoam Transport** segmented control showing **Direct (QUIC/TCP)** / **SSH Tunnel**. |
| `images/v2-tailscale-profiles.png` | §9 Tailscale → "Multiple Tailscale profiles" | The Tailscale **Profiles** list with two profiles (e.g. "Work" / "Personal"), one connected. |

## Not used by v2.0 (no action)

The old `IMG_*.PNG` files (750×1624 / 828×1792) are the v1.1 screenshots. The
v2.0 pages don't reference them; they're wrong-size for the framer and can be
ignored (or deleted once `main` is on v2.0).
