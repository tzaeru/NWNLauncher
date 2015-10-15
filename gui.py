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

import webbrowser

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

    config.serialize_to_main_conf(["download_music", "download_portraits", "download_overrides"],
        [music_var.get(), portraits_var.get(), overrides_var.get()])

    if path_finder.get_nwn_path() is not path_finder.NO_PATH:
        t = Thread(target=dependency_manager.start_check, args=())
        t.start()

def _dm_checkbox_clicked(e = None):
    if dm_var.get():
        dm_pass_label.place(in_=mainframe, anchor="e", relx=0.57, rely=.975)
        dm_pass_entry.place(in_=mainframe, anchor="w", relx=0.57, rely=.975)
    else:
        dm_pass_label.place_forget()
        dm_pass_entry.place_forget()

    config.serialize_to_main_conf(["login_as_dm"],
        [dm_var.get()])

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
    if dm_var.get():
        subprocess.call(path_finder.get_executable_path() + " -dmc +connect " + config.nwn_server_address +
            " +password " + dm_pass_var.get(), cwd=path_finder.get_nwn_path())
    else:
        subprocess.call(path_finder.get_executable_path() + " +connect " + config.nwn_server_address, cwd=path_finder.get_nwn_path())

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
music_var.set(config.main_conf_values["download_music"])
music_checkbox = Checkbutton(mainframe, text="Music", variable=music_var, foreground="#ffe0e0",
    selectcolor="#9a9b99", background="#5a5b59", borderwidth=0, pady=0, command=_do_check_update)
music_checkbox.place(in_=mainframe, anchor="w", relx=.03, rely=.975)

overrides_var = IntVar()
overrides_var.set(config.main_conf_values["download_overrides"])
overrides_checkbox = Checkbutton(mainframe, text="Overrides", variable=overrides_var, foreground="#ffe0e0",
    selectcolor="#9a9b99", background="#5a5b59", borderwidth=0, pady=0, command=_do_check_update)
overrides_checkbox.place(in_=mainframe, anchor="w", relx=.15, rely=.975)

portraits_var = IntVar()
portraits_var.set(config.main_conf_values["download_portraits"])
portraits_checkbox = Checkbutton(mainframe, text="Portraits", variable=portraits_var, foreground="#ffe0e0",
    selectcolor="#9a9b99", background="#5a5b59", borderwidth=0, pady=0, command=_do_check_update)
portraits_checkbox.place(in_=mainframe, anchor="w", relx=.27, rely=.975)

# DM Checkbox
dm_var = IntVar()
dm_var.set(config.main_conf_values["login_as_dm"])
dm_checkbox = Checkbutton(mainframe, text="Connect as DM", variable=dm_var, foreground="#ffe0e0",
    selectcolor="#9a9b99", background="#5a5b59", borderwidth=0, pady=0, command=_dm_checkbox_clicked)
dm_checkbox.place(in_=mainframe, anchor="e", relx=0.96, rely=.975)

dm_pass_label = Label(text = "Password: ", borderwidth = 3, width=0,
        padx=2, pady=2,
        font="TkTextFond 8 bold", foreground="#efeeee",
        background="#393b39")

dm_pass_var = StringVar()
dm_pass_entry = Entry(mainframe, show='*', textvariable=dm_pass_var)
_dm_checkbox_clicked()

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

LARGE_FONT= ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)

URL_FONT = ("Helvetica", 10, "underline")

def _gog_popupmsg():
    top = Toplevel()
    top.title("GoG CD key detected")

    msg = ttk.Label(top, text="You seem to be using the default CD key provided by Good old Games.\n\n" + 
        "Due to the potential for abuse, many servers have banned this CD key.\n", font=NORM_FONT)
    msg.pack()

    def open_gog(e):
        webbrowser.open("http://www.gog.com/support/neverwinter_nights_diamond_edition/online_play_in_neverwinter_nights_diamond")

    link = ttk.Label(top, text="Visit GoG for a fix!\n", foreground="blue", font=URL_FONT)
    link.bind("<Button-1>", open_gog)
    link.pack()

    dont_show_again_var = IntVar()
    dont_show_again_var.set(0)

    def serialize_gog_warning():
        config.serialize_to_main_conf(["show_gog_warning"], [dont_show_again_var.get() != True])

    dont_show_again_checkbox = Checkbutton(top, text="Don't show again", variable=dont_show_again_var,
        command=serialize_gog_warning)
    dont_show_again_checkbox.pack()

    button = ttk.Button(top, text="Dismiss", command=top.destroy)
    button.pack()

def _check_for_gog_cd_key():
    with open(path_finder.get_cdkey_path()) as cdkey:
        cd_keys = cdkey.read()
        cd_keys = cd_keys.replace(" ", "")
        key1_index = cd_keys.find("Key1")
        key1_index = cd_keys.find("=", key1_index) + 1
        key1 = cd_keys[key1_index:cd_keys.find("\n", key1_index)]
        key1 = key1.replace("-", "")
        public_key1 = ""
        for i in range(0,8):
            public_key1 += key1[1 + i*2]
        if public_key1 == "Q7RREKF3":
            _gog_popupmsg()

if config.main_conf_values["show_gog_warning"]:
    root.after(50, _check_for_gog_cd_key)

root.wm_protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()