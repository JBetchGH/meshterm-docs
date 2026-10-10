# SEO and indexing checklist (owner steps)

This file is excluded from the build (`exclude` in `_config.yml`), like the other internal notes. The site now ships
canonical links, absolute hreflang, Open Graph and Twitter tags, a `robots.txt` that points at the sitemap, and a sitemap
without the internal working pages. What is left needs the owner's Google account.

## 1. Verify the domain in Google Search Console

1. Open https://search.google.com/search-console and choose **Add property**.
2. Pick the **Domain** property type and enter `meshterm.com`. A Domain property covers `docs.meshterm.com`, `meshterm.com`,
   `www`, http and https in one place.
3. Google shows a `TXT` record (`google-site-verification=...`). Add it at the DNS host for meshterm.com as a TXT record on
   the root (`@`). Keep it there permanently, or verification lapses.
4. Wait for DNS to update (minutes to a few hours), then press **Verify**.

## 2. Submit the sitemap

1. In the property, open **Sitemaps**.
2. Enter `https://docs.meshterm.com/sitemap.xml` and **Submit**. Status should become "Success" and list 10 URLs
   (home, Spanish home, user guide, troubleshooting, Docker 101, Tailscale setup, privacy and EULA in English and Spanish).
3. It must not list `MISSING-IMAGES`, `SHOT-LIST` or `v202-images`. If it does, the exclude list did not deploy.

## 3. Request indexing for the key pages

In **URL inspection**, paste each URL, wait for "URL is not on Google" or the current status, and press **Request indexing**:

- `https://docs.meshterm.com/`
- `https://docs.meshterm.com/meshterm.html` (the user guide)
- `https://docs.meshterm.com/troubleshooting.html`
- `https://docs.meshterm.com/docker-101.html`

Use **Test live URL** first if you want to confirm Google can fetch the page (no `noindex`, canonical matches). There is a
daily quota for index requests, so these four are enough; the rest are found through the sitemap and internal links.

## 4. After it is live, check

- **Pages** report: the four pages above move to "Indexed" within days to a couple of weeks. "Discovered, currently not
  indexed" means Google has seen the URL and not yet decided; give it time and keep the pages linked from the home page.
- **URL inspection > Page indexing** shows the user-declared canonical and the Google-selected canonical. They should match.
- **Sitemaps** shows the last read date.
- Bing: import the property into **Bing Webmaster Tools** from Search Console, which also covers DuckDuckGo and others.

## Notes

- Spanish pages are linked with `hreflang` alternates (`en`, `es`, `x-default`). Troubleshooting and Docker 101 are English only
  for now; a Spanish twin would need `troubleshooting.es.html` and `docker-101.es.html` plus `alternates` in both front matters.
- A legacy GitHub Pages build means `Last modified` in the sitemap is the build time, not the edit time. That is normal.
- Quality matters more than tags: Google indexes pages it finds useful. The troubleshooting page matches what people search for
  (the exact error messages), so keep its headings in the app's wording.
