#!/usr/bin/python

import urllib, sys, os
from urllib.request import urlopen
import pytoml as toml
import config
import path_finder

STATUS_CHECKING = "Checking for updates..."
STATUS_NO_CONNECTION = "Failed to connect to file server."
STATUS_UPDATED = "Files are up to date."
STATUS_UPDATES_AVAILABLE = "Updates are available!"
STATUS_DOWNLOADING = "Downloading file: "

status = STATUS_CHECKING
file_being_downloaded = None
current_file_progress = 0.0
total_progress = 0.0

entries_to_update = []

def start_check():
    global entries_to_update
    global status

    remote_files_data = _load_remote_files_data()
    local_files_data = _load_local_files_data()

    updates_available = False

    entries_to_update = []

    for remote_file_entry in remote_files_data["files"]:
        do_fetch = True
        if "files" in local_files_data:
            if _find_version_match(remote_file_entry, local_files_data["files"]):
                do_fetch = False

        if do_fetch == False:
            continue

        entries_to_update.append(remote_file_entry)
        updates_available = True

    if updates_available == True:
        status = STATUS_UPDATES_AVAILABLE
    else:
        status = STATUS_UPDATED

def do_update():
    global status
    global file_being_downloaded

    for entry in entries_to_update:
        file_being_downloaded = entry["name"]
        status = STATUS_DOWNLOADING
        print("Going to fetch: ", entry["name"])
        _fetch_entry(entry)
        _move_entry(entry)
        _update_entry_to_local_data(entry)

    status = STATUS_UPDATED

def _update_entry_to_local_data(entry):
    local_files_data = _load_local_files_data()

    add_to_end = True

    if "files" in local_files_data:
        for local_entry in local_files_data["files"]:
            if local_entry["name"] == entry["name"]:
                local_entry["version"] = entry["version"]
                add_to_end = False

    if add_to_end:
        if "files" not in local_files_data:
            local_files_data["files"] = []
        local_files_data["files"].append(entry)

    f = open(path_finder.get_local_data_path(),'w')
    f.write(toml.dumps(local_files_data))
    f.flush()
    f.close()

def _move_entry(entry):
    target_dir = entry["target_dir"]

    if os.path.isfile(path_finder.get_path() + "/" + target_dir + "/" + entry["name"]):
        os.remove(path_finder.get_path() + "/" + target_dir + "/" + entry["name"])
    os.rename("tmp/" + entry["name"], path_finder.get_path() + "/" + target_dir + "/" + entry["name"])

def _fetch_entry(entry):
    url = entry["url"]

    target_dir = entry["target_dir"]

    if url[0] == '~':
        url = config.remote_data_file[:config.remote_data_file.rfind('/')+1] + url[1:]

    print (url)
    print (target_dir)

    response = urlopen(url)
    read_bytes, data = _chunk_read(response)

    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    f = open("tmp/" + entry["name"],'w')
    f.write(str(data))
    f.close()

def _find_version_match(entry_a, entries_b) -> bool:
    for entry_b in entries_b:
        if entry_a["name"] == entry_b["name"]:
            if entry_a["version"] == entry_b["version"]:
                return True

    return False

def _create_dummy_files_data_file():
    f = open(path_finder.get_local_data_path(),'w')
    print("Creating dummy file..")
    f.write('nwn_server_address = "' + config.nwn_server_address + '"\n\n')
    f.close()

def _load_local_files_data() -> dict:
    if os.path.isfile(path_finder.get_local_data_path()) != True:
        _create_dummy_files_data_file()

    with open(path_finder.get_local_data_path()) as local_data_file:
        data_as_dict = toml.load(local_data_file)
        return data_as_dict

def _load_remote_files_data() -> dict:
    response = urlopen(config.remote_data_file)
    read_bytes, data = _chunk_read(response)
    data_as_dict = toml.loads(data)

    return data_as_dict

def _chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent*100, 2)
    print("HI")
    print("Downloaded %d of %d bytes (%0.2f%%)\r" % 
        (bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
       sys.stdout.write('\n')

def _chunk_read(response, chunk_size=131072, report_hook=None):
    print(response.info())
    total_size = response.info().get('Content-Length')
    if (total_size):
        total_size = total_size.strip()
        total_size = int(total_size)
    else:
        total_size = 1
    bytes_so_far = 0

    data = None
 
    while 1:
       chunk = response.read(chunk_size)

       if bytes_so_far > 0:
          data += chunk
       else:
          data = chunk

       bytes_so_far += len(chunk)

       if not chunk:
          break

       if report_hook:
          report_hook(bytes_so_far, chunk_size, total_size)

    return (bytes_so_far, data)