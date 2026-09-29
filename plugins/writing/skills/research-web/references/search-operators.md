# Search Operators Cheatsheet

Construct queries that route around SEO content.

## Core operators

| Operator | Effect | Example |
|---|---|---|
| `site:domain.com` | Restrict to one domain | `site:reddit.com flux vs sdxl` |
| `-term` | Exclude a term | `image generator -best -top -2026` |
| `"phrase"` | Exact phrase match | `"i actually use" image generator` |
| `intitle:word` | Word must be in title | `intitle:comparison rust http` |
| `inurl:word` | Word must be in URL | `inurl:wiki installation art` |
| `OR` | Either term | `site:reddit.com OR site:lobste.rs` |
| `before:YYYY-MM-DD` | Date filter | `claude code skills before:2026-04-01` |
| `after:YYYY-MM-DD` | Date filter | `flux model after:2025-06-01` |
| `filetype:pdf` | Specific filetype | `installation art filetype:pdf site:*.edu` |

## High-signal source restrictions

```
site:reddit.com
site:news.ycombinator.com
site:lobste.rs
site:lemmy.world
site:stackexchange.com
site:stackoverflow.com
site:github.com
site:gitlab.com
site:lib.rs
site:crates.io
site:pypi.org
site:arxiv.org
site:scholar.google.com
site:en.wikipedia.org
site:*.edu
site:*.gov
site:archive.org
```

## Phrase patterns that find real users

These phrases are common in honest discussion and rare in marketing copy:

- `"what do you actually use"`
- `"i ended up using"`
- `"don't bother with"`
- `"after a year of"`
- `"daily driver"`
- `"changed my mind about"`
- `"endgame"` (hobby gear contexts)
- `"unpopular opinion"`
- `"hot take"`
- `"things i wish i knew"`
- `"lessons learned"`
- `"postmortem"`

## Anti-marketing exclusions

Append these to filter out listicle spam:

```
-best -top -ultimate -guide -review -2025 -2026 -"how to choose"
```

## Year disambiguation

When the topic is fast-moving, append the current year **inside** community sites only:

```
site:reddit.com flux 2026
```

Avoid bare `2026` in open searches — that's exactly what listicle SEO targets.

## Reddit deep search

Reddit's own search is bad. Use Google instead:

```
site:reddit.com/r/<subreddit> <topic>
site:old.reddit.com <topic>   # often returns cleaner threads
```

For multi-sub: `(site:reddit.com/r/MachineLearning OR site:reddit.com/r/StableDiffusion) flux quality`

## Hacker News deep search

```
site:news.ycombinator.com <topic>
```

Or use HN's own search (Algolia) via WebFetch:
```
https://hn.algolia.com/?q=<topic>&sort=byPopularity
```

## GitHub as a search engine

GitHub code search reveals what people actually import/use:

```
https://github.com/search?q=<term>&type=code
https://github.com/search?q=<term>&type=discussions
https://github.com/search?q=<term>&type=issues
```

The number of real repos using a tool is a stronger signal than any blog post.

## Wayback Machine

For dead links or to see a page before it was SEO-optimized:

```
https://web.archive.org/web/*/<url>
```

## Specialized search engines (when WebSearch fails)

If results are still mostly marketing, suggest the user try:

- **Kagi** — paid, has "Lenses" that filter to forums/blogs/academic
- **Marginalia Search** — `https://search.marginalia.nu/` — favors small independent sites
- **Wiby** — `https://wiby.me/` — old-school personal websites
- **Mwmbl** — `https://mwmbl.org/` — crowdsourced, ad-free
- **Searx/SearXNG** instances — meta-search with no tracking
