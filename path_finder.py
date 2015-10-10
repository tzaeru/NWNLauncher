import platform
import os.path
import config

NO_PATH = "Neverwinter Nights directory could not be resolved. Please set it manually."

cached_path = NO_PATH

paths_for_windows = [
    "C:/NWN",
    "C:/NWN/NeverwinterNights",
    "C:/NeverwinterNights/",
    "C:/NeverwinterNights/NWN",
    "C:/Program Files/NWN",
    "C:/Program Files/NeverwinterNights",
    "C:/Program Files(x86)/NWN",
    "C:/Program Files(x86)/NeverwinterNights",
    "C:/Games/NWN",
    "C:/Games/NeverwinterNights",
]

def get_path() -> str:
    global cached_path

    if cached_path == NO_PATH:
        cached_path = _resolve_path()

    return cached_path

def set_path(path : str):
    global cached_path

    cached_path = path

def get_executable_path() -> str:
    if platform.system() == "Windows":
        return get_path() + "/nwmain.exe"
    else:
        return get_path() + "/nwmain"

def get_local_data_path() -> str:
    return get_path() + '/' + config.local_data_file

def _resolve_path() -> str:
    if platform.system() == "Windows":
        return _resolve_path_win32()
    else:
        print ("Automatic path resolvement for non-Windows systems isn't supported yet.")
        return NO_PATH

def _resolve_path_win32() -> str:
    for path in paths_for_windows:
        if os.path.isfile(path + "/nwmain.exe"):
            print("Found path, it is: ", path)
            return path

    return NO_PATH