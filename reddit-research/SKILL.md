---
name: reddit-research
description: How to get forum-scale evidence from Reddit when researching for Ambry — the `reddit-search` command (Reddit's official OAuth Data API; the web fetcher cannot reach reddit.com), what to search, how to cite a thread, and the limits. Use whenever a research question needs what real users praise or complain about, and note explicitly when it is unavailable.
---

# Reddit as a source

**Why the fetcher fails.** reddit.com disallows every bot in its robots.txt and returns 403 to
unknown user agents, so `WebFetch` is refused and `WebSearch` only shows snippets. The
sanctioned path is Reddit's Data API over OAuth. The mini has a small client for it on the
daemon's PATH: `reddit-search` (`/opt/homebrew/bin/reddit-search`, Python, no dependencies).
It needs `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` in your run's environment — the research
agents carry them as audited custom env. If the command says they are not set, say so in your
report as a gap ("Reddit unavailable to this run") and continue without it — never scrape the
HTML site, never guess what a thread said.

## The commands

```bash
reddit-search search "paprika recipe editor" --sub r/Cooking --limit 25 --sort top --time year
reddit-search search "pantry inventory app" --time all            # all of Reddit
reddit-search thread https://www.reddit.com/r/iosapps/comments/<id>/...   # post + top comments
reddit-search hot r/iosapps --limit 25
```

Output is Markdown: one line per post with subreddit, date, score, comment count and the
permalink; `thread` prints the post body and the top comments with author, date and score.

## How to use it well

- **Search several angles, then read the threads.** A search line is a lead; the evidence is
  in `thread`. Read at least the top ten comments before quoting a sentiment.
- **Cite the permalink and the date**, and quote no more than a sentence per comment. A
  comment's score is context, not proof; say how many people said the same thing.
- **Subreddits that matter for Ambry:** r/iosapps, r/apple, r/iOSProgramming (for developer
  patterns), r/Cooking, r/MealPrepSunday, r/EatCheapAndHealthy, r/ZeroWaste, r/Frugal, r/Cookpad,
  r/Paprika (and the app-specific ones: r/PaprikaApp, r/AnyList), r/HomeKit is not relevant.
- **Rate limit:** 100 requests per minute per app. `search` is one request; `thread` is one.
  The tool warns when fewer than five remain; if it reports 429, wait a minute.
- **What it cannot do:** private or quarantined subreddits, votes, posting, anything needing a
  user login (the token is app-only, read-only), and images.

## Reporting

Reddit evidence goes under Findings only when you read the thread; a search-result title alone
is Unverified. Say which subreddits you searched and how many threads you read, so the reader
knows the sample.
