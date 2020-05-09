# nkbser.py

import serial
import serial.tools.list_ports



arduinoascii = {32: 'SPACE',
                33: '!',
                34: '"',
                35: '#',
                36: '$',
                37: '%',
                38: '&',
                39: "'",
                40: '(',
                41: ')',
                42: '*',
                43: '+',
                44: ',',
                45: '-',
                46: '.',
                47: '/',
                48: '0',
                49: '1',
                50: '2',
                51: '3',
                52: '4',
                53: '5',
                54: '6',
                55: '7',
                56: '8',
                57: '9',
                58: ':',
                59: ';',
                60: '<',
                61: '=',
                62: '>',
                63: '?',
                64: '@',
                91: '[',
                92: '\\',
                93: ']',
                94: '^',
                95: '_',
                96: '`',
                97: 'a',
                98: 'b',
                99: 'c',
                100: 'd',
                101: 'e',
                102: 'f',
                103: 'g',
                104: 'h',
                105: 'i',
                106: 'j',
                107: 'k',
                108: 'l',
                109: 'm',
                110: 'n',
                111: 'o',
                112: 'p',
                113: 'q',
                114: 'r',
                115: 's',
                116: 't',
                117: 'u',
                118: 'v',
                119: 'w',
                120: 'x',
                121: 'y',
                122: 'z',
                123: '{',
                124: '|',
                125: '}',
                126: '~',
                128: 'LEFT_CTRL',
                129: 'LEFT_SHIFT',
                130: 'LEFT_ALT',
                131: 'LEFT_OS',
                132: 'RIGHT_CTRL',
                133: 'RIGHT_SHIFT',
                134: 'RIGHT_ALT',
                135: 'RIGHT_OS',
                176: 'RETURN',
                177: 'ESC',
                178: 'BACKSPACE',
                179: 'TAB',
                193: 'CAPS_LOCK',
                194: 'F1',
                195: 'F2',
                196: 'F3',
                197: 'F4',
                198: 'F5',
                199: 'F6',
                200: 'F7',
                201: 'F8',
                202: 'F9',
                203: 'F10',
                204: 'F11',
                205: 'F12',
                209: 'INSERT',
                210: 'HOME',
                211: 'PAGE_UP',
                212: 'DELETE',
                213: 'END',
                214: 'PAGE_DOWN',
                215: 'RIGHT_ARROW',
                216: 'LEFT_ARROW',
                217: 'DOWN_ARROW',
                218: 'UP_ARROW',
                255: 'KEY_EMPTY'}
                
reverseddict = {value:key for key, value in arduinoascii.items()}

    

class deviceList(object):
    def __init__(self):
        self.device = [comport.device for comport in serial.tools.list_ports.comports()]
        self.manufacturer  = [comport.manufacturer for comport in serial.tools.list_ports.comports()]
        self.deviceCount = len(self.device)
        listdev = { i + 1 : self.device[i] for i in range(0,self.deviceCount)}
        self.list ={value:key for key, value in listdev.items()}
    def update(self):
        self.device = [comport.device for comport in serial.tools.list_ports.comports()]
        self.manufacturer  = [comport.manufacturer for comport in serial.tools.list_ports.comports()]
        self.deviceCount = len(self.device)
        listdev = { i + 1 : self.device[i] for i in range(0,self.deviceCount)}
        self.list ={value:key for key, value in listdev.items()}

class connect(object):
    def openSerial(self,device):
        
        try:
            with serial.Serial(device, 9600, timeout=5) as ser:
                print("Pinging %s..." % ser.name)
                try: 
                    ser.write(b'PG')
                    pver = int(ser.readline().decode("ascii", "ignore"))
                    if not pver == 1:
                        raise Exception("Port Unknown")
                    else:
                        ser.close()
                        return 1
                except Exception as e:
                    return 0
                    print("Error: %s" % e)
                    
        except Exception as e:
            return 0
            print("Error: %s" % e)
            

    def updateSerial(self,device):
        print("Retrieving %s Info..." % device)
        with serial.Serial(device, 9600, timeout=5) as ser:
            try:
                ser.write(b'IN')
                keyin = ser.readline().decode("ascii", "ignore").split(",")
                datain = ser.readline().decode("ascii", "ignore").split(",")
                devinfo = dict(zip(keyin,datain))
                
                ser.close()
                return devinfo
            except Exception as e:
                print("Error: %s" % e)
        
    def retrieveKey(self,device):
        converted = []
        with serial.Serial(device, 9600, timeout=5) as ser:
            try:
                ser.write(b'KI')
                kall = ser.readline().decode("ascii", "ignore").split("|")
            
                for i in range(len(kall)-1):
                    buff = kall[i].split(",")
                    for j in range(len(buff)):
                        try:
                            '''
                            if int(buff[j]) < 128:
                                buff[j] = '%s' % (chr(int(buff[j])) )
                            else:
                            '''
                            buff[j] = '%s' % (arduinoascii[int(buff[j])])
                        except:
                            buff[j] ="UNKNOWN"
                    converted.append(buff)
            except Exception as e:
                print("Error: %s" % e)
        print("keylist {}".format(converted))
        
        print("keycount1 {}".format(len(converted[0])))
        return converted

    def sendrgb(self,device,inr,ing,inb):
        with serial.Serial(device, 9600, timeout=5) as ser:
            try:
                print("Sending RGB Change..")
                cmd = "LC %d %d %d" %(inr ,ing ,inb)
                print(cmd)
                ser.write(bytearray(cmd,encoding="ascii"))
                print("Device: %s" % (ser.readline().decode("ascii", "ignore")))
                print("Saving Changes...")
                ser.write(b'SS')
                print("Status: %s" % (ser.readline().decode("ascii", "ignore")))
                
            except Exception as e:
                print("Error: %s" % e)
                

            return
    def sendkey(self,device,inrow,incol,inkey):
        with serial.Serial(device, 9600, timeout=5) as ser:
            try:
                print("Sending Change..")
                cmd = "CK %d %d %d" %(incol ,inrow ,inkey)
                print(cmd)
                ser.write(bytearray(cmd,encoding="ascii"))
                print("Device: %s" % (ser.readline().decode("ascii", "ignore")))
                print("Saving Changes...")
                ser.write(b'SS')
                print("Status: %s" % (ser.readline().decode("ascii", "ignore")))
                
                
            except Exception as e:
                print("Error: %s" % e)
                
        

    def defaultkey(self,device):
        with serial.Serial(device, 9600, timeout=5) as ser:
            try:    
                print("Reverting to Default Key...")
                ser.write(b'DK')
                respond = ser.readline()
                print("Device: %s" % respond.decode("ascii", "ignore"))
                print("Saving Changes...")
                ser.write(b'SS')
                respond = ser.readline()
                print("Status: %s" % respond.decode("ascii", "ignore"))
            except Exception as e:
                print("Error: %s" % e)
                
    def defaultrgb(self,device):
        with serial.Serial(device, 9600, timeout=5) as ser:
            try:
                print("Reverting to Default RGB Values...")
                ser.write(b'DL')
                respond = ser.readline()
                print("Device: %s" % respond.decode("ascii", "ignore"))
                print("Saving Changes...")
                ser.write(b'SS')
                respond = ser.readline()
                print("Status: %s" % respond.decode("ascii", "ignore"))
            except Exception as e:
                print("Error: %s" % e)
                
        



