# Screenshot shot list - post-2.1.2 docs refresh

Supersedes the stale `MISSING-IMAGES.md` / `v202-images.md` notes. Reflects the
docs as they stand after the 2.1.2 content rewrite (main guide + Tailscale +
landing). Capture spec unchanged: **iPhone native portrait** (per the old note,
iPhone 16 Pro, 1179x2556), then frame with the framing script and drop into
`images/<name>` - the pages hide any missing image gracefully, so nothing
breaks while these are pending.

Priority key: P1 = shows the wrong/old UI (misleading), P2 = missing file, P3 =
nice-to-have for a new section.

## A. Re-shoots - the current image shows OLD UI (P1)

| File (current) | Section | Old shot shows | Re-shoot to show |
|---|---|---|---|
| `v2-host-list.png.png` | §3 / landing area | the retired **Hosts tab** | the **Sessions tab** with a host expanded to its sessions. (Also rename to `v2-sessions-list.png` - the doubled `.png.png` is ugly; if you rename, tell me and I'll update the `<img>` src.) |
| `v2-themes.png` | §18 Color modes | the old **8-theme** picker (Solarized/Gruvbox/…) | the **Color Mode** picker: True Color + Green/Blue/Red Phosphor + Monochrome, ideally with the live preview tile. |
| `v2-edit-host.png` | §4 Managing hosts | older Edit Host | Edit Host for an **mtRoam host**, scrolled to show the **Persistence (Halo)** section with the **"What is mtRoam (Halo)?"** link and the **Port Forwarding** section. |
| `v2-install-roam.PNG` | §6 Installing the daemon | "Set Up Roam" older copy | the current **"What is mtRoam (Halo)?"** explainer sheet (now includes the Halo ring-buffer section) OR the install sheet with current "Set Up mtRoam" copy. |

## B. Missing files (referenced by the HTML, not in images/) (P2)

| File | Section | What to capture |
|---|---|---|
| `v2-predictions.png` | §11 Predictions & history | An active session at a shell prompt; type `git st` so the chip strip above the keyboard shows history matches (`git status`, `git stash`, …). Seed `~/.bash_history` first. |
| `v2-tailscale-settings.png` | §9 Tailscale | **Settings → Connections → Tailscale**: the profiles list with one connected (green status / tailnet IP), showing the embedded-Tailscale + profiles story. |
| `v202-tailscale-signin.png` | Tailscale page, Part 1 | The **Sign in with Tailscale** flow - the profile-creation screen with the sign-in button, or the in-app browser sheet mid-sign-in. |
| `v202-tailnet-browser-connected.png` | Tailscale page, Part 2 | The Tailnet device browser **connected with no API token**: "Connected · \<profile\>" + device list with online/offline dots. Take it on a profile with no token saved, to prove the point. |

## C. New sections with no screenshot yet (P3 - optional)

These sections are currently text-only. If you want shots, I'll add the
`<figure><img>` placeholders (they hide until the file lands):

| Suggested file | Section | What to capture |
|---|---|---|
| `v2-tunnels.png` | §10 Port forwarding / Tunnels | The **Tunnels** screen with a couple of rules and their live status (Listening / a web forward you can tap). |
| `v2-icloud-sync.png` | §20 iCloud Sync | **Settings → iCloud Sync** with the master toggle on and the per-item toggles visible. |
| `v2-halo-explainer.png` | §6 Roam / Halo | The explainer sheet scrolled to the **"Halo, the persistent ring buffer"** section. |

## Notes

- `v2-keyboard-modes.png` (§10 Keyboard) is a wide side-by-side composite the
  framing script can't frame; two single-mode shots already exist unreferenced
  (`v2-keyboard-second.PNG`, `v2-keyboard-minimal.PNG`). Optional: swap the
  composite for framed singles.
- Everything else (SSH keys, snippet vault, macros, SFTP, scrollback search,
  settings overview, add-host, roam sessions) still matches the current UI - no
  re-shoot needed.
- Hand me the raw shots and I'll frame + commit them, or drop framed files into
  `images/` under the names above and push.
