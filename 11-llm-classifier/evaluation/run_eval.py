"""
evaluation/run_eval.py
======================
Runs the classifier against a labelled test set and prints:
  - Accuracy
  - Per-class F1
  - Calibration table (confidence bucket vs actual accuracy)
  - Flag rate and flag precision

Usage:
    python -m evaluation.run_eval

Set OPENAI_API_KEY in your environment before running.
"""

import asyncio
import json
import os
from collections import defaultdict
from typing import Optional

from app.classifier import classify_product

# ---------- Labelled test set ----------
# 30 examples across all categories, including ambiguous edge cases.
# Add more to increase statistical power.

TEST_SET = [
    # Electronics
    {"description": "4K OLED 65-inch smart TV with HDR10+ and Dolby Vision", "label": "Electronics"},
    {"description": "True wireless earbuds with active noise cancellation, IPX5 waterproof", "label": "Electronics"},
    {"description": "Mechanical keyboard with Cherry MX red switches, RGB backlit", "label": "Electronics"},
    {"description": "Portable power bank 20000mAh, 65W PD fast charging", "label": "Electronics"},
    # Clothing
    {"description": "Women's waterproof hiking jacket, 3-layer shell, detachable hood", "label": "Clothing & Apparel"},
    {"description": "Men's merino wool base layer, long sleeve, medium weight", "label": "Clothing & Apparel"},
    {"description": "Running shoes with carbon fibre plate, marathon-grade cushioning", "label": "Clothing & Apparel"},
    # Home & Kitchen
    {"description": "Stainless steel 6-quart Instant Pot with air fryer lid", "label": "Home & Kitchen"},
    {"description": "Bamboo cutting board set with juice groove, 3 sizes", "label": "Home & Kitchen"},
    {"description": "Robot vacuum with LiDAR mapping and self-emptying base", "label": "Home & Kitchen"},
    # Sports & Outdoors
    {"description": "Carbon road bike frame, 700c, Di2 compatible, 1000g", "label": "Sports & Outdoors"},
    {"description": "Camping hammock with rain fly and straps, holds 400 lbs", "label": "Sports & Outdoors"},
    {"description": "Resistance band set 5-piece, light to heavy, includes door anchor", "label": "Sports & Outdoors"},
    # Health & Beauty
    {"description": "Retinol 0.5% serum with hyaluronic acid and niacinamide", "label": "Health & Beauty"},
    {"description": "Electric toothbrush with pressure sensor, 4 modes, 60-day battery", "label": "Health & Beauty"},
    {"description": "Magnesium glycinate 400mg capsules, 120 count, non-GMO", "label": "Health & Beauty"},
    # Books & Media
    {"description": "Hardcover edition — Atomic Habits by James Clear", "label": "Books & Media"},
    {"description": "Vinyl record — Kind of Blue by Miles Davis, 180g audiophile pressing", "label": "Books & Media"},
    # Toys & Games
    {"description": "LEGO Technic Formula 1 car, 1432 pieces, age 10+", "label": "Toys & Games"},
    {"description": "Strategy board game for 2–6 players, 45-minute playtime", "label": "Toys & Games"},
    # Food & Grocery
    {"description": "Organic cold-brew coffee concentrate, 32oz, single-origin Ethiopian beans", "label": "Food & Grocery"},
    {"description": "Extra virgin olive oil 500ml, first cold press, PDO certified", "label": "Food & Grocery"},
    # Automotive
    {"description": "Dash cam 4K front and rear, built-in GPS, parking mode", "label": "Automotive"},
    {"description": "OBD2 bluetooth scanner, reads and clears fault codes", "label": "Automotive"},
    # Office Supplies
    {"description": "Wireless vertical ergonomic mouse, 6 DPI settings, silent click", "label": "Office Supplies"},
    {"description": "A4 hardcover dotted notebook, 240 pages, lay-flat binding", "label": "Office Supplies"},
    # Ambiguous / edge cases (these test calibration)
    {"description": "Smart water bottle that tracks hydration via mobile app", "label": "Electronics"},
    {"description": "Yoga mat with alignment lines and carrying strap", "label": "Sports & Outdoors"},
    {"description": "Posture corrector brace, adjustable, wear under clothing", "label": "Health & Beauty"},
    {"description": "Portable espresso maker, manual, no electricity needed, travel size", "label": "Home & Kitchen"},
]


async def run_eval(confidence_threshold: float = 0.75) -> dict:
    results = []

    print(f"\nRunning evaluation on {len(TEST_SET)} examples...\n")

    for i, item in enumerate(TEST_SET, 1):
        pred = await classify_product(item["description"])
        correct = pred["category"] == item["label"]
        flagged = pred["confidence"] < confidence_threshold

        results.append({
            "description": item["description"][:60],
            "label": item["label"],
            "predicted": pred["category"],
            "confidence": pred["confidence"],
            "correct": correct,
            "flagged": flagged,
        })

        status = "✓" if correct else "✗"
        flag = " [FLAGGED]" if flagged else ""
        print(f"  [{i:02d}] {status} {pred['category']:<22} conf={pred['confidence']:.2f}{flag}")
        print(f"       └─ {item['description'][:70]}")

    return results


def print_metrics(results: list[dict], confidence_threshold: float = 0.75):
    total = len(results)
    correct_all = [r for r in results if r["correct"]]
    flagged = [r for r in results if r["flagged"]]
    correct_flagged = [r for r in flagged if r["correct"]]
    not_flagged = [r for r in results if not r["flagged"]]
    correct_not_flagged = [r for r in not_flagged if r["correct"]]

    print("\n" + "=" * 60)
    print("OVERALL METRICS")
    print("=" * 60)
    print(f"  Total examples:          {total}")
    print(f"  Overall accuracy:        {len(correct_all)/total:.1%}")
    print(f"  Flag rate:               {len(flagged)/total:.1%}  ({len(flagged)} items)")
    if not_flagged:
        print(f"  Accuracy (non-flagged):  {len(correct_not_flagged)/len(not_flagged):.1%}")
    if flagged:
        print(f"  Accuracy (flagged):      {len(correct_flagged)/len(flagged):.1%}")

    # Per-class F1
    print("\nPER-CLASS RESULTS")
    print("-" * 60)
    print(f"  {'Category':<25} {'TP':>4} {'FP':>4} {'FN':>4} {'F1':>6}")
    print(f"  {'-'*25} {'----':>4} {'----':>4} {'----':>4} {'----':>6}")

    categories = sorted({r["label"] for r in results})
    for cat in categories:
        tp = sum(1 for r in results if r["label"] == cat and r["predicted"] == cat)
        fp = sum(1 for r in results if r["label"] != cat and r["predicted"] == cat)
        fn = sum(1 for r in results if r["label"] == cat and r["predicted"] != cat)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
        print(f"  {cat:<25} {tp:>4} {fp:>4} {fn:>4} {f1:>6.2f}")

    # Calibration table
    print("\nCALIBRATION (confidence bucket vs actual accuracy)")
    print("-" * 60)
    print(f"  {'Bucket':<15} {'Count':>6} {'Accuracy':>10} {'Avg conf':>10}")
    print(f"  {'-'*15} {'-----':>6} {'--------':>10} {'--------':>10}")

    buckets = defaultdict(list)
    for r in results:
        bucket = round(r["confidence"] * 10) / 10  # round to nearest 0.1
        buckets[bucket].append(r)

    for bucket in sorted(buckets.keys()):
        items = buckets[bucket]
        acc = sum(1 for r in items if r["correct"]) / len(items)
        avg_conf = sum(r["confidence"] for r in items) / len(items)
        label = f"{bucket-0.05:.1f}–{bucket+0.05:.1f}"
        print(f"  {label:<15} {len(items):>6} {acc:>10.1%} {avg_conf:>10.2f}")

    # Errors
    errors = [r for r in results if not r["correct"]]
    if errors:
        print(f"\nMISCLASSIFICATIONS ({len(errors)})")
        print("-" * 60)
        for r in errors:
            flag = " [FLAGGED]" if r["flagged"] else ""
            print(f"  ✗ {r['description'][:55]}")
            print(f"    Label: {r['label']}  →  Predicted: {r['predicted']}  conf={r['confidence']:.2f}{flag}")


async def main():
    threshold = float(os.getenv("CONFIDENCE_THRESHOLD", "0.75"))
    results = await run_eval(threshold)
    print_metrics(results, threshold)

    # Save results to JSON for further analysis
    output_path = "evaluation/results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nFull results saved to {output_path}\n")


if __name__ == "__main__":
    asyncio.run(main())
