global DATAW
DATAW = 16    ## Half of the actual data to be encrypted
global C
C = pow(2,DATAW)-4
global enKey

enKey = 0x794928fe49283f89  ## Key bit length should


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

def lsfr():
    state = 0b11111
    bits = []
    for i in range(0,31):
        bits.append(state&1)
        newbit = ((state>>3)^state)&1
        state = (state>>1)|(newbit<<4)
    return bits



def enckey(Key):       ##key generation function  
    keylist=[]
    rand = lsfr()
    keyout = Key%(pow(2,DATAW))
    key3 = ((Key%(pow(2,2*DATAW)))//pow(2,DATAW))
    key2 = ((Key%(pow(2,3*DATAW)))//pow(2,2*DATAW))
    key1 = ((Key%(pow(2,4*DATAW)))//pow(2,3*DATAW))
    for i in range(0,len(rand)):
        keylist.append(keyout)
        keyout = keyout^(key3 & rotL(DATAW,key3,5))         ##
        keyout = keyout^rotL(DATAW,key3,1)                  ## round function
        keyout = keyout^C^rand[i]                           ##
        (key1,key2,key3,keyout) = (keyout,key1,key2,key3)     ##packet flipping
        
    return keylist

def encrypt(Data):           ##encryption function
    masterkey = enKey
    stateL = ((Data%(pow(2,2*DATAW)))//pow(2,DATAW))
    stateR = Data%(pow(2,DATAW))
    Key = enckey(masterkey)
    for i in range(0,len(Key)):
        stateR = stateR^(stateL & rotL(DATAW,stateL,5))  ##
        stateR = stateR^rotL(DATAW,stateL,1)             ## round function
        stateR = stateR^Key[i]                           ##
        if (i<len(Key)-1):
            (stateR,stateL) = (stateL,stateR)            ##packet flipping

        print("Key: ",hex(Key[i])," Left: ",hex(stateL)," Right: ",hex(stateR))
    encdata = [stateL,stateR]
    print("Encrypted packets: ",hex(encdata[0]),hex(encdata[1]))
    encrdata = pow(2,DATAW)*encdata[0] + encdata[1]
    print(" Final encrypted data: ",hex(encrdata))

in_data = int("0x"+input("Input the 32-bit data in hexadecimal"),16)
encrypt(in_data)
                    


    
    
    
