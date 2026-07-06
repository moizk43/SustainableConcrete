import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Domain"))

from mortar_domain import domain
import pandas as pd
import numpy as np

from bofire.data_models.surrogates.api import MixedSingleTaskGPSurrogate, BotorchSurrogates
from bofire.data_models.strategies.api import SoboStrategy
from bofire.data_models.acquisition_functions.api import qLogEI
import bofire.strategies.api as strategies_api

# Load prior data
experiments = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "..", "data", "mortar_prior_subset_labeled.csv")
)

# Log-time transformation
experiments["log_curing_age"] = np.log(experiments["curing_age_days"])

# Build the surrogate
surrogate_data_model = MixedSingleTaskGPSurrogate(
    inputs=domain.inputs,
    outputs=domain.outputs,
)

surrogates = BotorchSurrogates(surrogates=[surrogate_data_model])

# Build the batch BO strategy
sobo_data_model = SoboStrategy(
    domain=domain,
    surrogate_specs=surrogates,
    acquisition_function=qLogEI(),
)
sobo_strategy = strategies_api.map(sobo_data_model)

# Tell the strategy about existing data
sobo_strategy.tell(experiments)

# Ask for a batch of new candidates
n_batch = 4  #*******Decide (3, 4, or 5)***************
candidates = sobo_strategy.ask(n_batch)
candidates["data_source"] = "OurLab"
print(candidates)
candidates.to_csv(os.path.join(os.path.dirname(__file__), "next_batch_candidates.csv"), index=False)

# Retraining loop (run this block AFTER lab results come back)
# new_results = pd.read_csv(os.path.join(os.path.dirname(__file__), "batch_1_results.csv"))
# experiments = pd.concat([experiments, new_results], ignore_index=True)
# sobo_strategy.tell(experiments)
# next_candidates = sobo_strategy.ask(n_batch)