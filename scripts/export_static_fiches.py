from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "data" / "fiches.json"
sys.path.insert(0, str(ROOT))

from app import load_all_fiches


def main() -> None:
    fiches = load_all_fiches()
    OUTPUT_FILE.write_text(
        json.dumps(fiches, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{len(fiches)} fiches exportées vers {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
