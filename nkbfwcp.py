from tkinter import *
import tkinter.messagebox
import nkbser 
import sys

root = Tk()



deviceroot = nkbser.deviceList()
class deviceChooser(Frame):
    def __init__(self,parent):
        self.parent = parent
        parent.title('nkbfwcp')
        parent.geometry("225x255")
        parent.resizable(0,0)
        parent.iconbitmap('f.ico')
        print(deviceroot.deviceCount)
        self.devicestring = StringVar(parent)
        self.devText(self.devicestring,deviceroot.deviceCount)
        self.Introtext = Label(parent,text="Choose your device")
        self.devicetext = Label(parent,textvariable=self.devicestring,underline=9)
        self.devicepick = Listbox(parent,width=35)
        self.okbutton = Button(parent,text="OK",padx=15,command=sys.exit)
        self.updatebutton = Button(parent,text="Refresh",padx=15,command=lambda : self.updateList(self.devicepick))
        self.updateList(self.devicepick)
        self.Introtext.pack(side=TOP)
        self.devicetext.pack(side=TOP)
        self.devicepick.pack()
        self.okbutton.pack(fill=X,side=BOTTOM)
        self.updatebutton.pack(fill=X,side=BOTTOM)

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
    def devText(self,variable,number):
        variable.set("There is %d device(s) connected." % number)
        
    




windevchoose = deviceChooser(root)
root.mainloop()