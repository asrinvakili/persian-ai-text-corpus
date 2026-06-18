"""
load_dataset.py
===============
Minimal example showing four common ways to load and use the corpus.
Works on Python 3.10+ with only the standard library (no external dependencies).

Usage:
    python examples/load_dataset.py
"""

import json
import random
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


# ---------------------------------------------------------------------------
# 1. Basic JSONL loader
# ---------------------------------------------------------------------------


def load_jsonl(path):
    """Read a JSONL file into a list of dicts."""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# ---------------------------------------------------------------------------
# 2. Load the default train/val/test splits
# ---------------------------------------------------------------------------


def load_splits():
    return {
        "train": load_jsonl(DATA / "splits" / "train.jsonl"),
        "val": load_jsonl(DATA / "splits" / "val.jsonl"),
        "test": load_jsonl(DATA / "splits" / "test.jsonl"),
    }


# ---------------------------------------------------------------------------
# 3. Load the full corpus and group AI texts by their human counterpart
# ---------------------------------------------------------------------------


def load_paired():
    """
    Returns (humans, ai_by_human_id) where:
      humans: {human_id: human_record}
      ai_by_human_id: {human_id: [ai_record, ai_record, ai_record]}
    """
    humans = {r["human_id"]: r for r in load_jsonl(DATA / "full" / "human_texts.jsonl")}
    ai_by_hid = defaultdict(list)
    for r in load_jsonl(DATA / "full" / "ai_texts.jsonl"):
        ai_by_hid[r["human_id"]].append(r)
    return humans, ai_by_hid


# ---------------------------------------------------------------------------
# 4. Build a balanced 1:1 subset (one AI version per topic)
# ---------------------------------------------------------------------------


def build_balanced(seed=42):
    """Subsample one AI record per human topic to obtain a 1:1 class balance."""
    rng = random.Random(seed)
    humans, ai_by_hid = load_paired()
    balanced = []
    for hid, h in humans.items():
        balanced.append(h)
        balanced.append(rng.choice(ai_by_hid[hid]))
    rng.shuffle(balanced)
    return balanced


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------


def main():
    print("=" * 60)
    print("Demo 1 — default splits")
    print("=" * 60)
    splits = load_splits()
    for name, recs in splits.items():
        n_human = sum(1 for r in recs if r["label"] == 0)
        n_ai = sum(1 for r in recs if r["label"] == 1)
        print(f"  {name:5s}: {len(recs):4d} total ({n_human} human / {n_ai} AI)")

    print("\n" + "=" * 60)
    print("Demo 2 — matched pairs (human + 3 AI per topic)")
    print("=" * 60)
    humans, ai_by_hid = load_paired()
    sample_hid = next(iter(humans))
    print(f"  Topic: {humans[sample_hid]['title']}")
    print(f"  Human ({humans[sample_hid]['num_words']} words):")
    print(f"    {humans[sample_hid]['text'][:120]}...")
    for ai in ai_by_hid[sample_hid]:
        print(f"  AI [{ai['model']}] ({ai['num_words']} words):")
        print(f"    {ai['text'][:120]}...")

    print("\n" + "=" * 60)
    print("Demo 3 — balanced 1:1 subset")
    print("=" * 60)
    balanced = build_balanced()
    n_human = sum(1 for r in balanced if r["label"] == 0)
    n_ai = sum(1 for r in balanced if r["label"] == 1)
    print(f"  Total: {len(balanced)} ({n_human} human / {n_ai} AI)")

    print("\n" + "=" * 60)
    print("Demo 4 — texts and labels for sklearn-style training")
    print("=" * 60)
    train = splits["train"]
    X = [r["text"] for r in train]
    y = [r["label"] for r in train]
    print(f"  X: list of {len(X)} strings")
    print(f"  y: list of {len(y)} labels (0=human, 1=AI)")
    print(f"  Example X[0]: {X[0][:80]}...")
    print(f"  Example y[0]: {y[0]}")


if __name__ == "__main__":
    main()
