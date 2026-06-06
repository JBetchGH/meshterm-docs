# v2.0.2 docs-site screenshot requests

Placeholders are already wired into the pages — drop the files into
`images/` with these exact names and push; they appear automatically
(the placeholder box hides itself when the image loads).

## 1. `images/v202-tailscale-signin.png`
**Page:** Tailscale Setup → Part 1, after the sign-in steps.
**Shot:** the **Sign in with Tailscale** flow — either the profile-creation
screen with the "Sign in with Tailscale" button, or the in-app browser
sheet mid-sign-in (whichever reads better). Portrait iPhone.

## 2. `images/v202-tailnet-browser-connected.png`
**Page:** Tailscale Setup → Part 2 intro ("you don't need a token").
**Shot:** the Tailnet device browser **connected with no API key**:
the connection section showing "Connected · <profile>" with the
Disconnect button, plus the device list with online/offline dots.
Best taken on a profile that has NO API token saved, to prove the point.

## 3. `images/v2-tailnet-browser.png` (refresh of existing)
**Page:** User Guide §9 Tailscale (existing figure).
**Shot:** same device browser as #2 — the current image predates the
connection section and online dots. Overwriting the existing filename
updates the User Guide with no HTML change.

## Notes
- Existing convention: PNGs, portrait iPhone frames (scripts/iphone-frame-v2.py
  in the meshTerm repo frames raw screenshots).
- Screenshot mode (Settings → Developer) seeds mock devices if you'd
  rather not show your real tailnet — though mocks currently render
  without online dots (REST-shaped), so a real-tailnet shot with
  hostnames you don't mind showing is the better demo of #2.
