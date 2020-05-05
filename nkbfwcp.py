from tkinter import *
from tkinter import messagebox
import nkbser as nkbser
import sys

root = Tk()
global device
device = ""

deviceroot = nkbser.deviceList()
connect = nkbser.connect()
#root.geometry("570x250")
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
        print("count {}".format(deviceroot.deviceCount))
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
        print("count {}".format(deviceroot.deviceCount))
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
            print("device {}".format(device))
        else:
            print("device {}".format(device))
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
            self.text.grid(sticky=N)
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
        self.currentrow = [0]
        self.currentcol = [0]
        self.keyselectedtext = StringVar(self)
        self.keyselectedtext.set("Currently Selected Row: 0  Column: 0")
        self.keyselectedlabel = Label(self,textvariable=self.keyselectedtext,padx=3)
        self.keyselectedlabel.grid(row=1,column=2,padx=10)
        self.colbox = Listbox(self,selectmode=BROWSE,takefocus=False)
        self.rowbox.grid(row=2,column=0)
        self.colbox.grid(row=2,column=1)
        self.rowupdate()
        self.selectonce = False
        self.rowpoll()
        self.colpoll()
        
    def rowpoll(self):
        rowselect = self.rowbox.curselection()
        if rowselect != self.currentrow:
            
            try:
                self.colupdate(rowselect[0])
                self.currentrow = rowselect
                self.selectonce = True
                print(self.currentrow)

                self.currentkeyupdate()
            except :
                
                pass
            
        self.after(250, self.rowpoll)
    def colpoll(self):
        colselect = self.colbox.curselection()
        if colselect != self.currentcol:
            try:
                self.currentcol = colselect
                print(self.currentcol)
                if self.selectonce == True:
                    self.currentkeyupdate()
            except:
                
                pass
            
        self.after(250, self.colpoll)
    def rowupdate(self):
        for i in range(len(self.keychar)):
            self.rowbox.insert(i,*str(i+1))
            pass
        pass
    def colupdate(self,row):
        self.colbox.delete(0,END)
        for i in range(len(self.keychar[row])):
            text = "{}|{} - {}".format(row+1,i+1,self.keychar[row][i])
            self.colbox.insert(i,text)
    def currentkeyupdate(self):
        self.keyselectedtext.set("Currently Selected Row: {}  Column: {}".format(int(self.currentrow[0])+1, int(self.currentcol[0])+1))

        

    
        
    




def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()



root.protocol("WM_DELETE_WINDOW", on_closing)

mainwin = controlPanel(root)

root.mainloop()