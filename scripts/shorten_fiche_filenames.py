from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FICHES_DIR = ROOT / "Fiches de postes"
TITLE_MAP_FILE = ROOT / "data" / "fiches_titles.json"
DEFAULT_MAX_NAME_LENGTH = 55
HASH_LENGTH = 6


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    ascii_text = ascii_text.replace("&", " et ")
    ascii_text = ascii_text.replace("_", " ")
    ascii_text = re.sub(r"(?<=\w)\.(?=\w)", "", ascii_text)
    ascii_text = re.sub(r"[’'`]+", "", ascii_text)
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    ascii_text = re.sub(r"-{2,}", "-", ascii_text).strip("-")
    return ascii_text or "fiche"


def trim_slug(slug: str, max_length: int) -> str:
    if len(slug) <= max_length:
        return slug

    trimmed = slug[:max_length].rstrip("-")
    split_at = trimmed.rfind("-")
    if split_at >= max_length // 2:
        trimmed = trimmed[:split_at]

    trimmed = trimmed.rstrip("-")
    return trimmed or slug[:max_length]


def build_short_name(file_path: Path, max_name_length: int) -> str:
    ext = file_path.suffix.lower()
    max_slug_length = max_name_length - len(ext) - HASH_LENGTH - 1
    if max_slug_length < 8:
        raise ValueError("max_name_length is too small to build a safe filename.")

    slug = trim_slug(slugify(file_path.stem), max_slug_length)
    digest = hashlib.md5(str(file_path.relative_to(FICHES_DIR)).encode("utf-8")).hexdigest()[:HASH_LENGTH]
    return f"{slug}-{digest}{ext}"


def build_plan(max_name_length: int) -> tuple[list[tuple[Path, Path]], dict[str, str]]:
    rename_ops: list[tuple[Path, Path]] = []
    title_map: dict[str, str] = {}
    future_paths: set[Path] = set()

    files = sorted(
        (path for path in FICHES_DIR.rglob("*") if path.is_file()),
        key=lambda path: str(path.relative_to(FICHES_DIR)),
    )

    for src in files:
        if len(src.name) > max_name_length:
            dst = src.with_name(build_short_name(src, max_name_length))
        else:
            dst = src

        if dst in future_paths:
            raise RuntimeError(f"Collision détectée pour {dst}")
        future_paths.add(dst)
        rename_ops.append((src, dst))
        title_map[str(dst.relative_to(FICHES_DIR)).replace("\\", "/")] = src.stem

    current_paths = {path.resolve(): path for path in files}
    for src, dst in rename_ops:
        if dst == src:
            continue
        dst_resolved = dst.resolve()
        if dst_resolved in current_paths and current_paths[dst_resolved] != src:
            raise RuntimeError(f"Le fichier cible existe déjà: {dst}")

    return rename_ops, title_map


def apply_plan(rename_ops: list[tuple[Path, Path]], title_map: dict[str, str]) -> None:
    for src, dst in rename_ops:
        if src == dst:
            continue
        src.rename(dst)

    TITLE_MAP_FILE.write_text(
        json.dumps(title_map, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Raccourcit les noms de fichiers des fiches de poste et génère une table de titres."
    )
    parser.add_argument("--apply", action="store_true", help="Applique réellement les renommages.")
    parser.add_argument(
        "--max-name-length",
        type=int,
        default=DEFAULT_MAX_NAME_LENGTH,
        help=f"Longueur maximale du nom de fichier, extension comprise (défaut: {DEFAULT_MAX_NAME_LENGTH}).",
    )
    parser.add_argument("--show", type=int, default=20, help="Nombre d'exemples à afficher.")
    args = parser.parse_args()

    rename_ops, title_map = build_plan(args.max_name_length)
    changed = [(src, dst) for src, dst in rename_ops if src != dst]

    print(f"Fichiers analysés: {len(rename_ops)}")
    print(f"Fichiers à renommer: {len(changed)}")
    print(f"Fichier de titres: {TITLE_MAP_FILE}")

    for src, dst in changed[: args.show]:
        print(f"- {src.relative_to(FICHES_DIR)}")
        print(f"  -> {dst.relative_to(FICHES_DIR)}")

    if not args.apply:
        print("Dry run uniquement. Relancer avec --apply pour renommer.")
        return

    apply_plan(rename_ops, title_map)
    print("Renommage terminé.")


if __name__ == "__main__":
    main()
