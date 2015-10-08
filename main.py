#!/usr/bin/python

from tkinter import *
from tkinter import ttk

from threading import Thread
import time

import yaml

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass
    
root = Tk()
root.title("Feet to Meters")
#root.geometry("170x200+30+30") 

ttk.Style().configure("TButton", padding=6, relief="flat",
   background="#595b59")

ttk.Style().configure("TEntry", padding=6, relief="flat",
   background="#595b59")

mainframe = ttk.Frame(root, padding="0 0 0 0")
#mainframe.geometry("170x200+30+30")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#mainframe.columnconfigure(0, weight=1)
#mainframe.rowconfigure(0, weight=1)

feet = StringVar()
meters = StringVar()

background_image=PhotoImage(file="images/potm_title.png").zoom(x = 1, y = 1)
background_label = Label(mainframe, image=background_image, borderwidth=0)
background_label.grid(row=0,column=0, rowspan=6, columnspan=6)

progress = ttk.Progressbar(mainframe)
progress.grid(row=4,column=0)

launch_button = ttk.Button(mainframe, text = 'Launch')
launch_button.grid(row=5,column=0)

nwn_path = StringVar()
nwn_path_entry = ttk.Entry(mainframe, textvariable=nwn_path)
nwn_path_entry.grid(row=5,column=2)
nwn_path.set("NWN url")

quit_button = ttk.Button(mainframe, text = "Quit")
quit_button.grid(row = 5, column = 5)
#stacy.place(x=0, y=0, relwidth=1, relheight=1)

#background_label.grid_configure()
#for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

test = 1

def sleeper(i):
    print ("thread %d sleeps for 5 seconds" % i)
    global test
    test = test + 1
    time.sleep(5)
    print ("thread %d woke up" % i)
    test = test + 1
    print(test)

for i in range(10):
    t = Thread(target=sleeper, args=(i,))
    t.start()

root.mainloop()