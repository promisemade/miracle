import io
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd
import requests

URL_DEST_NATURE = "https://www.budget.gouv.fr/documentation/file-download/31618"
DATA_PATH = Path("data/ministeres.json")


def normalize_text(text: str) -> str:
    if text is None:
        return ""
    text = str(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_col(name: str) -> str:
    return re.sub(r"\s+", "", normalize_text(name))


def find_col(df: pd.DataFrame, target: str) -> str:
    target_norm = normalize_col(target)
    for col in df.columns:
        if normalize_col(col) == target_norm:
            return col
    raise KeyError(f"Missing column '{target}'")


def to_mdeur(value: float) -> str:
    return f"{value / 1_000_000_000:.2f}".replace(".00", ".0").replace(".00", "")


def build_budget_lines(df_min: pd.DataFrame) -> list[str]:
    cp_col = find_col(df_min, "CP PLF")
    ae_col = find_col(df_min, "AE PLF")
    titre_col = find_col(df_min, "Code Titre")
    mission_col = find_col(df_min, "Mission")
    prog_col = find_col(df_min, "Programme")
    prog_label_col = find_col(df_min, "Libellé Programme")

    df_min = df_min.copy()
    df_min[cp_col] = pd.to_numeric(df_min[cp_col], errors="coerce").fillna(0)
    df_min[ae_col] = pd.to_numeric(df_min[ae_col], errors="coerce").fillna(0)

    total_cp = float(df_min[cp_col].sum())
    total_ae = float(df_min[ae_col].sum())

    df_t2 = df_min[df_min[titre_col] == 2]
    t2_cp = float(df_t2[cp_col].sum())
    hors_t2_cp = total_cp - t2_cp

    mission_cp = df_min.groupby(mission_col)[cp_col].sum().sort_values(ascending=False)
    prog_cp = (
        df_min.groupby([prog_col, prog_label_col])[cp_col]
        .sum()
        .sort_values(ascending=False)
    )

    lines = []
    lines.append(f"Total CP PLF 2026 : {to_mdeur(total_cp)} MdEUR")
    lines.append(f"Total AE PLF 2026 : {to_mdeur(total_ae)} MdEUR")
    lines.append(f"Titre 2 (personnel) CP 2026 : {to_mdeur(t2_cp)} MdEUR")
    lines.append(f"Hors titre 2 CP 2026 : {to_mdeur(hors_t2_cp)} MdEUR")

    lines.append("Missions (CP 2026) :")
    for mission, cp in mission_cp.head(6).items():
        lines.append(f"- {mission} : {to_mdeur(float(cp))} MdEUR")

    lines.append("Programmes principaux (CP 2026) :")
    for (prog, label), cp in prog_cp.head(8).items():
        lines.append(f"- P{int(prog):03d} {label} : {to_mdeur(float(cp))} MdEUR")

    return lines


def resolve_ministere_mapping(data: list[dict], source_names: list[str]) -> dict[str, str]:
    data_norm = []
    for m in data:
        name = normalize_text(m.get("name", ""))
        short_name = normalize_text(m.get("short_name", ""))
        data_norm.append((m.get("id"), name, short_name))

    mapping = {}
    for source in source_names:
        source_norm = normalize_text(source)
        best_id = None
        best_score = 0
        for m_id, name, short_name in data_norm:
            if not m_id:
                continue
            candidates = [name, short_name]
            for cand in candidates:
                if not cand:
                    continue
                if source_norm in cand or cand in source_norm:
                    score = max(len(source_norm), len(cand))
                    if score > best_score:
                        best_id = m_id
                        best_score = score
        if best_id:
            mapping[best_id] = source
    return mapping


def main() -> int:
    resp = requests.get(URL_DEST_NATURE, timeout=60)
    resp.raise_for_status()
    df = pd.read_excel(io.BytesIO(resp.content))
    df.columns = [str(c).strip() for c in df.columns]

    ministere_col = find_col(df, "Ministère")
    df["__min_norm"] = df[ministere_col].map(normalize_text)

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    ministeres = data.get("ministeres", [])

    source_names = sorted({str(v).strip() for v in df[ministere_col].dropna().unique()})
    mapping = resolve_ministere_mapping(ministeres, source_names)

    updated = 0
    for m in ministeres:
        source_name = mapping.get(m.get("id"))
        if not source_name:
            continue
        source_norm = normalize_text(source_name)
        df_min = df[df["__min_norm"] == source_norm]
        if df_min.empty:
            continue
        m["budget"] = build_budget_lines(df_min)
        updated += 1

    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Updated budget for {updated} ministeres.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
