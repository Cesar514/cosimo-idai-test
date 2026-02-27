#!/usr/bin/env python3
"""Generate PRISMA counts in markdown from a CSV file."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

LABELS = {
    "identified_db": "Records identified through database searching",
    "identified_other": "Additional records identified through other sources",
    "deduped": "Records after duplicates removed",
    "screened": "Records screened (title/abstract)",
    "excluded": "Records excluded",
    "fulltext_assessed": "Full-text articles assessed for eligibility",
    "fulltext_excluded": "Full-text articles excluded (with reasons)",
    "qualitative_included": "Studies included in qualitative synthesis",
    "quantitative_included": "Studies included in quantitative synthesis (meta-analysis)",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate PRISMA markdown from CSV.")
    parser.add_argument("--input", default="prisma_counts.csv", help="Input CSV file")
    parser.add_argument("--output", default="prisma_counts.md", help="Output markdown file")
    args = parser.parse_args()

    counts: dict[str, str] = {}
    reasons: list[tuple[str, str]] = []

    with open(args.input, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stage = (row.get("stage") or "").strip()
            count = (row.get("count") or "").strip()
            if not stage:
                continue
            if stage.lower().startswith("reason:"):
                reason = stage.split(":", 1)[1].strip() or "Other"
                reasons.append((reason, count))
            else:
                counts[stage] = count

    lines = ["# PRISMA Counts", ""]
    for key, label in LABELS.items():
        value = counts.get(key, "")
        lines.append(f"- {label}: **n = {value}**")
    lines.append("")

    if reasons:
        lines.append("## Reasons for Full-Text Exclusion")
        lines.append("")
        lines.append("| Reason | Count |")
        lines.append("|---|---|")
        for reason, count in reasons:
            lines.append(f"| {reason} | {count} |")
        lines.append("")

    Path(args.output).write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
