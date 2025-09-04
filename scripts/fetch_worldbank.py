# scripts/fetch_worldbank.py
import wbdata
import pandas as pd
import datetime
import os

os.makedirs('data/raw', exist_ok=True)

# countries to query (WDI country codes)
countries = {
    'IN': 'India',
    'BR': 'Brazil',
    'ZA': 'South Africa',
    'TR': 'Turkey',
    'LK': 'Sri Lanka',
    'EG': 'Egypt'
}

# indicators: code -> column name
indicators = {
    'FP.CPI.TOTL.ZG': 'CPI_annual_pct',
    'NY.GDP.MKTP.KD.ZG': 'GDP_growth_annual_pct',
    'DT.DOD.DECT.CD': 'External_debt_usd'
}

start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2024, 12, 31)

all_dfs = []
for code, country_name in countries.items():
    print("Fetching for", code)
    try:
        df = wbdata.get_dataframe(indicators, country=code, date=(start, end))
        df = df.reset_index().rename(columns={'index':'date'})
        df['country'] = country_name
        all_dfs.append(df)
    except Exception as e:
        print("Error for", code, e)

wb_df = pd.concat(all_dfs, ignore_index=True)
wb_df.to_csv('data/raw/worldbank_wdi_2010_2024.csv', index=False)
print("Saved data/raw/worldbank_wdi_2010_2024.csv")