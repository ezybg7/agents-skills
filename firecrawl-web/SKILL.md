---
name: firecrawl-web
description: How to get clean web content when a research run needs more than WebSearch snippets or WebFetch can give — Firecrawl's REST API (search, scrape, map) called with curl, what each endpoint is for, the exact requests, and the limits. Use when a page is JS-rendered, blocks the fetcher, is a public PDF/DOCX, or when a query needs full page content rather than snippets; note explicitly when it is unavailable.
---

# Firecrawl for web evidence

**What it adds.** `WebFetch` fails on JS-rendered pages, bot-walled sites and documents;
`WebSearch` returns snippets only. Firecrawl renders the page and returns clean Markdown, and
its search can return full page content per result. Nothing is installed — it is plain HTTPS
with `curl` and `jq`.

It needs `FIRECRAWL_API_KEY` in your run's environment (audited custom env, like the Reddit
keys). Check once at the start:

```bash
[ -n "$FIRECRAWL_API_KEY" ] && echo firecrawl: ok || echo firecrawl: unavailable
```

If unavailable, say so in the report as a gap ("Firecrawl unavailable to this run") and
continue with WebSearch/WebFetch. **Never echo the key, never put it in a comment, a HANDOFF,
a file, or a URL** — it goes only in the `Authorization` header below.

Base: `https://api.firecrawl.dev/v2` · header `Authorization: Bearer $FIRECRAWL_API_KEY`.

## The requests

Keep one helper for the run:

```bash
fc() { curl -sS -X POST "https://api.firecrawl.dev/v2/$1" \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" -H 'Content-Type: application/json' -d "$2"; }
mkdir -p .firecrawl
```

**Search** — discovery; add `scrapeOptions` only when you need full content (costs more):

```bash
fc search '{"query":"pantry inventory app barcode scanning","limit":10}' \
  | jq -r '.data.web[] | "\(.title) — \(.url)"'
fc search '{"query":"USDA FoodData Central API rate limit","limit":5,
            "scrapeOptions":{"formats":["markdown"],"onlyMainContent":true}}' > .firecrawl/q1.json
```

**Scrape** — you have the URL (HTML pages and public PDF/DOCX alike):

```bash
fc scrape '{"url":"https://example.com/pricing","formats":["markdown"],"onlyMainContent":true}' \
  | jq -r '.data.markdown' > .firecrawl/example-pricing.md
```

**Map** — list a site's URLs before choosing which to scrape:

```bash
fc map '{"url":"https://docs.example.com","search":"webhooks","limit":50}' | jq -r '.links[].url'
```

Save every page you cite under `.firecrawl/` and read it from the file — do not pipe whole
pages into your context. `head`/`grep` the file for the part you need.

## Use it well

- **Order:** search → pick URLs → scrape the few that matter. Do not scrape a whole result set.
- **Prefer the cheap path.** If `WebFetch` returns the page cleanly, use it; Firecrawl is for
  what the fetcher cannot read.
- **Respect sites that forbid it.** Reddit goes through `reddit-search`, not Firecrawl. Never
  use Firecrawl to get past a login, a paywall or a CAPTCHA.
- **Failures:** `401` → key missing/invalid (report as unavailable); `402` → credits exhausted
  (report it, stop calling); `429` → wait a minute, retry once; `success:false` → read `.error`
  and report it, do not guess the page's content.
- Not available here: crawl jobs, monitors, browser `interact` sessions — they are long-running
  or stateful; ask the orchestrator if a task truly needs one.

## Reporting

A claim goes under Findings only from a page you scraped or read; a search title or snippet
alone is Unverified. Cite the URL and the page's date (or the scrape date when it has none).
Say which queries you ran and how many pages you read, so the reader knows the sample.
