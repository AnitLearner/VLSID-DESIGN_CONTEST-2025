import serial
import time
import pandas as pd

# Function to split the hexadecimal string into bytes
def split_hex_to_bytes(hex_string):
    if hex_string.startswith("0x"):
        hex_string = hex_string[2:]
    data_sequence = [bytes([int(hex_string[i:i+2], 16)]) for i in range(0, len(hex_string), 2)]
    return data_sequence

# Function to send the latest encrypted data over UART
def send_hex_data_from_file_continuously(port, baudrate, file_path, delay):
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

   
        while True:
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

if __name__ == '__main__':
    file_path = '/content/encrypted_data.xlsx'  
    uart_port = "COM3"  
    baud_rate = 115200
    delay_between_sends = 0.05  # Delay in seconds (50ms)

    send_hex_data_from_file_continuously(uart_port, baud_rate, file_path, delay_between_sends)
