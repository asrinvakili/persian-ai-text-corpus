"""
merge_full.py
=============
Combine data/full/human_texts.jsonl and data/full/ai_texts.jsonl
into a single dataset_combined.jsonl file.

This is convenient for users who prefer one file over two,
but it produces the same records as loading both files together.

Usage:
    python examples/merge_full.py
    # writes data/dataset_combined.jsonl
"""

import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"


def main():
    out_path = DATA / "dataset_combined.jsonl"
    count = 0
    with open(out_path, "w", encoding="utf-8", newline="\n") as fout:
        for src in [DATA / "full" / "human_texts.jsonl", DATA / "full" / "ai_texts.jsonl"]:
            with open(src, encoding="utf-8") as fin:
                for line in fin:
                    if line.strip():
                        fout.write(line if line.endswith("\n") else line + "\n")
                        count += 1
    print(f"Wrote {count} records to {out_path}")


if __name__ == "__main__":
    main()
