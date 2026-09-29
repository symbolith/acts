# Spam / Low-Trust Domain Patterns

Not a hard blocklist. Use as red flags. A site matching these patterns can still be useful, but should never be the **only** source for a claim.

## Structural red flags in any domain

- URL contains: `best`, `top10`, `review`, `guide`, `hub`, `wiki` (when not actually wiki software), `compare`, `picks`
- Domain registered in the last 12 months for a "review" site
- No author bios, or bios that are obviously generic ("John is a tech enthusiast who loves gadgets")
- Identical article structure across unrelated topics
- "Last updated 2026" but no actual change history
- Affiliate links on every recommendation, no exceptions
- "Disclosure: we may earn a commission" but no editorial separation
- Pop-up newsletter on first scroll
- Comments disabled or non-existent

## Categories to be skeptical of

### "Best of" content farms
Sites whose entire business model is ranking for "best <product>" queries. Even when they include real testing, the incentive structure pushes toward whatever pays the highest commission.

### Vendor-adjacent "comparison" sites
Sites like `<vendor> vs <competitor>` pages hosted by one of the vendors. Always biased.

### AI-generated content farms
Tells:
- Suspiciously uniform paragraph length
- Generic intro paragraph that could apply to any topic
- No specific anecdotes, no measurements, no images of the product in use
- Headings that exactly match the search query
- Conclusions that hedge on every recommendation
- Author photo is a stock image or AI-generated face

### "Top X in 2026" listicles
Particularly when:
- The same products appear in the same order across multiple sites
- The "ranking" criteria is vague
- The "we tested" claim has no methodology section
- Prices/specs are generic and don't match current vendor pages

### SEO-bait Q&A sites
Sites that scrape Quora/Stack Exchange answers and re-publish them with ads. The original is always better.

### "Press release as news" sites
Tech "news" sites that republish vendor press releases verbatim with minimal editing. Useful for knowing what was announced, useless for evaluating it.

### Product-comparison spam (product research specific)
Sites that exist purely to rank for "<Product A> vs <Product B>" queries. Tells:
- The "comparison" is a feature checklist, not actual usage.
- Both products are "great choices for different needs" — the universal cop-out.
- The "winner" coincidentally has the highest affiliate commission.
- Identical structure across many vs-pages.
- Hosted by an "AI tool directory" or "SaaS comparison" site that covers everything.

### Star-rating aggregators (G2, Capterra, TrustRadius, Software Advice)
Useful **only** for discovering candidate products, not for quality signal:
- Many reviews are "complete this for a $10 Amazon gift card" submissions.
- Vendors actively manage their listings and bury bad reviews.
- Star averages are essentially marketing.
- The detailed text of negative reviews can still be useful when read individually.

### ProductHunt
Launch-day hype. Upvotes are not adoption. A product can hit #1 of the day and be dead in six months. Use only to discover candidates, never as a quality signal.

### Trustpilot
Gameable in both directions. Read individual detailed negative reviews; ignore the star average. Vendors with templated responses to every complaint are a yellow flag.

### "AI tools directory" sites
Sites listing thousands of AI tools with one-paragraph descriptions and signup links. Pure affiliate plays. Useful only as a discovery surface.

## Specific red-flag patterns (not exhaustive)

These are illustrative, not a blacklist. Context matters.

- Domains ending in `-reviews.com`, `-hub.io`, `-guide.net`
- Sites that rank #1 for hundreds of unrelated "best X" queries
- Subdomains of marketing companies (`blog.<seo-agency>.com`)
- "10 best…" articles on general-interest publications that don't normally cover the topic
- Medium/Substack posts whose only outbound links are affiliate

## When a low-trust source is still useful

- Specs and feature lists (verifiable against the vendor's own page)
- Discovering candidate products you didn't know existed (then research them properly)
- Historical pricing snapshots
- Date a product was released

Never use them for: "is this actually good", "should I buy this", "what do users think long-term".

## How to fact-check a suspicious source

1. Open the same page in `web.archive.org` and check if it's been silently updated
2. Search the exact phrases from the review on Google in quotes — duplicated content across sites is a strong AI-content signal
3. Look up the author on LinkedIn / their personal site
4. Check if the "we tested" photos are stock images (reverse image search)
5. See if the recommended product has a referral code in the link
