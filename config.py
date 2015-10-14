import pytoml as toml

current_server = ""
remote_data_file = ""
local_versions_file = ""
local_checksums_file = ""
nwn_server_address = ""

def load_config(file):
    with open(file) as conffile:
        config = toml.load(conffile)

        global current_server
        current_server = config["default_server"]

        server_config = config["servers"][current_server]

        global remote_data_file
        remote_data_file = server_config["remote_data_file"]

        global local_versions_file
        local_versions_file = server_config["local_versions_file"]

        global local_checksums_file
        local_checksums_file = server_config["local_checksums_file"]

        global nwn_server_address
        nwn_server_address = server_config["nwn_server_address"]