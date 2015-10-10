import pytoml as toml

remote_data_file = ""
local_data_file = ""
nwn_server_address = ""

def load_config(file):
    with open(file) as conffile:
        config = toml.load(conffile)

        global remote_data_file
        remote_data_file = config["remote_data_file"]

        global local_data_file
        local_data_file = config["local_data_file"]

        global nwn_server_address
        nwn_server_address = config["nwn_server_address"]