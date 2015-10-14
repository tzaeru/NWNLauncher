#!/usr/bin/python
from threading import Thread

import path_finder
import config
import dependency_manager


config.load_config("config")
path = path_finder.get_nwn_path()

if path is not path_finder.NO_PATH:
    t = Thread(target=dependency_manager.start_check, args=())
    t.start()

import gui