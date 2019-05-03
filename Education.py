#!/usr/bin/env python
import tkinter
import time

def dnd_start(source, event):
    h = DndHandler(source, event)
    if h.root:
        return h
    else:
        return None


##DND HANDLER (Found online)
class DndHandler:

    root = None

    def __init__(self, source, event):
        if event.num > 5:
            return
        root = event.widget._root()
        try:
            root.__dnd
            return # Don't start recursive dnd
        except AttributeError:
            root.__dnd = self
            self.root = root
        self.source = source
        self.target = None
        self.initial_button = button = event.num
        self.initial_widget = widget = event.widget
        self.release_pattern = "<B%d-ButtonRelease-%d>" % (button, button)
        self.save_cursor = widget['cursor'] or ""
        widget.bind(self.release_pattern, self.on_release)
        widget.bind("<Motion>", self.on_motion)
        widget['cursor'] = "hand2"

    def __del__(self):
        root = self.root
        self.root = None
        if root:
            try:
                del root.__dnd
            except AttributeError:
                pass

    def on_motion(self, event):
        x, y = event.x_root, event.y_root
        target_widget = self.initial_widget.winfo_containing(x, y)
        source = self.source
        new_target = None
        while target_widget:
            try:
                attr = target_widget.dnd_accept
            except AttributeError:
                pass
            else:
                new_target = attr(source, event)
                if new_target:
                    break
            target_widget = target_widget.master
        old_target = self.target
        if old_target is new_target:
            if old_target:
                old_target.dnd_motion(source, event)
        else:
            if old_target:
                self.target = None
                old_target.dnd_leave(source, event)
            if new_target:
                new_target.dnd_enter(source, event)
                self.target = new_target

    def on_release(self, event):
        self.finish(event, 1)

    def cancel(self, event=None):
        self.finish(event, 0)

    def finish(self, event, commit=0):
        target = self.target
        source = self.source
        widget = self.initial_widget
        root = self.root
        try:
            del root.__dnd
            self.initial_widget.unbind(self.release_pattern)
            self.initial_widget.unbind("<Motion>")
            widget['cursor'] = self.save_cursor
            self.target = self.source = self.initial_widget = self.root = None
            if target:
                if commit:
                    target.dnd_commit(source, event)
                else:
                    target.dnd_leave(source, event)
        finally:
            source.dnd_end(target, event)



##The Class for my exit Button
class Button:
    p1_a1 = 0
    p1_a2 = 0
    p1_a3 = 0
    a1_a1 = 0
    a1_a2 = 0
    a1_a3 = 0
    #Names it whatever Name We pass in for it
    def __init__(self, name):
        #Set that name
        self.name = name
        print("Self.Name:",self.name)
        self.canvas = self.label = self.id = None

    #This actually Attaches it to the Canvas (The X and Y can be overriden but these are the default values)
    def attach(self, canvas, x=10, y=30):
        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return

        #Actually Creates the Exit Button
        if(self.name == "EXIT"):
            print("Exit")
            ExitButton = tkinter.Button(canvas,text = "Exit",command = self.exit)
            id = canvas.create_window(x, y, window=ExitButton, anchor="nw")
            self.canvas = canvas
            self.id = id
            
        elif(self.name == "Problem 1"):
            print("TEST1")
            Problem1Button = tkinter.Button(canvas,text = "Problem 1",command = self.problem_1)
            id = canvas.create_window(x, y, window=Problem1Button, anchor="nw")
            self.canvas = canvas
            self.id = id

    def exit(self):
        exit()

    def problem_1(self):
        self.p1_a1 = Possible_Answer("X",1)
        self.p1_a1.attach(self.canvas,50,300)
        self.p1_a2 = Possible_Answer("=",2)
        self.p1_a2.attach(self.canvas,100,300)
        self.p1_a3 = Possible_Answer("4",3)
        self.p1_a3.attach(self.canvas,150,300)
        self.a1_a1 = Answer_Box("1",1,self.p1_a1,self.p1_a2,self.p1_a3)
        self.a1_a1.attach(self.canvas,50,350)
        # self.a1_a2 = Answer_Box("2",2,self.p1_a1,self.p1_a2,self.p1_a3)
        # self.a1_a2.attach(self.canvas,100,350)
        # self.a1_a3 = Answer_Box("3",3,self.p1_a1,self.p1_a2,self.p1_a3)
        # self.a1_a3.attach(self.canvas,150,350)
        print(self.p1_a1.get_y())
        self.a1_a1.check_Boxes()
        #time.sleep(1)


        
class Possible_Answer:
    x=0
    y=0
    def __init__(self, name, correctSpot):
        self.name = name
        self.correctSpot = correctSpot
        self.canvas = self.label = self.id = None

    def attach(self, canvas, x=10, y=10):
        self.x = x
        self.y = y
        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return
        label = tkinter.Label(canvas, text=self.name,
                              borderwidth=2, relief="raised")
        id = canvas.create_window(x, y, window=label, anchor="nw")
        self.canvas = canvas
        self.label = label
        self.id = id
        label.bind("<ButtonPress>", self.press)

    def detach(self):
        canvas = self.canvas
        if not canvas:
            return
        id = self.id
        label = self.label
        self.canvas = self.label = self.id = None
        canvas.delete(id)
        label.destroy()

    def press(self, event):
        if dnd_start(self, event):
            # where the pointer is relative to the label widget:
            self.x_off = event.x
            self.y_off = event.y
            # where the widget is relative to the canvas:
            self.x_orig, self.y_orig = self.canvas.coords(self.id)

    def move(self, event):
        x, y = self.where(self.canvas, event)
        self.canvas.coords(self.id, x, y)

    def putback(self):
        self.canvas.coords(self.id, self.x_orig, self.y_orig)

    def where(self, canvas, event):
        # where the corner of the canvas is relative to the screen:
        x_org = canvas.winfo_rootx()
        y_org = canvas.winfo_rooty()
        # where the pointer is relative to the canvas widget:
        x = event.x_root - x_org
        y = event.y_root - y_org
        # compensate for initial pointer offset
        return x - self.x_off, y - self.y_off

    def dnd_end(self, target, event):
        pass
    
    def get_x(self):
        print(self.x)
        return self.x

    def get_y(self):
        print(self.y)
        return self.y

        
class Answer_Box:
    x=0
    y=0
    def __init__(self, name, number,test1,test2,test3):
        self.name = name
        self.number = number
        self.test1 = test1
        self.test2 = test2
        self.test3 = test3
        self.canvas = self.label = self.id = None


    def attach(self, canvas, x=10, y=10):
        self.x = x
        self.y = y
        if canvas is self.canvas:
            self.canvas.coords(self.id, x, y)
            return
        if self.canvas:
            self.detach()
        if not canvas:
            return
        label = tkinter.Label(canvas, text=self.name,
                              borderwidth=2, relief="raised")
        id = canvas.create_window(x, y, window=label, anchor="nw")
        self.canvas = canvas
        self.label = label
        self.id = id
        
    def get_x(self):
        print(self.x)
        return self.x

    def get_y(self):
        print(self.y)
        return self.y

    def check_Boxes(self):
        print("In Check Boxes")
        if(self.y == self.test1.get_y()):
            print("Collision")
        else:
            print("heere")
            self.check_Boxes
            




class Tester:

    def __init__(self, root):
        self.top = tkinter.Toplevel(root)
        self.canvas = tkinter.Canvas(self.top, width=400, height=400)
        self.canvas.pack(fill="both", expand=1)
        self.canvas.dnd_accept = self.dnd_accept

    def dnd_accept(self, source, event):
        return self

    def dnd_enter(self, source, event):
        self.canvas.focus_set() # Show highlight border
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = source.canvas.bbox(source.id)
        dx, dy = x2-x1, y2-y1
        self.dndid = self.canvas.create_rectangle(x, y, x+dx, y+dy)
        self.dnd_motion(source, event)

    def dnd_motion(self, source, event):
        x, y = source.where(self.canvas, event)
        x1, y1, x2, y2 = self.canvas.bbox(self.dndid)
        self.canvas.move(self.dndid, x-x1, y-y1)

    def dnd_leave(self, source, event):
        self.top.focus_set() # Hide highlight border
        self.canvas.delete(self.dndid)
        self.dndid = None

    def dnd_commit(self, source, event):
        self.dnd_leave(source, event)
        x, y = source.where(self.canvas, event)
        source.attach(self.canvas, x, y)



def test():
    #Starting the root as a tkinter window
    root = tkinter.Tk()
    #root.geometry("+1+1")
    root.withdraw()
    #Main Game Canvas
    t1 = Tester(root)
    t1.top.geometry("+1+80")

    b1 = Button("EXIT")
    b1.attach(t1.canvas,200,200)

    print("HERE")
    b2 = Button("Problem 1")
    b2.attach(t1.canvas,10,0)

    

    root.mainloop()




#Run Game
test()