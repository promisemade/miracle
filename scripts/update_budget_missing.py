import io
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd
import requests

URL_DEST_NATURE = "https://www.budget.gouv.fr/documentation/file-download/31618"
DATA_PATH = Path("data/ministeres.json")


def norm(text: str) -> str:
    text = str(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()
    return text


def to_mdeur(value: float) -> str:
    return f"{value / 1_000_000_000:.2f}".replace(".00", ".0").replace(".00", "")


def main() -> int:
    resp = requests.get(URL_DEST_NATURE, timeout=60)
    resp.raise_for_status()
    df = pd.read_excel(io.BytesIO(resp.content))
    df.columns = [str(c).strip() for c in df.columns]

    mapping = {
        "ministere-de-l-europe-et-des-affaires-etrangeres": "Europe et affaires étrangères",
        "ministere-de-l-economie-des-finances-et-de-la-souverainete-industrielle-et-numerique": "Économie, finances et souveraineté industrielle, énergétique et numérique",
        "ministere-de-la-culture": "Culture",
        "ministere-des-armees": "Armées et anciens combattants",
        "ministere-de-la-sante-des-familles-de-l-autonomie-et-des-personnes-handicapees": "Santé, familles, autonomie et personnes handicapées",
        "ministere-des-sports-de-la-jeunesse-et-de-la-vie-associative": "Sports, jeunesse et vie associative",
    }

    name_norm = df["Ministère"].astype(str).map(norm)
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    updated = 0

    for m in data.get("ministeres", []):
        mid = m.get("id")
        if mid not in mapping:
            continue
        target = mapping[mid]
        tnorm = norm(target)
        dfm = df[name_norm == tnorm].copy()
        if dfm.empty:
            print("No rows for", target)
            continue

        dfm["CP PLF"] = pd.to_numeric(dfm["CP PLF"], errors="coerce").fillna(0)
        dfm["AE  PLF"] = pd.to_numeric(dfm["AE  PLF"], errors="coerce").fillna(0)

        total_cp = float(dfm["CP PLF"].sum())
        total_ae = float(dfm["AE  PLF"].sum())
        t2_cp = float(dfm[dfm["Code Titre"] == 2]["CP PLF"].sum())
        hors_t2_cp = total_cp - t2_cp

        mission_cp = dfm.groupby("Mission")["CP PLF"].sum().sort_values(ascending=False)
        prog_cp = (
            dfm.groupby(["Programme", "Libellé Programme"])["CP PLF"]
            .sum()
            .sort_values(ascending=False)
        )

        lines = [
            f"Total CP PLF 2026 : {to_mdeur(total_cp)} MdEUR",
            f"Total AE PLF 2026 : {to_mdeur(total_ae)} MdEUR",
            f"Titre 2 (personnel) CP 2026 : {to_mdeur(t2_cp)} MdEUR",
            f"Hors titre 2 CP 2026 : {to_mdeur(hors_t2_cp)} MdEUR",
            "Missions (CP 2026) :",
        ]
        for mission, cp in mission_cp.head(6).items():
            lines.append(f"- {mission} : {to_mdeur(float(cp))} MdEUR")
        lines.append("Programmes principaux (CP 2026) :")
        for (prog, label), cp in prog_cp.head(8).items():
            lines.append(f"- P{int(prog):03d} {label} : {to_mdeur(float(cp))} MdEUR")

        m["budget"] = lines
        updated += 1

    if updated:
        DATA_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print("Updated budgets:", updated)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
