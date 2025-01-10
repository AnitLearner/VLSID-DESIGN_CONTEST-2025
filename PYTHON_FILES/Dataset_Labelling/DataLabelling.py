## ********* THE FINAL ONE FOR THE DATASET CREATION ********
import pandas as pd

file_path = '/content/generated_vehicle_dataset.xlsx'
df = pd.read_excel(file_path)

# One-hot encoding of categorical column i.e., Brake_Turn_Status
one_hot_encoded = pd.get_dummies(df['Brake_Turn_Status'], prefix='brake_turn')
df = pd.concat([df, one_hot_encoded], axis=1)

# The Output Classes:
# 1 --> Emergency Brake
# 2 --> Speed Up
# 3 --> Slow Down
# 4 --> Lane Change
# 5 --> No Action

left_turn_threshold = -30
right_turn_threshold = 30

def classify_output(row):
    speed = row['Speed_km_h']
    distance = row['Relative_Distance_m']
    direction = row['Direction_deg']
    brake_next_brake_self = row['brake_turn_brake_next_brake_self']
    none_none = row['brake_turn_none_none']
    brake_next_turn_self = row['brake_turn_brake_next_turn_self']
    none_next_turn_self = row['brake_turn_none_next_turn_self']
    none_next_brake_self = row['brake_turn_none_next_brake_self']

    # Output class determination
    if brake_next_brake_self == 1:
        if speed > 50 and distance < 20:
            return 1
        elif speed <= 50 and distance < 15:
            return 3
        else:
            return 5
    elif none_none == 1:
        if speed < 20 and distance < 10:
            return 1
        elif speed < 40 and distance < 20:
            return 3
        elif speed >= 40 and speed <= 60 and distance < 30:
            return 5
        else:
            return 2
    elif brake_next_turn_self == 1:
        if speed < 30 and distance < 20:
            return 4
        elif speed < 50 and distance < 30:
            return 5
        else:
            return 2
    elif none_next_turn_self == 1:
        if speed < 20 and distance < 10:
            return 1
        elif speed < 30 and distance < 15:
            return 5
        elif direction < left_turn_threshold:
            return 4
        elif direction > right_turn_threshold:
            return 4
        else:
            return 2
    elif none_next_brake_self == 1:
        if speed > 50 and distance < 20:
            return 1
        elif speed < 40 and distance < 30:
            return 3
        else:
            return 2
    else:
        # Default class determination based on direction checks
        if direction < left_turn_threshold:
            return 4
        elif direction > right_turn_threshold:
            return 4
        return 5  # Default to No Action if no specific conditions are met


df['Output'] = df.apply(classify_output, axis=1)
df.to_excel(file_path, index=False)
print(df[['Speed_km_h', 'Relative_Distance_m', 'Direction_deg', 'Brake_Turn_Status', 'Output']].head())