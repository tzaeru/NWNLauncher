import pytoml as toml
import os

current_server = ""
current_server_full_name = ""
remote_data_file = ""
local_versions_file = ""
local_checksums_file = ""
nwn_server_address = ""
confs = {}

def load_config(path):
    global confs
    confs = _load_configs(path)

    with open(os.path.join(path, "main_config.toml")) as conffile:
        config = toml.load(conffile)

        setup_config_for(config["default_server"])

def setup_config_for(server_name):
    server_config = confs[server_name]

    global current_server
    current_server = server_config["name_short"]

    global remote_data_file
    remote_data_file = server_config["remote_data_file"]

    global local_versions_file
    local_versions_file = "file_versions.toml"

    global local_checksums_file
    local_checksums_file = "file_checksums.toml"

    global nwn_server_address
    nwn_server_address = server_config["nwn_server_address"]

    global current_server_full_name
    current_server_full_name = server_config["name_full"]

def _load_configs(path) -> dict:
    confs = {}

    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            with open(os.path.join(path, item, "config.toml")) as conffile:
                config = toml.load(conffile)
                confs[config["name_short"]] = config

    return confs