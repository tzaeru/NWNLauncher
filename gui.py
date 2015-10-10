from tkinter import *
from tkinter import ttk

from threading import Thread
import time

import yaml

import path_finder

import os, subprocess

from tkinter.filedialog import askdirectory

import dependency_manager

from threading import Thread
    
root = Tk()
root.title("Feet to Meters")

ttk.Style().configure("TButton", padding=6, relief="flat",
   background="#595b59")

ttk.Style().configure("TEntry", padding=6, relief="flat",
   background="#595b59")

mainframe = ttk.Frame(root, padding="0 0 0 0")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

background_image=PhotoImage(file="images/potm_title.png")
background_label = Label(mainframe, image=background_image, borderwidth=0)
background_label.grid(row=0,column=0, rowspan=8, columnspan=8)

progress = ttk.Progressbar(mainframe)
#progress.grid(row=4,column=0)

launch_button = ttk.Button(mainframe, text = 'Launch')
launch_button.place(in_=mainframe, anchor="c", relx=.5, rely=.6)

def _trigger_launch(e):
    os.chdir(path_finder.get_path())
    subprocess.call(path_finder.get_executable_path() + " +connect 104.155.20.124:5121")

launch_button.bind("<Button-1>",_trigger_launch)

nwn_path = StringVar()
nwn_path.set(path_finder.get_path())
nwn_path_label = ttk.Label(mainframe, textvariable=nwn_path, width=0)
nwn_path_label.place(in_=mainframe, anchor="c", relx=.5, rely=.7)

def _trigger_path_dialogue(e):
    path = askdirectory(title="Select NWN installation directory")
    nwn_path.set(path)
    path_finder.set_path(path)

nwn_path_label.bind("<Button-1>",_trigger_path_dialogue)

def _trigger_quit(e):
    sys.exit()

quit_button = ttk.Button(mainframe, text = "Quit")
quit_button.grid(row = 7, column = 7)
quit_button.bind("<Button-1>", _trigger_quit)

def _trigger_update(e):
    t = Thread(target=dependency_manager.do_update, args=())
    t.start()

update_button = ttk.Button(mainframe, text = "Update")
update_button.grid(row = 7, column = 0)
update_button.bind("<Button-1>", _trigger_update)

update_status = StringVar()
update_status.set(dependency_manager.status)
update_status_label = ttk.Label(mainframe, textvariable=update_status, width=0)
update_status_label.grid(row = 7, column = 1)

def _check_update_status():
    root.after(250, _check_update_status)

    if dependency_manager.status is dependency_manager.STATUS_DOWNLOADING:
        update_status.set(dependency_manager.status + dependency_manager.file_being_downloaded)
    else:
        update_status.set(dependency_manager.status)

_check_update_status()

"""def sleeper(i):
    print ("thread %d sleeps for 5 seconds" % i)
    global test
    test = test + 1
    time.sleep(5)
    print ("thread %d woke up" % i)
    test = test + 1
    print(test)

for i in range(10):
    t = Thread(target=sleeper, args=(i,))
    t.start()"""

root.mainloop()