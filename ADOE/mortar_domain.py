from bofire.data_models.domain.api import Domain, Inputs, Outputs
from bofire.data_models.features.api import ContinuousInput, CategoricalInput, DiscreteInput, ContinuousOutput
from bofire.data_models.objectives.api import MaximizeObjective
from bofire.data_models.constraints.api import LinearEqualityConstraint, NChooseKConstraint

binder = ContinuousInput(key="total_binder", bounds=(240, 2150))
wb_ratio = ContinuousInput(key="w_b_ratio", bounds=(0.20, 0.50))
scm_pct = ContinuousInput(key="scm_replacement_pct", bounds=(0, 100))
hrwr = ContinuousInput(key="hrwr_dosage", bounds=(0, 22.5))
cure_temp = ContinuousInput(key="curing_temp", bounds=(4.5, 22))
scm_identity = CategoricalInput(key="scm_identity", categories=["C1","C2","F1","S1","S2","S3","None"])
curing_age = DiscreteInput(key="curing_age_days", values=[1, 3, 5, 28])

compressive_strength = ContinuousOutput(key="f_c_ksi", objective=MaximizeObjective(w=1.0))

inputs = Inputs(features=[binder, wb_ratio, scm_pct, hrwr, cure_temp, scm_identity, curing_age])
outputs = Outputs(features=[compressive_strength])

domain = Domain(inputs=inputs, outputs=outputs)

print("Domain created successfully!")
print(domain)
print("\nInput keys:", domain.inputs.get_keys())
print("Output keys:", domain.outputs.get_keys())