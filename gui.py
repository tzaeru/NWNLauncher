from tkinter import *
from tkinter import ttk

from threading import Thread
import time

import path_finder

import os, subprocess

from tkinter.filedialog import askdirectory

import dependency_manager

import config
from PIL import Image, ImageTk

import webbrowser

import utilities
import functools

import version_checker

gui_update_cycles = 0
update_check_queued = False
shown_update = False

def _image_to_selected(event):
    if event.widget.enabled == True:
        event.widget["image"] = buttons[event.widget.name + "_button_hovered"]

def _image_to_deselected(event):
    if event.widget.enabled == True:
        event.widget["image"] = buttons[event.widget.name + "_button_active"]

def _image_to_disabled(widget, image_name):
    widget.enabled = False
    widget["image"] = buttons[image_name + "_button_disabled"]
    widget["foreground"] = config.get_gui_conf("button_disabled_fg_color")

def _image_to_enabled(widget, image_name):
    widget.enabled = True
    widget["image"] = buttons[image_name + "_button_active"]
    widget["foreground"] = config.get_gui_conf("button_enabled_fg_color")

def _create_label_button(text, image_name, font = config.get_gui_conf("button_font")) -> Button:
    if (config.get_gui_conf("put_labels_on_buttons") is False):
        text = ""

    label = Label(mainframe, text = text, compound="center",
        image=buttons[image_name + "_button_active"], borderwidth = 0,
        relief = "flat",  padx=0, pady=0, background=config.get_gui_conf("button_bg_color"),
        font=config.get_gui_conf("button_font"), foreground=config.get_gui_conf("button_enabled_fg_color"))

    label.enabled = True

    label.name = image_name

    label.bind("<Enter>", _image_to_selected)
    label.bind("<Leave>", _image_to_deselected)

    return label

def _create_label(text_v) -> Label:
    label = Label(mainframe, textvariable = text_v,
        borderwidth = 3, width=0,
        relief = SUNKEN, padx=2, pady=2,
        font="TkTextFond 9", foreground="#efeeee",
        background="#393b39")

    return label

def _do_check_update(e = None):
    dependency_manager.download_music = bool(music_var.get())
    dependency_manager.download_portraits = bool(portraits_var.get())
    dependency_manager.download_overrides = bool(overrides_var.get())
    dependency_manager.allow_overwrite = bool(overrides_var.get())

    config.serialize_to_main_conf(["download_music", "download_portraits", "download_overrides", "allow_overwrite"],
        [music_var.get(), portraits_var.get(), overrides_var.get(), overwrite_var.get()])

    global update_check_queued
    update_check_queued = True
    _check_update_status(False)

def _dm_checkbox_clicked(e = None):
    if dm_var.get():
        dm_pass_label.place(in_=mainframe,
            anchor=config.get_gui_conf("dm_pass_label_anchor"),
            relx=config.get_gui_conf("dm_pass_label_pos")[0],
            rely=config.get_gui_conf("dm_pass_label_pos")[1])
        dm_pass_entry.place(in_=mainframe,
            anchor=config.get_gui_conf("dm_pass_entry_anchor"),
            relx=config.get_gui_conf("dm_pass_entry_pos")[0],
            rely=config.get_gui_conf("dm_pass_entry_pos")[1])
    else:
        dm_pass_label.place_forget()
        dm_pass_entry.place_forget()

    config.serialize_to_main_conf(["login_as_dm"],
        [dm_var.get()])

def _trigger_delete_overrides(e = None):
    dependency_manager.delete_overrides()

root = Tk()
root.title("NWN Launcher - Prisoners of The Mist")
root.resizable(0,0)
#root.iconify()
#root.attributes('-alpha', 0.0) #For icon
#main_window = Toplevel()
#main_window.overrideredirect(False)
#main_window.geometry("1000x1000") #Whatever size

# Load the images we'll use
background_image=ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), "background.png"))

buttons = {}

for button_name in ["clear", "launch", "update", "website", "gear"]:
    buttons[button_name + "_button_active"] = ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), button_name + "_button_active.png"))
    buttons[button_name + "_button_disabled"] = ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), button_name + "_button_disabled.png"))
    buttons[button_name + "_button_hovered"] = ImageTk.PhotoImage(file=os.path.join(path_finder.get_server_images_path(), button_name + "_button_hovered.png"))

"""def _load_images():
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

    _image_to_enabled(launch_button)"""

ttk.Style().configure("TEntry", padding=6, relief="flat",
   background="#595b59")

#mainframe = ttk.Frame(main_window, padding="0 0 0 0")
mainframe = ttk.Frame(root, padding="0 0 0 0")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

background_label = Label(mainframe, image=background_image, borderwidth=0, background="#000000")
background_label.grid(row=0,column=0, rowspan=8, columnspan=8)
background_label.bind("<Button-1>", lambda event: print("Pressed BG"))

launch_button = _create_label_button("Launch", "launch")
launch_button.place(in_=mainframe, anchor=config.get_gui_conf("launch_button_anchor"),
    relx=config.get_gui_conf("launch_button_pos")[0],
    rely=config.get_gui_conf("launch_button_pos")[1])

def _trigger_launch(e):
    config.set_player_name(player_var.get())

    utilities.backup_logs()

    if dm_var.get():
        subprocess.Popen(path_finder.get_executable_path() + " -dmc +connect " + config.nwn_server_address +
            " +password " + dm_pass_var.get(), cwd=path_finder.get_nwn_path())
    else:
        print("Exe dir path: " + path_finder.get_executable_dir_path())
        print("Exe path: " + path_finder.get_executable_path())
        subprocess.Popen(path_finder.get_executable_path() + " +connect " + config.nwn_server_address, cwd=path_finder.get_executable_dir_path())

launch_button.bind("<Button-1>",_trigger_launch)

website_button = _create_label_button("Website", "website")
website_button.place(in_=mainframe, anchor=config.get_gui_conf("website_button_anchor"),
    relx=config.get_gui_conf("website_button_pos")[0],
    rely=config.get_gui_conf("website_button_pos")[1])

website_button.bind("<Button-1>", lambda event: webbrowser.open(config.get_server_conf("website")))

def _change_player_conf(*args):
    for key, value in config.confs.items():
        if value["name_full"] == server_var.get():
            config.setup_config_for(value["name_short"])
            break

diagnosis_button = _create_label_button("Gear", "gear")
diagnosis_button.place(in_=mainframe, anchor=config.get_gui_conf("gear_button_anchor"),
    relx=config.get_gui_conf("gear_button_pos")[0],
    rely=config.get_gui_conf("gear_button_pos")[1])

def _open_diagnosis(e):
    subprocess.Popen("winmtr/WinMTR.exe " + config.nwn_server_address, cwd=path_finder.get_nwn_path())

diagnosis_button.bind("<Button-1>",_open_diagnosis)



player_name_label = Label(mainframe, text = "Player name: ", borderwidth = 0, width=0,
        padx=2, pady=2,
        font=config.get_gui_conf("player_name_label_font", "label_default_font"),
        foreground=config.get_gui_conf("player_name_label_fg_color", "label_default_fg_color"),
        background=config.get_gui_conf("player_name_label_bg_color", "label_default_bg_color"))
player_name_label.place(in_=mainframe, anchor=config.get_gui_conf("player_name_label_anchor"),
    relx=config.get_gui_conf("player_name_label_pos")[0],
    rely=config.get_gui_conf("player_name_label_pos")[1])

player_var = StringVar()
player_combobox = ttk.Combobox(mainframe, textvariable=player_var, width=29)
player_combobox["values"] = config.main_conf_values["player_names"]
player_var.set(config.player_name)
#player_combobox.state(['readonly'])
player_combobox.place(in_=mainframe,
    anchor=config.get_gui_conf("player_combobox_anchor"),
    relx=config.get_gui_conf("player_combobox_pos")[0],
    rely=config.get_gui_conf("player_combobox_pos")[1])
#player_var.trace("w", _change_player_conf)

def _save_player():
    if player_var.get() not in config.main_conf_values["player_names"]:
        config.main_conf_values["player_names"].append(player_var.get())
        config.serialize_to_main_conf(["player_names"], [config.main_conf_values["player_names"]])

player_save_button = Label(mainframe, text = "Save Name", borderwidth = 0, width=0,
        padx=2, pady=2,
        font=config.get_gui_conf("save_button_font", "button_font"),
        foreground=config.get_gui_conf("save_button_fg_color", "button_enabled_fg_color"),
        background=config.get_gui_conf("save_button_bg_color", "button_bg_color"))
player_save_button.place(in_=mainframe,
    anchor=config.get_gui_conf("save_button_anchor"),
    relx=config.get_gui_conf("save_button_pos")[0],
    rely=config.get_gui_conf("save_button_pos")[1])
player_save_button.bind("<Button-1>",lambda e:_save_player())

nwn_path = StringVar()
nwn_path.set(path_finder.get_nwn_path())
nwn_path_label = _create_label(nwn_path)
nwn_path_label.place(in_=mainframe,
    anchor=config.get_gui_conf("nwn_path_label_anchor"),
    relx=config.get_gui_conf("nwn_path_label_pos")[0],
    rely=config.get_gui_conf("nwn_path_label_pos")[1])

nwn_path_name_label = Label(mainframe, text = "NWN Path:", borderwidth = 0, width=0,
        padx=2, pady=2,
        font=config.get_gui_conf("nwn_path_name_label_font", "label_font"),
        foreground=config.get_gui_conf("nwn_path_name_label_fg_color", "label_fg_color"),
        background=config.get_gui_conf("nwn_path_name_label_bg_color", "label_bg_color"))
nwn_path_name_label.place(in_=mainframe,
    anchor=config.get_gui_conf("nwn_path_name_label_anchor"),
    relx=config.get_gui_conf("nwn_path_name_label_pos")[0],
    rely=config.get_gui_conf("nwn_path_name_label_pos")[1])

def _trigger_path_dialogue(e):
    path = askdirectory(title="Select NWN installation directory")
    if len(path) > 0:
        print("Setting path!")
        if path_finder.set_nwn_path(path):
            nwn_path.set(path)
            _do_check_update()
            config.serialize_to_main_conf(["nwn_path"], [path])
        else:
            print("False path: " + path)

nwn_path_label.bind("<Button-1>",_trigger_path_dialogue)

update_button = _create_label_button("Update", "update")
update_button.place(in_=mainframe,
    anchor=config.get_gui_conf("update_button_anchor"),
    relx=config.get_gui_conf("update_button_pos")[0],
    rely=config.get_gui_conf("update_button_pos")[1])
_image_to_disabled(update_button, "update")

music_var = IntVar()
music_var.set(config.main_conf_values["download_music"])
music_checkbox = Checkbutton(mainframe, text="Music", variable=music_var,
    foreground=config.get_gui_conf("music_checkbox_select_color", "checkbox_fg_color"),
    background=config.get_gui_conf("music_checkbox_bg_color", "checkbox_bg_color"),
    selectcolor=config.get_gui_conf("music_checkbox_fg_color", "checkbox_select_color"),
    borderwidth=0, pady=0, command=_do_check_update)
music_checkbox.place(in_=mainframe,
    anchor=config.get_gui_conf("music_checkbox_anchor"),
    relx=config.get_gui_conf("music_checkbox_pos")[0],
    rely=config.get_gui_conf("music_checkbox_pos")[1])

overrides_var = IntVar()
overrides_var.set(config.main_conf_values["download_overrides"])
overrides_checkbox = Checkbutton(mainframe, text="Overrides", variable=overrides_var,
    foreground=config.get_gui_conf("overrides_checkbox_select_color", "checkbox_fg_color"),
    background=config.get_gui_conf("overrides_checkbox_bg_color", "checkbox_bg_color"),
    selectcolor=config.get_gui_conf("overrides_checkbox_fg_color", "checkbox_select_color"),
    borderwidth=0, pady=0, command=_do_check_update)
overrides_checkbox.place(in_=mainframe,
    anchor=config.get_gui_conf("overrides_checkbox_anchor"),
    relx=config.get_gui_conf("overrides_checkbox_pos")[0],
    rely=config.get_gui_conf("overrides_checkbox_pos")[1])

portraits_var = IntVar()
portraits_var.set(config.main_conf_values["download_portraits"])
portraits_checkbox = Checkbutton(mainframe, text="Portraits", variable=portraits_var,
    foreground=config.get_gui_conf("portraits_checkbox_select_color", "checkbox_fg_color"),
    background=config.get_gui_conf("portraits_checkbox_bg_color", "checkbox_bg_color"),
    selectcolor=config.get_gui_conf("portraits_checkbox_fg_color", "checkbox_select_color"),
    borderwidth=0, pady=0, command=_do_check_update)
portraits_checkbox.place(in_=mainframe,
    anchor=config.get_gui_conf("portraits_checkbox_anchor"),
    relx=config.get_gui_conf("portraits_checkbox_pos")[0],
    rely=config.get_gui_conf("portraits_checkbox_pos")[1])

overwrite_var = IntVar()
overwrite_var.set(config.main_conf_values["allow_overwrite"])
overwrite_checkbox = Checkbutton(mainframe, text="Allow overwriting dependencies", variable=overwrite_var,
    foreground=config.get_gui_conf("overwrite_checkbox_select_color", "checkbox_fg_color"),
    background=config.get_gui_conf("overwrite_checkbox_bg_color", "checkbox_bg_color"),
    selectcolor=config.get_gui_conf("overwrite_checkbox_fg_color", "checkbox_select_color"),
    borderwidth=0, pady=0, command=_do_check_update)
overwrite_checkbox.place(in_=mainframe,
    anchor=config.get_gui_conf("overwrite_checkbox_anchor"),
    relx=config.get_gui_conf("overwrite_checkbox_pos")[0],
    rely=config.get_gui_conf("overwrite_checkbox_pos")[1])

# DM Checkbox
dm_var = IntVar()
dm_var.set(config.main_conf_values["login_as_dm"])
dm_checkbox = Checkbutton(mainframe, text="Connect as DM", variable=dm_var,
    foreground=config.get_gui_conf("dm_checkbox_select_color", "checkbox_fg_color"),
    background=config.get_gui_conf("dm_checkbox_bg_color", "checkbox_bg_color"),
    selectcolor=config.get_gui_conf("dm_checkbox_fg_color", "checkbox_select_color"),
    borderwidth=0, pady=0, command=_dm_checkbox_clicked)
dm_checkbox.place(in_=mainframe,
    anchor=config.get_gui_conf("dm_checkbox_anchor"),
    relx=config.get_gui_conf("dm_checkbox_pos")[0],
    rely=config.get_gui_conf("dm_checkbox_pos")[1])

dm_pass_label = Label(text = "Pass: ", borderwidth = 3, width=0,
        padx=2, pady=2,
        font=config.get_gui_conf("dm_pass_label_font", "label_font"),
        foreground=config.get_gui_conf("dm_pass_label_fg_color", "label_fg_color"),
        background=config.get_gui_conf("dm_pass_label_bg_color", "label_bg_color"))

dm_pass_var = StringVar()
dm_pass_entry = Entry(mainframe, show='*', textvariable=dm_pass_var)
_dm_checkbox_clicked()

def _change_server_conf(*args):

    for key, value in config.confs.items():
        if value["name_full"] == server_var.get():
            config.serialize_to_main_conf(["default_server"], [value["name_short"]])
            #config.setup_config_for(value["name_short"])
            break

    python = sys.executable
    os.execl(python, python, * sys.argv)

    #_do_check_update()
    #_load_images()

server_var = StringVar()
server_combobox = ttk.Combobox(mainframe, textvariable=server_var, width=29)
servers = []
for key, value in config.confs.items():
    servers.append(value["name_full"])
server_combobox["values"] = servers
server_var.set(config.current_server_full_name)
server_combobox.state(['readonly'])
server_combobox.place(in_=mainframe,
    anchor=config.get_gui_conf("server_combobox_anchor"),
    relx=config.get_gui_conf("server_combobox_pos")[0],
    rely=config.get_gui_conf("server_combobox_pos")[1])
server_var.trace("w", _change_server_conf)

def _trigger_update(e):
    _image_to_disabled(update_button, "update")
    t = Thread(target=dependency_manager.do_update, args=())
    t.start()

update_button.bind("<Button-1>", _trigger_update)

#music_checkbox.bind("<Button-1>", _do_check_update)
#overrides_checkbox.bind("<Button-1>", _do_check_update)
#portraits_checkbox.bind("<Button-1>", _do_check_update)

update_status = StringVar()
update_status.set(dependency_manager.status + "\nHi" + "\nHello")
update_status_label = Label(mainframe, textvariable=update_status,
    width=40, height=4, anchor="w",
    justify=LEFT, borderwidth = 3,
    relief = SUNKEN, padx=2, pady=2,
    font=config.get_gui_conf("update_status_label_font", "label_font"),
    foreground=config.get_gui_conf("update_status_label_fg_color", "label_fg_color"),
    background=config.get_gui_conf("update_status_label_bg_color", "label_bg_color"))
update_status_label.place(in_=mainframe,
    anchor=config.get_gui_conf("update_status_label_anchor"),
    relx=config.get_gui_conf("update_status_label_pos")[0],
    rely=config.get_gui_conf("update_status_label_pos")[1])

delete_overrides_button = _create_label_button("Delete overrides..", "clear", font="TkHeadingFont 10")
delete_overrides_button.place(in_=mainframe,
    anchor=config.get_gui_conf("delete_overrides_button_anchor"),
    relx=config.get_gui_conf("delete_overrides_button_pos")[0],
    rely=config.get_gui_conf("delete_overrides_button_pos")[1])
delete_overrides_button.bind("<Button-1>", _trigger_delete_overrides)

def _check_update_status(repeat = True):
    if dependency_manager.do_quit == True:
        return

    global gui_update_cycles

    if repeat:
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
    elif dependency_manager.status is dependency_manager.STATUS_CHECKING:
        update_text = ("Checking for updates" +
            '.' * (1 + gui_update_cycles%3))
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
        _image_to_enabled(update_button, "update")

    global update_check_queued

    if (update_check_queued and
        dependency_manager.status is not dependency_manager.STATUS_DOWNLOADING and
        dependency_manager.status is not dependency_manager.STATUS_CHECKING):
        if path_finder.get_nwn_path() is not path_finder.NO_PATH:
            t = Thread(target=dependency_manager.start_check, args=())
            t.start()

        update_check_queued = False
    gui_update_cycles += 1

_check_update_status()

def on_closing():
    print("Quitting..")
    dependency_manager.do_quit = True
    root.quit()

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
    try:
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
            print("Public key: " + public_key1)
            if public_key1 == "Q7RREKF3":
                _gog_popupmsg()
    except:
        print("Couldn't check GoG CD key!")

def _check_for_upgrade():
    if version_checker.is_update_available() == True and shown_update == False:
        top = Toplevel()
        top.title("New launcher version available!")

        msg = ttk.Label(top, text="A new version of the launcher is available\n",
            font=NORM_FONT)
        msg.pack()

        def download_launcher(e):
            webbrowser.open("http://5.9.81.74:2020/NWN%20Launcher%20Installer.exe")

        download_button = ttk.Button(top, text="Download Update")
        download_button.bind("<Button-1>", download_launcher)
        download_button.pack()

        close_button = ttk.Button(top, text="Dismiss", command=top.destroy)
        close_button.pack()

        global shown_update
        shown_update = True

    if shown_update == False:
        root.after(5000, _check_for_upgrade)

root.after(50, _check_for_upgrade)

if config.main_conf_values["show_gog_warning"]:
    root.after(50, _check_for_gog_cd_key)

def _hosts_file_popupmsg():
    top = Toplevel()
    top.title("Speed up launch by modifying Hosts?")

    msg = ttk.Label(top, text="NWN launch time can be improved by modifying the Windows host file.\n\n" + 
        "However, some antivirus software may disallow this. Should we try it?\n", font=NORM_FONT)
    msg.pack()

    dont_show_again_var = IntVar()
    dont_show_again_var.set(0)

    def serialize_gog_warning():
        config.serialize_to_main_conf(["show_hosts_file_popupmsg"], [dont_show_again_var.get() != True])

    dont_show_again_checkbox = Checkbutton(top, text="Don't show again", variable=dont_show_again_var,
        command=serialize_gog_warning)
    dont_show_again_checkbox.pack()

    def do_authentication_skip():
        status = utilities._add_authentication_skip()
        top.destroy()
        status_level = Toplevel()
        msg = None
        if (status):
            status_level.title("Success")
            msg = ttk.Label(status_level, text="Modification succesful - enjoy your faster load time!", font=NORM_FONT)
        else:
            status_level.title("Failure")
            msg = ttk.Label(status_level, text="Modification unsuccesful - no file access?", font=NORM_FONT)
        msg.pack()

    button_yes = ttk.Button(top, text="Try it!", command=do_authentication_skip)
    button_yes.pack()

    button_no = ttk.Button(top, text="No, let's skip.", command=top.destroy)
    button_no.pack()

if config.main_conf_values["show_hosts_file_popupmsg"] and not utilities._check_authentication_skip():
    root.after(50, _hosts_file_popupmsg)

root.wm_protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
