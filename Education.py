#!/usr/bin/env python

#importing GUI Library
import Tkinter
import time
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



        self.T = Text(root, height=20, width=30)
        self.T.place(x=30,y=50)
        self.T.insert(END, "Just a text Widget\nin two lines\n")
        self.T.config(state=DISABLED)

        self.sayHiButton = Button(self,text = "Say Hi",command = lambda: self.say_Hi(self.T))
        self.sayHiButton.pack(side="top")

        quitButton = Button(self,text = "Quit",command = self.client_exit)
        quitButton.place(x=0,y=0)

    def client_exit(self):
        ##Doing print in here prints to consol
        print("Goodbye")
        time.sleep(1)
        exit()
    def say_Hi(self,T):
        print("Say Hi")
        T.config(state = NORMAL)
        T.insert(END, "Just a text Widget\nin two lines\n")
        T.config(state=DISABLED)




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

