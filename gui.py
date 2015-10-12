from tkinter import *
from tkinter import ttk

from threading import Thread
import time

import path_finder

import os, subprocess

from tkinter.filedialog import askdirectory

import dependency_manager

from threading import Thread

def _image_to_selected(event):
    if event.widget.enabled == True:
        event.widget["image"] = button_hovered_image

def _image_to_deselected(event):
    if event.widget.enabled == True:
        event.widget["image"] = button_active_image

def _image_to_disabled(widget):
    widget.enabled = False
    widget["image"] = button_disabled_image
    widget["foreground"] = "#908080"

def _image_to_enabled(widget):
    widget.enabled = True
    widget["image"] = button_active_image
    widget["foreground"] = "#ffe0e0"

def _create_label_button(text) -> Label:
    label = Label(mainframe, text = text, compound="center",
        image=button_active_image, borderwidth = 0,
        relief = "flat", padx=0, pady=0,
        font="TkHeadingFont 15 bold", foreground="#ffe0e0")

    label.enabled = True

    label.bind("<Enter>", _image_to_selected)
    label.bind("<Leave>", _image_to_deselected)

    return label

def _create_label(text_v) -> Label:
    label = Label(mainframe, textvariable = text_v,
        borderwidth = 3, width=0,
        relief = SUNKEN, padx=2, pady=2,
        font="TkTextFond 10 bold", foreground="#efeeee",
        background="#393b39")

    return label

root = Tk()
root.title("NWN Launcher - Prisoners of The Mist")
root.resizable(0,0)

# Load the images we'll use
background_image=PhotoImage(file="images/potm_title.png")
button_active_image=PhotoImage(file="images/button_active.png")
button_disabled_image=PhotoImage(file="images/button_disabled.png")
button_hovered_image=PhotoImage(file="images/button_hovered.png")

ttk.Style().configure("TEntry", padding=6, relief="flat",
   background="#595b59")

mainframe = ttk.Frame(root, padding="0 0 0 0")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

background_label = Label(mainframe, image=background_image, borderwidth=0)
background_label.grid(row=0,column=0, rowspan=8, columnspan=8)

progress = ttk.Progressbar(mainframe)
progress.grid(row=4,column=0)

launch_button = _create_label_button("Launch")
launch_button.place(in_=mainframe, anchor="c", relx=.5, rely=.6)
#launch_button.grid(row=6, column=0)

def _trigger_launch(e):
    os.chdir(path_finder.get_path())
    subprocess.call(path_finder.get_executable_path() + " +connect 104.155.20.124:5121")

launch_button.bind("<Button-1>",_trigger_launch)

nwn_path = StringVar()
nwn_path.set(path_finder.get_path())
nwn_path_label = _create_label(nwn_path)
nwn_path_label.place(in_=mainframe, anchor="c", relx=.5, rely=.7)

def _trigger_path_dialogue(e):
    path = askdirectory(title="Select NWN installation directory")
    nwn_path.set(path)
    path_finder.set_path(path)

nwn_path_label.bind("<Button-1>",_trigger_path_dialogue)

def _trigger_quit(e):
    sys.exit()

quit_button = _create_label_button("Quit")
quit_button.grid(row = 7, column = 7)
quit_button.bind("<Button-1>", _trigger_quit)

update_button = _create_label_button("Update")
update_button.grid(row = 7, column = 0)
_image_to_disabled(update_button)

def _trigger_update(e):
    _image_to_disabled(update_button)
    t = Thread(target=dependency_manager.do_update, args=())
    t.start()

update_button.bind("<Button-1>", _trigger_update)

update_status = StringVar()
update_status.set(dependency_manager.status)
update_status_label = ttk.Label(mainframe, textvariable=update_status, width=0)
update_status_label.grid(row = 7, column = 1)

def _check_update_status():
    root.after(250, _check_update_status)
    if dependency_manager.status is dependency_manager.STATUS_UPDATES_AVAILABLE:
        _image_to_enabled(update_button)

    if dependency_manager.status is dependency_manager.STATUS_DOWNLOADING:
        update_status.set(dependency_manager.status + dependency_manager.file_being_downloaded)
    else:
        update_status.set(dependency_manager.status)

_check_update_status()

root.mainloop()