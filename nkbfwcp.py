from tkinter import *
from tkinter import messagebox
import nkbser as nkbser
import sys

root = Tk()
global device
device = ""


deviceroot = nkbser.deviceList()
connect = nkbser.connect()
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

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
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("nkbfw")
        self.parent.iconbitmap('f.ico')
        self.selectionmenu()
        self.chooseDevice()
        

    def selectionmenu(self):
        self.menutab = Menu(root)
        self.submenu = Menu(self.menutab,tearoff=False)
        self.submenu.add_command(label="Reselect Device",command=self.deleteScene)
        self.submenu.add_separator()
        self.submenu.add_command(label="Exit",command=on_closing)
        self.menutab.add_cascade(label="Device",menu=self.submenu)
        root.config(menu=self.menutab)
        pass



    def chooseDevice(self):
        self.submenu.entryconfig("Reselect Device",state="disabled")
        self.connecttext = Label(self.parent,text="Waiting for Device...")
        self.connecttext.grid(sticky=N,padx=50,pady=50)
        self.chDev = Toplevel(self.parent)
        deviceChooser(self.chDev)
        self.chDev.wait_window()
        
        self.selecteddevice = device
        self.setScene(self.selecteddevice)

    def setScene(self, name):
        self.submenu.entryconfig("Reselect Device",state="normal")
        isserial = connect.openSerial(name)
        self.connecttext.destroy()
        try:
            if isserial:
                print(isserial)
                self.deviceinfo = connect.updateSerial(name) 
                self.textframe = LabelFrame(self.parent,text="{} on {}".format(self.deviceinfo["NAME"],name))
                self.textframe.grid(sticky=N)
                #temp \/
                self.text2 = Label(self.textframe,text="Keys: {},Matrix Configuration: {}x{},LED: {},RGB: {}".format(self.deviceinfo["KEY"],self.deviceinfo["COL"],self.deviceinfo["ROW"],self.deviceinfo["LED"],self.deviceinfo["RGB"]))
                self.text2.grid(row=2)
                self.keydata = keyFrame(self.parent,name)
                self.keydata.grid(row=1)
            else:
                print(isserial)
                raise Exception("Unable to Connect to the Device.")
        except Exception as e:
            print(e)
            print(isserial)
            self.deleteScene()
            

    def deleteScene(self):
        try:
            slavelist = root.grid_slaves()
            for i in slavelist:
                print(i)
                i.destroy()
            pass
            self.chooseDevice()
        except:
            pass
        pass

class keyFrame(Frame):
    def __init__(self,parent,name):
        super(keyFrame, self).__init__()
        Frame.__init__(self, parent)
        self.parent = parent
        self.keychar = connect.retrieveKey(name)
        row = len(self.keychar)
        col = len(self.keychar[0])
        self.keycharlabel = LabelFrame(self,text="Key")
        self.keycharlabel.grid(sticky=N)
        self.rowbox = Listbox(self.keycharlabel,selectmode=BROWSE,takefocus=False,yscrollcommand=True)
        self.currentrow = [0]
        self.currentcol = [0]
        self.keyselectedtext = StringVar(self.keycharlabel)
        self.keyselectedtext.set("Currently Selected Row: 0  Column: 0")
        self.keyselectedlabel = Label(self.keycharlabel,textvariable=self.keyselectedtext)
        self.keyselectedlabel.grid(row=1,column=2,padx=10)
        self.rowlabel = Label(self.keycharlabel,text='Row')
        self.collabel = Label(self.keycharlabel,text='Column')
        self.rowlabel.grid(row=1,column=0)
        self.collabel.grid(row=1,column=1)
        self.colbox = Listbox(self.keycharlabel,selectmode=BROWSE,yscrollcommand=True)
        self.rowbox.grid(row=2,column=0,pady=10)
        self.colbox.grid(row=2,column=1,)
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
            
        self.after(100, self.colpoll)
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

        

    
        
    







root.protocol("WM_DELETE_WINDOW", on_closing)

mainwin = controlPanel(root)

root.mainloop()