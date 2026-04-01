"""Simple DB backup helper for production use."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import os
import shutil

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.getenv("MIRACLE_DB_PATH", PROJECT_ROOT / "data" / "miracle.db"))
BACKUP_DIR = Path(os.getenv("MIRACLE_BACKUP_DIR", PROJECT_ROOT / "data" / "backups"))
KEEP = int(os.getenv("MIRACLE_BACKUP_KEEP", "10"))


def main() -> int:
    if not DB_PATH.exists():
        print(f"Database not found: {DB_PATH}")
        return 1

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"miracle_{timestamp}.db"
    shutil.copy2(DB_PATH, backup_path)
    print(f"Backup created: {backup_path}")

    backups = sorted(BACKUP_DIR.glob("miracle_*.db"), key=lambda p: p.stat().st_mtime, reverse=True)
    for old in backups[KEEP:]:
        old.unlink()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
