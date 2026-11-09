# TrustMRR Niche Scout | Powered by Bright Data

> **Do not buy the niche story. Check the listings behind it.**

Turn public TrustMRR pages into a cited niche snapshot. Keep displayed revenue attached to its source and its stated period. Keep missing data missing. Walk away with a small sample you can defend, not a market fantasy.

## The decision

**Which category deserves a closer look?**

Use it to:

- Compare small category samples before choosing a niche to research.
- Inspect the company rows behind a category without mixing unknown-period revenue into MRR.
- Recheck the same captured companies for displayed-figure changes.

No acquisition shortlist. No founder profiling. No personal contact enrichment. No invented “verified by me” revenue claims.

## Why Bright Data

A directory is only useful when your agent can turn pages into evidence rows. [Bright Data](https://docs.brightdata.com/products/mcp-server/overview) MCP brings public page-to-Markdown collection into the same workflow as the analysis. One connection. No one-off scraper project. Less plumbing, more time deciding what the displayed numbers actually mean.

## Start with 5,000 free credits

**New Bright Data accounts include 5,000 free credits per month. No credit card is required.** Credits share one account-level pool, reset monthly, and are subject to current eligibility and product terms.

The default plan uses **14 public-page requests**, with at most **2 retries**. Your agent shows the exact plan before collection. The free allowance is not a promise of unlimited access or successful retrieval.

## What you get

- `report.md`: category samples and company-level evidence rows.
- `companies.csv`: stable `slug` keys for Sheets or your own niche-research queue.
- `categories.csv`: sortable sample counts, missing-MRR counts, averages, and medians for category comparison.
- `run.json`: the current snapshot to pass back next week for new, changed, and unchanged rows.
- Clear `unknown` values, average and median explicit MRR, and a no-ranking rule below three captured companies.

Rows that disappear from a later input are not labeled as removed or delisted; the diff covers rows present in the current capture.

## Give this to your agent

```text
Use trustmrr-niche-scout for niche validation in [category].

Use Bright Data MCP to fetch https://trustmrr.com/ and
https://trustmrr.com/acquire, then at most 12 discovered public startup pages.
Show me the 14-request plan first. Retry a failed page at most once, with at most
2 retries overall. Do not infer missing revenue periods or independently verify
TrustMRR's claims. Exclude founder names and personal contacts.

Normalize the evidence to this skill's schema and run scripts/report.py.
Return the category caveats, company evidence rows, categories.csv comparison, and output paths.
Do not turn this into a lead list, contact anyone, or buy anything.
```

## Install

Requires Python 3.10+ and an MCP-compatible agent. This is a public repo.

### 1. Connect Bright Data MCP

Follow [Install Bright Data MCP](docs/install-bright-data-mcp.md). Choose hosted or local setup, then verify `search_engine` and `scrape_as_markdown` are connected as `brightdata`.

### 2. Clone the skill

```bash
git clone https://github.com/yaronbeen/trustmrr-niche-scout-powered-by-bright-data.git \
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

| Company | Category | Displayed revenue | Period | Annual multiple | Status |
|---|---|---:|---|---:|---|
| Acme Analytics | SEO | 4000.0 | monthly | 1.5 | new |
| Beta Keywords | SEO | 2500.0 | monthly | 1.5 | new |
| Coda Content | SEO | 1500.0 | monthly | unknown | new |
| Delta Forms | Sales | 3000.0 | unknown | unknown | new |
| Ember CRM | Sales | unknown | unknown | unknown | new |

| Category | n | Missing MRR | Average explicit MRR | Median explicit MRR | Rankable |
|---|---:|---:|---:|---:|---|
| SEO | 3 | 0 | 2666.67 | 2500.0 | True |
| Sales | 2 | 2 | unknown | unknown | False |

A displayed multiple stays a displayed multiple. The helper calculates its own annual multiple only when price, positive revenue, and an explicit monthly period are all present. Unknown-period revenue never enters the MRR average or median. Use the median alongside the average so one large listing does not dominate the comparison.

## Tests

This repo was built test-first. The first commit contains the tests before the implementation.

```bash
python3 -m unittest discover -s tests -v
```

Tests cover money parsing, unknown periods, dedupe, personal-field removal, small-sample suppression, category averages and medians, `categories.csv`, MCP installation docs, CSV formula injection, deterministic diffs, and a sanitized live capture. See [the testing note](docs/testing.md).

## What this is not

- Not a market census. Leaderboard and marketplace samples have selection and survivorship bias.
- Not independent revenue verification. TrustMRR remains the source of its claims.
- Not a valuation or purchase recommendation.
- Not an outreach machine. It never sends messages, submits forms, or enriches people.
- Not permission to ignore TrustMRR's current terms. Review them before collection.

## Repo map

```text
SKILL.md                 Agent workflow and MCP limits
scripts/report.py        Stdlib-only deterministic helper
tests/                   Unit tests + sanitized live fixture
examples/                Synthetic input and generated output
docs/                    Setup, schema, testing, and live-check notes
```

## FAQ

**Can I use the CSV as a lead list?**  No. This repo is for niche research, not prospecting or acquisition screening. The key is `slug`; personal contacts and buying-intent claims are deliberately excluded.

**Does it filter companies by my MRR band?**  No. The helper reports the normalized sample and category summaries. Any additional filtering is a separate, explicit human or spreadsheet step.

**What if only two companies match a category?**  You get context, not a category ranking. Two data points are not a trend.

**What if a page fails?**  Record the failure and mark its fields unknown. Do not backfill from memory or snippets.

---

Independent project by Yaron Been. MIT licensed. Powered by Bright Data; no affiliation or endorsement is implied.
