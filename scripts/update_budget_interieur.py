import io
import json
import math
from pathlib import Path

import pandas as pd
import requests

URL_DEST_NATURE = "https://www.budget.gouv.fr/documentation/file-download/31618"
DATA_PATH = Path("data/ministeres.json")


def to_mdeur(value: float) -> str:
    return f"{value / 1_000_000_000:.2f}".replace(".00", ".0").replace(".00", "")


def main() -> int:
    resp = requests.get(URL_DEST_NATURE, timeout=60)
    resp.raise_for_status()
    content = resp.content

    df = pd.read_excel(io.BytesIO(content))

    # Normalize column names
    df.columns = [str(c).strip() for c in df.columns]

    # Filter Interior ministry
    df_int = df[df["Ministère"].astype(str).str.strip().str.lower() == "intérieur"]
    if df_int.empty:
        print("No rows found for ministere 'Intérieur'.")
        return 1

    # Use CP PLF for totals (payment credits)
    df_int["CP PLF"] = pd.to_numeric(df_int["CP PLF"], errors="coerce").fillna(0)
    df_int["AE  PLF"] = pd.to_numeric(df_int["AE  PLF"], errors="coerce").fillna(0)

    total_cp = float(df_int["CP PLF"].sum())
    total_ae = float(df_int["AE  PLF"].sum())

    # Titre 2 vs hors T2
    df_t2 = df_int[df_int["Code Titre"] == 2]
    t2_cp = float(df_t2["CP PLF"].sum())
    hors_t2_cp = total_cp - t2_cp

    # Mission totals (CP)
    mission_cp = (
        df_int.groupby("Mission")["CP PLF"].sum().sort_values(ascending=False)
    )

    # Program totals (CP)
    prog_cp = (
        df_int.groupby(["Programme", "Libellé Programme"])["CP PLF"].sum().sort_values(ascending=False)
    )

    budget_lines = []
    budget_lines.append(f"Total CP PLF 2026 : {to_mdeur(total_cp)} MdEUR")
    budget_lines.append(f"Total AE PLF 2026 : {to_mdeur(total_ae)} MdEUR")
    budget_lines.append(f"Titre 2 (personnel) CP 2026 : {to_mdeur(t2_cp)} MdEUR")
    budget_lines.append(f"Hors titre 2 CP 2026 : {to_mdeur(hors_t2_cp)} MdEUR")

    budget_lines.append("Missions (CP 2026) :")
    for mission, cp in mission_cp.head(6).items():
        budget_lines.append(f"- {mission} : {to_mdeur(float(cp))} MdEUR")

    budget_lines.append("Programmes principaux (CP 2026) :")
    for (prog, label), cp in prog_cp.head(8).items():
        budget_lines.append(f"- P{int(prog):03d} {label} : {to_mdeur(float(cp))} MdEUR")

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for m in data.get("ministeres", []):
        if m.get("id") == "ministere-de-l-interieur":
            m["budget"] = budget_lines
            break

    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Updated budget lines for ministere-de-l-interieur")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
