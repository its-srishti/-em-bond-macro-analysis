# scripts/read_bonds.py
import pandas as pd
import os

# Paths
RAW_DIR = r"C:\Users\ASUS\Documents\-em-bond-macro-analysis\data\Raw\Dependent"
CLEAN_DIR = r"C:\Users\ASUS\Documents\-em-bond-macro-analysis\data\cleaned"

# Ensure cleaned directory exists
os.makedirs(CLEAN_DIR, exist_ok=True)

def clean_investing_csv(path, country):
    """Reads Investing.com CSV, cleans, and aggregates to monthly yields."""
    # Read CSV
    df = pd.read_csv(path)

    # Pick correct value column
    if "Price" in df.columns:
        value_col = "Price"
    elif "Yield" in df.columns:
        value_col = "Yield"
    else:
        raise ValueError(f"Neither 'Price' nor 'Yield' column found in {path}")

    # Standardize column names
    df = df.rename(columns={"Date": "date", value_col: "yield"})
    df["date"] = pd.to_datetime(df["date"])

    # Clean yield column (strip % if present)
    df["yield"] = (
        df["yield"]
        .astype(str)              # make sure it's string
        .str.replace("%", "", regex=False)  # remove %
        .str.replace(",", "", regex=False)  # remove thousand separators if any
    )
    df["yield"] = pd.to_numeric(df["yield"], errors="coerce")

    # Sort and resample monthly (use "ME" instead of deprecated "M")
    df = df.set_index("date").sort_index()
    monthly = df.resample("ME").mean(numeric_only=True).reset_index()

    # Save cleaned file
    out_path = os.path.join(CLEAN_DIR, f"{country.lower()}_10y_monthly.csv")
    monthly.to_csv(out_path, index=False)
    print(f"✅ Saved {out_path}")

    return monthly


# --- Countries and file names ---
countries = {
    "India": "India 10-Year Bond Yield Historical Data.csv",
    "Brazil": "Brazil 10-Year Bond Yield Historical Data.csv",
    "South Africa": "South Africa 10-Year Bond Yield Historical Data.csv",
    "Turkey": "Turkey 10-Year Bond Yield Historical Data.csv",
    "Egypt": "Egypt 10-Year Bond Yield Historical Data.csv",
    "SriLanka": "Sri Lanka 10-Year Bond Yield Historical Data.csv",
}

# --- Loop over countries ---
all_data = {}
for country, filename in countries.items():
    file_path = os.path.join(RAW_DIR, filename)
    if os.path.exists(file_path):
        all_data[country] = clean_investing_csv(file_path, country)
    else:
        print(f"⚠️ File not found for {country}: {file_path}")