# TrustMRR Niche Scout | Powered by Bright Data

> **Do not buy the niche story. Check the listings behind it.**

Turn public TrustMRR pages into a cited niche snapshot, an acquisition watchlist, or a company-only research list. Keep the revenue figures attached to their source. Keep missing data missing. Walk away with a shortlist you can defend, not a market fantasy.

## The decision

**Which category, listing, or company deserves a closer look?**

Use it to:

- Compare small category samples before choosing a niche to research.
- Screen displayed price and MRR figures for acquisition follow-up.
- Build a company-only prospect research list that matches your category and MRR rules.

No founder profiling. No personal contact enrichment. No invented “verified by me” revenue claims.

## Why Bright Data

A directory is only useful when your agent can turn pages into evidence rows. [Bright Data](https://brightdata.com/) MCP brings public page-to-Markdown collection into the same workflow as the analysis. One connection. No one-off scraper project. Less plumbing, more time deciding what the displayed numbers actually mean.

## Start with 5,000 free credits

**New Bright Data accounts include 5,000 free credits per month. No credit card is required.** Credits share one account-level pool, reset monthly, and are subject to current eligibility and product terms.

The default plan uses **14 public-page requests**, with at most **2 retries**. Your agent shows the exact plan before collection. The free allowance is not a promise of unlimited access or successful retrieval.

## What you get

- `report.md`: category samples, company rows, and acquisition context.
- `companies.csv`: stable `slug` keys for Sheets, a CRM research stage, or your own review queue.
- `run.json`: the snapshot to pass back next week for new, changed, and unchanged rows.
- Clear `unknown` values, sample sizes, missing-MRR counts, and a no-ranking rule below three captured companies.

## Give this to your agent

```text
Use trustmrr-niche-scout for [niche validation / acquisition screening / company research].
My category filter is [category]. My displayed-MRR band is [minimum] to [maximum].
My optional company-fit rules are [rules].

Use Bright Data MCP to fetch https://trustmrr.com/ and
https://trustmrr.com/acquire, then at most 12 discovered public startup pages.
Show me the 14-request plan first. Retry a failed page at most once, with at most
2 retries overall. Do not infer missing revenue periods or independently verify
TrustMRR's claims. Exclude founder names and personal contacts.

Normalize the evidence to this skill's schema and run scripts/report.py.
Return the category caveats, the manual-review shortlist, and the output paths.
Do not contact anyone or buy anything.
```

## Install

Requires Python 3.10+, an agent with Bright Data MCP connected as `brightdata`, and access to this private repo.

```bash
git clone git@github.com:yaronbeen/trustmrr-niche-scout-powered-by-bright-data.git \
  ~/.claude/skills/trustmrr-niche-scout
```

For OpenCode, clone into `~/.config/opencode/skills/trustmrr-niche-scout` instead. See the [connection and schema guide](docs/technical-guide.md).

## Run the example

```bash
cd ~/.claude/skills/trustmrr-niche-scout
python3 scripts/report.py examples/input.json --output-dir examples/output
```

Next week, pass the old snapshot back:

```bash
python3 scripts/report.py new-input.json \
  --previous examples/output/run.json --output-dir output
```

The example is synthetic. The [live-check note](docs/live-check.md) records what MCP actually returned.

## Example output

| Company | Category | Displayed MRR | Annual multiple | Decision context |
|---|---|---:|---:|---|
| Acme Analytics | SEO | $4,000 | 1.50 | Manual review |
| Beta Forms | Sales | $2,500 | unknown | Revenue period unknown |

A displayed multiple stays a displayed multiple. The helper calculates its own annual multiple only when price, positive MRR, and a monthly revenue period are all explicit.

## Tests

This repo was built test-first. The first commit contains the tests before the implementation.

```bash
python3 -m unittest discover -s tests -v
```

Tests cover money parsing, unknown periods, dedupe, personal-field removal, small-sample suppression, CSV formula injection, deterministic diffs, output files, and a sanitized live capture. See [the testing note](docs/testing.md).

## What this is not

- Not a market census. Leaderboard and marketplace samples have selection and survivorship bias.
- Not independent revenue verification. TrustMRR remains the source of its claims.
- Not a valuation or purchase recommendation.
- Not an outreach machine. It never sends messages, submits forms, or enriches people.

## Repo map

```text
SKILL.md                 Agent workflow and MCP limits
scripts/report.py        Stdlib-only deterministic helper
tests/                   Unit tests + sanitized live fixture
examples/                Synthetic input and generated output
docs/                    Setup, schema, testing, and live-check notes
```

## FAQ

**Can I use the CSV as a lead list?**  Yes, as a company-level research list. The key is `slug`. It deliberately excludes personal contacts and does not claim buying intent.

**What if only two companies match a category?**  You get context, not a category ranking. Two data points are not a trend.

**What if a page fails?**  Record the failure and mark its fields unknown. Do not backfill from memory or snippets.

---

Built by Yaron Been. MIT licensed. Powered by Bright Data, without implying endorsement.
