from tkinter import *
from tkinter import messagebox
import nkbser as nkbser
import sys

root = Tk()
global device
device = ""

deviceroot = nkbser.deviceList()
connect = nkbser.connect()
class deviceChooser(Frame):
    def __init__(self,parent):
        
        winWidth = parent.winfo_reqwidth()
        winHeight = parent.winfo_reqheight()
        posRight = int(root.winfo_screenwidth()/2 - winWidth/2)
        posnDown = int(root.winfo_screenheight()/2 - winHeight/1.25)
        self.parent = parent
        parent.title('nkbfwcp')
        parent.geometry("225x255+{}+{}".format(posRight,posnDown))
        parent.resizable(0,0)
        parent.iconbitmap('f.ico')
        print(deviceroot.deviceCount)
        self.devicestring = StringVar(parent)
        self.devText(self.devicestring,deviceroot.deviceCount)
        self.Introtext = Label(parent,text="Choose your device")
        self.devicetext = Label(parent,textvariable=self.devicestring,underline=9)
        self.devicepick = Listbox(parent,width=35)
        self.okbutton = Button(parent,text="OK",padx=15,command=self.setCurrentDevice)
        self.updatebutton = Button(parent,text="Refresh",padx=15,command=lambda : self.updateList(self.devicepick))
        self.updateList(self.devicepick)
        self.Introtext.pack(side=TOP)
        self.devicetext.pack(side=TOP)
        self.devicepick.pack()
        self.okbutton.pack(fill=X,side=BOTTOM)
        self.updatebutton.pack(fill=X,side=BOTTOM)
        self.parent.protocol("WM_DELETE_WINDOW", on_closing)

    def updateList(self,sellist):
        print(deviceroot.deviceCount)
        deviceroot.__init__()
        self.devText(self.devicestring,deviceroot.deviceCount)
        sellist.delete(0,1)
        for i in range(0,deviceroot.deviceCount):
            if "Arduino" in deviceroot.manufacturer[i]:
                inserttext = "%s <- Most Likely" % deviceroot.device[i]
            else:
                inserttext = deviceroot.device[i]
            sellist.insert(i,inserttext)
        self.devicepick.activate(0)
    def devText(self,variable,number):
        variable.set("There is %d device(s) connected." % number)
    def setCurrentDevice(self):
        global device
        device = self.devicepick.get(ACTIVE)
        devicein = device.find(" ")
        if not devicein == -1:
            device = device[0:devicein]
            print(device)
        else:
            print(device)
        self.parent.destroy()
        return device
        
        
    
    
class controlPanel(Frame):
    def __init__(self,parent): 
        global device
        self.parent = parent
        self.parent.title("nkbfw")
        self.parent.iconbitmap('f.ico')
        self.parent.geometry("300x300")
        self.chooseDevice()
        
    def chooseDevice(self):
        chDev = Toplevel(self.parent)
        deviceChooser(chDev)
        chDev.wait_window()
        self.selecteddevice = device
        
        self.setScene(self.selecteddevice)
    def setScene(self, name):
        self.isserial = connect.openSerial(name)
        
        if self.isserial :
            self.text = Label(self.parent,text="We are Connected on {}".format(name))
            self.text.pack()
            self.deviceinfo = connect.updateSerial(name) #temp \/
            self.text2 = Label(self.parent,text="Keys: {},Matrix Configuration: {}x{},LED: {},RGB: {}".format(self.deviceinfo["KEY"],self.deviceinfo["COL"],self.deviceinfo["ROW"],self.deviceinfo["LED"],self.deviceinfo["RGB"]))
            self.text2.pack()
        else:
            raise Exception("Failed to Connect to Device")
            self.chooseDevice()
            return
            




def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
mainwin = controlPanel(root)

root.mainloop()