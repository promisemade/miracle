import io
import re
from collections import defaultdict

import pandas as pd
import requests

URL_T2 = "https://www.budget.gouv.fr/documentation/file-download/32004"
URL_DEST = "https://www.budget.gouv.fr/documentation/file-download/31621"
URL_DEST_NATURE = "https://www.budget.gouv.fr/documentation/file-download/31618"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text)).strip()


def main() -> int:
    resp = requests.get(URL_T2, timeout=60)
    resp.raise_for_status()
    content = resp.content

    xlsx = pd.ExcelFile(io.BytesIO(content))
    print("Sheets:", xlsx.sheet_names)

    # Scan sheets for likely budget tables.
    matches = defaultdict(list)
    for name in xlsx.sheet_names:
        df = xlsx.parse(name, dtype=str, header=None)
        print("\n---", name, "shape:", df.shape, "---")
        print("Head rows:")
        print(df.head(5))

        header_row = df.iloc[0].tolist()
        print("Header row:", header_row)

        # Identify numeric-like columns.
        numeric_cols = []
        for col in df.columns:
            sample = df[col].dropna().astype(str).head(20)
            if sample.empty:
                continue
            ratio = sample.str.contains(r"\d", regex=True).mean()
            if ratio > 0.6:
                numeric_cols.append(col)
        print("Numeric-like columns:", numeric_cols)

        for row_idx, row in df.iterrows():
            row_text = " | ".join([normalize(v) for v in row.values if v and str(v) != "nan"])
            if not row_text:
                continue
            if any(
                key in row_text.lower()
                for key in [
                    "programme",
                    "mission",
                    "total",
                    "ae",
                    "cp",
                    "t2",
                    "titre 2",
                    "emplois",
                    "effectifs",
                ]
            ):
                matches[name].append((row_idx, row_text))
        if matches[name]:
            print("\n=== Sheet:", name, "===")
            for row_idx, row_text in matches[name][:12]:
                print(f"{row_idx}: {row_text}")

    print("\n=== Destination expenses file ===")
    resp = requests.get(URL_DEST, timeout=60)
    resp.raise_for_status()
    dest_content = resp.content

    try:
        df_dest = pd.read_excel(io.BytesIO(dest_content))
    except Exception as exc:
        print("Failed to read XLS with pandas, error:", exc)
        return 1

    print("Columns:", list(df_dest.columns))
    print("Sample rows:")
    print(df_dest.head(8))

    print("\n=== Destination+Nature expenses file ===")
    resp = requests.get(URL_DEST_NATURE, timeout=60)
    resp.raise_for_status()
    dest_nat_content = resp.content
    try:
        df_dest_nat = pd.read_excel(io.BytesIO(dest_nat_content))
    except Exception as exc:
        print("Failed to read XLS with pandas, error:", exc)
        return 1

    print("Columns:", list(df_dest_nat.columns))
    print("Sample rows:")
    print(df_dest_nat.head(8))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
