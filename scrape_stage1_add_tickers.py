#!/usr/bin/env python3
"""Stage 1: Add New Tickers and Update Old Ones"""

import numpy as np
import pandas as pd

print("=" * 60)
print("STAGE 1: ADD NEW TICKERS AND UPDATE OLD ONES")
print("=" * 60)

# Collect NASDAQ data
print("\nFetching NASDAQ tickers...")
nasdaq = pd.read_json("https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nasdaq/nasdaq_full_tickers.json")
nasdaq = nasdaq.set_index('symbol')
nasdaq['exchange'] = 'NMS'
nasdaq['market'] = 'NASDAQ Global Select'
print(f"  Found {len(nasdaq)} NASDAQ tickers")

# Collect NYSE data
print("Fetching NYSE tickers...")
nyse = pd.read_json("https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/nyse/nyse_full_tickers.json")
nyse = nyse.set_index('symbol')
nyse['exchange'] = 'ASE'
nyse['market'] = 'NYSE MKT'
print(f"  Found {len(nyse)} NYSE tickers")

# Collect AMEX data, since it got acquired this is now the same exchange/market as NYSE
print("Fetching AMEX tickers...")
amex = pd.read_json("https://raw.githubusercontent.com/rreichel3/US-Stock-Symbols/main/amex/amex_full_tickers.json")
amex = amex.set_index('symbol')
amex['exchange'] = 'ASE'
amex['market'] = 'NYSE MKT'
print(f"  Found {len(amex)} AMEX tickers")

# Combine the datasets
exchange_data = pd.concat([nasdaq, nyse, amex])
print(f"\n  Total tickers from exchanges: {len(exchange_data)}")

# Obtain the categories from the FinanceDatabase for conversion
print("\nLoading category mapping files...")
fd_categories_path = 'compression/categories/github_exchange_categories.xlsx'
fd_sectors = pd.read_excel(fd_categories_path, sheet_name='sector', index_col=1)
fd_industry_groups = pd.read_excel(fd_categories_path, sheet_name='industry_group', index_col=1)
fd_industries = pd.read_excel(fd_categories_path, sheet_name='industry', index_col=1)

# Read the equities database
print("Loading existing equities database...")
equities = pd.read_csv('database/equities.csv', index_col=0)
print(f"  Current database size: {len(equities)} equities")

ticker_dict = {}

# Loop over the exchange dataset and create a new object that will be added to the database
print("\nProcessing tickers...")
for index, row in exchange_data.iterrows():
    if row['marketCap']:
        market_cap_value = float(row['marketCap'])

        if market_cap_value >= 200_000_000_000:
            market_cap = 'Mega Cap'
        elif market_cap_value >= 10_000_000_000 and market_cap_value < 200_000_000_000:
            market_cap= 'Large Cap'
        elif market_cap_value >= 2_000_000_000 and market_cap_value < 10_000_000_000:
            market_cap = 'Mid Cap'
        elif market_cap_value >= 300_000_000 and market_cap_value < 2_000_000_000:
            market_cap = 'Small Cap'
        elif market_cap_value >= 50_000_000 and market_cap_value < 300_000_000:
            market_cap = 'Micro Cap'
        else:
            market_cap = 'Nano Cap'
    else:
        market_cap = np.nan

    try:
        # Checks if ticker exists, if yes, continue
        fd_data = equities.loc[index]

        if fd_data['market_cap'] != market_cap and market_cap == market_cap:
            ticker_dict[index] = {'symbol': index}
            for column, value in fd_data.items():
                if column == 'market_cap':
                    ticker_dict[index][column] = market_cap
                else:
                    ticker_dict[index][column] = value
        continue
    except KeyError:
        if index != index:
          # Specific case where the ticker is NA which is recognized
          # as a NaN instead meaning it will continuously be added
          index = "NA"

        ticker_dict[index] = {}

        ticker_dict[index]['name'] = row['name']
        ticker_dict[index]['summary'] = np.nan
        ticker_dict[index]['currency'] = "USD"

        try:
            industry = fd_industries.loc[row['industry']].iloc[0]

            if isinstance(industry, pd.Series):
                industry = industry[0]

            ticker_dict[index]['industry'] = industry
        except KeyError:
            ticker_dict[index]['industry'] = np.nan

        try:
            industry_divison = equities[equities['industry'] == ticker_dict[index]['industry']]
            industry_group = industry_divison['industry_group'].mode()[0]

            ticker_dict[index]['industry_group'] = industry_group
        except KeyError:
            ticker_dict[index]['industry_group'] = np.nan

        try:
            sector_division = equities[(equities['industry_group'] == ticker_dict[index]['industry_group']) & (equities['industry'] == ticker_dict[index]['industry'])]
            sector = sector_division['sector'].mode()[0]

            ticker_dict[index]['sector'] = sector
        except Exception:
            ticker_dict[index]['sector'] = np.nan

        ticker_dict[index]['exchange'] = row['exchange']
        ticker_dict[index]['market'] = row['market']
        ticker_dict[index]['country'] = row['country']
        ticker_dict[index]['state'] = np.nan
        ticker_dict[index]['city'] = np.nan
        ticker_dict[index]['zipcode'] = np.nan
        ticker_dict[index]['website'] = np.nan
        ticker_dict[index]['market_cap'] = market_cap
        ticker_dict[index]['isin'] = np.nan
        ticker_dict[index]['cusip'] = np.nan
        ticker_dict[index]['figi'] = np.nan
        ticker_dict[index]['composite_figi'] = np.nan
        ticker_dict[index]['shareclass_figi'] = np.nan

# Create a DataFrame out of the created dictionary
updated_companies = pd.DataFrame.from_dict(ticker_dict, orient='index')
updated_companies.index.name = 'symbol'

print(f"\nThere are {len(updated_companies)} new updates!")

if not updated_companies.empty:
    # Loop over all acquired values and update data
    for index, values in updated_companies.iterrows():
        try:
            equities.loc[index] = updated_companies.loc[index]
        except KeyError:
            equities = pd.concat([equities, values])

    # Sort the index
    equities = equities.sort_index()

    # Drop NaN values in the index
    new_index = equities.index.dropna()

    # Update the equities DataFrame
    equities = equities.loc[new_index]

    # Send to CSV
    print("\nSaving updated database...")
    equities.to_csv('database/equities.csv')
    print(f"  Database updated! New size: {len(equities)} equities")
else:
    print("\nNo updates needed. Database is up to date.")

print("\n" + "=" * 60)
print("STAGE 1 COMPLETE")
print("=" * 60)
