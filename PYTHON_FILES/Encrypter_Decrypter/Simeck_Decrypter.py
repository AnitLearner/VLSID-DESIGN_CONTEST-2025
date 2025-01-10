global DATAW
DATAW = 16    ## Half of the actual data to be decrypted
global C
C = pow(2,DATAW)-4

global deKey
deKey = 0x9c18a4b3d408eeb7

def rotL(n,x,y):
    rot = x
    m = pow(2,n)
    l = m/2
    for i in range(0,y):           ##left rotate function
        if rot>=l:
            rot=rot<<1
            rot = rot+1             ## n = data width
            rot = rot%m
        else:
            rot=rot<<1
            rot = rot%m
    return rot


def lsfr53():
    state = 0b01100
    bits = []
    for i in range(0,31):
        bits.append(state&1)
        newbit = ((state>>2)^state)&1
        state = (state>>1)|(newbit<<4)
    return bits

def deckey(Key):       ##encryption function  
    keylist=[]
    rand = lsfr53()
    keyout = ((Key%(pow(2,4*DATAW)))//pow(2,3*DATAW))
    key2 = ((Key%(pow(2,3*DATAW)))//pow(2,2*DATAW))
    key3 = ((Key%(pow(2,2*DATAW)))//pow(2,DATAW))
    key4 = Key%(pow(2,DATAW))
    for i in range(0,len(rand)):
        keylist.append(keyout)
        key4 = key4^(keyout & rotL(DATAW,keyout,5))                    ##
        key4 = key4^rotL(DATAW,keyout,1)                               ## round function
        key4 = key4^(pow(2,DATAW)-4)^rand[i]                           ##
        (keyout,key2,key3,key4) = (key4,keyout,key2,key3)     ##packet flipping
    return keylist


def decrypt(Data):           ##encryption function
    demasterkey = deKey
    stateL = ((Data%(pow(2,2*DATAW)))//pow(2,DATAW))
    stateR = Data%(pow(2,DATAW))
    Key = deckey(demasterkey)
    for i in range(0,len(Key)):
        stateR = stateR^(stateL & rotL(DATAW,stateL,5))  ##
        stateR = stateR^rotL(DATAW,stateL,1)             ## round function
        stateR = stateR^Key[i]                           ##
        if (i<len(Key)-1):
            (stateR,stateL) = (stateL,stateR)      ##packet flipping

        print("Key: ",hex(Key[i])," Left: ",hex(stateL)," Right: ",hex(stateR))
    decdata = [stateL,stateR]
    print("Decrypted packets: ",hex(decdata[0]),hex(decdata[1]))
    decrdata = pow(2,DATAW)*decdata[0] + decdata[1]
    print(" Final decrypted data: ",hex(decrdata))


in_data = int("0x"+input("Input the 32-bit encrypted data in hexadecimal"),16)
decrypt(in_data)                    


    
    
    
