#!/usr/bin/env python3
"""Turn normalized TrustMRR evidence into a cautious niche/account report."""
import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

PUBLIC_FIELDS = {"company", "slug", "category", "mrr", "displayed_revenue", "growth", "price", "revenue_period", "displayed_multiple", "source_url", "captured_at"}


def csv_cell(value):
    text = "" if value is None else str(value)
    return "'" + text if text.startswith(("=", "+", "-", "@", "\t", "\r")) else text


def parse_money(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"\s*[$€£]?\s*([\d,]+(?:\.\d+)?)\s*([kKmM]?)\s*", value)
    if not match:
        return None
    number = float(match.group(1).replace(",", ""))
    multiplier = {"": 1, "k": 1_000, "m": 1_000_000}[match.group(2).lower()]
    return number * multiplier


def annual_multiple(price, mrr, period):
    price_value, mrr_value = parse_money(price), parse_money(mrr)
    if period != "monthly" or not price_value or not mrr_value or mrr_value <= 0:
        return None
    return round(price_value / (mrr_value * 12), 2)


def public_record(record):
    return {k: v for k, v in record.items() if k in PUBLIC_FIELDS}


def normalize_records(records):
    deduped = {}
    for raw in records:
        row = public_record(raw)
        slug = str(row.get("slug", "")).strip().lower()
        if not slug:
            raise ValueError("Every TrustMRR row needs a slug")
        row["slug"] = slug
        displayed_revenue = parse_money(row.get("displayed_revenue") if row.get("displayed_revenue") is not None else row.get("mrr"))
        row["displayed_revenue"] = displayed_revenue
        row["mrr"] = displayed_revenue if row.get("revenue_period") == "monthly" else None
        row["price"] = parse_money(row.get("price"))
        row["annual_multiple"] = annual_multiple(row.get("price"), displayed_revenue, row.get("revenue_period"))
        deduped[slug] = row
    return [deduped[key] for key in sorted(deduped)]


def category_summary(rows):
    groups = defaultdict(list)
    for row in rows:
        groups[row.get("category") or "unknown"].append(row)
    result = []
    for category, members in groups.items():
        known = [r["mrr"] for r in members if r.get("mrr") is not None]
        result.append({
            "category": category,
            "sample_count": len(members),
            "missing_mrr": len(members) - len(known),
            "average_displayed_mrr": round(sum(known) / len(known), 2) if known else None,
            "rankable": len(members) >= 3,
        })
    return sorted(result, key=lambda r: r["category"])


def comparison_value(value):
    if isinstance(value, dict):
        return {k: comparison_value(v) for k, v in value.items() if k not in {"status", "captured_at"}}
    if isinstance(value, list):
        return [comparison_value(v) for v in value]
    return value


def apply_diff(rows, previous, key):
    old_rows = (previous or {}).get("rows", [])
    old = {r[key]: comparison_value(r) for r in old_rows if key in r}
    for row in rows:
        identity = row[key]
        row["status"] = "new" if identity not in old else ("unchanged" if old[identity] == comparison_value(row) else "changed")
    return rows


def md(value):
    return " ".join(str(value if value is not None else "").split()).replace("|", "\\|")


def render(result):
    lines = [
        "# TrustMRR Niche Scout | Powered by Bright Data", "",
        "This is a bounded, search-selected sample, not a market census. Metrics are displayed by TrustMRR and are not independently verified.", "",
        "| Company | Category | Displayed revenue | Period | Annual multiple | Status |", "|---|---|---:|---|---:|---|",
    ]
    for r in result["rows"]:
        lines.append(f"| {md(r.get('company', r['slug']))} | {md(r.get('category', 'unknown'))} | {r.get('displayed_revenue') if r.get('displayed_revenue') is not None else 'unknown'} | {md(r.get('revenue_period') or 'unknown')} | {r.get('annual_multiple') if r.get('annual_multiple') is not None else 'unknown'} | {r['status']} |")
    lines += ["", "## Category samples", "", "| Category | n | Missing MRR | Average explicit MRR | Rankable |", "|---|---:|---:|---:|---|"]
    for r in result["categories"]:
        average = r["average_displayed_mrr"] if r["average_displayed_mrr"] is not None else "unknown"
        lines.append(f"| {md(r['category'])} | {r['sample_count']} | {r['missing_mrr']} | {average} | {r['rankable']} |")
    lines += ["", "Categories with fewer than three captured companies are context, not rankings. Only explicit monthly revenue enters MRR summaries; unknown-period revenue stays displayed revenue. No personal contacts are included."]
    return "\n".join(lines) + "\n"


def analyze(payload, previous=None):
    rows = apply_diff(normalize_records(payload.get("rows", [])), previous, "slug")
    run_id = hashlib.sha256(json.dumps(comparison_value(rows), sort_keys=True).encode()).hexdigest()[:12]
    result = {"rows": rows, "categories": category_summary(rows), "snapshot": {"schema_version": 1, "run_id": run_id, "rows": rows}}
    result["report"] = render(result)
    return result


def write_outputs(result, output_dir):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.md").write_text(result["report"])
    (out / "run.json").write_text(json.dumps(result["snapshot"], indent=2, sort_keys=True) + "\n")
    fields = ["slug", "company", "category", "displayed_revenue", "revenue_period", "mrr", "growth", "price", "annual_multiple", "status", "source_url", "captured_at"]
    with (out / "companies.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in result["rows"]:
            writer.writerow({key: csv_cell(row.get(key)) for key in fields})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input")
    parser.add_argument("--previous", help="Prior run.json; omit on the first run")
    parser.add_argument("--output-dir", default="output")
    args = parser.parse_args()
    payload = json.loads(Path(args.input).read_text())
    previous = json.loads(Path(args.previous).read_text()) if args.previous else None
    write_outputs(analyze(payload, previous), args.output_dir)


if __name__ == "__main__":
    main()
