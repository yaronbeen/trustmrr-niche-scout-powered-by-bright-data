# TrustMRR Live Check | Powered by Bright Data

Checked 2026-11-09 with Bright Data MCP `scrape_as_markdown`.

## What worked

- `https://trustmrr.com/` returned public Markdown with marketplace cards and actual `/startup/<slug>` link targets.
- `/acquire`, `/stats`, and a selected `/startup/<slug>` page were also retrieved during source validation.
- The home capture reported 106,429 characters and returned the first 40,000. Recently listed cards and many detail links were visible before the cut.

## Sanitized observation

The home page displayed Sportii App in Community with revenue `$971`, price `$53k`, and multiple `4.5x`. It displayed Nex File: File Manager in Productivity with revenue `$83`, price `$2.5k`, and multiple `2.5x`.

The card label was `Revenue`, not enough by itself to assume a monthly period. The sanitized fixture therefore uses `revenue_period=unknown`, and the helper must not calculate its own annual multiple from that card alone.

## Limits

- Truncation means the capture is not a complete directory inventory.
- TrustMRR's displayed verification language remains a source claim. This repo does not independently verify revenue.
- Source terms and permitted use must be reviewed before collection. No login or restricted area is used.
