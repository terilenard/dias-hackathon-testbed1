from Crypto.Hash import CMAC
from Crypto.Cipher import AES

def synchronize_counter(message, truncCounter, mac):
    #Secret Key and Data identifier
    identifier = '00c8'
    hexSecKey = "D251E60F5CDFC443A3DADD6968E871CB"

    #MAC generation
    secret= bytearray.fromhex(hexSecKey)
    for i in range(0x00, 0xFFFFFF):
        cobj = CMAC.new(secret, ciphermod=AES)
        counter = str('{:06x}'.format(i)) + truncCounter
        hexMes = identifier + message + counter
        byteMes= bytearray.fromhex(hexMes)
        cobj.update(byteMes)
        if cobj.hexdigest()[0:6] == mac:
            with open("counter.txt", "w") as f:
                f.write(str(counter)+ "\n")
            return
