import pytoml as toml
import os
import path_finder

current_server = ""
current_server_full_name = ""
remote_data_file = ""
local_versions_file = ""
local_checksums_file = ""
nwn_server_address = ""
config_path = ""
main_conf_values = {}
confs = {}
gui_confs = {}
player_name = ""

def load_config(path):
    global confs, gui_confs
    confs, gui_confs = _load_configs(path)

    print(gui_confs)

    global config_path
    config_path = path

    global player_name
    player_name = _load_player_name()

    global main_conf_values

    with open(os.path.join(path, "main_config.toml")) as conffile:
        config = toml.load(conffile)
        main_conf_values = config
        if config["default_server"] in confs:
            setup_config_for(config["default_server"])
        else:
            serialize_to_main_conf(["default_server"], [next(iter(confs.values()))["name_short"]])
            setup_config_for(next(iter(confs.values()))["name_short"])

def setup_config_for(server_name):
    print("setting up server for: " + server_name)
    server_config = confs[server_name]

    global current_server
    current_server = server_config["name_short"]

    global remote_data_file
    remote_data_file = server_config["remote_data_file"]

    global local_versions_file
    local_versions_file = current_server + "_file_versions.toml"

    global local_checksums_file
    local_checksums_file = "file_checksums.toml"

    global nwn_server_address
    nwn_server_address = server_config["nwn_server_address"]

    global current_server_full_name
    current_server_full_name = server_config["name_full"]

def get_gui_conf(key, alt_key = None, default_value = None) -> object:
    if key in gui_confs[current_server]:
        return gui_confs[current_server][key]
    else:
        if alt_key in gui_confs[current_server]:
            return gui_confs[current_server][alt_key]
    return default_value

def get_server_conf(key, default_value = None) -> object:
    if key in confs[current_server]:
        return confs[current_server][key]
    return default_value

def serialize_to_main_conf(keys : list, values : list):
    config = None
    print("Setting keys: ", keys, " to values: ", values)
    with open(os.path.join(config_path, "main_config.toml")) as conffile:
        config = toml.load(conffile)

    for i in range(0, len(keys)):
        config[keys[i]] = values[i]

    global main_conf_values
    main_conf_values = config

    if config is not None:
        f = open(os.path.join(config_path, "main_config.toml"),'w')
        f.write(toml.dumps(config))
        f.flush()
        f.close()

def _load_player_name() -> str:
    try:
        with open(path_finder.get_nwnplayer_path()) as nwnplayer_conf:
            for line in nwnplayer_conf:
                if "Player Name" in line or "player name" in line:
                    return line[line.index('=') + 1:-1]
    except:
        print("Couldn't open NWN config file.")

    return " "

def set_player_name(name: str):
    f = open(path_finder.get_nwnplayer_path(), 'r')
    lines = f.readlines()

    for i in range(0, len(lines)):
        if "Player Name" in lines[i] or "player name" in lines[i]:
            lines[i] = lines[i][0:lines[i].index('=')+1] + name + '\n'
    f.close()

    f = open(path_finder.get_nwnplayer_path(), 'w')
    f.writelines(lines)
    # do the remaining operations on the file
    f.close()

def _load_configs(path) -> dict:
    confs = {}
    gui_confs = {}

    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            name_short = ""

            try:
                with open(os.path.join(path, item, "config.toml")) as conffile:
                    config = toml.load(conffile)
                    name_short = config["name_short"]
                    confs[name_short] = config
            except IOError:
                continue

            try:
                with open(os.path.join(path, item, "gui_config.toml")) as conffile:
                    config = toml.load(conffile)
                    gui_confs[name_short] = config
            except IOError:
                print("Failed to open GUI conf file.")
                continue

    return confs, gui_confs
