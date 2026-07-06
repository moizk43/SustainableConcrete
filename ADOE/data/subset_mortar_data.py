import pandas as pd

df = pd.read_csv("../../data/boxcrete_data.csv")

# Mortar mixes have zero coarse aggregate
mortar_df = df[df["Coarse Aggregates (kg/m3)"] == 0].copy()

mortar_df = mortar_df.rename(columns={
    "Cement (kg/m3)": "cement",
    "Fly Ash (kg/m3)": "fly_ash",
    "Slag (kg/m3)": "slag",
    "Water (kg/m3)": "water",
    "HRWR (kg/m3)": "hrwr_dosage",
    "Fine Aggregate (kg/m3)": "fine_aggregate",
    "Temp (C)": "curing_temp",
    "Time": "curing_age_days",
    "GWP": "gwp",
    "Strength (Mean)": "f_c_psi",
    "Material Source": "material_source_code",
})

# Drop rows with missing strength measurements before anything else
mortar_df = mortar_df.dropna(subset=["f_c_psi"])

# Derived factors needed for the BoFire domain
mortar_df["total_binder"] = mortar_df["cement"] + mortar_df["fly_ash"] + mortar_df["slag"]
mortar_df["w_b_ratio"] = mortar_df["water"] / mortar_df["total_binder"]
mortar_df["scm_replacement_pct"] = (
    (mortar_df["fly_ash"] + mortar_df["slag"]) / mortar_df["total_binder"] * 100
)

keep_cols = [
    "Mix Name", "total_binder", "w_b_ratio", "scm_replacement_pct",
    "hrwr_dosage", "curing_temp", "curing_age_days",
    "fine_aggregate", "f_c_psi"
]
mortar_df = mortar_df[keep_cols]

# Reproducible subset spanning the design space
subset = mortar_df.sample(n=12, random_state=42)

# Tag the source covariate as required by the ADOE doc (Step 2)
subset["data_source"] = "BOxCrete_UIUC"

subset.to_csv("mortar_prior_subset_labeled.csv", index=False)
print(subset)