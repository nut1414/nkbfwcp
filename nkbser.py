# nkbser.py
import os
import serial
import serial.tools.list_ports
from retrying import retry


global device
device =0
def searchselect():
    global device
    comp = [comport.device for comport in serial.tools.list_ports.comports()]
    manu = [comport.manufacturer for comport in serial.tools.list_ports.comports()]
    devicecount = len(comp)
    devicelist = { i + 1 : comp[i] for i in range(0,devicecount)}
    print("%d Port(s) Detected " % (len(devicelist))) 
    print("Enter 0 to reload")

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
try:
    with serial.Serial(device, 9600, timeout=5) as ser:
        print("Pinging %s..." % ser.name)
        ser.write(b'PG')
        if not int(ser.readline().decode("ascii", "ignore")) == 1:
            raise Exception("Port Busy")
        ser.write(b'IN')
        keyin = ser.readline().decode("ascii", "ignore").split(",")
        datain = ser.readline().decode("ascii", "ignore").split(",")
        devinfo = dict(zip(keyin,datain))
        
        print(devinfo)
        print(datain)

except:
    print("Port Unavailable")
