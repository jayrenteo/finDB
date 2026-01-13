#!/usr/bin/env python3
"""Stage 3: Update Categorization Files"""

import pandas as pd

print("=" * 60)
print("STAGE 3: UPDATE CATEGORIZATION FILES")
print("=" * 60)

print("\nExtracting categories from databases...\n")

# Cryptos
print("  Processing cryptos categories...")
cryptos = pd.read_csv("database/cryptos.csv", index_col=0)
cryptos_categories = {}
for column in cryptos:
    if column in ['name', 'summary']:
        continue

    cryptos_categories[column] = cryptos[column].dropna().unique()
    cryptos_categories[column].sort()

df_temp = pd.DataFrame.from_dict(cryptos_categories, orient='index').reset_index()
df_temp.to_csv('compression/categories/cryptos_categories.gzip', index=False, compression='gzip')
print(f"    → {len(cryptos_categories)} category columns extracted")

# Currencies
print("  Processing currencies categories...")
currencies = pd.read_csv("database/currencies.csv", index_col=0)
currencies_categories = {}
for column in currencies:
    if column in ['name']:
        continue

    currencies_categories[column] = currencies[column].dropna().unique()
    currencies_categories[column].sort()

df_temp = pd.DataFrame.from_dict(currencies_categories, orient='index').reset_index()
df_temp.to_csv('compression/categories/currencies_categories.gzip', index=False, compression='gzip')
print(f"    → {len(currencies_categories)} category columns extracted")

# Equities
print("  Processing equities categories...")
equities = pd.read_csv("database/equities.csv", index_col=0)
equities_categories = {}
for column in equities:
    if column in ['name', 'summary', 'website']:
        continue

    equities_categories[column] = equities[column].dropna().unique()
    equities_categories[column].sort()

df_temp = pd.DataFrame.from_dict(equities_categories, orient='index').reset_index()
df_temp.to_csv('compression/categories/equities_categories.gzip', index=False, compression='gzip')
print(f"    → {len(equities_categories)} category columns extracted")

# ETFs
print("  Processing etfs categories...")
etfs = pd.read_csv("database/etfs.csv", index_col=0)
etfs_categories = {}
for column in etfs:
    if column in ['name', 'summary']:
        continue

    etfs_categories[column] = etfs[column].dropna().unique()
    etfs_categories[column].sort()

df_temp = pd.DataFrame.from_dict(etfs_categories, orient='index').reset_index()
df_temp.to_csv('compression/categories/etfs_categories.gzip', index=False, compression='gzip')
print(f"    → {len(etfs_categories)} category columns extracted")

# Funds
print("  Processing funds categories...")
funds = pd.read_csv("database/funds.csv", index_col=0)
funds_categories = {}
for column in funds:
    if column in ['name', 'summary', 'manager_name', 'manager_bio']:
        continue

    funds_categories[column] = funds[column].dropna().unique()
    funds_categories[column].sort()

df_temp = pd.DataFrame.from_dict(funds_categories, orient='index').reset_index()
df_temp.to_csv('compression/categories/funds_categories.gzip', index=False, compression='gzip')
print(f"    → {len(funds_categories)} category columns extracted")

# Indices
print("  Processing indices categories...")
indices = pd.read_csv("database/indices.csv", index_col=0)
indices_categories = {}
for column in indices:
    if column in ['name']:
        continue

    indices_categories[column] = indices[column].dropna().unique()
    indices_categories[column].sort()

df_temp = pd.DataFrame.from_dict(indices_categories, orient='index').reset_index()
df_temp.to_csv('compression/categories/indices_categories.gzip', index=False, compression='gzip')
print(f"    → {len(indices_categories)} category columns extracted")

# Money Markets
print("  Processing moneymarkets categories...")
moneymarkets = pd.read_csv("database/moneymarkets.csv", index_col=0)
moneymarkets_categories = {}
for column in moneymarkets:
    if column in ['name']:
        continue

    moneymarkets_categories[column] = moneymarkets[column].dropna().unique()
    moneymarkets_categories[column].sort()

df_temp = pd.DataFrame.from_dict(moneymarkets_categories, orient='index').reset_index()
df_temp.to_csv('compression/categories/moneymarkets_categories.gzip', index=False, compression='gzip')
print(f"    → {len(moneymarkets_categories)} category columns extracted")

print("\n" + "=" * 60)
print("STAGE 3 COMPLETE")
print("=" * 60)
