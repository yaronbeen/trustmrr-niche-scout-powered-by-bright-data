import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
from report import analyze, annual_multiple, category_summary, csv_cell, normalize_records, parse_money, write_outputs


class TrustMRRTests(unittest.TestCase):
    def test_money_parser_is_explicit_about_unknowns(self):
        self.assertEqual(parse_money("$12.5k"), 12500.0)
        self.assertEqual(parse_money("$1.2M"), 1200000.0)
        self.assertEqual(parse_money("€1,200"), 1200.0)
        self.assertEqual(parse_money(42), 42.0)
        self.assertIsNone(parse_money("not disclosed"))
        self.assertIsNone(parse_money(None))

    def test_multiple_requires_positive_monthly_revenue(self):
        self.assertEqual(annual_multiple("$120k", "$10k", "monthly"), 1.0)
        self.assertIsNone(annual_multiple("$120k", "$10k", "annual"))
        self.assertIsNone(annual_multiple("$120k", 0, "monthly"))
        self.assertIsNone(annual_multiple(None, "$10k", "monthly"))

    def test_categories_below_three_are_not_rankable(self):
        rows = [{"category": "SEO", "mrr": n, "growth": None} for n in (100, 200)]
        rows += [{"category": "Sales", "mrr": n, "growth": None} for n in (100, 200, None)]
        summary = {r["category"]: r for r in category_summary(rows)}
        self.assertFalse(summary["SEO"]["rankable"])
        self.assertTrue(summary["Sales"]["rankable"])
        self.assertEqual(summary["Sales"]["missing_mrr"], 1)

    def test_dedupe_and_personal_fields_are_removed(self):
        rows = [
            {"company": "Acme", "slug": "acme", "founder": "A Person", "mrr": "$1k"},
            {"company": "Acme renamed", "slug": "acme", "author": "B Person", "mrr": "$2k"},
        ]
        clean = normalize_records(rows)
        self.assertEqual(len(clean), 1)
        self.assertEqual(clean[0]["mrr"], 2000.0)
        self.assertNotIn("founder", json.dumps(clean).lower())
        self.assertNotIn("author", json.dumps(clean).lower())

    def test_csv_formula_cells_are_neutralized(self):
        self.assertEqual(csv_cell("=1+1"), "'=1+1")
        self.assertEqual(csv_cell("+cmd"), "'+cmd")
        self.assertEqual(csv_cell("ordinary"), "ordinary")

    def test_weekly_diff_and_outputs(self):
        payload = {"rows": [
            {"company": "Acme", "slug": "acme", "category": "SEO", "mrr": "$1k", "growth": 4, "price": "$12k", "revenue_period": "monthly", "source_url": "https://trustmrr.com/startup/acme", "captured_at": "2026-11-09"},
            {"company": "Beta", "slug": "beta", "category": "SEO", "mrr": "$2k", "growth": 2, "price": "unknown", "revenue_period": "monthly", "source_url": "https://trustmrr.com/startup/beta", "captured_at": "2026-11-09"},
            {"company": "Coda", "slug": "coda", "category": "Sales", "mrr": "unknown", "growth": None, "price": "$10k", "revenue_period": "monthly", "source_url": "https://trustmrr.com/startup/coda", "captured_at": "2026-11-09"},
        ]}
        first = analyze(payload)
        second_payload = dict(payload)
        second_payload["rows"] = [payload["rows"][0], dict(payload["rows"][1], mrr="$2.5k"), {"company": "New Co", "slug": "new-co", "category": "SEO", "mrr": "$3k", "source_url": "https://trustmrr.com/startup/new-co", "captured_at": "2026-11-10"}]
        second = analyze(second_payload, first["snapshot"])
        status = {r["slug"]: r["status"] for r in second["rows"]}
        self.assertEqual(status["new-co"], "new")
        self.assertEqual(status["acme"], "unchanged")
        self.assertIn("changed", status["beta"])
        self.assertEqual(second["snapshot"]["schema_version"], 1)
        with tempfile.TemporaryDirectory() as tmp:
            write_outputs(second, tmp)
            self.assertTrue((Path(tmp) / "report.md").is_file())
            self.assertTrue((Path(tmp) / "run.json").is_file())
            with (Path(tmp) / "companies.csv").open() as f:
                self.assertEqual(len(list(csv.DictReader(f))), 3)

    def test_sanitized_live_capture_preserves_unknown_period(self):
        fixture = json.loads((Path(__file__).parent / "fixtures" / "sanitized_live.json").read_text())
        rows = normalize_records(fixture["rows"])
        self.assertEqual(rows[0]["mrr"], 83.0)
        self.assertEqual(rows[1]["mrr"], 971.0)
        self.assertTrue(all(row["annual_multiple"] is None for row in rows))


if __name__ == "__main__":
    unittest.main()
