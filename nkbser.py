# nkbser.py

import os
import serial
import serial.tools.list_ports
import prompt
from retrying import retry
arduinoascii =  {'128' : 'LEFT_CTRL'
                ,'129' : 'LEFT_SHIFT'
                ,'130' : 'LEFT_ALT'
                ,'131' : 'LEFT_GUI'
                ,'132' : 'RIGHT_CTRL'
                ,'133' : 'RIGHT_SHIFT'
                ,'134' : 'RIGHT_ALT'
                ,'135' : 'RIGHT_GUI'
                ,'218' : 'UP_ARROW'
                ,'217' : 'DOWN_ARROW'
                ,'216' : 'LEFT_ARROW'
                ,'215' : 'RIGHT_ARROW'
                ,'178' : 'BACKSPACE'
                ,'179' : 'TAB'
                ,'176' : 'RETURN'
                ,'177' : 'ESC'
                ,'209' : 'INSERT'
                ,'212' : 'DELETE'
                ,'211' : 'PAGE_UP'
                ,'214' : 'PAGE_DOWN'
                ,'210' : 'HOME'
                ,'213' : 'END'
                ,'193' : 'CAPS_LOCK'
                ,'194' : 'F1'
                ,'195' : 'F2'
                ,'196' : 'F3'
                ,'197' : 'F4'
                ,'198' : 'F5'
                ,'199' : 'F6'
                ,'200' : 'F7'
                ,'201' : 'F8'
                ,'202' : 'F9'
                ,'203' : 'F10'
                ,'204' : 'F11'
                ,'205' : 'F12'
                ,'255' : 'KEY_SPACE'}


global device
device = 0


def searchselect():
    global device
    comp = [comport.device for comport in serial.tools.list_ports.comports()]
    manu = [comport.manufacturer for comport in serial.tools.list_ports.comports()]
    devicecount = len(comp)
    devicelist = { i + 1 : comp[i] for i in range(0,devicecount)}
    print("%d Port(s) Detected " % (len(devicelist))) 
    print("Enter 0 to reload")
    #print(arduinoascii)

    for number in range(devicecount):
        if ("Arduino" in manu[number]) == True:
            respondtext = " <- Probably this one"
        else:
            respondtext = " "
            pass
        print("%d.%s %s" % ((number+1) , comp[number] , respondtext))
    try:
        currentdev = int(input("Type in your device number: "))
    except ValueError:
        
        os.system('cls||clear')
        raise Exception("Invalid Value") 
    
    os.system('cls||clear')

    if not 0 < currentdev <= devicecount:
        os.system('cls||clear')
        raise Exception("Invalid Value") 
    device = comp[(currentdev-1)]
    return device

os.system('cls||clear')

@retry
def setdevice():
    global device
    device = searchselect()
    print("Selected Device: %s" % (device))

setdevice()
#try:
    

#except:
#    print("Port Unavailable")
def home():
    a = 0
    os.system('cls||clear')
    def info():
        print("NKBFWCPv1 - Keypad on %s Info" % device)
        print(" -Keys: %s\r\n" % devinfo["KEY"] 
             ,"-Matrix Configuration: %s X %s\r\n" % (devinfo["COL"],devinfo["ROW"])
             ,"-LED: %s\r\n" % devinfo["LED"]
             ,"-RGB: %s\r\n" % devinfo["RGB"])
        print("Option"
             ,"\n1.List All Key"
             ,"\n2.Change Key"
             ,"\n3.Change RGB Color"
             ,"\n4.Revert to Default Key"
             ,"\n5.Revert to Default RGB Color"
             ,"\n6.Exit")
        
        
    
    while not a in range(1,7):
        os.system('cls||clear')
        info()
        a = prompt.integer(prompt="Enter number (1-6):" )
            
    if a == 1:
        listkey()
    elif a == 2:
        print(2)
    elif a == 3:
        print(3)
    elif a == 6:
        exit()

def listkey():
    os.system('cls||clear')
    ser.write(b'KI')
    kall = ser.readline().decode("ascii", "ignore").split("|")
    for i in range(len(kall)-1):
        buff = kall[i].split(",")
        for j in range(len(buff)):
            if int(buff[j]) < 127:
                buff[j] = chr(int(buff[j]))
            else:
                buff[j] = arduinoascii[buff[j]]
        print(buff)
    print("Press Any Key To Continue...")
    input()
    home()

with serial.Serial(device, 9600, timeout=5) as ser:
        print("Pinging %s..." % ser.name)
        ser.write(b'PG')
        pver = int(ser.readline().decode("ascii", "ignore"))
        if not pver == 1:
            raise Exception("Port Busy")
        ser.write(b'IN')
        keyin = ser.readline().decode("ascii", "ignore").split(",")
        datain = ser.readline().decode("ascii", "ignore").split(",")
        devinfo = dict(zip(keyin,datain))
        os.system('cls||clear')
        home()
        
