#!/usr/bin/python
from threading import Thread

import path_finder
import config
import dependency_manager
import os
import platform

config.load_config("config")
path = path_finder.get_nwn_path()

if path is not path_finder.NO_PATH:
    t = Thread(target=dependency_manager.start_check, args=())
    t.start()

# Add hosts entry to skip NWN authentication.
def _add_skip_authentication():
    if platform.system() == "Windows":
        hosts = None

        with open(path_finder.get_windows_hosts_path()) as hosts_file:
            hosts = hosts_file.read()

            #Early bails to avoid writing twice to it
            if hosts.find("nwmaster") >= 0:
                return
            if hosts.find("NWN") >= 0:
                return

            hosts += "\n# NWN entry to skip authentication attempts to NWN master server\n"
            hosts += "0.0.0.0 nwmaster.bioware.com"
            hosts += "\n\n"
            
        if hosts is not None:
            f = open(path_finder.get_windows_hosts_path(),'w')
            f.write(hosts)
            f.flush()
            f.close()

_add_skip_authentication()

import gui