---
name: research-web
description: Research a topic on the web while bypassing SEO marketing slop, affiliate spam, and "best of 2026" listicles. Use when the user asks to "research", "find honest reviews", "compare options", "find real sources", "what do people actually use", "what tool should I use", "what's the best X", or any question where the default Google results would be dominated by marketing content. Includes a dedicated Product Research Mode that elicits user constraints, runs freshness and trust checks, and forbids recommending stale or enshittified products. Prefers community discussion (Reddit, HN, forums), primary sources (docs, papers, repos), and independent/nonprofit reviewers.
argument-hint: [topic to research]
allowed-tools: WebSearch, WebFetch, Bash, AskUserQuestion, TaskCreate, TaskUpdate
---

# Web Research (Anti-SEO)

Default web search is poisoned by SEO. The first page of "best free X" is almost always affiliate listicles, vendor blogs, and AI-generated comparison spam. This skill exists to **deliberately route around that** and find what real practitioners actually use and say.

## Is this product research?

If the topic is a **product, tool, service, app, library, or piece of hardware** the user might adopt, this is product research and you must follow [references/product-research.md](references/product-research.md). That file overrides defaults: it requires eliciting user constraints up front, freshness and trust gates on every candidate, and a mandatory "Rejected and why" section in the output.

If the topic is a concept, a fact, a how-to, a paper, history, or anything not adoptable, use the workflow below directly.

## Core Principles

1. **Never trust a single "best of" listicle.** Treat any page with "Top 10", "Best of 2026", or matching headings across competitors as marketing noise unless cross-referenced.
2. **Prefer humans talking to humans** over vendors talking at customers.
3. **Prefer primary sources** (official docs, source code, papers, datasheets) over secondary descriptions.
4. **Prefer independent/nonprofit reviewers** (Wirecutter, Consumer Reports, RTINGS, project maintainers, academics) over ad-supported blogs.
5. **Cross-reference at least 3 independent sources** before stating a recommendation as fact.
6. **Be transparent about source quality** in the final answer. Mark each citation with source type.
7. **Elicit constraints before searching** when the user is going to adopt something based on the answer. A correct answer to the wrong question wastes everyone's time.
8. **Recency matters.** A recommendation from 2023 about a fast-moving product is suspect. Always check the date of every source.

## Workflow

### 1. Reformulate the query

Before searching, rewrite the user's question into 2-4 search queries that target high-signal sources. Apply the techniques in [references/search-operators.md](references/search-operators.md).

Examples of reformulation:

| User asks | Don't search | Search instead |
|---|---|---|
| "best free image generator" | `best free AI image generator 2026` | `site:reddit.com what image generator do you actually use`, `site:news.ycombinator.com flux vs sdxl`, `image generator comparison site:github.com` |
| "good Rust HTTP client" | `best rust http client` | `site:reddit.com/r/rust http client recommendation`, `reqwest vs hyper site:news.ycombinator.com`, `site:lib.rs http client` |
| "best mechanical keyboard" | `best mechanical keyboard 2026` | `site:reddit.com/r/MechanicalKeyboards endgame`, `site:rtings.com mechanical keyboard`, daily driver thread |

### 2. Run searches in parallel

Issue **multiple WebSearch calls in a single message** targeting different source classes:

- **Community**: `site:reddit.com`, `site:news.ycombinator.com`, `site:lobste.rs`, `site:stackexchange.com`, niche forums
- **Primary**: `site:github.com`, official project docs, vendor docs (only the maker, not resellers)
- **Independent reviewers**: Wirecutter, Consumer Reports, RTINGS, Project Farm (YouTube), iFixit
- **Academic/technical**: `site:arxiv.org`, `scholar.google.com`, `site:*.edu`, `site:*.gov`
- **Reference**: `site:en.wikipedia.org` for neutral overviews and disambiguation

### 3. Filter the results

Before fetching anything, scan the search results and **discard**:

- Domains you've never heard of with "review", "best", "top", "guide", "hub" in the URL or title
- Pages whose title matches the "Top N <thing> in <year>" pattern
- AI-generated content farms (telltale signs: anodyne intro paragraph, identical structure across competitors, no author bio, no dates, no methodology)
- Vendor pages comparing themselves to competitors
- Affiliate-heavy domains (see [references/known-spam-domains.md](references/known-spam-domains.md))

**Keep**:

- Forum threads with substantial discussion (>10 comments, real usernames)
- Project READMEs, official docs, source code
- Single-author technical blogs from people with track records
- Academic papers and standards documents
- Independent test labs with documented methodology

### 4. Fetch and read the survivors

Use `WebFetch` on the filtered URLs. When fetching a Reddit/HN thread, ask for:
- The actual recommendations made (with vote counts if visible)
- Counterarguments and dissent
- Date of the discussion (stale recommendations are a trap)

When fetching docs/papers, ask for the specific facts you need, not a summary.

### 5. Cross-reference

A claim only graduates from "someone said" to "consensus" when **3+ independent sources** agree. Independence means: different authors, different domains, different incentives. Three affiliate blogs citing each other count as one source.

If sources disagree, **report the disagreement** instead of picking a winner.

### 6. Present results with source typing

In the final answer, tag every citation:

- `[primary]` official docs, source code, papers, standards
- `[community]` forum/Reddit/HN threads
- `[independent]` nonprofit or no-affiliate reviewers
- `[vendor]` the maker's own marketing (use sparingly, only for factual specs)
- `[secondary]` blogs/articles (note if affiliate-supported)

Lead with what the **community and primary sources** say. Only mention secondary/vendor content as supporting context. If you couldn't find good sources, say so explicitly rather than padding with marketing.

## When to ask for clarification

Use `AskUserQuestion` if:

- The topic is broad enough that "non-marketing" sources differ wildly by sub-niche (e.g. "best camera" — for video? stills? travel? studio?)
- You need to know whether the user wants commercial-use, open source, self-hosted, etc.
- Initial searches return mostly marketing and you need a steer toward a specific community
- The topic is a product the user will adopt — see Phase 0 in [references/product-research.md](references/product-research.md) for the checklist of constraints to lock down before searching

## Anti-patterns

- Citing a "Top 10" listicle as authoritative
- Quoting a vendor's own claim as evidence the product is good
- Padding the answer with results you didn't actually verify
- Treating Google's first page as the search universe
- Failing to mark which sources are affiliate-supported
- Calling something "the best" when sources disagree
- Recommending a product without checking it's still maintained
- Recommending a product without checking for recent billing/support/quality complaints
- Eliciting user constraints **after** producing an answer, then patching it
- Skipping the "Rejected and why" section in product research

## References

- [references/product-research.md](references/product-research.md) — **mandatory** workflow when the topic is a product/tool/service
- [references/search-operators.md](references/search-operators.md) — query construction cheatsheet
- [references/trusted-sources.md](references/trusted-sources.md) — domains and communities worth searching
- [references/known-spam-domains.md](references/known-spam-domains.md) — domains to filter out
