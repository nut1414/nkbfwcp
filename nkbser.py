# nkbser.py

import os
import sys
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
                ,'255' : 'KEY_SPACE'
                ,'32' : 'SPACE'}


device = 0
reversedtable = None
os.system('color 17')

def searchselect():
    global device
    comp = [comport.device for comport in serial.tools.list_ports.comports()]
    manu = [comport.manufacturer for comport in serial.tools.list_ports.comports()]
    devicecount = len(comp)
    devicelist = { i + 1 : comp[i] for i in range(0,devicecount)}
    print("NKBFWCPv1 - Selecting Device")
    print("-%d Port(s) Detected- " % (len(devicelist))) 
    
    #print(arduinoascii)

    for number in range(devicecount):
        if ("Arduino" in manu[number]) == True:
            respondtext = " <- Most Likely Device"
        else:
            respondtext = " "
            pass
        print("%d.%s %s" % ((number+1) , comp[number] , respondtext))
    try:
        print("\nEnter 0 to reload")
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


def home():
    global devinfo
    a = 0
    update()
    os.system('cls||clear')
    
    def info():
        try:
            print("NKBFWCPv1 - %s on %s Info" % (devinfo["NAME"],device))
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
                 ,"\n6.Exit\n")
        except:
            update()
        
        
    
    while not a in range(1,7):
        os.system('cls||clear')
        info()
        a = prompt.integer(prompt="Enter number (1-6):" )
            
    if a == 1:
        listkey()
    elif a == 2:
        setkey()
    elif a == 3:
        setrgb()
    elif a == 4:
        defaultkey()
    elif a == 5:
        defaultrgb()
    elif a == 6:
        sys.exit()

def listkey():
    global converted
    converted = []
    os.system('cls||clear')
    print("Requesting Key List...")
    
    os.system('cls||clear')
    print("Key List 'Column|Row'\n")
    for i in range(len(retrivekey())):
        print(retrivekey()[i])
    print("\nPress Enter To Continue...")
    input()
    home()

def retrivekey():
    global converted
    converted = []
    try:
        ser.write(b'KI')
        kall = ser.readline().decode("ascii", "ignore").split("|")
    
        for i in range(len(kall)-1):
            buff = kall[i].split(",")
            for j in range(len(buff)):
                try:
                    if int(buff[j]) < 128:
                        buff[j] = '%d|%d:"%s"' % (j+1,i+1,chr(int(buff[j])) )
                    else:
                        buff[j] = '%d|%d:"%s"' % (j+1,i+1,arduinoascii[buff[j]])
                except:
                    buff[j] ="UNKNOWN"
            converted.append(buff)
    except Exception as e:
        print("Error: %s" % e)
        input()
            
    return converted

def defaultkey():
    try:
        os.system('cls||clear')
        print("Reverting to Default Key...")
        ser.write(b'DK')
        respond = ser.readline()
        print("Device: %s" % respond.decode("ascii", "ignore"))
        print("Saving Changes...")
        ser.write(b'SS')
        respond = ser.readline()
        print("Status: %s" % respond.decode("ascii", "ignore"))
        input("Press Enter to Continue...")
        home()
    except Exception as e:
        print("Error: %s" % e)
        input()
        home()

def defaultrgb():
    global devinfo
    os.system('cls||clear')
    if not int(devinfo["LED"] ) == 0:
        try:
            print("Reverting to Default RGB Values...")
            ser.write(b'DL')
            respond = ser.readline()
            print("Device: %s" % respond.decode("ascii", "ignore"))
            print("Saving Changes...")
            ser.write(b'SS')
            respond = ser.readline()
            print("Status: %s" % respond.decode("ascii", "ignore"))
            input("Press Enter to Continue...")
            home()
        except Exception as e:
            print("Error: %s" % e)
            input()
            home()
    else:
        input("No LED Detected...")
        home() 
    

def setkey():
    global devinfo
    global reversedtable
    ascii=0
    if not reversedtable : 
        reversedtable = {value:key for key, value in arduinoascii.items()}
        
    os.system('cls||clear')
    try:
        print("Change Key\n")
        print("Key List 'Column|Row'\n")
        for i in range(len(retrivekey())):
            print(retrivekey()[i])
        print("\nEnter nothing to return to home.")
        col = prompt.integer(prompt="Enter column:",empty=True)
        if not col:
            raise Exception("Returning Home...")
        elif not col in range(1,int(devinfo["COL"])+1):
            print("Please enter number in range of 1-%s." % (devinfo["COL"]))
            input()
            setkey()
        if int(devinfo["ROW"]) == 1:
            print("Enter row:1")
            row = 1
        else:
            row = prompt.integer(prompt="Enter row:",empty=True)
            if not row:
                raise Exception("Returning Home...")
            elif not row in range(1,int(devinfo["ROW"])+1):
                print("Please enter number in range of 1-%s." % (devinfo["ROW"]))
                input()
                setkey()
        key = prompt.string(prompt="Enter key:",empty=True)
        try:  
            ascii = ord(key)
            
        except:
            home()
        key.upper()
        try:
            if not key:
                raise Exception("Returning Home...")
            elif key in reversedtable:
           
                key = reversedtable[key]
                sendkey(col,row,int(key))
                home()
            
            elif ascii in range(1,128):
            
                sendkey(col,row,int(ord(key)))
                home()
            else:
                print("Please enter a valid key.")
                input()
                setkey()
        except:
            home()
        

    except Exception as e:
        print(e)
        home()
        
        

def sendkey(incol,inrow,inkey):
    '''
    pushing key change via the already opened serial
    '''
    try:
        print("\nSending Change..")
        cmd = "CK %d %d %d" %(incol-1 ,inrow-1 ,inkey)
        ser.write(bytearray(cmd,encoding="ascii"))
        print("Device: %s" % (ser.readline().decode("ascii", "ignore")))
        print("Saving Changes...")
        ser.write(b'SS')
        print("Status: %s" % (ser.readline().decode("ascii", "ignore")))
        input("Press Enter to Continue...")
        
    except Exception as e:
        print("Error: %s" % e)
        input()
        home()

    return




def setrgb():
    global devinfo
        
    os.system('cls||clear')
    if not int(devinfo["LED"] ) == 0:
        try:
            print("Change RGB\n")
            print("Current RGB Value: %s\n" % (devinfo["RGB"]))
            print("\nEnter nothing to return to home.")
            r = prompt.integer(prompt="Enter Red value:",empty=True)
            if not r:
                raise Exception("Returning Home...")
            elif not r in range(0,256):
                print("Please enter number in range of 0-255.")
                input()
                setrgb()
            g = prompt.integer(prompt="Enter Green value:",empty=True)
            if not g:
                raise Exception("Returning Home...")
            elif not g in range(0,256):
                print("Please enter number in range of 0-255.")
                input()
                setrgb()
            b = prompt.integer(prompt="Enter Blue value:",empty=True)
            if not b:
                raise Exception("Returning Home...")
            elif not b in range(0,256):
                print("Please enter number in range of 0-255.")
                input()
                setrgb()

            sendrgb(r,g,b)
            raise Exception("Returning Home...")
            

        except Exception as e:
            print(e)
            home()
    else:
        input("No LED Detected...")
        home()        
        

def sendrgb(inr,ing,inb):
    '''
    pushing rgb change via the already opened serial
    '''
    try:
        print("\nSending Change..")
        cmd = "LC %d %d %d" %(inr ,ing ,inb)
        ser.write(bytearray(cmd,encoding="ascii"))
        print("Device: %s" % (ser.readline().decode("ascii", "ignore")))
        print("Saving Changes...")
        ser.write(b'SS')
        print("Status: %s" % (ser.readline().decode("ascii", "ignore")))
        input("Press Enter to Continue...")
        
    except Exception as e:
        print("Error: %s" % e)
        input()
        home()

    return
def update():
    print("Retrieving %s Info..." % ser.name)
    global devinfo
    try:
        ser.write(b'IN')
        keyin = ser.readline().decode("ascii", "ignore").split(",")
        datain = ser.readline().decode("ascii", "ignore").split(",")
        devinfo = dict(zip(keyin,datain))
        os.system('cls||clear')
    except Exception as e:
        print("Error: %s" % e)
        input()
        

setdevice()

try:
    with serial.Serial(device, 9600, timeout=5) as ser:
        print("Pinging %s..." % ser.name)
        try: 
            ser.write(b'PG')
            pver = int(ser.readline().decode("ascii", "ignore"))
            if not pver == 1:
                raise Exception("Port Unknown")
        except Exception as e:
            print("Error: %s" % e)
            input()
            
        os.system('cls||clear')
        home()
        
except Exception as e:
    print("Error: %s" % e)
    input()