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
player_name = ""

def load_config(path):
    global confs
    confs = _load_configs(path)

    global config_path
    config_path = path

    global player_name
    player_name = _load_player_name()

    global main_conf_values

    with open(os.path.join(path, "main_config.toml")) as conffile:
        config = toml.load(conffile)
        main_conf_values = config
        setup_config_for(config["default_server"])

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
    with open(path_finder.get_nwnplayer_path()) as nwnplayer_conf:
        for line in nwnplayer_conf:
            if "Player Name" in line or "player name" in line:
                return line[line.index('=') + 1:-1]

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

    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            try:
                with open(os.path.join(path, item, "config.toml")) as conffile:
                    config = toml.load(conffile)
                    confs[config["name_short"]] = config
            except IOError:
                continue

    return confs
