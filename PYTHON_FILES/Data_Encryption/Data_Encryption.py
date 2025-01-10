import pandas as pd

global DATAW
DATAW = 16     # Half of the actual data to be encrypted
global C
C = pow(2,DATAW)-4

def rotL(n,x,y):
    rot = x
    m = pow(2,n)
    l = m/2
    for i in range(0,y):           #left rotate function
        if rot>=l:
            rot=rot<<1
            rot = rot+1            # n = data width
            rot = rot%m
        else:
            rot=rot<<1
            rot = rot%m
    return rot

def lsfr():
    state = 0b11111
    bits = []
    for i in range(0,31):
        bits.append(state&1)
        newbit = ((state>>3)^state)&1
        state = (state>>1)|(newbit<<4)
    return bits

def enckey(Key):                   #encryption function
    keylist=[]
    rand = lsfr()
    keyout = Key%(pow(2,DATAW))
    key3 = ((Key%(pow(2,2*DATAW)))//pow(2,DATAW))
    key2 = ((Key%(pow(2,3*DATAW)))//pow(2,2*DATAW))
    key1 = ((Key%(pow(2,4*DATAW)))//pow(2,3*DATAW))
    print("Key 1: ",hex(key1),"Key 2: ",hex(key2),"Key 3: ",hex(key3),"Key Out: ",hex(keyout))
    for i in range(0,len(rand)):
        keylist.append(keyout)
        print("Key:",i,"= ",hex(keyout),"randbit = ",rand[i])
        keyout = keyout^(key3 & rotL(DATAW,key3,5))
        keyout = keyout^rotL(DATAW,key3,1)                     # round function
        keyout = keyout^C^rand[i]
        (key1,key2,key3,keyout) = (keyout,key1,key2,key3)      #packet flipping

    return keylist

def encround(Data,masterkey):                                  #encryption function
    stateL = ((Data%(pow(2,2*DATAW)))//pow(2,DATAW))
    stateR = Data%(pow(2,DATAW))
    Key = enckey(masterkey)
    for i in range(0,len(Key)):
        stateR = stateR^(stateL & rotL(DATAW,stateL,5))
        stateR = stateR^rotL(DATAW,stateL,1)                   # round function
        stateR = stateR^Key[i]
        if (i<len(Key)-1):
            (stateR,stateL) = (stateL,stateR)                  #packet flipping

        print("Key: ",hex(Key[i])," Left: ",hex(stateL)," Right: ",hex(stateR))
    encdata = [stateL,stateR]
    return encdata


# Define the key to be used for encryption
Key = 0x73bce979d5123456  # Key bit length should be double the length of actual data, i.e., 4 x DATAW

# File paths for input and output
input_file = "/content/Data_Binary.xlsx"
output_file = "encrypted_data.xlsx"

df = pd.read_excel(input_file)
binary_string = df.loc[0, 'Binary_String']
encrypted_data = []
data = int(binary_string, 2)

# Perform encryption
encrypted_packets = encround(data, Key)
encrypted_value = pow(2, DATAW) * encrypted_packets[0] + encrypted_packets[1]

# Add or update the 'Encrypted_Data' column for the first row
df.at[0, 'Encrypted_Data'] = hex(encrypted_value)  # Safely update the column for the first row

# Save the updated DataFrame to the output file
df.to_excel(output_file, index=False)

print(f"Encrypted data saved to {output_file}")

