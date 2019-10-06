import serial
import binascii

def read():
    prot = {
        'enquiry_module': '\x03\x12\x00\x15',
        'enquiry_module_return': '\x02\x12\x14',
        'active_buzzer': '\x02\x13\x15',
        'enquiry_card': '\x03\x02\x00\x05',
        'enquiry_cards_return': '\x03\x02\x01\x06', # got valid card
        'enquiry_no_card_found': '\x02\x01\x03', # no card reachable or invalid
        'enquiry_all_cards': '\x03\x02\x01\x05',
        'anticollision' : '\x02\x03\x05\x00',
        'select_card' : '\x02\x04\x06',
    }

    ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
    last=""

    while True:
        ser.write(prot['enquiry_card'].encode())
        resp =  ser.read(4)
        #print(resp.encode('hex'))
        #if resp == prot['enquiry_no_card_found']:
            #print ("no valid card reachable")
        if resp == prot['enquiry_cards_return'].encode():

            resp = ser.read(3)
            #print(resp.encode('hex'))
            #if resp == prot['active_buzzer'].encode():

            ser.write(prot['anticollision'].encode())
            resp = ser.read(7)
            header = binascii.b2a_hex(resp)[:4].decode("utf-8")

            if header == "0603" and binascii.b2a_hex(resp)[-5:].decode("utf-8"):
                ser.write(prot['active_buzzer'].encode())
                #print(binascii.b2a_hex(resp).decode("utf-8"))
                #last = binascii.b2a_hex(resp).decode("utf-8")
                return binascii.b2a_hex(resp).decode("utf-8")

    ser.close()
