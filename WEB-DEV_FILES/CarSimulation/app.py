from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import serial
import time

app = Flask(__name__)

# Global Encryption Parameters
DATAW = 16
C = pow(2, DATAW) - 4
Key = 0x794928fe49283f89  # Encryption Key
transmission_active = False

# Left rotate function
def rotL(n, x, y):
    m = pow(2, n)
    l = m // 2
    for _ in range(y):
        if x >= l:
            x = (x << 1) + 1
            x = x % m
        else:
            x = (x << 1) % m
    return x

# Linear-feedback shift register (LFSR)
def lsfr():
    state = 0b11111
    bits = []
    for _ in range(31):
        bits.append(state & 1)
        newbit = ((state >> 3) ^ state) & 1
        state = (state >> 1) | (newbit << 4)
    return bits

# Key encryption
def enckey(Key):
    keylist = []
    rand = lsfr()
    keyout = Key % (pow(2, DATAW))
    key3 = ((Key % (pow(2, 2 * DATAW))) // pow(2, DATAW))
    key2 = ((Key % (pow(2, 3 * DATAW))) // pow(2, 2 * DATAW))
    key1 = ((Key % (pow(2, 4 * DATAW))) // pow(2, 3 * DATAW))
    for randbit in rand:
        keylist.append(keyout)
        keyout = keyout ^ (key3 & rotL(DATAW, key3, 5))
        keyout = keyout ^ rotL(DATAW, key3, 1)
        keyout = keyout ^ C ^ randbit
        key1, key2, key3, keyout = keyout, key1, key2, key3
    return keylist

# Encryption rounds
def encround(Data, masterkey):
    stateL = (Data % (pow(2, 2 * DATAW))) // pow(2, DATAW)
    stateR = Data % pow(2, DATAW)
    Key = enckey(masterkey)
    for key in Key:
        stateR = stateR ^ (stateL & rotL(DATAW, stateL, 5))
        stateR = stateR ^ rotL(DATAW, stateL, 1)
        stateR = stateR ^ key
        if key != Key[-1]:
            stateR, stateL = stateL, stateR
    return [stateL, stateR]

# Convert to two's complement
def to_twos_complement(value, bit_length=7):
    if value < 0:
        return format((1 << bit_length) + value, f'0{bit_length}b')
    return format(value, f'0{bit_length}b')

# Function to split the hexadecimal string into bytes
def split_hex_to_bytes(hex_string):
    if hex_string.startswith("0x"):
        hex_string = hex_string[2:]
    data_sequence = [bytes([int(hex_string[i:i+2], 16)]) for i in range(0, len(hex_string), 2)]
    return data_sequence

# Function to send the latest encrypted data over UART
def send_hex_data_from_file_continuously(port, baudrate, file_path, delay):
    
    global transmission_active
    transmission_active = True  # Allow transmission to start
    
    try:
        # Initialize the serial connection
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,  # 8-bit data
            parity=serial.PARITY_NONE,  # No parity
            stopbits=serial.STOPBITS_ONE,  # 1 stop bit
            timeout=1
        )

        if not ser.is_open:
            ser.open() 
        print(f"Port {ser.port} is open: {ser.is_open}")

   
        while transmission_active:
            data = pd.read_excel(file_path)
            row = data.iloc[0]
            encrypted_data = row['Encrypted_Data'] 
            print(encrypted_data) 

            data_sequence = split_hex_to_bytes(encrypted_data)

            for value in data_sequence:
                ser.write(value)  # Transmit the byte
                print(f"Sent: {value.hex()}")  # Log the byte in hexadecimal format
                time.sleep(delay)  # Wait between transmissions

    except KeyboardInterrupt:
        print("\nTransmission interrupted by user.")
        for value in data_sequence:
            ser.write(value)  # Write the remaining binary data
            print(f"Sent: {value.hex()}")  # Log the remaining data
            time.sleep(delay)  # Wait before sending the next value
    except serial.SerialException as e:
        print(f"Serial Exception: {e}")
    finally:
        if ser.is_open:
            ser.close()
            print("Port closed.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_to_excel():
    data = request.json
    
    car_simulation_folder = os.getcwd()  
    excel_path = os.path.join(car_simulation_folder, 'Final_VLSID_Dataset.xlsx')
    binary_path = os.path.join(car_simulation_folder, 'Data_Binary.xlsx')
    encrypted_path = os.path.join(car_simulation_folder, 'encrypted_data.xlsx')
    data_conversion_path = os.path.join(car_simulation_folder, 'Data_Conversion.xlsx')

    required_columns = ['Speed_km_h', 'Relative_Distance_m', 'Direction_deg', 'Brake_Turn_Status']

    # Mapping for Brake_Turn_Status
    brake_turn_mapping = {
        "brake_next_brake_self": [1, 0, 0, 0, 0],
        "brake_next_turn_self": [0, 1, 0, 0, 0],
        "none_next_brake_self": [0, 0, 1, 0, 0],
        "none_next_turn_self": [0, 0, 0, 1, 0],
        "none_none": [0, 0, 0, 0, 1]
    }

    try:
        # Create a DataFrame with the new entry, overwriting previous content
        new_entry = {
            'Speed_km_h': data['speed'],
            'Relative_Distance_m': data['distance'],
            'Direction_deg': data['degree'],
            'Brake_Turn_Status': data['status']
        }

        df = pd.DataFrame([new_entry], columns=required_columns)

        # Overwrite the Excel file with just this new row
        df.to_excel(excel_path, index=False)
        
          # Format DataFrame for Data_Conversion.xlsx
        brake_turn_columns = [
            "brake_next_brake_self",
            "brake_next_turn_self",
            "none_next_brake_self",
            "none_next_turn_self",
            "none_none"
        ]

        # Convert Brake_Turn_Status to one-hot encoded columns
        one_hot = brake_turn_mapping.get(new_entry["Brake_Turn_Status"], [0, 0, 0, 0, 0])
        brake_turn_df = pd.DataFrame([one_hot], columns=brake_turn_columns)

        # Append Speed, Relative Distance, and Direction
        formatted_df = pd.concat(
            [brake_turn_df,
             pd.DataFrame([{
                 'Speed_km_h': data['speed'],
                 'Relative_Distance_m': data['distance'],
                 'Direction_deg': data['degree']
             }])],
            axis=1
        )
        formatted_df.to_excel(data_conversion_path, index=False)
        # Binary conversion
        binary_data = []
        for _, row in df.iterrows():
            brake_turn_status = row["Brake_Turn_Status"]
            one_hot = brake_turn_mapping.get(brake_turn_status, [0] * 5)
            speed_bin = format(int(row["Speed_km_h"]), '010b')
            distance_bin = format(int(row["Relative_Distance_m"]), '010b')
            direction_bin = to_twos_complement(int(row["Direction_deg"]), 7)
            binary_string = ''.join(map(str, one_hot)) + speed_bin + distance_bin + direction_bin
            binary_data.append(binary_string[:32])

        df['Binary_String'] = binary_data
        # Overwrite the Binary Excel file with just the new row
        df.to_excel(binary_path, index=False)

        # Encryption
        encrypted_data = []
        for binary_string in binary_data:
            data = int(binary_string, 2)
            encrypted_packets = encround(data, Key)
            encrypted_value = pow(2, DATAW) * encrypted_packets[0] + encrypted_packets[1]
            encrypted_data.append(hex(encrypted_value))

        df['Encrypted_Data'] = encrypted_data
        # Overwrite the Encrypted Excel file with just the new row
        df.to_excel(encrypted_path, index=False)

        
          
        uart_port = "COM3"  
        baud_rate = 115200
        delay_between_sends = 0.05  # Delay in seconds (50ms)

        send_hex_data_from_file_continuously(uart_port, baud_rate, encrypted_path, delay_between_sends)
        
        return jsonify({'message': 'Data saved and processed successfully!'})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': str(e)}), 500

@app.route('/stop', methods=['POST'])
def stop_transmission():
    global transmission_active
    transmission_active = False  # Stop transmission
    return jsonify({'message': 'Transmission stopped successfully!'})


if __name__ == '__main__':
    app.run(debug=True)
