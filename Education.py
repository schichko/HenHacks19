#!/usr/bin/env python

#importing GUI Library
import Tkinter
#Importing stuff from Tkinter
from tkinter import *



class Application(Tkinter.Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.init_window()
    
    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH,expand = 1)
        quitButton = Button(self,text = "Quit",command = self.client_exit)
        quitButton.place(x=0,y=0)

    def client_exit(self):
        exit()



print("Hello");

print("John Has the Code x=3 right now, can you help John turn that x into a 4?");

#Sets up root to be a new Tkinter
root = Tk();
#Sets the size of the Window
root.geometry("400x300")
#Creates a new app with the root that we have created before
app = Application(root)
#Starts its loop
root.mainloop();

#Getting user input
Help_Input = raw_input("Enter your code : ");
print(Help_Input);

#Splitting a String based on
Help_Input_Split = Help_Input.split(" ")

if(Help_Input == "123"):
    print(Help_Input + 2);

# for(Help_Input.)

