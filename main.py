# from tkinter import Tk, RIGHT, BOTH, RAISED, Frame, Label, Button, Checkbutton, Entry, W, E, Listbox, END
from tkinter import *
import time as times
from pynput import mouse
import keyboard
from threading import Thread
from SimConf import SimConf

def pressMouse(cord):
    x, y = cord
    controller = mouse.Controller()
    controller.position = (x, y)
    controller.click(mouse.Button.left, 1)
    del controller

def sleepS(time):
    times.sleep(time)

def prnt(txt):
    keyboard.write(txt)

class App(Frame):

    def __init__(self):
        super().__init__()
        self.config = SimConf(default_atr = {"lines": []}, ensure_ascii=False)
        self.initUI()
        self.listener = mouse.Listener(on_move=self.cord)

    def start(self):
        def main():
            print("A"*50)
            self.stoop = True

            for command in self.config["lines"]:
                key, atr = tuple(command.items())[0]
                if self.stoop:
                    if key == "press":
                        pressMouse(atr)
                    elif key == "sleep":
                        sleepS(atr)
                    elif key == "prnt":
                        prnt(atr)
        Thread(target=main).start()

    def stop(self):
        self.stoop = False


    def Temps(self):
        temp = []
        for command in self.config["lines"]:
            key, atr = tuple(command.items())[0]
            temp.append(key+" : "+str(atr))
        return temp

    def cord(self, x, y):
        self.lblCord["text"] = f"x:{x} y:{y}"

    def addPress(self):
        x = int(self.ent00.get())
        y = int(self.ent01.get())
        self.config["lines"].append({"press": (x,y)})
        self.config.save()
        self.choicesvar.set(self.Temps())

    def addSleep(self):
        timeadd = int(self.ent1.get())
        self.config["lines"].append({"sleep": timeadd})
        self.config.save()
        self.choicesvar.set(self.Temps())

    def addWrite(self):
        txt = self.ent2.get()
        self.config["lines"].append({"prnt": txt})
        self.config.save()
        self.choicesvar.set(self.Temps())

    def remLast(self):
        self.config["lines"].pop(-1)
        self.config.save()
        self.choicesvar.set(self.Temps())



    def initUI(self):
        self.master.title("StepByStep")

        line = Frame(self)
        ####
        self.choicesvar = StringVar(value=self.Temps())
        libo = Listbox(line, listvariable=self.choicesvar)
        libo.grid(row=1, column=1, pady=5)
        ###
        btnStart = Button(line, text="Start", command=self.start)
        btnStart.grid(row=1, column=2, padx=5, pady=5)
        ###
        btnStop = Button(line, text="Stop", command=self.stop)
        btnStop.grid(row=1, column=3, padx=5, pady=5)
        ####

        control = Frame(self)
        ####
        tit0 = Label(control, text="Press")
        tit1 = Label(control, text="Sleep")
        tit2 = Label(control, text="Write")
        tit0.grid(row=1, column=1, padx=5, pady=1)
        tit1.grid(row=2, column=1, padx=5, pady=1)
        tit2.grid(row=3, column=1, padx=5, pady=1)
        ###
        self.ent00 = Entry(control)
        self.ent01 = Entry(control)
        self.ent1 = Entry(control)
        self.ent2 = Entry(control)
        self.ent00.grid(row=1, column=2)
        self.ent01.grid(row=1, column=3)
        self.ent1.grid(row=2, column=2, columnspan=2, sticky=W+E)
        self.ent2.grid(row=3, column=2, columnspan=2, sticky=W+E)
        ###
        btn0 = Button(control, text="add", command=self.addPress)
        btn1 = Button(control, text="add", command=self.addSleep)
        btn2 = Button(control, text="add", command=self.addWrite)
        btn0.grid(row=1, column=4, padx=5, pady=1)
        btn1.grid(row=2, column=4, padx=5, pady=1)
        btn2.grid(row=3, column=4, padx=5, pady=1)
        ###
        btnr = Button(control, text="remove last", command=self.remLast)
        btnr.grid(row=1, column=5, padx=5, pady=1)
        ##
        self.lblCord = Label(control, text="x:0 y:0")
        self.lblCord.grid(row=2, column=5, padx=5, pady=1)
        ##
        self.var = BooleanVar()
        self.chec = Checkbutton(control, text="listen", variable=self.var, command=self.onClick)
        self.chec.grid(row=3, column=5, padx=5, pady=1)
        ####

        line.grid(row=0, column=0)
        control.grid(row=1, column=0)

        self.pack()

    def onClick(self):
        if self.var.get():
            self.listener.start()
        else:
            self.listener.stop()
            self.listener = mouse.Listener(on_move=self.cord)


def main():
    root = Tk()
    root.attributes("-topmost",True)
    app = App()

    root.mainloop()


if __name__ == '__main__':
    main()
