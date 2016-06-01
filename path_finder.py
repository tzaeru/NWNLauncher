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

def get_nwn_path() -> str:
    global cached_path

    if cached_path == NO_PATH:
        cached_path = _resolve_path()

    return cached_path

def set_nwn_path(path : str):
    if _verify_path(path) is False:
        return

    global cached_path
    cached_path = path

def get_server_config_path() -> str:
    return os.path.join("./config", config.current_server)

def get_server_images_path() -> str:
    return os.path.join("./config", config.current_server, "images")

def get_executable_path() -> str:
    if platform.system() == "Windows":
        return os.path.join(get_nwn_path(), "nwmain.exe")
    else:
        return os.path.join(get_nwn_path(), "nwmain")

def get_config_path() -> str:
    return "./config";

def get_local_version_data_path() -> str:
    if not os.path.exists(os.path.join("./config", "file_info")):
        os.makedirs(os.path.join("./config", "file_info"))
    return os.path.join("./config", "file_info", config.local_versions_file)

def get_local_checksums_path() -> str:
    if not os.path.exists(os.path.join("./config", "file_info")):
        os.makedirs(os.path.join("./config", "file_info"))
    return os.path.join("./config", "file_info", config.local_checksums_file)

def get_cdkey_path() -> str:
    return os.path.join(get_nwn_path(), "nwncdkey.ini")

def get_nwnplayer_path() -> str:
    return os.path.join(get_nwn_path(), "nwnplayer.ini") 

def get_windows_hosts_path() -> str:
    return os.path.join("C:/Windows/System32/drivers/etc", "hosts") 

def get_logs_path() -> str:
    if platform.system() == "Windows":
        return os.path.join(get_nwn_path(), "logs")
    else:
        return None

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