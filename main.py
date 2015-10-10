#!/usr/bin/python
from threading import Thread

import path_finder
import config
import dependency_manager

config.load_config("config.toml")
path = path_finder.get_path()

t = Thread(target=dependency_manager.start_check, args=())
t.start()

import gui