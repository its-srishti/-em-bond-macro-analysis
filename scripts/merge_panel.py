import pandas as pd

# --- Load annual WDI ---
wdi = pd.read_csv("data/raw/worldbank_wdi_2010_2024.csv", parse_dates=["date"])

# Generate monthly dates
panel_months = pd.date_range(start="2010-01-31", end="2024-12-31", freq="M")

# Forward-fill annual data into monthly
wdi_monthly_list = []
for country in wdi["country"].unique():
    sub = wdi[wdi["country"] == country].set_index("date")
    sub = sub.reindex(panel_months).ffill().reset_index()
    sub = sub.rename(columns={"index": "date"})
    sub["country"] = country
    wdi_monthly_list.append(sub)

wdi_monthly = pd.concat(wdi_monthly_list, ignore_index=True)

# --- Load bond + oil + USD data ---
panel = pd.read_csv("data/cleaned/panel_monthly_2010_2024.csv", parse_dates=["date"])

# --- Merge them ---
final = panel.merge(wdi_monthly, on=["country", "date"], how="left")

# --- Save final dataset ---
final.to_csv("data/cleaned/panel_final_2010_2024.csv", index=False)

print("✅ Final panel saved at data/cleaned/panel_final_2010_2024.csv")
