from bofire.data_models.domain.api import Domain, Inputs, Outputs
from bofire.data_models.features.api import (
    ContinuousInput, CategoricalInput, DiscreteInput, ContinuousOutput
)
from bofire.data_models.objectives.api import MaximizeObjective

# All units are native to the BOxCrete dataset: kg/m3, degC, days, psi.
# Bounds below are the ACTUAL min/max observed across all 77 mortar rows
# (Coarse Aggregates (kg/m3) == 0) in boxcrete_data.csv, not the paper's
# lb/yd3 / ksi text values.

total_binder = ContinuousInput(key="total_binder", bounds=(144, 1266))          # kg/m3
w_b_ratio = ContinuousInput(key="w_b_ratio", bounds=(0.197, 0.500))              # unitless
scm_replacement_pct = ContinuousInput(key="scm_replacement_pct", bounds=(0, 100))  # %
hrwr_dosage = ContinuousInput(key="hrwr_dosage", bounds=(0, 14.67))              # kg/m3
curing_temp = ContinuousInput(key="curing_temp", bounds=(4.5, 22.0))            # degC
fine_aggregate = ContinuousInput(key="fine_aggregate", bounds=(1233, 2357))      # kg/m3
curing_age_days = DiscreteInput(key="curing_age_days", values=[1, 3, 5, 28])     # days (multi-fidelity factor)

data_source = CategoricalInput(key="data_source", categories=["BOxCrete_UIUC", "OurLab"]) #*******Decide what the sources should be called*****

# Response: compressive strength in psi (native dataset unit)
f_c_psi = ContinuousOutput(key="f_c_psi", objective=MaximizeObjective(w=1.0))

inputs = Inputs(features=[
    total_binder, w_b_ratio, scm_replacement_pct,
    hrwr_dosage, curing_temp, fine_aggregate,
    curing_age_days, data_source
])
outputs = Outputs(features=[f_c_psi])

domain = Domain(inputs=inputs, outputs=outputs)

if __name__ == "__main__":
    print("Domain created successfully!")
    print(domain)
    print("\nInput keys:", domain.inputs.get_keys())
    print("Output keys:", domain.outputs.get_keys())
    for feat in domain.inputs.features:
        print(feat.key, "->", feat)