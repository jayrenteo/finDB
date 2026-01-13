#!/usr/bin/env python3
"""Stage 2: Update Compression Files"""

import pandas as pd

print("=" * 60)
print("STAGE 2: UPDATE COMPRESSION FILES")
print("=" * 60)

print("\nCompressing databases to BZ2 format...\n")

# Cryptos
print("  Processing cryptos.csv...")
cryptos = pd.read_csv('database/cryptos.csv')
cryptos.to_csv('compression/cryptos.bz2', index=False, compression='bz2')
print(f"    → {len(cryptos)} records compressed")

# Currencies
print("  Processing currencies.csv...")
currencies = pd.read_csv('database/currencies.csv')
currencies.to_csv('compression/currencies.bz2', index=False, compression='bz2')
print(f"    → {len(currencies)} records compressed")

# Equities
print("  Processing equities.csv...")
equities = pd.read_csv('database/equities.csv')
equities.to_csv('compression/equities.bz2', index=False, compression='bz2')
print(f"    → {len(equities)} records compressed")

# ETFs
print("  Processing etfs.csv...")
etfs = pd.read_csv('database/etfs.csv')
etfs.to_csv('compression/etfs.bz2', index=False, compression='bz2')
print(f"    → {len(etfs)} records compressed")

# Funds
print("  Processing funds.csv...")
funds = pd.read_csv('database/funds.csv')
funds.to_csv('compression/funds.bz2', index=False, compression='bz2')
print(f"    → {len(funds)} records compressed")

# Indices
print("  Processing indices.csv...")
indices = pd.read_csv('database/indices.csv')
indices.to_csv('compression/indices.bz2', index=False, compression='bz2')
print(f"    → {len(indices)} records compressed")

# Money Markets
print("  Processing moneymarkets.csv...")
moneymarkets = pd.read_csv('database/moneymarkets.csv')
moneymarkets.to_csv('compression/moneymarkets.bz2', index=False, compression='bz2')
print(f"    → {len(moneymarkets)} records compressed")

print("\n" + "=" * 60)
print("STAGE 2 COMPLETE")
print("=" * 60)
