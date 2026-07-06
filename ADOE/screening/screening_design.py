import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Domain"))

from mortar_domain import domain

import pandas as pd
from bofire.data_models.strategies.api import RandomStrategy
import bofire.strategies.api as strategies_api

# Build the strategy from existing Domain
strategy_data_model = RandomStrategy(domain=domain, seed=42)
strategy = strategies_api.map(strategy_data_model)


n_screening_runs = 12 # ******Decide batch size**********

# Generate the screening design
screening_design = strategy.ask(n_screening_runs)

screening_design["data_source"] = "OurLab" #*******Decide what the sources should be called*****
screening_design["curing_age_days"] = screening_design["curing_age_days"].astype(int)

print("Generated screening design:")
print(screening_design)

# Check the output
print("\nSummary statistics:")
print(screening_design.describe(include="all"))

print("\nColumn bounds check:")
for feat in domain.inputs.features:
    if feat.key in screening_design.columns:
        print(feat.key, "min:", screening_design[feat.key].min(),
              "max:", screening_design[feat.key].max())

# Export for the lab technician

screening_design.to_csv("mortar_screening_design.csv", index=False)
print("\nSaved to mortar_screening_design.csv")