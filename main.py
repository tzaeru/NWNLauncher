#!/usr/bin/python
from threading import Thread

import path_finder
import config
import dependency_manager
import os, sys
import platform
import zipfile

if len(os.path.dirname(sys.argv[0])) > 0:
    os.chdir(os.path.dirname(sys.argv[0]))

print ('Number of arguments:', len(sys.argv), 'arguments.')
print ('Argument List:', str(sys.argv))

if len(sys.argv) > 1:
    filename, file_extension = os.path.splitext(str(sys.argv[1]))  
    if file_extension == ".nwnl":
        target_dir = os.path.join("./config", fislename)

        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        print("Extracting NWN server configuration set..")
        with zipfile.ZipFile(filename + file_extension, "r") as z:
            z.extractall(target_dir)

config.load_config("config")
path = path_finder.get_nwn_path()


if path is not path_finder.NO_PATH:
    t = Thread(target=dependency_manager.start_check, args=([True]))
    t.start()

import gui