from tkinter import *
from tkinter import messagebox
import nkbser as nkbser
import sys

root = Tk()
global device
device = ""

deviceroot = nkbser.deviceList()
connect = nkbser.connect()
root.geometry("400x400")
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
        sellist.delete(0,END)
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
        super(controlPanel, self).__init__()
        global device
        self.parent = parent
        self.parent.title("nkbfw")
        self.parent.iconbitmap('f.ico')
        
        self.chooseDevice()
        
    def chooseDevice(self):
        chDev = Toplevel(self.parent)
        deviceChooser(chDev)
        chDev.wait_window()
        self.selecteddevice = device
        
        self.setScene(self.selecteddevice)
    def setScene(self, name):
        self.isserial = connect.openSerial(name)
    #try:
        if self.isserial :
            self.deviceinfo = connect.updateSerial(name) 
            self.text = Label(self.parent,text="{} on {}".format(self.deviceinfo["NAME"],name))
            self.text.grid(row=0)
            #temp \/
            self.text2 = Label(self.parent,text="Keys: {},Matrix Configuration: {}x{},LED: {},RGB: {}".format(self.deviceinfo["KEY"],self.deviceinfo["COL"],self.deviceinfo["ROW"],self.deviceinfo["LED"],self.deviceinfo["RGB"]))
            self.text2.grid(row=2)
            self.keydata = keyFrame(self.parent,name)
            self.keydata.grid(row=1)
        else:
            raise Exception("Device Connection Failed")
    #except:
        
        #self.chooseDevice()


class keyFrame(Frame):
    def __init__(self,parent,name):
        super(keyFrame, self).__init__()
        self.parent = parent
        self.keychar = connect.retrieveKey(name)
        row = len(self.keychar)
        col = len(self.keychar[0])
        self.keycharlabel = Label(self,text="{}  , Count {}x{}".format(self.keychar, col, row))
        self.keycharlabel.grid(row=1,column=0,padx=10)
        self.rowbox = Listbox(self,selectmode=BROWSE,takefocus=False)
        self.currentrow = None
        self.colbox = Listbox(self,selectmode=BROWSE,takefocus=False)
        self.rowbox.grid(row=2,column=0)
        self.colbox.grid(row=2,column=1)
        self.rowupdate()
        self.rowpoll()
        
    def rowpoll(self):
        nowselect = self.rowbox.curselection()
        if nowselect != self.currentrow:
            try:
                self.colupdate(nowselect[0])
            except Exception as e:
                print(nowselect)
                print(e)
                pass
            self.currentrow = nowselect
        self.after(250, self.rowpoll)
    def rowupdate(self):
        for i in range(len(self.keychar)):
            print(i+1)
            self.rowbox.insert(i,*str(i+1))
            pass
        pass
    def colupdate(self,row):
        print(len(self.keychar[row]))
        print(row)
        self.colbox.delete(0,END)
        for i in range(len(self.keychar[row])):
            text = "{}|{}  {}".format(row+1,i+1,self.keychar[row][i])
            self.colbox.insert(i,text)
            pass
        pass
    pass




def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()



root.protocol("WM_DELETE_WINDOW", on_closing)

mainwin = controlPanel(root)

root.mainloop()