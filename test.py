#!/usr/bin/python

#
#   Example Satel Integra ETHM-1 module TCP/IP connection
#

import socket
import binascii


def connect(cmd):

    # testopstelling
    host = "10.0.1.248"
    port = 7094

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(cmd)
        data = s.recv(1024)

    return data


def hexToBin(hex):
    res = "{0:08b}".format(int(hex, 16))
    return str(res)


def leftRotate(st):
    n0 = st[0]
    n1 = st[1]
    n2 = st[2]
    n3 = st[3]
    n4 = st[4]
    n5 = st[5]
    n6 = st[6]
    n7 = st[7]
    return n1+n2+n3+n4+n5+n6+n7+n0


def binToHex(bin):
    return hex(int(bin, 2))


def makeCRC16():
    nr1 = "14"
    nr2 = "7A"

    out1 = binToHex(leftRotate(hexToBin(nr1)))
    out2 = binToHex(leftRotate(hexToBin(nr2)))
    a = int(out1[2] + out1[3] + out2[2] + out2[3], 16)
    b = 0xffff
    return hex(a ^ b)


def makeCRC32(crc16):
    # print(crc16)
    var1 = crc16[2] + crc16[3]
    var2 = crc16[4] + crc16[5]
    hout1 = binToHex(leftRotate(hexToBin(var1)))
    hout2 = binToHex(leftRotate(hexToBin(var2)))
    a = int(hout1[2] + hout1[3] + hout2[2] + hout2[3], 16)
    b = 0xffff
    return hex(a ^ b)
        

def makeCMD(cmd, cmd2=''):
    retour = makeCRC16() 
    CRChigh = retour[2] + retour[3]
    CRClow = retour[4] + retour[5]
    retour = int(retour, 0)
    somhigh = int('0x' + CRChigh, 0)
    somcmd = int('0x' + cmd, 0)
    som = retour + somhigh + somcmd
    som_hex = hex(som)
    if cmd2:
        retour2 = makeCRC32(som_hex)
        CRChigh2 = retour2[2] + retour2[3]
        retour2 = int(retour2, 0)
        somhigh2 = int('0x' + CRChigh2, 0)
        somcmd2 = int('0x' + cmd2, 0)
        som2 = retour2 + somhigh2 + somcmd2
        som_hex2 = hex(som2)

        CRChigh2 = som_hex2[2] + som_hex2[3]
        CRClow2 = som_hex2[4] + som_hex2[5]

        s1 = binascii.unhexlify('FE')
        s2 = binascii.unhexlify('FE')

        d1 = binascii.unhexlify(cmd) # cmd
        d2 = binascii.unhexlify(cmd2) # cmd2
        d3 = binascii.unhexlify(CRChigh2) # CRChigh
        d4 = binascii.unhexlify(CRClow2) # CRClow

        e1 = binascii.unhexlify('FE')
        e2 = binascii.unhexlify('0D')
        cmd = s1+s2+d1+d2+d3+d4+e1+e2
        return cmd
    else:
        CRChigh = som_hex[2] + som_hex[3]
        CRClow = som_hex[4] + som_hex[5]

        s1 = binascii.unhexlify('FE')
        s2 = binascii.unhexlify('FE')

        d1 = binascii.unhexlify(cmd) # cmd
        d2 = binascii.unhexlify(CRChigh) # CRChigh
        d3 = binascii.unhexlify(CRClow) # CRClow

        e1 = binascii.unhexlify('FE')
        e2 = binascii.unhexlify('0D')
        cmd = s1+s2+d1+d2+d3+e1+e2
        return cmd


# version
# print(binascii.hexlify(connect(makeCMD('7C')))) # INT-RS/ETHM-1 module version
# print(binascii.hexlify(connect(makeCMD('7E')))) # INTEGRA version


# # 32 BIT
# print(binascii.hexlify(connect(makeCMD('00', 'ff')))) # zones violation
# print(binascii.hexlify(connect(makeCMD('01', 'ff')))) # zones tamper
# print(binascii.hexlify(connect(makeCMD('02', 'ff')))) # zones alarm
# print(binascii.hexlify(connect(makeCMD('03', 'ff')))) # zones tamper alarm
# print(binascii.hexlify(connect(makeCMD('04', 'ff')))) # zones alarm memory
# print(binascii.hexlify(connect(makeCMD('05', 'ff')))) # zones tamper alarm memory
# print(binascii.hexlify(connect(makeCMD('06', 'ff')))) # zones bypass
# print(binascii.hexlify(connect(makeCMD('07', 'ff')))) # zones 'no violation' trouble
# print(binascii.hexlify(connect(makeCMD('08', 'ff')))) # zones 'long violation' trouble
# print(binascii.hexlify(connect(makeCMD('17', 'ff')))) # outputs state
# print(binascii.hexlify(connect(makeCMD('26', 'ff')))) # zones isolate
# print(binascii.hexlify(connect(makeCMD('28', 'ff')))) # zones masked

# # stream
# print(binascii.hexlify(connect(makeCMD('7F'))))




data = {
    'cmd': {
        '7C': {
            'meaning': 'INT-RS/ETHM-1 module version',
            'bytes': 12,
            'answer': {
                'Version:': 11,
                'Module:': 1 # INT-GSM module as addition
            }
        },
        '7E': {
            'meaning': 'INTEGRA version',
            'bytes': 14,
            'answer': {
                'Type:': 1,
                'V:': 11,
                'Language:': 1,
                'settings stored in FLASH:': 1
            },
            'type': {
                0: 'INTEGRA 24',
                1: 'INTEGRA 32',
                2: 'INTEGRA 64',
                3: 'INTEGRA 128',
                4: 'INTEGRA 128-WRL SIM300',
                66: 'INTEGRA 64 PLUS',
                67: 'INTEGRA 128 PLUS',
                72: 'INTEGRA 256 PLUS',
                132: 'INTEGRA 128-WRL LEON'
            },
            'languages': {
                0: {
                    'code': 'PL',
                    'name': 'Poland'
                },
                9: {
                    'code': 'NL',
                    'name': 'Netherlands'
                }
            }
        }
    },

}
# print(data['cmd']['7C']['meaning'])
# print(data['cmd']['7C']['bytes'])




def send(cmd):
    r = binascii.hexlify(connect(makeCMD(cmd.upper()))).decode("utf-8")[4:-8] # INT-RS/ETHM-1 module version
    # print(r) # 7c323039323032323033313803
    cmd = r[0] + r[1]
    # print(cmd)
    getdata = data['cmd'][cmd.upper()]
    print(getdata['meaning'])
    # print(r)
    # print(getdata['bytes'])
    

    r = r[2:]
    # print(r)
    for name in getdata['answer']:
        charters = getdata['answer'][name] * 2

        if charters > 2:
            out = binascii.a2b_hex(r[:charters]).decode("utf-8")
        else:
            out = int(r[:charters], base=16)
        
        print(name + str(out))
        r = r[charters:]



    print('')
    print('')


    # v = binascii.a2b_hex(r[2:-14]).decode("utf-8")
    # d = binascii.a2b_hex(r[2:]).decode("utf-8")[3:]

    # print('cmd:    ' + cmd)
    # print('versie: ' + v)
    # print('datum:  ' + d)




    # print(binascii.a2b_hex(r).decode("utf-8"))

send('7C')
send('7E')