import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Number of samples
num_samples = 5000

# -------------------------------
# 1. Generate Speed (8 bits: 0-255 km/h)
# -------------------------------
# Parameters for Log-Normal Distribution
# Given:
# - Median = exp(mu) = 40 km/h => mu = ln(40) ≈ 3.688879
# - Mean = exp(mu + sigma^2 / 2) = 45 km/h
# Solve for sigma:
# sigma^2 / 2 = ln(45) - mu ≈ 3.806662 - 3.688879 ≈ 0.117783
# sigma ≈ sqrt(0.235566) ≈ 0.4853514

mu = 3.688879 # ln(10)
sigma = 0.4853514

# Generate log-normal distributed speeds
speed = np.random.lognormal(mean=mu, sigma=sigma, size=num_samples)

# Clip speeds to the range [0, 255] and convert to integers
speed = np.clip(speed, 0, 255).astype(int)

# ----------------------------------------
# 2. Generate Relative Distance (0-127 meters)
# ----------------------------------------

relative_distance = np.random.uniform(low=0, high=127, size=num_samples)
relative_distance = relative_distance.round().astype(int)

# ----------------------------------------
# 3. Generate Direction (0-360 degrees)
# ----------------------------------------

direction = np.random.uniform(low=-60, high=60, size=num_samples)
direction = direction.round().astype(int)

# ----------------------------------------
# 5. Generate Brake/Turn Status
# ----------------------------------------

brake_turn_choices = [
    'brake_next_brake_self',  # brake_next, brake_self
    'brake_next_turn_self',   # brake_next, turn_self
    'none_next_brake_self',   # none_next, brake_self
    'none_next_turn_self',    # none_next, turn_self
    'none_none'               # none, none
]
brake_turn_probs = [0.15, 0.07, 0.25, 0.12, 0.41]
brake_turn_status = np.random.choice(brake_turn_choices, size=num_samples, p=brake_turn_probs)

# ----------------------------------------
# 7. Create DataFrame
# ----------------------------------------

data = pd.DataFrame({
    'Speed_km_h': speed,
    'Relative_Distance_m': relative_distance,
    'Direction_deg': direction,
    'Brake_Turn_Status': brake_turn_status
})


# ----------------------------------------
# 8. Export to CSV
# ----------------------------------------

# Save the DataFrame to a CSV file without encoding categorical variables
data.to_csv('synthetic_dataset.csv', index=False)

print("Dataset generation complete. 'synthetic_dataset.csv' has been created.")