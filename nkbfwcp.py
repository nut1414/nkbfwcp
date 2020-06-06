import os
import sys
from tkinter import *
from tkinter import messagebox
import nkbser as nkbser
import sys


root = Tk()
global device
device = ""

deviceroot = nkbser.deviceList()
connect = nkbser.connect()
devtextinfo = StringVar()



if hasattr(sys, '_MEIPASS'):
        icopath = os.path.join(sys._MEIPASS, "f.ico")
else:
        icopath =  os.path.join(os.path.abspath("."), "f.ico")



def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        try:
            root.destroy()
        except:
            pass
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
        parent.iconbitmap(icopath)
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
        self.parent.title("nkbfwcp")
        self.parent.iconbitmap(icopath)
        self.parent.iconbitmap(default=icopath)
        self.selectionmenu()
        self.chooseDevice()
    

    def selectionmenu(self):
        self.menutab = Menu(root)
        self.submenu1 = Menu(self.menutab,tearoff=False)
        self.submenu1.add_command(label="Reselect Device",command=self.deleteScene)
        self.submenu1.add_separator()
        self.submenu1.add_command(label="Revert Keys to Default",command=lambda : self.keydata.revertkey(self.keydata.name))
        self.submenu1.add_command(label="Revert LEDs to Default",command=lambda : self.keydata.revertrgb(self.keydata.name))
        self.submenu1.add_command(label="Revert All Setting to Default",command=lambda : self.keydata.revertall(self.keydata.name))
        self.submenu1.add_separator()
        self.submenu1.add_command(label="Exit",command=on_closing)
        self.menutab.add_cascade(label="Device",menu=self.submenu1)
        self.menutab.add_command(label="Refresh",command=lambda : self.keydata.updateinfo(self.keydata.name))
        root.config(menu=self.menutab)
        pass



    def chooseDevice(self):
        self.menutab.entryconfig("Refresh",state="disabled")
        self.submenu1.entryconfig("Reselect Device",state="disabled")
        self.submenu1.entryconfig("Revert Keys to Default",state="disabled")
        self.submenu1.entryconfig("Revert LEDs to Default",state="disabled")
        self.submenu1.entryconfig("Revert All Setting to Default",state="disabled")
        self.connecttext = Label(self.parent,text="Waiting for Device...")
        self.connecttext.grid(sticky=N,padx=50,pady=50)
        self.chDev = Toplevel(self.parent)
        deviceChooser(self.chDev)
        self.chDev.wait_window()
        
        self.selecteddevice = device
        self.setScene(self.selecteddevice)

    def setScene(self, name):
        try:
            self.submenu1.entryconfig("Reselect Device",state="normal")
            self.submenu1.entryconfig("Revert Keys to Default",state="normal")
            self.submenu1.entryconfig("Revert LEDs to Default",state="normal")
            self.submenu1.entryconfig("Revert All Setting to Default",state="normal")
            self.menutab.entryconfig("Refresh",state="normal")
            print("\nvalidating")
            isserial = connect.openSerial(name)
            self.connecttext.destroy()
            try:
                if isserial:
                    print(isserial)
                    self.deviceinfo = connect.updateSerial(name) 
                    self.textframe = LabelFrame(self.parent,text="{} on {}".format(self.deviceinfo["NAME"],name))
                    self.textframe.grid(sticky=N)
                    #temp \/
                    devtextinfo.set("Keys: {},Matrix Configuration: {}x{},LED: {},RGB: {}".format(self.deviceinfo["KEY"],self.deviceinfo["COL"],self.deviceinfo["ROW"],self.deviceinfo["LED"],self.deviceinfo["RGB"]))
                    self.text2 = Label(self.textframe,textvariable=devtextinfo)
                    self.text2.grid(row=2)
                    self.keydata = keyFrame(self.textframe,name,self.deviceinfo)
                    
                    self.keydata.grid(row=1)
                else:
                    print(isserial)
                    raise Exception("Unable to Connect to the Device.")
            except Exception as e:
                print(e)
                print(isserial)
                self.deleteScene()
        except:
            pass

    def deleteScene(self):
        try:
            slavelist = root.grid_slaves()
            for i in slavelist:
                i.destroy()
            pass
            self.chooseDevice()
        except:
            pass
        pass

class keyFrame(Frame):
    def __init__(self,parent,name,info):
        super(keyFrame, self).__init__()
        Frame.__init__(self, parent)
        self.parent = parent
        self.deviceinfo = info
        self.name = name
        self.keychar = connect.retrieveKey(self.name)
        row = len(self.keychar)
        col = len(self.keychar[0])
        self.keycharlabel = LabelFrame(self,text="Config")
        self.rgbcharlabel = LabelFrame(self.keycharlabel,text="RGB")
        self.keycharlabel.grid(sticky=N)
        self.rgbcharlabel.grid(row=2,column=3)

        self.rowboxframe = Frame(self.keycharlabel)
        self.colboxframe = Frame(self.keycharlabel)
        self.rowscroll = Scrollbar(self.rowboxframe)
        self.colscroll = Scrollbar(self.colboxframe)
        self.rowlabel = Label(self.keycharlabel,text='Row')
        self.collabel = Label(self.keycharlabel,text='Column')
        self.rowbox = Listbox(self.rowboxframe,selectmode=BROWSE,yscrollcommand=self.rowscroll.set)
        self.colbox = Listbox(self.colboxframe,selectmode=BROWSE,yscrollcommand=self.colscroll.set)
        self.rowscroll.configure(command=self.rowbox.yview)
        self.colscroll.configure(command=self.colbox.yview)
        self.currentrow = [0]
        self.currentcol = [0]
        self.currentkey = [0]
        self.setkeyframe = Frame(self.keycharlabel)
        
        self.keychboxframe = Frame(self.setkeyframe)
        self.keychscroll = Scrollbar(self.keychboxframe)
        self.keychooser = Listbox(self.keychboxframe,height=8,selectmode=BROWSE,yscrollcommand=self.keychscroll.set)
        self.keychscroll.configure(command=self.keychooser.yview)
        self.keysetbutton = Button(self.setkeyframe,text='Set Key',state='disabled',command=lambda : self.setkey(self.name,self.selrow-1,self.selcol-1,self.keychooser.get(ACTIVE)))
        self.keychboxframe.grid(row=1,column=1)
        self.keychscroll.grid(row=1,column=2,sticky=NS)
        self.keychooser.grid(row=1,column=1)
        self.keysetbutton.grid(row=2,column=1,sticky=N,pady=1)
        self.setkeyframe.grid(row=2,column=2)
        
        self.keydictlistupdate()
        self.r = IntVar()
        self.g = IntVar()
        self.b = IntVar()
        self.rgbcanvas =Canvas(self.rgbcharlabel,height=15,width=15)
        self.rlabel = Label(self.rgbcharlabel,text='  R')
        self.glabel = Label(self.rgbcharlabel,text='  G')
        self.blabel = Label(self.rgbcharlabel,text='  B')
        self.rscale = Scale(self.rgbcharlabel,variable=self.r,from_=255,to=0,length=125,)
        self.gscale = Scale(self.rgbcharlabel,variable=self.g,from_=255,to=0,length=125)
        self.bscale = Scale(self.rgbcharlabel,variable=self.b,from_=255,to=0,length=125)
        self.rgbsetbutton = Button(self.rgbcharlabel,text="Set RGB",command=lambda : self.setrgb(self.name,self.r.get(),self.g.get(),self.b.get()))
        
        self.keyselectedtext = StringVar(self.keycharlabel)
        self.currentkeyupdate()
        
        self.keyselectedlabel = Label(self.keycharlabel,textvariable=self.keyselectedtext)
        self.keyselectedlabel.grid(row=1,column=2)
        
        self.rowboxframe.grid(row=2,column=0)
        self.colboxframe.grid(row=2,column=1)
        self.rowscroll.grid(row=1,column=1,sticky=NS)
        self.colscroll.grid(row=1,column=1,sticky=NS)
        self.rowlabel.grid(row=1,column=0,sticky=S)
        self.collabel.grid(row=1,column=1,sticky=S)
        self.rowbox.grid(row=1,column=0)
        self.colbox.grid(row=1,column=0)
        self.rlabel.grid(row=1,column=1)
        self.glabel.grid(row=1,column=2)
        self.blabel.grid(row=1,column=3)
        self.rgbcanvas.grid(row=3,column=2)
        self.rscale.grid(row=2,column=1,sticky=W)
        self.gscale.grid(row=2,column=2,sticky=W)
        self.bscale.grid(row=2,column=3,sticky=W)
        self.rgbsetbutton.grid(row=3,column=3)
        self.updateinfo(self.name)

        if int(self.deviceinfo["LED"]) == 0:
            self.rscale.config(state="disabled")
            self.gscale.config(state="disabled")
            self.bscale.config(state="disabled")
            self.rgbsetbutton.config(state="disabled")
            pass
        self.rowupdate()
        self.selectonce = False
        self.updatergbcanvas()
        self.rowpoll()
        self.colpoll()
        self.keypoll()


    def rowpoll(self):
        rowselect = self.rowbox.curselection()
        if rowselect != self.currentrow:
            
            try:
                self.colupdate(rowselect[0])
                self.currentrow = rowselect
                self.selectonce = True
                print('selected {}'.format(self.currentrow[0]+1))

                self.currentkeyupdate()
            except :
                
                pass
            
        self.after(250, self.rowpoll)
    def colpoll(self):
        colselect = self.colbox.curselection()
        
        if colselect != self.currentcol:
            try:
                self.currentcol = colselect
                print('selected {}'.format(self.currentcol[0]+1))
                self.currentkeyupdate()
            except:
                
                pass
        self.after(100, self.colpoll)

    def keypoll(self):
        keyselect = self.keychooser.curselection()
        if keyselect != ():
            try:
                self.currentkey = keyselect
                self.selectonce = True
            except:
                
                pass
        if self.selectonce:
            self.keysetbutton.config(state='normal')
            pass
        self.after(100, self.keypoll)

    def rowupdate(self):
        self.rowbox.delete(0,END)
        for i in range(len(self.keychar)):
            self.rowbox.insert(i,*str(i+1))
            pass
        pass

    def colupdate(self,row):
        self.colbox.delete(0,END)
        for i in range(len(self.keychar[row])):
            text = "{}|{} - {}".format(row+1,i+1,self.keychar[row][i])
            self.colbox.insert(i,text)

    def keydictlistupdate(self):
        self.keychooser.delete(0,END)
        x=0
        for i in nkbser.arduinoascii.keys():
            self.keychooser.insert(x,nkbser.arduinoascii[i])
            x+=1


    def currentkeyupdate(self):
        self.selrow = int(self.currentrow[0])+1
        self.selcol = int(self.currentcol[0])+1
        self.keyselectedtext.set("Currently Selected  Row: {}  Column: {}".format(self.selrow, self.selcol))

    def setrgb(self,name,r,g,b):
        self.waitpopup("Sending Information...")
        try:
            connect.sendrgb(name,r,g,b)
            self.killpopup()
            self.updateinfo(name)
            
        except:
            mainwin.deleteScene()
        

    def setkey(self,name,row,col,key):
        self.waitpopup("Sending Information...")
        try:
            convertedkey = nkbser.reverseddict[key]
            connect.sendkey(name,row,col,convertedkey)
            self.killpopup()
            self.updateinfo(name)
        except:
            mainwin.deleteScene()
        
        pass


    def revertkey(self,name):
        connect.defaultkey(name)
        self.updateinfo(name)
    def revertrgb(self,name):
        connect.defaultrgb(name)
        self.updateinfo(name)
        
    def revertall(self,name):
        self.revertkey(name)
        self.revertrgb(name)

    def updateinfo(self,name):
        print("\nupdating info")
        print("reconnecting")
        
        try:
            self.waitpopup("Updating Information...")
            self.deviceinfo = connect.updateSerial(self.name)
            devtextinfo.set("Keys: {},Matrix Configuration: {}x{},LED: {},RGB: {}".format(self.deviceinfo["KEY"],self.deviceinfo["COL"],self.deviceinfo["ROW"],self.deviceinfo["LED"],self.deviceinfo["RGB"]))
            rgbvalue = self.deviceinfo["RGB"].split("|")
            self.keychar = connect.retrieveKey(self.name)
            self.rowupdate()
            self.colupdate(self.currentrow[0])
            self.r.set(int(rgbvalue[0]))
            self.g.set(int(rgbvalue[1]))
            self.b.set(int(rgbvalue[2]))
        except Exception as e:
            print(e)
            mainwin.deleteScene()
        self.killpopup()

    def updatergbcanvas(self):
        htmlcolor = "#{0:02x}{1:02x}{2:02x}".format(self.r.get(),self.g.get(),self.b.get())
        self.rgbcanvas.config(bg=htmlcolor)
        self.after(50, self.updatergbcanvas)

    def waitpopup(self,msg):
        self.pop = Toplevel(self)
        self.pop.text = Label(self.pop,text=msg)
        self.pop.text.pack(padx=30,pady=10)
        self.pop.textwait = Label(self.pop,text="Please Wait...")
        self.pop.textwait.pack(padx=30,pady=10)
        self.pop.attributes('-disabled', True)

        while (not self.pop.winfo_ismapped()):
            self.pop.update()
            pass
        
    def killpopup(self):
        self.pop.destroy()
        pass
    

    

    
        
    




root.resizable(0,0)

root.protocol("WM_DELETE_WINDOW", on_closing)

mainwin = controlPanel(root)

root.mainloop()