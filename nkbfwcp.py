from tkinter import *
import tkinter.messagebox
import nkbser 

root = Tk()
deviceroot = nkbser.deviceList()
root.title('nkbfwcp')
root.geometry("500x500")
variable = StringVar(root)
print(deviceroot.deviceCount)

devicestring = "There is %d device(s) connected." % deviceroot.deviceCount

devicetext = Label(root,text=devicestring)
devicpick = OptionMenu(root,variable,*deviceroot.list)
devicebutton = Button(root,text="OK")
devicetext.pack()
devicpick.pack()
devicebutton.pack()
root.mainloop()
