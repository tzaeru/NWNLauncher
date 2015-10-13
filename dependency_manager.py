#!/usr/bin/python

import urllib, sys, os, hashlib, shutil
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

total_amount_of_updates = 0
total_size_of_updates = 0

do_quit = False

entries_to_update = []

def start_check():
    global entries_to_update
    global status
    global total_size_of_updates
    global total_amount_of_updates

    remote_files_data = _load_remote_files_data()
    local_files_data = _load_local_version_data()

    updates_available = False

    entries_to_update = []

    for remote_file_entry in remote_files_data["files"]:
        do_fetch = True
        if "files" in local_files_data:
            if _find_entry_checksum_match(remote_file_entry):
                do_fetch = False

        if do_fetch == False:
            continue

        if "size" in remote_file_entry:
            total_size_of_updates += float(remote_file_entry["size"])

        total_amount_of_updates += 1

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
        print("Checking if the following file already exists with corret checksum: ", entry["name"])
        _fetch_entry(entry)
        _validate_target_dir(entry)
        _move_entry(entry)
        _update_entry_to_local_data(entry)
        _update_checksum_entry(entry)

    status = STATUS_UPDATED

def _validate_target_dir(entry):
    target_dir = os.path.join(path_finder.get_path(), entry["target_dir"])

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

def _find_entry_checksum_match(entry) -> bool:
    file_path = os.path.join(path_finder.get_path(), entry["target_dir"])
    file_path = os.path.join(file_path, entry["name"])

    # Bail out early if the file doesn't even exist!
    if os.path.isfile(file_path) != True:
        return False

    local_checksum_data = _load_local_checksum_data()

    local_entry = None

    # Check if the entry exists in the local checksum data
    if "files" in local_checksum_data:
        for file_entry in local_checksum_data["files"]:
            if file_entry["name"] == entry["name"]:
                local_entry = file_entry
                break

    # If local entry doesn't exist, create it now
    if local_entry is None:
        local_entry = _update_checksum_entry(entry)
    print("Checksum entry: ", local_entry)
    print("Remote entry: ", entry)

    # Finally check for a matching checksum
    if local_entry["checksum"] == entry["checksum"]:
        return True
    return False

def _update_checksum_entry(entry):
    local_checksum_data = _load_local_checksum_data()

    file_path = os.path.join(path_finder.get_path(), entry["target_dir"])
    file_path = os.path.join(file_path, entry["name"])

    print("Doing checksum for: ", entry["name"])
    checksum = _generate_file_md5(file_path)

    print ("Checksum: ", checksum)

    checksum_entry = {}
    checksum_entry["name"] = entry["name"]
    checksum_entry["checksum"] = checksum

    existing_entry = None
    if "files" in local_checksum_data:
        for local_entry in local_checksum_data["files"]:
            if local_entry["name"] == checksum_entry["name"]:
                existing_entry = checksum_entry
    else:
        local_checksum_data["files"] = []

    if existing_entry:
        existing_entry = checksum_entry
    else:
        local_checksum_data["files"].append(checksum_entry)

    f = open(path_finder.get_local_checksums_path(),'w')
    f.write(toml.dumps(local_checksum_data))
    f.flush()
    f.close()

    return checksum_entry

def _generate_file_md5(path, blocksize=2**20):
    m = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update( buf )
    return m.hexdigest()

def _update_entry_to_local_data(entry):
    local_files_data = _load_local_version_data()

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

    f = open(path_finder.get_local_version_data_path(),'w')
    f.write(toml.dumps(local_files_data))
    f.flush()
    f.close()

def _move_entry(entry):
    target_dir = entry["target_dir"]

    src_path = os.path.join("tmp", entry["name"])

    dst_path = os.path.join(path_finder.get_path(), target_dir)
    dst_path = os.path.join(dst_path, entry["name"])

    if os.path.isfile(dst_path):
        os.remove(dst_path)

    shutil.move(src_path,dst_path)

def _fetch_entry(entry):
    url = entry["url"]

    target_dir = entry["target_dir"]

    if url[0] == '~':
        url = config.remote_data_file[:config.remote_data_file.rfind('/')+1] + url[1:]

    print (url)
    print (target_dir)

    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    f = open("tmp/" + entry["name"],'wb')

    response = urlopen(url)
    read_bytes = _chunk_read(response, f, report_hook=_chunk_report)

    f.close()

def _find_version_match(entry_a, entries_b) -> bool:
    for entry_b in entries_b:
        if entry_a["name"] == entry_b["name"]:
            if entry_a["version"] == entry_b["version"]:
                return True

    return False

def _create_dummy_checksum_data_file():
    f = open(path_finder.get_local_checksums_path(),'w')
    print("Creating dummy checksum data file..")
    f.close()

def _create_dummy_version_data_file():
    f = open(path_finder.get_local_version_data_path(),'w')
    print("Creating dummy version data file..")
    f.write('nwn_server_address = "' + config.nwn_server_address + '"\n\n')
    f.close()

def _load_local_checksum_data() -> dict:
    if os.path.isfile(path_finder.get_local_checksums_path()) != True:
        _create_dummy_checksum_data_file()

    with open(path_finder.get_local_checksums_path()) as local_checksums_file:
        data_as_dict = toml.load(local_checksums_file)
        return data_as_dict

def _load_local_version_data() -> dict:
    if os.path.isfile(path_finder.get_local_version_data_path()) != True:
        _create_dummy_version_data_file()

    with open(path_finder.get_local_version_data_path()) as local_version_data_file:
        data_as_dict = toml.load(local_version_data_file)
        return data_as_dict

def _load_remote_files_data() -> dict:
    response = urlopen(config.remote_data_file)
    data = response.read()
    data_as_dict = toml.loads(data)

    return data_as_dict

def _chunk_report(bytes_so_far, chunk_size, total_size):
    global current_file_progress

    current_file_progress = float(bytes_so_far) / total_size

def _chunk_read(response, file_to_write_to, chunk_size=2**20, report_hook=None):
    print(response.info())
    total_size = response.info().get('Content-Length')
    if (total_size):
        total_size = total_size.strip()
        total_size = int(total_size)
    else:
        total_size = 1
    bytes_so_far = 0
 
    global total_progress

    while 1 and do_quit is False:
       chunk = response.read(chunk_size)

       file_to_write_to.write(chunk)

       bytes_so_far += len(chunk)
       
       total_progress += float(len(chunk)) / total_size_of_updates

       if not chunk:
          break

       if report_hook:
          report_hook(bytes_so_far, chunk_size, total_size)
    
    return bytes_so_far