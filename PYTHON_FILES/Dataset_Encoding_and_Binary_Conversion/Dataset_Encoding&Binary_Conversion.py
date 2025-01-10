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
print(df[['Speed_km_h', 'Relative_Distance_m', 'Direction_deg', 'Brake_Turn_Status', 'Output']].head())import pandas as pd

def update_and_convert_to_binary(old_file_path, new_file_path, binary_file_path):
    try:
        old_data = pd.read_excel(old_file_path)
    except FileNotFoundError:
        print(f"Error: {old_file_path} not found!")
        return

    brake_turn_mapping = {
        "brake_next_brake_self": [1, 0, 0, 0, 0],
        "brake_next_turn_self": [0, 1, 0, 0, 0],
        "none_next_brake_self": [0, 0, 1, 0, 0],
        "none_next_turn_self": [0, 0, 0, 1, 0],
        "none_none": [0, 0, 0, 0, 1]
    }

    def to_twos_complement(value, bit_length=7):
        if value < 0:

            return format((1 << bit_length) + value, f'0{bit_length}b')
        else:
            return format(value, f'0{bit_length}b')

    new_data = []
    binary_data = []
    for _, row in old_data.iterrows():
        try:
            speed = row["Speed_km_h"]
            distance = row["Relative_Distance_m"]
            direction = row["Direction_deg"]
            brake_turn_status = row["Brake_Turn_Status"]

            one_hot = brake_turn_mapping.get(brake_turn_status, None)
            if one_hot is None:
                continue

            speed_bin = format(int(speed), '010b')  # 10 bits for speed
            distance_bin = format(int(distance), '010b')  # 10 bits for distance

            # Convert direction to two's complement binary
            direction_bin = to_twos_complement(int(direction), 7)  # 7 bits for direction (-60 to +60 directly)

            binary_string = ''.join(map(str, one_hot)) + speed_bin + distance_bin + direction_bin
            binary_string = binary_string[:32]  # Ensure 32-bit length

            new_data.append({
                "brake_next_brake_self": one_hot[0],
                "brake_next_turn_self": one_hot[1],
                "none_next_brake_self": one_hot[2],
                "none_next_turn_self": one_hot[3],
                "none_none": one_hot[4],
                "Speed_km_h": speed,
                "Relative_Distance_m": distance,
                "Direction_deg": direction
            })
            binary_data.append({"Binary_String": binary_string})

        except KeyError as e:
            print(f"Missing column: {e}")
            continue

    # If no data was added, add a default empty row
    if not new_data:
        print("No valid data found in the old file. Writing default empty row.")
        new_data.append({
            "brake_next_brake_self": 0,
            "brake_next_turn_self": 0,
            "none_next_brake_self": 0,
            "none_next_turn_self": 0,
            "none_none": 0,
            "Speed_km_h": 0,
            "Relative_Distance_m": 0,
            "Direction_deg": 0
        })
        binary_data.append({"Binary_String": '0' * 32})

    new_data_df = pd.DataFrame(new_data)
    new_data_df.to_excel(new_file_path, index=False)
    print(f"New file saved to {new_file_path}")

    binary_data_df = pd.DataFrame(binary_data)
    binary_data_df.to_excel(binary_file_path, index=False)
    print(f"Binary file saved to {binary_file_path}")

old_file_path = "/content/Final_VLSID_Dataset.xlsx"
new_file_path = "/content/Data_Conversion.xlsx"
binary_file_path = "/content/Data_Binary.xlsx"
update_and_convert_to_binary(old_file_path, new_file_path, binary_file_path)
