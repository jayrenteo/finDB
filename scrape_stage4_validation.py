#!/usr/bin/env python3
"""Stage 4: Check GICS Categorisation"""

import pandas as pd
import json

print("=" * 60)
print("STAGE 4: VALIDATE GICS CATEGORIZATION")
print("=" * 60)

print("\nValidating GICS hierarchy...")

invalid_rows = pd.DataFrame()
errors = []
gics = json.load(open("compression/categories/categories.json", "r"))
equities = pd.read_csv("database/equities.csv", index_col=0)
filtered_data = equities[equities['sector'].notna() & equities['industry_group'].notna() & equities['industry'].notna()]

print(f"  Total equities: {len(equities)}")
print(f"  Equities with full categorization: {len(filtered_data)}")

validation_errors = 0
for index, row in filtered_data.iterrows():
    sector, industry_group, industry = row['sector'], row['industry_group'], row['industry']

    try:
        # Search whether it can find the combination
        gics[sector][industry_group][industry]
    except KeyError as error:
        # If it can't, add to invalid_rows DataFrame
        row['error'] = error
        invalid_rows = pd.concat([invalid_rows, row], axis=1)
        validation_errors += 1


if not invalid_rows.empty:
    invalid_rows = invalid_rows.T

    print("\n" + "!" * 60)
    print("VALIDATION ERRORS FOUND:")
    print("!" * 60)
    for index, row in invalid_rows.iterrows():
        print(f"{index}: {row['error']}")

    raise ValueError("There are invalid sector, industry groups and/or industries found. "
                     "Please check if it adheres to compression/categories/categories.json")
else:
    print("\n  ✓ All categorizations are valid!")

print("\n" + "=" * 60)
print("STAGE 4 COMPLETE")
print("=" * 60)
