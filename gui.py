from tkinter import *
from tkinter import ttk

from threading import Thread
import time

import path_finder

import os, subprocess

from tkinter.filedialog import askdirectory

import dependency_manager

from threading import Thread

import config
from PIL import Image, ImageTk

gui_update_cycles = 0

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

def _create_label_button(text) -> Button:
    label = Label(mainframe, text = text, compound="center",
        image=button_active_image, borderwidth = 0,
        relief = "flat",  padx=0, pady=0, background="#030200",
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

def _do_check_update(e = None):
    dependency_manager.download_music = bool(music_var.get())
    dependency_manager.download_portraits = bool(portraits_var.get())
    dependency_manager.download_overrides = bool(overrides_var.get())

    if path_finder.get_nwn_path() is not path_finder.NO_PATH:
        t = Thread(target=dependency_manager.start_check, args=())
        t.start()

root = Tk()
root.title("NWN Launcher - Prisoners of The Mist")
root.resizable(0,0)

# Load the images we'll use
background_image=ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), "background.png"))
button_active_image=ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), "button_active.png"))
button_disabled_image=ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), "button_disabled.png"))
button_hovered_image=ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), "button_hovered.png"))

def _load_images():
    global background_image
    background_image=ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), "background.png"))
    global button_active_image
    button_active_image=ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), "button_active.png"))
    global button_disabled_image
    button_disabled_image=ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), "button_disabled.png"))
    global button_hovered_image
    button_hovered_image=ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), "button_hovered.png"))
    background_label["image"] = background_image

    if update_button.enabled:
        _image_to_enabled(update_button)
    else:
        _image_to_disabled(update_button)

    _image_to_enabled(launch_button)
    _image_to_enabled(quit_button)

ttk.Style().configure("TEntry", padding=6, relief="flat",
   background="#595b59")

mainframe = ttk.Frame(root, padding="0 0 0 0")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

background_label = Label(mainframe, image=background_image, borderwidth=0, background="#000000")
background_label.grid(row=0,column=0, rowspan=8, columnspan=8)

launch_button = _create_label_button("Launch")
launch_button.place(in_=mainframe, anchor="c", relx=.5, rely=.6)
#launch_button.grid(row=6, column=0)

def _trigger_launch(e):
    os.chdir(path_finder.get_nwn_path())
    subprocess.call(path_finder.get_executable_path() + " +connect 104.155.20.124:5121")

launch_button.bind("<Button-1>",_trigger_launch)

nwn_path = StringVar()
nwn_path.set(path_finder.get_nwn_path())
nwn_path_label = _create_label(nwn_path)
nwn_path_label.place(in_=mainframe, anchor="c", relx=.5, rely=.7)

def _trigger_path_dialogue(e):
    path = askdirectory(title="Select NWN installation directory")
    nwn_path.set(path)
    path_finder.set_nwn_path(path)

nwn_path_label.bind("<Button-1>",_trigger_path_dialogue)

def _trigger_quit(e):
    dependency_manager.do_quit = True
    root.quit()

quit_button = _create_label_button("Quit")
quit_button.grid(row = 7, column = 7)
quit_button.bind("<Button-1>", _trigger_quit)

update_button = _create_label_button("Update")
update_button.grid(row = 7, column = 0)
_image_to_disabled(update_button)

music_var = IntVar()
music_var.set(1)
music_checkbox = Checkbutton(mainframe, text="Music", variable=music_var, foreground="#ffe0e0",
    selectcolor="#9a9b99", background="#5a5b59", borderwidth=0, pady=0, command=_do_check_update)
music_checkbox.place(in_=mainframe, anchor="w", relx=.03, rely=.975)

overrides_var = IntVar()
overrides_var.set(1)
overrides_checkbox = Checkbutton(mainframe, text="Overrides", variable=overrides_var, foreground="#ffe0e0",
    selectcolor="#9a9b99", background="#5a5b59", borderwidth=0, pady=0, command=_do_check_update)
overrides_checkbox.place(in_=mainframe, anchor="w", relx=.15, rely=.975)

portraits_var = IntVar()
portraits_var.set(1)
portraits_checkbox = Checkbutton(mainframe, text="Portraits", variable=portraits_var, foreground="#ffe0e0",
    selectcolor="#9a9b99", background="#5a5b59", borderwidth=0, pady=0, command=_do_check_update)
portraits_checkbox.place(in_=mainframe, anchor="w", relx=.27, rely=.975)

def _change_server_conf(*args):
    for key, value in config.confs.items():
        if value["name_full"] == server_var.get():
            config.setup_config_for(value["name_short"])
            break

    _do_check_update()
    _load_images()

server_var = StringVar()
server_combobox = ttk.Combobox(mainframe, textvariable=server_var, width=29)
servers = []
for key, value in config.confs.items():
    servers.append(value["name_full"])
server_combobox["values"] = servers
server_var.set(config.current_server_full_name)
server_combobox.state(['readonly'])
server_combobox.place(in_=mainframe, anchor="nw", relx=.0, rely=.0)
server_var.trace("w", _change_server_conf)

def _trigger_update(e):
    _image_to_disabled(update_button)
    t = Thread(target=dependency_manager.do_update, args=())
    t.start()

update_button.bind("<Button-1>", _trigger_update)

#music_checkbox.bind("<Button-1>", _do_check_update)
#overrides_checkbox.bind("<Button-1>", _do_check_update)
#portraits_checkbox.bind("<Button-1>", _do_check_update)

update_status = StringVar()
update_status.set(dependency_manager.status + "\nHi" + "\nHello")
update_status_label = Label(mainframe, textvariable=update_status,
    width=36, height=3, anchor="w",
    justify=LEFT, borderwidth = 3,
    relief = SUNKEN, padx=2, pady=2,
    font="TkTextFond 10 bold", foreground="#efeeee",
    background="#393b39")
update_status_label.place(in_=mainframe, anchor="nw", relx=.25, rely=.80)

def _check_update_status():
    global gui_update_cycles

    root.after(250, _check_update_status)
    if dependency_manager.status is dependency_manager.STATUS_DOWNLOADING:
        current_progress = dependency_manager.current_file_progress
        current_progress_str = '{0:0.1f}'.format(current_progress*100.0)

        total_progress = dependency_manager.total_progress
        total_progress_str = '{0:0.1f}'.format(total_progress*100.0)

        update_text = ("Downloading " +
            dependency_manager.file_being_downloaded +
            '.' * (1 + gui_update_cycles%3) +
            "\nCurrent progress: " + current_progress_str + " %" +
            "\nTotal progress: " + total_progress_str)  + " %"
        update_status.set(update_text)
    else:
        update_status.set(dependency_manager.status)

    if dependency_manager.status is dependency_manager.STATUS_UPDATES_AVAILABLE:
        update_text = ("Updates are available for " +
            str(dependency_manager.total_amount_of_updates) +
            " files,\ntotaling at: " +
            '{0:0.1f}'.format(dependency_manager.total_size_of_updates/1024.0/1024.0) +
            " MB\n")

        update_status.set(update_text)
        _image_to_enabled(update_button)

    gui_update_cycles += 1

_check_update_status()

def on_closing():
    _trigger_quit(None)

root.wm_protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()