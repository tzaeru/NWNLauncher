import platform
import os.path
import config
from winreg import *

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
    "C:/Program Files (x86)/GOG.com/Neverwinter Nights Diamond Edition/",
]

keys_for_windows = [
    r"SOFTWARE\BioWare\NWN\Neverwinter",
]

def get_path() -> str:
    global cached_path

    if cached_path == NO_PATH:
        cached_path = _resolve_path()

    return cached_path

def set_path(path : str):
    if _verify_path(path) is False:
        return

    global cached_path
    cached_path = path

def get_executable_path() -> str:
    if platform.system() == "Windows":
        return os.path.join(get_path(), "nwmain.exe")
    else:
        return os.path.join(get_path(), "nwmain")

def get_local_version_data_path() -> str:
    return os.path.join(get_path(), config.local_versions_file)

def get_local_checksums_path() -> str:
    return os.path.join(get_path(), config.local_checksums_file)

def _resolve_path() -> str:
    if platform.system() == "Windows":
        return _resolve_path_win32()
    else:
        print ("Automatic path resolvement for non-Windows systems isn't supported yet.")
        return NO_PATH

def _resolve_path_win32() -> str:
    resolved_path = NO_PATH

    resolved_path = _find_from_win32_registry()
    print(resolved_path)

    if resolved_path is not NO_PATH and _verify_path(resolved_path) is True:
        return resolved_path

    for path in paths_for_windows:
        if _verify_path(path):
            print("Found path, it is: ", path)
            return path

    return NO_PATH

def _verify_path(path : str) -> bool:
    if platform.system() == "Windows":
        return os.path.isfile(os.path.join(path, "nwmain.exe"))
    else:
        return os.path.isfile(os.path.join(path, "nwmain"))

def _find_from_win32_registry() -> str:
    registry = ConnectRegistry(None,HKEY_LOCAL_MACHINE)

    for key_string in keys_for_windows:
        try:
            key = OpenKey(registry, key_string)
            print("Found key: ", key_string)
            path_val = QueryValueEx(key, "Location")
            return path_val[0]
        except EnvironmentError:
            print("Key not found: ", key_string)

    return NO_PATH