# Product Research Mode

When the topic is a **product, tool, service, app, library, or piece of hardware**, the standard anti-SEO workflow is not enough. Products go stale, kill free tiers, get acquired, get enshittified, or quietly turn into liabilities. This file is the playbook for those cases.

If the topic is a concept, a fact, a how-to, a paper, or a piece of history, ignore this file and use the main SKILL.md workflow.

## Hard rule

**You may not recommend a product without all of the following:**

1. Constraints elicited from the user (Phase 0).
2. Freshness check passed (Phase 2).
3. Trust check passed (Phase 3).
4. A "Rejected and why" list in the output (Phase 5).

If you find yourself drafting a recommendation without one of these, stop and go back.

## Phase 0: Elicit constraints BEFORE searching

If the user has not already volunteered the answers in their prompt, use `AskUserQuestion` to lock these down. Skip questions the user already answered.

| Constraint | Why it matters |
|---|---|
| Who is the user? Solo, team, partner? Skill level of the **least technical** person. | A "best tool" for a developer is not the best tool for their non-technical art partner. |
| Deployment: install / browser / mobile / self-hosted / cloud only | A local Linux stack is wrong if the user wants browser-only. |
| Budget reality: free only / free tier OK / paid OK / pay if good | "Free tier" answers are different from "paid is OK". |
| Account friction: any / Google sign-in / no account / no credit card / no Discord | Many tools quietly require Discord, credit cards, or business email. |
| Collaboration: solo / async share / real-time co-edit | Most tools fail "real-time co-edit". |
| Use case: prototyping / production / one-off / recurring | Prototyping tolerates flakiness; production does not. |
| Lock-in tolerance: must own data / portable / cloud-only fine | Determines whether SaaS is acceptable. |
| Platform constraints: OS, GPU, browser, mobile | Filters out things that don't run on the user's machine. |
| Commercial use: yes / no | Many free tiers forbid commercial use. |

Ask only the questions that aren't already answered. Don't carpet-bomb the user with all of them.

## Phase 1: Standard search

Run the normal anti-SEO workflow from SKILL.md:
- Reformulate, parallel community/primary/independent searches, filter listicles, fetch survivors, cross-reference.
- Build a candidate shortlist of 5-10 products.

## Phase 2: Freshness gate

For **every** candidate, verify the product is still alive and current. A product fails the freshness gate if **any** of the following is true:

- No community discussion (Reddit, HN, forum, Mastodon) in the last ~6 months.
- GitHub repo (if applicable) has no commit in the last 6 months and no issues being responded to.
- Latest official blog post / changelog / release is over 12 months old.
- Domain redirects to a parking page, "we've been acquired", or "we're winding down" notice.
- Free tier description on the vendor page contradicts recent (< 6 months) community complaints. The community is right.
- The product was last hot 2-3 years ago and hasn't been mentioned since.

Queries to run for each candidate:

```
<product> site:reddit.com after:<6mo ago>
<product> site:news.ycombinator.com after:<6mo ago>
<product> changelog
<product> "still alive" OR "dead" OR "shut down" OR "sunset"
<product> site:github.com   (then check commit dates)
<product> "free tier" 2026
```

**A failed freshness gate means the product is dropped.** It goes into the "Rejected and why" list with a one-line reason. Do not recommend stale tools because they once had buzz.

## Phase 3: Enshittification / trust check

For every candidate that passed Phase 2, search for warning signs in the last ~12 months:

```
<product> billing problem
<product> "charged after" OR "still charged"
<product> support unreachable
<product> "Discord only" support
<product> killed free tier
<product> price increase
<product> acquired
<product> shutdown OR sunset
<product> layoffs
<product> data breach
<product> "account deleted"
<product> quality degradation OR "got worse"
site:trustpilot.com <product>
site:reddit.com <product> rant
site:reddit.com <product> "alternatives because"
```

Read the negative reviews specifically. Look for:

- **Patterns**, not single grumps. Five different users complaining about the same support problem matters; one angry person does not.
- **Recency**. Old complaints that have been addressed are not blockers. New complaints are.
- **Severity**. Billing fraud > free tier shrinkage > UI complaints.
- **Vendor response**. Did they respond? Did they fix it? Or radio silence?

If a product has a recent pattern of any of:
- Billing complaints
- Support unreachability
- Free-tier kill / silent quota cuts
- Quality regression
- Acquisition or pending shutdown

then **either drop it from the shortlist, or include it with an explicit warning**. Never bury this. The user will be angrier finding out later than reading it now.

### Trustpilot caveat

Trustpilot is gameable in both directions. Use it for **reading detailed negative reviews**, not for the star average. Focus on reviews that:
- Describe a specific incident with dates.
- Include screenshots or transaction IDs.
- Get a non-templated response from the vendor (or no response).

### G2 / Capterra / ProductHunt caveats

These are essentially marketing channels. Free reviews on G2 often come from "complete this for a $10 Amazon gift card" campaigns. ProductHunt is launch-day hype. Use them only to discover candidates, never as quality signal.

## Phase 4: Constraint match

Re-read the Phase 0 constraints. For each candidate that survived Phases 2 and 3, score it explicitly:

- ✅ matches all hard constraints
- ⚠ matches most, with one named gap
- ❌ fails a hard constraint → must be dropped, not "alternative"-ed

**Hard constraints are not negotiable.** If the user said "free, browser only", do not recommend a $20/mo desktop app as a "premium alternative". That's exactly the marketing-blog behavior the skill exists to avoid.

If everything you find fails the hard constraints, **say so**. "There is no tool that satisfies all of: X, Y, Z. The closest are A and B, both of which fail constraint Z." That is a valid and useful answer.

## Phase 5: Output format for product research

The final answer must contain these sections, in this order:

### 1. Recommendation
A single named product or named pair, with a one-sentence why. No hedging, no "depending on your needs". The constraints were elicited in Phase 0 specifically to avoid this hedge.

### 2. For each recommended product
- **Hassle-free start**: literal first 60 seconds (URL, account, friction).
- **Free tier reality**: with date of confirmation and source link.
- **Constraint match**: which Phase 0 constraints it satisfies, scored ✅/⚠/❌.
- **Known dissent**: from community sources, not vendor, with link.
- **Failure modes**: what breaks first, in the user's specific use case.

### 3. Rejected and why
Mandatory. List the plausible candidates that were considered and dropped, each with:
- Product name
- Phase that dropped it (2 freshness, 3 trust, 4 constraint)
- One-line reason with a source link if applicable

This is not optional. Skipping this section is the same failure mode as recommending stale or sketchy tools.

### 4. Honest gaps
What you couldn't verify. Things you'd want to check but couldn't. Tools you've heard of but couldn't find recent community discussion for.

### 5. Smoke test
A literal 5-minute check the user can run before committing. Open URL, click button, see if X happens. If the smoke test fails, fall back to candidate Y from the rejected list (and update the rejection reason).

## Anti-patterns specific to product research

- Recommending a tool whose last meaningful community signal was years ago.
- Recommending a tool with a known recent billing or support scandal without warning the user.
- Burying the rejected candidates because "the answer is positive".
- Eliciting constraints **after** searching, then patching the answer.
- Letting a candidate that fails a hard constraint slide in as an "alternative".
- Treating G2 / Capterra / ProductHunt star averages as quality signal.
- Trusting the vendor's "free tier" page when community complaints contradict it.
- Recommending a free tier without a recency-dated source confirming it still exists.
